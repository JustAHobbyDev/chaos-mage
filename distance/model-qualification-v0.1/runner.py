#!/usr/bin/env python3
"""One-shot, Muse-only qualification; historical comparison requires committed results."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid
import jsonschema

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RUNTIME = ROOT / '.runtime/model-qualification-v0.1'
IDS = {'validity': ['E003', 'E010', 'E014', 'E006', 'E022', 'E030'],
       'anti-collapse': ['N010', 'N006', 'N001', 'N002', 'N004', 'N009']}
CATEGORIES = ('none', 'ontology_specification_ambiguity', 'legitimate_reasoning_variation', 'model_failure')
OUTCOMES = ('qualified', 'not_qualified', 'qualification_inconclusive')
DIMENSIONS = ('protocol_compliance', 'instrument_structure', 'mechanism_reasoning',
              'warrant_reasoning', 'native_baseline_use', 'uncertainty_handling', 'rationale_coherence')


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


contracts = module('qualification_contracts', ROOT / 'distance/anti-collapse-v0.1/contracts.py')
projection = module('qualification_projection', ROOT / 'distance/anti-collapse-v0.1/build_schemas.py').projection
muse = module('qualification_muse', HERE / 'provider/muse/adapter.py')
read, require = contracts.read, contracts.require


def now(): return datetime.now(timezone.utc).isoformat()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(*args): return subprocess.check_output(['git', *args], cwd=ROOT, stderr=subprocess.PIPE)
def head(): return git('rev-parse', 'HEAD').decode().strip()
def config(): return read(HERE / 'execution-config.json')
def cases(): return read(HERE / 'manifest.json')['cases']
def case(cid): return next(c for c in cases() if c['qualification_id'] == cid)
def order(): return read(HERE / 'execution-order.json')['runs']
def canonical(stage): return HERE / 'schemas' / (stage + '.schema.json')
def wire(stage): return HERE / 'schemas' / (stage + '-wire.schema.json')
def fixture(stage): return read(HERE / 'preflight' / ('fixture-' + stage + '.json'))
def packet(cid, provider='muse'):
    require(provider == 'muse', 'Only Muse receives fresh measurements')
    return (ROOT / case(cid)['packet_path']).read_bytes()
def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f: f.write(data)
def write(path, value): put(path, (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode())
def inventory(paths): return {str(p.relative_to(ROOT)): sha(p) for p in sorted(paths) if p.is_file() and '__pycache__' not in p.parts}
def verify_inventory(files):
    for p, digest in files.items(): require(sha(ROOT / p) == digest, 'Frozen bytes changed: ' + p)
def committed(path): require(git('show', 'HEAD:' + str(path.relative_to(ROOT))) == path.read_bytes(), 'Uncommitted artifact: ' + str(path))
def checkpoint(path):
    committed(path)
    return git('log', '-1', '--format=%H', '--', str(path.relative_to(ROOT))).decode().strip()


def verify_inputs():
    rows = cases()
    require(len(rows) == len({c['qualification_id'] for c in rows}) == 12, 'Exactly twelve cases')
    for stage, ids in IDS.items():
        require([c['qualification_id'] for c in rows if c['stage'] == stage] == ids, 'Prescribed case IDs changed')
        require(read(wire(stage)) == projection(read(canonical(stage))), 'Historical structural projection changed')
    for c in rows:
        for k in ('input', 'classifier', 'canonical_schema', 'source_freeze'):
            p = ROOT / c[k + '_path']
            require(sha(p) == c[k + '_sha256'], 'Historical hash mismatch')
            require(git('show', c['source_commit'] + ':' + c[k + '_path']) == p.read_bytes(), 'Historical source commit mismatch')
        require(c['historical_context']['available'] and c['historical_context']['hidden_from_measurement'], 'Historical masking missing')
        frozen = read(ROOT / c['source_freeze_path'])
        for family, name in [('A', 'astra'), ('B', 'fable')]:
            h = c['historical_context']['artifacts'][name]
            require(sha(ROOT / h['path']) == h['sha256'], 'Historical response hash mismatch')
            require(hashlib.sha256(git('show', c['source_commit'] + ':' + h['path'])).hexdigest() == h['sha256'], 'Historical response source mismatch')
            e = next(v for v in frozen['runs'] if v['case_id'] == c['source_case_id'] and v['family'] == family)
            require(e['reservation']['packet_sha256'] == c['input_sha256'], 'Packet not measured historically')
            require(e['reservation']['canonical_schema_sha256'] == c['canonical_schema_sha256'], 'Historical schema mismatch')
            digest = e.get('response_sha256') or next(v for k, v in e['files'].items() if k.endswith('/response.json'))
            require(digest == h['sha256'], 'Historical response not frozen')
        raw = packet(c['qualification_id'])
        require(raw == (ROOT / c['input_path']).read_bytes(), 'Packet rewritten')
        require(raw.startswith((ROOT / c['classifier_path']).read_bytes() + b'\n\nCASE PACKET\n'), 'Classifier mismatch')
        require(sha(canonical(c['stage'])) == c['canonical_schema_sha256'], 'Canonical copy mismatch')
        require((HERE / 'classifiers' / (c['stage'] + '.md')).read_bytes() == (ROOT / c['classifier_path']).read_bytes(), 'Classifier copy mismatch')
        for banned in ('historical_context', 'historical_fable', 'operator metadata', 'coverage intent', 'stable valid anchor', 'historical disagreement', 'Claude', 'Fable', 'Astra', 'Muse'):
            require(banned.casefold() not in raw.decode().casefold(), 'Operator label leakage')
    runs = order()
    require(len(runs) == 12 and {r['case_id'] for r in runs} == {c['qualification_id'] for c in rows}, 'Schedule coverage')
    require(all(r['provider'] == 'muse' and r['stage'] == case(r['case_id'])['stage'] for r in runs), 'Invalid scheduled provider/stage')
    require(all(a['stage'] != b['stage'] for a, b in zip(runs, runs[1:])), 'Strata not interleaved')
    cfg = config()
    require(set(cfg['providers']) == {'muse'} and cfg['primary_budget'] == {'muse': 12} and cfg['preflight_budget'] == {'muse': 2}, 'Provider budget')
    require(cfg['data_use']['tier'] == cfg['providers']['muse']['tier'] == 'Contributor', 'Contributor provenance')
    muse.request_body('probe', {}, cfg['providers']['muse'])
    verify_inventory(read(HERE / 'preservation.json')['files'])
    return {'cases': 12, 'historical_artifacts_unchanged': True}


def verify(prepared=True):
    result = verify_inputs()
    if prepared:
        p = read(HERE / 'prepared.json'); verify_inventory(p['files'])
        for name in [*p['files'], str((HERE / 'prepared.json').relative_to(ROOT))]: committed(ROOT / name)
    return result


def validate(value, stage, cid=None):
    jsonschema.Draft202012Validator(read(canonical(stage))).validate(value)
    candidate = None
    if cid:
        require(value['case_id'] == cid, 'Case identity mismatch')
        candidate = json.loads(packet(cid).decode().split('\n\nCASE PACKET\n', 1)[1]) if stage == 'validity' else {'case_id': cid}
    contracts.validate(value, stage, candidate)
    return value


def stop(where, reason):
    if not (RUNTIME / 'STOP.json').exists():
        write(RUNTIME / 'STOP.json', {'at': now(), 'where': where, 'reason': reason, 'recovery_requires_explicit_authorization': True})


def guard():
    require(not (RUNTIME / 'STOP.json').exists(), 'Scheduling stopped; explicit recovery authorization required')
    verify()


def safe_error(exc):
    value = type(exc).__name__ + ': ' + str(exc)
    key = os.environ.get('META_API_KEY')
    return value.replace(key, '[REDACTED]') if key else value


def failure_kind(exc):
    if isinstance(exc, jsonschema.ValidationError): return 'schema_failure'
    if isinstance(exc, json.JSONDecodeError): return 'malformed_output'
    if isinstance(exc, TimeoutError): return 'timeout'
    if 'model' in str(exc).lower(): return 'model_identity_failure'
    if 'credential' in str(exc).lower(): return 'credential_unavailable'
    return 'provider_or_protocol_failure'


def catalog():
    guard(); d = HERE / 'preflight/catalog'; d.mkdir(parents=True, exist_ok=False)
    write(d / 'reservation.json', {'at': now(), 'input_commit': head(), 'endpoint': muse.BASE + '/models', 'credential_source': 'environment', 'inference_calls': 0})
    try:
        require(bool(os.environ.get('META_API_KEY')), 'Muse environment credential unavailable')
        result = muse.request('models', None, 60, lambda n, b: put(d / n, b))
        entry = next((v for v in result['data'] if v['id'] == muse.MODEL), None)
        require(entry is not None, 'Exact Contributor model unavailable')
        value = {'status': 'valid', 'at': now(), 'requested_model': muse.MODEL, 'entry': entry}
    except Exception as exc:
        value = {'status': 'failed', 'at': now(), 'failure_kind': failure_kind(exc), 'error': safe_error(exc)}
        stop('catalog', value['error'])
    write(d / 'validation.json', value)
    require(value['status'] == 'valid', 'Catalog failed; no recovery')
    return value


def execute(stage, directory, raw, cid=None):
    guard(); directory.mkdir(parents=True, exist_ok=False)
    session = str(uuid.uuid4()); cfg = config(); arm = cfg['providers']['muse']
    metadata = None; received = False
    reservation = {'at': now(), 'input_commit': head(), 'provider': 'muse', 'stage': stage, 'case_id': cid,
        'session_id': session, 'process_id': os.getpid(), 'packet_sha256': hashlib.sha256(raw).hexdigest(),
        'canonical_schema_sha256': sha(canonical(stage)), 'wire_schema_sha256': sha(wire(stage)),
        'configuration': arm, 'python_version': sys.version, 'api_version': 'v1',
        'fresh_process': True, 'history_messages': 0, 'tools': [], 'credential_source': 'environment', 'harness_retries': 0}
    try:
        with tempfile.TemporaryDirectory(prefix='muse-qualification-') as cwd:
            reservation.update(working_directory=cwd, working_directory_initially_empty=not list(Path(cwd).iterdir()))
            require(reservation['working_directory_initially_empty'], 'Nonempty request context')
            body = muse.request_body(raw.decode(), read(wire(stage)), arm)
            put(directory / 'prompt.txt', raw); write(directory / 'request.json', body); write(directory / 'reservation.json', reservation)
            require(bool(os.environ.get('META_API_KEY')), 'Muse environment credential unavailable')
            previous = Path.cwd()
            try:
                os.chdir(cwd)
                result = muse.request('chat/completions', body, cfg['timeout_seconds'], lambda n, b: put(directory / n, b))
            finally: os.chdir(previous)
            received = True
            text, metadata = muse.parse_response(result, session)
            put(directory / 'response.json', text.encode())
            value = read(directory / 'response.json'); validate(value, stage, cid)
            if cid is None: require(value == fixture(stage), 'Artificial fixture mismatch')
            validation = {'status': 'valid', 'at': now(), 'metadata': metadata, 'error': None}
    except Exception as exc:
        if not (directory / 'reservation.json').exists(): write(directory / 'reservation.json', reservation)
        validation = {'status': 'failed', 'at': now(), 'metadata': metadata, 'error': safe_error(exc),
                      'failure_kind': failure_kind(exc), 'response_received': received}
        stop(str(directory.relative_to(ROOT)), validation['error'])
    write(directory / 'validation.json', validation)
    return validation


def child(stage, cid=None):
    cmd = [sys.executable, '-B', str(HERE / 'runner.py'), '_one', '--stage', stage]
    if cid: cmd += ['--case', cid]
    # Only the Muse credential and ordinary runtime/transport environment are inherited.
    env = {k: v for k, v in os.environ.items() if k in ('PATH', 'LANG', 'LC_ALL', 'TMPDIR', 'SSL_CERT_FILE', 'SSL_CERT_DIR', 'HTTPS_PROXY', 'HTTP_PROXY', 'NO_PROXY', 'META_API_KEY')}
    p = subprocess.run(cmd, cwd=ROOT, env=env)
    require(p.returncode == 0, 'Isolated child stopped; inspect preserved failure')


def preflight():
    guard(); require(read(HERE / 'preflight/catalog/validation.json')['status'] == 'valid', 'Catalog required')
    write(RUNTIME / 'preflight-reservation.json', {'at': now(), 'commit': head()})
    for stage in IDS: child(stage)
    entries = [{'stage': s, 'validation': read(HERE / 'preflight' / s / 'validation.json'),
                'reservation': read(HERE / 'preflight' / s / 'reservation.json')} for s in IDS]
    write(HERE / 'preflight/freeze.json', {'at': now(), 'input_commit': head(), 'entries': entries,
          'files': inventory((HERE / 'preflight').rglob('*'))})


def prerequisites():
    guard(); committed(HERE / 'preflight/freeze.json')
    frozen = read(HERE / 'preflight/freeze.json'); verify_inventory(frozen['files'])
    for p in frozen['files']: committed(ROOT / p)
    require(len(frozen['entries']) == 2 and all(e['validation']['status'] == 'valid' for e in frozen['entries']), 'Two successful probes required')
    require(len({e['reservation']['session_id'] for e in frozen['entries']}) == 2, 'Preflight session reuse')


def run_all():
    prerequisites(); write(RUNTIME / 'measurement-reservation.json', {'at': now(), 'commit': head()})
    for run in order(): child(run['stage'], run['case_id'])


def freeze(partial=False):
    verify()
    if partial: require((RUNTIME / 'STOP.json').exists(), 'Failure required for partial freeze')
    else: prerequisites()
    entries = []
    for run in order():
        d = HERE / 'judgments' / run['case_id']
        if not d.exists():
            require(partial, 'Missing primary result'); continue
        result = read(d / 'validation.json')
        if not partial: require(result['status'] == 'valid', 'Unsuccessful primary result')
        entries.append({**run, 'validation': result, 'reservation': read(d / 'reservation.json'), 'files': inventory(d.rglob('*'))})
    if not partial: require(len(entries) == 12, 'Twelve results required')
    name = 'partial-freeze.json' if partial else 'results-freeze.json'
    write(HERE / name, {'at': now(), 'complete': not partial, 'prepared_sha256': sha(HERE / 'prepared.json'),
        'runs': entries, 'evidence': inventory([*(HERE / 'judgments').rglob('*'), *(HERE / 'preflight').rglob('*')]),
        'runtime_reservations': {str(p.relative_to(RUNTIME)): read(p) for p in RUNTIME.rglob('*.json')},
        'stop': read(RUNTIME / 'STOP.json') if partial else None})
    return {'frozen': len(entries), 'complete': not partial}


def complete_results():
    verify(); p = HERE / 'results-freeze.json'; committed(p); frozen = read(p)
    require(frozen['complete'] and len(frozen['runs']) == 12, 'Complete committed freeze required before comparison')
    require(frozen['prepared_sha256'] == sha(HERE / 'prepared.json'), 'Preparation mismatch')
    require([{k: r[k] for k in ('case_id', 'stage', 'provider')} for r in frozen['runs']] == order(), 'Frozen order mismatch')
    verify_inventory(frozen['evidence'])
    for p in frozen['evidence']: committed(ROOT / p)
    sessions = []; data = {}
    for run in frozen['runs']:
        require(run['validation']['status'] == 'valid', 'Invalid frozen result')
        sessions.append(run['reservation']['session_id'])
        require(run['reservation']['packet_sha256'] == hashlib.sha256(packet(run['case_id'])).hexdigest(), 'Executed packet drift')
        data[run['case_id']] = validate(read(HERE / 'judgments' / run['case_id'] / 'response.json'), run['stage'], run['case_id'])
    require(len(set(sessions)) == 12, 'Primary session reuse')
    return data


def historical():
    # This is the only path that decodes historical judgment content.
    complete_results()
    return {c['qualification_id']: {name: read(ROOT / h['path']) for name, h in c['historical_context']['artifacts'].items()} for c in cases()}


def status(value, stage): return value['validity']['final_status'] if stage == 'validity' else value['anti_collapse']['status']


def metrics():
    data = complete_results(); history = historical()
    distributions = {s: dict(Counter(status(data[cid], s) for cid in ids)) for s, ids in IDS.items()}
    matches = Counter()
    for c in cases():
        cid = c['qualification_id']; s = c['stage']; current = status(data[cid], s)
        count = sum(current == status(h, s) for h in history[cid].values())
        matches[{2: 'same_as_both', 1: 'same_as_one', 0: 'different_from_both'}[count]] += 1
    kept = sum(status(data[cid], 'anti-collapse') != 'CLEAR_COLLAPSE' for cid in IDS['anti-collapse'])
    result = {'results_freeze_commit': checkpoint(HERE / 'results-freeze.json'), 'requested_judgments': 12,
        'attempted_judgments': 12, 'successful_judgments': 12, 'schema_failures': 0, 'provider_failures': 0,
        'status_distributions': distributions, 'anti_collapse_gate': {'keep': kept, 'reject': 6-kept},
        'descriptive_historical_status_comparison': {k: matches[k] for k in ('same_as_both', 'same_as_one', 'different_from_both')}}
    write(HERE / 'metrics.json', result); return result


def check_reviews(rows, outcome):
    require(outcome in OUTCOMES, 'Invalid qualification outcome')
    require(len(rows) == 12 and {r['qualification_id'] for r in rows} == {c['qualification_id'] for c in cases()}, 'Review coverage')
    for r in rows:
        require(r['source_case_id'] == r['qualification_id'], 'Review identity mismatch')
        require(r['disagreement_class'] in CATEGORIES, 'Invalid disagreement class')
        require(set(r['capability_dimensions']) == set(DIMENSIONS), 'Missing capability dimension')
        require(all(v in ('pass', 'concern', 'fail') for v in r['capability_dimensions'].values()), 'Invalid capability assessment')
        require(r['downstream_consequence'] in ('none', 'minor', 'material'), 'Invalid consequence')
        require(bool(r['rationale'].strip()) and bool(r['muse']['key_reasoning'].strip()), 'Missing rationale')


def audit():
    data = complete_results(); history = historical(); reviews = read(HERE / 'review/case-reviews.json')
    check_reviews(reviews['cases'], reviews['qualification'])
    require(reviews['results_freeze_commit'] == checkpoint(HERE / 'results-freeze.json'), 'Review freeze binding')
    for r in reviews['cases']:
        cid = r['qualification_id']; s = case(cid)['stage']
        require(r['muse']['status'] == status(data[cid], s), 'Reviewed Muse status changed')
        for name in ('astra', 'fable'): require(r['historical_context'][name+'_status'] == status(history[cid][name], s), 'Historical review status changed')
    reservations = [read(p) for base in ('preflight','judgments') for p in (HERE / base).rglob('reservation.json') if 'session_id' in read(p)]
    require(len(reservations) == len({r['session_id'] for r in reservations}) == 14, 'Expected fourteen unique probe/primary requests')
    result = {'at': now(), 'results_freeze_commit': reviews['results_freeze_commit'],
        'primary_calls': {'muse': 12, 'astra': 0, 'fable': 0}, 'artificial_probes': 2,
        'unique_request_sessions': 14, 'harness_retries': 0, 'historical_artifacts_unchanged': True,
        'experiment_f_calls': 0, 'disagreement_counts': dict(Counter(r['disagreement_class'] for r in reviews['cases']))}
    write(HERE / 'review/execution-audit.json', result); return result


def one(stage, cid):
    if cid:
        prerequisites(); run = next(r for r in order() if r['case_id'] == cid)
        require(stage == run['stage'], 'Wrong stage')
        require(read(RUNTIME / 'measurement-reservation.json')['commit'] == head(), 'Measurement commit drift')
        require(all(read(HERE / 'judgments' / r['case_id'] / 'validation.json')['status'] == 'valid' for r in order()[:order().index(run)]), 'Out of order')
        directory = HERE / 'judgments' / cid; raw = packet(cid)
    else:
        require(read(RUNTIME / 'preflight-reservation.json')['commit'] == head(), 'Preflight commit drift')
        directory = HERE / 'preflight' / stage
        raw = ('Return exactly this artificial formatting fixture; no classification, tools or external context.\n' + json.dumps(fixture(stage))).encode()
    result = execute(stage, directory, raw, cid)
    print('muse', stage, cid or 'artificial', result['status'], flush=True)
    require(result['status'] == 'valid', 'Request failed; scheduling stopped')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    actions = {'verify': verify, 'catalog': catalog, 'preflight': preflight, 'run': run_all,
        'freeze': freeze, 'freeze-failure': lambda: freeze(True), 'metrics': metrics, 'audit': audit}
    p.add_argument('action', choices=(*actions, '_one')); p.add_argument('--stage', choices=tuple(IDS)); p.add_argument('--case')
    a = p.parse_args()
    try:
        if a.action == '_one': require(a.stage is not None, 'Stage required'); result = one(a.stage, a.case)
        else: result = actions[a.action]()
        if result is not None: print(json.dumps(result, indent=2))
    except Exception as exc:
        print(safe_error(exc), file=sys.stderr); sys.exit(1)


if __name__ == '__main__': main()
