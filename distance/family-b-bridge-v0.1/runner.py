#!/usr/bin/env python3
"""Frozen bridge collection; no semantic comparison before committed complete results."""
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
import jsonschema

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RUNTIME = ROOT / '.runtime/family-b-bridge-v0.1'
CATEGORIES = ('stable', 'instrumentation_drift', 'substantive_close', 'substantive_divergence')
IDS = {'validity': ['E003', 'E010', 'E014', 'E006', 'E022', 'E030'],
       'anti-collapse': ['N010', 'N006', 'N001', 'N002', 'N004', 'N009']}


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


legacy = module('bridge_event_audit', ROOT / 'distance/boundary-v0.2/harness.py')
contracts = module('bridge_contracts', ROOT / 'distance/anti-collapse-v0.1/contracts.py')
projection = module('bridge_projection', ROOT / 'distance/anti-collapse-v0.1/build_schemas.py').projection
muse = module('bridge_muse', HERE / 'provider/muse.py')
fable = module('bridge_fable', HERE / 'provider/fable.py')
read, require = contracts.read, contracts.require


def now(): return datetime.now(timezone.utc).isoformat()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git', *args], cwd=ROOT)
def head(): return git('rev-parse', 'HEAD').decode().strip()
def config(): return read(HERE / 'execution-config.json')
def cases(): return read(HERE / 'manifest.json')['cases']
def case(cid): return next(v for v in cases() if v['bridge_id'] == cid)
def order(): return read(HERE / 'execution-order.json')['runs']
def canonical(stage): return HERE / 'schemas' / (stage + '.schema.json')
def wire(stage): return HERE / 'schemas' / (stage + '-wire.schema.json')
def packet(cid, provider):
    require(provider in ('fable', 'muse'), 'No third provider')
    return (ROOT / case(cid)['packet_path']).read_bytes()
