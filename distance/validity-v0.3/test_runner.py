import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('validity_runner', Path(__file__).with_name('runner.py'))
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


class RunnerTests(unittest.TestCase):
    def sample(self, status='Valid', case_id='001'):
        value = copy.deepcopy(r.probe_response()); value['case_id'] = case_id
        value['validity']['final_status'] = status
        if status == 'Conditional':
            value['validity']['operational_coherence']['status'] = 'conditional'
            value['validity']['unresolved_conditions'] = ['Validate a discriminating probe using controls.']
        elif status == 'Invalid':
            value['validity']['mechanism_fidelity']['status'] = 'not-preserved'
        return value

    def test_snapshot_and_wire_projection(self):
        r.validate_inputs()
        original = r.read(r.SNAPSHOT / 'validity.schema.json')
        projected = r.read(r.HERE / 'wire.schema.json')
        self.assertEqual(projected, r.projection(original))
        for status in r.STATUSES:
            value = self.sample(status)
            r.c.validate(value, 'validity', r.candidate('001'))
            r.c.jsonschema.validate(value, projected)

    def test_wire_does_not_override_canonical_cross_field_checks(self):
        value = self.sample(); value['validity']['final_status'] = 'Invalid'
        r.c.jsonschema.validate(value, r.read(r.HERE / 'wire.schema.json'))
        with self.assertRaises(r.c.jsonschema.ValidationError): r.c.validate(value, 'validity')

    def test_packet_identity_and_no_operator_metadata(self):
        for run in r.order():
            prompt = r.packet(run)
            self.assertEqual(prompt, r.preparation.judge_packet(r.candidate(run['case_id'])))
            value = json.loads(prompt.split('\n\nCASE PACKET\n')[1])
            self.assertEqual(set(value), {'case_id', 'source', 'target', 'mapping'})
            other = dict(run, family='B' if run['family'] == 'A' else 'A')
            self.assertEqual(r.packet(other), prompt)

    def test_commands_request_isolation(self):
        a = r.build_command('A', '/tmp/empty', Path('/tmp/output'), 'session')
        for flag in ('--ignore-user-config', '--ignore-rules', '--ephemeral', '--skip-git-repo-check'):
            self.assertIn(flag, a)
        self.assertIn('project_doc_max_bytes=0', a)
        self.assertIn('web_search="disabled"', a)
        for feature in ('shell_tool', 'apps', 'plugins', 'memories', 'multi_agent', 'hooks'):
            self.assertIn(feature, a)
        b = r.build_command('B', '/tmp/empty', Path('/tmp/output'), 'session')
        for flag in ('--safe-mode', '--strict-mcp-config', '--disable-slash-commands', '--no-session-persistence'):
            self.assertIn(flag, b)
        self.assertEqual(b[b.index('--tools') + 1], '')
        self.assertEqual(b[b.index('--setting-sources') + 1], '')
        settings = json.loads(b[b.index('--settings') + 1])
        self.assertTrue(settings['disableAllHooks'])
        self.assertFalse(settings['autoMemoryEnabled'])
        self.assertTrue(all(x is False for x in settings['enabledPlugins'].values()))

    def test_parent_and_provider_overrides_removed(self):
        environment = {'PATH': '/bin', 'HOME': '/tmp/auth-owner', 'CODEX_THREAD_ID': 'old',
                       'OPENAI_MODEL': 'wrong', 'ANTHROPIC_MODEL': 'wrong',
                       'CLAUDECODE': 'old', 'CLAUDE_SESSION_ID': 'old'}
        with patch.dict(r.os.environ, environment, clear=True):
            self.assertEqual(r.clean_environment(), {'PATH': '/bin', 'HOME': '/tmp/auth-owner'})

    def test_exclusive_writes(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'file.json'; r.write_new(path, {'one': 1})
            with self.assertRaises(FileExistsError): r.write_new(path, {'two': 2})
            self.assertEqual(r.read(path), {'one': 1})

    def test_invalid_transfer_is_a_valid_response(self):
        r.c.validate(self.sample('Invalid'), 'validity', r.candidate('001'))

    def test_status_metric_preserves_nominal_confusion(self):
        pairs = [(self.sample('Valid'), self.sample('Valid')),
                 (self.sample('Conditional'), self.sample('Invalid'))]
        metrics = r.metrics(pairs)
        self.assertEqual(metrics['final_status'], {'agreements': 1, 'pairs': 2, 'rate': .5})
        self.assertEqual(metrics['confusion_rows_A_columns_B']['Conditional']['Invalid'], 1)
        self.assertEqual(metrics['criteria']['target_fidelity']['agreements'], 2)
        self.assertEqual(metrics['planned_pairs'], 24)
        self.assertNotIn('distance', metrics)
        self.assertIsNone(r.metrics([])['final_status']['rate'])

    def test_run_coverage_and_unique_sessions(self):
        entries = [{**run, 'audit': {'metadata': {'session_id': run['id']}}} for run in r.order()]
        probes = {'families': {'A': {'metadata': {'session_id': 'probe-A'}},
                              'B': {'metadata': {'session_id': 'probe-B'}}}}
        schedule = r.order()
        with patch.object(r, 'read', return_value=probes), patch.object(r, 'order', return_value=schedule):
            r.check_runs(entries)
            with self.assertRaises(ValueError): r.check_runs(entries[:-1])
            duplicate = copy.deepcopy(entries); duplicate[-1]['audit'] = duplicate[0]['audit']
            with self.assertRaises(ValueError): r.check_runs(duplicate)
            duplicate[-1]['audit'] = {'metadata': {'session_id': 'probe-A'}}
            with self.assertRaises(ValueError): r.check_runs(duplicate)

    def test_scheduler_stops_and_cannot_repeat(self):
        with tempfile.TemporaryDirectory() as td, patch.object(r, 'RUNTIME', Path(td)), \
             patch.object(r, 'verify'), patch.object(r, 'git', return_value=b'commit'), \
             patch.object(r.subprocess, 'check_output', side_effect=['codex-cli 0.157.0', '2.1.282 (Claude Code)', 'codex-cli 0.157.0', '2.1.282 (Claude Code)']), \
             patch.object(r, 'execute', return_value={'status': 'failed', 'error': 'fixture failure'}) as execute:
            with self.assertRaises(ValueError): r.run_all()
            self.assertEqual(execute.call_count, 1)
            self.assertTrue((Path(td) / 'STOP.json').exists())
            with self.assertRaises(FileExistsError): r.run_all()
            self.assertEqual(execute.call_count, 1)

    def test_timeout_preserves_attempt_and_kills_group(self):
        class Process:
            pid = 999999
            def communicate(self, *args, **kwargs): raise subprocess.TimeoutExpired('fixture', 900)
            def wait(self): return -9
        with tempfile.TemporaryDirectory() as td, patch.object(r.subprocess, 'Popen', return_value=Process()), \
             patch.object(r.subprocess, 'check_output', return_value='codex-cli 0.157.0'), \
             patch.object(r, 'git', return_value=b'commit'), patch.object(r.os, 'killpg') as kill:
            result = r.execute('A', Path(td) / 'attempt', 'fixture')
            self.assertEqual(result['status'], 'failed')
            self.assertIn('TimeoutExpired', result['error'])
            kill.assert_called_once()
            self.assertTrue((Path(td) / 'attempt/reservation.json').exists())
            self.assertTrue((Path(td) / 'attempt/validation.json').exists())

    def claude_events(self, value):
        return [{'type': 'system', 'subtype': 'init', 'session_id': 'session',
                 'model': 'claude-fable-5-1', 'tools': ['StructuredOutput'], 'plugins': [], 'mcp_servers': []},
                {'type': 'assistant', 'message': {'model': 'claude-fable-5-1',
                 'content': [{'type': 'tool_use', 'name': 'StructuredOutput', 'input': value}]}},
                {'type': 'result', 'subtype': 'success', 'session_id': 'session', 'structured_output': value,
                 'modelUsage': {'claude-fable-5-1': {}}, 'num_turns': 2}]

    def test_event_audit_rejects_tools_plugins_fallback_and_mismatch(self):
        for change in ('tool', 'plugin', 'model', 'session'):
            events = self.claude_events(self.sample())
            if change == 'tool': events[0]['tools'].append('Read')
            if change == 'plugin': events[0]['plugins'].append('unexpected')
            if change == 'model': events[1]['message']['model'] = 'another-model'
            if change == 'session': events[0]['session_id'] = 'another-session'
            with self.assertRaises(ValueError):
                r.legacy.audit_events(events, 'B', 'claude-fable-5-1[1m]', 'session')

    def test_internal_formatter_retries_are_retained(self):
        events = self.claude_events(self.sample()); events.insert(2, copy.deepcopy(events[1]))
        metadata, payload = r.legacy.audit_events(events, 'B', 'claude-fable-5-1[1m]', 'session')
        self.assertEqual(metadata['formatting_retries']['observed_formatting_retries'], 1)
        self.assertEqual(payload, self.sample())

    def test_response_retained_before_canonical_failure(self):
        invalid = self.sample(); invalid['validity']['final_status'] = 'Invalid'
        events = self.claude_events(invalid)
        class Process:
            returncode = 0
            def communicate(self, *args, **kwargs): pass
        def popen(*args, **kwargs):
            kwargs['stdout'].write('\n'.join(json.dumps(e) for e in events) + '\n')
            kwargs['stdout'].flush()
            return Process()
        with tempfile.TemporaryDirectory() as td, patch.object(r.subprocess, 'Popen', side_effect=popen), \
             patch.object(r.subprocess, 'check_output', return_value='2.1.282 (Claude Code)'), \
             patch.object(r, 'git', return_value=b'commit'), patch.object(r.uuid, 'uuid4', return_value='session'):
            directory = Path(td) / 'attempt'
            result = r.execute('B', directory, 'fixture', {'case_id': '001'})
            self.assertEqual(result['status'], 'failed')
            self.assertIn('ValidationError', result['error'])
            self.assertEqual(r.read(directory / 'response.json'), invalid)
            self.assertTrue((directory / 'events.jsonl').exists())

    def test_commit_gate_checks_actual_file_bytes(self):
        # No mocked validator: prepared inputs are checked by the real verifier when available.
        if not (r.HERE / 'prepared.json').exists(): self.skipTest('Preparation manifest not generated yet')
        with patch.object(r, 'git', return_value=b'not the committed bytes'):
            with self.assertRaisesRegex(ValueError, 'Uncommitted input'): r.verify(committed=True)


if __name__ == '__main__': unittest.main()
