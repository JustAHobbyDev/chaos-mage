"""Offline checks for watch records and unresolved obligation counts."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('h7_inventory', Path(__file__).resolve().parents[1] / 'stages.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


class InventoryTests(unittest.TestCase):
    def test_governance_cannot_hide_supplied_asserted_operation(self):
        claims = {'claims': [{'claim_id': 'C1', 'proposition': 'Fixture rule', 'scope': 'Fixture scope'}]}
        assignments = {'classifications': [{'claim_id': 'C1', 'atomicity': 'ATOMIC',
            'content_origin': 'MAPPING_GENERATED', 'epistemic_function': 'GOVERNANCE_RULE',
            'assertion_mode': None}]}
        discovery = {'claims': [{'claim_id': 'C1', 'closure': 'COMPLETE', 'base_evidence_used': [],
            'dependencies': [{'dependency_id': 'D1', 'subject': 'Fixture supplied action', 'scope': 'Same scope',
                'content_origin': 'SOURCE_SUPPLIED', 'epistemic_function': 'OPERATION',
                'assertion_mode': 'ASSERTED_COMPONENT', 'distinct': True, 'material': True,
                'unevaluated': True, 'another_independent_level_required': False,
                'resolution': 'INLINE_OBLIGATION', 'evidence_used': [{'source_id': 'S001'}]}]}]}
        result = s.obligation_inventory(claims, assignments, discovery)
        self.assertEqual(result['evaluation_session_count'], 3)
        self.assertEqual([x['contract'] for x in result['obligations']],
                         ['GOVERNANCE_STRUCTURE', 'SOURCE_FIDELITY', 'OPERATION_LICENSE'])
        watch = result['supplied_operation_watch'][0]
        self.assertTrue(watch['operation_license_present'])
        self.assertIsNone(watch['fidelity_verdict'])
        self.assertIsNone(watch['operation_license_verdict'])

    def test_split_required_leaves_fanout_unresolved(self):
        result = s.obligation_inventory(
            {'claims': [{'claim_id': 'C1'}]},
            {'classifications': [{'claim_id': 'C1', 'atomicity': 'SPLIT_REQUIRED'}]},
            {'claims': [{'claim_id': 'C1', 'closure': 'SPLIT_REQUIRED'}]})
        self.assertIsNone(result['evaluation_session_count'])
        self.assertFalse(result['ready_for_evaluation'])
        self.assertTrue(result['routing_issues'])
        self.assertNotIn('scientific_status', result)


if __name__ == '__main__':
    unittest.main()