def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f: f.write(data)
def write(path, value): put(path, (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode())
def inventory(paths): return {str(p.relative_to(ROOT)): sha(p) for p in sorted(paths) if p.is_file() and '__pycache__' not in p.parts}
def verify_inventory(files):
    for name, digest in files.items(): require(sha(ROOT / name) == digest, 'Frozen bytes changed: ' + name)
def committed(path): require(git('show', 'HEAD:' + str(path.relative_to(ROOT))) == path.read_bytes(), 'Uncommitted artifact: ' + str(path))
def checkpoint(path):
    committed(path)
    return git('log', '-1', '--format=%H', '--', str(path.relative_to(ROOT))).decode().strip()


def verify_inputs():
    rows = cases()
    require(len(rows) == 12 and len({r['bridge_id'] for r in rows}) == 12, 'Exactly 12 conceptual cases')
    for stage, ids in IDS.items():
        require([r['bridge_id'] for r in rows if r['stage'] == stage] == ids, 'Prescribed source IDs changed')
        require(read(wire(stage)) == projection(read(canonical(stage))), 'Projection changed fields or constraints')
    for r in rows:
        for pathkey, hashkey in [('input_path', 'input_sha256'), ('classifier_path', 'classifier_sha256'),
                                 ('canonical_schema_path', 'canonical_schema_sha256'), ('source_freeze_path', 'source_freeze_sha256')]:
            p = ROOT / r[pathkey]
            require(sha(p) == r[hashkey], 'Historical hash mismatch')
            require(git('show', r['source_commit'] + ':' + r[pathkey]) == p.read_bytes(), 'Historical commit mismatch')
        h = r['historical_fable']; p = ROOT / h['judgment_path']
        require(sha(p) == h['judgment_sha256'], 'Historical Fable changed')
        require(git('show', r['source_commit'] + ':' + h['judgment_path']) == p.read_bytes(), 'Historical judgment commit mismatch')
        frozen = read(ROOT / r['source_freeze_path'])
        e = next(v for v in frozen['runs'] if v['case_id'] == r['bridge_id'] and v['family'] == 'B')
        require(e['reservation']['packet_sha256'] == r['input_sha256'], 'Not measured historical packet')
        require(e['reservation']['canonical_schema_sha256'] == r['canonical_schema_sha256'], 'Not measured schema')
        historical_hash = e.get('response_sha256') or next(v for k, v in e['files'].items() if k.endswith('/response.json'))
        require(historical_hash == h['judgment_sha256'], 'Not frozen historical response')
        raw = packet(r['bridge_id'], 'fable')
        require(raw == packet(r['bridge_id'], 'muse') == (ROOT / r['input_path']).read_bytes(), 'Packet rewritten')
        require(raw.startswith((ROOT / r['classifier_path']).read_bytes() + b'\n\nCASE PACKET\n'), 'Classifier differs')
        require(sha(canonical(r['stage'])) == r['canonical_schema_sha256'], 'Canonical schema changed')
        require((HERE / 'classifiers' / (r['stage'] + '.md')).read_bytes() == (ROOT / r['classifier_path']).read_bytes(), 'Classifier copy changed')
        for banned in ('Claude', 'Fable', 'Muse', 'historical_fable', 'historical result', 'expected result', 'bridge rationale', 'operator review'):
            require(banned.casefold() not in raw.decode().casefold(), 'Operator/provider identity leakage')
    verify_inventory(read(HERE / 'preservation.json')['files'])
    return {'cases': 12, 'historical_artifacts_unchanged': True}


def verify(prepared=True):
    result = verify_inputs()
    if prepared:
        p = read(HERE / 'prepared.json')
        verify_inventory(p['files'])
        for name in [*p['files'], str((HERE / 'prepared.json').relative_to(ROOT))]: committed(ROOT / name)
    return result


def fixture(stage):
    if stage == 'validity':
        return {'case_id': 'PREFLIGHT', 'validity': {
            'mechanism_fidelity': {'status': 'preserved', 'rationale': 'Formatting fixture only.'},
            'target_fidelity': {'status': 'addressed', 'rationale': 'Formatting fixture only.'},
            'operational_coherence': {'status': 'coherent', 'rationale': 'Formatting fixture only.'},
            'target_reframe': {'occurred': False, 'original_question': None, 'reframed_question': None, 'relationship': None},
            'unresolved_conditions': [], 'final_status': 'Valid', 'rationale': 'Formatting fixture only.'}, 'uncertainty': []}
    return {'case_id': 'PREFLIGHT', 'anti_collapse': {'status': 'BORDERLINE_KEEP',
        'departures': {k: {'status': 'uncertain', 'rationale': 'Formatting fixture only.'} for k in contracts.LOCI},
        'materiality': {'status': 'uncertain', 'rationale': 'Formatting fixture only.'},
        'native_reduction': {'collapses_without_loss': 'uncertain', 'closest_native_equivalent': 'Formatting fixture only.', 'lost_if_reduced': [], 'rationale': 'Formatting fixture only.'},
        'formalization': {'merely_makes_native_reasoning_explicit': 'uncertain', 'new_epistemic_constraint': None, 'rationale': 'Formatting fixture only.'},
        'decisive_reason': 'Formatting fixture only.', 'uncertainty': ['Artificial fixture.']}}


def validate(value, stage, cid=None):
    jsonschema.Draft202012Validator(read(canonical(stage))).validate(value)
    candidate = None
    if cid:
        require(value['case_id'] == cid, 'Case identity mismatch')
        candidate = json.loads(packet(cid, 'fable').decode().split('\n\nCASE PACKET\n', 1)[1]) if stage == 'validity' else {'case_id': cid}
    contracts.validate(value, stage, candidate)
    return value


def stop(where, reason):
    if not (RUNTIME / 'STOP.json').exists(): write(RUNTIME / 'STOP.json', {'at': now(), 'where': where, 'reason': reason, 'recovery_requires_explicit_authorization': True})


def guard():
    require(not (RUNTIME / 'STOP.json').exists(), 'Scheduling stopped; explicit recorded recovery authorization required')
    verify()


def load_muse_credential():
    # bws returns only a path; consume within the local launcher, never print/store its value.
    if os.environ.get('META_API_KEY'): return
    result = subprocess.run(['bws-4-agents', 'get', 'META_API_KEY'], text=True, capture_output=True)
    require(result.returncode == 0, 'Credential helper failed; secret output suppressed')
    path = Path(result.stdout.strip())
    require(path.is_absolute() and path.is_file(), 'Credential helper did not return file')
    try: os.environ['META_API_KEY'] = path.read_text().strip()
    finally: path.unlink()
    require(bool(os.environ['META_API_KEY']), 'Empty credential')


def catalog():
    guard()
    d = RUNTIME / 'catalog'; d.mkdir(parents=True, exist_ok=False)
    write(d / 'reservation.json', {'at': now(), 'commit': head(), 'endpoint': muse.BASE + '/models', 'credential_source': 'environment', 'inference_calls': 0})
    try:
        load_muse_credential()
        result = muse.request('models', None, 60, lambda name, data: put(d / name, data))
        ids = [v['id'] for v in result['data']]
        require(muse.MODEL in ids, 'Requested Contributor model unavailable')
        write(d / 'validation.json', {'status': 'valid', 'requested_model': muse.MODEL, 'available': True, 'at': now()})
    except Exception as exc:
        write(d / 'validation.json', {'status': 'failed', 'error': safe_error(exc), 'at': now()})
        stop('catalog', safe_error(exc)); raise
    write(HERE / 'provider/catalog.json', {'at': now(), 'requested_model': muse.MODEL, 'entry': next(v for v in result['data'] if v['id'] == muse.MODEL), 'files': inventory(d.iterdir()), 'input_commit': head()})
    return {'catalog': 'valid', 'model': muse.MODEL}


def safe_error(exc):
    value = type(exc).__name__ + ': ' + str(exc)
    key = os.environ.get('META_API_KEY')
    return value.replace(key, '[REDACTED]') if key else value


def execute(provider, stage, d, raw, cid=None):
    guard()
    require(provider in ('fable', 'muse'), 'No third judge')
    d.mkdir(parents=True, exist_ok=False)
    session = str(uuid.uuid4()); metadata = None
    put(d / 'prompt.txt', raw)
    cfg = config(); arm = cfg['providers'][provider]
    reservation = {'at': now(), 'input_commit': head(), 'provider': provider, 'stage': stage,
        'case_id': cid, 'session_id': session, 'packet_sha256': sha_bytes(raw),
        'canonical_schema_sha256': sha(canonical(stage)), 'wire_schema_sha256': sha(wire(stage)),
        'configuration': arm, 'harness_retries': 0, 'credential_source': 'environment' if provider == 'muse' else 'existing subscription authentication',
        'python_version': sys.version, 'fresh_process': True, 'history_messages': 0}
    try:
        with tempfile.TemporaryDirectory(prefix='family-b-isolated-') as cwd:
            reservation.update(working_directory=cwd, working_directory_initially_empty=not list(Path(cwd).iterdir()))
            require(reservation['working_directory_initially_empty'], 'Nonempty model context')
            if provider == 'fable':
                require(sha(Path(arm['cli'])) == arm['executable_sha256'], 'Fable executable changed')
                version = subprocess.check_output([arm['cli'], '--version'], text=True).strip()
                require(version == arm['cli_version'], 'Fable CLI version changed')
                cmd = fable.command(arm, wire(stage).read_text(), session)
                reservation.update(command=cmd, cli_version=version)
                write(d / 'reservation.json', reservation)
                with (d / 'events.jsonl').open('x') as stdout, (d / 'stderr.txt').open('x') as stderr:
                    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, cwd=cwd,
                        env=fable.environment(), start_new_session=True)
                    try: p.communicate(raw, timeout=cfg['timeout_seconds'])
                    except subprocess.TimeoutExpired:
                        os.killpg(p.pid, signal.SIGKILL); p.wait(); raise
                events = [json.loads(line, object_pairs_hook=contracts.unique_object) for line in (d / 'events.jsonl').read_text().splitlines() if line.strip()]
                # Preserve a structured payload even when later transport/schema checks fail.
                values = [e['structured_output'] for e in events if isinstance(e.get('structured_output'), dict)]
                if len(values) == 1: write(d / 'response.json', values[0])
                require(p.returncode == 0, 'Fable process failed: ' + str(p.returncode))
                metadata, value = legacy.audit_events(events, 'B', arm['requested_model'], session)
                require(metadata['returned_model_identifiers'], 'Missing Fable returned model')
                require(read(d / 'response.json') == value, 'Structured event mismatch')
            else:
                body = muse.request_body(raw.decode(), read(wire(stage)), arm)
                write(d / 'request.json', body); write(d / 'reservation.json', reservation)
                load_muse_credential()
                result = muse.request('chat/completions', body, cfg['timeout_seconds'], lambda name, data: put(d / name, data))
                text, metadata = muse.parse_response(result, session)
                put(d / 'response.json', text.encode())
                value = read(d / 'response.json')
            validate(value, stage, cid)
            if cid is None: require(value == fixture(stage), 'Artificial fixture mismatch')
            existing = [read(p)['session_id'] for p in RUNTIME.rglob('reservation.json') if p != d / 'reservation.json' and 'session_id' in read(p)]
            require(session not in existing, 'Repeated session')
            result = {'status': 'valid', 'at': now(), 'metadata': metadata, 'error': None}
    except Exception as exc:
        if not (d / 'reservation.json').exists(): write(d / 'reservation.json', reservation)
        result = {'status': 'failed', 'at': now(), 'metadata': metadata, 'error': safe_error(exc)}
        stop(str(d.relative_to(RUNTIME)), result['error'])
    write(d / 'validation.json', result)
    return result


