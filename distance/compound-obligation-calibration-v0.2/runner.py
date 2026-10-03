#!/usr/bin/env python3
"""H6.R3: offline preparation and explicit gated batches; no automatic consent/retry."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
import re
from pathlib import Path
import signal
import sqlite3
import subprocess
import sys
import tempfile
import contracts as c
H = Path(__file__).resolve().parent
R = H.parents[1]
RT = R / '.runtime/compound-obligation-calibration-v0.2'
sys.path.insert(0, str(R / 'scripts'))
import experiment_budget as budget
import codex_usage as usage
STAGES = ('classification', 'dependency', 'evaluation')


def now():
    return datetime.now(timezone.utc).isoformat()


def unique(pairs):
    result = {}
    for key, value in pairs:
        c.require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read(path):
    return json.loads(path.read_text(), object_pairs_hook=unique)


def raw(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)


def write(path, value):
    raw(path, (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=R).decode().strip()


def head():
    return git('rev-parse', 'HEAD')


def rel(path):
    return str(path.relative_to(R))


def committed(path):
    actual = subprocess.check_output(['git', 'show', 'HEAD:' + rel(path)], cwd=R)
    c.require(actual == path.read_bytes(), 'Uncommitted dependency: ' + rel(path))


def inventory(paths):
    return {rel(p): sha(p) for p in sorted(paths) if p.is_file() and '__pycache__' not in p.parts}


def hashes(files, commit=False):
    for path, expected in files.items():
        p = R / path
        c.require(sha(p) == expected, 'Frozen hash changed: ' + path)
        if commit:
            committed(p)


def config():
    return read(H / 'execution-config.json')


def manifest():
    return read(H / 'manifest.json')


def taxonomy():
    return read(H / 'taxonomy.json')


def stem(uid):
    return uid.replace('/', '--')


def judgment(stage, uid):
    return H / (stage + '-judgments') / (stem(uid) + '.json')


def packet_path(stage, uid, suffix='json'):
    return H / (stage + '-packets') / (stem(uid) + '.' + suffix)


def frozen_path(stage):
    return H / (stage + '-freeze.json')


def require_freeze(stage):
    p = frozen_path(stage)
    c.require(p.exists(), 'Missing complete stage freeze: ' + stage)
    committed(p)
    hashes(read(p)['files'], commit=True)
    return read(p)


def binary_check():
    cfg = config()
    c.require(cfg['model'] == 'gpt-6-astra' and cfg['reasoning_effort'] == 'high', 'Model drift')
    c.require(sha(Path(cfg['cli'])) == cfg['cli_sha256'], 'CLI drift')
    c.require(sha(Path(cfg['native_executable']['path'])) == cfg['native_executable']['sha256'],
              'Native executable drift')
    c.require(subprocess.check_output([cfg['cli'], '--version'], text=True).strip() == cfg['cli_version'],
              'CLI version drift')


def clean_env():
    return {key: val for key, val in os.environ.items()
            if not key.startswith(('CODEX_', 'CLAUDE_', 'ANTHROPIC_', 'OPENAI_', 'AZURE_OPENAI_',
                                   'GEMINI_', 'GOOGLE_GENAI_'))
            and key not in ('CLAUDECODE', 'MODEL_PROVIDER', 'MODEL', 'LLM_MODEL')}


def command(stage, cwd, destination):
    cfg = config()
    cmd = [cfg['cli'], 'exec', '--ignore-user-config', '--ignore-rules', '--ephemeral',
           '--skip-git-repo-check', '--sandbox', 'read-only', '--json', '--color', 'never',
           '--cd', str(cwd), '--model', cfg['model'], '-c', 'model_reasoning_effort="high"',
           '-c', 'project_doc_max_bytes=0', '-c', 'web_search="disabled"',
           '--output-schema', str(H / 'schemas' / (stage + '-wire.schema.json')),
           '--output-last-message', str(destination / 'response.json')]
    for feature in cfg['disabled_features']:
        cmd.extend(['--disable', feature])
    return cmd + ['-']


def plan_file():
    revisions = sorted((H / 'budgets').glob('plan-*.json'))
    c.require(revisions, 'Missing cumulative financial plan')
    return revisions[-1]


def latest_state():
    paths = sorted((RT / 'states').glob('*.json'))
    return read(paths[-1]) if paths else None


def transition(state, detail):
    paths = sorted((RT / 'states').glob('*.json'))
    write(RT / 'states' / f'{len(paths):04}.json', {'at': now(), 'state': state, 'detail': detail,
          'execution_commit': head(), 'previous_sha256': sha(paths[-1]) if paths else None})


def active_batch(stage, uid):
    state = latest_state()
    c.require(state is not None and state['state'] == 'RUNNING', 'No active authorized batch')
    batch = read(Path(state['detail']['batch']) / 'batch.json')
    c.require(batch['stage'] == stage and uid in batch['claim_ids'], 'Outside active batch')


def forecast(out, scope, calibration):
    verify()
    plan = check_plan()
    out = out.resolve()
    c.require(out.is_relative_to(RT), 'Account forecasts must stay under experiment .runtime')
    before = usage.normalize(usage.read_limits(config()['cli']), scope)
    write(out / 'before.json', before)
    cal = read(calibration)
    write(out / 'calibration.json', cal)
    remaining = remaining_plan(plan)
    write(out / 'usage-plan.json', remaining)
    # Use timestamp precision preserved in JSON so exact preflight replay works.
    report = usage.predict(remaining, before, cal, reserve_points=10, as_of=usage.epoch(now()))
    write(out / 'usage-report.json', report)
    status = budget.Gate().status(plan, read(budget.DEFAULT_POLICY))
    write(out / 'financial-report.json', status)
    print(json.dumps({'financial': status, 'usage': report}, indent=2))
    return 2 if not status['allowed'] or report['approval_required'] else 0


def approve_usage_check(report, plan, review, stage, count):
    if not report['approval_required']:
        return
    c.require(review is not None, 'Usage forecast requires explicit user review')
    consent = read(review)
    c.require(consent['plan_sha256'] == budget.digest(plan) and
              consent['report_sha256'] == report['report_sha256'] and
              consent['stage'] == stage and consent['max_sessions'] >= count and
              bool(consent['user_message_reference'].strip()), 'Usage consent does not cover this exact batch')


def usage_check(preflight, plan, stage, count, review):
    snapshot = read(preflight / 'before.json')
    calibration = read(preflight / 'calibration.json')
    remaining = remaining_plan(plan)
    c.require(read(preflight / 'usage-plan.json') == remaining, 'Remaining work changed; reforecast')
    report = read(preflight / 'usage-report.json')
    historical = usage.predict(remaining, snapshot, calibration, 10,
                               as_of=usage.epoch(report['forecast_at']))
    c.require(report == historical, 'Usage report changed or inputs mismatched')
    current = usage.predict(remaining, snapshot, calibration, 10)
    c.require(not current['global_reasons'], 'Fresh complete allowance snapshot required')
    c.require(all(w['seconds_until_reset'] > 0 for w in current['windows']), 'Reset passed; reforecast')
    approve_usage_check(report, plan, review, stage, count)
    return snapshot


def audit_events(events, response):
    starts = [e for e in events if e.get('type') == 'thread.started']
    c.require(len(starts) == 1 and starts[0].get('thread_id'), 'Fresh session missing')
    c.require(sum(e.get('type') == 'turn.completed' for e in events) == 1, 'Incomplete turn')
    c.require(not any(e.get('type') in ('error', 'turn.failed') for e in events), 'Provider event')
    c.require(all(e['item'].get('type') in ('agent_message', 'reasoning') for e in events if 'item' in e),
              'Unexpected tool activity')
    models = []

    def walk(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in ('model', 'model_id', 'model_name') and isinstance(item, str):
                    models.append(item)
                c.require(not ('fallback' in key.lower() and item), 'Fallback event')
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(events)
    c.require(all(m == 'gpt-6-astra' for m in models), 'Model substitution')
    finals = [e['item']['text'] for e in events if e.get('type') == 'item.completed'
              and e.get('item', {}).get('type') == 'agent_message']
    c.require(len(finals) == 1 and finals[0].strip() == response.strip(), 'Final stream mismatch')
    return {'session_id': starts[0]['thread_id'], 'requested_model': 'gpt-6-astra',
            'requested_reasoning_effort': 'high', 'returned_model_identifiers': models,
            'verified_served_snapshot': None,
            'usage': [e.get('usage') for e in events if e.get('type') == 'turn.completed'],
            'retry_observability': 'No harness retries; unexposed internal retries cannot be ruled out.'}


def run_one(stage, uid, plan, gate):
    active_batch(stage, uid)
    verify()
    binary_check()
    if stage == 'evaluation':
        verify_projection_barrier()
    c.require(uid in ids(stage), 'Claim is not eligible')
    c.require(not judgment(stage, uid).exists(), 'Judgment already exists')
    destination = RT / 'attempts' / stage / stem(uid)
    c.require(not destination.exists(), 'Attempt exists; no retry')
    packet = read(packet_path(stage, uid))
    c.require(packet == build_packet(stage, uid), 'Packet differs from frozen evidence construction')
    request = packet_path(stage, uid, 'txt').read_bytes()
    c.require(request == prompt(stage, packet), 'Prompt differs from frozen construction')
    session = stage + ':' + uid
    with tempfile.TemporaryDirectory(prefix='h6r3-isolated-') as cwd:
        cmd = command(stage, cwd, destination)
        # Every real provider launch is dominated by this per-session reservation.
        gate.reserve(plan, read(budget.DEFAULT_POLICY), stage, session, cmd)
        process = None
        try:
            write(destination / 'reservation.json', {'at': now(), 'session_key': session,
                  'execution_commit': head(), 'plan_sha256': budget.digest(plan), 'command': cmd,
                  'request_sha256': hashlib.sha256(request).hexdigest(),
                  'schema_sha256': sha(H / 'schemas' / (stage + '.schema.json')),
                  'wire_schema_sha256': sha(H / 'schemas' / (stage + '-wire.schema.json')),
                  'configuration': config(), 'working_directory': cwd,
                  'initially_empty': not list(Path(cwd).iterdir()), 'available_packets': [uid]})
            raw(destination / 'request.txt', request)
            with (destination / 'events.jsonl').open('xb') as out, (destination / 'stderr.txt').open('xb') as err:
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=out, stderr=err,
                                           cwd=cwd, env=clean_env(), start_new_session=True)
                write(destination / 'process.json', {'pid': process.pid, 'launched_at': now()})
                try:
                    process.communicate(request, timeout=config()['timeout_seconds'])
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                    raise
            write(destination / 'exit.json', {'at': now(), 'returncode': process.returncode})
            gate.finish(plan['experiment_id'], session, process.returncode)
            c.require(process.returncode == 0, 'CLI nonzero exit')
            response = (destination / 'response.json').read_text()
            events = [json.loads(line, object_pairs_hook=unique)
                      for line in (destination / 'events.jsonl').read_text().splitlines() if line.strip()]
            metadata = audit_events(events, response)
            sessions = [read(p)['metadata']['session_id']
                        for p in (RT / 'attempts').glob('*/*/validation.json')]
            c.require(metadata['session_id'] not in sessions, 'Session reused')
            value = json.loads(response, object_pairs_hook=unique)
            diagnostics = c.validate(stage, value, packet,
                                     read(H / 'schemas' / (stage + '.schema.json')), taxonomy())
            write(destination / 'validation.json', {'at': now(), 'schema_valid': True,
                  'metadata': metadata, 'diagnostics': diagnostics,
                  'response_sha256': sha(destination / 'response.json')})
            write(judgment(stage, uid), value)
            return metadata
        except BaseException as exc:
            if process is not None and process.poll() is None:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            write(destination / 'failure.json', {'at': now(), 'error': type(exc).__name__ + ': ' + str(exc),
                  'process_created': process is not None, 'scientific_verdict_for_missing_observation': None,
                  'retry_authorized': False})
            raise


def run_batch(stage, preflight, count, review):
    c.require(1 <= count <= 3, 'Batches contain one to three sessions')
    scheduling_clear()
    verify()
    c.require(not frozen_path(stage).exists(), 'Stage already frozen')
    committed(H / (stage + '-prepared.json'))
    if stage == 'evaluation':
        verify_projection_barrier()
    plan = check_plan()
    todo = [uid for uid in ids(stage) if not judgment(stage, uid).exists()]
    selected = todo[:count]
    c.require(selected, 'No unmeasured claims')
    snapshot = usage_check(preflight, plan, stage, len(selected), review)
    gate = budget.Gate()
    c.require(gate.status(plan, read(budget.DEFAULT_POLICY))['allowed'], 'Financial approval required')
    batch = RT / 'batches' / f'{len(list((RT / "batches").glob("*"))):04}'
    write(batch / 'before.json', snapshot)
    write(batch / 'batch.json', {'at': now(), 'stage': stage, 'claim_ids': selected,
          'preflight': str(preflight), 'usage_review': str(review) if review else None,
          'plan_sha256': budget.digest(plan), 'usage_profile': next(
              s['usage_profile'] for s in plan['stages'] if s['id'] == stage)})
    transition('RUNNING', {'batch': str(batch), 'stage': stage})
    outcome = 'BATCH_COMPLETE'
    try:
        for uid in selected:
            run_one(stage, uid, plan, gate)
            print(stage + ' ' + uid + ': original response preserved', flush=True)
    except budget.BudgetError as exc:
        outcome = 'PAUSED_BUDGET'
        transition(outcome, {'error': str(exc), 'batch': str(batch)})
        raise
    except BaseException as exc:
        outcome = 'PAUSED_EVENT'
        transition(outcome, {'error': type(exc).__name__ + ': ' + str(exc), 'batch': str(batch)})
        raise
    finally:
        write(batch / 'finished.json', {'at': now(), 'state': outcome})
        try:
            write(batch / 'after-immediate.json', usage.normalize(
                usage.read_limits(config()['cli']), snapshot['account_scope']))
        except Exception as exc:
            write(batch / 'snapshot-error.json', {'at': now(), 'error': str(exc)})
    transition('BATCH_COMPLETE', {'batch': str(batch), 'bookkeeping_required': True})


def record_batch(batch, isolated, settled, reference):
    """A later read retains immediate telemetry too; operator attests isolation."""
    record = read(batch / 'batch.json')
    before = read(batch / 'before.json')
    after = usage.normalize(usage.read_limits(config()['cli']), before['account_scope'])
    write(batch / 'after-settled.json', after)
    attempts = [RT / 'attempts' / record['stage'] / stem(uid) for uid in record['claim_ids']]
    attempted = [p for p in attempts if (p / 'reservation.json').exists()]
    tokens = []
    for p in attempted:
        event_path = p / 'events.jsonl'
        if event_path.exists():
            for line in event_path.read_text().splitlines():
                try:
                    event = json.loads(line, object_pairs_hook=unique)
                except ValueError:
                    continue  # retain raw malformed bytes; no token total is invented
                if isinstance(event, dict) and event.get('usage') is not None:
                    tokens.append({'attempt': p.name, 'event_type': event.get('type'),
                                   'usage': event['usage']})
    reasons = []
    if not isolated:
        reasons.append('Account isolation not established; concurrent/unattributed activity possible')
    if not settled:
        reasons.append('Telemetry settling not established')
    if any(not (p / 'validation.json').exists() for p in attempted):
        reasons.append('Incomplete session attribution; reservations conservatively included')
    sample = {'usage_profile': record['usage_profile'], 'isolated_account_work': not reasons,
              'account_isolation_attested': isolated, 'telemetry_settled_attested': settled,
              'sessions': len(attempted), 'before': before, 'after': after,
              'available_usage_records': tokens, 'operator_reference': reference,
              'exclusion_reasons': reasons}
    for window in after['windows']:
        try:
            usage.sample_rate(sample, after, window, usage.epoch(after['captured_at']))
        except Exception as exc:
            sample['exclusion_reasons'].append(str(exc))
    write(batch / 'calibration-record.json', sample)
    write(batch / 'calibration.json', {'version': 1, 'samples': [read(p) for p in
          sorted((RT / 'batches').glob('*/calibration-record.json'))]})
    print(json.dumps({'sessions': len(attempted), 'exclusion_reasons': sample['exclusion_reasons']}, indent=2))


def freeze(stage):
    scheduling_clear()
    verify()
    expected = ids(stage)
    actual = sorted(p.stem for p in (H / (stage + '-judgments')).glob('*.json'))
    c.require(actual == sorted(stem(uid) for uid in expected), 'Stage incomplete or unexpected judgments')
    for uid in expected:
        p = judgment(stage, uid)
        value = read(p)
        c.validate(stage, value, read(packet_path(stage, uid)),
                   read(H / 'schemas' / (stage + '.schema.json')), taxonomy())
        source = RT / 'attempts' / stage / stem(uid)
        c.require(read(source / 'validation.json')['schema_valid'], 'Missing successful validation')
        c.require(value == read(source / 'response.json'), 'Observation was changed')
        verify_attempt(stage,uid,source)
        destination = H / 'raw' / stage / stem(uid)
        for artifact in source.iterdir():
            if artifact.is_file():
                raw(destination / artifact.name, artifact.read_bytes())
    dependencies = list((H / (stage + '-judgments')).glob('*.json'))
    dependencies += list((H / 'raw' / stage).rglob('*'))
    write(frozen_path(stage), {'parent_commit': head(), 'stage': stage, 'claim_ids': expected,
          'excluded_claim_ids': [uid for uid in manifest()['claim_order'] if uid not in
              ({j['claim_id'] for j in jobs().values()} if stage == 'evaluation' else set(expected))],
          'files': inventory(dependencies)})



def verify_attempt(stage,uid,source):
    reservation=read(source/'reservation.json')
    validation=read(source/'validation.json')
    response=(source/'response.json').read_text()
    events=[json.loads(line,object_pairs_hook=unique) for line in (source/'events.jsonl').read_text().splitlines() if line.strip()]
    c.require(audit_events(events,response)==validation['metadata'],'Raw event metadata changed')
    c.require(sha(source/'response.json')==validation['response_sha256'],'Raw response changed')
    c.require((source/'request.txt').read_bytes()==packet_path(stage,uid,'txt').read_bytes(),'Executed request differs from frozen packet')
    c.require(sha(source/'request.txt')==reservation['request_sha256'],'Reservation request hash mismatch')
    c.require(reservation['schema_sha256']==sha(H/'schemas'/(stage+'.schema.json')) and
              reservation['wire_schema_sha256']==sha(H/'schemas'/(stage+'-wire.schema.json')),'Executed schema mismatch')
    c.require(reservation['configuration']==config(),'Executed configuration mismatch')
    c.require(reservation['command']==command(stage,Path(reservation['working_directory']),source),'Executed command mismatch')
    c.require(reservation['initially_empty'] and reservation['available_packets']==[uid],'Isolation record mismatch')
    execution=reservation['execution_commit']
    c.require(git('merge-base',execution,'HEAD')==execution,'Execution commit is outside lineage')
    for path in (packet_path(stage,uid,'txt'),H/'runner.py',H/'contracts.py',H/'execution-config.json'):
        historical=subprocess.check_output(['git','show',execution+':'+rel(path)],cwd=R)
        c.require(historical==path.read_bytes(),'Executed input changed: '+rel(path))
    with sqlite3.connect('file:'+str(budget.DEFAULT_LEDGER)+'?mode=ro',uri=True) as db:
        db.row_factory=sqlite3.Row
        rows=db.execute('SELECT * FROM reservations WHERE experiment=? AND session=?',
            (manifest()['experiment_id'],stage+':'+uid)).fetchall()
    c.require(len(rows)==1,'Missing unique ledger reservation')
    row=rows[0]
    c.require(row['stage']==stage and row['plan_hash']==reservation['plan_sha256'] and
              json.loads(row['command_json'])==reservation['command'],'Ledger lineage mismatch')
    c.require(row['at']<=read(source/'process.json')['launched_at'],'Reservation followed launch')
    c.require(row['returncode']==read(source/'exit.json')['returncode']==0,'Unsuccessful attempt cannot freeze')
    return validation['metadata']['session_id']


def claims():
    return {claim['claim_id']: (claim, case) for case in
            [read(H/'cases'/(key+'.json')) for key in manifest()['case_order']]
            for claim in case['claims']}


def assignments():
    require_freeze('classification')
    return {uid:read(judgment('classification',uid)) for uid in manifest()['claim_order']}


def discoveries():
    require_freeze('dependency')
    require_freeze('obligation-sets')
    result = {uid: read(H / 'obligations' / (uid + '.json')) for uid in ids('dependency')}
    a, corpus = assignments(), claims()
    for uid, value in result.items():
        c.require(value == c.resolve(corpus[uid][0], a[uid], read(judgment('dependency', uid)), taxonomy()),
                  'Frozen obligations differ from frozen dependency routing')
    return result


def resolve_dependencies():
    verify(); require_freeze('dependency')
    a, corpus = assignments(), claims()
    for uid in ids('dependency'):
        value = c.resolve(corpus[uid][0], a[uid], read(judgment('dependency', uid)), taxonomy())
        write(H / 'obligations' / (uid + '.json'), value)
    write(frozen_path('obligation-sets'), {'parent_commit': head(),
          'files': inventory((H / 'obligations').glob('*.json'))})


def barrier_result():
    planned = jobs()
    packets = {p.stem: read(p) for p in (H / 'evaluation-packets').glob('*.json')}
    checks = c.projection_barrier(planned, packets)
    for uid in planned:
        c.require(packets[uid] == build_packet('evaluation', uid),
                  'PROVENANCE_PROJECTION_FAILURE: resolved packet differs')
        c.require(packet_path('evaluation', uid, 'txt').read_bytes() == prompt('evaluation', packets[uid]),
                  'PROVENANCE_PROJECTION_FAILURE: rendered request differs')
    p2 = c.p2_preflight(discoveries()['R3K08-C1'])
    return {'projection_checks': checks, 'all_exact_match': True, 'planned_obligations': len(planned),
            'p2_preflight': p2, 'reference_order_semantically_irrelevant': True}


def verify_projection_barrier():
    require_freeze('projection')
    c.require(read(H / 'projection-manifests' / 'complete.json') == barrier_result(),
              'PROVENANCE_PROJECTION_FAILURE: complete barrier changed')


def jobs():
    a, b, corpus = assignments(), discoveries(), claims()
    sets = {uid:value['claim_obligation_set'] for uid,value in b.items()}
    c.dependency_order(sets, a)  # reject cycles before evaluation packets/launches
    result = {}
    seen_subjects = set()
    normalize = lambda text: ' '.join(re.findall(r'\w+',text.casefold()))
    for uid in manifest()['claim_order']:
        if uid not in b:
            continue
        for job in c.obligation_jobs(corpus[uid][0], a[uid], b[uid]):
            if job['kind'] == 'INLINE':
                existing = [x for x in corpus[uid][1]['claims'] if x['claim_id'] != uid]
                c.require(not any(normalize(x['value']) == normalize(job['subject']) for x in existing),
                          'DEPENDENCY_DUPLICATION: existing frozen proposition must use CLAIM_REF')
            subject_key = (corpus[uid][1]['case_id'],normalize(job['subject']),job['contract'])
            c.require(subject_key not in seen_subjects, 'DEPENDENCY_DUPLICATION: repeated subject/contract')
            seen_subjects.add(subject_key)
            key = uid+'--'+job['obligation_id']
            c.require(key not in result, 'Duplicate scientific obligation')
            result[key] = job
    return result


def ids(stage):
    if stage == 'classification':
        return manifest()['claim_order']
    if stage == 'dependency':
        return [uid for uid,a in assignments().items() if c.eligible(a)]
    return list(jobs())


def verify(commit=True):
    m=manifest()
    c.require(git('branch','--show-current')==m['branch'],'Wrong branch')
    c.require(git('merge-base',m['base_sha'],'HEAD')==m['base_sha'],'Wrong ancestry')
    c.require(git('rev-parse',m['base_sha']+':distance/natural-admission-v0.1')==
              m['h6_tree']==git('rev-parse',m['h6_terminal_sha']+':distance/natural-admission-v0.1'),
              'Historical H.6 tree mismatch')
    allowed=('distance/compound-obligation-calibration-v0.2/',
             'docs/PROBLEM_FRAMES-compound-obligation-calibration-v0.2.md',
             'distance/review/compound-obligation-calibration-v0.2.md')
    for line in git('diff','--name-status','--no-renames',m['base_sha'],'--').splitlines():
        status,path=line.split('\t',1)
        c.require(status=='A' and path.startswith(allowed),'Outside additive H6.R3 scope: '+path)
    corpus=claims()
    c.require(len(m['case_order'])==len(set(m['case_order']))==12 and
              len(corpus)==len(m['claim_order'])==len(set(m['claim_order']))==13 and
              set(corpus)==set(m['claim_order']),'Corpus count/identity changed')
    for p in sorted(H.glob('*-freeze.json'))+sorted(H.glob('*-prepared.json')):
        if commit: committed(p)
        hashes(read(p)['files'],commit)
    for historical in ('distance/compound-obligation-calibration-v0.1', 'distance/claim-role-taxonomy-v0.1', 'distance/natural-admission-v0.1'):
        c.require(not git('diff', m['base_sha'], '--', historical), 'Historical evidence changed')
    return {'base_sha':m['base_sha'],'branch':m['branch'],'cases':12,'claims':13,
            'historical_files_unchanged':True}


def scheduling_clear():
    state=latest_state()
    c.require(not state or state['state'] in ('BATCH_COMPLETE','PAUSED_BUDGET'),
              'Preserved event/incomplete/terminal state blocks dispatch; no automatic recovery')
    for batch in (RT/'batches').glob('*'):
        c.require((batch/'calibration-record.json').exists(),'Complete bookkeeping before more work')


def prompt(stage, packet):
    preamble=(H/(stage.upper()+'-PROMPT.md')).read_text()
    t=taxonomy()
    details=({'origins':t['origins'],'functions':t['functions']} if stage=='classification'
             else {'verdict_meanings':t['verdicts']} if stage=='evaluation'
             else {k:t[k] for k in ('origins','functions')})
    if stage=='dependency':
        preamble+='\n'+(H/'DEPENDENCIES.md').read_text()
    return (preamble+'\n'+json.dumps(details,indent=2)+'\nFROZEN PACKET\n'+
            json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode()


def build_packet(stage, uid):
    corpus=claims()
    if stage=='evaluation':
        job=jobs()[uid]; claim,case=corpus[job['claim_id']]
        return c.evaluation_packet(claim,case,job,taxonomy())
    claim,case=corpus[uid]
    if stage=='classification':
        return c.classification_packet(claim,case)
    a=assignments()
    return c.obligation_packet(claim,case,a[uid],a)


def prepare(stage):
    verify();binary_check()
    p=H/(stage+'-prepared.json')
    c.require(not p.exists(),'Packets already prepared')
    try:
        selected = ids(stage)
    except ValueError as exc:
        code = next((code for code in ('DEPENDENCY_CYCLE','DEPENDENCY_DUPLICATION') if code in str(exc)),None)
        if code:
            write(H/'review'/('blocked-'+stage+'-preparation.json'),{'at':now(),'code':code,'detail':str(exc),'provider_launches':0})
        raise
    for uid in selected:
        packet=build_packet(stage,uid)
        write(packet_path(stage,uid),packet)
        raw(packet_path(stage,uid,'txt'),prompt(stage,packet))
    if stage == 'evaluation':
        barrier = barrier_result()
        write(H / 'projection-manifests' / 'complete.json', barrier)
        # Regressions must pass on the same frozen harness before measurement.
        subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(H / 'tests')], check=True)
        write(frozen_path('projection'), {'parent_commit': head(), 'files': inventory([
            H / 'projection-manifests' / 'complete.json', *list((H / 'evaluation-packets').glob('*'))])})
    dependencies=list((H/(stage+'-packets')).glob('*'))
    dependencies += [H/n for n in ('runner.py','contracts.py','audit.py','execution-config.json',
        'CLASSIFICATION-PROMPT.md','DEPENDENCY-PROMPT.md','EVALUATION-PROMPT.md',
        'schema-freeze.json','selection-freeze.json')]
    dependencies += list((H/'tests').glob('test_*.py'))
    dependencies += [H/'review-guidance.md']
    dependencies += list((H/'schemas').glob('*.json'))
    dependencies += [R/'scripts'/n for n in ('experiment_budget.py','codex_usage.py')]
    dependencies += [frozen_path(s) for s in STAGES[:STAGES.index(stage)]]
    if stage == 'evaluation':
        dependencies += [frozen_path('projection'), frozen_path('obligation-sets')]
    write(p,{'parent_commit':head(),'stage':stage,'claim_ids':ids(stage),'files':inventory(dependencies)})


def financial_plan():
    counts={'classification':13,'dependency':len(ids('dependency')) if frozen_path('classification').exists() else 13,
            'evaluation':len(ids('evaluation')) if frozen_path('obligation-sets').exists() else None}
    return {'version':1,'experiment_id':manifest()['experiment_id'],
      'description':'H6.R3: 12 controls / 13 claim records; classification, discovery, isolated obligation evaluation; no retries.',
      'execution_fingerprint':budget.digest({n:sha(H/n) if (H/n).exists() else None for n in
       ('schema-freeze.json','selection-freeze.json',*[s+'-prepared.json' for s in STAGES])}),
      'execution_allowed':True,'stages':[{'id':s,'sessions':counts[s], 'estimated_cost_usd':None,
       'estimate_basis':'Unknown: new H6.R3 task profiles lack matched billing. Historical H.6 cash-reload proxy is not a price for this study.',
       'usage_profile':'astra-high-h6r3-'+s+'-frozen-context-v2'} for s in STAGES]}


def check_plan():
    p=plan_file();committed(p);plan=read(p);expected=financial_plan()
    c.require(plan['execution_fingerprint']==expected['execution_fingerprint'],'Stale execution fingerprint')
    c.require(plan['experiment_id']==expected['experiment_id'],'Experiment identity changed')
    c.require([(s['id'],s['sessions'],s['usage_profile']) for s in plan['stages']]==
              [(s['id'],s['sessions'],s['usage_profile']) for s in expected['stages']],
              'Cumulative plan omits expected sessions/profiles')
    return plan


def remaining_plan(plan):
    result=json.loads(json.dumps(plan))
    for stage in result['stages']:
        done=len(list((RT/'attempts'/stage['id']).glob('*/reservation.json')))
        if stage['sessions'] is not None:
            stage['sessions']=max(0,stage['sessions']-done)
    result['description']='Usage-only remaining work; never replaces cumulative financial forecast.'
    return result


def aggregate():
    require_freeze('evaluation');verify()
    evaluations={(v['claim_id'],v['obligation_id']):v for v in
                 [read(judgment('evaluation',uid)) for uid in ids('evaluation')]}
    result=c.aggregate(assignments(),discoveries(),evaluations,taxonomy())
    write(H/'aggregation/results.json',result)
    write(H/'aggregation-freeze.json',{'parent_commit':head(),
        'files':inventory([H/'aggregation/results.json'])})


def metrics():
    verify();require_freeze('classification');require_freeze('dependency');require_freeze('evaluation')
    p=H/'aggregation-freeze.json';committed(p);hashes(read(p)['files'],True)
    import audit
    a,b=assignments(),discoveries()
    ev=[read(judgment('evaluation',uid)) for uid in ids('evaluation')]
    vals=read(H/'aggregation/results.json')
    diagnostics=[]
    for s in STAGES:
        for uid in ids(s):
            diagnostics.extend(c.validate(s,read(judgment(s,uid)),read(packet_path(s,uid)),
                               read(H/'schemas'/(s+'.schema.json')),taxonomy()))
    hypotheses=read(H/'hidden-hypotheses/controls.json')
    review_path=H/'review/dependency-audit.json'
    if not review_path.exists():
        write(H/'review/dependency-audit-template.json',audit.operator_template(hypotheses))
        print('Complete semantic dependency audit before metrics; observations remain unchanged.')
        return
    result=audit.report(a,b,ev,vals,hypotheses,diagnostics,read(review_path))
    write(H/'metrics.json',result)


def seal_audit():
    verify()
    p=H/'review/operator-audit.json';value=read(p)
    c.require(value['status']=='COMPLETE','Operator audit incomplete')
    c.require(value['metrics_sha256']==sha(H/'metrics.json'),'Audit metrics mismatch')
    c.require(len(value['research_answers'])==14 and all(x.strip() for x in value['research_answers']),
              'All fourteen research questions require answers')
    c.require(value['recommendation_executed'] is False,'Recommendation execution forbidden')
    write(H/'audit-freeze.json',{'parent_commit':head(),
        'files':inventory([p,H/'review/dependency-audit.json',H/'metrics.json',H/'aggregation-freeze.json'])})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='action',required=True)
    sub.add_parser('verify')
    for action in ('prepare','freeze'):
        sub.add_parser(action).add_argument('stage',choices=STAGES)
    sub.add_parser('write-plan').add_argument('--out',type=Path,required=True)
    p=sub.add_parser('forecast');p.add_argument('--out',type=Path,required=True)
    p.add_argument('--scope',required=True);p.add_argument('--calibration',type=Path,required=True)
    p=sub.add_parser('run');p.add_argument('stage',choices=STAGES)
    p.add_argument('--preflight',type=Path,required=True);p.add_argument('--count',type=int,default=3)
    p.add_argument('--usage-review',type=Path)
    p=sub.add_parser('record-batch');p.add_argument('--batch',type=Path,required=True)
    p.add_argument('--isolated-account-work',action='store_true');p.add_argument('--telemetry-settled',action='store_true');p.add_argument('--reference',required=True)
    for action in ('aggregate','metrics','seal-audit','resolve-dependencies'):sub.add_parser(action)
    args=parser.parse_args()
    if args.action=='verify':print(json.dumps(verify(),indent=2))
    elif args.action in ('prepare','freeze'):globals()[args.action](args.stage)
    elif args.action=='write-plan':verify();write(args.out,financial_plan())
    elif args.action=='forecast':return forecast(args.out,args.scope,args.calibration)
    elif args.action=='run':run_batch(args.stage,args.preflight,args.count,args.usage_review)
    elif args.action=='record-batch':record_batch(args.batch,args.isolated_account_work,args.telemetry_settled,args.reference)
    elif args.action=='resolve-dependencies':resolve_dependencies()
    elif args.action=='aggregate':aggregate()
    elif args.action=='metrics':metrics()
    elif args.action=='seal-audit':seal_audit()
    return 0


if __name__=='__main__':
    try:sys.exit(main())
    except Exception as exc:
        print(type(exc).__name__+': '+str(exc),file=sys.stderr);sys.exit(2)
