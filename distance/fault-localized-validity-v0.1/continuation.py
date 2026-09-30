"""Additive G recovery: validate exact paragraph excerpts without changing observations.

Only a frozen-schema-valid signal_basis made entirely of verbatim, whole source
paragraphs in source order can pass the supplementary representation audit.
Original validation, terminal event, inputs, schema and response remain unchanged.
"""
import argparse,concurrent.futures,json,re,subprocess
from pathlib import Path
from unittest.mock import patch
import runner as r
import contracts as c
H=r.H;R=r.R;RT=r.RT; REC=H/'recovery/quote-representation'; CRT=RT/'continuation'
ORIGINAL_VALIDATE=r.validate_response

def quote_proof(value,candidate):
 blocks=value.split('\n\n');c.require(len(blocks)>1 and all(blocks),'Not multiple complete paragraphs')
 for field,text in candidate['mapping'].items():
  cursor=0; spans=[]
  for block in blocks:
   start=text.find(block,cursor);end=start+len(block)
   if start<0 or (start and text[start-2:start]!='\n\n') or (end<len(text) and text[end:end+2]!='\n\n'):break
   spans.append({'source_field':'mapping.'+field,'start':start,'end':end,'sha256':c.digest(block.encode())});cursor=end
  else:return {'representation':'ordered exact whole source paragraphs separated by blank lines','spans':spans,'inserted_source_words':0,'modified_source_words':0}
 raise ValueError('Signal basis is not a sequence of verbatim whole source paragraphs')

def validate(value,stage,identity):
 try:ORIGINAL_VALIDATE(value,stage,identity);return None
 except ValueError as exc:
  if stage!='claim-warrant' or str(exc)!='Signal basis must be an exact quotation':raise
  a=next(a for a in r.claims() if a['claim_id']==identity);candidate=r.candidate(a['case_id'])
  # All original schema, identity, conditional and uncertainty constraints remain.
  c.validate(value,stage,identity)
  relation=value['stated_empirical_relation']
  if relation is not None:c.require(any(relation in t for t in candidate['mapping'].values()),'Empirical relation absent')
  return quote_proof(value['signal_basis'],candidate)

def state_files():return sorted((CRT/'states').glob('*.json'))
def state():return c.read(state_files()[-1])['state'] if state_files() else None
def transition(s,reason):
 files=state_files();r.write(CRT/'states'/f'{len(files):04}.json',{'state':s,'reason':reason,'at':r.now(),'commit':r.head(),'previous_sha256':c.sha(files[-1]) if files else None})

def audit_incident():
 r.verify('claim-warrant',True);c.require(r.state()=='TERMINATED_MEASUREMENT','Original stop missing')
 dirs=sorted((RT/'runs/claim-warrant').glob('*'),key=lambda d:c.read(d/'attempt.json')['at'])
 c.require([d.name for d in dirs]==r.order('claim-warrant')[:7],'Unexpected attempts/prefix')
 failures=[];rows=[]
 for d in dirs:
  v=c.read(d/'validation.json');value=c.read(d/'response.json');proof=validate(value,'claim-warrant',d.name)
  events=[json.loads(x,object_pairs_hook=c.unique) for x in (d/'events.jsonl').read_text().splitlines() if x.strip()]
  c.require(r.audit_events(events)==v['metadata'],'Metadata drift')
  finals=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
  c.require(len(finals)==1 and finals[0].strip()==(d/'response.json').read_text().strip(),'Final mismatch')
  c.require((d/'prompt.txt').read_bytes()==r.packet('claim-warrant',d.name).read_bytes(),'Input changed')
  if v['status']!='valid':
   failures.append(d.name);c.require(proof is not None,'Not representation-only');c.require(v['error']=='ValueError: Signal basis must be an exact quotation','Unexpected error')
  rows.append({'identity':d.name,'original_validation':v,'supplementary_quote_proof':proof,'response_sha256':c.sha(d/'response.json'),'files':r.inventory(d.iterdir())})
 c.require(failures==['C-add735401d4d'],'Wrong failure identity')
 return {'classification':'recoverable_integrity_violation','kind':'source_quotation_metadata_representation','authority':'Experiment G handoff and docs/EXPERIMENT-RECOVERY-POLICY.md permit recovery with positive non-contamination evidence.','reason':'The exact-quotation rubric and wire schema do not require one contiguous paragraph. The returned signal_basis concatenates two verbatim complete source paragraphs in their original order. The harness applied an unstated single-substring restriction.','scientific_response_schema_valid':True,'scientific_classifier_unchanged':True,'model_answer_repaired_or_replaced':False,'input_packet_schema_model_context_changed':False,'rows':rows,'original_state_files':r.inventory((RT/'states').glob('*.json')),'resume_from':r.order('claim-warrant')[7],'retained_observations':7,'extra_provider_calls':0}