def child(provider, stage, cid=None):
    cmd = [sys.executable, '-B', str(HERE / 'runner.py'), '_one', '--provider', provider, '--stage', stage]
    if cid: cmd += ['--case', cid]
    process = subprocess.run(cmd, cwd=ROOT)
    require(process.returncode == 0, 'Isolated child stopped; inspect preserved failure')


def preflight():
    guard(); require((HERE / 'provider/catalog.json').exists(), 'Catalog verification required')
    write(RUNTIME / 'preflight-reservation.json', {'at': now(), 'commit': head()})
    # New API first, preserving subscription budget if its contracts fail.
    for provider in ('muse', 'fable'):
        for stage in IDS: child(provider, stage)
    write(HERE / 'preflight/freeze.json', {'at': now(), 'input_commit': head(), 'files': inventory((RUNTIME / 'preflight').rglob('*')),
        'entries': [{'provider': p, 'stage': s, 'validation': read(RUNTIME / 'preflight' / (p + '-' + s) / 'validation.json'),
                     'reservation': read(RUNTIME / 'preflight' / (p + '-' + s) / 'reservation.json')} for p in ('muse', 'fable') for s in IDS]})


def prerequisites():
    guard(); committed(HERE / 'preflight/freeze.json'); committed(HERE / 'provider/catalog.json')
    p = read(HERE / 'preflight/freeze.json'); verify_inventory(p['files'])
    require(len(p['entries']) == 4 and all(e['validation']['status'] == 'valid' for e in p['entries']), 'Four successful contract probes required')


