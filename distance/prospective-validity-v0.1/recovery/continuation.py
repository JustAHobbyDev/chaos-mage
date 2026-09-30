"""Additive Experiment F scheduler. Scientific inputs and original attempts stay frozen."""
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
import argparse
import fcntl
import importlib.util
import json
import os
import signal
import subprocess
import tempfile
import evidence as e

c, old = e.c, e.old
HERE, F, ROOT = e.HERE, e.F, e.ROOT
RUNTIME = ROOT / '.runtime/prospective-validity-v0.1-recovery'
STATES = {'RUNNING', 'PAUSED_RECOVERABLE', 'PAUSED_AMBIGUOUS', 'TERMINATED_LINEAGE', 'TERMINATED_MEASUREMENT', 'COMPLETE'}
TERMINAL = {'TERMINATED_LINEAGE', 'TERMINATED_MEASUREMENT', 'COMPLETE'}
spec = importlib.util.spec_from_file_location('f_recovery_contracts', F / 'contracts.py')
contracts = importlib.util.module_from_spec(spec); spec.loader.exec_module(contracts)


class MeasurementFailure(Exception): pass
class LineageFailure(Exception): pass


@contextmanager
def lock(name):
    RUNTIME.mkdir(parents=True, exist_ok=True)
    with (RUNTIME / (name + '.lock')).open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def state_events():
    paths = sorted((RUNTIME / 'state').glob('*.json'))
    previous = None
    rows = []
    for index, path in enumerate(paths):
        row = c.read(path)
        c.require(row['index'] == index and row['previous_sha256'] == previous and row['state'] in STATES, 'State chain invalid')
        if rows: c.require(rows[-1]['state'] not in TERMINAL, 'Transition out of terminal state')
        rows.append(row); previous = c.sha(path)
    return rows


def state():
    rows = state_events()
    return rows[-1]['state'] if rows else 'PAUSED_AMBIGUOUS'


def transition(value, reason, evidence=None):
    c.require(value in STATES, 'Unknown state')
    with lock('state'):
        rows = state_events()
        c.require(not rows or rows[-1]['state'] not in TERMINAL, 'Terminal state cannot clear')
        index = len(rows)
        previous = c.sha(RUNTIME / 'state' / f'{index-1:04}.json') if rows else None
        if value == 'RUNNING':
            c.require(evidence is not None, 'Committed recovery evidence required')
            old.committed(evidence)
            c.require(c.read(evidence)['classification'] == 'recoverable_integrity_violation', 'Only recoverable incidents can resume')
        old.write(RUNTIME / 'state' / f'{index:04}.json', {'index': index, 'at': old.now(), 'state': value,
                  'reason': reason, 'previous_sha256': previous, 'commit': old.head(),
                  'evidence': {'path': old.rel(evidence), 'sha256': c.sha(evidence)} if evidence else None})


def running(): c.require(state() == 'RUNNING', 'Scheduling blocked: ' + state())
def root_for(stage): return F if stage == 'taxonomy' else HERE
def order(stage): return c.read(root_for(stage) / 'execution-orders' / f'{stage}.json')['order']
def packet(stage, identity): return (root_for(stage) / 'packets' / stage / f'{identity}.txt').read_text()
def schema(stage, wire=False): return root_for(stage) / 'schemas' / (stage + ('-wire' if wire else '') + '.schema.json')


def validate(value, stage, identity):
    previous = contracts.HERE
    try:
        contracts.HERE = root_for(stage)
        return contracts.validate(value, stage, identity)
    finally: contracts.HERE = previous


def command(cwd, directory, stage):
    cmd = old.command(cwd, directory, stage)
    cmd[cmd.index('--output-schema') + 1] = str(schema(stage, True))
    return cmd


def retained(): return c.read(F / 'taxonomy-partial-freeze.json')['runs']


