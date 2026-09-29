#!/usr/bin/env python3
"""Additive recovery of Experiment E; no provider call while execution is paused."""
import argparse
from copy import deepcopy
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parent / 'anti-collapse-natural-v0.1'
sys.path.insert(0, str(ORIGINAL))
spec = importlib.util.spec_from_file_location('original_experiment_e', ORIGINAL / 'runner.py')
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)
ORIGINAL_RUNTIME = e.RUNTIME
e.HERE = HERE
e.RUNTIME = e.ROOT / '.runtime/anti-collapse-natural-recovery-v0.1'
STAGES = e.STAGES[1:]
original_validate = e.validate_response
original_build_command = e.build_command
original_execute = e.execute
original_preflight = e.preflight
original_run = e.run_all
original_order = e.order


def imports(stage):
    return e.read(HERE / 'imports.json')['stages'].get(stage, [])


def original_entries(stage):
    path = ORIGINAL / ('audit-partial-freeze.json' if stage == 'audit' else stage + '-freeze.json')
    data = e.read(path)
    entries = data['attempts'] if stage == 'audit' else data['runs']
    return path, [v for v in entries if stage == 'generation' or v['validation']['status'] == 'valid']


def validate_response(value, stage, run=None):
    if stage != 'generation':
        return original_validate(value, stage, run)
    # Keep the frozen checker. Permit only the three exact, previously reviewed
    # payloads, with schema and identity checks still required. This is not a
    # general semantic novelty classifier or permission for future generations.
    try:
        return original_validate(value, stage, run)
    except ValueError as exc:
        if str(exc) != 'Generation self-label violation':
            raise
        exceptions = e.read(HERE / 'lexical-corrections.json')['cases']
        correction = next((v for v in exceptions if v['case_id'] == value['case_id']), None)
        e.require(correction is not None and run is not None, 'Unapproved generation self-label violation')
        source = e.ROOT / correction['payload_path']
        e.require(e.c.sha(source) == correction['raw_sha256'] and value == e.read(source), 'Lexical exception payload changed')
        e.c.validate(value, 'generation', {'case_id': run['case_id']})
        inp = e.source_input(run['case_id'])
        e.require(value['target'] == inp['target'], 'Generated target identity mismatch')
        e.require(value['source'] == {k: inp['source'][k] for k in ('name', 'practice')}, 'Generated source identity mismatch')
        return value


def pending(stage):
    e.require(stage in STAGES, 'Recovery cannot generate replacements')
    reused = {v['id'] for v in imports(stage)}
    return [v for v in original_order(stage) if v['id'] not in reused]


def order(stage):
    return original_order(stage) if stage == 'generation' else pending(stage)


def binaries():
    cfg = e.config()
    for family in 'AB':
        path = Path(cfg['families'][family]['cli'])
        e.require(path.is_absolute() and 'latest' not in path.parts, 'CLI must use a version-specific absolute path')
        e.require(e.c.sha(path) == cfg['executable_sha256'][family], 'Pinned executable changed')
        version = subprocess.check_output([str(path), '--version'], text=True).strip()
        e.require(version == cfg['expected_cli_versions'][family], 'CLI version changed')
    return cfg['expected_cli_versions']


def execution_authorized():
    path = HERE / 'execution-authorization.json'
    e.require(path.exists(), 'PAUSED: explicit user resumption and committed execution authorization required before any provider probe or measurement')
    e.committed(path)
    value = e.read(path)
    e.require(value.get('resume_provider_calls') is True and bool(value.get('user_instruction')), 'Missing explicit resumption')
    e.require(value.get('prepared_sha256') == e.c.sha(HERE / 'prepared.json'), 'Authorization preparation mismatch')
    e.require(datetime.fromisoformat(value['recorded_at']) > datetime.fromisoformat(e.read(HERE / 'prepared.json')['created_at']), 'Authorization predates pause')


def build_command(family, cwd, directory, session, stage):
    command = original_build_command(family, cwd, directory, session, stage)
    command[0] = e.config()['families'][family]['cli']
    return command


def check_fresh_session(session, directory):
    e.require(bool(session), 'Missing session')
    for root in (ORIGINAL_RUNTIME, e.RUNTIME):
        for path in root.rglob('validation.json'):
            if path.parent != directory:
                metadata = e.read(path).get('metadata')
                e.require(not metadata or metadata['session_id'] != session, 'Session reused across original/recovery calls')


