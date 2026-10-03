#!/usr/bin/env python3
"""H7 generation, atomization and role stages. Offline by default; no retries or automatic recovery."""
import argparse
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

from jsonschema import Draft202012Validator

H = Path(__file__).resolve().parent
R = H.parents[1]
RT = R / '.runtime/natural-admission-v0.2'
sys.path.insert(0, str(R / 'scripts'))
import experiment_budget as budget
import codex_usage as usage


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read(path):
    return json.loads(path.read_text(), object_pairs_hook=unique)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def raw(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(value)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=R).decode().strip()


def head():
    return git('rev-parse', 'HEAD')


def order():
    return read(H / 'manifest.json')['packet_order']


def config():
    return read(H / 'execution-config.json')


def inventory(paths):
    return {str(p.relative_to(R)): sha(p) for p in sorted(paths) if p.is_file()}


def effective_freeze_files():
    """Keep original freezes; apply only the user's hash-bound policy amendment."""
    files = {}
    for name in ('preservation.json', 'initial-freeze.json'):
        files.update(read(H / name)['files'])
    for amendment_name in ('usage-gate-amendment.json', 'role-stage-amendment.json', 'unified-gate-amendment.json'):
        amendment = read(H / amendment_name)
        for name, change in amendment['changes'].items():
            require(files.get(name) == change['original_sha256'], 'Amendment baseline mismatch: ' + name)
            files[name] = change['updated_sha256']
    files.update(read(H / 'role-stage-static-freeze.json')['files'])
    amendment = read(H / 'continuation-amendment.json')
    for name, change in amendment['changes'].items():
        require(files.get(name) == change['original_sha256'], 'Continuation baseline mismatch: ' + name)
        files[name] = change['updated_sha256']
    files.update(amendment['added_files'])
    return files


def verify():
    require(git('branch', '--show-current') == 'experiment-h7-natural-admission', 'Wrong branch')
    require(len(order()) == 6 and len(set(order())) == 6, 'Exactly six distinct slots')
    files = effective_freeze_files()
    for p in sorted(H.glob('*-freeze.json')):
        if p.name not in ('initial-freeze.json', 'role-stage-static-freeze.json'):
            files.update(read(p)['files'])
    for name, digest in files.items():
        require(sha(R / name) == digest, 'INTEGRITY: ' + name)
    c = config()
    require(c['model'] == 'gpt-6-astra' and c['reasoning_effort'] == 'high', 'Model drift')
    require(sha(Path(c['cli'])) == c['cli_sha256'], 'CLI drift')
    require(sha(Path(c['native_executable']['path'])) == c['native_executable']['sha256'], 'Native drift')
    require(subprocess.check_output([c['cli'], '--version'], text=True).strip() == c['cli_version'], 'CLI version drift')
    return {'historical_files_checked': len(read(H / 'preservation.json')['files']),
            'authorized_amendments': ['usage-gate-amendment.json', 'role-stage-amendment.json', 'unified-gate-amendment.json'], 'slots': 6}


def state():
    paths = sorted((RT / 'states').glob('*.json'))
    return read(paths[-1])['state'] if paths else None


def transition(value, reason):
    paths = sorted((RT / 'states').glob('*.json'))
    write(RT / 'states' / f'{len(paths):04}.json', {
        'state': value, 'reason': reason, 'at': usage.stamp(), 'commit': head(),
        'previous_sha256': sha(paths[-1]) if paths else None})


def command(cwd, output, stage):
    c = config()
    cmd = [c['cli'], 'exec', '--ignore-user-config', '--ignore-rules', '--ephemeral',
           '--skip-git-repo-check', '--sandbox', 'read-only', '--json', '--color', 'never',
           '--cd', str(cwd), '--model', 'gpt-6-astra', '-c', 'model_reasoning_effort="high"',
           '-c', 'project_doc_max_bytes=0', '-c', 'web_search="disabled"',
           '--output-schema', str(H / 'schemas' / f'{stage}.schema.json'),
           '--output-last-message', str(output / 'response.json')]
    for feature in c['disabled_features']:
        cmd += ['--disable', feature]
    return cmd + ['-']


def clean_env():
    return {k: v for k, v in os.environ.items()
            if not k.startswith(('CODEX_', 'CLAUDE_', 'ANTHROPIC_', 'OPENAI_',
                                 'AZURE_OPENAI_', 'GEMINI_', 'GOOGLE_GENAI_'))
            and k not in ('CLAUDECODE', 'MODEL_PROVIDER', 'MODEL', 'LLM_MODEL')}