def run_directories(stage, kind='runs'):
    parent = RUNTIME / kind / stage
    return sorted([p for p in parent.iterdir() if p.is_dir()],
                  key=lambda p: c.read(p / 'attempt.json')['at']) if parent.exists() else []


def validation_path(directory):
    supplement = directory / 'validation-recovery.json'
    return supplement if supplement.exists() else directory / 'validation.json'


def reservation_path(directory):
    supplement = directory / 'reservation-launch.json'
    return supplement if supplement.exists() else directory / 'reservation.json'


def unlaunched(directory):
    return (not (directory / 'launch-intent.json').exists() or (directory / 'not-launched.json').exists()) and not any(
        (directory / name).exists() for name in ('process.json', 'exit.json', 'response.json', 'launch-resume-intent.json')) and all(
        not (directory / name).exists() or not (directory / name).read_bytes() for name in ('events.jsonl', 'stderr.txt'))


def next_identity(stage):
    frozen = order(stage)
    imported = [x['identity'] for x in retained()] if stage == 'taxonomy' else []
    directories = run_directories(stage)
    observed = imported + [p.name for p in directories]
    c.require(len(set(observed)) == len(observed), 'Duplicate reservation across segments')
    c.require(observed == frozen[:len(observed)], 'Schedule prefix changed')
    for directory in directories:
        v = validation_path(directory)
        if not (v.exists() and c.read(v)['status'] == 'valid'):
            token = directory / 'resume-unlaunched.json'
            c.require(directory == directories[-1] and unlaunched(directory) and token.exists(), 'Unresolved reservation blocks scheduling')
            authorization = ROOT / c.read(token)['record']
            old.committed(authorization)
            c.require(c.sha(authorization) == c.read(token)['sha256'], 'Unlaunched authorization changed')
            return directory.name
    return frozen[len(observed)] if len(observed) < len(frozen) else None


def prepared_files(stage):
    result = dict(c.read(HERE / 'continuation-prepared.json')['files'])
    if stage == 'prospective': result.update(c.read(HERE / 'prospective-prepared.json')['files'])
    return result


def verify_inputs(stage, committed=False):
    c.require(stage in ('taxonomy', 'prospective'), 'Unauthorized stage')
    e.preservation(c.read(HERE / 'original-preservation.json')['files'])
    files = prepared_files(stage)
    old.verify_hashes(files)
    old.binary_check()
    if committed:
        old.committed(HERE / 'continuation-prepared.json')
        if stage == 'prospective': old.committed(HERE / 'prospective-prepared.json')
        for name in files: old.committed(ROOT / name)
    c.require(c.read(schema(stage, True)) == c.wire(c.read(schema(stage))), 'Wire projection differs')
    if stage == 'taxonomy':
        c.require(order(stage) == old.order('taxonomy') and len(order(stage)) == 196, 'Taxonomy order changed')
    else:
        c.require(set(order(stage)) == {f'E{i:03}' for i in range(1,31)} and len(order(stage)) == 30, 'Prospective schedule coverage')
        for identity in order(stage):
            expected = (HERE / 'CLASSIFIER.md').read_text() + '\nCASE PACKET\n' + json.dumps(
                {'case_id': identity, **c.read(F / 'imports/candidates' / f'{identity}.json')}, indent=2, ensure_ascii=False) + '\n'
            c.require(packet(stage, identity) == expected, 'Prospective packet not allowlisted')
    return {'stage': stage, 'files': len(files), 'preserved': True}


