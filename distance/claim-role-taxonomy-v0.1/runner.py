#!/usr/bin/env python3
"""H6.R1: offline preparation by default; explicit gated batches only."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile

import contracts as c

H = Path(__file__).resolve().parent
R = H.parents[1]
OLD = R / 'distance/natural-admission-v0.1'
RT = R / '.runtime/claim-role-taxonomy-v0.1'
sys.path.insert(0, str(R / 'scripts'))
import experiment_budget as budget
import codex_usage as usage

STAGES = ('role', 'evaluation')


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


def ids(stage):
    order = manifest()['claim_order']
    if stage == 'role':
        return order
    require_freeze('role')
    return [uid for uid in order if read(judgment('role', uid))['assignment_status'] == 'ASSIGNED'
            and read(judgment('role', uid))['atomicity'] == 'ATOMIC']


def verify(commit=True):
    m = manifest()
    c.require(git('branch', '--show-current') == m['branch'], 'Wrong branch')
    c.require(git('rev-parse', m['base_sha'] + ':distance/natural-admission-v0.1') ==
              m['h6_tree'] == git('rev-parse', m['h6_terminal_sha'] + ':distance/natural-admission-v0.1'),
              'H.6 base/terminal tree mismatch')
    # No base-tracked file may change. This checks working bytes and deletions too,
    # without reading historical labels into any packet or operator output.
    changes = git('diff', '--name-status', '--no-renames', m['base_sha'], '--')
    allowed = ('distance/claim-role-taxonomy-v0.1/',
               'docs/PROBLEM_FRAMES-claim-role-taxonomy-v0.1.md',
               'distance/review/claim-role-taxonomy-v0.1.md')
    for line in changes.splitlines():
        status, path = line.split('\t', 1)
        c.require(status == 'A' and path.startswith(allowed), 'Outside additive study scope: ' + path)
    hashes(m['input_hashes'])
    for p in sorted(H.glob('*-freeze.json')) + sorted(H.glob('*-prepared.json')):
        if commit:
            committed(p)
        hashes(read(p)['files'], commit)
    return {'base_sha': m['base_sha'], 'h6_terminal_sha': m['h6_terminal_sha'],
            'h6_unchanged': True, 'selected': len(m['claim_order'])}


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


def prompt(stage, packet):
    preamble = (H / ('ROLE-PROMPT.md' if stage == 'role' else 'EVALUATION-PROMPT.md')).read_text()
    details = ({'roles': taxonomy()['roles']} if stage == 'role' else
               {'verdict_meanings': taxonomy()['verdicts']})
    return (preamble + '\n' + json.dumps(details, indent=2) + '\nFROZEN PACKET\n' +
            json.dumps(packet, indent=2, ensure_ascii=False) + '\n').encode()


def build_packet(stage, uid):
    claim = read(H / 'selection/claims.json')[uid]
    evidence = read(H / 'selection/evidence.json')[uid]
    if stage == 'role':
        return c.role_packet(claim, evidence)
    require_freeze('role')
    return c.evaluation_packet(claim, evidence, read(judgment('role', uid)), taxonomy())


def prepare(stage):
    verify()
    binary_check()
    p = H / (stage + '-prepared.json')
    c.require(not p.exists(), 'Packets already prepared')
    for uid in ids(stage):
        packet = build_packet(stage, uid)
        write(packet_path(stage, uid), packet)
        raw(packet_path(stage, uid, 'txt'), prompt(stage, packet))
    dependencies = list((H / (stage + '-packets')).glob('*'))
    dependencies += [H / n for n in ('runner.py', 'contracts.py', 'execution-config.json',
                                    'ROLE-PROMPT.md', 'EVALUATION-PROMPT.md')]
    dependencies += list((H / 'tests').glob('test_*.py'))
    dependencies += list((H / 'schemas').glob('*-wire.schema.json'))
    dependencies += [H / 'schema-freeze.json', H / 'selection-freeze.json']
    if stage == 'evaluation':
        dependencies.append(frozen_path('role'))
    dependencies += [R / 'scripts' / n for n in ('experiment_budget.py', 'codex_usage.py')]
    write(p, {'parent_commit': head(), 'stage': stage, 'claim_ids': ids(stage),
              'files': inventory(dependencies)})


def financial_plan(stage_b=None):
    n = len(manifest()['claim_order'])
    fingerprint = budget.digest({'schema': sha(H / 'schema-freeze.json'),
                                 'selection': sha(H / 'selection-freeze.json'),
                                 'role_packets': sha(H / 'role-prepared.json'),
                                 'evaluation_packets': sha(H / 'evaluation-prepared.json')
                                 if (H / 'evaluation-prepared.json').exists() else None})
    return {'version': 1, 'experiment_id': manifest()['experiment_id'],
            'description': 'H6.R1: 24 frozen natural claims; A role assignment then B routed evaluation; no retries.',
            'execution_fingerprint': fingerprint, 'execution_allowed': True,
            'stages': [{'id': stage, 'sessions': count, 'estimated_cost_usd': None,
                        'estimate_basis': 'Unknown: new role/routed prompt profiles lack matched billing. '
                                          'docs/experiment-budget-calibration.json supplies only an H.6 cash-reload proxy.',
                        'usage_profile': 'astra-high-h6r1-' + stage + '-frozen-context-v1'}
                       for stage, count in [('role', n), ('evaluation', n if stage_b is None else stage_b)]]}


def plan_file():
    revisions = sorted((H / 'budgets').glob('plan-*.json'))
    c.require(revisions, 'Missing cumulative financial plan')
    return revisions[-1]


def check_plan():
    p = plan_file()
    committed(p)
    plan = read(p)
    expected = financial_plan(len(ids('evaluation')) if frozen_path('role').exists() else None)
    c.require(plan['execution_fingerprint'] == expected['execution_fingerprint'], 'Stale execution fingerprint')
    c.require([(s['id'], s['sessions'], s['usage_profile']) for s in plan['stages']] ==
              [(s['id'], s['sessions'], s['usage_profile']) for s in expected['stages']],
              'Plan omits expected cumulative sessions or changes profiles')
    c.require(plan['experiment_id'] == manifest()['experiment_id'], 'Experiment identity changed')
    return plan


def remaining_plan(plan):
    result = json.loads(json.dumps(plan))
    for stage in result['stages']:
        done = len(list((RT / 'attempts' / stage['id']).glob('*/reservation.json')))
        stage['sessions'] = max(0, stage['sessions'] - done)
    result['description'] = 'Usage-only remaining work; never replaces cumulative financial plan.'
    return result


def latest_state():
    paths = sorted((RT / 'states').glob('*.json'))
    return read(paths[-1]) if paths else None


def transition(state, detail):
    paths = sorted((RT / 'states').glob('*.json'))
    write(RT / 'states' / f'{len(paths):04}.json', {'at': now(), 'state': state, 'detail': detail,
          'execution_commit': head(), 'previous_sha256': sha(paths[-1]) if paths else None})


def scheduling_clear():
    state = latest_state()
    c.require(not state or state['state'] not in ('PAUSED_EVENT', 'PAUSED_INTEGRITY', 'RUNNING'),
              'Preserved event or incomplete batch blocks dispatch; no automatic resume')
    for batch in (RT / 'batches').glob('*'):
        c.require((batch / 'calibration-record.json').exists(), 'Complete batch bookkeeping before more work')


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
    c.require(uid in ids(stage), 'Claim is not eligible')
    c.require(not judgment(stage, uid).exists(), 'Judgment already exists')
    destination = RT / 'attempts' / stage / stem(uid)
    c.require(not destination.exists(), 'Attempt exists; no retry')
    packet = read(packet_path(stage, uid))
    c.require(packet == build_packet(stage, uid), 'Packet differs from frozen evidence construction')
    request = packet_path(stage, uid, 'txt').read_bytes()
    c.require(request == prompt(stage, packet), 'Prompt differs from frozen construction')
    session = stage + ':' + uid
    with tempfile.TemporaryDirectory(prefix='h6r1-isolated-') as cwd:
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
        destination = H / 'raw' / stage / stem(uid)
        for artifact in source.iterdir():
            if artifact.is_file():
                raw(destination / artifact.name, artifact.read_bytes())
    dependencies = list((H / (stage + '-judgments')).glob('*.json'))
    dependencies += list((H / 'raw' / stage).rglob('*'))
    write(frozen_path(stage), {'parent_commit': head(), 'stage': stage, 'claim_ids': expected,
          'excluded_claim_ids': [uid for uid in manifest()['claim_order'] if uid not in expected],
          'files': inventory(dependencies)})


def compare():
    verify()
    require_freeze('role')
    require_freeze('evaluation')
    rows = []
    for uid in manifest()['claim_order']:
        old_path = OLD / 'claim-judgments' / (stem(uid) + '.json')
        old = read(old_path) if old_path.exists() else None
        a = read(judgment('role', uid))
        b = read(judgment('evaluation', uid)) if judgment('evaluation', uid).exists() else None
        rows.append({'claim_id': uid, 'mandatory_anchor': uid in manifest()['mandatory_anchor_ids'],
                     'old_h6_status': old['status'] if old else None,
                     'old_h6_rationale': old['rationale'] if old else None,
                     'old_h6_sha256': sha(old_path) if old else None,
                     'assignment_status': a['assignment_status'], 'new_frozen_role': a['primary_role'],
                     'new_contract': b['contract_id'] if b else None,
                     'new_verdict': b['verdict'] if b else None})
    # Attribution is a separate operator audit, never inferred from a changed label.
    write(H / 'comparison/historical.json', {'after_stage_b_commit': head(), 'claims': rows,
          'contract_mismatch_attribution': 'Requires evidence-backed operator audit; no automatic rescue.'})


def seal_review(kind):
    verify()
    require_freeze('role')
    require_freeze('evaluation')
    if kind == 'comparison':
        c.require((H / 'comparison/historical.json').exists(), 'Historical comparison missing')
        paths = list((H / 'comparison').glob('*'))
    else:
        require_freeze('comparison')
        audit = read(H / 'review/operator-audit.json')
        c.require(len(audit['research_questions']) == 12 and all(
            x.get('answer') and x.get('evidence') for x in audit['research_questions']),
            'All twelve research questions require evidence-backed answers')
        c.require(set(audit['anchor_assessments']) == set(manifest()['mandatory_anchor_ids']),
                  'Every anchor requires an audit assessment')
        c.require(audit['recommendation_executed'] is False, 'Follow-on work is out of scope')
        paths = [H / 'metrics.json', H / 'review/operator-audit.json',
                 R / 'distance/review/claim-role-taxonomy-v0.1.md']
        c.require(all(p.exists() for p in paths), 'Final artifacts incomplete')
    write(frozen_path(kind), {'parent_commit': head(), 'stage': kind, 'files': inventory(paths)})


def metrics():
    require_freeze('role')
    require_freeze('evaluation')
    hypotheses = read(H / 'hidden-hypotheses/operator.json')
    assignments = [read(judgment('role', uid)) for uid in manifest()['claim_order']]
    evaluations = [read(judgment('evaluation', uid)) for uid in ids('evaluation')]
    paired = [a for a in assignments if a['primary_role'] is not None and
              hypotheses[a['claim_id']]['intended_role'] is not None]
    concordant = sum(a['primary_role'] == hypotheses[a['claim_id']]['intended_role'] for a in paired)
    by_role = {role: {verdict: sum(b['verdict'] == verdict and b['frozen_role'] == role for b in evaluations)
                     for verdict in taxonomy()['verdicts']}
               for role in taxonomy()['roles']}
    return {'selected_count': len(assignments),
            'role_counts': {role: sum(a['primary_role'] == role for a in assignments)
                            for role in taxonomy()['roles']},
            'assignment_counts': {status: sum(a['assignment_status'] == status for a in assignments)
                                  for status in ('ASSIGNED', 'ROLE_UNCERTAIN', 'ATOMIZATION_DEFECT')},
            'atomicity_concordance': {'numerator': sum(a['atomicity'] == hypotheses[a['claim_id']]
                ['intended_atomicity'] for a in assignments), 'denominator': len(assignments)},
            'role_concordance': {'numerator': concordant, 'paired_denominator': len(paired),
                                'all_selected_denominator': len(assignments)},
            'verdicts_by_role': by_role,
            'verdicts_by_contract': {taxonomy()['routing'][role]: counts for role, counts in by_role.items()},
            'strict_derived_rejection_observed': any(b['frozen_role'] == 'DERIVED_INFERENCE' and
                b['verdict'] == 'VIOLATED' for b in evaluations),
            'interpretation': 'No repeatability estimate or H.6-wide prevalence inference.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('verify')
    for action in ('prepare', 'freeze'):
        sub.add_parser(action).add_argument('stage', choices=STAGES)
    sub.add_parser('write-plan').add_argument('--out', type=Path, required=True)
    p = sub.add_parser('forecast')
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--scope', required=True)
    p.add_argument('--calibration', type=Path, required=True)
    p = sub.add_parser('run')
    p.add_argument('stage', choices=STAGES)
    p.add_argument('--preflight', type=Path, required=True)
    p.add_argument('--count', type=int, default=3)
    p.add_argument('--usage-review', type=Path)
    p = sub.add_parser('record-batch')
    p.add_argument('--batch', type=Path, required=True)
    p.add_argument('--isolated-account-work', action='store_true')
    p.add_argument('--telemetry-settled', action='store_true')
    p.add_argument('--reference', required=True)
    sub.add_parser('compare')
    sub.add_parser('metrics')
    sub.add_parser('seal-review').add_argument('kind', choices=('comparison', 'audit'))
    args = parser.parse_args()
    if args.action == 'verify':
        print(json.dumps(verify(), indent=2))
    elif args.action in ('prepare', 'freeze'):
        globals()[args.action](args.stage)
    elif args.action == 'write-plan':
        verify()
        write(args.out, financial_plan(len(ids('evaluation')) if frozen_path('role').exists() else None))
    elif args.action == 'forecast':
        return forecast(args.out, args.scope, args.calibration)
    elif args.action == 'run':
        run_batch(args.stage, args.preflight, args.count, args.usage_review)
    elif args.action == 'record-batch':
        record_batch(args.batch, args.isolated_account_work, args.telemetry_settled, args.reference)
    elif args.action == 'compare':
        compare()
    elif args.action == 'metrics':
        write(H / 'metrics.json', metrics())
    elif args.action == 'seal-review':
        seal_review(args.kind)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(type(exc).__name__ + ': ' + str(exc), file=sys.stderr)
        sys.exit(2)
