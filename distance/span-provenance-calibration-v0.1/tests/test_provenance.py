"""Harness behavior tests; golden semantic reviews are not an entailment oracle."""
import copy
import json
from pathlib import Path
import sys
import unittest

H = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(H))
import segment as s
import validate as v


def mapping(text, field='state'):
    return {f: text if f == field else '' for f in s.FIELDS}


def fixture(refs=None, value='Both mechanisms remain live.'):
    return {'fixture_id': 'synthetic', 'packet_id': 'synthetic', 'description': 'Harness test only',
            'category': 'positive', 'expected_mechanical_codes': [], 'components': [{
                'component_id': 'C1', 'component_type': 'contrast', 'value': value,
                'scope': 'The test case.', 'provenance': {'refs': refs or [{'source_id': 'P001', 'role': 'SUPPORT'}]},
                'expected_support_status': 'SUFFICIENT', 'expected_codes': []}]}


def review(f, status='SUFFICIENT', codes=()):
    return {'fixture_id': f['fixture_id'], 'packet_id': f['packet_id'], 'fixture_sha256': s.canonical_hash(f),
            'reviewer': 'Codex engineering review', 'independent_rater': False,
            'assessment_basis': 'Authored golden review for harness routing only.',
            'components': [{'component_id': c['component_id'], 'support_status': status, 'codes': list(codes),
                            'rationale': 'Explicit test review; this does not demonstrate automatic entailment.'}
                           for c in f['components']]}


