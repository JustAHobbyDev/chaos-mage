"""Artificial accounting fixtures; no expected outcomes for diagnostic mappings."""
from pathlib import Path
from unittest.mock import patch
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import publication as p


class PublicationTests(unittest.TestCase):
    def test_taxonomy_split_keeps_mixed_uncertain_separate(self):
        fake = {f'ART-{i}':{'category':category} for i,category in enumerate(p.c.CATEGORIES)}
        with patch.object(p, 'responses', return_value=fake):
            result = p.taxonomy_metrics()
        self.assertEqual(result['completed'],6)
        self.assertEqual(len(result['execution']),1)
        self.assertEqual(len(result['validity_relevant']),3)
        self.assertEqual(len(result['mixed_uncertain']),2)

    def compute(self, valid_count):
        ids = [f'ARTIFICIAL-{i:03}' for i in range(30)]
        data = {identity:{'final_status':'Valid' if i<valid_count else 'Invalid',
                'execution_readiness':{'status':'requires_preconditions'},
                'conditions':[{'category':'execution_precondition'}]} for i,identity in enumerate(ids)}
        manifest = [{'case_id':identity,'fidelity_pass':i<20,'generator_family':'A' if i<15 else 'B','source_path':'artificial-source'} for i,identity in enumerate(ids)]
        def read(path):
            if path.name=='mapping-assessments.json': return {'findings':[{'case_id':identity} for identity in ids]}
            if path.name=='operator-manifest.json': return {'cases':manifest}
            if path.name.startswith('validity-'): return {'validity':{'final_status':'Conditional'}}
            raise AssertionError('Unexpected artifact read: '+str(path))
        with tempfile.TemporaryDirectory() as tmp, patch.object(p.r,'RUNTIME',Path(tmp)), patch.object(p.old,'RUNTIME',Path(tmp)), patch.object(p.c,'read',side_effect=read), patch.object(p.old,'committed'), patch.object(p,'taxonomy_metrics',return_value={'completed':196}), patch.object(p,'responses',return_value=data):
            return p.complete_metrics()

    def test_single_model_intersection_and_threshold(self):
        below=self.compute(17); at=self.compute(18); beyond=self.compute(25)
        self.assertFalse(below['reaches_18'])
        self.assertTrue(at['reaches_18'])
        self.assertEqual(beyond['single_model_prospective_eligible_count'],20)
        self.assertTrue(beyond['E_remains_stopped'])
        self.assertFalse(beyond['dual_family_rule_satisfied'])

    def test_more_permissive_transitions_and_readiness(self):
        result=self.compute(18)
        self.assertEqual(len(result['more_permissive_transitions']),18)
        self.assertEqual(result['old_to_new_transitions']['Conditional']['Invalid'],12)
        self.assertEqual(result['execution_readiness_distribution']['requires_preconditions'],30)
        self.assertEqual(sum(result['prospective_status_distribution'].values()),30)

    def test_historical_comparison_blocked_without_committed_assessments(self):
        with patch.object(p,'taxonomy_metrics',return_value={}), patch.object(p,'responses',return_value={}), patch.object(p.old,'committed',side_effect=ValueError('Assessment not committed')), patch.object(p.c,'read') as read:
            with self.assertRaisesRegex(ValueError,'Assessment not committed'): p.complete_metrics()
            read.assert_not_called()

    def test_prospective_preparation_requires_committed_taxonomy(self):
        with patch.object(p,'frozen',side_effect=ValueError('Taxonomy not frozen')), patch.object(p.old,'write') as write:
            with self.assertRaisesRegex(ValueError,'Taxonomy not frozen'): p.prepare_prospective()
            write.assert_not_called()

    def test_exact_schema_contract_is_reused(self):
        self.assertEqual(p.c.schema('prospective'),p.r.contracts.schema('prospective'))

    def test_prechecks_must_finish_before_measurement(self):
        check={'input_commit':'fixture','checks':[{'exit_code':0} for _ in range(36)],'legacy_F':{'tests':37},'at':'2026-09-30T12:00:00+00:00'}
        with patch.object(p.c,'read',return_value=check):
            p.verify_precheck(Path('fixture'),'fixture','2026-09-30T12:00:01+00:00')
            with self.assertRaisesRegex(ValueError,'after provider'): p.verify_precheck(Path('fixture'),'fixture','2026-09-30T11:59:59+00:00')
            with self.assertRaisesRegex(ValueError,'commit mismatch'): p.verify_precheck(Path('fixture'),'other','2026-09-30T12:00:01+00:00')
            check['checks'][0]['exit_code']=1
            with self.assertRaisesRegex(ValueError,'Incomplete historical'): p.verify_precheck(Path('fixture'),'fixture','2026-09-30T12:00:01+00:00')


if __name__=='__main__': unittest.main()
