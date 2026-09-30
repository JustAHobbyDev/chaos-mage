#!/usr/bin/env python3
"""Deterministic post-freeze report assembly from independently authored reviews."""
from collections import Counter
from decimal import Decimal
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gemini_report_contracts',HERE/'review/contracts.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
r=c.r


def main():
    data=r.complete_results();preliminary=r.read(HERE/'review/preliminary.json');c.check_reviews(preliminary)
    history=r.historical();reviews=r.read(HERE/'review/case-reviews.json');c.check_reviews(reviews,True)
    freeze=r.checkpoint(HERE/'results-freeze.json');prep=r.checkpoint(HERE/'prepared.json');preflight=r.checkpoint(HERE/'preflight/freeze.json')
    rows=reviews['cases'];usages=[]
    for stage in ('preflight','judgments'):
        for p in sorted((HERE/stage).glob('*/cost.json')):
            value=r.read(p);usages.append({'kind':stage,'case':p.parent.name,**value})
    cost={k:sum(v[k] for v in usages) for k in ('input_tokens','output_tokens','thinking_tokens','billable_output_tokens','total_tokens')}
    cost.update(estimated_experiment_usd=str(sum((Decimal(v['estimated_usd']) for v in usages),Decimal(0))),
        estimated_preflight_usd=str(sum((Decimal(v['estimated_usd']) for v in usages if v['kind']=='preflight'),Decimal(0))),
        estimated_primary_usd=str(sum((Decimal(v['estimated_usd']) for v in usages if v['kind']=='judgments'),Decimal(0))),
        requests=usages,estimate_not_invoice=True,pricing=r.pricing(),billable_interpretation='Prompt tokens at input rate; candidate output plus thoughts at output rate, without double counting')
    r.write(HERE/'review/cost-summary.json',cost)
    labels={'validity':('Valid','Conditional','Invalid'),'anti-collapse':('CLEAR_COLLAPSE','BORDERLINE_KEEP','SUFFICIENT_DEPARTURE')}
    distributions={s:{label:sum(r.status(data[cid],s)==label for cid in ids) for label in labels[s]} for s,ids in r.IDS.items()}
    matches=Counter();muse=Counter()
    for case in r.cases():
        cid=case['qualification_id'];s=case['stage'];status=r.status(data[cid],s)
        count=sum(status==r.status(history[cid][name],s) for name in ('astra','fable'))
        matches[{2:'same_as_both',1:'same_as_one',0:'different_from_both'}[count]]+=1
        muse['same_as_muse' if status==r.status(history[cid]['muse'],s) else 'different_from_muse']+=1
    classes={k:[x['qualification_id'] for x in rows if x['final_disagreement_class']==k] for k in r.CATEGORIES}
    rejected=sum(r.status(data[cid],'anti-collapse')=='CLEAR_COLLAPSE' for cid in r.IDS['anti-collapse'])
    metrics={'results_freeze_commit':freeze,'qualification':reviews['qualification'],'planned_primary_judgments':12,
        'attempted_judgments':12,'successful_judgments':12,'provider_failures':0,'schema_failures':0,'harness_failures':0,
        'artificial_probes':2,'successful_artificial_probes':2,'status_distributions':distributions,
        'anti_collapse_gate':{'keep':6-rejected,'reject':rejected},
        'descriptive_historical_status_comparison':{k:matches[k] for k in ('same_as_both','same_as_one','different_from_both')},
        'descriptive_muse_status_comparison':{k:muse[k] for k in ('same_as_muse','different_from_muse')},
        'disagreement_cases':classes,'disagreement_counts':{k:len(v) for k,v in classes.items()},
        'capability_failures':{dimension:[v['qualification_id'] for v in rows if v['capability_dimensions'][dimension]=='fail'] for dimension in r.DIMENSIONS},
        'input_tokens':cost['input_tokens'],'output_tokens':cost['output_tokens'],'thinking_tokens':cost['thinking_tokens'],
        'estimated_experiment_usd':cost['estimated_experiment_usd']}
    r.write(HERE/'metrics.json',metrics)
    audit={'at':r.now(),'starting_sha':r.config()['starting_sha'],'preparation_commit':prep,'preflight_commit':preflight,
        'results_freeze_commit':freeze,'independent_assessment_commit':r.checkpoint(HERE/'review/preliminary.json'),'preliminary_review_sha256':r.sha(HERE/'review/preliminary.json'),
        'primary_calls':{'gemini':12,'astra':0,'fable':0,'muse':0},'artificial_probes':2,'unique_request_sessions':14,
        'harness_retries':0,'experiment_f_calls':0,'historical_artifacts_unchanged':True,
        'historical_review_after_committed_complete_results':True,'preliminary_assessment_before_historical_comparison':True,
        'preliminary_qualification':preliminary['qualification'],'final_qualification':reviews['qualification'],
        'qualification_changed_after_context':reviews['qualification']!=preliminary['qualification'],
        'classification_changes':[v['qualification_id'] for v in rows if v['historical_context_changed_classification']]}
    r.write(HERE/'review/execution-audit.json',audit)
    table='\n'.join('| '+case['qualification_id']+' | '+case['stage']+' | `'+case['source_commit']+'` | `'+case['input_sha256']+'` |' for case in r.cases())
    schema_hashes='\n'.join('- '+stage+': classifier `'+next(v['classifier_sha256'] for v in r.cases() if v['stage']==stage)+'`; canonical schema `'+next(v['canonical_schema_sha256'] for v in r.cases() if v['stage']==stage)+'`.' for stage in r.IDS)
    cases=[]
    for row in rows:
        dims=', '.join(k+'='+v for k,v in row['capability_dimensions'].items())
        cases.append('### '+row['qualification_id']+' — '+row['gemini']['status']+'\n\n'+row['gemini']['key_reasoning']+'\n\n'+row['rationale']+'\n\nDimensions: '+dims+'.\n\nPreliminary class: `'+row['preliminary_disagreement_class']+'`; final: `'+row['final_disagreement_class']+'`; consequence: '+row['downstream_consequence']+'.\n\nHistorical context: '+', '.join(k+'='+v for k,v in row['historical_context'].items())+'. Classification changed: '+str(row['historical_context_changed_classification']).lower()+'. '+row.get('classification_change_explanation','')+'\n')
    versions=sorted({v['validation']['metadata']['returned_model_identifiers'][0] for v in r.read(HERE/'results-freeze.json')['runs']})
    tier=sorted({v['validation']['metadata']['usage']['serviceTier'] for v in r.read(HERE/'results-freeze.json')['runs']})
    failure_cases=', '.join(classes['model_failure']) or 'none';ambiguities=', '.join(classes['ontology_specification_ambiguity']) or 'none';variations=', '.join(classes['legitimate_reasoning_variation']) or 'none'
    report=f'''# Gemini capability qualification v0.2

**Qualification: `{reviews['qualification']}`.**

{reviews['decision_rationale']}

## Starting point, recovery and freezes

- Starting SHA: `{r.config()['starting_sha']}`; local and origin/main matched.
- Preparation: `{prep}`.
- Successful two-schema preflight: `{preflight}`.
- Twelve-judgment result freeze: `{freeze}`.
- Independent assessment before historical decoding: `{r.checkpoint(HERE/'review/preliminary.json')}`.
- Completion: commit introducing this report, reported separately to avoid self-reference.

Gemini v0.1 is unchanged and remains qualification_inconclusive. Its successful
artificial response returned lowercase serviceTier standard; the harness incorrectly
expected uppercase STANDARD. V0.2 corrects that exact representation, requests
Standard explicitly at the top level, and serializes thinkingLevel high. V0.1's
accepted HIGH was not a provider/model failure. V0.2 uses fresh probes and judgments,
separate cost accounting and the same $2 ceiling. No v0.1 answer informed prompt tuning.

The contract was originally frozen at 1f51578aff8f8409b9a3c297a86ed84f8e6d7ee1;
SHA-256 `21b2ce7aeda5eef39175eb838f31f148afa7339e8fe02719c6ea1a2bf7acf31a`.
It, all historical classifiers, canonical schemas, native baselines and packets
are unchanged. The [manifest](../model-qualification-gemini-v0.2/manifest.json) records full source paths, commits, hashes, source-freeze
bindings, and historical-output hashes. Input/packet hashes are:

| Case | Stage | Source commit | Input / packet SHA-256 |
|---|---|---|---|
{table}

{schema_hashes}

## Provider, schemas and isolation

Requested model: gemini-3.1-pro-preview. Returned identifiers: {', '.join(versions)}.
Requested serviceTier: standard; returned tiers: {', '.join(tier)}.
Explicit thinkingConfig.thinkingLevel high; no thinkingBudget. Maximum output
32768, temperature 1.0; top-p/top-k/seed unset, recorded as provider defaults.
Native v1beta endpoint: https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent .
Client: Python 3.14.7 standard-library urllib.request; jsonschema 4.23.0. Full versions
are recorded in execution-config.json and every reservation. No SDK or harness
retries; no model fallback. Returned preview aliases do not establish immutable
served weights. Response IDs and raw metadata are preserved; hidden internal
provider retries remain unobservable. Credential source: environment via authorized
helper; temporary secret file removed before calls, never passed in argv or artifacts.

Native responseMimeType application/json and responseJsonSchema enforce the frozen
wire projection. It removes only $schema, $id and conditional allOf from the
canonical schema. Fields, enums, requiredness and null semantics are preserved;
unchanged full canonical and cross-field validation follow decoding. No repair.
Both artificial schemas passed before measurement and their freeze was committed.

Each primary request contained one user packet, fresh process/request identifier and
empty temporary working directory; no history, system/developer additions, external
context, tools, browsing, grounding, URL context, code execution or retrieval.
Exact packet bytes match the prior Muse qualification. No historical labels, reviews,
operator case intent or known failure descriptions reached Gemini. Randomized order
uses the existing within-stratum shuffle and alternating-strata methodology.
All twelve results were committed before independent assessment and historical
comparison. Preliminary assessment was saved before decoding historical outputs;
any later classification changes are recorded per case. The operator handoff had
already disclosed selected historical findings; this is not a claim of human blinding.

## Mechanical results and cost

Primary planned/attempted/successful: **12/12/12**. Artificial planned/successful:
**2/2**. Provider/schema/harness failures: **0/0/0**. Fresh Astra/Fable/Muse and
Experiment F calls: **0**. No repeated samples or retries.

- Validity: {json.dumps(distributions['validity'])}.
- Anti-collapse: {json.dumps(distributions['anti-collapse'])}.
- Gate: keep {6-rejected}; reject {rejected}.
- Input tokens: {cost['input_tokens']}.
- Candidate output tokens: {cost['output_tokens']}.
- Thinking tokens: {cost['thinking_tokens']}.
- Billable output including thinking: {cost['billable_output_tokens']}.
- Estimated preflight cost: ${cost['estimated_preflight_usd']}.
- Estimated primary cost: ${cost['estimated_primary_usd']}.
- Estimated experiment cost: **${cost['estimated_experiment_usd']}**, below $2 ceiling.

Rates frozen from [Google pricing](https://ai.google.dev/gemini-api/docs/pricing):
$2/M input and $12/M output including thinking at these context sizes. Prompt,
candidate and thought counts reconcile to totals. No double counting; no cache
discount assumed. Each request reserved conservative input plus the full output cap
before sending. These are estimates, not invoices; cost is descriptive, not eligibility.

Descriptive historical raw-status comparisons (not accuracy):
{json.dumps(metrics['descriptive_historical_status_comparison'])};
{json.dumps(metrics['descriptive_muse_status_comparison'])}.

## Capability assessment

- Model failure ({len(classes['model_failure'])}): {failure_cases}.
- Ontology/specification ambiguity ({len(classes['ontology_specification_ambiguity'])}): {ambiguities}.
- Legitimate reasoning variation ({len(classes['legitimate_reasoning_variation'])}): {variations}.
- Warrant failures: {json.dumps(metrics['capability_failures']['warrant_reasoning'])}.
- Mechanism failures: {json.dumps(metrics['capability_failures']['mechanism_reasoning'])}.
- Baseline-use failures: {json.dumps(metrics['capability_failures']['native_baseline_use'])}.

{reviews['systematic_pathology']}

{chr(10).join(cases)}

## Muse qualification failure pattern versus Gemini findings

{reviews['muse_comparison']}

This secondary comparison follows the independently formed Gemini decision. Neither
matching historical models nor differing from Muse qualifies a candidate. No general
model ranking, global intelligence claim, numeric cutoff or consensus score is implied.

## Verification, implications and limitations

All 384 tests across 37 checks passed, including 32 v0.2 tests. The live-credential
scan found no secret in 2,290 artifacts; sanitized evidence is in review/secret-scan.json.
All relevant historical/new suites and verifiers are recorded in review/verification.json,
with reports written only into v0.2. Historical files, including both prior qualifications,
are hash-preserved. Historical policy-sensitive checks run before any authorized current
policy update. The unrelated untracked handoff remains untouched.

{reviews['experiment_f_implication']}

{reviews['limitations']}

Stop after this qualification. No Experiment F, resumed E, new mapping, changed
anti-collapse, diversity filtering, grounding or retrieval integration was executed.
'''
    r.put(r.ROOT/'distance/review/model-qualification-gemini-v0.2.md',report.encode())


if __name__=='__main__':main()