def audit(events, response):
    starts = [e for e in events if e.get('type') == 'thread.started']
    require(len(starts) == 1 and starts[0].get('thread_id'), 'Fresh session missing')
    require(sum(e.get('type') == 'turn.completed' for e in events) == 1, 'Incomplete turn')
    require(not any(e.get('type') in ('error', 'turn.failed') for e in events), 'Provider failure')
    require(all(e['item'].get('type') in ('agent_message', 'reasoning')
                for e in events if 'item' in e), 'Tool activity')
    finals = [e['item']['text'] for e in events if e.get('type') == 'item.completed'
              and e.get('item', {}).get('type') == 'agent_message']
    require(len(finals) == 1 and finals[0].strip() == response.strip(), 'Final stream mismatch')
    models = []

    def walk(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in ('model', 'model_id', 'model_name') and isinstance(child, str):
                    models.append(child)
                require(not ('fallback' in key.lower() and child), 'Fallback event')
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(events)
    require(all(m == 'gpt-6-astra' for m in models), 'Model substitution')
    return {'session_id': starts[0]['thread_id'], 'requested_model': 'gpt-6-astra',
            'requested_reasoning_effort': 'high', 'returned_model_identifiers': models,
            'verified_served_snapshot': None,
            'usage': [e.get('usage') for e in events if e.get('type') == 'turn.completed'],
            'retry_observability': 'No harness retries; provider-internal behavior unavailable.'}


def validate_claims(value, packet):
    require(value['packet_id'] == packet['packet_id'], 'Packet identity mismatch')
    ids = [c['claim_id'] for c in value['claims']]
    require(ids and len(ids) == len(set(ids)), 'Missing/duplicate claims')
    allowed = set(packet['allowed_source_ids'])
    for claim in value['claims']:
        require(claim['proposition'].strip() and claim['fields'], 'Empty proposition/location')
        require(claim['evidence_used'], 'Unlocated claim')
        for ref in claim['evidence_used']:
            require(ref['source_id'] in allowed, 'RESPONSE_SOURCE_UNKNOWN')
    coverage = value['coverage']
    require(len(coverage) == 5 and {x['field'] for x in coverage} ==
            {'state', 'operation', 'signal', 'inference', 'limit'}, 'Field coverage missing')
    for item in coverage:
        require(set(item['claim_ids']) <= set(ids), 'Unknown claim in coverage')
        require(not item['unrepresented_material'], 'Material atomization coverage unresolved')
    for claim in value['claims']:
        for field in claim['fields']:
            require(any(c['field'] == field and claim['claim_id'] in c['claim_ids']
                        for c in coverage), 'Claim absent from declared field coverage')


def reserve_and_launch(gate, plan, policy, stage, uid, argv, launch):
    """The only provider launch path. Reservation failure cannot reach transport."""
    gate.reserve(plan, policy, stage, uid, argv)
    return launch()


def execute(stage, cid, plan):
    verify()
    require(not git('status', '--porcelain'), 'Unclean checkpoint')
    require(state() == 'RUNNING', 'Scheduling paused')
    import continuation
    continuation.guard(sys.modules[__name__], cid, stage)
    d = RT / 'attempts' / stage / cid
    d.mkdir(parents=True, exist_ok=False)
    request = (H / 'packets' / stage / f'{cid}.txt').read_bytes()
    raw(d / 'request.txt', request)
    uid = stage + '/' + cid
    gate = budget.Gate()
    policy = read(R / 'docs/experiment-budget-policy.json')
    with tempfile.TemporaryDirectory(prefix='h7-isolated-') as cwd:
        cmd = command(cwd, d, stage)
        write(d / 'attempt.json', {'at': usage.stamp(), 'execution_commit': head(),
              'stage': stage, 'packet_id': cid, 'command': cmd, 'initially_empty': True,
              'request_sha256': sha(d / 'request.txt'),
              'schema_sha256': sha(H / 'schemas' / f'{stage}.schema.json'),
              'configuration': config(), 'allowed_mapping_packets': [cid],
              'collision_exposure': 0, 'harness_attempt': 1})

        def launch():
            # All paths opened before Popen; an uncertain launch is never retried.
            with (d / 'events.jsonl').open('x') as out, (d / 'stderr.txt').open('x') as err:
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=out, stderr=err,
                                           cwd=cwd, env=clean_env(), start_new_session=True)
                write(d / 'process.json', {'pid': process.pid, 'at': usage.stamp()})
                try:
                    process.communicate(request, timeout=config()['timeout_seconds'])
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                    write(d / 'exit.json', {'returncode': process.returncode, 'timeout': True})
                    gate.finish(plan['experiment_id'], uid, process.returncode)
                    raise
                write(d / 'exit.json', {'returncode': process.returncode})
                gate.finish(plan['experiment_id'], uid, process.returncode)
                require(process.returncode == 0, 'Provider/transport nonzero exit')
        reserve_and_launch(gate, plan, policy, stage, uid, cmd, launch)
    response = (d / 'response.json').read_text()
    events = [json.loads(line, object_pairs_hook=unique)
              for line in (d / 'events.jsonl').read_text().splitlines() if line.strip()]
    metadata = audit(events, response)
    prior = [read(p)['metadata']['session_id'] for p in (RT / 'attempts').glob('*/*/validation.json')]
    require(metadata['session_id'] not in prior, 'Session reuse')
    value = json.loads(response, object_pairs_hook=unique)
    Draft202012Validator(read(H / 'schemas' / f'{stage}.schema.json')).validate(value)
    if stage == 'claims':
        validate_claims(value, read(H / 'packets' / stage / f'{cid}.json'))
    elif stage in ('classification', 'discovery'):
        import stages
        stages.validate(stage, value, read(H / 'packets' / stage / f'{cid}.json'))
    write(d / 'validation.json', {'metadata': metadata, 'response_sha256': sha(d / 'response.json'),
                                 'schema_valid': True})


