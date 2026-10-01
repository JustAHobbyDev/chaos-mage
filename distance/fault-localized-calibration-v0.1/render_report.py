"""Render the final report from frozen measurements and operator audit."""
import json
from collections import Counter,defaultdict
from pathlib import Path
import runner as r
import contracts as c
H=r.H
m=c.read(H/'metrics.json');rows=m['cases'];manifest=c.read(H/'manifest.json')
def table(headers,values):
 return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join('---' for _ in headers)+'|']+['| '+' | '.join(str(x).replace('|','/') for x in row)+' |' for row in values])+'\n'
def case_link(cid):return f'[{cid}](../fault-localized-calibration-v0.1/cases/{cid}.json)'
def ids(items):return ', '.join(case_link(x['case_id']) for x in items) or 'None.'
def artifact(row):return row['artifact']['artifact_status'] if row['artifact'] else 'NOT_APPLICABLE'
core=[x for x in rows if artifact(x)=='CORE_INVALID'];uncertain=[x for x in rows if artifact(x)=='UNCERTAIN_LOAD_BEARING'];controls=sorted([x for x in rows if x['is_control']],key=lambda x:x['control_number'])
text=['# Experiment H — Fault-localized viability calibration v0.1\n',c.read(H/'review/interpretation.json')['lead'],'\n## Checkpoints\n']
commits=[]
for line in r.git('log','--reverse','--format=%H%x09%s',manifest['starting_sha']+'..HEAD').decode().splitlines():
 sha,subject=line.split('\t',1);commits.append([f'`{sha}`',subject])
text.append(table(['SHA','Checkpoint'],commits))
text.append('The publication checkpoint is the commit containing this report; its SHA is supplied in the final handoff rather than self-embedded. Starting main/origin: `'+manifest['starting_sha']+'`.\n')
text.append('## Design and measured workload\n')
text.append('Six accepted frozen instruments, each with a LOCAL/SCOPE/CORE primary triple, plus six controls: 24 authored cases. The exact mechanism set is shown below. Existing target questions were reused; no natural output was generated and no instrument was extracted.\n')
text.append(table(['Mechanism','Primary outcomes'],[[key,', '.join(f'{s}: {n}' for s,n in value.items())] for key,value in m['primary_by_mechanism'].items()]))
text.append('Each triple holds source, target, signal, limits, two-panel procedure, and conditional target actions constant. Panel ownership and inference referents implement the dependency manipulation: two focal-object panels plus a leaf defect; one focal panel and one comparison panel with a defective transfer bridge; or two comparison panels with a shared defective bridge to the focal target. Every primary mapping has three explicit inference-field claims and one intended unsupported claim. Embedded compatibility assertions are also measured. Hidden graphs were frozen separately and never sent to judges.\n')
text.append('This is a controlled but narrow construction. All six families use template identity as the unwarranted bridge. Panel routing necessarily changes which object was observed; H is not a pure graph intervention on identical prose. Shared target-domain reference objects preserve instrument-to-target domain distance, but reference-versus-focal ownership is a salient textual cue that a judge could exploit. The experiment therefore cannot isolate dependency reasoning from all alternative heuristics. Hidden intended classes are design hypotheses, not ground truth.\n')
text.append(table(['Control','Mechanism','Design','Outcome'],[[x['control_number'],x['mechanism'],{1:'One unsupported central claim',2:'Several unsupported local leaves',3:'Dramatic-sounding leaf',4:'Mundane central bridge',5:'Many executable operations without target payoff',6:'Small distinctive material surviving branch'}[x['control_number']],artifact(x)] for x in controls]))
text.append(f"\nAll five fields were audited in 470 source units; {m['claim_count']} atomic claims received one fresh Astra/high judgment each. There were {len([x for x in rows if x['artifact']])} eligible simultaneous ablations, {m['provider_calls']} provider calls and {m['unique_sessions']} unique sessions. No harness retries, duplicate samples, alternative providers or review-model calls occurred.\n")
text.append(table(['Claim status','Count'],m['claim_warrant_distribution'].items()))
text.append('Claim results were committed before ablation packets. All measured UNSUPPORTED spans were deleted simultaneously. No CONDITIONAL_WARRANT, UNCERTAIN, or zero-unsupported cases occurred, so all 24 cases received artifact judgments.\n')
text.append('## Artifact dimensions and structural positions\n')
for dimension,distribution in m['distributions'].items():
 text.append('### '+dimension+'\n');text.append(table(['Value','Count'],distribution.items()))
text.append(table(['Primary intended position','Observed statuses'],[[p,', '.join(f'{s}: {n}' for s,n in values.items())] for p,values in m['primary_by_position'].items()]))
text.append('Cascade was diagnostic only. The frozen base derivation uses hard failures, then decisive uncertainty, then mechanism/target contribution. The user-confirmed unresolved-contradiction exception can override even a hard failure. Raw responses were never rewritten to make their fields agree.\n')
text.append('## Every case and shortcut diagnostics\n')
text.append(table(['Case','Mechanism','Design position','Control','Claims','Unsupported','Deleted chars','Deleted %','Artifact status','Review'],[[case_link(x['case_id']),x['mechanism'],x['intended_position'],x['control_number'] or '—',x['claims'],x['claim_statuses']['UNSUPPORTED'],x['deleted_characters'],f"{100*x['deleted_fraction']:.2f}",artifact(x),x['review']['category']] for x in rows]))
text.append('Deletion volume counts Python Unicode characters in the union of nonoverlapping deleted spans, divided by characters across the five original mapping fields. This is descriptive, not a fitted classifier or an accuracy threshold.\n')
by_count=defaultdict(Counter)
for x in rows:by_count[x['claim_statuses']['UNSUPPORTED']][artifact(x)]+=1
text.append(table(['Unsupported count','Artifact counts'],[[n,', '.join(f'{s}: {v}' for s,v in values.items())] for n,values in sorted(by_count.items())]))
by_status=defaultdict(list)
for x in rows:
 if x['artifact']:by_status[artifact(x)].append(x)