def execute(family, directory, prompt, stage, run=None):
    e.require(stage in STAGES, 'Recovery cannot generate replacements')
    execution_authorized()
    binaries()
    return original_execute(family, directory, prompt, stage, run)


def preflight(stage):
    execution_authorized()
    binaries()
    return original_preflight(stage)


def run_all(stage):
    execution_authorized()
    binaries()
    return original_run(stage)


def verify(check_committed=False, private=False):
    e.validate_inputs()
    e.preservation(private)
    prepared = e.read(HERE / 'prepared.json')
    e.verify_inventory(prepared['files'])
    if check_committed:
        for name in [*prepared['files'], str((HERE / 'prepared.json').relative_to(e.ROOT))]:
            e.committed(e.ROOT / name)
    for stage in ('generation', 'neutralization', 'audit'):
        source_file, entries = original_entries(stage)
        source_by_id = {v['id']: v for v in entries}
        reused = imports(stage)
        e.require(len(reused) == len(entries), 'Imported coverage drift')
        for entry in reused:
            provenance = entry['recovery_import']
            original = source_by_id[entry['id']]
            e.require(provenance['entry_file'] == str(source_file.relative_to(e.ROOT)), 'Import source drift')
            e.require(provenance['original_validation'] == original['validation'], 'Original validation changed')
            comparison = deepcopy(entry)
            del comparison['recovery_import']
            comparison['validation'] = provenance['original_validation']
            e.require(comparison == original, 'Imported execution metadata changed')
            payload = e.ROOT / provenance['payload_path']
            copied = e.public_path(stage, entry)
            e.require(copied.read_bytes() == payload.read_bytes() and e.c.sha(copied) == original['response_sha256'], 'Imported response changed')
            validate_response(e.read(copied), stage, entry)
            if private:
                e.verify_inventory(entry['files'])
    return prepared


def freeze(stage):
    """Freeze pending calls plus unchanged imports, recording separate segments."""
    e.prerequisites(stage)
    entries = {v['id']: v for v in imports(stage)}
    stage_commit = e.read(e.RUNTIME / (stage + '-reservation.json'))['commit']
    for run in pending(stage):
        directory = e.RUNTIME / stage / run['id']
        validation = e.read(directory / 'validation.json')
        reservation = e.read(directory / 'reservation.json')
        e.require(validation['status'] in ('valid', 'excluded'), 'Fatal measurement cannot complete stage')
        e.require(reservation['input_commit'] == stage_commit, 'Commit changed during recovery stage')
        e.require((directory / 'prompt.txt').read_text() == e.packet(stage, run['case_id']), 'Executed packet drift')
        response = directory / 'response.json'
        if validation['status'] == 'valid':
            validate_response(e.read(response), stage, run)
            e.copy_new(e.public_path(stage, run), response.read_bytes())
        else:
            e.require(stage == 'neutralization' and validation['failure_category'] == 'content', 'Invalid recovery content attrition')
            e.copy_new(HERE / 'failures' / stage / (run['id'] + '.txt'), response.read_bytes())
        entries[run['id']] = {**run, 'validation': validation, 'reservation': reservation, 'response_sha256': e.c.sha(response), 'files': e.inventory(directory.iterdir())}
    scheduled = original_order(stage)
    e.require(set(entries) == {v['id'] for v in scheduled}, 'Combined stage coverage mismatch')
    e.write_new(HERE / (stage + '-freeze.json'), {'at': e.now(), 'stage': stage, 'prepared_sha256': e.c.sha(HERE / 'prepared.json'), 'stage_inputs_sha256': e.c.sha(HERE / 'stage-inputs' / (stage + '.json')), 'recovery_execution_commit': stage_commit, 'imported_run_ids': [v['id'] for v in imports(stage)], 'runs': [entries[v['id']] for v in scheduled]})