def check_usage_review(report, review):
    require(not report['refresh_required'], 'Refresh account reading; approval cannot replace it')
    if report['approval_required']:
        require(review.get('usage_approved') is True and review.get('usage_consent_reference', '').strip(),
                'Usage approval required below 30% remaining')


def run_batch(path):
    """Read an operator-reviewed, fresh preflight; never create approval here."""
    review = read(path)
    require(review['authorization_reference'].strip(), 'Scientific task authorization reference required')
    stage, ids = review['stage'], review['packet_ids']
    require(stage in ('generation', 'claims', 'classification', 'discovery'), 'Evaluation remains gated')
    require(1 <= len(ids) <= 2 and len(set(ids)) == len(ids), 'Batch limit is two')
    remaining = [cid for cid in order() if not (RT / 'attempts' / stage / cid).exists()]
    require(ids == remaining[:len(ids)], 'Frozen order or already attempted slot')
    require(state() in (None, 'COMPLETE'), 'Pause/terminal states need committed recovery evidence')
    verify()
    if stage != 'generation':
        require((H / f'{stage}-packets-freeze.json').exists(), 'Stage packets not frozen')
    plan = read(H / 'budgets/plan-005.json')
    require(plan['execution_fingerprint'] == budget.digest(effective_freeze_files()),
            'Execution fingerprint changed')
    require(review['plan_sha256'] == budget.digest(plan), 'Budget plan changed')
    before, calibration, usage_plan = (read(Path(review[key])) for key in
                                      ('snapshot_path', 'calibration_path', 'usage_plan_path'))
    declared = next(s for s in plan['stages'] if s['id'] == stage)
    require(usage_plan == {'stages': [{**declared, 'sessions': len(ids)}]}, 'Usage batch mismatch')
    report = usage.predict(usage_plan, before, calibration, reserve_points=10)
    check_usage_review(report, review)
    require(0 <= datetime.now(timezone.utc).timestamp() - usage.epoch(before['captured_at']) <= 300,
            'Fresh snapshot required')
    require(all(w['resets_at'] > datetime.now(timezone.utc).timestamp() for w in before['windows']),
            'Reset crossed; refresh account snapshot')
    require(review['snapshot_sha256'] == usage.canonical_hash(before), 'Snapshot changed')
    require(review['calibration_sha256'] == usage.canonical_hash(calibration), 'Calibration changed')
    require(not git('status', '--porcelain'), 'Unclean checkpoint')
    gate = budget.Gate()
    require(gate.status(plan, read(R / 'docs/experiment-budget-policy.json'))['allowed'], 'Budget gate denied')
    batch = RT / 'batches' / f'{len(list((RT / "batches").glob("*"))):04}'
    write(batch / 'review.json', review)
    write(batch / 'before.json', before)
    write(batch / 'forecast.json', report)
    write(batch / 'calibration-before.json', calibration)
    transition('RUNNING', f'{stage}: {ids}')
    try:
        for cid in ids:
            execute(stage, cid, plan)
        transition('COMPLETE', 'Bounded batch complete, not experiment completion')
    except BaseException as exc:
        write(batch / 'failure.json', {'error': type(exc).__name__ + ': ' + str(exc), 'at': usage.stamp()})
        transition('PAUSED_AMBIGUOUS', 'Preserve; no retry/substitution; classify incident before any continuation')
        raise
    finally:
        try:
            after = usage.normalize(usage.read_limits(cli=config()['cli']), before['account_scope'])
            write(batch / 'after.json', after)
            attempts = [RT / 'attempts' / stage / cid for cid in ids]
            launched = sum((p / 'process.json').exists() for p in attempts)
            observations = [read(p / 'validation.json')['metadata']['usage'] for p in attempts
                            if (p / 'validation.json').exists()]
            write(batch / 'calibration-record.json', {
                'usage_profile': declared['usage_profile'], 'sessions': launched,
                'available_usage': observations, 'before': before, 'after': after,
                'isolated_account_work': False, 'included_as_clean_calibration': False,
                'exclusion_reason': 'Concurrent account work/telemetry isolation not attested; review before inclusion.',
                'potential_uncertain_launches': [str(p) for p in attempts if p.exists() and not (p / 'process.json').exists()]})
        except Exception as exc:
            write(batch / 'bookkeeping-failure.json', {'error': str(exc)})
            if state() == 'COMPLETE':
                transition('PAUSED_RECOVERABLE', 'Usage after-snapshot/bookkeeping requires preserved recovery')


