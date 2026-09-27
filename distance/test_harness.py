"""Checks protect experimental denominators, ordinal metrics, and input integrity."""
import copy
import unittest
import yaml
import jsonschema
import harness as h


def judgment(label='Native', level=0, status='native'):
    return {'case_id':'CASE-001', 'target_native_profile':dict.fromkeys(h.DIMS,'native profile'),
        'source_transfer_profile':dict.fromkeys(h.DIMS,'transfer profile'),
        'displacement':{d:{'level':level,'rationale':'reason'} for d in h.DIMS},
        'naturalization':{'status':status,'evidence':'practice example','rationale':'reason'},
        'final_class':label,'class_rationale':'reason','uncertainty':[]}


class HarnessTests(unittest.TestCase):
    def test_known_metrics_and_boundaries(self):
        pairs=[(judgment(),judgment()),(judgment(),judgment('Adjacent',1)),
               (judgment('Adjacent',1),judgment('Remote',2,'non-native')),
               (judgment(),judgment('Alien',3,'uncertain'))]
        result=h.metrics(pairs)
        self.assertEqual(result['final_class']['exact_rate'],.25)
        self.assertEqual(result['final_class']['one_step_rate'],.5)
        self.assertEqual(result['final_class']['within_one_step_rate'],.75)
        self.assertEqual(result['naturalization']['exact_rate'],.5)
        for value in result['dimensions'].values():
            self.assertEqual(value['exact_rate'],.25)
            self.assertEqual(value['mean_absolute_disagreement'],1.25)
        self.assertEqual(result['boundary_dimensions']['Adjacent ↔ Remote']['operations']['absolute_disagreement'],1)

    def test_different_class_same_vector_is_preserved(self):
        result=h.metrics([(judgment('Adjacent'),judgment('Remote'))])
        self.assertEqual(result['final_class']['exact_count'],0)
        self.assertEqual(result['dimensions']['operations']['exact_count'],1)

    def test_output_contract_rejects_extras_missing_fields_and_bad_levels(self):
        base={'classification':judgment()}
        h.validate_judgment(base,'CASE-001')
        for level in (True, 1.0, -1, 4):
            bad=copy.deepcopy(base)
            bad['classification']['displacement']['entities']['level']=level
            with self.assertRaises((ValueError,jsonschema.ValidationError)):
                h.validate_judgment(bad,'CASE-001')
        bad=copy.deepcopy(base); bad['classification']['usefulness']=3
        with self.assertRaises(jsonschema.ValidationError): h.validate_judgment(bad,'CASE-001')
        bad=copy.deepcopy(base); del bad['classification']['displacement']['relations']
        with self.assertRaises(jsonschema.ValidationError): h.validate_judgment(bad,'CASE-001')
        with self.assertRaises(ValueError): h.validate_judgment(base,'CASE-002')

    def test_duplicate_keys_rejected(self):
        with self.assertRaises(ValueError): yaml.load('a: 0\na: 3',Loader=h.UniqueLoader)

    def test_case_coverage_provenance_and_contrasts(self):
        self.assertEqual(len(h.cases()),20)

    def test_empty_denominator_rejected(self):
        with self.assertRaises(ValueError): h.metrics([])


if __name__=='__main__': unittest.main()