def audit_response(directory, stage, identity, kind):
    x = c.read(reservation_path(directory))
    c.require(x['configuration'] == old.config(), 'Configuration drift')
    c.require(x['command'] == command(x['working_directory'], directory, stage), 'Command drift')
    c.require(x['working_directory_initially_empty'] and x['requested_session'] == 'ephemeral', 'Isolation drift')
    c.require(x['packet_sha256'] == c.sha(directory / 'prompt.txt'), 'Executed prompt drift')
    c.require(x['canonical_schema_sha256'] == c.sha(schema(stage)) and x['wire_schema_sha256'] == c.sha(schema(stage, True)), 'Schema drift')
    expected = packet(stage, identity) if kind == 'runs' else artificial_prompt(stage)
    c.require((directory / 'prompt.txt').read_text() == expected, 'Executed packet mismatch')
    c.require(c.read(directory / 'exit.json')['returncode'] == 0, 'Provider process failed')
    events = [json.loads(s, object_pairs_hook=c.unique) for s in (directory / 'events.jsonl').read_text().splitlines() if s.strip()]
    metadata = old.audit_events(events)
    finals = [x['item']['text'] for x in events if x.get('type') == 'item.completed' and x.get('item', {}).get('type') == 'agent_message']
    c.require(len(finals) == 1 and finals[0].strip() == (directory / 'response.json').read_text().strip(), 'Stream/response mismatch')
    validate(c.read(directory / 'response.json'), stage, identity)
    if kind == 'probes': c.require(c.read(directory / 'response.json') == old.probe_fixture(stage), 'Artificial fixture mismatch')
    return metadata


def verify_attempts():
    sessions = {x['validation']['metadata']['session_id'] for x in [c.read(F / 'probes/taxonomy.json')['entry'], *retained()]}
    counts = {}
    last = max(datetime.fromisoformat(x['validation']['finished_at']) for x in retained())
    all_dirs = []
    for stage in ('taxonomy', 'prospective'):
        for kind in ('probes', 'runs'):
            directories = run_directories(stage, kind)
            c.require(kind != 'probes' or len(directories) <= (0 if stage == 'taxonomy' else 1), 'Unauthorized extra probe')
            all_dirs += [(p, stage, kind) for p in directories]
        if stage == 'taxonomy' or (HERE / 'prospective-prepared.json').exists(): next_identity(stage)
    for directory, stage, kind in sorted(all_dirs, key=lambda row: c.read(row[0] / 'attempt.json')['at']):
        if unlaunched(directory) and (directory / 'resume-unlaunched.json').exists(): continue
        a = c.read(directory / 'attempt.json'); v = c.read(validation_path(directory))
        c.require(a['harness_attempt'] == 1, 'Repeated attempt')
        m = audit_response(directory, stage, directory.name, kind)
        capture_path = directory / 'response-capture.json'
        if not capture_path.exists(): capture_path = directory / 'response-capture-recovery.json'
        capture = c.read(capture_path)
        old.verify_hashes(capture['files'])
        c.require(v['status'] == 'valid' and v['metadata'] == m, 'Validation differs from raw evidence')
        c.require(m['session_id'] not in sessions, 'Session reuse'); sessions.add(m['session_id'])
        start = datetime.fromisoformat(c.read(reservation_path(directory))['started_at'])
        end = datetime.fromisoformat(v['finished_at'])
        c.require(start <= end and (last is None or last <= start), 'Execution overlap'); last = end
        counts[stage + '/' + kind] = counts.get(stage + '/' + kind, 0) + 1
    return {'counts': counts, 'unique_sessions': len(sessions)}


def history_before_stage(stage):
    verify_inputs(stage, True)
    next_identity(stage)
    verify_attempts()
    result = e.history()
    directory = RUNTIME / 'prechecks'
    path = directory / f'{len(list(directory.glob("*.json"))):04}-{stage}.json'
    old.write(path, result)
    verify_inputs(stage, True)
    return path


def resume(record_path):
    c.require(state() not in TERMINAL, 'Terminal state cannot clear')
    old.committed(record_path)
    record = c.read(record_path)
    e.gate(record)
    c.require(not state_events(), 'Initial recovery cannot clear later incidents')
    verify_inputs('taxonomy', True)
    transition('RUNNING', 'Original preservation incident recovered under user handoff', record_path)


