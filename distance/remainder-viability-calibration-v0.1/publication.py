"""Postmeasurement publication. Raw provider judgments are read-only inputs."""
import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import contracts as c
import runner as r
from common import guard

H,R=r.H,r.R
REPORT=R/'distance/review/remainder-viability-calibration-v0.1.md'

def checkpoint(path):
    return r.git('log','-1','--format=%H','--',r.rel(path)).decode().strip()

def compute():
    manifest=c.read(H/'manifest.json');order=manifest['case_order']
    review=c.read(H/'review/operator.json');audits={x['case_id']:x for x in review['case_reviews']}
    atoms=r.claims();claims={a['claim_id']:c.read(H/'judgments/claim-warrant'/f'{a["claim_id"]}.json') for a in atoms}
    rows=[];all_candidates=[]
    for cid in order:
        a=c.read(H/'judgments/artifact'/f'{cid}.json')['remainder_viability']
        d=c.read(H/'hidden-design'/f'{cid}.json');frozen=c.read(H/'remainder-candidates'/f'{cid}.json')
        deleted=[x for x in atoms if x['case_id']==cid and claims[x['claim_id']]['status']=='UNSUPPORTED']
        case=r.candidate(cid);size=sum(len(x['exact_claim_span']) for x in deleted)
        all_candidates.extend(a['candidate_remainders'])
        rows.append({'case_id':cid,'mechanism_key':d['mechanism_key'],'is_control':d['is_control'],
            'pair_role':d.get('pair_role'),'control':d.get('control'),'hidden_hypothesis':d['hypothesis'],
            'artifact_status':a['artifact_status'],'reason':a['no_viable_remainder_reason'],
            'scope_survival':a['scope_survival']['status'],
            **{key:a[key]['status'] for key in ['mechanism_survival','remainder_check','target_contribution_survival','dependency_cascade']},
            'central_bridge':a['central_bridge'],'strongest_surviving_target_inference':a['strongest_surviving_target_inference'],
            'viable_remainders':a['viable_remainders'],'candidate_count':len(a['candidate_remainders']),
            'frozen_candidate_count':len(frozen['candidates']),
            'judge_added_count':sum(x['origin']=='judge_added' for x in a['candidate_remainders']),
            'decisively_unresolved_count':sum(c.unresolved(x) for x in a['candidate_remainders']),
            'deleted_claim_ids':[x['claim_id'] for x in deleted],'deleted_chars':size,
            'mapping_chars':len('\n'.join(case['mapping'].values())),
            'deleted_fraction':size/len('\n'.join(case['mapping'].values())),
            'operator_category':audits[cid]['category'],'case_design_problem':audits[cid]['case_design_problem'],
            'judge_remainder_error':audits[cid]['judge_remainder_error']})
    byid={x['case_id']:x for x in rows};pairs=[]
    for pair in c.read(H/'hidden-design/pairs.json'):
        a,b=[byid[cid] for cid in pair['case_ids']]
        lengths=[a['deleted_chars'],b['deleted_chars']]
        pairs.append({'mechanism_key':pair['mechanism_key'],'reduced':a['case_id'],'core':b['case_id'],
            'reduced_status':a['artifact_status'],'core_status':b['artifact_status'],
            'measured_deleted_chars':lengths,'measured_max_min_ratio':max(lengths)/min(lengths) if min(lengths) else None,
            'viable_vs_nonviable_separated':bool(a['viable_remainders']) and b['artifact_status']=='CORE_INVALID',
            'intended_reduced_core_labels_observed':a['artifact_status']=='KEEP_WITH_REDUCED_SCOPE' and b['artifact_status']=='CORE_INVALID'})
    freezes={stage:c.read(H/f'{stage}-freeze.json') for stage in r.STAGES}
    sessions=[x['validation']['metadata']['session_id'] for f in freezes.values() for x in f['runs']]
    checkpoints={**{k:v for k,v in manifest.items() if k.endswith('_checkpoint')},
        'claim_inventory_checkpoint':checkpoint(H/'claims/inventory.json'),
        'claim_preflight_checkpoint':checkpoint(H/'review/claim-warrant-preflight.json'),
        'host_launch_recovery_checkpoint':checkpoint(H/'recovery/premeasurement-launch.json'),
        'claim_freeze_checkpoint':checkpoint(H/'claim-warrant-freeze.json'),
        'candidate_freeze_checkpoint':checkpoint(H/'artifact-manifest.json'),
        'artifact_preflight_checkpoint':checkpoint(H/'review/artifact-preflight.json'),
        'artifact_freeze_checkpoint':checkpoint(H/'artifact-freeze.json'),
        'operator_review_checkpoint':checkpoint(H/'review/operator.json')}
    return {'status':'COMPLETE','base_sha':manifest['base_sha'],'branch':manifest['branch'],
        'checkpoints':checkpoints,'completion_sha_resolution':'git log -1 --format=%H -- distance/remainder-viability-calibration-v0.1/publication-manifest.json',
        'primary_pair_count':6,'primary_case_count':12,'control_count':4,
        'claim_judgment_count':len(claims),'artifact_judgment_count':len(rows),'provider_calls':len(sessions),
        'unique_sessions':len(set(sessions)),
        'claim_status_counts':{s:sum(x['status']==s for x in claims.values()) for s in c.CLAIM},
        'artifact_status_counts':{s:sum(x['artifact_status']==s for x in rows) for s in c.ARTIFACT},
        'no_viable_remainder_reason_counts':{s:sum(x['reason']==s for x in rows) for s in c.REASONS},
        'diagnostic_distributions':{key:dict(Counter(x[key] for x in rows)) for key in ['mechanism_survival','remainder_check','target_contribution_survival','dependency_cascade','scope_survival']},
        'frozen_candidate_count':sum(x['frozen_candidate_count'] for x in rows),
        'judge_added_candidate_count':sum(x['judge_added_count'] for x in rows),
        'assessed_candidate_count':len(all_candidates),
        'viability_field_distributions':{d:{s:sum(x[d]['status']==s for x in all_candidates) for s in c.YESNO} for d in c.DIMENSIONS},
        'viable_candidate_count':sum(c.viable(x) for x in all_candidates),
        'decisively_unresolved_candidate_count':sum(c.unresolved(x) for x in all_candidates),
        'empty_deletion_cases':c.read(H/'artifact-manifest.json')['empty_deletion_cases'],
        'case_design_problems':sum(x['case_design_problem'] for x in rows),
        'judge_remainder_errors':sum(x['judge_remainder_error'] for x in rows),
        'operator_category_counts':dict(Counter(x['operator_category'] for x in rows)),
        'operator_review_is_independent_rater_evidence':False,
        'historical_preservation':guard(),'pairs':pairs,'cases':rows,
        'provider_limitations':{'verified_served_snapshots':sorted({x['validation']['metadata']['verified_served_snapshot'] for f in freezes.values() for x in f['runs']},key=str),
            'harness_retries':0,'exposed_internal_retry_events':sum(len(x['validation']['metadata']['internal_retry_events']) for f in freezes.values() for x in f['runs']),
            'sampling':'one fresh Astra/high context per claim and artifact; no independent-rater or repeat-sample estimate'},
        'interpretation':review['interpretation'],'recommended_next_step':review['recommended_next_step']}

