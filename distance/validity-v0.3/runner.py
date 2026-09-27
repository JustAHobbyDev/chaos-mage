#!/usr/bin/env python3
"""Isolated execution of frozen Experiment A; no repair or automatic retry."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SNAPSHOT = ROOT / 'distance/v0.3'
RUNTIME = ROOT / '.runtime/validity-v0.3'
sys.path.insert(0, str(SNAPSHOT))
import contracts as c
import verify_preparation as preparation

spec = importlib.util.spec_from_file_location('frozen_boundary_audit', ROOT / 'distance/boundary-v0.2/harness.py')
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
read, require = c.read, c.require
STATUSES = ('Valid', 'Conditional', 'Invalid')
CRITERIA = ('mechanism_fidelity', 'target_fidelity', 'operational_coherence')


def now(): return datetime.now(timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()
def git(*args): return subprocess.check_output(['git', *args], cwd=ROOT)
def config(): return read(HERE / 'execution-config.json')
def order(): return read(SNAPSHOT / 'execution-order.json')
def candidate(cid): return read(SNAPSHOT / 'cases' / f'{cid}.json')
def packet(run): return preparation.judge_packet(candidate(run['case_id']))


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def copy_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream: stream.write(data)


def projection(value):
    if isinstance(value, dict):
        return {k: projection(v) for k, v in value.items() if k not in ('$schema', '$id', 'allOf')}
    if isinstance(value, list): return [projection(v) for v in value]
    return value


def validate_inputs():
    preparation.verify()
    require(read(HERE / 'wire.schema.json') == projection(read(SNAPSHOT / 'validity.schema.json')),
            'Wire schema differs from the declared projection')
    cfg = config()
    require(cfg['timeout_seconds'] == 900 and cfg['max_concurrent_processes'] == 1,
            'Execution schedule/timeout changed')
    require(set(cfg['families']) == {'A', 'B'}, 'Two families required')


def build_command(family, cwd, directory, session):
    cfg = config(); model = cfg['families'][family]['requested_model']
    schema = HERE / 'wire.schema.json'
    if family == 'A':
        cmd = ['codex', 'exec', '--ignore-user-config', '--ignore-rules', '--ephemeral',
               '--skip-git-repo-check', '--sandbox', 'read-only', '--json', '--color', 'never',
               '--cd', str(cwd), '--model', model, '-c', 'model_reasoning_effort="high"',
               '-c', 'project_doc_max_bytes=0', '-c', 'web_search="disabled"',
               '--output-schema', str(schema), '--output-last-message', str(directory / 'response.json')]
        for feature in cfg['codex_disabled_features']: cmd += ['--disable', feature]
        return cmd + ['-']
    settings = {'disableAllHooks': True, 'autoMemoryEnabled': False,
                'enabledPlugins': {'agents-md@builtin': False, 'telemetry@builtin': False},
                'disableClaudeAiConnectors': True, 'syncClaudeAiSkills': False,
                'syncClaudeAiPlugins': False}
    return ['claude', '--print', '--safe-mode', '--setting-sources', '', '--settings', json.dumps(settings),
            '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}', '--tools', '',
            '--disable-slash-commands', '--no-session-persistence', '--session-id', session,
            '--model', model, '--effort', 'high', '--output-format', 'stream-json', '--verbose',
            '--json-schema', schema.read_text()]


def clean_environment():
    return {k: v for k, v in os.environ.items()
            if not k.startswith(('CODEX_', 'CLAUDE_', 'ANTHROPIC_', 'OPENAI_'))
            and k not in ('CLAUDECODE',)}


def events_at(directory):
    return [json.loads(line, object_pairs_hook=c.unique_object)
            for line in (directory / 'events.jsonl').read_text().splitlines() if line.strip()]


def audit(directory, family, session):
    events = events_at(directory)
    metadata, payload = legacy.audit_events(events, family,
        config()['families'][family]['requested_model'], session if family == 'B' else None)
    response = read(directory / 'response.json')
    if family == 'B':
        require(payload == response, 'Structured payload differs from retained response')
    else:
        finals = [e['item']['text'] for e in events if e.get('type') == 'item.completed'
                  and e.get('item', {}).get('type') == 'agent_message']
        require(len(finals) == 1, 'Expected one completed final response')
        require(json.loads(finals[0], object_pairs_hook=c.unique_object) == response,
                'Final event differs from retained response')
    return metadata


def execute(family, directory, prompt, run=None):
    directory.mkdir(parents=True, exist_ok=False)
    copy_new(directory / 'prompt.txt', prompt.encode())
    session = str(uuid.uuid4()); cfg = config(); cli = cfg['families'][family]['cli']
    with tempfile.TemporaryDirectory(prefix='validity-isolated-') as cwd:
        cmd = build_command(family, cwd, directory, session)
        version = subprocess.check_output([cli, '--version'], text=True).strip()
        require(version == cfg['expected_cli_versions'][family], 'CLI version changed')
        reservation = {'run': run, 'family': family, 'started_at': now(),
                       'packet_sha256': sha(prompt.encode()),
                       'schema_sha256': c.sha(HERE / 'wire.schema.json'),
                       'canonical_schema_sha256': c.sha(SNAPSHOT / 'validity.schema.json'),
                       'configuration': cfg, 'cli_version': version, 'command': cmd,
                       'working_directory': cwd, 'fresh_session_requested': session if family == 'B' else 'ephemeral',
                       'environment_policy': 'Provider/model overrides and parent agent markers removed; existing on-disk subscription authentication',
                       'prepared_commit': git('rev-parse', 'HEAD').decode().strip()}
        write_new(directory / 'reservation.json', reservation)
        status = 'failed'; error = None; metadata = None
        try:
            with (directory / 'events.jsonl').open('x') as stdout, (directory / 'stderr.txt').open('x') as stderr:
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                                           text=True, cwd=cwd, env=clean_environment(), start_new_session=True)
                try: process.communicate(prompt, timeout=cfg['timeout_seconds'])
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL); process.wait(); raise
            # Preserve an available structured response before any validation, even on failure.
            if family == 'B':
                payloads = [e['structured_output'] for e in events_at(directory)
                            if e.get('type') == 'result' and isinstance(e.get('structured_output'), dict)]
                if len(payloads) == 1: write_new(directory / 'response.json', payloads[0])
            require(process.returncode == 0, f'CLI exit {process.returncode}')
            metadata = audit(directory, family, session)
            value = read(directory / 'response.json')
            c.validate(value, 'validity', candidate(run['case_id']) if run else None)
            if run is None: require(value == probe_response(), 'Preflight response differs from specified fixture')
            status = 'valid'
        except Exception as exc:
            error = f'{type(exc).__name__}: {exc}'
        result = {'status': status, 'error': error, 'finished_at': now(), 'metadata': metadata}
        write_new(directory / 'validation.json', result)
        return result


def probe_response():
    return {'case_id': 'PREFLIGHT', 'validity': {
        'mechanism_fidelity': {'status': 'preserved', 'rationale': 'Formatting fixture only.'},
        'target_fidelity': {'status': 'addressed', 'rationale': 'Formatting fixture only.'},
        'operational_coherence': {'status': 'coherent', 'rationale': 'Formatting fixture only.'},
        'target_reframe': {'occurred': False, 'original_question': None, 'reframed_question': None, 'relationship': None},
        'unresolved_conditions': [], 'final_status': 'Valid', 'rationale': 'Formatting fixture only.'},
        'uncertainty': []}


def preflight(attempt):
    validate_inputs(); require(attempt.isalnum(), 'Use an alphanumeric attempt name')
    base = RUNTIME / 'preflight' / attempt
    prompt = ('Return exactly the following JSON object. This is an artificial formatting probe, '
              'not a classification task. Use no tools or external context.\n' + json.dumps(probe_response()))
    summary = {}
    for family in ('A', 'B'):
        result = execute(family, base / family, prompt)
        summary[family] = {**result, 'cli_version': read(base / family / 'reservation.json')['cli_version']}
        print(f'preflight {family}: {result["status"]}', flush=True)
        require(result['status'] == 'valid', result['error'])
    write_new(HERE / 'preflight.json', {'completed_at': now(), 'attempt': attempt, 'families': summary,
        'raw_files': {str(p.relative_to(RUNTIME)): c.sha(p)
                      for p in sorted((RUNTIME / 'preflight').rglob('*')) if p.is_file()}})


def input_paths():
    names = ['EXECUTION.md', 'execution-config.json', 'wire.schema.json', 'runner.py',
             'test_runner.py', 'preflight.json', 'README.md', 'PREFLIGHT-NOTES.md']
    paths = [HERE / name for name in names]
    paths += [ROOT / 'docs/PROBLEM_FRAMES-validity-execution-v0.3.md',
              ROOT / 'distance/boundary-v0.2/harness.py', SNAPSHOT / 'preparation.json']
    paths += [ROOT / name for name in read(SNAPSHOT / 'preparation.json')['files']]
    return sorted(set(paths))


def prepare():
    validate_inputs()
    probes = read(HERE / 'preflight.json')['families']
    require(set(probes) == {'A', 'B'} and all(p['status'] == 'valid' for p in probes.values()),
            'Both preflights must succeed')
    write_new(HERE / 'prepared.json', {'prepared_at': now(),
        'source_preparation_commit': '7b1aad2f12080031d46a5619cdc49ea14380e365',
        'files': {str(p.relative_to(ROOT)): c.sha(p) for p in input_paths()},
        'packets': {run['id']: sha(packet(run).encode()) for run in order()}})


def verify(committed=False):
    validate_inputs(); manifest = read(HERE / 'prepared.json')
    require(set(manifest['files']) == {str(p.relative_to(ROOT)) for p in input_paths()}, 'Input inventory differs')
    for name, digest in manifest['files'].items():
        require(c.sha(ROOT / name) == digest, f'Prepared input changed: {name}')
    require(manifest['packets'] == {run['id']: sha(packet(run).encode()) for run in order()}, 'Packet hash changed')
    if committed:
        for name in [*manifest['files'], str((HERE / 'prepared.json').relative_to(ROOT))]:
            require(git('show', f'HEAD:{name}') == (ROOT / name).read_bytes(), f'Uncommitted input: {name}')
    return manifest


def run_all():
    verify(committed=True)
    for family in ('A', 'B'):
        actual = subprocess.check_output([config()['families'][family]['cli'], '--version'], text=True).strip()
        require(actual == config()['expected_cli_versions'][family], 'CLI changed after preflight')
    write_new(RUNTIME / 'execution-reservation.json', {'started_at': now(), 'commit': git('rev-parse', 'HEAD').decode().strip()})
    for run in order():
        try:
            verify(committed=True)
            result = execute(run['family'], RUNTIME / 'runs' / run['id'], packet(run), run)
            print(f'{run["id"]}: {result["status"]}', flush=True)
            require(result['status'] == 'valid', result['error'])
        except Exception as exc:
            write_new(RUNTIME / 'STOP.json', {'run': run, 'stopped_at': now(), 'error': str(exc),
                'action': 'Scheduling stopped; preserve all attempts. An amendment is required before continuation.'})
            raise


def check_runs(entries):
    require(len(entries) == 48 and {e['id'] for e in entries} == {r['id'] for r in order()}, 'Missing/duplicate results')
    sessions = [entry['audit']['metadata']['session_id'] for entry in entries]
    require(len(set(sessions)) == 48, 'Reused measurement session')
    probes = read(HERE / 'preflight.json')['families']
    require(not set(sessions).intersection(p['metadata']['session_id'] for p in probes.values()), 'Preflight session reused')


def freeze_results():
    verify(committed=True)
    require(not (RUNTIME / 'STOP.json').exists(), 'Cannot freeze a failed run as complete')
    entries = []
    prepared_commit = read(RUNTIME / 'execution-reservation.json')['commit']
    for run in order():
        directory = RUNTIME / 'runs' / run['id']; result = read(directory / 'validation.json')
        require(result['status'] == 'valid', f'Failed run: {run["id"]}')
        reservation = read(directory / 'reservation.json')
        require(reservation['prepared_commit'] == prepared_commit, 'Preparation commit changed during measurement')
        require(reservation['packet_sha256'] == sha(packet(run).encode()), 'Prompt reservation mismatch')
        require((directory / 'prompt.txt').read_text() == packet(run), 'Retained prompt changed')
        require(reservation['schema_sha256'] == c.sha(HERE / 'wire.schema.json'), 'Wire schema changed')
        require(reservation['canonical_schema_sha256'] == c.sha(SNAPSHOT / 'validity.schema.json'), 'Canonical contract changed')
        metadata = audit(directory, run['family'], reservation['fresh_session_requested'])
        require(metadata == result['metadata'], 'Audit metadata changed')
        c.validate(read(directory / 'response.json'), 'validity', candidate(run['case_id']))
        entries.append({**run, 'audit': result, 'reservation': reservation,
                        'files': {p.name: c.sha(p) for p in sorted(directory.iterdir()) if p.is_file()}})
    check_runs(entries)
    write_new(HERE / 'results-freeze.json', {'frozen_at': now(), 'prepared_commit': prepared_commit,
        'prepared_sha256': c.sha(HERE / 'prepared.json'), 'runs': entries})


def freeze_failure():
    verify(); require((RUNTIME / 'STOP.json').exists(), 'No stopped measurement to freeze')
    write_new(HERE / 'failure-freeze.json', {'frozen_at': now(), 'stop': read(RUNTIME / 'STOP.json'),
        'prepared_sha256': c.sha(HERE / 'prepared.json'), 'planned_judgments': 48, 'planned_pairs': 24,
        'files': {str(p.relative_to(RUNTIME)): c.sha(p) for p in sorted(RUNTIME.rglob('*')) if p.is_file()}})


def frozen_results(private=False):
    verify(); frozen = read(HERE / 'results-freeze.json')
    require(frozen['prepared_sha256'] == c.sha(HERE / 'prepared.json'), 'Preparation changed after freeze')
    check_runs(frozen['runs'])
    if private:
        for entry in frozen['runs']:
            for name, digest in entry['files'].items():
                require(c.sha(RUNTIME / 'runs' / entry['id'] / name) == digest, 'Private artifact changed')
    return frozen


def publish():
    frozen = frozen_results(private=True)
    for entry in frozen['runs']:
        copy_new(HERE / 'judgments' / f'{entry["id"]}.json',
                 (RUNTIME / 'runs' / entry['id'] / 'response.json').read_bytes())


def agreement(values):
    pairs = list(values)
    return {'agreements': sum(a == b for a, b in pairs), 'pairs': len(pairs),
            'rate': sum(a == b for a, b in pairs) / len(pairs) if pairs else None}


def metrics(pairs):
    result = {'planned_pairs': 24, 'observed_pairs': len(pairs),
              'final_status': agreement((a['validity']['final_status'], b['validity']['final_status']) for a, b in pairs),
              'criteria': {key: agreement((a['validity'][key]['status'], b['validity'][key]['status']) for a, b in pairs) for key in CRITERIA},
              'reframe_occurred': agreement((a['validity']['target_reframe']['occurred'], b['validity']['target_reframe']['occurred']) for a, b in pairs),
              'class_distributions': {family: dict(Counter(p[i]['validity']['final_status'] for p in pairs)) for i, family in enumerate(('A', 'B'))},
              'confusion_rows_A_columns_B': {a: {b: 0 for b in STATUSES} for a in STATUSES}}
    for a, b in pairs: result['confusion_rows_A_columns_B'][a['validity']['final_status']][b['validity']['final_status']] += 1
    return result


def published():
    frozen = frozen_results(); values = {}
    for entry in frozen['runs']:
        path = HERE / 'judgments' / f'{entry["id"]}.json'
        require(c.sha(path) == entry['files']['response.json'], 'Published response changed')
        values[(entry['case_id'], entry['family'])] = c.validate(read(path), 'validity', candidate(entry['case_id']))
    return values


def analyze():
    values = published()
    pairs = [(values[(f'{n:03}', 'A')], values[(f'{n:03}', 'B')]) for n in range(1, 25)]
    result = metrics(pairs); write_new(HERE / 'metrics.json', result)
    return result


def verify_results(private=False):
    frozen_results(private=private); values = published()
    expected = metrics([(values[(f'{n:03}', 'A')], values[(f'{n:03}', 'B')]) for n in range(1, 25)])
    require(read(HERE / 'metrics.json') == expected, 'Metrics differ from original responses')
    return {'judgments': len(values), 'pairs': 24, 'private_hashes_checked': private}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('validate', 'preflight', 'prepare', 'verify', 'run', 'freeze-results',
                                           'freeze-failure', 'publish', 'analyze', 'verify-results'))
    parser.add_argument('--attempt', default='initial')
    parser.add_argument('--private', action='store_true')
    args = parser.parse_args()
    actions = {'validate': validate_inputs, 'preflight': lambda: preflight(args.attempt), 'prepare': prepare,
               'verify': verify, 'run': run_all, 'freeze-results': freeze_results, 'freeze-failure': freeze_failure,
               'publish': publish, 'analyze': analyze, 'verify-results': lambda: verify_results(args.private)}
    actions[args.command]()
    print(f'{args.command}: OK')


if __name__ == '__main__': main()
