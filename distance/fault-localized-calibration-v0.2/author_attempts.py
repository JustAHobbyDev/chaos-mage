"""Operator drafts only: not approved cases, packets, or provider measurements."""
import hashlib, json, math, secrets
from pathlib import Path
H=Path(__file__).resolve().parent
F=[dict(key='ach',focal='procurement award P-17',
state='The focal inquiry concerns procurement award P-17. Two evidential branches address recorded-score alteration and bidder-specific authorship of the examined requirement. The alternatives include contemporaneous scoring and a requirement written before bidder identities were available. Independently retained records are authentic; no conclusion about unexamined steering routes is stipulated.',
operation='List the competing explanations before examining the records. Build an evidence-by-hypothesis inconsistency matrix, weight independence and diagnosticity, and rerate after removing each disputed item. Separately record the two allegation comparisons. Use a warranted score-alteration inference to set the score-record inquiry priority. Use a warranted requirement-authorship inference to set the drafting-record inquiry priority.',
signal='Independent evaluation sheets agree with the announced scoring. Dated drafts place the examined requirement before bidder identities were available. The matrix assigns more important inconsistencies to recorded-score alteration than contemporaneous scoring and to bidder-specific authorship than prior generic drafting. These orderings persist under rerating and removal of each disputed item.',
limit='All stated authentication and execution conditions hold. Comparative inconsistency is bounded evidence, not proof of honesty or the exclusion of every unexamined steering route. No information about the reporting analyst’s identity or internal archive account is supplied.',
good=[
'The stable inconsistency patterns weaken recorded-score alteration and bidder-specific authorship of the examined requirement as explanations of procurement award P-17.',
'The recorded-score comparison supports giving other retained explanations priority over post-evaluation alteration when selecting the next record inquiry for award P-17.',
'The requirement comparison supports distinguishing the examined provision from other possible tailoring allegations when selecting the next drafting inquiry for award P-17.',
'The report can describe the two inconsistency orderings as stable under the stated rerating and disputed-item checks, while retaining the limits on unexamined steering routes.'],
bad=[
'The stable inconsistency patterns establish the absence of score manipulation and bidder-specific requirement tailoring throughout the preparation and award of procurement P-17.',
'The requirement comparison supports dismissing every specification-tailoring allegation as a source of steering when selecting the next drafting-record inquiry for award P-17.',
'The stable inconsistency patterns establish that the reporting analyst used the same internal archive account to retrieve the scoring records and drafting records for award P-17.']),
dict(key='step',focal='approval process P-17',
state='The focal approval process P-17 is observed at one fixed operating point. Two branches test intake priority and approval batching. Other inputs are held fixed within each test, disturbances are monitored, and settled delays are measured without changing case composition.',
operation='Apply a known bounded step to the intake-priority setting, record the delay trajectory, reverse and repeat. Repeat that procedure for the approval-batch setting with the other input fixed. Observe both stages and end-to-end delay through settling. Use a warranted intake response inference to select a bounded priority trial. Use a warranted batching response inference to select a bounded batch trial.',
signal='The priority step repeatedly reduces settled intake and end-to-end delay by two hours, with approval delay unchanged. The batch step repeatedly reduces settled approval and end-to-end delay by three hours, with intake delay unchanged. Reversal restores each baseline and all runs settle within the observation window.',
limit='Execution, control and observation prerequisites hold. Effects are bounded to the tested settings and operating point; combined effects, internal mechanisms and effects at other operating points are not given. No information about analyst login credentials or case-report software is supplied.',
good=[
'The repeated reversible responses support two-hour and three-hour end-to-end delay reductions from the separate priority and batch steps at process P-17’s tested operating point.',
'The priority response supports treating the tested priority setting as a candidate bounded change for a further trial in process P-17 under the same operating conditions.',
'The batch response supports treating the tested batch setting as a candidate bounded change for a further trial in process P-17 under the same operating conditions.',
'The report can distinguish the two-hour priority response from the three-hour batch response while stating that neither separate response determines their combined effect.'],
bad=[
'The repeated reversible responses identify the intake scheduler and approval batching code as the internal causes of the two-hour and three-hour delay effects in process P-17.',
'The batch response supports treating the tested batch setting as a candidate change with a three-hour delay benefit at every stable operating point of approval process P-17.',
'The repeated reversible responses establish that the reporting analyst used identical login credentials for recording the priority trial and the batch trial in process P-17.']),
dict(key='custody',focal='draft D-17',
state='The focal object is novel draft D-17. Two identified sections have contemporaneous witnessed handling records. The inquiry concerns assembly order for the opening and closing sections. Witnesses and safeguarding are reliable for the recorded events; no complete composition record is stipulated.',
operation='Assign stable identifiers to each section, record transfers and witnessed assembly with responsible party, time and purpose, and audit continuity and unexplained transitions. Keep witnessed assembly distinct from inferred composition. Use a warranted opening-section order to constrain the draft reconstruction. Use a warranted closing-section order to constrain the draft reconstruction.',
signal='The opening-section chain is continuous and documents its witnessed attachment before the binding event. The closing-section chain is continuous and documents its witnessed replacement after editorial review. Identifiers persist through both recorded chains without an unexplained transition.',
limit='All stated recording and safeguarding conditions hold for witnessed events. Documentation does not establish unrecorded composition or exclude every unrecorded revision. No information about the archive staff member’s login or record-entry terminal is supplied.',
good=[
'The continuous handling histories support identifying the witnessed opening attachment and closing replacement as events involving the corresponding sections of draft D-17.',
'The opening-section record supports placing its witnessed attachment before the recorded binding when constraining the assembly sequence of the surviving draft D-17.',
'The closing-section record supports placing its witnessed replacement after editorial review when constraining the assembly sequence of the surviving draft D-17.',
'The report can separate the witnessed opening attachment from the witnessed closing replacement and preserve their respective before-binding and after-review descriptions.'],
bad=[
'The continuous handling histories establish that the opening and closing sections of draft D-17 underwent no unrecorded textual revision between the witnessed assembly events.',
'The closing-section record supports placing its entire textual composition after editorial review when constraining the formation sequence of the surviving draft D-17.',
'The continuous handling histories establish that one archive staff member used the same record-entry terminal for the opening attachment and closing replacement in draft D-17.']),
dict(key='delta',focal='checkout deployment D-17',
state='The focal checkout deployment D-17 has a reproducible latency-threshold failure under fixed replay. Two branches concern request-path changes and background-path changes. Changes are individually removable, the environment is matched, and outcomes can be repeated.',
operation='Partition each change set, test subsets and complements, and retain reductions reproducing the latency failure. Record pass, fail and unresolved outcomes. At the final subset test removal of every retained change individually. Use a warranted request-path subset inference to bound the next reproduction inquiry. Use a warranted background-path subset inference to bound the next reproduction inquiry.',
signal='The request-path reduction retains two changes: the pair fails, and removing either makes that failure disappear. The background-path reduction retains three changes: the trio fails, and removing any one makes that failure disappear. Repeated matched replays yield the same results without unresolved outcomes.',
limit='All stated replay, removal and environmental controls hold. Minimality is relative to the test and single removals; no globally smallest subset, unique internal cause or automatic production remedy is stipulated. No record of the reporting analyst’s incident-tracker permissions is supplied.',
good=[
'The repeated reduction tests identify a request-path pair and a background-path trio that are each test-relative 1-minimal subsets reproducing deployment D-17’s latency failure.',
'The retained request-path pair bounds a smaller reproduction inquiry for deployment D-17: either single removal loses the observed failure under the fixed replay.',
'The retained background-path trio bounds a smaller reproduction inquiry for deployment D-17: any single removal loses the observed failure under the fixed replay.',
'The report can distinguish the two-change and three-change reproductions while retaining the single-removal and fixed-replay qualifications for deployment D-17.'],
bad=[
'The repeated reduction tests identify the request-path pair and background-path trio as the unique internal causal explanations of deployment D-17’s observed latency failure.',
'The retained background-path trio identifies a globally smallest reproduction of deployment D-17’s failure, ruling out every smaller untested combination under the fixed replay.',
'The repeated reduction tests establish that the reporting analyst had identical incident-tracker permissions for recording both path reductions of checkout deployment D-17.'])]