def record():
 result=audit_incident();r.write(REC/'incident.json',{'at':r.now(),'checkpoint':r.head(),**result})
 for row in result['rows']:
  d=RT/'runs/claim-warrant'/row['identity'];r.raw(REC/'responses'/f'{d.name}.json',(d/'response.json').read_bytes())
 transition('PAUSED_RECOVERABLE','Original terminal event retained; explicit source-paragraph proof establishes representation-only harness failure.')
 r.write(REC/'prepared.json',{'at':r.now(),'files':r.inventory([H/'continuation.py',H/'tests/test_continuation.py',REC/'incident.json',*list((REC/'responses').glob('*.json'))]),'scientific_prepared_sha256':c.sha(H/'claim-warrant-prepared.json'),'original_classifier_sha256':c.sha(H/'contracts.py'),'original_runner_sha256':c.sha(H/'runner.py')})

def gate():
 p=REC/'prepared.json';r.committed(p);r.hashes(c.read(p)['files']);r.committed(REC/'incident.json')
 recorded=c.read(REC/'incident.json');current=audit_incident_before_extension()
 c.require(current,'Incident verification failed')
 r.hashes(recorded['original_state_files'])
 for row in recorded['rows']:r.hashes(row['files']);validate(c.read(RT/'runs/claim-warrant'/row['identity']/'response.json'),'claim-warrant',row['identity'])
 c.require(c.sha(H/'claim-warrant-prepared.json')==c.read(p)['scientific_prepared_sha256'],'Scientific preparation changed')
 c.require(c.sha(H/'contracts.py')==c.read(p)['original_classifier_sha256'],'Classifier changed')
 c.require(c.sha(H/'runner.py')==c.read(p)['original_runner_sha256'],'Original harness changed')

def audit_incident_before_extension():
 data=c.read(REC/'incident.json')
 c.require(data['classification']=='recoverable_integrity_violation' and data['retained_observations']==7,'Wrong recovery class')
 row=next(x for x in data['rows'] if x['identity']=='C-add735401d4d')
 d=RT/'runs/claim-warrant'/row['identity']; proof=validate(c.read(d/'response.json'),'claim-warrant',row['identity'])
 c.require(proof==row['supplementary_quote_proof'],'Quote proof drift');return True

def preflight():
 gate();r.verify('claim-warrant',True);r.binary_check()
 commands=c.read(H/'historical-commands.json')+[['python','-B','-m','unittest','discover','-s',r.rel(H/'tests'),'-p','test_*.py']]
 def check(cmd):
  x=subprocess.run(cmd,cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600);return {'command':cmd,'exit_code':x.returncode,'output':x.stdout}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(check,commands))
 r.write(REC/'preflight.json',{'at':r.now(),'commit':r.head(),'provider_calls':0,'prepared_sha256':c.sha(REC/'prepared.json'),'checks':results})
 print(json.dumps({'checks':len(results),'failed':[x['command'] for x in results if x['exit_code']]}),flush=True)
 c.require(all(x['exit_code']==0 for x in results),'Recovery preflight failed');gate()

def effective_validation(stage,identity):
 d=RT/'runs'/stage/identity;v=c.read(d/'validation.json')
 if v['status']=='valid':return v
 c.require(stage=='claim-warrant' and identity=='C-add735401d4d','Nonrecoverable observation')
 data=c.read(REC/'incident.json');row=next(x for x in data['rows'] if x['identity']==identity)
 c.require(v==row['original_validation'],'Original validation changed')
 proof=validate(c.read(d/'response.json'),stage,identity);c.require(proof==row['supplementary_quote_proof'],'Proof mismatch')
 return {**v,'status':'valid','error':None,'supplementary_validation':r.rel(REC/'incident.json'),'original_status':'failed','original_error':v['error']}

