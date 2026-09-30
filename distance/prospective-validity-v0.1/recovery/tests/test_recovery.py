from pathlib import Path
from unittest.mock import patch
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import continuation as r
import evidence as e
c, old = e.c, e.old


class EvidenceTests(unittest.TestCase):
    def test_original_publication_and_stop_preserved(self):
        self.assertTrue(e.preservation()['original_runtime_unchanged'])

    def test_ten_gate_measurement_evidence(self):
        result = e.audit()
        self.assertEqual(result, c.read(e.HERE / 'initial-audit.json'))
        self.assertEqual(result['classification'], 'recoverable_integrity_violation')
        self.assertEqual([x['identity'] for x in result['measurements']], ['ARTIFICIAL','Q0020','Q0032','Q0185','Q0135'])
        self.assertEqual(result['resume_from'], 'Q0094')
        self.assertFalse(result['measurement_dependency_audit']['model_context_exposure'])

    def test_policy_and_archive_preserved(self):
        self.assertIn('Pause on invariant violation', e.POLICY.read_text())
        fix = c.read(e.F / 'review/preservation-correction.json')
        self.assertEqual(c.sha(e.ROOT / fix['historical_path']), fix['restored_sha256'])
        self.assertEqual(c.sha(e.ROOT / fix['executed_preparation_document_archive']), fix['executed_preparation_sha256'])

    def test_prompt_tamper_rejected(self):
        sha = c.sha
        with patch.object(c, 'sha', side_effect=lambda p: '0'*64 if str(p).endswith('Q0020/prompt.txt') else sha(p)):
            with self.assertRaises(ValueError): e.audit()

    def test_schema_tamper_rejected(self):
        sha = c.sha
        with patch.object(c, 'sha', side_effect=lambda p: '0'*64 if str(p).endswith('schemas/taxonomy.schema.json') else sha(p)):
            with self.assertRaises(ValueError): e.audit()

    def test_response_tamper_rejected(self):
        sha = c.sha
        with patch.object(c, 'sha', side_effect=lambda p: '0'*64 if str(p).endswith('Q0020/response.json') else sha(p)):
            with self.assertRaises(ValueError): e.audit()

    def test_unknown_or_nonrecoverable_classification_rejected(self):
        for classification in ('unknown', 'measurement_lineage_violation', 'ambiguous_impact'):
            with self.assertRaises(ValueError): e.gate({'classification': classification})

    def test_legacy_diff_scope_does_not_hide_live_tampering(self):
        with patch.object(e, 'preservation', side_effect=ValueError('tampered')):
            with self.assertRaisesRegex(ValueError, 'tampered'): e.legacy_check()


class StateTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for target, name, value in ((r, 'RUNTIME', self.root), (old, 'rel', lambda p: str(p)), (old, 'head', lambda: 'fixture-commit')):
            p = patch.object(target, name, value); p.start(); self.addCleanup(p.stop)
        self.record = self.root / 'record.json'
        old.write(self.record, {'classification': 'recoverable_integrity_violation'})

    def start(self):
        with patch.object(old, 'committed'): r.transition('RUNNING', 'fixture', self.record)

    def test_defaults_to_paused(self):
        self.assertEqual(r.state(), 'PAUSED_AMBIGUOUS')
        with self.assertRaises(ValueError): r.running()

    def test_resume_needs_committed_evidence(self):
        with patch.object(old, 'committed', side_effect=ValueError('not committed')):
            with self.assertRaisesRegex(ValueError, 'not committed'): r.transition('RUNNING', 'fixture', self.record)
        with self.assertRaises(ValueError): r.transition('RUNNING', 'fixture')

    def test_recoverable_pause_and_append_only_clearance(self):
        self.start(); before = (self.root / 'state/0000.json').read_bytes()
        r.transition('PAUSED_RECOVERABLE', 'fixture bookkeeping')
        self.start()
        self.assertEqual(r.state(), 'RUNNING')
        self.assertEqual((self.root / 'state/0000.json').read_bytes(), before)

    def test_lineage_and_provider_terminal_cannot_clear(self):
        for target in ('TERMINATED_LINEAGE', 'TERMINATED_MEASUREMENT', 'COMPLETE'):
            with tempfile.TemporaryDirectory() as tmp, patch.object(r, 'RUNTIME', Path(tmp)):
                r.transition(target, 'fixture')
                with self.assertRaises(ValueError): self.start()
                with self.assertRaises(ValueError): r.recover(self.record)

    def test_state_tampering_rejected(self):
        self.start(); r.transition('PAUSED_AMBIGUOUS', 'fixture')
        path = self.root / 'state/0001.json'; row = c.read(path); row['previous_sha256'] = '0'*64
        path.write_text(json.dumps(row))
        with self.assertRaises(ValueError): r.state()

    def test_nonrecoverable_evidence_cannot_run(self):
        self.record.write_text(json.dumps({'classification': 'measurement_lineage_violation'}))
        with patch.object(old, 'committed'):
            with self.assertRaises(ValueError): r.transition('RUNNING', 'fixture', self.record)

    def test_initial_record_cannot_clear_later_pause(self):
        self.start(); r.transition('PAUSED_RECOVERABLE', 'later incident')
        with patch.object(old, 'committed'), patch.object(e, 'gate'):
            with self.assertRaisesRegex(ValueError, 'later incidents'): r.resume(self.record)


class ScheduleTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        p = patch.object(r, 'RUNTIME', self.root); p.start(); self.addCleanup(p.stop)

    def reserve(self, identity, valid=True, timestamp='2026-09-30T12:00:00+00:00'):
        p = self.root / 'runs/taxonomy' / identity
        p.mkdir(parents=True)
        old.write(p / 'attempt.json', {'at': timestamp, 'identity': identity, 'harness_attempt': 1})
        if valid: old.write(p / 'validation.json', {'status': 'valid'})
        return p

    def test_resume_next_original_id(self): self.assertEqual(r.next_identity('taxonomy'), 'Q0094')

    def test_retained_ids_never_execute(self):
        with patch.object(r, 'running'), patch.object(r, 'verify_inputs'), patch.object(old, 'binary_check'), patch.object(r.subprocess, 'Popen') as process:
            for identity in ('Q0020', 'Q0032', 'Q0185', 'Q0135'):
                with self.assertRaises(ValueError): r.execute('taxonomy', identity)
            process.assert_not_called()

    def test_duplicate_reservation_rejected(self):
        self.reserve('Q0020')
        with self.assertRaisesRegex(ValueError, 'Duplicate'): r.next_identity('taxonomy')

    def test_schedule_reshuffle_rejected(self):
        self.reserve(old.order('taxonomy')[5])
        with self.assertRaisesRegex(ValueError, 'prefix'): r.next_identity('taxonomy')

    def test_measured_prefix_advances_once(self):
        self.reserve('Q0094')
        self.assertEqual(r.next_identity('taxonomy'), old.order('taxonomy')[5])

    def test_unknown_attempt_blocks(self):
        self.reserve('Q0094', False)
        with self.assertRaisesRegex(ValueError, 'Unresolved'): r.next_identity('taxonomy')

    def test_uncertain_launch_not_recoverable(self):
        directory = self.reserve('Q0094', False)
        old.write(directory / 'launch-intent.json', {})
        self.assertFalse(r.unlaunched(directory))

    def test_prelaunch_proof_retains_single_reservation(self):
        directory = self.reserve('Q0094', False)
        self.assertTrue(r.unlaunched(directory))
        old.write(directory / 'launch-intent.json', {})
        old.write(directory / 'not-launched.json', {})
        self.assertTrue(r.unlaunched(directory))
        old.write(directory / 'process.json', {'pid': 123})
        self.assertFalse(r.unlaunched(directory))

    def test_no_taxonomy_probe_replay(self):
        with patch.object(r, 'running'), patch.object(r, 'verify_inputs'):
            with self.assertRaisesRegex(ValueError, 'already measured'): r.execute('taxonomy', 'ARTIFICIAL', 'probes')

    def test_no_E_anti_collapse_or_other_stage(self):
        for stage in ('generation', 'neutralization', 'anti-collapse', 'Experiment E'):
            with self.assertRaisesRegex(ValueError, 'Unauthorized stage'): r.verify_inputs(stage)

    def test_prechecks_precede_execution(self):
        with patch.object(r, 'running'), patch.object(r, 'state', return_value='PAUSED_AMBIGUOUS'), patch.object(r, 'history_before_stage', side_effect=ValueError('history failed')), patch.object(r, 'execute') as execute:
            with self.assertRaisesRegex(ValueError, 'history failed'): r.run('taxonomy')
            execute.assert_not_called()

    def test_original_launch_configuration_preserved(self):
        cmd = r.command('/tmp/empty', Path('/tmp/output'), 'taxonomy')
        self.assertEqual(cmd, old.command('/tmp/empty', Path('/tmp/output'), 'taxonomy'))
        self.assertEqual(cmd[cmd.index('--model')+1], 'gpt-6-astra')
        self.assertIn('model_reasoning_effort="high"', cmd)
        self.assertIn('--ephemeral', cmd)


