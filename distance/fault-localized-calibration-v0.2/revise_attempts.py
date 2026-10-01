"""Second conditional attempt: eliminate material reporting-leaf redundancy."""
import json, secrets, math
from pathlib import Path
from author_attempts import F, H, dump
BRANCHES={
'ach':[
'If that joint conclusion holds, the recorded-score allegation can be given lower priority than the retained alternatives in the next inquiry for procurement award P-17.',
'If that joint conclusion holds, the examined requirement can be separated from unexamined tailoring allegations in the next drafting inquiry for procurement award P-17.',
'If that joint conclusion holds, the retained drafting record excludes every specification-tailoring route to steering, leaving no tailoring allegation needing inquiry for award P-17.'],
'step':[
'If that joint conclusion holds, the tested priority setting is a candidate bounded delay-reduction change for a further trial at process P-17’s measured operating point.',
'If that joint conclusion holds, the tested batch setting is a candidate bounded delay-reduction change for a further trial at process P-17’s measured operating point.',
'If that joint conclusion holds, the tested batch setting reproducibly delivers a three-hour delay benefit at every stable operating point of process P-17 under the monitored inputs.'],
'custody':[
'If that joint conclusion holds, the opening section’s witnessed attachment can be placed before binding when constraining the assembly sequence of draft D-17.',
'If that joint conclusion holds, the closing section’s witnessed replacement can be placed after editorial review when constraining the assembly sequence of draft D-17.',
'If that joint conclusion holds, the closing section’s entire textual composition occurred after editorial review of draft D-17, constraining its formation sequence.'],
'delta':[
'If that joint conclusion holds, the retained request-path pair provides a smaller sufficient reproduction for the next fixed-replay inquiry into deployment D-17.',
'If that joint conclusion holds, the retained background-path trio provides a smaller sufficient reproduction for the next fixed-replay inquiry into deployment D-17.',
'If that joint conclusion holds, the retained background-path trio is globally smallest for D-17’s latency failure, excluding all smaller untested combinations under replay.']}

def main():
 if (H/'hidden-design'/'revised-attempts.json').exists():raise SystemExit('Draft set already exists; preserve authoring evidence.')
 targets={x['mechanism_key']:x for x in json.loads((H/'targets.json').read_text())}; rows=[]
 for f in F:
  t=targets[f['key']]
  for position,index,badindex in [('local',3,2),('scope',2,1),('core',0,0)]:
   claims=[f['good'][0],*BRANCHES[f['key']][:2],'The report can use two separate numbered entries, one for each of the two examined branches.']
   claims[index]=BRANCHES[f['key']][2] if position=='scope' else f['bad'][badindex]
   mapping={k:f[k] for k in ['state','operation','signal','limit']};mapping['inference']='\n'.join(claims)
   mapping={k:mapping[k] for k in ['state','operation','signal','inference','limit']}
   cid='H1-'+secrets.token_hex(6);dump(H/'authoring-attempts'/f'{cid}.json',{'source':t['source'],'target':t['target'],'mapping':mapping})
   span=claims[index];start=mapping['inference'].index(span)
   rows.append({'case_id':cid,'mechanism_key':f['key'],'mechanism':t['source']['name'],'revision':'conditional_reporting_only','intended_position':position,'focal_object_definition':f['focal'],'intended_defective_slot':index,'intended_defective_span':{'source_field':'mapping.inference','exact_text':span,'start':start,'end':start+len(span)},'unsupported_span_chars':len(span),'token_estimate':math.ceil(len(span)/4),'unsupported_span_fraction':len(span)/len('\n'.join(mapping.values())),'focal_identity_check':dict(same_target=True,same_focal_object=True,same_signal_ownership=True,same_operation_ownership=True),'claim_graph_hypothesis':{'nodes':['S','C','A','B','L','Q1','Q2'],'edges':[['S','C'],['C','A'],['C','B'],['S','L'],['A','Q1'],['B','Q2']]},'warning':'Unapproved authoring attempt; not a final case or provider observation.'})
 for key in BRANCHES:
  g=[x for x in rows if x['mechanism_key']==key];print(key,[(x['intended_position'],x['unsupported_span_chars']) for x in g],max(x['unsupported_span_chars'] for x in g)/min(x['unsupported_span_chars'] for x in g))
 dump(H/'hidden-design/revised-attempts.json',rows)
if __name__=='__main__':main()