def recover(record_path):
    """Later incident clearance: no scientific replay, only retained evidence recheck."""
    c.require(state() in ('PAUSED_RECOVERABLE', 'PAUSED_AMBIGUOUS'), 'Not a recoverable pause')
    old.committed(record_path); record = c.read(record_path)
    c.require(record['classification'] == 'recoverable_integrity_violation', 'Nonrecoverable classification')
    latest = sorted((RUNTIME / 'state').glob('*.json'))[-1]
    c.require(record['incident_sha256'] == c.sha(latest), 'Recovery incident mismatch')
    c.require(record['authorization'] == old.rel(HERE / 'AUTHORIZATION.md') and record['remediation'], 'Missing authority/remediation')
    old.verify_hashes(record['files'])
    c.require(record['files'] == old.inventory((RUNTIME / 'runs').rglob('*')) | old.inventory((RUNTIME / 'probes').rglob('*')),
              'Recovery must bind all attempted measurements')
    verify_inputs(record['stage'], True)
    # This command never converts invalid raw output into a valid measurement.
    # It can supplement failed local bookkeeping only after raw output validates.
    for stage in ('taxonomy', 'prospective'):
        for kind in ('runs', 'probes'):
            for directory in run_directories(stage, kind):
                v = validation_path(directory)
                if v.exists() and c.read(v)['status'] == 'valid': continue
                if unlaunched(directory):
                    old.write(directory / 'resume-unlaunched.json', {'record': old.rel(record_path), 'sha256': c.sha(record_path)})
                else:
                    metadata = audit_response(directory, stage, directory.name, kind)
                    if not (directory / 'response-capture.json').exists():
                        old.write(directory / 'response-capture-recovery.json', {'at': old.now(),
                            'recovery_record': old.rel(record_path), 'files': old.inventory(directory / name for name in
                            ('prompt.txt', 'events.jsonl', 'stderr.txt', 'response.json', 'exit.json', 'process.json'))})
                    old.write(directory / 'validation-recovery.json', {'status': 'valid', 'error': None,
                        'finished_at': c.read(directory / 'exit.json')['at'], 'metadata': metadata,
                        'recovery_record': old.rel(record_path), 'original_validation_preserved': True})
    verify_attempts()
    e.history()
    transition('RUNNING', 'Committed later non-contamination recovery', record_path)


def artificial_prompt(stage):
    return 'Return exactly this artificial schema fixture. No classification, tools or external context.\n' + json.dumps(old.probe_fixture(stage))