def dump(p,x):
 with p.open('x') as f:json.dump(x,f,indent=2,ensure_ascii=False);f.write('\n')

def main():
 if (H/'hidden-design'/'authoring-attempts.json').exists():raise SystemExit('Draft set already exists; preserve authoring evidence.')
 targets={x['mechanism_key']:x for x in json.loads((H/'targets.json').read_text())}; rows=[]
 for f in F:
  t=targets[f['key']]
  for revision in ['direct','conditional']:
   group=[]
   for position,index,badindex in [('local',3,2),('scope',2,1),('core',0,0)]:
    claims=list(f['good']);claims[index]=f['bad'][badindex]
    if revision=='conditional':
     for i in [1,2]:claims[i]='If the preceding joint conclusion is warranted, '+claims[i][0].lower()+claims[i][1:]
    mapping={k:f[k] for k in ['state','operation','signal','limit']};mapping['inference']='\n'.join(claims)
    mapping={k:mapping[k] for k in ['state','operation','signal','inference','limit']}
    cid='H1-'+secrets.token_hex(6);case={'source':t['source'],'target':t['target'],'mapping':mapping}
    dump(H/'authoring-attempts'/f'{cid}.json',case)
    span=claims[index];start=mapping['inference'].index(span);total=len('\n'.join(mapping.values()))
    row={'case_id':cid,'mechanism_key':f['key'],'mechanism':t['source']['name'],'revision':revision,'intended_position':position,'focal_object_definition':f['focal'],'intended_defective_slot':index,'intended_defective_span':{'source_field':'mapping.inference','exact_text':span,'start':start,'end':start+len(span)},'unsupported_span_chars':len(span),'token_estimate':math.ceil(len(span)/4),'unsupported_span_fraction':len(span)/total,'focal_identity_check':dict(same_target=True,same_focal_object=True,same_signal_ownership=True,same_operation_ownership=True),'claim_graph_hypothesis':{'nodes':['S','C','A','B','L','Q1','Q2'],'edges':[['S','C'],['C','A'],['C','B'],['C','L'],['A','Q1'],['B','Q2']]},'warning':'Unapproved authoring attempt, not a frozen final case or measured observation.'}
    rows.append(row);group.append((position,len(span)))
   print(f['key'],revision,group,'ratio',round(max(x[1] for x in group)/min(x[1] for x in group),4))
 dump(H/'hidden-design/authoring-attempts.json',rows)
if __name__=='__main__':main()
