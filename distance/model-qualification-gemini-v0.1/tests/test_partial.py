import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('gemini_partial_tests',HERE/'review/verify_incomplete.py')
v = importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
r=v.r


class PartialTests(unittest.TestCase):
    def test_partial_evidence(self): self.assertTrue(v.verify()['passed'])
    def test_complete_results_gate_stays_closed(self):
        with self.assertRaises(Exception): r.complete_results()
    def test_historical_decode_stays_closed(self):
        with self.assertRaises(Exception): r.historical()
    def test_scheduler_stays_stopped(self):
        with self.assertRaises(ValueError): r.prerequisites()
        with self.assertRaises(ValueError): r.guard()
    def test_one_probe_cost_below_ceiling(self):
        from decimal import Decimal
        c=r.read(HERE/'review/cost-summary.json')
        self.assertLess(Decimal(c['estimated_experiment_usd']),Decimal('2'))
        self.assertEqual(c['billable_output_tokens'],c['output_tokens']+c['thinking_tokens'])
    def test_report_no_capability_claim(self):
        report=(r.ROOT/'distance/review/model-qualification-gemini-v0.1.md').read_text()
        self.assertIn('**Qualification: `qualification_inconclusive`.**',report)
        self.assertIn('No primary judgments were collected',report)
    def test_allowed_categories_outcomes(self):
        self.assertEqual(set(r.CATEGORIES),{'none','ontology_specification_ambiguity','legitimate_reasoning_variation','model_failure'})
        self.assertEqual(set(r.OUTCOMES),{'qualified','not_qualified','qualification_inconclusive'})
        self.assertIn(r.read(HERE/'metrics.json')['qualification'],r.OUTCOMES)
    def test_no_accuracy_or_consensus_metric(self):
        text=(HERE/'metrics.json').read_text()
        for word in ('accuracy','consensus','majority'): self.assertNotIn(word,text)
    def test_actual_single_request_no_tools(self):
        body=r.read(HERE/'preflight/validity/request.json')
        self.assertEqual(set(body),{'contents','generationConfig'})
        self.assertEqual(len(body['contents']),1)
        self.assertEqual(body['generationConfig']['thinkingConfig'],{'thinkingLevel':'HIGH'})
    def test_historical_files_byte_identical(self):
        r.verify_inventory(r.read(HERE/'preservation.json')['files'])


if __name__=='__main__': unittest.main()
