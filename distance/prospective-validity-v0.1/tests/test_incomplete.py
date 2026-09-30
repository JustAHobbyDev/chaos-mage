"""Terminal evidence checks; no provider calls and no diagnostic outcome keys."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'review'))
import verify_incomplete as v

class IncompleteTests(unittest.TestCase):
    def test_complete_terminal_evidence(self):
        x=v.verify(); self.assertEqual(x['status'],'incomplete'); self.assertEqual(x['attempts_after_stop'],0)
    def test_new_raw_artifact_rejected(self):
        original=v.r.inventory
        def changed(paths): return {**original(paths),'unexpected.json':'0'*64}
        with patch.object(v.r,'inventory',side_effect=changed):
            with self.assertRaisesRegex(ValueError,'Execution after terminal freeze'): v.verify()
    def test_changed_order_rejected(self):
        order=v.r.order('taxonomy'); order[0],order[1]=order[1],order[0]
        with patch.object(v.r,'order',return_value=order):
            with self.assertRaisesRegex(ValueError,'Partial order/coverage'): v.verify()
    def test_metrics_are_recomputed(self):
        bad=v.metrics.compute(); bad['taxonomy_completed']+=1
        with patch.object(v.metrics,'compute',return_value=bad):
            with self.assertRaisesRegex(ValueError,'Metrics do not reconstruct'): v.verify()
    def test_missing_measurement_is_not_zero_eligible(self):
        x=v.metrics.compute()
        for field in ('single_model_prospective_eligible_count','reaches_18','prospective_status_distribution','old_to_new_transition_matrix','execution_readiness_distribution','cross_model_robustness','within_model_stability'):
            self.assertIsNone(x[field])
    def test_partial_is_original_prefix_with_no_replacement(self):
        x=v.c.read(v.r.HERE/'taxonomy-partial-freeze.json')
        self.assertEqual([e['identity'] for e in x['runs']],v.r.order('taxonomy')[:x['completed']])
        self.assertLess(x['completed'],x['planned'])
    def test_bad_freeze_binding_rejected(self):
        read=v.c.read
        def altered(path):
            x=read(path)
            if Path(path).name=='taxonomy-partial-freeze.json': x['failure_freeze_sha256']='0'*64
            return x
        with patch.object(v.c,'read',side_effect=altered):
            with self.assertRaisesRegex(ValueError,'Failure binding'): v.verify()

if __name__=='__main__': unittest.main()