def render(m):
    review=c.read(H/'review/operator.json');targets=c.read(H/'targets.json');byid={x['case_id']:x for x in m['cases']}
    lines=['# Experiment H.2 — remainder-viability calibration v0.1','',
        review['interpretation']['summary'],'',
        '## Publication and lineage','',f'Base: `{m["base_sha"]}`. Branch: `{m["branch"]}`. No merge to main.',
        'The final publication SHA is the commit containing `publication-manifest.json`; resolve it with the command in metrics.json. Checkpoints preceding publication:', '',
        '| Checkpoint | SHA |','|---|---|']
    lines += [f'| {key.removesuffix("_checkpoint")} | `{sha}` |' for key,sha in m['checkpoints'].items()]
    lines += ['', 'H.1 remains `STOPPED_PREMEASUREMENT_DESIGN_GATE`, with zero provider calls. Historical files and runtime evidence were preserved. Each provider stage passed 46 historical checks plus the H.2 test suite before launch.', '',
        'A sandboxed detached launcher ended before any reservation or provider call. Its empty files, positive non-contamination proof and passing 47-check recovery were committed before a host-only launcher continued. No observation was retried or replaced. See [recovery evidence](../remainder-viability-calibration-v0.1/recovery/premeasurement-launch.json).','',
        '## Construct and paired authoring','',
        '**CORE_INVALID means no viable source-derived remainder after all measured unsupported claims are deleted.** A remainder must be warranted, distinctively source-derived, material and relevant to the exact target. Graph position and prose volume do not control status. Unresolved viability or structural contradiction yields UNCERTAIN_LOAD_BEARING; generator policy remains keep + flag.','',
        'Six source instruments were reused verbatim from accepted inputs. The source, bounded target and focal object are identical within each pair. Targets were committed before variants. The following questions and narrowing rationales are frozen:', '',
        '| Mechanism | Bounded target | Narrowing rationale |','|---|---|---|']
    lines += [f'| {t["source"]["name"]} | {t["target"]["question"]} | {t["narrowing_rationale"]} |' for t in targets]
    lines += ['', 'Reduced members preserve a cited bounded comparative, intervention, ordering, reproduction, offset or diagnostic result. Core members retain erased comparison ratings, an input-recorder trace, later custody, a pooled wrong-outcome flag, ordinary documentary dating, or mere test completion. The contrast changes informative evidence, not focal/comparison ownership; it is not a pure graph intervention.', '',
        'The recorded operator gate marked all twelve primary audits as passing before measurement: each reduced member had a four-YES remainder and every enumerated core candidate had a definite NO. Post-freeze review found five primary false passes because negative evidentiary candidates were omitted or misclassified. All five mapping fields were searched, including negative constraints and meaningful next inquiries. The audits are author hypotheses, not independent-rater truth. [Primary audits](../remainder-viability-calibration-v0.1/authoring-audit/primary.json) and [control audits](../remainder-viability-calibration-v0.1/authoring-audit/controls.json).','',
        'The delta draft explicitly made the pooled flag neither necessary nor sufficient for F before freeze, avoiding a negative-flag singleton exclusion. No provider result informed this authoring change.','',
        '| Mechanism | Intended deletion max/min | Measured deleted characters (reduced/core) | Measured max/min |','|---|---:|---|---:|']
    balance={x['mechanism_key']:x for x in c.read(H/'authoring-audit/primary.json')['surface_balance']}
    for pair in m['pairs']:
        ratio=pair['measured_max_min_ratio'];lines.append(f'| {pair["mechanism_key"]} | {balance[pair["mechanism_key"]]["max_min_ratio"]:.3f} | {pair["measured_deleted_chars"]} | {ratio:.3f} |')
    lines += ['', 'All intended ratios were below 1.06. Delta debugging exceeded the 1.15 target after an additional measured unsupported span was deleted. This is retained as a measured imbalance, not repaired. Full lengths, fractions, modal/position checks and case provenance are in the authoring audit and metrics.','',
        '## Claim judgments, ablation and candidates','',
        f'{m["claim_judgment_count"]} claim judgments: '+', '.join(f'{s}={n}' for s,n in m['claim_status_counts'].items())+'.',
        'Every measured UNSUPPORTED span was deleted simultaneously; all other text remained. No subset search, semantic repair or replacement inference was used. All 16 cases were eligible, including empty deletion sets by policy; none actually had an empty set.',
        f'{m["frozen_candidate_count"]} candidates were frozen before artifact calls. The judge added {m["judge_added_candidate_count"]} cited candidates, for {m["assessed_candidate_count"]} assessments. These are correlated, operator-selected text units and direct entailments, not independent observations.', '',
        '| Viability field | YES | NO | UNCERTAIN |','|---|---:|---:|---:|']
    lines += [f'| {d} | {counts["YES"]} | {counts["NO"]} | {counts["UNCERTAIN"]} |' for d,counts in m['viability_field_distributions'].items()]
    lines += ['',f'Four-YES candidates: {m["viable_candidate_count"]}. Decisively unresolved candidates (UNCERTAIN with no NO): {m["decisively_unresolved_candidate_count"]}. Exact model outputs remain in judgments; viable_remainder_assessment files are deterministic projections, not rewritten judgments.','',
        '## Artifact outcomes','', '| Status | Count |','|---|---:|']
    lines += [f'| {s} | {n} |' for s,n in m['artifact_status_counts'].items()]
    lines += ['', '| Mechanism | Intended reduced member | Intended core member | Viable/nonviable boundary separated |','|---|---|---|---|']
    for p in m['pairs']:
        lines.append(f'| {p["mechanism_key"]} | `{p["reduced"]}`: {p["reduced_status"]} | `{p["core"]}`: {p["core_status"]} | {p["viable_vs_nonviable_separated"]} |')
    lines += ['', '| Control | Case | Outcome | Reason |','|---|---|---|---|']
    names={'A':'tiny viable remainder','B':'large generic remainder','C':'target-irrelevant source remainder','D':'unresolved viability'}
    for row in sorted((x for x in m['cases'] if x['is_control']),key=lambda x:x['control']):
        lines.append(f'| {row["control"]}: {names[row["control"]]} | `{row["case_id"]}` | {row["artifact_status"]} | {row["reason"]} |')
    lines += ['', '### All cases and surviving contributions','', '| Case | Status | Reason | Strongest assessed candidate | Operator category |','|---|---|---|---|']
    for row in m['cases']:
        strongest=row['strongest_surviving_target_inference']['text'] or 'None'
        lines.append(f'| [{row["case_id"]}](../remainder-viability-calibration-v0.1/judgments/artifact/{row["case_id"]}.json) | {row["artifact_status"]} | {row["reason"]} | {strongest.replace(chr(10)," ").replace("|","/")} | {row["operator_category"]} |')
    lines += ['', 'A strongest candidate is not automatically viable: its four fields still control. This table includes every KEEP_WITH_WARRANT_FLAGS, KEEP_WITH_REDUCED_SCOPE, CORE_INVALID and UNCERTAIN_LOAD_BEARING case.', '',
        '## Failure modes and operator audit','', '| No-viable-remainder reason | Count |','|---|---:|']
    lines += [f'| {s} | {n} |' for s,n in m['no_viable_remainder_reason_counts'].items()]
    for key,text in review['failure_mode_findings'].items():lines += ['',f'**{key}:** {text}']
    lines += ['',f'Operator categories: {json.dumps(m["operator_category_counts"],sort_keys=True)}.',
        f'Case-design problems: {m["case_design_problems"]}; judge remainder errors: {m["judge_remainder_errors"]}.',
        'Review occurred after both provider stages were frozen. It addresses warrant, source specificity, materiality, exact target relevance, invented repair, overlooked remainders, procedure-volume reasoning and hidden-design mistakes for every case and pair. This is operator interpretation, not independent-rater evidence. [Complete audit](../remainder-viability-calibration-v0.1/review/operator.json).','']
    for text in review['prominent_limitations']:lines.append('- '+text)
    lines += ['', 'The only CORE_INVALID also depends on an explicit distinction between the recorder channel and the target process. This is not a second comparison process, but remains a salient measurement-ownership cue; H.2 does not demonstrate a core boundary free of such cues.', '', '## Research questions and interpretation','']
    for key,value in review['research_answers'].items():lines += [f'**{key}:** {value}','']
    for key in ['boundary_operational','absence_vs_centrality','natural_output_readiness']:
        lines += [f'**{key}:** {review["interpretation"][key]}','']
    lines += ['**Recommended next step:** '+m['recommended_next_step'],'',
        'The recommendation was not executed. No natural-output admission run, Experiment E continuation, production integration, historical experiment modification, or merge to main occurred.','',
        '## Unsupported claims','', '| Case | Claim | Deleted exact span |','|---|---|---|']
    for atom in r.claims():
        judgment=c.read(H/'judgments/claim-warrant'/f'{atom["claim_id"]}.json')
        if judgment['status']=='UNSUPPORTED':
            text=atom['exact_claim_span'].replace('|','/').replace('\n',' ')
            lines.append(f'| `{atom["case_id"]}` | [{atom["claim_id"]}](../remainder-viability-calibration-v0.1/judgments/claim-warrant/{atom["claim_id"]}.json) | {text} |')
    lines += ['', '## Measurement limitations','',
        f'Exactly {m["provider_calls"]} observations in {m["unique_sessions"]} fresh sessions used GPT-6 Astra/high, pinned Codex 0.157.1, disabled tools and isolated contexts. No harness retry, duplicate sample or review model was used. Served snapshots were unavailable (null), not inferred from aliases. Exposed internal retry events: {m["provider_limitations"]["exposed_internal_retry_events"]}; unexposed provider internals remain unknown.',
        'Synthetic authoring, explicit observation semantics, one sample per case, operator-selected candidates and correlated paired/control examples limit generalization. Single-model concordance is not independent validation or an estimate of natural-output error prevalence.','']
    return '\n'.join(lines)