class SegmentationTests(unittest.TestCase):
    def test_identical_policy_in_all_five_fields(self):
        text = 'First sentence. Second sentence; if a condition holds, retain the qualifier.'
        tables = [s.segment('test', mapping(text, field)) for field in s.FIELDS]
        self.assertEqual(len({tuple(x['text'] for x in t['spans'].values()) for t in tables}), 1)

    def test_no_field_crossing_and_unique_opaque_ids(self):
        m = {f: 'One sentence. Another sentence.' for f in s.FIELDS}
        t = s.segment('test', m)
        self.assertEqual(list(t['spans']), [f'P{i:03d}' for i in range(1, 11)])
        for row in t['spans'].values():
            a, b = row['source_range']
            self.assertEqual(row['text'], m[row['field']][a:b])

    def test_list_items_independent_and_nested_parent(self):
        t = s.segment('test', mapping('- Parent sentence. Extra sentence.\n  - Child item\n  - Second child\n- Last item'))
        self.assertEqual(len(t['spans']), 4)
        self.assertEqual(t['spans']['P002']['parent_id'], 'P001')
        self.assertEqual(t['spans']['P003']['parent_id'], 'P001')
        self.assertNotIn('parent_id', t['spans']['P004'])
        self.assertIn('Extra sentence.', t['spans']['P001']['text'])

    def test_list_continuation(self):
        t = s.segment('test', mapping('1. First item\n   continued with qualification\n2. Second item'))
        self.assertEqual(len(t['spans']), 2)
        self.assertIn('qualification', t['spans']['P001']['text'])

    def test_table_header_and_row_no_cells(self):
        t = s.segment('test', mapping('| Hypothesis | Evidence |\n| --- | --- |\n| H1 | inconsistent |\n| H2 | consistent |'))
        self.assertEqual(len(t['spans']), 3)
        self.assertEqual(t['spans']['P001']['kind'], 'table_header')
        self.assertEqual(t['spans']['P002']['header_id'], 'P001')
        self.assertEqual(t['spans']['P003']['header_id'], 'P001')

    def test_no_clause_segmentation_or_length_cap(self):
        text = 'If the workload is fixed, measure waits; because occupancy matters, compare both: high waits favor contention whereas low waits favor exhaustion and retain all qualifiers ' + 'word ' * 2000 + '.'
        t = s.segment('test', mapping(text))
        self.assertEqual([x['text'] for x in t['spans'].values()], [text])

    def test_uncertain_abbreviations_initials_decimals_quotes(self):
        for text in ['Dr. Smith checks the result.', 'A. Smith checks the result.',
                     'The score is 1.5 under these conditions.', 'He says “First. Second.”',
                     '(First. Second.)', 'Wait... Then continue.', 'One sentence. lowercase continuation.']:
            with self.subTest(text=text):
                self.assertEqual(len(s.segment('test', mapping(text))['spans']), 1)

    def test_paragraphs_before_sentences_and_soft_newlines(self):
        t = s.segment('test', mapping('One sentence\ncontinues here.\n\nAnother paragraph.'))
        self.assertEqual(len(t['spans']), 2)
        self.assertEqual(t['spans']['P001']['block_index'], 0)
        self.assertEqual(t['spans']['P002']['block_index'], 1)

    def test_empty_fields_no_phantom_spans(self):
        self.assertEqual(s.segment('empty', mapping(''))['spans'], {})

    def test_frozen_tables_determinism_and_roundtrip(self):
        manifest = json.loads((H / 'manifest.json').read_text())
        self.assertEqual(len(manifest['sources']), 20)
        for source in manifest['sources']:
            m = json.loads((H.parents[1] / source['path']).read_text())['mapping']
            a = s.segment(source['packet_id'], m)
            b = s.segment(source['packet_id'], dict(reversed(list(m.items()))))
            self.assertEqual(a, b)
            self.assertEqual(json.loads(json.dumps(a, ensure_ascii=True)), a)
            self.assertEqual(a, json.loads((H / 'span-tables' / (source['packet_id'] + '.json')).read_text()))
            self.assertFalse(v.schema_errors('span-table', a))

    def test_changed_source_is_integrity_failure(self):
        m = mapping('Source sentence.')
        t = s.segment('test', m)
        with self.assertRaisesRegex(ValueError, 'INTEGRITY_SPAN_TABLE'):
            s.verify_table(t, mapping('Source sentence!'))


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.table = s.segment('synthetic', mapping('Both mechanisms remain live. Inspect the ledger next.'))

    def errors(self, f, table=None):
        return {e['code'] for e in v.mechanical(table or self.table, v.annotation_from_fixture(f))}

    def test_unknown_id(self):
        self.assertEqual(self.errors(fixture([{'source_id': 'P999', 'role': 'SUPPORT'}])), {'PROV_UNKNOWN_SOURCE_ID'})

    def test_context_only_and_empty_fail(self):
        f = fixture([{'source_id': 'P001', 'role': 'CONTEXT'}])
        self.assertEqual(self.errors(f), {'PROV_NO_SUPPORT'})
        f['components'][0]['provenance']['refs'] = []
        self.assertEqual(self.errors(f), {'PROV_NO_SUPPORT'})

    def test_duplicate_and_role_conflict(self):
        f = fixture([{'source_id': 'P001', 'role': role} for role in ['SUPPORT', 'SUPPORT']])
        self.assertEqual(self.errors(f), {'PROV_DUPLICATE_REF'})
        f['components'][0]['provenance']['refs'][1]['role'] = 'CONTEXT'
        self.assertEqual(self.errors(f), {'PROV_DUPLICATE_REF', 'PROV_ROLE_CONFLICT'})

    def test_wrong_packet_even_when_id_exists(self):
        f = fixture(); f['packet_id'] = 'different'
        self.assertEqual(self.errors(f), {'PROV_WRONG_PACKET'})

    def test_invalid_roles_and_model_offsets_rejected_by_schema(self):
        for key in ['start', 'end', 'byte_offset', 'character_offset', 'exact_text']:
            f = fixture(); f['components'][0]['provenance']['refs'][0][key] = 0
            self.assertEqual(self.errors(f), {'PROV_SCHEMA'})
        f = fixture(); f['components'][0]['provenance']['refs'][0]['role'] = 'EVIDENCE'
        self.assertEqual(self.errors(f), {'PROV_SCHEMA'})

    def test_component_wording_not_byte_compared(self):
        for value in ['Both mechanisms remain live', 'Both mechanisms remain live.',
                      '“Both mechanisms” remain live', 'Both mechanisms\r\nremain live']:
            self.assertFalse(self.errors(fixture(value=value)))

    def test_citation_serialization_whitespace_and_unicode_escaping(self):
        a = v.annotation_from_fixture(fixture(value='“Both mechanisms” remain live.'))
        b = json.loads(json.dumps(a, indent=4, ensure_ascii=True))
        self.assertEqual(v.mechanical(self.table, a), v.mechanical(self.table, b))

    def test_same_span_reused_and_multiple_supports(self):
        f = fixture([{'source_id': sid, 'role': 'SUPPORT'} for sid in ['P001', 'P002']])
        c = copy.deepcopy(f['components'][0]); c['component_id'] = 'C2'; f['components'].append(c)
        self.assertFalse(self.errors(f))

    def test_unnecessary_context_is_not_failure(self):
        f = fixture([{'source_id': 'P001', 'role': 'SUPPORT'}, {'source_id': 'P002', 'role': 'CONTEXT'}])
        self.assertFalse(self.errors(f))

    def test_no_review_does_not_use_expectation_or_self_report(self):
        f = fixture(); f['components'][0]['provenance']['support_status'] = 'SUFFICIENT'
        result = v.validate_fixture(self.table, f)
        self.assertEqual(result['review_errors'], ['REVIEW_MISSING'])
        self.assertEqual(result['components'], [])

    def test_review_binding_prevents_stale_semantic_label(self):
        f = fixture(); r = review(f); f['components'][0]['value'] = 'A changed claim'
        self.assertEqual(v.validate_fixture(self.table, f, r)['review_errors'], ['REVIEW_BINDING'])

    def test_review_cannot_omit_component_or_conflict_with_status(self):
        f = fixture(); r = review(f); r['components'] = []
        self.assertEqual(v.validate_fixture(self.table, f, r)['review_errors'], ['REVIEW_COVERAGE'])
        r = review(f, 'SUFFICIENT', ['PROV_MISSING_CONTEXT'])
        self.assertEqual(v.validate_fixture(self.table, f, r)['review_errors'], ['REVIEW_STATUS_CODES'])

    def test_former_latter_with_and_without_context_recorded_reviews(self):
        table = s.segment('synthetic', mapping('The alternatives are contention and exhaustion. Long waits favor the former; short waits favor the latter.'))
        f = fixture([{'source_id': 'P002', 'role': 'SUPPORT'}, {'source_id': 'P001', 'role': 'CONTEXT'}],
                    'Long waits favor contention; short waits favor exhaustion.')
        self.assertEqual(v.validate_fixture(table, f, review(f))['components'][0]['support_status'], 'SUFFICIENT')
        f['components'][0]['provenance']['refs'].pop()
        result = v.validate_fixture(table, f, review(f, 'INSUFFICIENT', ['PROV_MISSING_CONTEXT']))
        self.assertEqual(result['components'][0]['codes'], ['PROV_MISSING_CONTEXT'])

    def test_synthetic_list_and_table_provenance(self):
        for text, support, context in [('- Named target\n  - Qualifier for that target', 'P002', 'P001'),
                ('| Hypothesis | Evidence |\n| --- | --- |\n| H1 | inconsistent |', 'P002', 'P001')]:
            table = s.segment('synthetic', mapping(text))
            f = fixture([{'source_id': support, 'role': 'SUPPORT'}, {'source_id': context, 'role': 'CONTEXT'}])
            self.assertFalse(self.errors(f, table))

    def test_recorded_uncertainty_not_automatic_failure(self):
        f = fixture(); result = v.validate_fixture(self.table, f, review(f, 'UNCERTAIN', ['PROV_UNCERTAIN_SUPPORT']))
        self.assertTrue(result['mechanically_valid']); self.assertFalse(result['review_errors'])
        self.assertEqual(result['components'][0]['support_status'], 'UNCERTAIN')

    def test_conflict_requires_all_reviewed_conditions_and_is_nonfailing(self):
        left = fixture()['components'][0]; right = copy.deepcopy(left); right['value'] = 'Incompatible assertion'
        finding = {'mutually_incompatible': True, 'material_support_overlap': True, 'rationale': 'Explicit test review'}
        signal = v.conflict_review('p', left, 'p', right, finding)
        self.assertEqual(signal[0]['code'], 'PROV_CONFLICT_REVIEW'); self.assertFalse(signal[0]['failing'])
        self.assertFalse(v.conflict_review('p', left, 'p', right, None))
        self.assertFalse(v.conflict_review('p', left, 'other', right, finding))
        for key, value in [('component_type', 'different'), ('scope', 'different')]:
            changed = {**right, key: value}; self.assertFalse(v.conflict_review('p', left, 'p', changed, finding))
        right['provenance']['refs'][0]['source_id'] = 'P002'
        self.assertFalse(v.conflict_review('p', left, 'p', right, finding))
        for key in ['mutually_incompatible', 'material_support_overlap']:
            self.assertFalse(v.conflict_review('p', left, 'p', left, {**finding, key: False}))