def prepare():
    e.require(not (HERE / 'prepared.json').exists(), 'Recovery already prepared')
    e.require(not e.RUNTIME.exists(), 'Recovery runtime already exists')
    # Read-only verification of the interrupted run, including its failed attempt.
    subprocess.run([sys.executable, '-B', str(ORIGINAL / 'review/verify_incomplete.py'), '--private'], cwd=e.ROOT, check=True)
    tracked = [e.ROOT / name for name in e.git('ls-files').decode().splitlines()]
    e.write_new(HERE / 'preservation.json', {'base_commit': e.git('rev-parse', 'HEAD').decode().strip(), 'files': e.inventory(tracked), 'private_files': e.inventory((e.ROOT / '.runtime').rglob('*'))})
    static = [*e.DOCS.values(), 'operator-manifest.json']
    for name in static:
        e.copy_new(HERE / name, (ORIGINAL / name).read_bytes())
    for directory in ('schemas', 'baselines', 'generation-inputs', 'execution-orders'):
        for path in sorted((ORIGINAL / directory).glob('*')):
            e.copy_new(HERE / directory / path.name, path.read_bytes())
    cfg = e.read(ORIGINAL / 'execution-config.json')
    cfg['executable_sha256'] = {}
    tools = {'A': ('npm:@openai/codex', 'codex'), 'B': ('npm:@anthropic-ai/claude-code', 'claude')}
    for family, (tool, command) in tools.items():
        install = Path(subprocess.check_output(['mise', 'where', tool], cwd=e.ROOT, text=True).strip()).resolve()
        binary = install / 'node_modules' / '.bin' / command
        cfg['families'][family]['cli'] = str(binary)
        cfg['executable_sha256'][family] = e.c.sha(binary)
    e.write_new(HERE / 'execution-config.json', cfg)
    binaries()
    corrections = e.read(ORIGINAL / 'review/content-exclusion-review.json')['cases']
    for correction in corrections:
        _, entries = original_entries('generation')
        entry = next(v for v in entries if v['case_id'] == correction['case_id'])
        correction['payload_path'] = str((ORIGINAL / 'failures/generation' / (entry['id'] + '.txt')).relative_to(e.ROOT))
        correction['readmitted'] = True
    e.write_new(HERE / 'lexical-corrections.json', {'policy': 'Exact hash-bound exceptions for the three documented lexical false positives; no payload changes or new generations.', 'cases': corrections})
    imported = {}
    for stage in ('generation', 'neutralization', 'audit'):
        source_file, entries = original_entries(stage)
        imported[stage] = []
        for old in entries:
            entry = deepcopy(old)
            payload = ORIGINAL / e.OUT[stage] / (entry['case_id'] + '.json' if stage in ('generation', 'neutralization') else entry['id'] + '.json')
            if entry['validation']['status'] == 'excluded':
                payload = ORIGINAL / 'failures' / stage / (entry['id'] + '.txt')
            e.require(e.c.sha(payload) == entry['response_sha256'], 'Original response hash mismatch')
            validate_response(e.read(payload), stage, entry)
            entry['recovery_import'] = {'entry_file': str(source_file.relative_to(e.ROOT)), 'payload_path': str(payload.relative_to(e.ROOT)), 'original_validation': deepcopy(entry['validation']), 'lexical_correction': entry['validation']['status'] == 'excluded'}
            if entry['validation']['status'] == 'excluded':
                entry['validation'] = {**entry['validation'], 'status': 'valid', 'failure_category': None, 'error': None}
            e.copy_new(e.public_path(stage, entry), payload.read_bytes())
            imported[stage].append(entry)
    e.write_new(HERE / 'imports.json', {'at': e.now(), 'stages': imported, 'original_stop_retained': True, 'new_generation_calls': 0})
    e.write_new(HERE / 'generation-freeze.json', {'at': e.now(), 'stage': 'generation', 'kind': 'authorized revalidation of unchanged frozen outputs', 'runs': imported['generation']})
    e.validate_inputs()
    e.write_new(HERE / 'prepared.json', {'created_at': e.now(), 'base_commit': e.git('rev-parse', 'HEAD').decode().strip(), 'state': 'paused before all provider calls', 'files': e.inventory([*HERE.rglob('*'), e.ROOT / 'mise.toml'])})
    verify(private=True)
    print(json.dumps({'prepared': True, 'generations': 30, 'imported_neutralizations': 27, 'imported_audits': 21, 'pending_neutralizations': len(pending('neutralization')), 'provider_calls': 0, 'paused': True}))