def run_all():
    prerequisites()
    write(RUNTIME / 'measurement-reservation.json', {'at': now(), 'commit': head()})
    for run in order():
        prerequisites()
        child(run['provider'], run['stage'], run['case_id'])


def freeze(partial=False):
    verify()
    if not partial: prerequisites()
    else: require((RUNTIME / 'STOP.json').exists(), 'Partial freeze requires failure')
    entries = []
    for run in order():
        d = RUNTIME / 'judgments' / run['id']
        if not d.exists():
            require(partial, 'Missing primary response'); continue
        result = read(d / 'validation.json')
        if not partial: require(result['status'] == 'valid', 'Failed primary response')
        if (d / 'response.json').exists():
            put(HERE / 'judgments' / run['provider'] / (run['case_id'] + '.json'), (d / 'response.json').read_bytes())
        entries.append({**run, 'validation': result, 'reservation': read(d / 'reservation.json'), 'files': inventory(d.iterdir())})
    if not partial: require(len(entries) == 24, 'Exactly 24 primary judgments required')
    write(HERE / ('partial-freeze.json' if partial else 'results-freeze.json'), {
        'at': now(), 'complete': not partial, 'prepared_sha256': sha(HERE / 'prepared.json'),
        'runs': entries, 'all_runtime_files': inventory(RUNTIME.rglob('*')),
        'stop': read(RUNTIME / 'STOP.json') if partial else None})
    return {'frozen': len(entries), 'complete': not partial}