def run(stage):
 c.require(state() in ['PAUSED_RECOVERABLE','COMPLETE'],'No implicit terminal/ambiguous resume')
 gate();r.verify(stage,True);p=REC/'preflight.json' if stage=='claim-warrant' else H/'review/ablation-preflight.json';r.committed(p)
 c.require(all(x['exit_code']==0 for x in c.read(p)['checks']),'Preflight failure')
 c.require(not r.git('status','--porcelain').strip(),'Unclean continuation')
 existing=[i for i in r.order(stage) if (RT/'runs'/stage/i).exists()]
 c.require(existing==r.order(stage)[:len(existing)],'Non-prefix reservations')
 for identity in existing:effective_validation(stage,identity)
 transition('RUNNING',stage+' after committed non-contamination evidence and preflight');initial=r.head()
 try:
  with patch.object(r,'validate_response',validate),patch.object(r,'transition',transition):
   for identity in r.order(stage)[len(existing):]:
    c.require(state()=='RUNNING' and r.head()==initial,'State/checkpoint changed');gate();r.verify(stage,True)
    r.execute(stage,identity)
    print(f'{stage} {r.order(stage).index(identity)+1}/{len(r.order(stage))} {identity}: valid',flush=True)
  transition('COMPLETE',stage)
 except Exception as exc:
  if state()=='RUNNING':transition('PAUSED_AMBIGUOUS',str(exc))
  raise

def freeze(stage):
 c.require(state()=='COMPLETE','Incomplete stage');r.verify(stage,True);gate();entries=[]
 for identity in r.order(stage):
  d=RT/'runs'/stage/identity;v=effective_validation(stage,identity);proof=validate(c.read(d/'response.json'),stage,identity)
  r.raw(H/'judgments'/stage/f'{identity}.json',(d/'response.json').read_bytes())
  entries.append({'identity':identity,'reservation':c.read(d/'reservation.json'),'validation':v,'original_validation':c.read(d/'validation.json'),'supplementary_quote_proof':proof,'response_sha256':c.sha(d/'response.json'),'files':r.inventory(d.iterdir())})
 r.write(H/f'{stage}-freeze.json',{'at':r.now(),'prepared_sha256':c.sha(H/f'{stage}-prepared.json'),'recovery_prepared_sha256':c.sha(REC/'prepared.json'),'runs':entries,'states':r.inventory((RT/'states').glob('*.json')),'continuation_states':r.inventory(state_files())})

def verify_results(stage,commit=False):
 fpath=H/f'{stage}-freeze.json';f=c.read(fpath)
 if commit:r.committed(fpath)
 c.require([x['identity'] for x in f['runs']]==r.order(stage),'Freeze coverage')
 sessions=[];previous=None
 for row in f['runs']:
  identity=row['identity'];d=RT/'runs'/stage/identity;r.hashes(row['files'])
  c.require(c.sha(H/'judgments'/stage/f'{identity}.json')==row['response_sha256']==c.sha(d/'response.json'),'Model response changed')
  c.require(effective_validation(stage,identity)==row['validation'],'Validation provenance')
  validate(c.read(d/'response.json'),stage,identity)
  x=row['reservation'];r.committed(r.packet(stage,identity),x['input_commit'])
  c.require(x['packet_sha256']==c.sha(r.packet(stage,identity))==c.sha(d/'prompt.txt'),'Packet drift')
  c.require(x['command']==r.command(x['working_directory'],d,stage) and x['configuration']==r.cfg(),'Config drift')
  events=[json.loads(line,object_pairs_hook=c.unique) for line in (d/'events.jsonl').read_text().splitlines() if line.strip()];meta=r.audit_events(events)
  c.require(meta==row['validation']['metadata'],'Metadata drift');sessions.append(meta['session_id'])
  c.require(previous is None or previous<=x['at'],'Overlapping calls');previous=row['validation']['finished_at']
 c.require(len(sessions)==len(set(sessions)),'Reused session')
 return {'stage':stage,'judgments':len(sessions),'unique_sessions':len(sessions),'retained_representation_failure':1 if stage=='claim-warrant' else 0,'replacement_observations':0}

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['record','preflight','run','freeze','verify-results','prepare-ablation']);p.add_argument('--stage',choices=r.STAGES,default='claim-warrant');a=p.parse_args()
 if a.action=='prepare-ablation':
  with patch.object(r,'verify_results',verify_results):r.prepare('ablation')
 elif a.action in ['record','preflight']:globals()[a.action]()
 elif a.action=='verify-results':print(json.dumps(verify_results(a.stage)))
 else:globals()[a.action](a.stage)
if __name__=='__main__':main()