def execution_audit(private=False):
    """Audit original and recovery execution segments without inventing one commit."""
    verify(True, private)
    sessions = []
    for stage in ('generation', 'neutralization', 'audit'):
        sessions += [v['validation']['metadata']['session_id'] for v in imports(stage)]
        probe = e.read(ORIGINAL / 'probes' / (stage + '.json'))
        sessions += [v['validation']['metadata']['session_id'] for v in probe['entries']]
    stages = {}
    for stage in STAGES:
        path = HERE / (stage + '-freeze.json')
        if not path.exists():
            continue
        data = e.read(path)
        e.verify_stage_inputs(stage)
        e.require(data['prepared_sha256'] == e.c.sha(HERE / 'prepared.json'), 'Prepared binding drift')
        e.require(data['stage_inputs_sha256'] == e.c.sha(HERE / 'stage-inputs' / (stage + '.json')), 'Stage binding drift')
        e.require([{k: v[k] for k in ('id', 'case_id', 'family')} for v in data['runs']] == original_order(stage), 'Combined coverage drift')
        reused = {v['id']: v for v in imports(stage)}
        probe_path = HERE / 'probes' / (stage + '.json')
        probe = e.read(probe_path)
        e.require(data['recovery_execution_commit'] == e.checkpoint(probe_path), 'Recovery execution must follow probe checkpoint')
        last = datetime.fromisoformat(probe['at'])
        for v in probe['entries']:
            e.require(v['validation']['status'] == 'valid', 'Probe failure')
            sessions.append(v['validation']['metadata']['session_id'])
            if private:
                e.verify_inventory(v['files'])
        for entry in data['runs']:
            if entry['id'] in reused:
                e.require(entry == reused[entry['id']], 'Imported segment drift')
                continue
            reservation, validation = entry['reservation'], entry['validation']
            start = datetime.fromisoformat(reservation['started_at'])
            end = datetime.fromisoformat(validation['finished_at'])
            e.require(last <= start <= end, 'Recovery chronology drift')
            last = end
            e.require(reservation['configuration'] == e.config() and reservation['input_commit'] == data['recovery_execution_commit'], 'Recovery configuration/commit drift')
            e.require(reservation['cli_version'] == e.config()['expected_cli_versions'][entry['family']], 'CLI drift')
            e.require(reservation['command'][0] == e.config()['families'][entry['family']]['cli'], 'Mutable executable used')
            e.require(reservation['packet_sha256'] == e.sha(e.packet(stage, entry['case_id']).encode()), 'Packet drift')
            e.require(reservation['canonical_schema_sha256'] == e.c.sha(e.canonical(stage)) and reservation['wire_schema_sha256'] == e.c.sha(HERE / 'schemas' / (stage + '-wire.schema.json')), 'Schema drift')
            path = e.public_path(stage, entry) if validation['status'] == 'valid' else HERE / 'failures' / stage / (entry['id'] + '.txt')
            e.require(e.c.sha(path) == entry['response_sha256'], 'Response drift')
            if validation['status'] == 'valid':
                validate_response(e.read(path), stage, entry)
            else:
                e.require(stage == 'neutralization' and validation['status'] == 'excluded' and validation['failure_category'] == 'content', 'Unexpected exclusion')
            sessions.append(validation['metadata']['session_id'])
            if private:
                e.verify_inventory(entry['files'])
        e.require(last <= datetime.fromisoformat(data['at']), 'Freeze before completion')
        stages[stage] = {'imported': len(reused), 'recovery_calls': len(data['runs']) - len(reused), 'recovery_execution_commit': data['recovery_execution_commit'], 'freeze_commit': e.checkpoint(HERE / (stage + '-freeze.json'))}
    e.require(len(sessions) == len(set(sessions)), 'Session reused')
    return {'stages': stages, 'unique_sessions_including_probes': len(sessions), 'new_generation_calls': 0, 'original_prelaunch_failures_retained': 1}


e.validate_response = validate_response
e.order = order
e.build_command = build_command
e.check_fresh_session = check_fresh_session
e.execute = execute
e.preflight = preflight
e.run_all = run_all
e.verify = verify
e.execution_audit = execution_audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('prepare', 'verify', 'binaries', 'prepare-stage', 'preflight', 'run', 'freeze', 'admit', 'analyze', 'verify-results', 'freeze-failure'))
    parser.add_argument('--stage', choices=STAGES, default='neutralization')
    parser.add_argument('--private', action='store_true')
    args = parser.parse_args()
    if args.command == 'prepare': prepare()
    elif args.command == 'verify': verify(private=args.private); print('Recovery inputs and original artifacts verified')
    elif args.command == 'binaries': print(json.dumps(binaries()))
    elif args.command == 'prepare-stage': e.prepare_stage(args.stage)
    elif args.command == 'preflight': preflight(args.stage)
    elif args.command == 'run': run_all(args.stage)
    elif args.command == 'freeze': freeze(args.stage)
    elif args.command == 'admit': e.admit()
    elif args.command == 'analyze': e.analyze()
    elif args.command == 'verify-results': print(e.verify_results(args.private))
    else: e.freeze_failure()


if __name__ == '__main__':
    main()
