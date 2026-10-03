"""Offline recovery evidence and fail-closed scheduling; never launches providers."""
import json
import sqlite3
import subprocess

BASE = 'ad63e68d3bb22702eb6f8dd83aff97387de68b67'
AFFECTED = 'H7-T01-2'
AUTHORITY = 'User H7 continuation handoff, 2026-10-03: freeze no-observation policy, adjudicate preserved timeout, prove independence, continue only unaffected frozen lineages.'


def classify(e):
    # Known returned scientific observations cannot acquire no-observation semantics.
    if e.get('response_present') is True or e.get('scientific_observation_present') is True or e.get('completion_event_present') is True:
        return 'PROVIDER_OBSERVATION_FAILURE'
    positives = ('request_launched', 'launch_identity_certain', 'request_match',
                 'configuration_match', 'context_intact', 'unique_attempt')
    negatives = ('response_present', 'scientific_observation_present',
                 'completion_event_present', 'substitution')
    if (all(e.get(k) is True for k in positives) and
            all(e.get(k) is False for k in negatives) and e.get('retry_count') == 0 and
            e.get('frozen_request_sha256') and
            e.get('frozen_request_sha256') == e.get('executed_request_sha256')):
        return 'PROVIDER_NO_OBSERVATION'
    return 'PROVIDER_OBSERVATION_AMBIGUOUS'


def disposition(e):
    if classify(e) != 'PROVIDER_NO_OBSERVATION':
        raise ValueError('No-observation evidence incomplete')
    return {'instrumentation': 'FAILURE', 'admission': 'UNMEASURED',
            'end_to_end_complete': False, 'attempt_consumed': True,
            'retry': 'FORBIDDEN', 'replacement': 'FORBIDDEN'}


def schedulable(cid, fixed, quarantined, independence, attempted=False):
    return (cid in fixed and cid not in quarantined and not attempted and
            independence.get(cid, {}).get('independent') is True)


def ledger(r):
    with sqlite3.connect(f'file:{r.budget.DEFAULT_LEDGER}?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        return [dict(x) for x in db.execute('SELECT * FROM reservations WHERE experiment=?',
                                           ('h7-natural-admission-v0.2',))]


def inspect_attempt(r, stage, cid):
    d = r.RT / 'attempts' / stage / cid
    a = r.read(d / 'attempt.json')
    events = [json.loads(x) for x in (d / 'events.jsonl').read_text().splitlines() if x.strip()]
    starts = [e['thread_id'] for e in events if e.get('type') == 'thread.started']
    all_starts = []
    for p in (r.RT / 'attempts').glob('*/*/events.jsonl'):
        all_starts += [e['thread_id'] for e in map(json.loads, p.read_text().splitlines()) if e.get('type') == 'thread.started']
    rows = [x for x in ledger(r) if x['session'] == stage + '/' + cid]
    expected_cmd = r.command(a['command'][a['command'].index('--cd')+1], d, stage)
    frozen = r.sha(r.H / 'packets' / stage / (cid + '.txt'))
    executed = r.sha(d / 'request.txt')
    # Only these two events give an unambiguous empty stream in this adapter.
    # Any other partial/error/item event is unknown until positively adjudicated.
    clean_empty = [e.get('type') for e in events] == ['thread.started', 'turn.started']
    response_present = (d / 'response.json').exists()
    completed = any(e.get('type') == 'turn.completed' for e in events)
    observation = True if completed or response_present else False if clean_empty else None
    e = {'mapping_id': cid, 'stage': stage, 'attempt_id': stage + '/' + cid,
         'session_id': starts[0] if len(starts) == 1 else None,
         'request_launched': (d / 'process.json').exists() and clean_empty,
         'launch_identity_certain': len(starts) == 1 and (d / 'process.json').exists(),
         'frozen_request_sha256': frozen, 'executed_request_sha256': executed,
         'request_match': frozen == executed == a['request_sha256'],
         'configuration_match': a['configuration'] == r.config() and a['command'] == expected_cmd and a['schema_sha256'] == r.sha(r.H / 'schemas' / (stage + '.schema.json')),
         'context_intact': a['initially_empty'] is True and a['allowed_mapping_packets'] == [cid] and a['collision_exposure'] == 0,
         'unique_attempt': len(starts) == 1 and all_starts.count(starts[0]) == 1 and len(rows) == 1 and json.loads(rows[0]['command_json']) == a['command'] and a['harness_attempt'] == 1,
         'response_present': response_present, 'scientific_observation_present': observation,
         'completion_event_present': completed, 'retry_count': 0 if a['harness_attempt'] == 1 and len(rows) == 1 else None,
         'substitution': False if clean_empty and a['configuration'] == r.config() else None,
         'provider_internals': 'Unavailable; no provider-internal retry or served snapshot assertion.'}
    e['classification'] = classify(e)
    if e['classification'] == 'PROVIDER_NO_OBSERVATION':
        e['attempt_consumed'] = True
        e['mapping_disposition'] = disposition(e)
    return e


