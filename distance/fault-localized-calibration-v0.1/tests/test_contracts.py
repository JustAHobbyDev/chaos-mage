import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import contracts as c

class ScoringTests(unittest.TestCase):
    def test_all_decisive_combinations(self):
        expected = [
            ['KEEP_WITH_WARRANT_FLAGS', 'KEEP_WITH_REDUCED_SCOPE', 'CORE_INVALID', 'UNCERTAIN_LOAD_BEARING'],
            ['KEEP_WITH_REDUCED_SCOPE', 'KEEP_WITH_REDUCED_SCOPE', 'CORE_INVALID', 'UNCERTAIN_LOAD_BEARING'],
            ['CORE_INVALID'] * 4,
            ['UNCERTAIN_LOAD_BEARING', 'UNCERTAIN_LOAD_BEARING', 'CORE_INVALID', 'UNCERTAIN_LOAD_BEARING']]
        for i, mechanism in enumerate(c.MECHANISM):
            for j, target in enumerate(c.TARGET):
                self.assertEqual(c.derive(mechanism, target), expected[i][j])
                self.assertEqual(c.derive(mechanism, target, {'present': True, 'resolved': False}), 'UNCERTAIN_LOAD_BEARING')
                self.assertEqual(c.derive(mechanism, target, {'present': True, 'resolved': True}), expected[i][j])

    def test_exact_separate_excerpts_and_deletion(self):
        candidate = {'mapping': {'signal': 'Alpha evidence. Middle. Omega evidence.'}}
        spans = [{'source_field': 'mapping.signal', 'exact_text': text} for text in ['Alpha evidence.', 'Omega evidence.']]
        self.assertEqual(len(c.cited_spans(spans, candidate)), 2)
        with self.assertRaises(ValueError):
            c.cited_spans([{'source_field': 'mapping.signal', 'exact_text': 'Alpha evidence.\nOmega evidence.'}], candidate)
        deleted = [{'source_field': 'mapping.signal', 'span_start': 0, 'span_end': 15}]
        with self.assertRaises(ValueError):
            c.cited_spans(spans, candidate, deleted, surviving=True)
        c.cited_spans(spans[1:], candidate, deleted, surviving=True)

    def test_schema_and_duplicate_keys(self):
        for stage in ['claim-warrant', 'ablation']:
            c.jsonschema.Draft202012Validator.check_schema(c.schema(stage))
        with self.assertRaises(ValueError):
            c.unique([('status', 'SUPPORTED'), ('status', 'UNSUPPORTED')])

if __name__ == '__main__':
    unittest.main()
