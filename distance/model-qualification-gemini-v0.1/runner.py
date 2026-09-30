#!/usr/bin/env python3
"""One-shot, Gemini-only qualification; historical comparison requires committed results."""
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
from decimal import Decimal

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RUNTIME = ROOT / '.runtime/model-qualification-gemini-v0.1'
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
gemini = module('qualification_gemini', HERE / 'provider/gemini/adapter.py')
cost = module('gemini_cost', HERE / 'provider/gemini/cost.py')
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
def packet(cid, provider='gemini'):
    require(provider == 'gemini', 'Only Gemini receives fresh measurements')
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
        require(raw_identity(c), 'Prior qualification packet mismatch')
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
        for banned in ('historical_context', 'historical_fable', 'operator metadata', 'coverage intent', 'stable valid anchor', 'historical disagreement', 'Claude', 'Fable', 'Astra', 'Gemini', 'Muse'):
            require(banned.casefold() not in raw.decode().casefold(), 'Operator label leakage')
    runs = order()
    require(len(runs) == 12 and {r['case_id'] for r in runs} == {c['qualification_id'] for c in rows}, 'Schedule coverage')
    require(all(r['provider'] == 'gemini' and r['stage'] == case(r['case_id'])['stage'] for r in runs), 'Invalid scheduled provider/stage')
    require(all(a['stage'] != b['stage'] for a, b in zip(runs, runs[1:])), 'Strata not interleaved')
    cfg = config()
    require(set(cfg['providers']) == {'gemini'} and cfg['primary_budget'] == {'gemini': 12} and cfg['preflight_budget'] == {'gemini': 2}, 'Provider budget')
    require(cfg['starting_sha'] == read(HERE / 'manifest.json')['base_commit'] == 'cb5ac745d4326bc6a097411b819c14563ae28c80', 'Starting SHA mismatch')
    contract = read(HERE / 'manifest.json')['capability_contract']
    require(sha(HERE / 'CAPABILITY-CONTRACT.md') == contract['sha256'] == sha(ROOT / contract['path']), 'Capability contract changed')
    require(cfg['harness_retries'] == 0 and not cfg['fallback_allowed'] and cfg['cost_ceiling_usd'] == '2.00', 'Unsafe execution configuration')
    gemini.request_body('probe', {}, cfg['providers']['gemini'])
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
    key = os.environ.get('GEMINI_API_KEY')
    return value.replace(key, '[REDACTED]') if key else value


def failure_kind(exc):
    if isinstance(exc, jsonschema.ValidationError): return 'schema_failure'
    if isinstance(exc, json.JSONDecodeError): return 'malformed_output'
    if isinstance(exc, TimeoutError): return 'timeout'
    if 'cost' in str(exc).lower() or 'usage' in str(exc).lower() or 'consumption' in str(exc).lower(): return 'cost_or_usage_failure'
    if 'model' in str(exc).lower(): return 'model_identity_failure'
    if 'credential' in str(exc).lower(): return 'credential_unavailable'
    return 'provider_or_protocol_failure'



def raw_identity(c):
    return (ROOT / c['packet_path']).read_bytes() == (ROOT / c['prior_packet_path']).read_bytes()


def pricing(): return read(HERE / 'provider/gemini/pricing.json')


def cumulative():
    total = Decimal(0)
    for base in ('preflight', 'judgments'):
        for p in (HERE / base).glob('*/reservation.json'):
            if (p.parent / 'cost.json').exists(): total += Decimal(read(p.parent / 'cost.json')['estimated_usd'])
            elif (p.parent / 'request-sent.json').exists(): total += Decimal(read(p)['cost_reservation']['reserved_usd'])
    return total


def scan():
    key = os.environ.get('GEMINI_API_KEY')
    require(bool(key), 'Credential required for secret scan')
    paths = set(git('ls-files').decode().splitlines())
    paths.update(str(p.relative_to(ROOT)) for p in HERE.rglob('*') if p.is_file())
    for name in paths:
        p = ROOT / name
        require(key.encode() not in p.read_bytes(), 'Credential detected; path withheld')
    return {'scanned_artifacts': len(paths), 'secret_present': False}


