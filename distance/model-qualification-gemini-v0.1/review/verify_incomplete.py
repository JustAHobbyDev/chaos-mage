#!/usr/bin/env python3
"""Read-only partial-run audit; historical semantic decoding stays forbidden."""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('gemini_partial_verify', HERE/'runner.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


def verify():
    r.verify(); frozen = r.read(HERE/'partial-freeze.json'); r.committed(HERE/'partial-freeze.json')
    r.verify_inventory(frozen['evidence'])
    for p in frozen['evidence']: r.committed(r.ROOT/p)
    r.require(not frozen['complete'] and frozen['runs'] == [], 'Primary results invented')
    r.require(frozen['prepared_sha256'] == r.sha(HERE/'prepared.json'), 'Preparation mismatch')
    for name in ('results-freeze.json','preflight/freeze.json','preflight/anti-collapse','review/preliminary.json'):
        r.require(not (HERE/name).exists(), 'Execution or comparison continued after stop')
    r.require(not list((HERE/'judgments').rglob('*')), 'Unexpected primary artifacts')
    sent = list((HERE/'preflight').glob('*/request-sent.json'))
    r.require(len(sent) == 1, 'Expected one attempted artificial probe')
    d = sent[0].parent; reservation = r.read(d/'reservation.json')
    r.require(reservation['case_id'] is None and reservation['fresh_process'] and reservation['working_directory_initially_empty'], 'Isolation failure')
    r.require(reservation['input_commit'] == r.checkpoint(HERE/'prepared.json'), 'Probe preparation mismatch')
    body = r.read(d/'request.json')
    prompt = 'Return exactly this artificial formatting fixture; no classification, tools or external context.\n' + json.dumps(r.fixture('validity'))
    r.require(body == r.gemini.request_body(prompt,r.read(r.wire('validity')),r.config()['providers']['gemini']), 'Actual request drift')
    raw = r.read(d/'http-body.json'); text, metadata = r.gemini.parse_response(raw,reservation['session_id'])
    r.validate(json.loads(text),'validity'); r.require(json.loads(text) == r.fixture('validity'), 'Artificial output mismatch')
    r.require(r.read(d/'validation.json')['error'] == 'ValueError: Unexpected billing service tier', 'Original failure changed')
    r.require(raw['usageMetadata']['serviceTier'] == 'standard', 'Incident mismatch')
    try: r.cost.account(raw['usageMetadata'], r.pricing())
    except ValueError as exc: r.require(str(exc) == 'Unexpected billing service tier','Different accounting defect')
    else: raise ValueError('Frozen accountant repaired after stop')
    m = r.read(HERE/'metrics.json'); cost = r.read(HERE/'review/cost-summary.json'); audit = r.read(HERE/'review/execution-audit.json')
    r.require(m['qualification'] == 'qualification_inconclusive','Unsupported qualification')
    r.require(m['attempted_judgments'] == m['successful_judgments'] == 0 and m['planned_primary_judgments'] == 12,'Wrong workload')
    r.require(m['provider_failures'] == m['schema_failures'] == 0 and m['harness_failures'] == 1,'Failure attribution mismatch')
    r.require((cost['input_tokens'],cost['output_tokens'],cost['thinking_tokens']) == (154,112,652),'Usage mismatch')
    r.require(cost['estimated_experiment_usd'] == '0.009476','Cost mismatch')
    for k in ('validity','anti_collapse','anti_collapse_gate'):
        r.require(all(v is None for v in m[k].values()),'Unmeasured distribution invented')
    for k in ('model_failure_cases','ontology_specification_ambiguity_cases','legitimate_reasoning_variation_cases','historical_status_comparison'):
        r.require(m[k] is None,'Semantic findings invented')
    r.require(not audit['historical_decoding_performed'] and not audit['semantic_comparisons_performed'],'Premature review')
    r.require(all(v == 0 for v in audit['primary_calls'].values()) and audit['experiment_f_calls'] == 0,'Unauthorized call')
    reviews = r.read(HERE/'review/case-reviews.json')
    r.require(reviews['cases'] == [] and len(reviews['unmeasured_cases']) == 12,'Review evidence mismatch')
    r.require({v['qualification_id'] for v in reviews['unmeasured_cases']} == {c['qualification_id'] for c in r.cases()},'Missing case')
    r.require(all(v['assessment'] is None for v in reviews['unmeasured_cases']),'Unmeasured assessment invented')
    base = r.config()['starting_sha']
    r.require(r.git('show',base+':docs/MODEL-POLICY.md') == (r.ROOT/'docs/MODEL-POLICY.md').read_bytes(),'Policy changed without qualification')
    r.require(r.read(r.RUNTIME/'STOP.json') == frozen['stop'],'Stop changed')
    for obj in (m,cost,audit,reviews): r.require(obj['partial_freeze_commit'] == r.checkpoint(HERE/'partial-freeze.json'),'Freeze binding mismatch')
    return {'passed':True,'primary_calls':0,'artificial_probes':1,'provider_calls_in_audit':0,
            'qualification':'qualification_inconclusive','historical_artifacts_unchanged':True}


if __name__ == '__main__': print(json.dumps(verify(),indent=2))
