"""H.3 publication from immutable observations and post-freeze operator review."""
import argparse
from collections import Counter
import json
import contracts as c
import runner as r
from common import guard
H,R=r.H,r.R
REPORT=R/'distance/review/negative-remainder-calibration-v0.1.md'

def checkpoint(path):return r.git('log','-1','--format=%H','--',r.rel(path)).decode().strip()
def distribution(values,keys):
    counts=Counter(values)
    return {k:counts[k] for k in keys}
def focus_text(design):
    text=design['focal_texts'][-1] if design['intended_role']=='INQUIRY_CONSTRAINT' else design['focal_texts'][0]
    if ', but ' in text:text=text[text.index(', but '):]
    return text

def compute():
    m=c.read(H/'manifest.json');review=c.read(H/'review/operator.json');audits={x['case_id']:x for x in review['case_reviews']}
    atoms=r.claims();claim_results={a['claim_id']:c.read(H/'judgments/claim-warrant'/f'{a["claim_id"]}.json') for a in atoms}
    rows=[];negatives=[];all_candidates=[]
    for cid in m['case_order']:
        d=c.read(H/'hidden-design'/f'{cid}.json');value=c.read(H/'judgments/artifact'/f'{cid}.json');a=value['remainder_viability']
        negative=value['negative_remainder_assessment']['candidates'];byid={x['remainder_id']:x for x in a['candidate_remainders']}
        annotated=[{**x,'case_id':cid,'inference':byid[x['remainder_id']]['inference'],'source_spans':byid[x['remainder_id']]['source_spans'],'origin':byid[x['remainder_id']]['origin']} for x in negative]
        negatives.extend(annotated);all_candidates.extend(a['candidate_remainders'])
        focus=focus_text(d);focal_ids=[x['remainder_id'] for x in a['candidate_remainders'] if x['origin']=='frozen' and x['inference']==focus]
        actual={x['claim_id'] for x in atoms if x['case_id']==cid and claim_results[x['claim_id']]['status']=='UNSUPPORTED'}
        intended={x['claim_id'] for x in atoms if x['case_id']==cid and x['source_field']=='mapping.inference'}
        rows.append({'case_id':cid,'mechanism_key':d['mechanism_key'],'is_control':d['is_control'],'control':d['control'],
            'intended_role':d['intended_role'],'focal_text':focus,'focal_candidate_ids':focal_ids,
            'focal_assessments':[x for x in annotated if x['remainder_id'] in focal_ids],
            'negative_assessments':annotated,'artifact_status':a['artifact_status'],'viable_remainders':a['viable_remainders'],
            'strongest_surviving_target_inference':a['strongest_surviving_target_inference'],
            'scope_survival':a['scope_survival']['status'],'deleted_claim_ids':sorted(actual),
            'intended_deletion_realized':actual==intended,'empty_deletion_set':not actual,
            'mapping_chars':sum(map(len,r.candidate(cid)['mapping'].values())),
            'deleted_chars':sum(len(x['exact_claim_span']) for x in atoms if x['claim_id'] in actual),
            'claim_count':sum(x['case_id']==cid for x in atoms),
            'candidate_count':len(a['candidate_remainders']),'judge_added_count':sum(x['origin']=='judge_added' for x in a['candidate_remainders']),
            'operator_category':audits[cid]['category'],'case_design_problem':audits[cid]['case_design_problem'],
            'judge_productivity_error':audits[cid]['judge_productivity_error']})
    freezes={s:c.read(H/f'{s}-freeze.json') for s in r.STAGES};runs=[x for f in freezes.values() for x in f['runs']]
    sessions=[x['validation']['metadata']['session_id'] for x in runs]
    checkpoints={k:v for k,v in m.items() if k.endswith('_checkpoint')}
    for key,path in {'claim_inventory':'claims/inventory.json','claim_preflight':'review/claim-warrant-preflight.json',
                     'claim_judgments':'claim-warrant-freeze.json','ablations_and_candidates':'artifact-manifest.json',
                     'artifact_preflight':'review/artifact-preflight.json','artifact_judgments':'artifact-freeze.json',
                     'operator_audit':'review/operator.json'}.items():checkpoints[key+'_checkpoint']=checkpoint(H/path)
    focal=[x for row in rows for x in row['focal_assessments']]
    return {'status':'COMPLETE','base_sha':m['base_sha'],'branch':m['branch'],'checkpoints':checkpoints,
        'completion_sha_resolution':'git log -1 --format=%H -- distance/negative-remainder-calibration-v0.1/publication-manifest.json',
        'primary_case_count':12,'control_count':3,'claim_judgment_count':len(atoms),'artifact_judgment_count':len(rows),
        'provider_calls':len(runs),'unique_sessions':len(set(sessions)),
        'claim_status_counts':distribution((x['status'] for x in claim_results.values()),c.CLAIM),
        'negative_role_counts':distribution((x['role'] for x in negatives),c.ROLES),
        'negative_productive_counts':distribution((x['productive'] for x in negatives),c.YESNO),
        'negative_candidate_count':len(negatives),'focal_role_counts':distribution((x['role'] for x in focal),c.ROLES),
        'focal_productive_counts':distribution((x['productive'] for x in focal),c.YESNO),
        'focal_assessment_count':len(focal),'assessed_candidate_count':len(all_candidates),
        'viability_field_distributions':{d:distribution((x[d]['status'] for x in all_candidates),c.YESNO) for d in c.DIMENSIONS},
        'artifact_status_counts':distribution((x['artifact_status'] for x in rows),c.ARTIFACT),
        'empty_deletion_cases':[x['case_id'] for x in rows if x['empty_deletion_set']],
        'unrealized_manipulations':[x['case_id'] for x in rows if not x['intended_deletion_realized']],
        'operator_category_counts':dict(Counter(x['operator_category'] for x in rows)),
        'case_design_problems':sum(x['case_design_problem'] for x in rows),
        'judge_productivity_errors':sum(x['judge_productivity_error'] for x in rows),
        'operator_review_is_independent_rater_evidence':False,'historical_preservation':guard(),
        'cases':rows,'triplets':{k:[x['case_id'] for x in rows if x['mechanism_key']==k and not x['is_control']] for k in ['ach','crossdate','diagnosis','delta']},
        'provider_limitations':{'verified_served_snapshots':sorted({x['validation']['metadata']['verified_served_snapshot'] for x in runs},key=str),
            'harness_retries':0,'exposed_internal_retry_events':sum(len(x['validation']['metadata']['internal_retry_events']) for x in runs),
            'sampling':'One fresh Astra/high context per claim and artifact; no repeat sample or independent rater.'},
        'interpretation':review['interpretation'],'recommended_next_step':review['recommended_next_step']}