def execute(stage, identity, kind='runs'):
    running(); verify_inputs(stage)
    if kind == 'runs': c.require(identity == next_identity(stage), 'Only next frozen ID can execute')
    else: c.require(stage == 'prospective' and identity == 'ARTIFICIAL', 'Taxonomy probe already measured')
    old.binary_check()
    directory = RUNTIME / kind / stage / identity
    reuse = directory.exists()
    if reuse:
        c.require(unlaunched(directory) and (directory / 'resume-unlaunched.json').exists(), 'Duplicate reservation')
    else:
        directory.mkdir(parents=True, exist_ok=False)
        old.write(directory / 'attempt.json', {'at': old.now(), 'stage': stage, 'identity': identity, 'kind': kind,
                  'input_commit': old.head(), 'harness_attempt': 1})
    prompt = packet(stage, identity) if kind == 'runs' else artificial_prompt(stage)
    if (directory / 'prompt.txt').exists(): c.require((directory / 'prompt.txt').read_bytes() == prompt.encode(), 'Reserved prompt differs')
    else: old.copy(directory / 'prompt.txt', prompt.encode())
    launched = False
    try:
        with tempfile.TemporaryDirectory(prefix='f-recovery-isolated-') as cwd:
            c.require(not list(Path(cwd).iterdir()), 'Nonempty working directory')
            cmd = command(cwd, directory, stage)
            old.write(directory / ('reservation-launch.json' if reuse else 'reservation.json'), {'started_at': old.now(), 'input_commit': old.head(), 'stage': stage,
                'identity': identity, 'kind': kind, 'packet_sha256': c.digest(prompt.encode()),
                'canonical_schema_sha256': c.sha(schema(stage)), 'wire_schema_sha256': c.sha(schema(stage, True)),
                'configuration': old.config(), 'cli_version': old.binary_check(), 'command': cmd, 'working_directory': cwd,
                'working_directory_initially_empty': True, 'requested_session': 'ephemeral',
                'environment_policy': 'Original frozen clean_environment; no credentials copied or logged.'})
            with (directory / 'events.jsonl').open('a' if reuse else 'x') as output, (directory / 'stderr.txt').open('a' if reuse else 'x') as error:
                with lock('state'):
                    running(); verify_inputs(stage)
                    old.write(directory / ('launch-resume-intent.json' if reuse else 'launch-intent.json'), {'at': old.now(), 'commit': old.head()})
                    try:
                        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=output, stderr=error,
                            text=True, cwd=cwd, env=old.clean_environment(), start_new_session=True)
                    except OSError as exc:
                        old.write(directory / 'not-launched.json', {'at': old.now(), 'errno': exc.errno, 'proof': 'Popen raised before returning a child'})
                        raise
                    launched = True
                old.write(directory / 'process.json', {'pid': process.pid, 'parent_pid': os.getpid(), 'launched_at': old.now()})
                try: process.communicate(prompt, timeout=900)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL); process.wait()
                    raise MeasurementFailure('Provider timeout after launch; no retry')
            old.write(directory / 'exit.json', {'at': old.now(), 'returncode': process.returncode})
        old.write(directory / 'response-capture.json', {'at': old.now(), 'files': old.inventory(
            directory / name for name in ('prompt.txt', 'events.jsonl', 'stderr.txt', 'response.json', 'exit.json', 'process.json'))})
        try: metadata = audit_response(directory, stage, identity, kind)
        except (ValueError, c.jsonschema.ValidationError, json.JSONDecodeError, FileNotFoundError) as exc:
            raise MeasurementFailure(str(exc)) from exc
        sessions = [c.read(p)['metadata']['session_id'] for parent in (old.RUNTIME, RUNTIME)
                    for p in parent.rglob('validation*.json') if c.read(p).get('metadata')]
        if metadata['session_id'] in sessions: raise LineageFailure('Reused provider session')
        old.write(directory / ('validation-recovery.json' if reuse else 'validation.json'), {'status': 'valid', 'error': None, 'finished_at': old.now(), 'metadata': metadata})
        return directory
    except Exception as exc:
        if not (directory / 'validation.json').exists():
            old.write(directory / 'validation.json', {'status': 'failed', 'error': type(exc).__name__ + ': ' + str(exc),
                      'finished_at': old.now(), 'metadata': None, 'process_launched': launched})
        if isinstance(exc, LineageFailure): target = 'TERMINATED_LINEAGE'
        elif isinstance(exc, MeasurementFailure): target = 'TERMINATED_MEASUREMENT'
        elif not launched and not (directory / 'launch-intent.json').exists(): target = 'PAUSED_RECOVERABLE'
        elif (directory / 'not-launched.json').exists(): target = 'PAUSED_RECOVERABLE'
        else: target = 'PAUSED_AMBIGUOUS'
        if state() == 'RUNNING': transition(target, type(exc).__name__ + ': ' + str(exc))
        raise


def entry(directory, stage, kind='runs'):
    return {'identity': directory.name, 'kind': kind, 'reservation': c.read(reservation_path(directory)),
            'validation': c.read(validation_path(directory)), 'files': old.inventory(directory.iterdir()),
            'response_sha256': c.sha(directory / 'response.json'), 'response_path': old.rel(directory / 'response.json')}


