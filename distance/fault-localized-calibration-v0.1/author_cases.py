"""Operator-authored stimuli. NEVER provider input. Run only before measurement."""
import json
import secrets
import subprocess
from pathlib import Path
H=Path(__file__).resolve().parent
R=H.parent.parent
G=R/'distance/anti-collapse-natural-recovery-v0.1/generation-inputs'

def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(v,f,indent=2,ensure_ascii=False);f.write('\n')

FAMILIES=[
 dict(key='ach',input='E006',name='Analysis of Competing Hypotheses',
 focal='the procurement award under investigation',reference='a completed comparison award from the same agency',
 template='the agency tender-document template',
 branches=['recorded-score manipulation','bidder-specific specification tailoring'],
 state='The inquiry has two evidential panels: A concerns recorded-score manipulation; B concerns bidder-specific specification tailoring. The focal and comparison awards used the same tender-document template. Each panel contains authenticated, contemporaneous material for its assigned award, not a mixture of awards.',
 operation='For each panel, list the competing explanations before scoring evidence. Construct an evidence-by-hypothesis inconsistency matrix; weight documentary independence and diagnosticity rather than counting supporting items. Have a second analyst rerate the matrix and repeat after removal of each disputed item. Keep the scoring-manipulation and specification-tailoring questions separate.',
 signal='In panel A, independently retained evaluation sheets agree with the announced scoring, and the stable matrix pattern conflicts with post-evaluation alteration of recorded scores. In panel B, dated drafting records show a common requirement carried over before bidder identities were available; the stable matrix pattern conflicts with bidder-specific authorship of that requirement. The patterns persist under the stated rerating and sensitivity checks.',
 conclusions=['For {owner}, panel A weakens post-evaluation alteration of the recorded scores as an explanation of that award.', 'For {owner}, panel B weakens bidder-specific authorship of the examined requirement as an explanation of that award.'],
 actions=['In the focal-award account, de-prioritize the recorded-score alteration allegation only if the panel-A inference applies to that award.', 'In the focal-award account, distinguish the examined requirement from other unexamined tailoring allegations only if the panel-B inference applies to that award.'],
 bridge='Use of the same tender-document template makes the panel-{panels} evidential conclusion{plural} for the comparison award applicable to the focal award.',
 leaf='Use of the same tender-document template establishes that the two awards were assigned the same internal records-retention code.',
 limit='These are bounded evidential comparisons, not proof of honest intent or absence of steering by other means. Hypotheses and evidence quality constrain the matrix. Template identity is the only stated cross-award connection; no event, author, bidder, or outcome identity is stipulated.'),
 dict(key='step',input='E022',name='Step-response probing',
 focal='the approval process under investigation',reference='a completed comparison process in another unit',template='the approval-workflow template',
 branches=['intake-priority intervention','approval-batch intervention'],
 state='The inquiry uses two intervention panels: A tests an intake-priority setting; B tests an approval-batch setting. The focal and comparison processes use the same approval-workflow template. Each panel concerns its assigned process at a fixed operating point; the two processes are not asserted to share their response dynamics.',
 operation='For each panel, change only its named setting by a known bounded step, record stage and end-to-end delay through the transient and settled periods, then reverse and repeat. Hold other inputs fixed and monitor disturbances. Use the same observation window and abort criterion across repetitions.',
 signal='In panel A, the priority step reproducibly reduces settled intake delay by two hours without raising downstream delay, and reversal restores the prior trajectory. In panel B, the batch step reproducibly reduces settled approval delay by three hours without raising intake delay, and reversal restores the prior trajectory. Both responses settle within the observation window without an abort.',
 conclusions=['For {owner}, panel A supports a two-hour end-to-end delay reduction from the tested priority step at the tested operating point.', 'For {owner}, panel B supports a three-hour end-to-end delay reduction from the tested batch step at the tested operating point.'],
 actions=['Treat the tested priority step as a bounded candidate change for the focal process only if its panel-A response inference applies there.', 'Treat the tested batch step as a bounded candidate change for the focal process only if its panel-B response inference applies there.'],
 bridge='Use of the same approval-workflow template makes the panel-{panels} response conclusion{plural} for the comparison process applicable to the focal process.',
 leaf='Use of the same approval-workflow template establishes that the two processes have the same internal training-budget code.',
 limit='All stated intervention, disturbance-control, observation and reversal conditions are satisfied. Estimates concern only the tested settings and operating points, not unique internal causes or general optimization. Workflow-template identity is the only stated cross-process connection; staffing, dynamics and resource costs are not stipulated equal.'),
 dict(key='custody',input='E030',name='Chain-of-custody verification',
 focal='the novel draft under investigation',reference='a separate comparison draft held by the same archive',template='the archive handling-ledger template',
 branches=['opening-section assembly constraint','closing-section assembly constraint'],
 state='The inquiry uses two provenance panels: A tracks an opening-section packet; B tracks a closing-section packet. The focal and comparison drafts use the same archive handling-ledger template. Each panel tracks identified leaves of its assigned draft; a matching ledger form does not stipulate that two drafts contain the same events.',
 operation='Assign stable identifiers to leaves, record each witnessed handling or assembly event with responsible party, time and purpose, and audit the chain for unexplained transitions. Separate witnessed assembly from inferred composition and retain the event-specific evidence tags. Audit the two panels independently.',
 signal='Panel A has a continuous reliable ledger and witnessed attachments placing its identified opening-section assembly before its dated binding event. Panel B has a continuous reliable ledger and witnessed attachments placing its identified closing-section replacement after its dated editorial review. Neither chain contains an unexplained transition in the interval examined.',
 conclusions=['For {owner}, panel A supports the bounded sequence that its identified opening-section assembly preceded its recorded binding event.', 'For {owner}, panel B supports the bounded sequence that its identified closing-section replacement followed its recorded editorial review.'],
 actions=['Constrain the focal draft reconstruction by the opening-section assembly-before-binding sequence only if the panel-A sequence inference applies to that draft.', 'Constrain the focal draft reconstruction by the closing-section replacement-after-review sequence only if the panel-B sequence inference applies to that draft.'],
 bridge='Use of the same archive handling-ledger template makes the panel-{panels} sequence conclusion{plural} for the comparison draft applicable to the focal draft.',
 leaf='Use of the same archive handling-ledger template establishes that the two drafts received the same internal shelf-label color.',
 limit='Recording and safeguarding are reliable for the witnessed events stated here; no inference to unrecorded events, unchanged authorial intention or complete composition history is supplied. Ledger-template identity is the only stated cross-draft connection; shared authorship, leaf identity and assembly dates are not stipulated.'),
 dict(key='delta',input='E028',name='Delta debugging',
 focal='the checkout deployment under investigation',reference='a comparison checkout deployment maintained by another team',template='the deployment-manifest template',
 branches=['request-path latency configuration','background-path latency configuration'],
 state='The inquiry has two failure-reproduction panels: A concerns request-path changes; B concerns background-path changes. The focal and comparison deployments use the same deployment-manifest template. Each panel tests configurations from its assigned deployment, with reproducible latency failure and individually removable changes.',
 operation='Within each panel, partition the changed configuration, test subsets and complements, and retain reductions reproducing its latency threshold failure. Use a fixed replay and matched environment, record pass/fail/unresolved outcomes, and finish by testing removal of each retained change separately. Do not rank components from a single untested reduction.',
 signal='Panel A ends at a two-change request-path subset that reproduces its latency failure; removing either retained change makes that failure disappear. Panel B ends at a three-change background-path subset that reproduces its latency failure; removing any retained change makes that failure disappear. Repeated replays give the same outcomes without unresolved tests.',
 conclusions=['For {owner}, panel A identifies a test-relative 1-minimal request-path subset sufficient to reproduce its observed latency failure under the replay.', 'For {owner}, panel B identifies a test-relative 1-minimal background-path subset sufficient to reproduce its observed latency failure under the replay.'],
 actions=['Use the request-path subset to bound the focal deployment investigation only if the panel-A reproduction inference applies to that deployment.', 'Use the background-path subset to bound the focal deployment investigation only if the panel-B reproduction inference applies to that deployment.'],
 bridge='Use of the same deployment-manifest template makes the panel-{panels} reproduction conclusion{plural} for the comparison deployment applicable to the focal deployment.',
 leaf='Use of the same deployment-manifest template establishes that the two deployments use the same internal incident-ticket prefix.',
 limit='The replay and environmental controls stated above are satisfied. Minimality is relative to single removals and this test, not a unique cause, globally smallest subset or automatic production remedy. Manifest-template identity is the only stated cross-deployment connection; code, component semantics and failure mechanisms are not stipulated equal.'),
 dict(key='crossdate',input='E008',name='Dendrochronological crossdating',
 focal='the undated correspondence bundle under investigation',reference='a separate comparison correspondence bundle from the same collection',template='the correspondence-register template',
 branches=['earlier-run chronology','later-run chronology'],
 state='The inquiry uses two sequence panels: A is an earlier run of correspondence entries; B is a later run. The focal and comparison bundles use the same correspondence-register template. Each panel contains ordered observations from its assigned bundle and independently dated overlapping reference sequences recording the same external annual cycle.',
 operation='Compare distinctive ordered patterns of high and low annual activity across the panel and its independently dated references. Shift candidate alignments, check missing and duplicate increments against independent anchors, and retain the alignment consistently supported across the overlapping records. Keep the two panels separate.',
 signal='Panel A has one repeatedly supported multi-year alignment across three independent overlapping records, agreeing with two independent calendar anchors and exposing a missing increment. Panel B has one repeatedly supported multi-year alignment across three independent overlapping records, agreeing with two independent calendar anchors and exposing a duplicated increment. Competing shifts fail these stated checks.',
 conclusions=['For {owner}, panel A supports assigning its earlier-run entries to the reference-aligned calendar positions with the identified missing increment accounted for.', 'For {owner}, panel B supports assigning its later-run entries to the reference-aligned calendar positions with the identified duplicated increment accounted for.'],
 actions=['Use the earlier-run alignment to constrain the focal bundle chronology only if the panel-A dating inference applies to that bundle.', 'Use the later-run alignment to constrain the focal bundle chronology only if the panel-B dating inference applies to that bundle.'],
 bridge='Use of the same correspondence-register template makes the panel-{panels} dating conclusion{plural} for the comparison bundle applicable to the focal bundle.',
 leaf='Use of the same correspondence-register template establishes that the two bundles received the same internal catalog label color.',
 limit='The stated shared annual influences, ordered observations, independent references and anchors hold within each panel. Dating remains evidential support rather than infallibility. Register-template identity is the only stated cross-bundle connection; contemporaneity, correspondent identity and event synchrony between the two bundles are not stipulated.'),
 dict(key='diagnosis',input='E010',name='Differential diagnosis',
 focal='the approval process under investigation',reference='a comparison approval process in another unit',template='the approval-case form',
 branches=['intake-delay differential','approval-delay differential'],
 state='The inquiry has two diagnostic panels: A addresses intake delay; B addresses approval-stage delay. The focal and comparison processes use the same approval-case form. Each panel contains observations from its assigned process and a maintained list of rival explanations rather than a preselected single cause.',
 operation='For each panel, list plausible mechanisms, specify which observations would bear differently on them, inspect those observations and revise the relative plausibilities. Check the supplied observation definitions, independence and test limitations. Retain alternatives that the evidence does not discriminate.',
 signal='In panel A, delay clusters at fixed intake release times while independently logged available capacity remains idle between releases; this pattern fits scheduled release better than continuously exhausted capacity. In panel B, the same cases repeatedly return for documented missing fields while unrelated complete cases advance; this pattern fits case rework better than a uniform approval-stage queue. The observation definitions and reliability checks are satisfied.',
 conclusions=['For {owner}, panel A supports prioritizing scheduled intake release over continuously exhausted capacity within the supplied differential.', 'For {owner}, panel B supports prioritizing missing-field rework over a uniform approval-stage queue within the supplied differential.'],
 actions=['Prioritize inquiry into intake release scheduling in the focal process only if the panel-A differential inference applies there.', 'Prioritize inquiry into missing-field rework in the focal process only if the panel-B differential inference applies there.'],
 bridge='Use of the same approval-case form makes the panel-{panels} differential conclusion{plural} for the comparison process applicable to the focal process.',
 leaf='Use of the same approval-case form establishes that the two processes use the same internal case-file label color.',
 limit='The supplied comparisons warrant relative priorities, not exclusion of all unlisted or co-occurring causes. Evidence quality and hypothesis coverage still bound the differential. Form identity is the only stated cross-process connection; staffing, scheduling and rework mechanisms are not stipulated equal.')
]