def escape(x):return str(x).replace('|','/').replace('\n',' ')
def render(m):
    review=c.read(H/'review/operator.json');byid={x['case_id']:x for x in m['cases']}
    lines=['# Experiment H.3 — Productive Negative Remainder Calibration v0.1','',review['interpretation']['summary'],'',
        '## Lineage and preservation','',f'Base: `{m["base_sha"]}`. Branch: `{m["branch"]}`. Push only this branch; no merge to main.',
        'The completion SHA is the commit containing publication-manifest.json, resolved by the command in metrics.json.','',
        '| Checkpoint | SHA |','|---|---|']
    lines += [f'| {k} | `{v}` |' for k,v in m['checkpoints'].items()]
    lines += ['',f'Historical preservation: {m["historical_preservation"]}. Both measurement stages passed 49 historical checks and the H.3 test suite. Historical observations and files remain unchanged.','',
        '## Productive-negative rule and construction','',
        '**A negative remainder is productive only when it changes justified target states, bounds, alternative priorities, a stopping decision, or a specific discriminating next inquiry already present in surviving mapping content.** Merely acknowledging failure to establish an answer does not by itself supply viable remainder value.',
        'Cannot conclude X does not mean X is excluded. Viability requires warranted, source-derived, target-relevant, productive, and material, assessed in that order. Graph centrality and ownership do not control status.',
        'Four matched triplets cover ACH, dendrochronological crossdating, differential diagnosis and delta debugging. Source instruments, target, focal identity, baseline procedure and conditions are fixed within triplets. Observation content varies to license the intended consequence. The three controls manipulate wording or jargon while preserving a concrete semantic contrast.',
        'Each focal consequence appears once. Authoring audits inspect all five mapping fields, removal effects, inquiry components, redundancy and other possible contributions. These are operator hypotheses, not independent truth. The inventory stage split coordinated delta root-cause assertions and the wording control into separate atomic claims; the earlier authoring audit counts refer to pre-extraction prose units.',
        'Inquiry members contain an extra assertion. Text size and claim-count differences are disclosed below; no padding or numeric parity threshold was used.','',
        '| Case | Mechanism | Intended role/control | Claims | Mapping chars | Deleted chars |','|---|---|---|---:|---:|---:|']
    for x in m['cases']:lines.append(f'| `{x["case_id"]}` | {x["mechanism_key"]} | {x["intended_role"]} / {x["control"] or "primary"} | {x["claim_count"]} | {x["mapping_chars"]} | {x["deleted_chars"]} |')
    lines += ['', '## Claim judgments and ablation','',f'{m["claim_judgment_count"]} claim judgments: {json.dumps(m["claim_status_counts"],sort_keys=True)}.',
        'All measured UNSUPPORTED spans were deleted simultaneously; conditional and uncertain claims remained. No subset search, semantic repair or replacement inference occurred. All 15 artifacts were measured under the user-selected empty-deletion policy.',
        f'Empty deletion cases: {m["empty_deletion_cases"]}. Unrealized intended deletions: {m["unrealized_manipulations"]}. These cases are excluded from ablation-effect conclusions.',
        'Candidate inventories were frozen after claim results and before artifact calls. They cover surviving claims and an explicit all-field search for additional consequences. Judge-added candidates require exact surviving citations.','',
        '## Negative remainder and artifact results','',
        f'All negative-candidate assessments ({m["negative_candidate_count"]}): {json.dumps(m["negative_role_counts"],sort_keys=True)}.',
        f'Productivity among those candidates: {json.dumps(m["negative_productive_counts"],sort_keys=True)}.',
        f'Focal assessments ({m["focal_assessment_count"]}, separate denominator): {json.dumps(m["focal_role_counts"],sort_keys=True)}; productivity {json.dumps(m["focal_productive_counts"],sort_keys=True)}.',
        f'Artifact statuses: {json.dumps(m["artifact_status_counts"],sort_keys=True)}.','',
        '| Mechanism | Intended target member | Intended inquiry member | Intended insufficiency member |','|---|---|---|---|']
    for key,ids in m['triplets'].items():
        cells=[]
        for role in c.ROLES[:3]:
            x=next(byid[cid] for cid in ids if byid[cid]['intended_role']==role)
            focal=', '.join(a['role']+'/'+a['productive'] for a in x['focal_assessments']) or 'No surviving focal assessment'
            cells.append(f'{x["case_id"]}: {focal}; {x["artifact_status"]}')
        lines.append('| '+key+' | '+' | '.join(cells)+' |')
    lines += ['', '### Adversarial controls','']
    for x in m['cases']:
        if x['is_control']:lines += [f'- **{x["control"]}** (`{x["case_id"]}`): '+', '.join(a['role']+'/'+a['productive'] for a in x['focal_assessments'])+f'; {x["artifact_status"]}.']
    for status in ['CORE_INVALID','UNCERTAIN_LOAD_BEARING']:
        lines += ['',f'### All {status}','']
        selected=[x for x in m['cases'] if x['artifact_status']==status]
        lines += [f'- `{x["case_id"]}` ({x["mechanism_key"]}, {x["intended_role"]}): {escape(x["strongest_surviving_target_inference"]["text"])}' for x in selected] or ['None.']
    lines += ['', '### Every assessed negative remainder','',
        '| Case / remainder | Role | Productive | Exact candidate | Counterfactual effects |','|---|---|---|---|---|']
    for x in m['cases']:
        for a in x['negative_assessments']:lines.append(f'| {x["case_id"]} / {a["remainder_id"]} | {a["role"]} | {a["productive"]} | {escape(a["inference"])} | {escape(json.dumps(a["counterfactual_effect"],sort_keys=True))} |')
    lines += ['', '### All inquiry constraints and discriminating next inquiries','']
    inquiry=[a for x in m['cases'] for a in x['negative_assessments'] if a['role']=='INQUIRY_CONSTRAINT']
    for a in inquiry:
        q=a['inquiry_specificity'];lines += [f'- `{a["case_id"]}/{a["remainder_id"]}`: **{q["concrete_operation"]}**. Contrast: {q["unresolved_contrast"]}. Outcomes: {q["differential_outcome_relation"]}. Surviving provenance present: {q["all_present_in_surviving_mapping"]}.']
    if not inquiry:lines.append('None.')
    lines += ['', '### All insufficiency-only remainders','']
    for x in m['cases']:
        for a in x['negative_assessments']:
            if a['role']=='INSUFFICIENCY_ONLY':lines.append(f'- `{x["case_id"]}/{a["remainder_id"]}`: {a["inference"]}')
    lines += ['', '## Post-freeze operator audit','',f'Categories: {json.dumps(m["operator_category_counts"],sort_keys=True)}. Case-design problems: {m["case_design_problems"]}; judge-productivity errors: {m["judge_productivity_errors"]}.',
        'The operator reviewed every case after all artifact judgments froze. This is not independent-rater evidence. Raw outputs and hidden hypotheses remain unchanged.','',
        '| Case | Category | Finding |','|---|---|---|']
    for a in review['case_reviews']:lines.append(f'| `{a["case_id"]}` | {a["category"]} | {escape(a["finding"])} |')
    lines += ['', '## Research questions','']
    for key,value in review['research_answers'].items():lines += [f'**{key}:** {value}','']
    lines += ['## Interpretation, limitations and next step','']
    for k,v in review['interpretation'].items():
        if k!='summary':lines += [f'**{k}:** {v}','']
    lines += ['- '+s for s in review['limitations']]
    lines += ['',f'Exactly {m["provider_calls"]} observations in {m["unique_sessions"]} distinct fresh sessions requested GPT-6 Astra/high. No harness retries or duplicate samples. Verified served snapshots: {m["provider_limitations"]["verified_served_snapshots"]}; unavailable identifiers were not invented. Exposed internal retry events: {m["provider_limitations"]["exposed_internal_retry_events"]}.',
        '', '**Recommended next step:** '+m['recommended_next_step'],'',
        'The recommendation was not executed. Work stopped after H.3; no Experiment E continuation, natural-output admission experiment, production integration, historical experiment changes or main merge occurred.','']
    return '\n'.join(lines)