text.append(table(['Status','Deleted characters, min–max','Deleted fraction, min–max'],[[s,f"{min(x['deleted_characters'] for x in xx)}–{max(x['deleted_characters'] for x in xx)}",f"{100*min(x['deleted_fraction'] for x in xx):.2f}%–{100*max(x['deleted_fraction'] for x in xx):.2f}%"] for s,xx in by_status.items()]))
text.append(c.read(H/'review/interpretation.json')['shortcut_analysis'])
text.append('\n## CORE_INVALID and UNCERTAIN_LOAD_BEARING\n')
text.append('All CORE_INVALID cases: '+ids(core)+'\n\nAll UNCERTAIN_LOAD_BEARING cases: '+ids(uncertain)+'\n')
for x in core+uncertain:
 a=x['artifact'];text.append(f"### {x['case_id']} — {artifact(x)}\n\n{a['rationale']}\n\nCentral bridge: {a['central_bridge']['deleted_claim_is_required_for_all_material_contributions']}. {a['central_bridge']['rationale']}\n")
text.append('One-defect CORE cases: '+ids([x for x in core if x['claim_statuses']['UNSUPPORTED']==1])+'\n\nMany-defect non-core cases: '+ids([x for x in rows if x['claim_statuses']['UNSUPPORTED']>1 and artifact(x) in ['KEEP_WITH_WARRANT_FLAGS','KEEP_WITH_REDUCED_SCOPE']])+'\n')
text.append('## Post-freeze operator audit\n')
text.append('This is the same operator’s post-freeze design/interpretation audit, not independent-rater agreement. Every case separately assesses intended warrant, omitted surviving contributions, invented dependencies, overlooked dependencies, operations-only reasoning, and strongest-inference citation survival. Model responses and hidden designs remain unchanged. Structured audit records are in [operator-audit.json](../fault-localized-calibration-v0.1/review/operator-audit.json).\n')
for category in ['STRUCTURALLY_CONCORDANT','PLAUSIBLE_ALTERNATIVE','CASE_DESIGN_PROBLEM','JUDGE_DEPENDENCY_ERROR','AMBIGUOUS']:
 text.append(f"**{category}:** "+ids([x for x in rows if x['review']['category']==category])+'\n')
for x in rows:text.append(f"### {x['case_id']}\n\n{x['review']['rationale']}\n")
text.append('## Strongest surviving inference and no-repair audit\n')
text.append(table(['Case','Strongest inference','Citation excerpts'],[[case_link(x['case_id']),x['artifact']['strongest_surviving_target_inference']['text'] or 'None identified',len(x['strongest_source_proof'])] for x in rows if x['artifact']]))
text.append('All nonempty strongest-inference citations were validated as exact surviving mapping excerpts. Offset/hash proofs are retained in metrics. Mechanical validation establishes provenance and deletion non-overlap, not semantic entailment; the operator checks that separately. Empty strongest-inference fields are retained where no material target inference was identified.\n')
text.append(c.read(H/'review/interpretation.json')['no_repair_audit'])
text.append('\n## Integrity and recovery\n')
text.append(f"Historical preservation checks cover {m['historical_tracked_files']} tracked files and {m['historical_runtime_files']} runtime files. G/F and all earlier scientific evidence are unchanged. The passing preflights each contain 43 checks. H has 13 offline tests and the original G suite has 34. Provider isolation and raw-event audits recorded no tools, session reuse, model substitution or launches while paused. Requested model: gpt-6-astra/high through pinned CLI 0.157.1. Returned identifiers: {m['returned_model_identifiers']}; verified served snapshot remains unavailable. Unexposed provider-internal retries cannot be ruled out.\n")
text.append('One premeasurement engineering recovery was required: a G unit test directly invoked its historical Git allowlist and rejected H additions. The failed 42/43 preflight was preserved. The H-only adapter verifies live bytes and scopes historical Git queries while running unchanged G tests. The complete rerun passed before any request. Original prompts, schemas, classifiers, order, execution settings and runner hashes stayed unchanged. See [incident evidence](../fault-localized-calibration-v0.1/recovery/premeasurement/incident.json).\n')
text.append('A later agent-server restart killed the scheduler while the original fourth ablation child continued. That same child completed one fresh tool-free turn; its final event matched response.json and the frozen validator passed. The response was written about 72 seconds after launch, within the original 900-second deadline. The parent-collected exit code is unavailable and remains null; no zero exit code is inferred. Missing validation bookkeeping was added without replacing a response or earlier validation. A committed 44-check recovery preflight preceded the twenty never-reserved suffix requests. Their scheduler was detached from the daemon lifetime. See [restart evidence](../fault-localized-calibration-v0.1/recovery/daemon-restart/incident.json).\n')
interpretation=c.read(H/'review/interpretation.json')
text.append('## Research questions and interpretation\n'+interpretation['research_answers'])
text.append('\n## Limitations and recommendation\n'+interpretation['limitations_and_recommendation'])
text.append('\nNo accuracy threshold was preregistered or applied. No production integration, natural-output experiment, new instrument extraction or E resumption occurred. Stop after Experiment H; the recommendation has not been executed.\n')
p=r.R/'distance/review/fault-localized-calibration-v0.1.md'
r.raw(p,('\n'.join(text)).encode())
print(p)
