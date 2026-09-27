import copy
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import contracts as c
import verify_preparation as prep


class ContractTests(unittest.TestCase):
    def sample(self, key='003-A'):
        return {'transfer': copy.deepcopy(c.read(c.HERE / 'examples/retrospective' /
                                                  f'{key}.json')['transfer'])}

    def reject(self, value, kind='transfer', candidate=None):
        with self.assertRaises((ValueError, c.jsonschema.ValidationError)):
            c.validate(value, kind, candidate)

    def test_all_retrospectives_are_valid_records(self):
        self.assertEqual(len(prep.verify_retrospectives()), 12)

    def test_exact_displacement_vocabulary(self):
        for label in ('Native', 'Adjacent', 'Remote'):
            value = self.sample(); value['transfer']['displacement']['class'] = label
            c.validate(value, 'transfer')
        for label in ('Alien', 'remote', 'Unknown', 3):
            value = self.sample(); value['transfer']['displacement']['class'] = label
            self.reject(value)

    def test_exact_grounding_vocabulary(self):
        for label in ('Grounded', 'Partially-grounded', 'Weakly-grounded', 'Unknown'):
            value = self.sample(); g = value['transfer']['grounding']; g['status'] = label
            for item in g['essential_counterparts']: item['grounding_status'] = label
            c.validate(value, 'transfer')
        for label in ('grounded', 'uncertain', 'Alien', ''):
            value = self.sample(); value['transfer']['grounding']['status'] = label
            self.reject(value)

    def test_validity_truth_table_all_81_combinations(self):
        criteria = {'mechanism_fidelity': ['preserved', 'conditionally-preserved', 'not-preserved'],
                    'target_fidelity': ['addressed', 'conditional', 'not-addressed'],
                    'operational_coherence': ['coherent', 'conditional', 'incoherent']}
        for levels in itertools.product(range(3), repeat=3):
            expected = 'Invalid' if 2 in levels else 'Conditional' if 1 in levels else 'Valid'
            for final in ('Valid', 'Conditional', 'Invalid'):
                with self.subTest(levels=levels, final=final):
                    v = self.sample()['transfer']['validity']
                    for (key, statuses), level in zip(criteria.items(), levels):
                        v[key]['status'] = statuses[level]
                    v['final_status'] = final
                    v['unresolved_conditions'] = ['Establish measurement specificity with controls.'] if final == 'Conditional' else []
                    value = {'case_id': 'fixture', 'validity': v, 'uncertainty': []}
                    if final == expected: c.validate(value, 'validity')
                    else: self.reject(value, 'validity')

    def test_validity_vocabulary_rejects_alternatives(self):
        for label in ('valid', 'Unknown', 'Alien', 'Provisional'):
            value = self.sample(); value['transfer']['validity']['final_status'] = label
            self.reject(value)
        for criterion in ('mechanism_fidelity', 'target_fidelity', 'operational_coherence'):
            value = self.sample(); value['transfer']['validity'][criterion]['status'] = 'unknown'
            self.reject(value)

    def test_invalid_stops_both_downstream_judgments(self):
        value = self.sample('016-A'); c.validate(value, 'transfer')
        for field in ('displacement', 'grounding'):
            bad = copy.deepcopy(value); bad['transfer'][field] = self.sample()['transfer'][field]
            self.reject(bad)
            bad = copy.deepcopy(value); del bad['transfer'][field]; self.reject(bad)

    def test_conditional_nullable_and_provisional(self):
        value = self.sample('009-A'); c.validate(value, 'transfer')
        for displacement, grounding in itertools.product((True, False), repeat=2):
            v = copy.deepcopy(value)
            if not displacement: v['transfer']['displacement'] = None
            if not grounding: v['transfer']['grounding'] = None
            c.validate(v, 'transfer')
        for field in ('displacement', 'grounding'):
            v = copy.deepcopy(value); v['transfer'][field]['provisional'] = False
            self.reject(v)

    def test_conditional_requires_specific_condition_field(self):
        for conditions in ([], [''], ['   ']):
            v = self.sample('009-A'); v['transfer']['validity']['unresolved_conditions'] = conditions
            self.reject(v)

    def test_valid_requires_complete_downstream_records(self):
        for field in ('native_baseline', 'displacement', 'grounding'):
            v = self.sample(); v['transfer'][field] = None; self.reject(v)
        for field in ('displacement', 'grounding'):
            v = self.sample(); v['transfer'][field]['provisional'] = True; self.reject(v)

    def test_valid_requires_no_unresolved_validity_conditions(self):
        v = self.sample(); v['transfer']['validity']['unresolved_conditions'] = ['Unresolved warrant.']
        self.reject(v)

    def test_displacement_requires_baseline_even_when_conditional(self):
        v = self.sample('009-A'); v['transfer']['native_baseline'] = None; self.reject(v)
        v['transfer']['displacement'] = None; c.validate(v, 'transfer')

    def test_baseline_completeness_and_identity(self):
        for field in self.sample()['transfer']['native_baseline']:
            v = self.sample(); del v['transfer']['native_baseline'][field]; self.reject(v)
        for field in ('ordinary_methods', 'ordinary_evidence'):
            v = self.sample(); v['transfer']['native_baseline'][field] = []; self.reject(v)
        for field in ('target_domain', 'target_task'):
            v = self.sample(); v['transfer']['native_baseline'][field] = 'Different task'; self.reject(v)

    def test_dimension_levels_are_actual_ordinal_integers(self):
        for level in (0, 1, 2, 3):
            v = self.sample(); v['transfer']['displacement']['dimensions']['entities']['level'] = level
            c.validate(v, 'transfer')
        for level in (-1, 4, True, 1.0, '2'):
            v = self.sample(); v['transfer']['displacement']['dimensions']['entities']['level'] = level
            self.reject(v)

    def test_exactly_seven_dimensions(self):
        v = self.sample(); del v['transfer']['displacement']['dimensions']['relations']; self.reject(v)
        v = self.sample(); v['transfer']['displacement']['dimensions']['creativity'] = {'level': 1, 'rationale': 'extra'}
        self.reject(v)

    def test_no_composite_score_or_extra_fields(self):
        for field in ('distance_score', 'creativity', 'usefulness', 'final_class'):
            v = self.sample(); v['transfer'][field] = 1; self.reject(v)
        v = self.sample(); v['transfer']['source']['instrument']['sixth_field'] = 'extra'; self.reject(v)

    def test_counterpart_entries_are_required_and_complete(self):
        v = self.sample(); v['transfer']['grounding']['essential_counterparts'] = []; self.reject(v)
        for field in self.sample()['transfer']['grounding']['essential_counterparts'][0]:
            v = self.sample(); del v['transfer']['grounding']['essential_counterparts'][0][field]
            self.reject(v)
        v = self.sample(); v['transfer']['grounding']['essential_counterparts'][0]['grounding_status'] = 'uncertain'; self.reject(v)
        v = self.sample(); v['transfer']['grounding']['essential_counterparts'].append(copy.deepcopy(v['transfer']['grounding']['essential_counterparts'][0])); self.reject(v)

    def test_grounding_claims_have_supporting_entries(self):
        v = self.sample(); v['transfer']['grounding']['essential_counterparts'][0]['grounding_status'] = 'Unknown'; self.reject(v)
        v = self.sample(); v['transfer']['grounding']['status'] = 'Weakly-grounded'; self.reject(v)

    def test_weak_grounding_does_not_force_invalid_or_remote(self):
        for label in ('Native', 'Adjacent', 'Remote'):
            v = self.sample(); t = v['transfer']; t['displacement']['class'] = label
            t['grounding']['status'] = 'Weakly-grounded'
            t['grounding']['essential_counterparts'][0]['grounding_status'] = 'Weakly-grounded'
            t['grounding']['essential_counterparts'][0]['independent_target_basis'] = 'A stipulated speculative role with no independent basis; the bounded conditional-world operation is coherent.'
            c.validate(v, 'transfer')

    def test_unknown_grounding_does_not_force_conditional(self):
        v = self.sample(); v['transfer']['grounding']['status'] = 'Unknown'
        for item in v['transfer']['grounding']['essential_counterparts']:
            item['grounding_status'] = 'Unknown'; item['independent_target_basis'] = 'Information unavailable.'
        c.validate(v, 'transfer')

    def test_reframe_false_requires_null_details(self):
        for field in ('original_question', 'reframed_question', 'relationship'):
            v = self.sample(); v['transfer']['validity']['target_reframe'][field] = 'A reframe.'
            self.reject(v)

    def test_reframe_true_requires_all_details_and_original_identity(self):
        v = self.sample('016-A'); c.validate(v, 'transfer')
        for field in ('original_question', 'reframed_question', 'relationship'):
            bad = copy.deepcopy(v); bad['transfer']['validity']['target_reframe'][field] = None
            self.reject(bad)
        v['transfer']['validity']['target_reframe']['original_question'] = 'A different original question.'
        self.reject(v)

    def test_nonblank_rationales_and_basis(self):
        v = self.sample(); v['transfer']['validity']['rationale'] = ' \t\n'; self.reject(v)
        v = self.sample(); v['transfer']['grounding']['essential_counterparts'][0]['independent_target_basis'] = ''; self.reject(v)

    def test_strict_json_loading(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'value.json'
            for text in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":-Infinity}'):
                path.write_text(text)
                with self.assertRaises(ValueError): c.read(path)

    def test_validity_only_has_no_downstream_output(self):
        t = self.sample()['transfer']; v = {k: t[k] for k in ('case_id', 'validity', 'uncertainty')}
        c.validate(v, 'validity')
        v['displacement'] = None; self.reject(v, 'validity')

    def test_candidate_binding_rejects_changed_mapping_or_id(self):
        value = self.sample(); t = value['transfer']
        candidate = {k: copy.deepcopy(t[k]) for k in ('case_id', 'source', 'target', 'mapping')}
        c.validate(value, 'transfer', candidate)
        for field in ('case_id', 'source', 'target', 'mapping'):
            bad = copy.deepcopy(value)
            if field == 'case_id': bad['transfer'][field] = 'another'
            elif field == 'source': bad['transfer'][field]['name'] = 'another'
            elif field == 'target': bad['transfer'][field]['question'] = 'another'
            else: bad['transfer'][field]['inference'] = 'another'
            self.reject(bad, candidate=candidate)

    def test_validity_response_reframe_is_bound_to_candidate(self):
        t = self.sample('016-A')['transfer']
        candidate = {k: t[k] for k in ('case_id', 'source', 'target', 'mapping')}
        value = {k: copy.deepcopy(t[k]) for k in ('case_id', 'validity', 'uncertainty')}
        c.validate(value, 'validity', candidate)
        value['validity']['target_reframe']['original_question'] = 'Different question'
        self.reject(value, 'validity', candidate)

    def test_all_packets_and_operator_contrasts(self):
        self.assertEqual(len(prep.verify_cases()), 24)

    def test_judge_packets_exclude_operator_metadata(self):
        for path in (c.HERE / 'cases').glob('*.json'):
            candidate = c.read(path)
            payload = json.loads(prep.judge_packet(candidate).split('\n\nCASE PACKET\n')[1])
            self.assertEqual(set(payload), {'case_id', 'source', 'target', 'mapping'})
            self.assertEqual(payload, candidate)
            bad = copy.deepcopy(candidate); bad['design_intent'] = 'Valid'
            with self.assertRaises(c.jsonschema.ValidationError): prep.judge_packet(bad)

    def test_historical_manifest_matches_base_git_tree(self):
        manifest = c.read(c.HERE / 'preservation.json')
        self.assertEqual(manifest['base_commit'], 'b723b8d8f53537c8cd558935aa9492c81d4df07a')
        paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', manifest['base_commit'], '--', 'distance', 'instruments', 'docs/PROBLEM_FRAMES.md'], cwd=c.ROOT, text=True).splitlines()
        self.assertEqual(set(paths), set(manifest['files']))
        self.assertEqual(manifest['historical_distance_count'], 155)
        self.assertEqual(c.verify_preservation(), 174)

    def test_external_historical_freeze_paths_cannot_be_omitted(self):
        real_read = prep.read
        def missing_external_path(path):
            value = real_read(path)
            if path.name == 'preservation.json':
                del value['files']['docs/PROBLEM_FRAMES.md']
            return value
        with patch.object(prep, 'read', side_effect=missing_external_path):
            with self.assertRaises(ValueError): prep.verify_freeze()

    def test_freeze_and_preparation_inventory(self):
        prep.verify_freeze(); prep.verify_inventory()

    def test_result_artifacts_rejected_in_preparation_state(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); here = root / 'distance/v0.3'; here.mkdir(parents=True)
            (here / 'preparation.json').write_text(json.dumps({'status': 'PREPARED / UNEXECUTED', 'files': {}}))
            (here / 'judgments').mkdir(); (here / 'judgments/result.json').write_text('{}')
            with patch.object(prep, 'HERE', here), patch.object(prep, 'ROOT', root):
                with self.assertRaises(ValueError): prep.verify_inventory()

    def test_retrospective_marker_is_enforced(self):
        real_read = prep.read
        def missing_marker(path):
            value = real_read(path)
            if path.parent.name == 'retrospective': value['status'] = 'OBSERVATION'
            return value
        with patch.object(prep, 'read', side_effect=missing_marker):
            with self.assertRaises(ValueError): prep.verify_retrospectives()


if __name__ == '__main__':
    unittest.main()
