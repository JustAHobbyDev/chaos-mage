"""Operator-authored exact-span extraction; no warrant decisions in this file."""
import hashlib, json, re, subprocess, uuid
from pathlib import Path
H=Path(__file__).resolve().parent; R=H.parent.parent
CASES=['E006','E022','E030']
BASE='ac79a379938ae07d5a0a5a65e14c6145b60ed08b'
POLICY='2dc0ae0'
def read(p): return json.loads(p.read_text())
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f: json.dump(v,f,indent=2,ensure_ascii=False); f.write('\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def units(text):
 # Preserve punctuation/offsets; paragraph and sentence boundaries, including lists.
 return [m for m in re.finditer(r'.+?(?=\n+|(?<=[.!?])\s+(?=[A-Z])|(?<=\.) (?=\d+\.)|\Z)',text,re.S)]
# Indexes refer to lossless sentence units. None selects the full unit.
SELECTION={
'E006':{
'inference':{0:None,1:None,3:None,4:None,6:['the process was irregular','the records held do not settle whether that was deliberate'],8:None,9:None,10:None},
'operation':{14:None,32:None},
'signal':{3:None,4:None,5:None,6:None,7:['A full, contemporaneous evaluation record with consistent independent scoring would be inconsistent with the scoring-manipulation form of H1','but not with specification tailoring'],8:None,10:['Rows where the two raters differ','where removing one item changes the surviving set']}},
'E022':{
'inference':{1:['the handoff holds items in fixed waiting (scheduled review, batch release, transfer latency)','not a shortage of processing capacity'],2:['the stage is capacity-limited at the tested load','delay accumulates there'],3:['a stage that absorbs change through a large backlog','improvements there take long to appear end to end'],4:None,5:['Oscillation without such a match','with items re-entering earlier stages'],6:None,7:None,8:None,10:['Delay accumulates at the stages showing the longest dead time','non-settling queues','the slowest settling'],11:None,13:None},
'operation':{15:['keep the record as evidence of saturation or non-settling at that operating point.']},
'signal':{}},
'E030':{
'inference':{0:['the arrangement examined is the arrangement the author left','its order can be used as evidence of authorial assembly'],1:None,2:['supported by contemporaneous record','supported by reconstruction from trace','unsupported across a break'],3:["The sequence offered as best explaining the draft is the one that leaves the fewest breaks and contradictions"],4:['A break weakens only the claims that depend on that transition','at each break the competing assembly sequences are retained rather than reduced to one.'],5:None},
'operation':{},
'signal':{1:['stubs','gaps in numbering indicating removed leaves']}}
}
EXCLUSIONS={
('E006','inference',2):'Heading introducing output taxonomy, not a separate signal-to-claim assertion.',
('E006','inference',5):'Instruction to name survivors together; no additional inference.',
('E006','inference',7):'Instruction to label allegations and gaps separately; no additional inference.',
('E022','inference',0):'Heading bounding all following claims as constraints, not unique identification.',
('E022','inference',9):'Heading introducing target-level inferences.',
('E022','inference',12):'Scope qualification retained in every original mapping; no separate evidential consequence.'}
def main():
 assert subprocess.check_output(['git','show',POLICY+':distance/fault-localized-validity-v0.1/CORE-INVALIDITY.md'],cwd=R)==(H/'CORE-INVALIDITY.md').read_bytes()
 manifest={'starting_sha':BASE,'policy_checkpoint':subprocess.check_output(['git','rev-parse',POLICY],cwd=R,text=True).strip(),'cases':[],'claim_order':[],'extraction':'operator-authored exhaustive sentence audit and exact contiguous atomic spans; no operator blinding','policy_access_sequence':'policy committed before opening detailed mappings in this thread','uncertain_ablation':False}
 claims=[]; audit=[]
 for cid in CASES:
  src=R/'distance/anti-collapse-natural-recovery-v0.1'; gp=src/'generations'/f'{cid}.json'; ip=src/'generation-inputs'/f'{cid}.json'
  g=read(gp); inp=read(ip); candidate={'source':inp['source'],'target':inp['target'],'mapping':g['mapping']}
  write(H/'claims'/f'{cid}-source.json',candidate)
  manifest['cases'].append({'case_id':cid,'generation':{'path':str(gp.relative_to(R)),'sha256':sha(gp)},'input':{'path':str(ip.relative_to(R)),'sha256':sha(ip)}})
  for field in ['inference','operation','signal']:
   txt=g['mapping'][field]; ms=units(txt)
   # Ensure index scheme exactly matches the operator-reviewed segmentation.
   expected=re.split(r'\n+|(?<=[.!?])\s+(?=[A-Z])|(?<=\.) (?=\d+\.)',txt)
   normalized=[(m.start()+len(m[0])-len(m[0].lstrip()),m[0].strip()) for m in ms if m[0].strip()]
   assert [s for _,s in normalized]==expected,(cid,field)
   for idx,(start,parent) in enumerate(normalized):
    selected=idx in SELECTION[cid][field]; ids=[]
    if selected:
     spans=SELECTION[cid][field][idx] or [parent]
     for n,span in enumerate(spans):
      assert parent.count(span)==1,(cid,span)
      identity='C-'+uuid.uuid5(uuid.NAMESPACE_URL,f'chaos-mage/experiment-g/{cid}/{field}/{idx}/{n}').hex[:12]
      a=start+parent.index(span); b=a+len(span); assert txt[a:b]==span
      # Candidate downstream references are textual context, not causal verdicts.
      refs=[]
      if field=='inference':
       refs=[{'source_field':'mapping.inference','exact_text':s,'start':p,'end':p+len(s),'relationship':'subsequent inference-field text; dependency not yet judged'} for p,s in normalized[idx+1:]]
      else:
       refs=[{'source_field':'mapping.inference','exact_text':g['mapping']['inference'],'start':0,'end':len(g['mapping']['inference']),'relationship':'subsequent inference field; dependency not yet judged'}]
      claim={'claim_id':identity,'case_id':cid,'source_field':'mapping.'+field,'parent_start':start,'parent_end':start+len(parent),'exact_parent_text':parent,'span_start':a,'span_end':b,'exact_claim_span':span,'local_context':{'preceding_unit':normalized[idx-1][1] if idx else None,'following_unit':normalized[idx+1][1] if idx+1<len(normalized) else None,'interpretation':'Read exact span under all parent antecedents, modal qualifiers, and original mapping limits.'},'downstream_references':refs}
      claims.append(claim); ids.append(identity)
    reason=('Full unit retained.' if selected and len(ids)==1 and (SELECTION[cid][field][idx] is None) else 'Independent inferential consequences split; original parent supplies antecedents and modality.') if selected else EXCLUSIONS.get((cid,field,idx),'Procedure, heading, observation/feature definition, or recordkeeping description; no separate asserted evidential consequence. All remains in original mapping context.')
    audit.append({'case_id':cid,'source_field':'mapping.'+field,'unit_index':idx,'start':start,'end':start+len(parent),'exact_text':parent,'disposition':'represented' if selected else 'non_inferential','claim_ids':ids,'operator_reason':reason})
 write(H/'claims/inventory.json',claims); write(H/'claims/extraction-audit.json',audit)
 for c in claims:
  candidate=read(H/'claims'/f'{c["case_id"]}-source.json')
  body={**candidate,'atomic_claim':{k:c[k] for k in ['claim_id','source_field','exact_parent_text','exact_claim_span']}}
  packet=(H/'CLAIM-WARRANT.md').read_text()+'\nCASE PACKET\n'+json.dumps(body,indent=2,ensure_ascii=False)+'\n'
  (H/'packets/claim-warrant'/f'{c["claim_id"]}.txt').write_text(packet)
 manifest['claim_order']=[c['claim_id'] for c in claims]
 manifest['claims_by_case']={cid:sum(c['case_id']==cid for c in claims) for cid in CASES}
 write(H/'manifest.json',manifest)
 # Entire pre-G tracked corpus except new sibling/doc: immutable historical preservation.
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=R,text=True).splitlines()
 write(H/'preservation.json',{'baseline':BASE,'files':{p:sha(R/p) for p in paths}})
 print(json.dumps(manifest['claims_by_case']))
if __name__=='__main__': main()
