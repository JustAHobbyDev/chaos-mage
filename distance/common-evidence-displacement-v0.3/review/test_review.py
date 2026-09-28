import copy
import unittest
import diagnostics as d
import metrics
import runner as r

class ReviewTests(unittest.TestCase):
    def test_independent_counts(self):
        value=d.calculate();frozen=r.read(r.HERE/'metrics.json')
        for stage,summary in value['stages'].items():
            self.assertEqual(summary['independent_overall_agreement']['agreements'],frozen['stages'][stage]['overall_agreement']['agreements'])
    def test_identity_proof(self):
        value=d.calculate()
        self.assertEqual(len(value['shared_state_proof']),len(r.pair_records()))
        for p in value['shared_state_proof']:self.assertEqual(len(p['equal_component_hashes']),9)
    def test_controls_excluded_and_triangle_attrition(self):
        v=d.calculate()['coverage'];self.assertEqual(v['primary_pairs'],10);self.assertEqual(v['orientation_controls'],4)
        self.assertEqual(v['complete_triangle_targets'],['T01','T03']);self.assertEqual(v['measured_unique_mappings'],14)
    def test_measured_orientation_change_retained(self):
        value=d.calculate();self.assertEqual(value['stages']['prospective']['orientation_changes'],[])
        self.assertEqual(value['stages']['consequence']['orientation_changes'],[{'family':'A','primary':'C006','reversal':'C009'}])
    def test_transition_denominators_and_no_reverse(self):
        v=r.read(r.HERE/'metrics.json')
        for f in 'AB':
            self.assertEqual(sum(v['transitions'][f]['counts'].values()),10)
            self.assertEqual(v['transitions'][f]['counts'].get('direction-reversal',0),0)
    def test_final_outcomes_still_derive(self):
        for row in r.manifest():r.c.validate_outcome(row,r.read(r.HERE/'outcomes'/f'{row["mapping_id"]}.json'))

if __name__=='__main__':unittest.main()