def freeze(stage):
    verify()
    require(state() == 'COMPLETE', 'Stage cannot freeze during pause')
    paths = []
    for cid in order():
        d = RT / 'attempts' / stage / cid
        require((d / 'validation.json').exists(), 'All six require validation or explicit quarantine recovery')
        require(sha(d / 'response.json') == read(d / 'validation.json')['response_sha256'], 'Response drift')
        require(not (H / stage / f'{cid}.json').exists(), 'Already published')
    for cid in order():
        d = RT / 'attempts' / stage / cid
        for p in sorted(d.iterdir()):
            dest = H / 'raw' / stage / cid / p.name
            raw(dest, p.read_bytes())
            paths.append(dest)
        dest = H / stage / f'{cid}.json'
        write(dest, read(d / 'response.json'))
        paths.append(dest)
    write(H / f'{stage}-freeze.json', {'execution_parent': head(), 'files': inventory(paths)})


def prepare_claims():
    verify()
    require((H / 'generation-freeze.json').exists(), 'Freeze generations first')
    require(not git('status', '--porcelain'), 'Commit generation freeze first')
    spec = importlib.util.spec_from_file_location('h7_h5', R / 'distance/span-provenance-calibration-v0.1/segment.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    paths = []
    for cid in order():
        mapping = read(H / 'generation' / f'{cid}.json')['instrument']
        table = module.segment(cid, mapping)
        p = H / 'span-tables' / f'{cid}.json'
        write(p, table)
        paths.append(p)
        packet = read(H / 'packets/generation' / f'{cid}.json')
        packet.update(mapping=mapping, allowed_source_ids=list(table['spans']),
                      spans={sid: {k: v for k, v in s.items() if k != 'source_range'}
                             for sid, s in table['spans'].items()})
        p = H / 'packets/claims' / f'{cid}.json'
        write(p, packet)
        paths.append(p)
        p = p.with_suffix('.txt')
        raw(p, ((H / 'prompts/claims.md').read_text() + '\nFROZEN PACKET\n' +
                json.dumps(packet, indent=2) + '\n').encode())
        paths.append(p)
    write(H / 'claims-packets-freeze.json', {'parent_commit': head(), 'files': inventory(paths)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('verify')
    sub.add_parser('resume-continuation')
    p = sub.add_parser('run-batch'); p.add_argument('--review', type=Path, required=True)
    p = sub.add_parser('freeze'); p.add_argument('stage', choices=['generation', 'claims', 'classification', 'discovery'])
    sub.add_parser('prepare-claims')
    sub.add_parser('freeze-obligations')
    p = sub.add_parser('prepare-role'); p.add_argument('stage', choices=['classification', 'discovery'])
    args = parser.parse_args()
    if args.action == 'verify': print(json.dumps(verify(), indent=2))
    elif args.action == 'resume-continuation':
        import continuation
        continuation.resume(sys.modules[__name__])
    elif args.action == 'run-batch': run_batch(args.review)
    elif args.action == 'freeze': freeze(args.stage)
    elif args.action == 'freeze-obligations':
        import stages
        stages.freeze_obligations(sys.modules[__name__])
    elif args.action == 'prepare-role':
        import stages
        stages.prepare(args.stage, sys.modules[__name__])
    else: prepare_claims()


if __name__ == '__main__':
    main()