def make(f,position,control=None):
 owners={'local':[f['focal'],f['focal']], 'scope':[f['focal'],f['reference']], 'core':[f['reference'],f['reference']]}[position]
 inference=[f['conclusions'][i].format(owner=owners[i]) for i in range(2)]
 defect=f['leaf'] if position=='local' else f['bridge'].format(panels='B' if position=='scope' else 'A and B',plural='' if position=='scope' else 's')
 inference.append(defect)
 state=f["state"]+'\nPanel A is assigned to '+owners[0]+'.\nPanel B is assigned to '+owners[1]+'.'
 operation=f['operation']+'\n'+'\n'.join(f['actions'])
 cid='H-'+secrets.token_hex(6)
 source=json.loads((G/(f['input']+'.json')).read_text())
 case={'source':source['source'],'target':source['target'],'mapping':dict(state=state,operation=operation,signal=f['signal'],inference='\n'.join(inference),limit=f['limit'])}
 if control==1:
  case['mapping']['state']+=' The comparison dossier is professionally prepared and complete for its own award.'
 if control==2:
  inference += ['Use of the same archive handling-ledger template establishes that the two drafts received the same internal box-label font.', 'Use of the same archive handling-ledger template establishes that the two drafts were entered using the same inventory-workstation model.', 'Use of the same archive handling-ledger template establishes that the two drafts received the same internal transport-slip border.']
  case['mapping']['inference']='\n'.join(inference)
 if control==3:
  inference[-1]='Use of the same approval-case form establishes a catastrophic breach of the archive display-color standard for both processes.'
  case['mapping']['inference']='\n'.join(inference)
 if control==4:
  inference[-1]='The register-format match carries the two panel dating results over to the focal bundle.'
  case['mapping']['inference']='\n'.join(inference)
 if control==5:
  case['mapping']['operation']+='\nPreserve a run ledger. Record the replay identifier for each trial. Save each tested subset. Record complement tests separately. Keep the removal order. Retain unresolved-outcome logs. Archive the final configurations.'
 if control==6:
  # One small direct target branch; the elaborate advertised comparison branch remains unwarranted.
  case['mapping']['operation']+='\nFor panel B, retain the transient plot, settled-window table, reversal plot, disturbance log, stage-delay table and repetition overlay as separate work products. Prepare the focal-process batch-change briefing only if the panel-B inference applies there.'
  case['mapping']['state']+=' The priority change is a small operational adjustment; the batch-change proposal is the main advertised intervention package.'
 defects=inference[2:]
 intended={'mechanism':f['name'],'matched_triple':None if control else f['key'],'intended_structural_position':position,'is_control':control is not None,'control_number':control,
 'unsupported_claims':[{'id':f'D{i+1}','exact_text':x,'source_field':'mapping.inference'} for i,x in enumerate(defects)],
 'supported_by':['signal.panel_A','signal.panel_B','state.template_identity'],
 'dependents':{'claims':[], 'actions':[] if position=='local' else [f'operation.action_{i}' for i in ([2] if position=='scope' else [1,2])], 'target_contributions':[] if position=='local' else [f['branches'][i] for i in ([1] if position=='scope' else [0,1])]},
 'expected_surviving_contributions':f['branches'] if position=='local' else f['branches'][:1] if position=='scope' else [],
 'expected_artifact_status':{'local':'KEEP_WITH_WARRANT_FLAGS','scope':'KEEP_WITH_REDUCED_SCOPE','core':'CORE_INVALID'}[position],
 'warrant_plausibility_audit':'Template identity does not establish the asserted administrative property or transfer event-specific conclusions across distinct objects. The statement is unconditional, not a supplied unresolved empirical condition. The two panel conclusions are independently bounded to their assigned objects.',
 'survivor_audit':'For core designs both supported panel conclusions concern the comparison object. The focal-target directives are explicitly conditional on applying those conclusions to the focal object. There is no independent focal-target measurement or result. A reviewer may nevertheless find a material next-inquiry contribution; report that rather than forcing agreement.',
 'graph':{'nodes':[{'id':'signal.panel_A','text':f['signal'].split(' In panel B')[0] if f['key']=='step' else f['signal']},{'id':'signal.panel_B','text':f['signal']},{'id':'claim.panel_A','text':inference[0]},{'id':'claim.panel_B','text':inference[1]},{'id':'operation.action_1','text':f['actions'][0]},{'id':'operation.action_2','text':f['actions'][1]}],
 'edges':[['signal.panel_A','claim.panel_A'],['signal.panel_B','claim.panel_B']]+[['claim.panel_A','operation.action_1'],['claim.panel_B','operation.action_2']]+([] if position=='local' else [['D1','operation.action_2']])+([] if position!='core' else [['D1','operation.action_1']])}}
 write(H/'cases'/f'{cid}.json',case)
 write(H/'hidden-design'/f'{cid}.json',intended)
 return cid

def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['primary','controls']);a=p.parse_args()
 if a.stage=='primary':
  rows=[]
  for f in FAMILIES:
   ids=[make(f,pos) for pos in ['local','scope','core']]
   rows.append({'mechanism':f['name'],'case_ids':ids,'constant_fields':['target','source','mapping.signal','mapping.limit','operation procedure and focal-target directives'], 'controlled_changes':['panel ownership routes zero, one or both source-derived branches through the unsupported template-to-object bridge','bounded panel inferences name the assigned object','unsupported leaf versus branch or central bridge'], 'defect_count_intended':[1,1,1],'explicit_inference_count':[3,3,3], 'confound_disclosure':'Comparison-object routing is the operational implementation of dependency position. Thus state owner assignments and referents differ necessarily; this is not a pure identical-prose graph intervention. All six families use the same template-transfer warrant gap, limiting generalization across defect types.'})
  write(H/'hidden-design/comparability.json',rows)
 else:
  for i,key,pos in [(1,'ach','core'),(2,'custody','local'),(3,'diagnosis','local'),(4,'crossdate','core'),(5,'delta','core'),(6,'step','scope')]:make(next(f for f in FAMILIES if f['key']==key),pos,i)
if __name__=='__main__':main()