def write():
    for stage in r.STAGES:r.verify_results(stage,True)
    r.committed(H/'review/operator.json');m=compute();r.write(H/'metrics.json',m)
    r.raw(REPORT,render(m).encode())
    for row in m['cases']:
        value=c.read(H/'judgments/artifact'/f'{row["case_id"]}.json')
        r.write(H/'viable-remainder-assessments'/f'{row["case_id"]}.json',c.projection(value['remainder_viability']))
    r.write(H/'final-runtime-freeze.json',{'status':'COMPLETE','files':r.inventory(r.RT.rglob('*'))})

def seal():
    paths=[p for p in H.rglob('*') if p.is_file() and p.name!='publication-manifest.json']+[REPORT,R/'docs/PROBLEM_FRAMES-negative-remainder-calibration-v0.1.md']
    r.write(H/'publication-manifest.json',{'status':'COMPLETE','files':r.inventory(paths),'checkpoint_before_completion':r.head()})

def verify():
    r.verify()
    for stage in r.STAGES:r.verify_results(stage,True)
    m=compute();c.require(c.read(H/'metrics.json')==m,'Metrics drift');c.require(REPORT.read_text()==render(m),'Report drift')
    c.require(m['provider_calls']==m['unique_sessions']==55,'Observation/session count')
    review=c.read(H/'review/operator.json');c.require(review['artifact_freeze_sha256']==c.sha(H/'artifact-freeze.json'),'Review binding')
    c.require({x['case_id'] for x in review['case_reviews']}==set(c.read(H/'manifest.json')['case_order']),'Review coverage')
    for x in review['case_reviews']:c.require(x['judgment_sha256']==c.sha(H/'judgments/artifact'/f'{x["case_id"]}.json'),'Reviewed output changed')
    for x in m['cases']:
        a=c.read(H/'judgments/artifact'/f'{x["case_id"]}.json')['remainder_viability']
        c.require(c.read(H/'viable-remainder-assessments'/f'{x["case_id"]}.json')==c.projection(a),'Projection drift')
    frozen=c.read(H/'final-runtime-freeze.json')['files'];r.hashes(frozen)
    c.require(r.inventory(r.RT.rglob('*'))==frozen,'Runtime changed after final freeze')
    for stage in r.STAGES:c.require(sorted(x.name for x in (r.RT/'runs'/stage).iterdir())==sorted(r.order(stage)),'Unexpected reservation')
    if (H/'publication-manifest.json').exists():r.hashes(c.read(H/'publication-manifest.json')['files'])
    return {k:m[k] for k in ['status','primary_case_count','control_count','claim_judgment_count','artifact_judgment_count','negative_role_counts','negative_productive_counts','artifact_status_counts','case_design_problems','judge_productivity_errors']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['write','seal','verify']);a=p.parse_args()
    result=globals()[a.action]()
    if result:print(json.dumps(result,indent=2))