def baseline_review(r):
    """Reconstruct frozen dependencies and reconcile all twenty original attempts."""
    r.require(r.head() == BASE or r.git('merge-base', BASE, 'HEAD') == BASE, 'Wrong ancestry')
    baseline_files = r.git('ls-tree', '-r', '--name-only', BASE, str(r.H.relative_to(r.R))).splitlines()
    immutable = [p for p in baseline_files if any('/' + x + '/' in p for x in
        ('raw', 'packets', 'generation', 'claims', 'classification', 'discovery', 'span-tables', 'targets', 'pairings', 'prompts', 'schemas')) or p.endswith('-freeze.json') or p.endswith('/execution-config.json')]
    for name in immutable:
        old = subprocess.check_output(['git', 'show', BASE + ':' + name], cwd=r.R)
        r.require((r.R / name).read_bytes() == old, 'Baseline changed: ' + name)
    attempts = list((r.RT / 'attempts').glob('*/*/attempt.json'))
    rows = ledger(r)
    r.require(len(attempts) == len(rows) == 20, 'Unexpected scheduler attempts/reservations')
    sessions, evidence = [], {}
    pause_at = r.read(r.H / 'review/discovery-pause-state.json')['at']
    for p in attempts:
        a = r.read(p); stage, cid = a['stage'], a['packet_id']
        r.require(a['at'] < pause_at, 'Post-timeout launch')
        ds = p.parent
        for q in ds.iterdir():
            r.require((r.H / 'raw' / stage / cid / q.name).read_bytes() == q.read_bytes(), 'Runtime/raw mismatch')
        events = [json.loads(x) for x in (ds / 'events.jsonl').read_text().splitlines() if x.strip()]
        ids = [e['thread_id'] for e in events if e.get('type') == 'thread.started']
        r.require(len(ids) == 1, 'Session identity ambiguous'); sessions += ids
        cmd = a['command']; cwd = cmd[cmd.index('--cd')+1]
        historical_config = json.loads(subprocess.check_output(['git', 'show', a['execution_commit'] + ':' + str((r.H / 'execution-config.json').relative_to(r.R))], cwd=r.R))
        r.require(a['configuration'] == historical_config, 'Execution-time configuration mismatch')
        scientific_keys = set(r.config()) - {'allowed_stages', 'measurements'}
        r.require(cmd == r.command(cwd, ds, stage) and all(a['configuration'][k] == r.config()[k] for k in scientific_keys), 'Scientific configuration mismatch')
        r.require(a['initially_empty'] and a['allowed_mapping_packets'] == [cid] and a['collision_exposure'] == 0 and a['harness_attempt'] == 1, 'Context isolation mismatch')
        row = [x for x in rows if x['session'] == stage + '/' + cid]
        r.require(len(row) == 1 and json.loads(row[0]['command_json']) == cmd and row[0]['state'] == 'FINISHED', 'Ledger mismatch')
        r.require(r.sha(ds / 'request.txt') == r.sha(r.H / 'packets' / stage / (cid+'.txt')) == a['request_sha256'], 'Executed packet mismatch')
        evidence.setdefault(cid, []).append({'stage': stage, 'session_id': ids[0], 'request_sha256': a['request_sha256'], 'execution_commit': a['execution_commit']})
    r.require(len(set(sessions)) == 20, 'Duplicate session')
    verdict = {}
    for cid in r.order():
        if cid == AFFECTED: continue
        pkt = r.read(r.H / 'packets/discovery' / (cid+'.json'))
        expected = (r.H / 'prompts/discovery.md').read_text() + '\nFROZEN PACKET\n' + json.dumps(pkt, indent=2) + '\n'
        r.require((r.H / 'packets/discovery' / (cid+'.txt')).read_text() == expected, 'Packet envelope changed')
        r.require(pkt['packet_id'] == cid and pkt['claims'] == r.read(r.H / 'claims' / (cid+'.json')) and pkt['classifications'] == r.read(r.H / 'classification' / (cid+'.json')), 'Cross-mapping dependency')
        r.require(pkt['mapping'] == r.read(r.H / 'generation' / (cid+'.json'))['instrument'], 'Generation dependency mismatch')
        # Frozen before timeout, byte-identical to baseline, and no incident payload in packet.
        r.require(AFFECTED not in expected and '01a1039a-6ea9-7683-ba43-19337b2ca114' not in expected and 'TimeoutExpired' not in expected, 'Incident contamination')
        subset = [r.R / p for p in immutable if cid in p]
        verdict[cid] = {'independent': True, 'evidence': evidence[cid], 'frozen_identity': r.inventory(subset),
            'input_isolation': 'Pre-timeout frozen packet, exact envelope and own generation/claims/classification; no failed output exists. Dependency builders read only mapping-local records plus frozen shared source/target/schema/prompt.',
            'configuration_isolation': 'Exact original command and frozen configuration; fresh empty directory, ephemeral exec, no resume/fork/tools/history.',
            'scheduler_integrity': '20 unique finished reservations reconcile 20 attempts and 20 unique sessions; no post-timeout launch; four remaining discoveries absent.'}
    e = inspect_attempt(r, 'discovery', AFFECTED)
    r.require(e['classification'] == 'PROVIDER_NO_OBSERVATION', 'Ambiguous timeout; continuation forbidden')
    e['independence_review'] = {'status': 'VERIFIED'}
    return {'baseline': BASE, 'authority': AUTHORITY, 'provider_no_observation': e,
        'continuation_independence': {'affected_mapping': AFFECTED, 'unaffected': verdict, 'overall': 'CONTINUATION_ALLOWED'},
        'baseline_files_checked': len(immutable), 'attempts': 20, 'unique_sessions': 20,
        'immutable_files': r.inventory([r.R / p for p in immutable]),
        'resume_order': ['H7-T02-1', 'H7-T02-2', 'H7-T03-1', 'H7-T03-2']}


