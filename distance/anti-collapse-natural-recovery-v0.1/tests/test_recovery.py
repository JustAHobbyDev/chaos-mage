import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('recovery_under_test', HERE / 'runner.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
e = r.e


class RecoveryTests(unittest.TestCase):
    def test_project_pin(self):
        import tomllib
        config = tomllib.loads((e.ROOT / 'mise.toml').read_text())
        self.assertEqual(config['tools']['npm:@openai/codex'], '0.157.1')

    def test_history_and_preparation_preserved(self):
        r.verify(private=True)

    def test_exact_corrections_only(self):
        self.assertEqual({v['case_id'] for v in e.read(HERE / 'lexical-corrections.json')['cases']}, {'E027', 'E029', 'E030'})
        for entry in r.imports('generation'):
            payload = e.read(e.public_path('generation', entry))
            r.validate_response(payload, 'generation', entry)
            original = entry['recovery_import']['original_validation']['status']
            self.assertEqual(entry['recovery_import']['lexical_correction'], original == 'excluded')
            modified = json.loads(json.dumps(payload))
            modified['mapping']['operation'] += ' This mapping is novel and creative.'
            with self.assertRaises(ValueError):
                r.validate_response(modified, 'generation', entry)

    def test_import_counts(self):
        self.assertEqual([len(r.imports(s)) for s in ('generation', 'neutralization', 'audit')], [30, 27, 21])
        self.assertEqual(len(e.successful_ids('generation')), 30)

    def test_pending_neutralizations(self):
        self.assertEqual({v['case_id'] for v in r.pending('neutralization')}, {'E027', 'E029', 'E030'})
        expected = [v for v in e.planned('neutralization') if v['case_id'] in {'E027', 'E029', 'E030'}]
        self.assertEqual(r.pending('neutralization'), expected)

    def test_completed_audits_never_repeated(self):
        with patch.object(e, 'successful_ids', return_value={v['case_id'] for v in e.manifest()}):
            pending = r.pending('audit')
        self.assertEqual(len(pending), 39)
        self.assertFalse({v['id'] for v in pending} & {v['id'] for v in r.imports('audit')})
        self.assertIn('audit-E021-A', {v['id'] for v in pending})
        expected = [v for v in e.planned('audit') if v['id'] not in {x['id'] for x in r.imports('audit')}]
        self.assertEqual(pending, expected)

    def test_no_generation_schedule(self):
        with self.assertRaisesRegex(ValueError, 'cannot generate'):
            r.pending('generation')

    def test_pause_blocks_all_provider_entrypoints_before_side_effects(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(r, 'HERE', Path(directory)), patch.object(r, 'original_preflight') as probe, patch.object(r, 'original_run') as run, patch.object(r, 'original_execute') as execute, patch.object(r, 'binaries') as binaries:
            for stage in r.STAGES:
                for function in (r.preflight, r.run_all):
                    with self.assertRaisesRegex(ValueError, 'PAUSED'):
                        function(stage)
                with self.assertRaisesRegex(ValueError, 'PAUSED'):
                    r.execute('A', Path('/unused'), 'unused', stage)
            probe.assert_not_called(); run.assert_not_called(); execute.assert_not_called(); binaries.assert_not_called()

    def test_generation_cannot_launch_even_if_authorized(self):
        with patch.object(r, 'execution_authorized'), patch.object(r, 'original_execute') as execute:
            with self.assertRaisesRegex(ValueError, 'cannot generate'):
                r.execute('A', Path('/unused'), 'unused', 'generation')
            execute.assert_not_called()

    def test_executables_absolute_and_version_specific(self):
        for family in 'AB':
            with tempfile.TemporaryDirectory() as cwd:
                command = r.build_command(family, cwd, Path('/tmp/recovery-test'), 'test-session', 'audit')
                self.assertTrue(Path(command[0]).is_absolute())
                self.assertNotIn('latest', Path(command[0]).parts)
                self.assertEqual(command[0], e.config()['families'][family]['cli'])
                self.assertEqual(list(Path(cwd).iterdir()), [])

    def test_binary_version_drift_rejected(self):
        with patch.object(subprocess, 'check_output', return_value='different CLI version'):
            with self.assertRaisesRegex(ValueError, 'CLI version changed'):
                r.binaries()

    def test_binary_hash_drift_rejected(self):
        with patch.object(e.c, 'sha', return_value='changed'), patch.object(subprocess, 'check_output') as proc:
            with self.assertRaisesRegex(ValueError, 'Pinned executable changed'):
                r.binaries()
            proc.assert_not_called()

    def test_sessions_checked_against_original_run(self):
        session = r.imports('generation')[0]['validation']['metadata']['session_id']
        with self.assertRaisesRegex(ValueError, 'Session reused'):
            r.check_fresh_session(session, Path('/unused'))

    def test_preparation_records_pause_without_execution_authorization(self):
        prepared = e.read(HERE / 'prepared.json')
        self.assertEqual(prepared['state'], 'paused before all provider calls')
        self.assertNotIn(str((HERE / 'execution-authorization.json').relative_to(e.ROOT)), prepared['files'])
        self.assertTrue((r.ORIGINAL_RUNTIME / 'STOP.json').exists())

    def test_classifiers_and_docs_unchanged(self):
        for name in e.DOCS.values():
            self.assertEqual((HERE / name).read_bytes(), (r.ORIGINAL / name).read_bytes())

    def test_neutralizer_blindness(self):
        for item in r.pending('neutralization'):
            packet = e.packet_body('neutralization', item['case_id'])
            self.assertEqual(set(packet), {'case_id', 'target_question', 'mapping'})
            self.assertEqual(packet['mapping'], e.single('generation', item['case_id'])['mapping'])

    def test_neutralization_wording_ban_unchanged(self):
        for word in e.BANNED:
            value = e.probe_response('neutralization')
            value['source_neutral']['procedure'] = 'This is ' + word
            with self.assertRaisesRegex(ValueError, 'evaluative wording'):
                r.validate_response(value, 'neutralization')

    def test_admission_minimum_unchanged(self):
        cases = [{'case_id': str(i), 'target_id': str(i % 5), 'admitted': True} for i in range(18)]
        self.assertTrue(e.viability(cases)['viable'])
        self.assertFalse(e.viability(cases[:-1])['viable'])
        self.assertFalse(e.viability([{**v, 'target_id': 'one'} for v in cases])['viable'])

    def test_gate_statuses_unchanged(self):
        self.assertEqual(set(e.c.STATUSES), {'CLEAR_COLLAPSE', 'SUFFICIENT_DEPARTURE', 'BORDERLINE_KEEP'})

    def test_validity_and_both_audits_required(self):
        audits = {('fixture', f): {'overall': 'pass'} for f in 'AB'}
        validity = {('fixture', f): {'validity': {'final_status': 'Valid', 'unresolved_conditions': []}} for f in 'AB'}
        with patch.object(e, 'manifest', return_value=[{'case_id': 'fixture', 'target_id': 'fixture-target'}]), patch.object(e, 'successful_ids', return_value={'fixture'}), patch.object(e, 'published', side_effect=lambda stage: audits if stage == 'audit' else validity):
            self.assertTrue(e.derive_admission()[0]['admitted'])
            for status in ('Conditional', 'Invalid'):
                validity[('fixture', 'B')]['validity']['final_status'] = status
                self.assertFalse(e.derive_admission()[0]['admitted'])
            validity[('fixture', 'B')]['validity']['final_status'] = 'Valid'
            validity[('fixture', 'B')]['validity']['unresolved_conditions'] = ['fixture condition']
            self.assertFalse(e.derive_admission()[0]['admitted'])
            validity[('fixture', 'B')]['validity']['unresolved_conditions'] = []
            audits[('fixture', 'A')]['overall'] = 'exclude'
            row = e.derive_admission()[0]
            self.assertFalse(row['admitted'])
            self.assertTrue(row['valid_valid'])
            self.assertEqual(row['exclusion_reasons'], ['neutralization-audit-exclusion'])

    def test_combined_freeze_preserves_import_and_new_payload_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            local = root / 'recovery'
            runtime = root / 'runtime'
            reused = {'id': 'audit-fixture-A', 'case_id': 'fixture', 'family': 'A', 'original_provenance': 'unchanged'}
            run = {'id': 'audit-fixture-B', 'case_id': 'fixture', 'family': 'B'}
            call = runtime / 'audit' / run['id']
            payload = e.probe_response('audit')
            payload['case_id'] = 'fixture'
            e.write_new(call / 'response.json', payload)
            e.write_new(call / 'reservation.json', {'input_commit': 'probe-checkpoint'})
            e.write_new(call / 'validation.json', {'status': 'valid'})
            e.copy_new(call / 'prompt.txt', b'fixture packet')
            e.write_new(runtime / 'audit-reservation.json', {'commit': 'probe-checkpoint'})
            e.write_new(local / 'prepared.json', {})
            e.write_new(local / 'stage-inputs/audit.json', {})
            with patch.object(r, 'HERE', local), patch.object(e, 'HERE', local), patch.object(e, 'ROOT', root), patch.object(e, 'RUNTIME', runtime), patch.object(e, 'prerequisites'), patch.object(r, 'imports', return_value=[reused]), patch.object(r, 'pending', return_value=[run]), patch.object(r, 'original_order', return_value=[reused, run]), patch.object(e, 'packet', return_value='fixture packet'):
                r.freeze('audit')
                frozen = e.read(local / 'audit-freeze.json')
                self.assertEqual(frozen['runs'][0], reused)
                self.assertEqual(frozen['imported_run_ids'], [reused['id']])
                self.assertEqual(frozen['recovery_execution_commit'], 'probe-checkpoint')
                self.assertEqual((local / 'neutralization-audit' / (run['id'] + '.json')).read_bytes(), (call / 'response.json').read_bytes())
                with self.assertRaises(FileExistsError):
                    r.freeze('audit')

    def test_missing_upstream_freeze_blocks_audit_packet_preparation(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(e, 'HERE', Path(directory)), patch.object(e, 'verify'), patch.object(e, 'checkpoint', side_effect=FileNotFoundError('neutralization-freeze.json')), patch.object(e, '_write_stage_inputs') as write:
            with self.assertRaises(FileNotFoundError):
                e.prepare_stage('audit')
            write.assert_not_called()


if __name__ == '__main__':
    unittest.main()