def execute(stage, directory, raw, cid=None):
    guard(); directory.mkdir(parents=True, exist_ok=False)
    session = str(uuid.uuid4()); cfg = config(); arm = cfg['providers']['gemini']
    metadata = None; received = False
    reservation = {'at': now(), 'input_commit': head(), 'provider': 'gemini', 'stage': stage, 'case_id': cid,
        'session_id': session, 'process_id': os.getpid(), 'packet_sha256': hashlib.sha256(raw).hexdigest(),
        'canonical_schema_sha256': sha(canonical(stage)), 'wire_schema_sha256': sha(wire(stage)),
        'configuration': arm, 'python_version': sys.version, 'api_version': 'v1beta',
        'fresh_process': True, 'history_messages': 0, 'tools': [], 'credential_source': 'environment', 'harness_retries': 0}
    try:
        with tempfile.TemporaryDirectory(prefix='gemini-qualification-') as cwd:
            reservation.update(working_directory=cwd, working_directory_initially_empty=not list(Path(cwd).iterdir()))
            body = gemini.request_body(raw.decode(), read(wire(stage)), arm)
            reserve = cost.reserve(body, pricing()); prior = cumulative()
            reservation.update(cost_reservation=reserve, cumulative_before_usd=str(prior))
            put(directory / 'prompt.txt', raw); write(directory / 'request.json', body); write(directory / 'reservation.json', reservation)
            require(prior + Decimal(reserve['reserved_usd']) <= Decimal(cfg['cost_ceiling_usd']), 'Cost ceiling blocks next request')
            require(bool(os.environ.get('GEMINI_API_KEY')), 'Gemini environment credential unavailable')
            previous = Path.cwd()
            try:
                os.chdir(cwd)
                result = gemini.request(body, cfg['timeout_seconds'], lambda n, b: put(directory / n, b),
                    lambda: write(directory / 'request-sent.json', {'at': now(), 'session_id': session, 'attempt': 1}))
            finally: os.chdir(previous)
            received = True
            usage = cost.account(result.get('usageMetadata'), pricing())
            usage['cumulative_estimated_usd'] = str(prior + Decimal(usage['estimated_usd']))
            write(directory / 'cost.json', usage)
            require(usage['input_tokens'] <= reserve['input_token_upper_estimate'] and usage['billable_output_tokens'] <= 32768, 'Token consumption exceeded reserved bounds')
            require(prior + Decimal(usage['estimated_usd']) <= Decimal(cfg['cost_ceiling_usd']), 'Observed cost ceiling exceeded')
            text, metadata = gemini.parse_response(result, session)
            put(directory / 'response.json', text.encode())
            value = read(directory / 'response.json'); validate(value, stage, cid)
            if cid is None: require(value == fixture(stage), 'Artificial fixture mismatch')
            validation = {'status': 'valid', 'at': now(), 'metadata': metadata, 'error': None}
    except Exception as exc:
        if not (directory / 'reservation.json').exists(): write(directory / 'reservation.json', reservation)
        validation = {'status': 'failed', 'at': now(), 'metadata': metadata, 'error': safe_error(exc),
                      'failure_kind': failure_kind(exc), 'response_received': received,
                      'request_may_have_been_sent': (directory / 'request-sent.json').exists()}
        stop(str(directory.relative_to(ROOT)), validation['error'])
    write(directory / 'validation.json', validation)
    return validation


def child(stage, cid=None):
    cmd = [sys.executable, '-B', str(HERE / 'runner.py'), '_one', '--stage', stage]
    if cid: cmd += ['--case', cid]
    # Only the Gemini credential and ordinary runtime/transport environment are inherited.
    env = {k: v for k, v in os.environ.items() if k in ('PATH', 'LANG', 'LC_ALL', 'TMPDIR', 'SSL_CERT_FILE', 'SSL_CERT_DIR', 'HTTPS_PROXY', 'HTTP_PROXY', 'NO_PROXY', 'GEMINI_API_KEY')}
    p = subprocess.run(cmd, cwd=ROOT, env=env)
    require(p.returncode == 0, 'Isolated child stopped; inspect preserved failure')


def preflight():
    guard()
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
    complete_results()
    preliminary = HERE / 'review/preliminary.json'
    require(preliminary.exists(), 'Independent preliminary review required before historical decoding')
    require(len(read(preliminary)['cases']) == 12, 'Incomplete preliminary review')
    return {c['qualification_id']: {name: read(ROOT / h['path']) for name, h in c['historical_context']['artifacts'].items()} for c in cases()}


def status(value, stage): return value['validity']['final_status'] if stage == 'validity' else value['anti_collapse']['status']


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
    print('gemini', stage, cid or 'artificial', result['status'], flush=True)
    require(result['status'] == 'valid', 'Request failed; scheduling stopped')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    actions = {'verify': verify, 'scan': scan, 'preflight': preflight, 'run': run_all,
        'freeze': freeze, 'freeze-failure': lambda: freeze(True)}
    p.add_argument('action', choices=(*actions, '_one')); p.add_argument('--stage', choices=tuple(IDS)); p.add_argument('--case')
    a = p.parse_args()
    try:
        if a.action == '_one': require(a.stage is not None, 'Stage required'); result = one(a.stage, a.case)
        else: result = actions[a.action]()
        if result is not None: print(json.dumps(result, indent=2))
    except Exception as exc:
        print(safe_error(exc), file=sys.stderr); sys.exit(1)


if __name__ == '__main__': main()
