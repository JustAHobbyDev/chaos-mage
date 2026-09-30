"""Reconstruct published results from immutable evidence, independently of the builder."""
from collections import Counter
from decimal import Decimal
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('report_contract', HERE/'review/contracts.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
r = c.r


@unittest.skipUnless((HERE/'metrics.json').exists(), 'Final review pending')
class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metrics = r.read(HERE/'metrics.json')
        cls.reviews = r.read(HERE/'review/case-reviews.json')
        cls.data = r.complete_results()

    def test_distributions_reconstruct_from_judgments(self):
        for stage, ids in r.IDS.items():
            actual = Counter(r.status(self.data[cid], stage) for cid in ids)
            self.assertEqual(actual, Counter(self.metrics['status_distributions'][stage]))
        reject = self.metrics['status_distributions']['anti-collapse']['CLEAR_COLLAPSE']
        self.assertEqual(self.metrics['anti_collapse_gate'], {'keep': 6-reject, 'reject': reject})

    def test_review_and_failure_counts_reconstruct(self):
        self.assertEqual(self.metrics['qualification'], self.reviews['qualification'])
        for category in r.CATEGORIES:
            ids = [v['qualification_id'] for v in self.reviews['cases'] if v['final_disagreement_class'] == category]
            self.assertEqual(ids, self.metrics['disagreement_cases'][category])
            self.assertEqual(len(ids), self.metrics['disagreement_counts'][category])
        for dimension in r.DIMENSIONS:
            ids = [v['qualification_id'] for v in self.reviews['cases'] if v['capability_dimensions'][dimension] == 'fail']
            self.assertEqual(ids, self.metrics['capability_failures'][dimension])

    def test_token_and_cost_totals_from_raw_provider_metadata(self):
        raw = [r.read(p)['usageMetadata'] for stage in ('preflight', 'judgments') for p in (HERE/stage).glob('*/http-body.json')]
        self.assertEqual(len(raw), 14)
        totals = {'input_tokens': sum(v['promptTokenCount'] for v in raw),
                  'output_tokens': sum(v['candidatesTokenCount'] for v in raw),
                  'thinking_tokens': sum(v['thoughtsTokenCount'] for v in raw)}
        for k, v in totals.items():
            self.assertEqual(v, self.metrics[k])
        expected = (Decimal(totals['input_tokens'])*2 + Decimal(totals['output_tokens']+totals['thinking_tokens'])*12)/1000000
        self.assertEqual(expected, Decimal(self.metrics['estimated_experiment_usd']))
        self.assertLess(expected, Decimal('2'))

    def test_review_commit_ancestry_and_preserved_preliminary(self):
        freeze = r.checkpoint(HERE/'results-freeze.json')
        preliminary = r.checkpoint(HERE/'review/preliminary.json')
        self.assertNotEqual(freeze, preliminary)
        r.git('merge-base', '--is-ancestor', freeze, preliminary)
        original = r.read(HERE/'review/preliminary.json')
        for before, after in zip(original['cases'], self.reviews['cases']):
            for k in ('qualification_id', 'source_case_id', 'gemini', 'capability_dimensions', 'preliminary_disagreement_class'):
                self.assertEqual(before[k], after[k])
            self.assertTrue(after['rationale'].startswith(before['rationale']))

    def test_report_checkpoint_cost_and_decision_consistency(self):
        report = (r.ROOT/'distance/review/model-qualification-gemini-v0.2.md').read_text()
        for p in ('prepared.json', 'preflight/freeze.json', 'results-freeze.json', 'review/preliminary.json'):
            self.assertIn(r.checkpoint(HERE/p), report)
        self.assertIn(self.metrics['qualification'], report)
        self.assertIn(self.metrics['estimated_experiment_usd'], report)
        for cid in self.data:
            self.assertIn('### '+cid+' — ', report)
        self.assertEqual(r.git('show', r.config()['starting_sha']+':docs/MODEL-POLICY.md'), (r.ROOT/'docs/MODEL-POLICY.md').read_bytes())


if __name__ == '__main__':
    unittest.main()
