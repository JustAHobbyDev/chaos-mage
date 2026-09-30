#!/usr/bin/env python3
"""Read-only audit of the stopped bridge; never schedules or repairs provider calls."""
import argparse
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('incomplete_bridge', HERE / 'runner.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


def verify(private=False):
    r.verify()
    frozen = r.read(HERE / 'partial-freeze.json'); r.committed(HERE / 'partial-freeze.json')
    freeze_commit = r.checkpoint(HERE / 'partial-freeze.json')
    r.require(frozen['complete'] is False and frozen['runs'] == [], 'Unexpected primary evidence')
    r.require(frozen['prepared_sha256'] == r.sha(HERE / 'prepared.json'), 'Preparation mismatch')
    r.require(frozen['stop']['where'] == 'preflight/fable-validity', 'Unexpected stop')
    probes = r.read(HERE / 'preflight/partial.json'); r.committed(HERE / 'preflight/partial.json')
    r.require([(v['provider'], v['stage'], v['validation']['status']) for v in probes['entries']] == [
        ('muse', 'validity', 'valid'), ('muse', 'anti-collapse', 'valid'), ('fable', 'validity', 'failed')], 'Probe coverage changed')
    sessions = set()
    for entry in probes['entries']:
        reservation = entry['reservation']; provider = entry['provider']; stage = entry['stage']
        r.require(reservation['session_id'] not in sessions, 'Session reuse'); sessions.add(reservation['session_id'])
        r.require(reservation['case_id'] is None and reservation['working_directory_initially_empty'], 'Real case or context in preflight')
        r.require(reservation['configuration'] == r.config()['providers'][provider], 'Configuration changed')
        r.require(reservation['canonical_schema_sha256'] == r.sha(r.canonical(stage)), 'Schema changed')
        r.require(reservation['wire_schema_sha256'] == r.sha(r.wire(stage)), 'Wire schema changed')
        if provider == 'muse':
            r.validate(entry['response'], stage)
            r.require(entry['response'] == r.fixture(stage), 'Non-artificial probe')
            r.require(entry['validation']['metadata']['returned_model_identifiers'] == [r.muse.MODEL], 'Muse fallback')
        else:
            evidence = entry['failure_evidence']
            r.require(evidence['http_status'] == 401 and 'OAuth access token has expired' in evidence['provider_error'], 'Failure cause changed')
            r.require(not evidence['modelUsage'] and evidence['assistant_model_identifiers'] == ['<synthetic>'], 'Unexpected Fable inference')
            init = evidence['runner_init']
            r.require(not any(init.get(k) for k in ('mcp_servers','plugins','skills','slash_commands')), 'External context enabled')
            r.require(init['tools'] == ['StructuredOutput'], 'Unexpected Fable tools')
        if private:
            d = r.RUNTIME / 'preflight' / (provider + '-' + stage)
            r.verify_inventory(entry['files'])
            r.require(r.read(d / 'reservation.json') == reservation, 'Reservation mismatch')
            prompt = d.joinpath('prompt.txt').read_text()
            expected = 'Return exactly this artificial formatting fixture; no classification, tools or external context.\n' + json.dumps(r.fixture(stage))
            r.require(prompt == expected, 'Probe used real packet')
            if provider == 'muse':
                request = r.read(d / 'request.json')
                r.require(request == r.muse.request_body(prompt, r.read(r.wire(stage)), reservation['configuration']), 'Wire request differs')
                content, metadata = r.muse.parse_response(r.read(d / 'http-body.json'), reservation['session_id'])
                r.require(metadata == entry['validation']['metadata'] and json.loads(content) == entry['response'], 'Muse event mismatch')
            else:
                events = [json.loads(line) for line in (d / 'events.jsonl').read_text().splitlines() if line.strip()]
                result = next(e for e in events if e.get('type') == 'result')
                r.require(result['is_error'] and result['result'] == evidence['provider_error'], 'Fable error mismatch')
                assistant = [e for e in events if e.get('type') == 'assistant']
                r.require(len(assistant) == 1 and assistant[0]['error'] == 'authentication_failed', 'Unexpected assistant output')
                msg = assistant[0]['message']
                r.require(msg['model'] == '<synthetic>' and msg['usage']['input_tokens'] == msg['usage']['output_tokens'] == 0, 'Synthetic error misread as inference')
    if private:
        r.verify_inventory(frozen['all_runtime_files'])
        r.require(r.read(r.RUNTIME / 'STOP.json') == frozen['stop'], 'STOP changed')
        for name in ('judgments', 'measurement-reservation.json', 'preflight/fable-anti-collapse'):
            r.require(not (r.RUNTIME / name).exists(), 'Scheduling continued after failure')
    for name in ('results-freeze.json', 'preflight/freeze.json', 'review/case-reviews.json'):
        r.require(not (HERE / name).exists(), 'Incomplete evidence promoted to complete')
    r.require(not list((HERE / 'judgments').rglob('*.json')), 'Fresh results invented')
    metrics = r.read(HERE / 'metrics.json')
    r.require(metrics['transition_recommendation'] == 'inconclusive', 'Unsupported recommendation')
    r.require(metrics['primary_calls'] == {'fable': 0, 'muse': 0}, 'Call count incorrect')
    for stage in r.IDS:
        r.require(all(v is None for v in metrics[stage].values()), 'Unmeasured metric fabricated')
    r.require(all(v is None for pair in metrics['review_category_counts'].values() for v in pair.values()), 'Review counts fabricated')
    pending = r.read(HERE / 'review/unmeasured-cases.json')
    r.require(pending['results_freeze_commit'] is None and pending['partial_freeze_commit'] == freeze_commit, 'Unmeasured record claims complete freeze')
    r.require([x['bridge_id'] for x in pending['cases']] == [x['bridge_id'] for x in r.cases()], 'Missing pending case')
    for case in pending['cases']:
        r.require(all(case[k] is None for k in ('fresh_fable', 'fresh_muse', 'historical_vs_fresh_fable', 'fresh_fable_vs_muse', 'downstream_transition_effect')), 'Premature semantic review')
    historical = r.read(HERE / 'review/historical-fable-comparison.json')
    r.require(historical['evaluated_pairs'] == 0 and historical['state'] == 'not_performed', 'Historical substitute comparison')
    audit = r.read(HERE / 'review/execution-audit.json')
    r.require(audit['partial_freeze_commit'] == freeze_commit and audit['unique_preflight_sessions'] == len(sessions), 'Audit provenance mismatch')
    r.require(not audit['semantic_comparisons_performed'] and audit['third_judges'] == audit['experiment_f_calls'] == audit['harness_retries'] == 0, 'Out-of-scope execution')
    for obj in (pending, historical, audit):
        r.require(datetime.fromisoformat(obj['at']) > datetime.fromisoformat(frozen['at']), 'Report predates failure freeze')
    # Scan publication and transport artifacts for concrete credential syntax. Do not
    # echo matching content; this is defense in depth, not proof about unknown formats.
    patterns = (r'-----BEGIN .*PRIVATE KEY-----', r'Bearer\s+[A-Za-z0-9_.\-]{16,}', r'"(?:access_token|refresh_token|api_key)"\s*:\s*"[^"\s]+"')
    paths = list(HERE.rglob('*.json'))
    if private: paths += list(r.RUNTIME.rglob('*.json')) + list(r.RUNTIME.rglob('*.jsonl'))
    for path in paths:
        text = path.read_text()
        r.require(not any(re.search(pattern, text) for pattern in patterns), 'Possible credential in artifact')
    report = (r.ROOT / 'distance/review/family-b-bridge-v0.1.md').read_text()
    r.require('Recommendation: `inconclusive`' in report and 'zero fresh primary' in report, 'Report hides incomplete state')
    return {'status': 'inconclusive', 'source_cases': 12, 'primary_calls': {'fable': 0, 'muse': 0},
        'successful_muse_probes': 2, 'failed_fable_authentication_probes': 1, 'reviewed_pairs': 0,
        'historical_artifacts_unchanged': True, 'private_evidence_checked': private}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--private', action='store_true')
    print(json.dumps(verify(parser.parse_args().private), indent=2))