class ExecutionFixtureTests(unittest.TestCase):
    """Synthetic provider adapter, no network/model call or case answer key."""
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.runtime = Path(temp.name)
        self.identity = 'ARTIFICIAL-NEXT'
        self.value = old.probe_fixture('taxonomy'); self.value['condition_id'] = self.identity
        self.events = [{'type':'thread.started','thread_id':'fixture-session'},
                       {'type':'turn.started'},
                       {'type':'item.completed','item':{'type':'agent_message','text':json.dumps(self.value)}},
                       {'type':'turn.completed','usage':{'input_tokens':1,'output_tokens':1}}]
        for target, name, value in ((r, 'RUNTIME', self.runtime), (r, 'running', lambda: None),
            (r, 'verify_inputs', lambda *a, **k: None), (r, 'next_identity', lambda stage: self.identity),
            (r, 'packet', lambda *a: 'artificial packet'), (old, 'binary_check', lambda: 'codex-cli 0.157.1'),
            (old, 'rel', lambda p: str(p)), (r, 'transition', lambda *a: None), (r, 'state', lambda: 'RUNNING')):
            p = patch.object(target, name, value); p.start(); self.addCleanup(p.stop)
        p = patch.object(old, 'head', return_value='fixture-commit'); p.start(); self.addCleanup(p.stop)

    def fake_popen(self, cmd, **kwargs):
        owner = self
        class Process:
            pid = 999999; returncode = 0
            def communicate(self, prompt, timeout):
                self.prompt, self.timeout = prompt, timeout
                kwargs['stdout'].write('\n'.join(json.dumps(e) for e in owner.events)+'\n')
                Path(cmd[cmd.index('--output-last-message')+1]).write_text(json.dumps(owner.value))
        return Process()

    def test_success_captures_exact_response_and_fresh_configuration(self):
        with patch.object(r.subprocess, 'Popen', side_effect=self.fake_popen) as provider:
            directory = r.execute('taxonomy', self.identity)
        self.assertEqual(c.read(directory/'validation.json')['status'], 'valid')
        self.assertEqual(c.read(directory/'response.json'), self.value)
        self.assertEqual(provider.call_count, 1)
        self.assertTrue(provider.call_args.kwargs['start_new_session'])
        self.assertTrue((directory/'response-capture.json').exists())

    def test_malformed_observation_is_terminal_without_retry(self):
        self.value['category'] = 'not-a-category'
        self.events[2]['item']['text'] = json.dumps(self.value)
        with patch.object(r.subprocess, 'Popen', side_effect=self.fake_popen) as provider, patch.object(r, 'transition') as state:
            with self.assertRaises(r.MeasurementFailure): r.execute('taxonomy', self.identity)
        self.assertEqual(provider.call_count, 1)
        self.assertEqual(state.call_args.args[0], 'TERMINATED_MEASUREMENT')
        self.assertEqual(c.read(self.runtime/'runs/taxonomy'/self.identity/'response.json'), self.value)

    def test_prelaunch_oserror_is_recoverable_and_preserved(self):
        with patch.object(r.subprocess, 'Popen', side_effect=OSError(2, 'fixture executable unavailable')), patch.object(r, 'transition') as state:
            with self.assertRaises(OSError): r.execute('taxonomy', self.identity)
        directory = self.runtime/'runs/taxonomy'/self.identity
        self.assertTrue(r.unlaunched(directory))
        self.assertTrue((directory/'not-launched.json').exists())
        self.assertEqual(state.call_args.args[0], 'PAUSED_RECOVERABLE')

    def test_bookkeeping_failure_keeps_raw_response_and_pauses(self):
        write = old.write
        def broken(path, value):
            if path.name == 'response-capture.json': raise OSError('fixture accounting disk failure')
            return write(path, value)
        with patch.object(r.subprocess, 'Popen', side_effect=self.fake_popen) as provider, patch.object(old, 'write', side_effect=broken), patch.object(r, 'transition') as state:
            with self.assertRaises(OSError): r.execute('taxonomy', self.identity)
        directory = self.runtime/'runs/taxonomy'/self.identity
        self.assertEqual(c.read(directory/'response.json'), self.value)
        self.assertEqual(provider.call_count, 1)
        self.assertEqual(state.call_args.args[0], 'PAUSED_AMBIGUOUS')

    def test_bookkeeping_recovery_preserves_failed_validation_and_response(self):
        write = old.write
        def broken(path, value):
            if path.name == 'response-capture.json': raise OSError('fixture accounting disk failure')
            return write(path, value)
        with patch.object(r.subprocess, 'Popen', side_effect=self.fake_popen), patch.object(old, 'write', side_effect=broken):
            with self.assertRaises(OSError): r.execute('taxonomy', self.identity)
        directory = self.runtime/'runs/taxonomy'/self.identity
        original = (directory/'validation.json').read_bytes(); response = (directory/'response.json').read_bytes()
        latest = self.runtime/'state/0000.json'; old.write(latest, {'state':'PAUSED_AMBIGUOUS'})
        record = self.runtime/'recovery-record.json'
        old.write(record, {'classification':'recoverable_integrity_violation','incident_sha256':c.sha(latest),
            'authorization':old.rel(e.HERE/'AUTHORIZATION.md'),'remediation':'Fixture accounting repair',
            'files':old.inventory((self.runtime/'runs').rglob('*')),'stage':'taxonomy'})
        with patch.object(r, 'state', return_value='PAUSED_AMBIGUOUS'), patch.object(old, 'committed'), patch.object(e, 'history'), patch.object(r, 'transition') as transition:
            r.recover(record)
        self.assertEqual((directory/'validation.json').read_bytes(), original)
        self.assertEqual((directory/'response.json').read_bytes(), response)
        self.assertEqual(c.read(directory/'validation-recovery.json')['status'], 'valid')
        self.assertEqual(transition.call_args.args[0], 'RUNNING')


if __name__ == '__main__': unittest.main()