def verify_evidence(r):
    e = r.read(r.H / 'review/continuation-evidence.json')
    r.require(e['baseline'] == BASE and e['authority'] == AUTHORITY, 'Continuation authority mismatch')
    for name, digest in e['immutable_files'].items():
        r.require(r.sha(r.R / name) == digest, 'Continuation evidence drift: ' + name)
    current = inspect_attempt(r, 'discovery', AFFECTED)
    r.require(current['classification'] == 'PROVIDER_NO_OBSERVATION', 'Timeout evidence no longer established')
    return e


def quarantined(r):
    result = {AFFECTED}
    for p in (r.H / 'review/quarantines').glob('*.json'):
        result.add(r.read(p)['mapping_id'])
    return result


def guard(r, cid, stage):
    e = verify_evidence(r)
    r.require(schedulable(cid, r.order(), quarantined(r), e['continuation_independence']['unaffected'],
                         (r.RT / 'attempts' / stage / cid).exists()), 'Consumed, quarantined, replacement or unverified mapping')


def resume(r):
    r.verify()
    r.require(not r.git('status', '--porcelain'), 'Unclean continuation checkpoint')
    r.require(r.state() == 'PAUSED_AMBIGUOUS', 'Unexpected pause state')
    e = verify_evidence(r)
    r.require(baseline_review(r) == e, 'Continuation review changed')
    r.transition('COMPLETE', 'Authorized resume-ready batch boundary; original pause preserved. Evidence: review/continuation-evidence.json; next discovery H7-T02-1; H7-T01-2 permanently quarantined. Not run completion.')
    p = sorted((r.RT / 'states').glob('*.json'))[-1]
    r.raw(r.H / 'review/continuation-resume-state.json', p.read_bytes())
