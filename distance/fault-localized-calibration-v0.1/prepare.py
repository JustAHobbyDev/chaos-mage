"""Exact operator extraction, complete sentence audit, opaque shuffled scheduling."""
import json,re,secrets,random,subprocess
from pathlib import Path
import runner as r
import contracts as c
H=r.H

def units(text):
 for match in re.finditer(r'[^\n]+',text):
  # Sentence boundaries are explicit in these authored texts; no abbreviations/decimal numerals.
  part=match.group()
  for sentence in re.finditer(r'.+?(?:\.(?=\s|$)|$)',part):
   s=sentence.group();lead=len(s)-len(s.lstrip());s=s.strip()
   if s:yield match.start()+sentence.start()+lead,s

def main():
 cases=[p.stem for p in sorted((H/'cases').glob('*.json'))];random.SystemRandom().shuffle(cases)
 atoms=[];audit=[]
 compatibility=['the stable matrix pattern conflicts with post-evaluation alteration of recorded scores',
 'the stable matrix pattern conflicts with bidder-specific authorship of that requirement',
 'this pattern fits scheduled release better than continuously exhausted capacity',
 'this pattern fits case rework better than a uniform approval-stage queue']
 for cid in cases:
  mapping=r.candidate(cid)['mapping']
  for field,text in mapping.items():
   for start,parent in units(text):
    selected=[parent] if field=='inference' else [x for x in compatibility if field=='signal' and x in parent]
    ids=[]
    for span in selected:
     identity='C-'+secrets.token_hex(6);offset=start+parent.index(span);ids.append(identity)
     atoms.append({'claim_id':identity,'case_id':cid,'source_field':'mapping.'+field,'parent_start':start,'parent_end':start+len(parent),'exact_parent_text':parent,'span_start':offset,'span_end':offset+len(span),'exact_claim_span':span,'local_context':{'interpretation':'Retain full original parent antecedents and limits; panel ownership is fixed by state.'},'downstream_references':[]})
    reason='Exact explicit inference, retaining full sentence context.' if ids else {'state':'Stipulated case setting, panel assignment or scope; no signal-to-conclusion assertion.','operation':'Procedure or explicitly conditional action directive; not an assertion that its evidential antecedent holds.','signal':'Stipulated observed outcome or reliability check; explicit compatibility inferences are separately extracted.','limit':'Execution assumption or restriction on interpretation, not a new target conclusion.'}.get(field,'Non-inferential text.')
    audit.append({'case_id':cid,'source_field':'mapping.'+field,'start':start,'end':start+len(parent),'exact_text':parent,'claim_ids':ids,'disposition':'represented' if ids else 'non_inferential','operator_reason':reason})
 random.SystemRandom().shuffle(atoms)
 r.write(H/'claims/inventory.json',atoms);r.write(H/'claims/extraction-audit.json',audit)
 cfg=c.read(H.parent/'fault-localized-validity-v0.1/execution-config.json')
 cfg.update(scheduler='Sequential frozen opaque Experiment H order',authorized_claim_measurements=len(atoms),authorized_ablation_measurements='one per case with UNSUPPORTED claims, maximum 24')
 r.write(H/'execution-config.json',cfg)
 commands=c.read(H.parent/'fault-localized-validity-v0.1/historical-commands.json')
 for cmd in commands:
  if 'distance/fault-localized-validity-v0.1/historical.py' in cmd:cmd[2]='distance/fault-localized-calibration-v0.1/historical.py'
 commands += [['python','-B','-m','unittest','discover','-s','distance/fault-localized-validity-v0.1/tests','-p','test_*.py'],['python','-B','distance/fault-localized-validity-v0.1/publication.py','verify']]
 r.write(H/'historical-commands.json',commands)
 manifest={'starting_sha':c.read(H/'preservation.json')['baseline'],'policy_checkpoint':r.git('rev-parse','f0eae93').decode().strip(),'primary_checkpoint':r.git('rev-parse','5967627').decode().strip(),'controls_checkpoint':r.git('rev-parse','dc77fa8').decode().strip(),'case_order':cases,'claim_order':[a['claim_id'] for a in atoms],'case_files':r.inventory((H/'cases').glob('*.json')),'hidden_files':r.inventory((H/'hidden-design').glob('*.json')),'claims_by_case':{cid:sum(a['case_id']==cid for a in atoms) for cid in cases},'uncertain_ablation':False,'provider_packet_allowlist':['source','target','mapping','atomic_claim or unsupported_claims and ablated_mapping'],'extraction':'all five fields audited; explicit inference sentences and embedded compatibility assertions; no operator warrant labels'}
 r.write(H/'manifest.json',manifest)
 for a in atoms:r.raw(r.packet('claim-warrant',a['claim_id']),r.reconstructed_claim_packet(a).encode())
 links=[]
 for cid in cases:
  d=c.read(H/'hidden-design'/f'{cid}.json')
  for defect in d['unsupported_claims']:
   matches=[a['claim_id'] for a in atoms if a['case_id']==cid and a['exact_claim_span']==defect['exact_text']]
   c.require(len(matches)==1,'Intended claim not exactly represented')
   links.append({'case_id':cid,'design_node':defect['id'],'claim_id':matches[0]})
 r.write(H/'claims/hidden-design-links.json',links)
 print(json.dumps({'cases':len(cases),'claims':len(atoms),'audit_units':len(audit)}))
if __name__=='__main__':main()