def complete_results():
    verify(); path = HERE / 'results-freeze.json'; committed(path)
    freeze = read(path); require(freeze['complete'] and len(freeze['runs']) == 24, 'Incomplete bridge cannot be compared')
    require(freeze['prepared_sha256'] == sha(HERE / 'prepared.json'), 'Preparation mismatch')
    verify_inventory(freeze['all_runtime_files'])
    sessions = []; data = {}
    require([r['id'] for r in freeze['runs']] == [r['id'] for r in order()], 'Schedule/coverage mismatch')
    for run in freeze['runs']:
        require(run['validation']['status'] == 'valid', 'Failed frozen result')
        r = run['reservation']; sessions.append(r['session_id'])
        require(r['packet_sha256'] == sha_bytes(packet(run['case_id'], run['provider'])), 'Executed packet drift')
        path = HERE / 'judgments' / run['provider'] / (run['case_id'] + '.json')
        raw = RUNTIME / 'judgments' / run['id'] / 'response.json'
        require(path.read_bytes() == raw.read_bytes(), 'Published response changed')
        committed(path)
        data[(run['case_id'], run['provider'])] = validate(read(path), run['stage'], run['case_id'])
    require(len(set(sessions)) == 24, 'Session reuse')
    return data


def status(value, stage): return value['validity']['final_status'] if stage == 'validity' else value['anti_collapse']['status']
def policy(value, stage):
    return (value['validity']['final_status'] == 'Valid' and not value['validity']['unresolved_conditions']) if stage == 'validity' else value['anti_collapse']['status'] != 'CLEAR_COLLAPSE'
def agreement(pairs):
    n = len(pairs); k = sum(a == b for a, b in pairs)
    return {'numerator': k, 'denominator': n, 'fraction': k / n if n else None}


def metrics():
    data = complete_results(); result = {'results_freeze_commit': checkpoint(HERE / 'results-freeze.json')}
    for stage, ids in IDS.items():
        historical = {cid: read(ROOT / case(cid)['historical_fable']['judgment_path']) for cid in ids}
        pairs = [(data[(cid, 'fable')], data[(cid, 'muse')]) for cid in ids]
        policy_agreement = agreement([(policy(a, stage), policy(b, stage)) for a, b in pairs])
        result[stage] = {'fresh_distributions': {p: dict(Counter(status(data[(cid, p)], stage) for cid in ids)) for p in ('fable', 'muse')},
            'exact_status_agreement': agreement([(status(a, stage), status(b, stage)) for a, b in pairs]),
            'policy_equivalent_agreement': policy_agreement,
            'historical_vs_fresh_fable_exact_status_agreement': agreement([(status(historical[cid], stage), status(data[(cid, 'fable')], stage)) for cid in ids])}
        if stage == 'anti-collapse': result[stage]['keep_reject_agreement'] = policy_agreement
    write(HERE / 'metrics.json', result)
    return result


