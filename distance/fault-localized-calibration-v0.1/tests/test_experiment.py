import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import runner as r
import contracts as c

class ExperimentTests(unittest.TestCase):
    def test_full_frozen_corpus_and_claim_accounting(self):
        result = r.verify()
        self.assertEqual(len(result['cases']), 24)
        self.assertEqual(result['claims'], 91)
        self.assertEqual(len(c.read(r.H/'claims/hidden-design-links.json')), 27)

    def test_source_instruments_are_accepted_unchanged(self):
        import yaml
        instruments = [yaml.safe_load(p.read_text()) for p in (r.R/'instruments').glob('*.yaml')]
        for cid in c.read(r.H/'manifest.json')['case_order']:
            source = r.candidate(cid)['source']
            matches = [x for x in instruments if x['extraction']['name'] == source['name']]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]['extraction']['status'], 'accepted')
            self.assertEqual(matches[0]['instrument'], source['instrument'])

    def test_packet_allowlist_and_blinding(self):
        forbidden = ['intended_structural_position', 'matched_triple', 'expected_artifact_status',
                     'control_number', 'case_design', 'warrant_plausibility_audit', 'historical_judgments']
        for a in r.claims():
            packet = r.reconstructed_claim_packet(a)
            body = json.loads(packet.split('CASE PACKET\n')[1])
            self.assertEqual(set(body), {'source', 'target', 'mapping', 'atomic_claim'})
            for word in forbidden:
                self.assertNotIn(word, packet)

    def test_simultaneous_deletion_preserves_every_other_character(self):
        mapping = {'inference': 'first claim. second claim. third claim.'}
        atoms = [{'claim_id': 'C-a', 'source_field': 'mapping.inference', 'span_start': 0,
                  'span_end': 12, 'exact_claim_span': 'first claim.'},
                 {'claim_id': 'C-b', 'source_field': 'mapping.inference', 'span_start': 27,
                  'span_end': 39, 'exact_claim_span': 'third claim.'}]
        self.assertEqual(r.delete_claims(mapping, atoms)['inference'], '[DELETED C-a] second claim. [DELETED C-b]')
        self.assertEqual(mapping['inference'], 'first claim. second claim. third claim.')
        with self.assertRaises(ValueError):
            r.delete_claims(mapping, atoms + atoms[:1])

    def test_isolation_and_pinned_configuration(self):
        r.binary_check()
        command = r.command('/tmp/empty', Path('/tmp/evidence'), 'claim-warrant')
        for option in ['--ignore-user-config', '--ignore-rules', '--ephemeral', '--skip-git-repo-check']:
            self.assertIn(option, command)
        self.assertIn('gpt-6-astra', command)
        self.assertIn('model_reasoning_effort="high"', command)
        self.assertIn('project_doc_max_bytes=0', command)
        self.assertIn('web_search="disabled"', command)
        with patch.dict(r.os.environ, {'OPENAI_MODEL': 'other', 'CODEX_THREAD_ID': 'old'}):
            self.assertNotIn('OPENAI_MODEL', r.clean_env())
            self.assertNotIn('CODEX_THREAD_ID', r.clean_env())

    def test_event_tools_and_model_substitution_rejected(self):
        events = [{'type': 'thread.started', 'thread_id': 'fresh'}, {'type': 'turn.completed', 'usage': {}}]
        self.assertEqual(r.audit_events(events)['session_id'], 'fresh')
        for extra in [{'type': 'x', 'model': 'other'}, {'type': 'item.completed', 'item': {'type': 'command_execution'}}, {'type': 'error'}]:
            with self.assertRaises(ValueError):
                r.audit_events(events + [extra])

    def test_duplicate_reservation_and_terminal_state_block_before_launch(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(r, 'RT', Path(tmp)), patch.object(r, 'execute') as execute:
            r.transition('TERMINATED_MEASUREMENT', 'fixture')
            with self.assertRaises(ValueError):
                r.run('claim-warrant')
            execute.assert_not_called()
        with tempfile.TemporaryDirectory() as tmp, patch.object(r, 'RT', Path(tmp)), patch.object(r, 'execute') as execute:
            (Path(tmp)/'runs/claim-warrant/C-existing').mkdir(parents=True)
            with self.assertRaises(ValueError):
                r.run('claim-warrant')
            execute.assert_not_called()

class ArtifactTests(unittest.TestCase):
    def fixture(self):
        candidate = {'mapping': {'inference': 'Defect. Surviving evidence.'}}
        deleted = [{'claim_id': 'C-x', 'source_field': 'mapping.inference', 'span_start': 0, 'span_end': 7}]
        a = {'case_id': 'H-x', 'unsupported_claim_ids': ['C-x'],
             'mechanism_survival': {'status': 'SURVIVES', 'rationale': 'source chain'},
             'target_contribution_survival': {'status': 'SUBSTANTIALLY_SURVIVES', 'rationale': 'material contribution'},
             'dependency_cascade': {'status': 'UNCERTAIN', 'rationale': 'extent unknown', 'failed_claims': [], 'failed_actions_or_inquiries': [], 'surviving_claims': [], 'surviving_actions_or_inquiries': []},
             'remainder_check': {'status': 'DISTINCTIVE_REMAINDER', 'rationale': 'distinctive chain'},
             'strongest_surviving_target_inference': {'text': 'Surviving evidence.', 'source_spans': [{'source_field': 'mapping.inference', 'exact_text': 'Surviving evidence.'}], 'why_warranted': 'already in mapping'},
             'central_bridge': {'deleted_claim_is_required_for_all_material_contributions': 'no', 'rationale': 'independent branch'},
             'per_claim_dependencies': [{'claim_id': 'C-x', 'dependent_claims': [], 'dependent_actions_or_inquiries': [], 'rationale': 'leaf'}],
             'structural_conflict': {'present': False, 'resolved': True, 'explanation': 'no positive contradiction'},
             'artifact_status': 'KEEP_WITH_WARRANT_FLAGS', 'rationale': 'material chain survives'}
        return {'artifact_viability': a}, candidate, deleted

    def test_cascade_uncertainty_does_not_control_status(self):
        value, candidate, deleted = self.fixture()
        c.validate(value, 'ablation', 'H-x', candidate, deleted)
        a = value['artifact_viability']
        a['target_contribution_survival']['status'] = 'REDUCED_BUT_MATERIAL'
        a['artifact_status'] = 'KEEP_WITH_REDUCED_SCOPE'
        c.validate(value, 'ablation', 'H-x', candidate, deleted)

    def test_unresolved_conflict_is_valid_including_hard_failure(self):
        value, candidate, deleted = self.fixture(); a = value['artifact_viability']
        a['dependency_cascade']['status'] = 'GLOBAL'
        with self.assertRaises(ValueError): c.validate(value, 'ablation', 'H-x', candidate, deleted)
        a['structural_conflict'] = {'present': True, 'resolved': False, 'explanation': 'unreconciled dimensions'}
        a['artifact_status'] = 'UNCERTAIN_LOAD_BEARING'; a['rationale'] = 'unresolved structural contradiction'
        c.validate(value, 'ablation', 'H-x', candidate, deleted)
        a['mechanism_survival']['status'] = 'DOES_NOT_SURVIVE'
        c.validate(value, 'ablation', 'H-x', candidate, deleted)

    def test_no_survivor_is_representable_and_deleted_citation_rejected(self):
        value, candidate, deleted = self.fixture(); a = value['artifact_viability']
        a['strongest_surviving_target_inference']['source_spans'][0]['exact_text'] = 'Defect.'
        with self.assertRaises(ValueError): c.validate(value, 'ablation', 'H-x', candidate, deleted)
        a['strongest_surviving_target_inference'] = {'text': None, 'source_spans': [], 'why_warranted': 'No material inference survives.'}
        a['target_contribution_survival']['status'] = 'NO_MATERIAL_CONTRIBUTION'; a['artifact_status'] = 'CORE_INVALID'
        c.validate(value, 'ablation', 'H-x', candidate, deleted)

if __name__ == '__main__': unittest.main()
