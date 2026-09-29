"""Read-only terminal verification; never schedules providers or repairs results."""
import argparse
from collections import Counter
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('completed_recovery', HERE / 'runner.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
e = r.e


def verify(private=False):
    result = e.verify_results(private)
    e.require(result['status'] != 'incomplete', 'Recovery stopped before completion')
    subprocess.run([sys.executable, '-B', str(r.ORIGINAL / 'review/verify_incomplete.py'), *(['--private'] if private else [])], cwd=e.ROOT, check=True, stdout=subprocess.PIPE)
    r.execution_authorized()
    auth = e.read(HERE / 'execution-authorization.json')
    auth_commit = e.checkpoint(HERE / 'execution-authorization.json')
    admission = e.read(HERE / 'admission.json')
    metrics = e.read(HERE / 'metrics.json')
    data = {stage: e.published(stage) for stage in ('generation', 'neutralization', 'audit', 'validity')}
    rows = {v['case_id']: v for v in e.manifest()}
    generated = {cid for cid, _ in data['generation']}
    neutralized = {cid for cid, _ in data['neutralization']}
    e.require(len(generated) == 30, 'Generation cohort changed')
    e.require(Counter(v['generator_family'] for v in rows.values()) == {'A': 15, 'B': 15}, 'Generator allocation changed')
    e.require(set(data['validity']) == {(cid, f) for cid in generated for f in 'AB'}, 'Validity coverage differs from generation cohort')
    e.require(set(data['audit']) == {(cid, f) for cid in neutralized for f in 'AB'}, 'Audit coverage differs from neutralized cohort')
    vv = {cid for cid in generated if all(data['validity'][(cid, f)]['validity']['final_status'] == 'Valid' and not data['validity'][(cid, f)]['validity']['unresolved_conditions'] for f in 'AB')}
    faithful = {cid for cid in neutralized if all(data['audit'][(cid, f)]['overall'] == 'pass' for f in 'AB')}
    admitted = vv & faithful
    e.require(admitted == {v['case_id'] for v in admission['cases'] if v['admitted']}, 'Independent admission mismatch')
    expected_counts = {'generated_mappings': len(generated), 'generation_failures': 30 - len(generated), 'neutralization_successes': len(neutralized), 'neutralization_failures': len(generated - neutralized), 'neutralization_audit_exclusions': len(neutralized - faithful), 'validity_admitted_mappings': len(vv), 'validity_excluded_mappings': len(generated - vv), 'primary_admitted_mappings': len(admitted)}
    for key, expected in expected_counts.items():
        e.require(metrics[key] == expected, 'Independent count mismatch: ' + key)
    viable = len(admitted) >= 18 and len({rows[cid]['target_id'] for cid in admitted}) >= 5
    e.require(admission['viability']['viable'] == viable, 'Independent coverage mismatch')
    terminal = HERE / ('anti-collapse-freeze.json' if viable else 'admission.json')
    if viable:
        values = e.published('anti-collapse')
        e.require(set(values) == {(cid, f) for cid in admitted for f in 'AB'}, 'Anti-collapse cohort mismatch')
        statuses = {f: {s: sum(values[(cid, f)]['anti_collapse']['status'] == s for cid in admitted) for s in e.c.STATUSES} for f in 'AB'}
        e.require(metrics['status_distributions'] == statuses, 'Independent status distribution mismatch')
        comparisons = {'status_agreement': lambda v: v['status'], 'keep_reject_agreement': lambda v: v['status'] != 'CLEAR_COLLAPSE', 'materiality_agreement': lambda v: v['materiality']['status'], 'native_reduction_agreement': lambda v: v['native_reduction']['collapses_without_loss'], 'formalization_agreement': lambda v: v['formalization']['merely_makes_native_reasoning_explicit']}
        for key, get in comparisons.items():
            n = sum(get(values[(cid, 'A')]['anti_collapse']) == get(values[(cid, 'B')]['anti_collapse']) for cid in admitted)
            e.require(metrics[key] == {'numerator': n, 'denominator': len(admitted), 'fraction': n / len(admitted)}, 'Independent agreement mismatch: ' + key)
        for locus in e.c.LOCI:
            n = sum(values[(cid, 'A')]['anti_collapse']['departures'][locus]['status'] == values[(cid, 'B')]['anti_collapse']['departures'][locus]['status'] for cid in admitted)
            e.require(metrics['departure_locus_agreement'][locus]['numerator'] == n, 'Locus agreement mismatch')
    else:
        for path in (HERE / 'anti-collapse-freeze.json', HERE / 'probes/anti-collapse.json', HERE / 'stage-inputs/anti-collapse.json', HERE / 'packets/anti-collapse', e.RUNTIME / 'anti-collapse', e.RUNTIME / 'probes/anti-collapse'):
            e.require(not path.exists(), 'Anti-collapse measured below the admission minimum')
        e.require(metrics['measurement_status'] == 'insufficient natural-output coverage', 'Insufficient cohort presented as measured')
    e.committed(terminal)
    sessions = []
    returned = {f: set() for f in 'AB'}
    retries = {f: 0 for f in 'AB'}
    calls = []
    for stage in ('generation', 'neutralization', 'audit'):
        calls.extend((stage, v, False) for v in r.imports(stage))
        calls.extend((stage, v, False) for v in e.read(r.ORIGINAL / 'probes' / (stage + '.json'))['entries'])
    recovery_count = 0
    for stage in r.STAGES:
        path = HERE / (stage + '-freeze.json')
        if not path.exists():
            continue
        frozen = e.read(path)
        calls.extend((stage, v, True) for v in frozen['runs'] if 'recovery_import' not in v)
        calls.extend((stage, v, True) for v in e.read(HERE / 'probes' / (stage + '.json'))['entries'])
    for stage, entry, recovered in calls:
        metadata = entry['validation']['metadata']
        reservation = entry['reservation']
        family = entry['family']
        sessions.append(metadata['session_id'])
        returned[family].update(metadata['returned_model_identifiers'])
        retries[family] += metadata['formatting_retries']['observed_formatting_retries']
        e.require(reservation['working_directory_initially_empty'], 'Working directory not isolated')
        e.require(reservation['cli_version'] == e.config()['expected_cli_versions'][family], 'CLI version changed')
        if recovered:
            recovery_count += 1
            e.require(datetime.fromisoformat(reservation['started_at']) > datetime.fromisoformat(auth['recorded_at']), 'Recovery precedes authorization')
            e.require(e.git('merge-base', auth_commit, reservation['input_commit']).decode().strip() == auth_commit, 'Execution authorization not an ancestor')
            e.require(reservation['command'] == r.build_command(family, reservation['working_directory'], (e.ROOT / next(name for name in entry['files'] if name.endswith('/response.json'))).parent, reservation['requested_session'], stage), 'Recovery isolation command differs')
        if private:
            event_path = e.ROOT / next(name for name in entry['files'] if name.endswith('/events.jsonl'))
            events = [json.loads(line, object_pairs_hook=e.c.unique_object) for line in event_path.read_text().splitlines() if line.strip()]
            checked, payload = e.legacy.audit_events(events, family, reservation['configuration']['families'][family]['requested_model'], reservation['requested_session'] if family == 'B' else None)
            e.require(checked == metadata, 'Re-audited event metadata differs')
            response = e.ROOT / next(name for name in entry['files'] if name.endswith('/response.json'))
            if family == 'B':
                e.require(payload == e.read(response), 'Structured result differs from retained response')
            else:
                finals = [v['item']['text'] for v in events if v.get('type') == 'item.completed' and v.get('item', {}).get('type') == 'agent_message']
                e.require(len(finals) == 1 and finals[0].strip() == response.read_text().strip(), 'Stream/payload mismatch')
    e.require(len(sessions) == len(set(sessions)), 'Repeated provider session')
    e.require(not (e.RUNTIME / 'generation').exists(), 'Replacement generation detected')
    attrition = e.read(HERE / 'review/attrition.json')
    e.require({v['case_id'] for v in attrition['cases']} == generated and len(attrition['cases']) == len(generated), 'Attrition review coverage mismatch')
    for case in attrition['cases']:
        cid = case['case_id']
        e.require(case['admitted'] == (cid in admitted), 'Review admission mismatch')
        expected_labels = ([] if cid in vv else ['validity-excluded']) + ([] if cid in faithful else ['neutralization-excluded'])
        e.require(case['review_categories'] == expected_labels, 'Unexpected qualitative label')
        e.require(case['generator_family'] == rows[cid]['generator_family'] and case['neutralizer_family'] == rows[cid]['neutralizer_family'], 'Review family mismatch')
        for family in 'AB':
            v = data['validity'][(cid, family)]['validity']
            audit = data['audit'][(cid, family)]
            e.require(case['validity_status'][family] == v['final_status'] and case['validity_rationale'][family] == v['rationale'] and case['unresolved_conditions'][family] == v['unresolved_conditions'], 'Review validity evidence changed')
            e.require(case['audit_status'][family] == audit['overall'] and case['audit_nonpassing_checks'][family] == {k: v for k, v in audit['checks'].items() if v['status'] != 'pass'}, 'Review audit evidence changed')
    if not viable:
        absent = e.read(HERE / 'review/nonmeasurement.json')
        e.require(absent['anti_collapse_calls'] == 0 and all(v is None for v in absent['anti_collapse_metrics_and_findings'].values()), 'Unmeasured gate findings fabricated')
        e.require(absent['terminal_commit'] == e.checkpoint(terminal), 'Nonmeasurement binding mismatch')
        e.require(len(sessions) == 192 and recovery_count == 108, 'Published session count mismatch')
    report = e.ROOT / 'distance/review/anti-collapse-natural-recovery-v0.1.md'
    text = report.read_text()
    e.require('does **not answer**' in text and 'insufficient coverage' in text and 'No anti-collapse' in text, 'Report misses central limitation')
    for commit in re.findall(r'`([0-9a-f]{40})`', text):
        e.require(e.git('merge-base', commit, 'HEAD').decode().strip() == commit, 'Report checkpoint is not an ancestor')
    return {**result, **expected_counts, 'unique_sessions': len(sessions), 'original_sessions': len(sessions) - recovery_count, 'recovery_sessions': recovery_count, 'returned_identifiers': {f: sorted(returned[f]) for f in 'AB'}, 'observed_formatter_retries': retries, 'historical_artifacts_unchanged': True, 'private_event_audit': private}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.private), indent=2))
