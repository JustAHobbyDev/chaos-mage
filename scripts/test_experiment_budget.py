import copy
from contextlib import redirect_stderr
from datetime import datetime, timezone
import time
from concurrent.futures import ThreadPoolExecutor
import json
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from experiment_budget import BudgetError, Gate, forecast, launch, main


def snapshot(remaining):
    return {'version': 1, 'captured_at': datetime.now(timezone.utc).isoformat(),
            'account_scope': 'offline-test', 'available_reset_credits': 0,
            'reset_credit_expirations': [], 'windows': [{'bucket': 'codex', 'slot': 'primary',
            'plan_type': 'test', 'duration_minutes': 10080, 'used_percent': 100 - remaining,
            'resets_at': time.time() + 10000}]}


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
        self.allowance = snapshot(80)
        self.gate = Gate(self.path / 'ledger.sqlite3', usage_reader=lambda: self.allowance)
        self.policy = {'version': 1, 'approval_above_usd': '10', 'approval_above_sessions': 100}
        self.plan = {
            'version': 1, 'experiment_id': 'test-study', 'description': 'Offline test',
            'execution_fingerprint': 'test-runner-and-input-hash', 'execution_allowed': True,
            'stages': [{'id': 'generation', 'sessions': 2, 'estimated_cost_usd': '2',
                        'estimate_basis': 'Offline test values, not provider pricing'}],
        }

    def reserve(self, session, stage='generation', gate=None):
        (gate or self.gate).reserve(self.plan, self.policy, stage, session, ['offline-test'])

    def test_thresholds_are_cumulative_and_equality_is_allowed(self):
        self.plan['stages'][0]['estimated_cost_usd'] = '6'
        self.plan['stages'].append({'id': 'evaluation', 'sessions': 98,
                                   'estimated_cost_usd': '4', 'estimate_basis': 'test'})
        self.assertFalse(forecast(self.plan, self.policy)['approval_required'])
        self.plan['stages'][1]['estimated_cost_usd'] = '4.01'
        self.assertFalse(forecast(self.plan, self.policy)['approval_required'])
        self.assertTrue(forecast(self.plan, self.policy)['advisories'])
        self.plan['stages'][1]['estimated_cost_usd'] = '4'
        self.plan['stages'][1]['sessions'] = 99
        self.assertFalse(forecast(self.plan, self.policy)['approval_required'])
        self.assertTrue(forecast(self.plan, self.policy)['advisories'])

    def test_unknown_cost_does_not_require_approval_above_usage_threshold(self):
        self.plan['stages'][0]['estimated_cost_usd'] = None
        with patch('experiment_budget.subprocess.run') as run:
            run.return_value.returncode = 0
            self.assertEqual(launch(self.gate, self.plan, self.policy, 'generation', '1', ['test']), 0)
            run.assert_called_once()

    def test_each_reservation_checks_current_allowance(self):
        self.reserve('1')
        self.allowance = snapshot(29)
        with self.assertRaisesRegex(BudgetError, 'remaining usage is below 30%'):
            self.reserve('2')
        self.allowance = snapshot(30)
        self.reserve('2')
        with self.gate.connect() as db:
            rows = db.execute("SELECT details FROM audit WHERE event='RESERVED' ORDER BY sequence").fetchall()
        self.assertEqual([json.loads(row['details'])['usage_gate']['windows'][0]['remaining_percent']
                          for row in rows], [80, 30])

    def test_real_denied_process_has_no_side_effects(self):
        sentinel = self.path / 'SHOULD_NOT_EXIST'
        self.plan['stages'][0]['estimated_cost_usd'] = '11'
        quota_path = self.path / 'usage.json'
        quota_path.write_text(json.dumps(snapshot(29)))
        plan_path, policy_path = self.path / 'plan.json', self.path / 'policy.json'
        plan_path.write_text(json.dumps(self.plan))
        policy_path.write_text(json.dumps(self.policy))
        result = subprocess.run([
            sys.executable, '-B', str(Path(__file__).with_name('experiment_budget.py')),
            '--ledger', str(self.gate.path), '--policy', str(policy_path),
            '--usage-snapshot', str(quota_path), 'launch',
            '--plan', str(plan_path), '--stage', 'generation', '--session', 'sentinel', '--',
            sys.executable, '-c', 'from pathlib import Path; Path(' + repr(str(sentinel)) + ').touch()',
        ], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('remaining usage is below 30%', result.stderr)
        self.assertFalse(sentinel.exists())

    def test_unknown_workload_approval_cannot_dispatch_unknown_stage(self):
        self.plan['stages'][0]['sessions'] = None
        self.gate.approve(self.plan, self.policy, 'test-only authorization')
        with self.assertRaisesRegex(BudgetError, 'Resolve this stage'):
            self.reserve('1')

    def test_below_threshold_approval_is_bound_to_full_plan_and_policy(self):
        self.allowance = snapshot(29)
        self.plan['stages'][0]['estimated_cost_usd'] = '20'
        self.gate.approve(self.plan, self.policy, 'test-only authorization')
        self.reserve('1')
        original = copy.deepcopy(self.plan)
        self.plan['stages'][0]['sessions'] = 3
        with self.assertRaises(BudgetError):
            self.reserve('2')
        self.plan = original
        self.policy['approval_above_usd'] = '5'
        with self.assertRaises(BudgetError):
            self.reserve('2')
        self.allowance = snapshot(30)
        self.reserve('2')

    def test_failed_launches_and_restart_do_not_refund_slots(self):
        self.reserve('1')
        self.gate.finish('test-study', '1', 1)
        restarted = Gate(self.gate.path, usage_reader=lambda: self.allowance)
        self.reserve('2', gate=restarted)  # crash leaves RESERVED indefinitely
        with self.assertRaisesRegex(BudgetError, 'session limit'):
            self.reserve('3', gate=restarted)
        self.assertEqual(restarted.status(self.plan, self.policy)['reserved_sessions'], 2)

    def test_duplicate_session_is_not_retried(self):
        self.reserve('1')
        with self.assertRaisesRegex(BudgetError, 'already reserved'):
            self.reserve('1')

    def test_concurrent_workers_cannot_oversubscribe(self):
        self.plan['stages'][0]['sessions'] = 1
        def worker(i):
            try:
                self.reserve(str(i), gate=Gate(self.gate.path, usage_reader=lambda: self.allowance))
                return True
            except BudgetError:
                return False
        with ThreadPoolExecutor(max_workers=8) as pool:
            self.assertEqual(sum(pool.map(worker, range(12))), 1)

    def test_observed_overrun_is_advisory_above_usage_threshold(self):
        self.reserve('1')
        self.gate.observe_cost('test-study', '1', '3')
        report = self.gate.status(self.plan, self.policy)
        self.assertTrue(report['allowed'])
        self.assertTrue(any('Observed cost exceeds' in x for x in report['advisories']))
        self.plan['stages'][0]['estimated_cost_usd'] = '12'
        self.reserve('2')

    def test_only_strict_below_thirty_requires_approval(self):
        self.plan['stages'][0]['estimated_cost_usd'] = None
        for remaining, required in [(29.99, True), (30, False), (30.01, False)]:
            self.allowance = snapshot(remaining)
            report = self.gate.status(self.plan, self.policy)
            self.assertEqual(report['approval_required'], required)
            self.assertEqual(report['allowed'], not required)

    def test_unknown_future_fanout_does_not_block_known_stage(self):
        self.plan['stages'].append({'id': 'future', 'sessions': None, 'estimated_cost_usd': None})
        self.reserve('1')
        with self.assertRaisesRegex(BudgetError, 'Resolve this stage'):
            self.reserve('2', stage='future')

    def test_stale_account_cannot_be_approved_away(self):
        self.allowance['captured_at'] = '2000-01-01T00:00:00+00:00'
        self.gate.approve(self.plan, self.policy, 'test-only authorization')
        report = self.gate.status(self.plan, self.policy)
        self.assertTrue(report['refresh_required'])
        self.assertFalse(report['approval_required'])
        self.assertFalse(report['allowed'])

    def test_no_cost_refund_or_missing_observation(self):
        self.reserve('1')
        self.gate.observe_cost('test-study', '1', '2')
        with self.assertRaises(BudgetError):
            self.gate.observe_cost('test-study', '1', '1')
        with self.assertRaises(BudgetError):
            self.gate.observe_cost('test-study', 'missing', '1')

    def test_block_is_independent_of_budget_approval(self):
        self.gate.block('test-study', 'Terminal scientific stop')
        self.gate.approve(self.plan, self.policy, 'test-only authorization')
        with self.assertRaisesRegex(BudgetError, 'Terminal scientific stop'):
            self.reserve('1')

    def test_removed_or_shrunk_consumed_stage_denies(self):
        self.reserve('1')
        self.plan['stages'][0]['sessions'] = 0
        with self.assertRaisesRegex(BudgetError, 'shrinks'):
            self.reserve('2')
        self.plan['stages'][0]['id'] = 'renamed'
        with self.assertRaisesRegex(BudgetError, 'omits'):
            self.reserve('2', 'renamed')

    def test_invalid_estimates_fail_closed(self):
        for value in ('NaN', 'Infinity', '-1', True, {}, 'unknown'):
            with self.subTest(value=value):
                self.plan['stages'][0]['estimated_cost_usd'] = value
                with self.assertRaises(BudgetError):
                    forecast(self.plan, self.policy)
        self.plan['stages'][0]['estimated_cost_usd'] = '1'
        for value in (-1, 1.5, True):
            self.plan['stages'][0]['sessions'] = value
            with self.assertRaises(BudgetError):
                forecast(self.plan, self.policy)

    def test_pipe_cannot_approve(self):
        plan, policy = self.path / 'plan.json', self.path / 'policy.json'
        plan.write_text(json.dumps(self.plan))
        policy.write_text(json.dumps(self.policy))
        quota_path = self.path / 'quota.json'
        quota_path.write_text(json.dumps(self.allowance))
        with patch('sys.stdin.isatty', return_value=False), redirect_stderr(io.StringIO()):
            self.assertEqual(main(['--ledger', str(self.gate.path), '--policy', str(policy),
                                   '--usage-snapshot', str(quota_path),
                                   'approve', '--plan', str(plan), '--reference', 'test']), 1)
        self.assertIsNone(self.gate.status(self.plan, self.policy)['approval_reference'])

    def test_forecast_only_example_never_launches(self):
        self.plan['execution_allowed'] = False
        self.gate.approve(self.plan, self.policy, 'test-only authorization')
        with self.assertRaisesRegex(BudgetError, 'Forecast-only'):
            self.reserve('1')

    def test_successful_offline_command_records_exit(self):
        self.assertEqual(launch(self.gate, self.plan, self.policy, 'generation', '1',
                                [sys.executable, '-c', 'pass']), 0)
        with self.gate.connect() as db:
            row = db.execute('SELECT state,returncode FROM reservations').fetchone()
            self.assertEqual(tuple(row), ('FINISHED', 0))

    def test_fractional_allowance_does_not_create_rounding_overrun(self):
        self.plan['stages'][0]['sessions'] = 3
        self.plan['stages'][0]['estimated_cost_usd'] = '1'
        for sid in ('1', '2', '3'):
            self.reserve(sid)
        self.assertTrue(self.gate.status(self.plan, self.policy)['allowed'])

    def test_unknown_cost_approval_still_enforces_session_quota(self):
        self.plan['stages'][0]['estimated_cost_usd'] = None
        self.gate.approve(self.plan, self.policy, 'test-only unknown-cost authorization')
        self.reserve('1')
        self.reserve('2')
        with self.assertRaisesRegex(BudgetError, 'session limit'):
            self.reserve('3')


if __name__ == '__main__':
    unittest.main()