class FrozenCalibrationTests(unittest.TestCase):
    def test_historical_preservation_and_full_authoring_gate(self):
        import calibrate
        metrics, results = calibrate.evaluate()
        self.assertTrue(metrics['historical_preservation']['unchanged'])
        self.assertEqual(metrics['provider_calls'], 0)
        self.assertEqual(metrics['mappings_segmented'], 20)
        self.assertEqual(len(results), 33)
        self.assertEqual(metrics['unexpected_failures'], [])

    def test_all_fixtures_against_separate_recorded_reviews(self):
        for entry in json.loads((H / 'fixtures-freeze.json').read_text())['fixtures']:
            f = json.loads((H.parents[1] / entry['path']).read_text())
            table = json.loads((H / 'span-tables' / (entry['table_packet_id'] + '.json')).read_text())
            path = H / 'review' / (f['fixture_id'] + '.json')
            r = json.loads(path.read_text()) if path.exists() else None
            result = v.validate_fixture(table, f, r)
            with self.subTest(fixture=f['fixture_id']):
                self.assertFalse(result['review_errors'])
                self.assertEqual({e['code'] for e in result['mechanical_errors']}, set(f['expected_mechanical_codes']))
                if result['mechanically_valid']:
                    expected = {c['component_id']: (c['expected_support_status'], c['expected_codes']) for c in f['components']}
                    self.assertEqual({c['component_id']: (c['support_status'], c['codes']) for c in result['components']}, expected)

    def test_regressions_and_coarse_support_are_explicit(self):
        ids = ['H4-f070ba17a9b7', 'H4-86f4954813b3', 'H3-4d30014ef73c', 'H3-d6134c9f4c74']
        for fid in ids:
            category = 'h3-regressions' if fid.startswith('H3') else 'h4-regressions'
            f = json.loads((H / 'fixtures' / category / (fid + '.json')).read_text())
            self.assertEqual(f['expected_complete_units'], 0 if fid == ids[0] else 1)
            self.assertEqual(f['semantic_unit_id'], 'IQ1')
            self.assertTrue(all(c['expected_support_status'] == 'SUFFICIENT' for c in f['components']))
        f = json.loads((H / 'fixtures/h3-regressions/H3-4d30014ef73c.json').read_text())
        self.assertEqual(f['components'][1]['provenance']['refs'][0], f['components'][2]['provenance']['refs'][0])


if __name__ == '__main__':
    unittest.main()