def write_publication():
    for stage in r.STAGES:r.verify_results(stage,True)
    r.committed(H/'review/operator.json')
    m=compute();r.write(H/'metrics.json',m)
    for cid in c.read(H/'manifest.json')['case_order']:
        a=c.read(H/'judgments/artifact'/f'{cid}.json')['remainder_viability']
        r.write(H/'viable-remainder-assessments'/f'{cid}.json',c.projection(a))
    r.raw(REPORT,render(m).encode())
    r.write(H/'final-runtime-freeze.json',{'status':'COMPLETE','files':r.inventory(r.RT.rglob('*'))})

def seal():
    paths=[p for p in H.rglob('*') if p.is_file() and p.name!='publication-manifest.json']+[REPORT,R/'docs/PROBLEM_FRAMES-remainder-viability-calibration-v0.1.md']
    r.write(H/'publication-manifest.json',{'status':'COMPLETE','files':r.inventory(paths),'checkpoint_before_completion':r.head()})

def verify():
    r.verify();runs={stage:r.verify_results(stage,True) for stage in r.STAGES}
    m=compute();c.require(c.read(H/'metrics.json')==m,'Metrics changed')
    c.require(REPORT.read_text()==render(m),'Report changed')
    c.require(m['provider_calls']==73 and m['unique_sessions']==73,'Global observation/session count')
    review=c.read(H/'review/operator.json')
    c.require(review['artifact_freeze_sha256']==c.sha(H/'artifact-freeze.json'),'Review freeze binding')
    c.require({x['case_id'] for x in review['case_reviews']}==set(c.read(H/'manifest.json')['case_order']),'Review coverage')
    for row in review['case_reviews']:
        c.require(row['judgment_sha256']==c.sha(H/'judgments/artifact'/f'{row["case_id"]}.json'),'Review observation changed')
    for cid in c.read(H/'manifest.json')['case_order']:
        a=c.read(H/'judgments/artifact'/f'{cid}.json')['remainder_viability']
        c.require(c.read(H/'viable-remainder-assessments'/f'{cid}.json')==c.projection(a),'Assessment projection changed')
    final_runtime=c.read(H/'final-runtime-freeze.json')['files']
    r.hashes(final_runtime)
    c.require(r.inventory(r.RT.rglob('*'))==final_runtime,'Runtime files added or changed after final freeze')
    for stage in r.STAGES:
        c.require(sorted(p.name for p in (r.RT/'runs'/stage).iterdir())==sorted(r.order(stage)),'Extra or missing provider attempt')
    if (H/'publication-manifest.json').exists():r.hashes(c.read(H/'publication-manifest.json')['files'])
    c.require(r.git('branch','--show-current').decode().strip()=='experiment-h2-remainder','Wrong publication branch')
    return {key:m[key] for key in ['status','primary_pair_count','control_count','claim_judgment_count','artifact_judgment_count','artifact_status_counts','no_viable_remainder_reason_counts','case_design_problems','judge_remainder_errors','historical_preservation']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['write','seal','verify']);a=p.parse_args()
    if a.action=='write':write_publication()
    elif a.action=='seal':seal()
    else:print(json.dumps(verify(),indent=2))