def check_reviews(rows):
    require(len(rows) == 12 and {r['bridge_id'] for r in rows} == {r['bridge_id'] for r in cases()}, 'Review coverage')
    for r in rows:
        for pair in ('historical_vs_fresh_fable', 'fresh_fable_vs_muse'):
            require(r[pair]['category'] in CATEGORIES and bool(r[pair]['rationale']), 'Invalid review category/rationale')
        require(r['downstream_transition_effect'] in ('none', 'minor', 'material'), 'Invalid downstream effect')


def audit():
    data = complete_results(); reviews = read(HERE / 'review/case-reviews.json')
    require(reviews['results_freeze_commit'] == checkpoint(HERE / 'results-freeze.json'), 'Review not bound to complete freeze')
    require(datetime.fromisoformat(reviews['at']) > datetime.fromisoformat(read(HERE / 'results-freeze.json')['at']), 'Review predates freeze')
    check_reviews(reviews['cases'])
    for r in reviews['cases']:
        cid = r['bridge_id']; stage = case(cid)['stage']
        for label, value in [('historical_fable', read(ROOT / case(cid)['historical_fable']['judgment_path'])), ('fresh_fable', data[(cid, 'fable')]), ('fresh_muse', data[(cid, 'muse')])]:
            require(r[label]['status'] == status(value, stage), 'Review status mismatch')
    counts = {pair: {category: sum(r[pair]['category'] == category for r in reviews['cases']) for category in CATEGORIES} for pair in ('fresh_fable_vs_muse', 'historical_vs_fresh_fable')}
    value = {'at': now(), 'results_freeze_commit': checkpoint(HERE / 'results-freeze.json'), 'primary_calls': {'fable': 12, 'muse': 12},
             'preflight_calls': {'fable': 2, 'muse': 2}, 'unique_primary_sessions': 24, 'third_judges': 0, 'experiment_f_calls': 0,
             'harness_retries': 0, 'historical_artifacts_unchanged': True, 'review_counts': counts}
    write(HERE / 'review/execution-audit.json', value)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('verify', 'catalog', 'preflight', 'run', '_one', 'freeze', 'freeze-failure', 'metrics', 'audit'))
    parser.add_argument('--provider', choices=('fable', 'muse')); parser.add_argument('--stage', choices=tuple(IDS)); parser.add_argument('--case')
    args = parser.parse_args()
    if args.action == '_one':
        require(args.provider and args.stage, 'Provider/stage required')
        if args.case:
            prerequisites()
            run = next(r for r in order() if r['case_id'] == args.case and r['provider'] == args.provider)
            require(run['stage'] == args.stage, 'Wrong contract')
            reservation = read(RUNTIME / 'measurement-reservation.json')
            require(reservation['commit'] == head(), 'Commit changed during measurement')
            index = order().index(run)
            require(all((RUNTIME / 'judgments' / r['id'] / 'validation.json').exists() and read(RUNTIME / 'judgments' / r['id'] / 'validation.json')['status'] == 'valid' for r in order()[:index]), 'Out-of-order measurement')
            d = RUNTIME / 'judgments' / run['id']; raw = packet(args.case, args.provider)
        else:
            require((RUNTIME / 'preflight-reservation.json').exists(), 'Preflight not reserved')
            d = RUNTIME / 'preflight' / (args.provider + '-' + args.stage)
            raw = ('Return exactly this artificial formatting fixture; no classification, tools or external context.\n' + json.dumps(fixture(args.stage))).encode()
        result = execute(args.provider, args.stage, d, raw, args.case)
        print(args.provider, args.stage, args.case or 'artificial', result['status'], flush=True)
        if result['status'] != 'valid': sys.exit(1)
        return
    actions = {'verify': verify, 'catalog': catalog, 'preflight': preflight, 'run': run_all,
               'freeze': freeze, 'freeze-failure': lambda: freeze(True), 'metrics': metrics, 'audit': audit}
    try: result = actions[args.action]()
    except Exception as exc:
        # Provider failures are already preserved by the adapter; never schedule recovery.
        print(safe_error(exc), file=sys.stderr); sys.exit(1)
    if result is not None: print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