def run(stage, probe=False):
    with lock('scheduler'):
        running()
        try:
            precheck = history_before_stage(stage)
            running(); initial = old.head()
            if probe:
                c.require(stage == 'prospective', 'Original taxonomy probe retained')
                directory = execute(stage, 'ARTIFICIAL', 'probes')
                old.write(HERE / 'probes/prospective.json', {'at': old.now(), 'input_commit': initial,
                          'prepared_sha256': c.sha(HERE / 'prospective-prepared.json'), 'precheck': old.rel(precheck),
                          'entry': entry(directory, stage, 'probes')})
                return
            probe_path = F / 'probes/taxonomy.json' if stage == 'taxonomy' else HERE / 'probes/prospective.json'
            old.committed(probe_path)
            old.verify_hashes(c.read(probe_path)['entry']['files'])
            segments = RUNTIME / 'segments'
            old.write(segments / f'{len(list(segments.glob("*.json"))):04}-{stage}.json',
                      {'at': old.now(), 'stage': stage, 'commit': initial, 'precheck': old.rel(precheck), 'next_id': next_identity(stage)})
            while (identity := next_identity(stage)) is not None:
                running(); c.require(old.head() == initial, 'Commit changed during measurement segment')
                directory = execute(stage, identity)
                print(f'{stage} {order(stage).index(identity)+1}/{len(order(stage))} {identity}: valid', flush=True)
        except Exception as exc:
            if state() == 'RUNNING': transition('PAUSED_AMBIGUOUS', type(exc).__name__ + ': ' + str(exc))
            raise


def freeze(stage):
    running(); verify_inputs(stage, True); verify_attempts()
    c.require(next_identity(stage) is None, 'Cannot freeze incomplete stage')
    entries = []
    imported = {x['identity']: x for x in retained()} if stage == 'taxonomy' else {}
    for identity in order(stage):
        if identity in imported:
            row = {**imported[identity], 'response_path': old.rel(F / 'taxonomy-judgments' / f'{identity}.json'),
                   'response_sha256': c.sha(F / 'taxonomy-judgments' / f'{identity}.json'), 'retained_original': True}
        else:
            directory = RUNTIME / 'runs' / stage / identity
            destination = HERE / ('taxonomy-judgments' if stage == 'taxonomy' else 'judgments') / f'{identity}.json'
            if destination.exists(): c.require(destination.read_bytes() == (directory / 'response.json').read_bytes(), 'Published response differs')
            else: old.copy(destination, (directory / 'response.json').read_bytes())
            row = {**entry(directory, stage), 'response_path': old.rel(destination), 'retained_original': False}
        entries.append(row)
    old.write(HERE / f'{stage}-freeze.json', {'at': old.now(), 'stage': stage, 'original_incomplete_commit': e.ORIGINAL,
              'order': order(stage), 'runs': entries, 'retained_count': len(imported),
              'prepared_sha256': c.sha(HERE / ('continuation-prepared.json' if stage == 'taxonomy' else 'prospective-prepared.json')),
              'runtime_files': old.inventory(RUNTIME.rglob('*'))})


def main():
    p = argparse.ArgumentParser(); p.add_argument('action', choices=['resume', 'recover', 'run', 'preflight', 'freeze', 'verify', 'pause'])
    p.add_argument('--stage', choices=['taxonomy', 'prospective'], default='taxonomy')
    p.add_argument('--record', type=Path, default=HERE / 'recovery-record.json'); p.add_argument('--reason', default='Operator requested investigation')
    args = p.parse_args()
    if args.action == 'resume': resume(args.record)
    elif args.action == 'recover': recover(args.record)
    elif args.action == 'pause': transition('PAUSED_AMBIGUOUS', args.reason)
    elif args.action in ('run', 'preflight'): run(args.stage, args.action == 'preflight')
    elif args.action == 'freeze': freeze(args.stage)
    else: print(json.dumps({'inputs': verify_inputs(args.stage), 'attempts': verify_attempts(), 'state': state()}, indent=2))


if __name__ == '__main__': main()
