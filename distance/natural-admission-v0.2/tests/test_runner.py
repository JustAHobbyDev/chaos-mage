"""Offline boundary tests; no provider observations or calibration."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

H = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('h7_runner', H / 'runner.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class BoundaryTests(unittest.TestCase):
    def test_budget_denial_never_launches(self):
        gate, launch = Mock(), Mock()
        gate.reserve.side_effect = r.budget.BudgetError('denied')
        with self.assertRaises(r.budget.BudgetError):
            r.reserve_and_launch(gate, {}, {}, 'generation', 'slot', ['provider'], launch)
        launch.assert_not_called()

    def test_actual_gate_preserves_slot_on_failed_transport(self):
        with tempfile.TemporaryDirectory() as tmp:
            gate = r.budget.Gate(Path(tmp) / 'ledger.db')
            plan = {'version': 1, 'experiment_id': 'offline-test', 'description': 'fixture',
                    'execution_fingerprint': 'fixture', 'execution_allowed': True,
                    'stages': [{'id': 'generation', 'sessions': 1,
                                'estimated_cost_usd': '1', 'estimate_basis': 'offline fixture'}]}
            policy = {'version': 1, 'approval_above_usd': '10', 'approval_above_sessions': 100}
            launch = Mock(side_effect=RuntimeError('transport'))
            with self.assertRaises(RuntimeError):
                r.reserve_and_launch(gate, plan, policy, 'generation', 'slot', ['fixture'], launch)
            with self.assertRaises(r.budget.BudgetError):
                r.reserve_and_launch(gate, plan, policy, 'generation', 'slot', ['fixture'], launch)
            self.assertEqual(launch.call_count, 1)
            self.assertEqual(gate.status(plan, policy)['reserved_sessions'], 1)

    def test_unknown_citation_fails_without_role_requirement(self):
        value = {'packet_id': 'M', 'claims': [{'claim_id': 'C001', 'fields': ['state'],
                  'proposition': 'Fixture', 'evidence_used': [{'source_id': 'P001'}]}],
                 'coverage': [{'field': f, 'claim_ids': ['C001'] if f == 'state' else [],
                               'unrepresented_material': []}
                              for f in ['state', 'operation', 'signal', 'inference', 'limit']]}
        packet = {'packet_id': 'M', 'allowed_source_ids': ['P001']}
        r.validate_claims(value, packet)
        value['claims'][0]['evidence_used'][0]['source_id'] = 'P999'
        with self.assertRaisesRegex(ValueError, 'RESPONSE_SOURCE_UNKNOWN'):
            r.validate_claims(value, packet)

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"instrument":1,"instrument":2}', object_pairs_hook=r.unique)

    def test_tool_or_substitution_cannot_be_clean(self):
        events = [{'type': 'thread.started', 'thread_id': 'fixture'},
                  {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': '{}'}},
                  {'type': 'turn.completed'}]
        self.assertEqual(r.audit(events, '{}')['session_id'], 'fixture')
        events.append({'type': 'item.completed', 'item': {'type': 'command_execution'}})
        with self.assertRaisesRegex(ValueError, 'Tool activity'):
            r.audit(events, '{}')
        events.pop()
        events.append({'model': 'different-model'})
        with self.assertRaisesRegex(ValueError, 'Model substitution'):
            r.audit(events, '{}')

    def test_isolated_command_has_no_resume(self):
        cmd = r.command('/tmp/fixture', Path('/tmp/fixture-out'), 'generation')
        for flag in ['--ephemeral', '--ignore-user-config', '--ignore-rules']:
            self.assertIn(flag, cmd)
        self.assertNotIn('resume', cmd)
        self.assertNotIn('fork', cmd)
        self.assertIn('model_reasoning_effort="high"', cmd)
        self.assertIn('gpt-6-astra', cmd)


if __name__ == '__main__':
    unittest.main()
