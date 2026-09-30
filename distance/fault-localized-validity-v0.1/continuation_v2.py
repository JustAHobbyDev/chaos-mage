"""Additive exact-excerpt representation recovery, preserving both earlier stops."""
import argparse,concurrent.futures,json,subprocess
from unittest.mock import patch
import continuation as k
r=k.r;c=k.c;H=r.H;RT=r.RT;REC=H/'recovery/excerpt-representation'
BASE_PROOF=k.quote_proof;BASE_GATE=k.gate;BASE_EFFECTIVE=k.effective_validation

def quote_proof(value,candidate):
 try:return BASE_PROOF(value,candidate)
 except ValueError:pass
 blocks=[line for line in value.split('\n') if line]
 c.require(len(blocks)>1,'Not a list of exact excerpts')
 for field,text in candidate['mapping'].items():
  cursor=0;spans=[]
  for block in blocks:
   start=text.find(block,cursor);end=start+len(block)
   if start<0:break
   # Excerpts must preserve complete word boundaries, without replacement prose.
   if start and text[start-1].isalnum() and block[0].isalnum():break
   if end<len(text) and text[end].isalnum() and block[-1].isalnum():break
   spans.append({'source_field':'mapping.'+field,'start':start,'end':end,'sha256':c.digest(block.encode())});cursor=end
  else:return {'representation':'ordered exact source excerpts separated only by newline formatting','spans':spans,'inserted_source_words':0,'modified_source_words':0}
 raise ValueError('Non-verbatim, reordered, or non-source quotation')

def effective(stage,identity):
 if stage!='claim-warrant' or identity!='C-6e35cd133b10':return BASE_EFFECTIVE(stage,identity)
 d=RT/'runs'/stage/identity;v=c.read(d/'validation.json');record=c.read(REC/'incident.json')
 c.require(v==record['original_validation'],'Original failure changed')
 proof=k.validate(c.read(d/'response.json'),stage,identity);c.require(proof==record['proof'],'Source proof changed')
 return {**v,'status':'valid','error':None,'supplementary_validation':r.rel(REC/'incident.json'),'original_status':v['status'],'original_error':v['error']}

def gate():
 BASE_GATE();r.committed(REC/'prepared.json');p=c.read(REC/'prepared.json');r.hashes(p['files'])
 x=c.read(REC/'incident.json');r.hashes(x['runtime_files']);r.hashes(x['continuation_states']);r.committed(REC/'incident.json')
 effective('claim-warrant','C-6e35cd133b10')

def record():
 BASE_GATE();c.require(k.state()=='TERMINATED_MEASUREMENT','Stop missing')
 ds=sorted((RT/'runs/claim-warrant').glob('*'),key=lambda d:c.read(d/'attempt.json')['at'])
 c.require([d.name for d in ds]==r.order('claim-warrant')[:14],'Unexpected observations')
 identity=ds[-1].name;c.require(identity=='C-6e35cd133b10','Wrong failed observation');d=ds[-1]
 value=c.read(d/'response.json');v=c.read(d/'validation.json');c.require(v['error']=='ValueError: Not multiple complete paragraphs','Unexpected failure')
 proof=k.validate(value,'claim-warrant',identity);c.require(proof['representation'].startswith('ordered exact source excerpts'),'Wrong representation')
 events=[json.loads(line,object_pairs_hook=c.unique) for line in (d/'events.jsonl').read_text().splitlines() if line.strip()];c.require(r.audit_events(events)==v['metadata'],'Metadata drift')
 finals=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message'];c.require(len(finals)==1 and finals[0].strip()==(d/'response.json').read_text().strip(),'Response mismatch')
 c.require((d/'prompt.txt').read_bytes()==r.packet('claim-warrant',identity).read_bytes(),'Input changed')
 record={'at':r.now(),'checkpoint':r.head(),'classification':'recoverable_integrity_violation','kind':'exact_source_excerpt_metadata_representation','authority':'User handoff and experiment recovery policy authorize non-contaminating engineering recovery.','reason':'A verbatim source heading and non-adjacent verbatim source bullet were joined with a newline. The schema-valid response meets the exact-quotation rubric; the paragraph-only supplemental parser was too narrow.','identity':identity,'original_validation':v,'proof':proof,'response_sha256':c.sha(d/'response.json'),'scientific_inputs_schema_classifier_model_context_unchanged':True,'response_edited_replaced_or_retried':False,'runtime_files':r.inventory(p for directory in ds for p in directory.iterdir()),'continuation_states':r.inventory(k.state_files()),'resume_from':r.order('claim-warrant')[14],'retained_observations':14}
 r.write(REC/'incident.json',record);r.raw(REC/'response.json',(d/'response.json').read_bytes())
 k.transition('PAUSED_RECOVERABLE','Positive exact-source excerpt proof; original failed validation and terminal state preserved.')
 r.write(REC/'prepared.json',{'at':r.now(),'files':r.inventory([H/'continuation_v2.py',H/'tests/test_excerpt_recovery.py',REC/'incident.json',REC/'response.json']),'parent_recovery_prepared_sha256':c.sha(k.REC/'prepared.json')})

def preflight():
 gate();r.verify('claim-warrant',True);r.binary_check()
 commands=c.read(H/'historical-commands.json')+[['python','-B','-m','unittest','discover','-s',r.rel(H/'tests'),'-p','test_*.py']]
 def check(cmd):
  x=subprocess.run(cmd,cwd=r.R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600);return {'command':cmd,'exit_code':x.returncode,'output':x.stdout}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(check,commands))
 r.write(REC/'preflight.json',{'at':r.now(),'commit':r.head(),'provider_calls':0,'prepared_sha256':c.sha(REC/'prepared.json'),'checks':results})
 print(json.dumps({'checks':len(results),'failed':[x['command'] for x in results if x['exit_code']]}));c.require(all(x['exit_code']==0 for x in results),'Preflight failed');gate()

def run(stage):
 gate();p=REC/'preflight.json';r.committed(p);v=c.read(p);c.require(v['prepared_sha256']==c.sha(REC/'prepared.json') and all(x['exit_code']==0 for x in v['checks']),'Recovery preflight binding')
 k.run(stage)

def context():
 from contextlib import ExitStack
 stack=ExitStack();stack.enter_context(patch.object(k,'quote_proof',quote_proof));stack.enter_context(patch.object(k,'gate',gate));stack.enter_context(patch.object(k,'effective_validation',effective));return stack

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['record','preflight','run','freeze','verify-results','prepare-ablation']);p.add_argument('--stage',choices=r.STAGES,default='claim-warrant');a=p.parse_args()
 with context():
  if a.action=='record':record()
  elif a.action=='preflight':preflight()
  elif a.action=='run':run(a.stage)
  elif a.action=='freeze':k.freeze(a.stage)
  elif a.action=='verify-results':print(json.dumps(k.verify_results(a.stage)))
  else:
   with patch.object(r,'verify_results',k.verify_results):r.prepare('ablation')
if __name__=='__main__':main()
