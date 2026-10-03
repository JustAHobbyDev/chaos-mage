import importlib.util
from pathlib import Path
import unittest

H = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('h7_stages', H / 'stages.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


class PacketBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.packet = {'packet_id': 'M', 'claims': {'claims': [{'claim_id': 'C1'}, {'claim_id': 'C2'}]},
                       'allowed_source_ids': ['T001', 'S001', 'P001']}
        self.classes = {'packet_id': 'M', 'classifications': [
            {'claim_id': 'C1', 'evidence_used': [{'source_id': 'T001'}]},
            {'claim_id': 'C2', 'evidence_used': [{'source_id': 'P001'}]}]}

    def test_source_id_only_responses_are_valid(self):
        s.validate('classification', self.classes, self.packet)

    def test_missing_claim_cannot_silently_shrink_sample(self):
        self.classes['classifications'].pop()
        with self.assertRaisesRegex(ValueError, 'coverage'):
            s.validate('classification', self.classes, self.packet)

    def test_duplicate_claim_cannot_replace_another(self):
        self.classes['classifications'][1]['claim_id'] = 'C1'
        with self.assertRaisesRegex(ValueError, 'coverage'):
            s.validate('classification', self.classes, self.packet)

    def test_unknown_source_is_an_interface_failure(self):
        self.classes['classifications'][0]['evidence_used'][0]['source_id'] = 'S999'
        with self.assertRaisesRegex(ValueError, 'RESPONSE_SOURCE_UNKNOWN'):
            s.validate('classification', self.classes, self.packet)

    def test_unknown_and_self_claim_refs_fail(self):
        value = {'packet_id': 'M', 'claims': [{'claim_id': 'C1', 'dependencies': [
            {'dependency_id': 'D1', 'resolution': 'CLAIM_REF', 'referenced_claim_id': 'C9'}]},
            {'claim_id': 'C2', 'dependencies': []}]}
        with self.assertRaisesRegex(ValueError, 'Unknown claim'):
            s.validate('discovery', value, self.packet)
        value['claims'][0]['dependencies'][0]['referenced_claim_id'] = 'C1'
        with self.assertRaisesRegex(ValueError, 'Self-referential'):
            s.validate('discovery', value, self.packet)


class RoutingTests(unittest.TestCase):
    def test_supplied_asserted_operation_gets_both_contracts(self):
        for origin in s.FIDELITY:
            a = {'content_origin': origin, 'epistemic_function': 'OPERATION', 'assertion_mode': 'ASSERTED_COMPONENT'}
            self.assertEqual(s.contracts(a), s.FIDELITY[origin] + ['OPERATION_LICENSE'])

    def test_referenced_operation_has_no_generated_warrant(self):
        a = {'content_origin': 'TARGET_SUPPLIED', 'epistemic_function': 'OPERATION', 'assertion_mode': 'REFERENCED_PREMISE'}
        self.assertEqual(s.contracts(a), [])
        s.grounding(a, [{'source_id': 'T001'}])
        with self.assertRaises(ValueError):
            s.grounding(a, [{'source_id': 'S001'}])

    def test_generated_governance_has_narrow_structure_contract(self):
        a = {'content_origin': 'MAPPING_GENERATED', 'epistemic_function': 'GOVERNANCE_RULE', 'assertion_mode': None}
        self.assertEqual(s.contracts(a), ['GOVERNANCE_STRUCTURE'])
        a['epistemic_function'] = 'OPERATION'
        self.assertEqual(s.contracts(a), ['OPERATION_LICENSE'])

    def test_uncertain_axes_never_get_guessed_contracts(self):
        with self.assertRaises(ValueError):
            s.contracts({'content_origin': None, 'epistemic_function': 'FACT', 'assertion_mode': None})


if __name__ == '__main__':
    unittest.main()
