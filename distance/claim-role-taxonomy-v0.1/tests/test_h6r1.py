"""Offline engineering fixtures only. No provider calls or scientific observations."""
from copy import deepcopy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

H = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(H))
spec = importlib.util.spec_from_file_location('h6r1_runner', H / 'runner.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
c = r.c


class Contracts(unittest.TestCase):
    def setUp(self):
        self.t = r.read(H / 'taxonomy.json')
        self.uid = 'H6-T02-2/C001'
        self.claim = r.read(H / 'selection/claims.json')[self.uid]
        self.evidence = r.read(H / 'selection/evidence.json')[self.uid]
        self.packet = c.role_packet(self.claim, self.evidence)
        self.a = {'claim_id': self.uid, 'atomicity': 'ATOMIC', 'assignment_status': 'ASSIGNED',
                  'primary_role': 'SUPPLIED_FACT', 'competing_roles': [],
                  'role_provenance': [{'source_type': 'TARGET', 'source_id': 'T02'}],
                  'rationale': 'Engineering fixture'}

    def validate(self, a):
        return c.validate('role', a, self.packet, r.read(H / 'schemas/role.schema.json'), self.t)

    def test_all_status_combinations(self):
        for atomic in ('ATOMIC', 'SPLIT_REQUIRED'):
            for status in ('ASSIGNED', 'ROLE_UNCERTAIN', 'ATOMIZATION_DEFECT'):
                for role in (None, 'SUPPLIED_FACT'):
                    for competing in ([], ['SUPPLIED_FACT', 'LIMIT']):
                        a = {**self.a, 'atomicity': atomic, 'assignment_status': status,
                             'primary_role': role, 'competing_roles': competing}
                        permitted = (atomic, status, role, bool(competing)) in (
                            ('ATOMIC', 'ASSIGNED', 'SUPPLIED_FACT', False),
                            ('ATOMIC', 'ROLE_UNCERTAIN', None, True),
                            ('SPLIT_REQUIRED', 'ATOMIZATION_DEFECT', None, False))
                        if permitted:
                            self.validate(a)
                        else:
                            with self.assertRaises(ValueError):
                                self.validate(a)

    def test_uncertain_needs_distinct_competitors(self):
        a = {**self.a, 'assignment_status': 'ROLE_UNCERTAIN', 'primary_role': None,
             'competing_roles': ['LIMIT', 'LIMIT']}
        with self.assertRaises(Exception):
            self.validate(a)

    def test_no_eighth_role_or_extra_fields(self):
        for change in ({'primary_role': 'UNCERTAIN'}, {'old_status': 'SUPPORTED'}):
            with self.assertRaises(Exception):
                self.validate({**self.a, **change})

    def test_all_routes_and_verdicts(self):
        for role, contract in self.t['routing'].items():
            assignment = {**self.a, 'primary_role': role}
            p = c.evaluation_packet(self.claim, self.evidence, assignment, self.t)
            self.assertEqual(p['contract_question'], self.t['contracts'][contract])
            for verdict in self.t['verdicts']:
                b = {'claim_id': self.uid, 'frozen_role': role, 'contract_id': contract,
                     'verdict': verdict, 'evaluation_provenance': [],
                     'unresolved_conditions': ['Condition'] if verdict == 'CONDITIONAL' else [],
                     'rationale': 'Fixture fails or satisfies only its own contract'}
                c.validate('evaluation', b, p, r.read(H / 'schemas/evaluation.schema.json'), self.t)
                # VIOLATED must remain representable for every role, including inferences.
                wrong = {**b, 'contract_id': 'SOURCE_FIDELITY' if contract != 'SOURCE_FIDELITY'
                         else 'TARGET_FIDELITY'}
                with self.assertRaises(ValueError):
                    c.validate('evaluation', wrong, p, r.read(H / 'schemas/evaluation.schema.json'), self.t)

    def test_role_cannot_be_changed_even_with_matching_other_contract(self):
        p = c.evaluation_packet(self.claim, self.evidence, self.a, self.t)
        b = {'claim_id': self.uid, 'frozen_role': 'DERIVED_INFERENCE', 'contract_id': 'DERIVED_WARRANT',
             'verdict': 'VIOLATED', 'evaluation_provenance': [], 'unresolved_conditions': [],
             'rationale': 'Wrong role fixture'}
        with self.assertRaisesRegex(ValueError, 'Frozen role changed'):
            c.validate('evaluation', b, p, r.read(H / 'schemas/evaluation.schema.json'), self.t)

    def test_conditional_needs_explicit_condition(self):
        p = c.evaluation_packet(self.claim, self.evidence, self.a, self.t)
        b = {'claim_id': self.uid, 'frozen_role': 'SUPPLIED_FACT', 'contract_id': 'TARGET_FIDELITY',
             'verdict': 'CONDITIONAL', 'evaluation_provenance': [], 'unresolved_conditions': [],
             'rationale': 'Fixture'}
        with self.assertRaises(ValueError):
            c.validate('evaluation', b, p, r.read(H / 'schemas/evaluation.schema.json'), self.t)

    def test_identity_and_namespaces(self):
        with self.assertRaises(ValueError):
            self.validate({**self.a, 'claim_id': 'H6-T04-1/C001'})
        a = {**self.a, 'role_provenance': [{'source_type': 'TARGET', 'source_id': 'P001'}]}
        original = deepcopy(a)
        self.assertEqual(self.validate(a)[0]['code'], 'PROV_UNKNOWN_SOURCE_ID')
        self.assertEqual(a, original)  # diagnostics do not repair observations

    def test_blinded_packet_allowlist(self):
        poisoned = {**self.claim, 'old_status': 'UNSUPPORTED', 'operator_role': 'LIMIT',
                    'rationale': 'selection reason', 'terminal_audit': 'SECRET_SENTINEL'}
        p = c.role_packet(poisoned, self.evidence)
        self.assertEqual(p, self.packet)
        self.assertNotIn('contract_id', p)
        self.assertNotIn('SECRET_SENTINEL', json.dumps(p))
        for key in ('support_status', 'rationale', 'intended_role', 'selection_reason'):
            self.assertNotIn('"' + key + '"', json.dumps(p))

    def test_fidelity_evidence_projection(self):
        p = c.evaluation_packet(self.claim, self.evidence, self.a, self.t)
        self.assertIn('target', p)
        self.assertNotIn('source_instrument', p)
        self.assertNotIn('mapping', p)
        self.assertNotIn('mapping_refs', p['claim'])
        p = c.evaluation_packet(self.claim, self.evidence, {**self.a, 'primary_role': 'SOURCE_FACT'}, self.t)
        self.assertIn('source_instrument', p)
        self.assertNotIn('target', p)
        self.assertNotIn('mapping', p)
        self.assertNotIn('rationale', p)

    def test_mapping_evidence_is_fixed_and_local(self):
        p = c.evaluation_packet(self.claim, self.evidence, {**self.a, 'primary_role': 'OPERATION'}, self.t)
        self.assertEqual(set(p['mapping']['spans']), set(self.evidence['evaluation_mapping_ids']))
        self.assertEqual(p['mapping']['packet_id'], self.claim['packet_id'])

    def test_no_uncertain_or_defective_evaluation(self):
        for status, atomic in [('ROLE_UNCERTAIN', 'ATOMIC'), ('ATOMIZATION_DEFECT', 'SPLIT_REQUIRED')]:
            with self.assertRaises(ValueError):
                c.evaluation_packet(self.claim, self.evidence,
                    {**self.a, 'assignment_status': status, 'atomicity': atomic, 'primary_role': None}, self.t)

    def test_original_claims_preserved_and_anchors_present(self):
        m = r.manifest()
        claims = r.read(H / 'selection/claims.json')
        self.assertEqual(len(claims), 24)
        self.assertLessEqual(len(claims), m['max_selected_claims'])
        self.assertTrue(set(m['mandatory_anchor_ids']) <= set(claims))
        for uid, selected in claims.items():
            pid, cid = uid.split('/')
            old = next(x for x in r.read(r.OLD / 'claims' / (pid + '.json'))['claims'] if x['claim_id'] == cid)
            self.assertEqual(selected['value'], old['component']['value'])
            self.assertEqual(selected['scope'], old['component']['scope'])
            self.assertEqual(selected['mapping_refs'], old['component']['provenance']['refs'])


class Execution(unittest.TestCase):
    def test_freeze_required_before_stage_b_or_comparison(self):
        with patch.object(r, 'require_freeze', side_effect=ValueError('no freeze')):
            with self.assertRaises(ValueError):
                r.ids('evaluation')
            with patch.object(r, 'verify'):
                with self.assertRaises(ValueError):
                    r.compare()

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"claim_id":"a","claim_id":"b"}', object_pairs_hook=r.unique)

    def test_hash_tampering_detected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'input.json'
            p.write_text('{}')
            with patch.object(r, 'R', Path(d)):
                before = {'input.json': r.sha(p)}
                r.hashes(before)
                p.write_text('{"changed":true}')
                with self.assertRaisesRegex(ValueError, 'Frozen hash'):
                    r.hashes(before)

    def test_provider_event_audit(self):
        response = '{}'
        events = [{'type': 'thread.started', 'thread_id': 'fresh'},
                  {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': response}},
                  {'type': 'turn.completed', 'usage': {'input_tokens': 1}}]
        self.assertEqual(r.audit_events(events, response)['session_id'], 'fresh')
        for extra in ({'type': 'error'}, {'model': 'substituted'}, {'fallback': True},
                      {'item': {'type': 'command_execution'}}):
            with self.assertRaises(ValueError):
                r.audit_events(events + [extra], response)
        with self.assertRaises(ValueError):
            r.audit_events(events, '{"changed":true}')

    def test_isolation_command(self):
        cmd = r.command('role', Path('/tmp/empty'), Path('/tmp/out'))
        for flag in ('--ignore-user-config', '--ignore-rules', '--ephemeral', '--sandbox'):
            self.assertIn(flag, cmd)
        self.assertEqual(cmd[cmd.index('--model') + 1], 'gpt-6-astra')
        self.assertIn('model_reasoning_effort="high"', cmd)
        self.assertEqual(cmd[cmd.index('--cd') + 1], '/tmp/empty')

    def test_budget_denial_dominates_provider_launch(self):
        uid = 'H6-T02-2/C001'
        packet = r.build_packet('role', uid)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'p.json'; p.write_text(json.dumps(packet))
            txt = Path(d) / 'p.txt'; txt.write_bytes(r.prompt('role', packet))
            gate = Mock(); gate.reserve.side_effect = r.budget.BudgetError('denied')
            with patch.object(r, 'RT', Path(d) / 'runtime'), patch.object(r, 'verify'), \
                 patch.object(r, 'active_batch'), \
                 patch.object(r, 'binary_check'), patch.object(r, 'packet_path',
                 side_effect=lambda stage, uid, suffix='json': p if suffix == 'json' else txt), \
                 patch.object(r.subprocess, 'Popen') as launch:
                with self.assertRaises(r.budget.BudgetError):
                    r.run_one('role', uid, {'experiment_id': 'fixture'}, gate)
                launch.assert_not_called()
                gate.reserve.assert_called_once()

    def test_failed_provider_attempt_is_preserved_without_retry(self):
        uid = 'H6-T02-2/C001'; packet = r.build_packet('role', uid)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p = root / 'p.json'; p.write_text(json.dumps(packet))
            txt = root / 'p.txt'; txt.write_bytes(r.prompt('role', packet))
            gate = Mock()
            def fail(*args, **kwargs):
                gate.reserve.assert_called_once()
                raise OSError('mock transport unavailable')
            with patch.object(r, 'RT', root / 'runtime'), patch.object(r, 'verify'), \
                 patch.object(r, 'active_batch'), \
                 patch.object(r, 'head', return_value='offline-fixture'), \
                 patch.object(r, 'binary_check'), patch.object(r, 'packet_path',
                 side_effect=lambda stage, uid, suffix='json': p if suffix == 'json' else txt), \
                 patch.object(r.subprocess, 'Popen', side_effect=fail) as launch:
                with self.assertRaises(OSError):
                    r.run_one('role', uid, {'experiment_id': 'fixture'}, gate)
                dest = root / 'runtime/attempts/role' / r.stem(uid)
                self.assertTrue((dest / 'failure.json').exists())
                self.assertTrue((dest / 'request.txt').exists())
                with self.assertRaisesRegex(ValueError, 'no retry'):
                    r.run_one('role', uid, {'experiment_id': 'fixture'}, gate)
                self.assertEqual(launch.call_count, 1)

    def test_successful_attempt_preserves_raw_and_reserves_once(self):
        uid = 'H6-T02-2/C001'; packet = r.build_packet('role', uid)
        answer = {'claim_id': uid, 'atomicity': 'ATOMIC', 'assignment_status': 'ASSIGNED',
                  'primary_role': 'SUPPLIED_FACT', 'competing_roles': [],
                  'role_provenance': [{'source_type': 'TARGET', 'source_id': 'T02'}],
                  'rationale': 'Offline engineering fixture; never a scientific observation'}
        response = json.dumps(answer)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p = root / 'p.json'; p.write_text(json.dumps(packet))
            txt = root / 'p.txt'; txt.write_bytes(r.prompt('role', packet))
            gate = Mock()
            class FakeProcess:
                pid = 999999999
                returncode = 0
                def __init__(self, cmd, **kwargs):
                    gate.reserve.assert_called_once()
                    self.out = kwargs['stdout']
                    self.response_path = Path(cmd[cmd.index('--output-last-message') + 1])
                def communicate(self, request, timeout):
                    r.raw(self.response_path, response.encode())
                    for event in [{'type': 'thread.started', 'thread_id': 'offline-fixture-session'},
                                  {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': response}},
                                  {'type': 'turn.completed', 'usage': {'input_tokens': 1, 'output_tokens': 1}}]:
                        self.out.write((json.dumps(event) + '\n').encode())
                def poll(self):
                    return 0
            with patch.object(r, 'RT', root / 'runtime'), patch.object(r, 'verify'), \
                 patch.object(r, 'active_batch'), patch.object(r, 'head', return_value='offline-fixture'), \
                 patch.object(r, 'binary_check'), patch.object(r, 'judgment', return_value=root / 'judgment.json'), \
                 patch.object(r, 'packet_path', side_effect=lambda stage, uid, suffix='json':
                              p if suffix == 'json' else txt), \
                 patch.object(r.subprocess, 'Popen', side_effect=FakeProcess) as launch:
                metadata = r.run_one('role', uid, {'experiment_id': 'fixture'}, gate)
                self.assertEqual(metadata['session_id'], 'offline-fixture-session')
                self.assertEqual(r.read(root / 'judgment.json'), answer)
                dest = root / 'runtime/attempts/role' / r.stem(uid)
                self.assertEqual((dest / 'response.json').read_text(), response)
                self.assertTrue(r.read(dest / 'validation.json')['schema_valid'])
                gate.finish.assert_called_once_with('fixture', 'role:' + uid, 0)
                self.assertEqual(launch.call_count, 1)

    def test_batch_size_and_pause_block_scheduling(self):
        for count in (0, 4):
            with self.assertRaises(ValueError):
                r.run_batch('role', Path('/unused'), count, None)
        for state in ('PAUSED_EVENT', 'PAUSED_INTEGRITY', 'RUNNING'):
            with patch.object(r, 'latest_state', return_value={'state': state}):
                with self.assertRaises(ValueError):
                    r.scheduling_clear()

    def test_dispatch_requires_active_batch(self):
        for state in (None, {'state': 'PAUSED_EVENT'}, {'state': 'BATCH_COMPLETE'}):
            with patch.object(r, 'latest_state', return_value=state):
                with self.assertRaises(ValueError):
                    r.active_batch('role', 'H6-T02-2/C001')

    def test_incomplete_stage_cannot_freeze(self):
        with patch.object(r, 'scheduling_clear'), patch.object(r, 'verify'):
            with self.assertRaisesRegex(ValueError, 'incomplete'):
                r.freeze('role')

    def test_no_automatic_usage_approval(self):
        report = {'approval_required': True, 'report_sha256': 'report'}
        with self.assertRaises(ValueError):
            r.approve_usage_check(report, {}, None, 'role', 3)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'review.json'
            r.write(p, {'plan_sha256': r.budget.digest({}), 'report_sha256': 'different',
                        'stage': 'role', 'max_sessions': 3, 'user_message_reference': 'fixture only'})
            with self.assertRaises(ValueError):
                r.approve_usage_check(report, {}, p, 'role', 3)

    def test_stale_snapshot_blocks_even_with_consent(self):
        plan = {'stages': [{'id': 'role', 'sessions': 24, 'usage_profile': 'fixture'}]}
        snapshot = {'version': 1, 'captured_at': '2020-01-01T00:00:00+00:00',
                    'account_scope': 'fixture', 'available_reset_credits': 0,
                    'reset_credit_expirations': [], 'windows': [
                        {'bucket': 'test', 'slot': 'primary', 'plan_type': 'test',
                         'duration_minutes': 300, 'used_percent': 0, 'resets_at': 9999999999}]}
        cal = {'version': 1, 'samples': []}
        report = r.usage.predict(plan, snapshot, cal, as_of=r.usage.epoch(r.now()))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            for name, obj in [('before', snapshot), ('calibration', cal),
                              ('usage-plan', plan), ('usage-report', report)]:
                r.write(p / (name + '.json'), obj)
            with patch.object(r, 'remaining_plan', return_value=plan), \
                 patch.object(r, 'approve_usage_check') as approve:
                with self.assertRaisesRegex(ValueError, 'Fresh'):
                    r.usage_check(p, plan, 'role', 3, Path('/unused'))
                approve.assert_not_called()


if __name__ == '__main__':
    unittest.main()
