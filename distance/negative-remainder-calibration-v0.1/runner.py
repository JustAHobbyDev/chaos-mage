#!/usr/bin/env python3
"""H.3-only scheduler: exact immutable inputs, isolated observations, deletion-only ablation."""
import argparse, concurrent.futures, copy, importlib.util, json, os, re, signal, subprocess, tempfile
from datetime import datetime,timezone
from pathlib import Path
import contracts as c
H=Path(__file__).resolve().parent; R=H.parent.parent; RT=R/'.runtime/negative-remainder-calibration-v0.1'
STAGES=['claim-warrant','artifact']
def now(): return datetime.now(timezone.utc).isoformat()
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
def head(): return git('rev-parse','HEAD').decode().strip()
def rel(p): return str(p.relative_to(R))
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f: json.dump(v,f,indent=2,ensure_ascii=False); f.write('\n')
def raw(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
def inventory(paths): return {rel(p):c.sha(p) for p in sorted(paths) if p.is_file() and '__pycache__' not in p.parts}
def hashes(files):
 for p,h in files.items(): c.require(c.sha(R/p)==h,'Frozen bytes changed: '+p)
def committed(p,commit='HEAD'): c.require(git('show',f'{commit}:{rel(p)}')==p.read_bytes(),'Uncommitted input '+rel(p))
def claims(): return c.read(H/'claims/inventory.json')
def candidate(cid): return c.read(H/'cases'/f'{cid}.json')
def order(stage): return c.read(H/'manifest.json')['claim_order'] if stage=='claim-warrant' else c.read(H/'artifact-manifest.json')['case_order']
def packet(stage,identity): return H/'packets'/stage/f'{identity}.txt'
def cfg(): return c.read(H/'execution-config.json')
def clean_env(): return {k:v for k,v in os.environ.items() if not k.startswith(('CODEX_','CLAUDE_','ANTHROPIC_','OPENAI_','AZURE_OPENAI_','GEMINI_','GOOGLE_GENAI_')) and k not in ('CLAUDECODE','MODEL_PROVIDER','MODEL','LLM_MODEL')}
def binary_check():
 x=cfg(); cli=x['families']['A']['cli']
 c.require(x['families']=={'A':{'cli':cli,'requested_model':'gpt-6-astra','effort':'high'}},'Only Astra/high')
 c.require(c.sha(cli)==x['executable_sha256']['A'],'CLI changed')
 c.require(c.sha(x['native_executable']['path'])==x['native_executable']['sha256'],'Native CLI changed')
 version=subprocess.check_output([cli,'--version'],text=True).strip(); c.require(version=='codex-cli 0.157.1','CLI version'); return version

def command(cwd,d,stage):
 cmd=[cfg()['families']['A']['cli'],'exec','--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check','--sandbox','read-only','--json','--color','never','--cd',str(cwd),'--model','gpt-6-astra','-c','model_reasoning_effort="high"','-c','project_doc_max_bytes=0','-c','web_search="disabled"','--output-schema',str(H/'schemas'/f'{stage}.schema.json'),'--output-last-message',str(d/'response.json')]
 for f in cfg()['codex_disabled_features']: cmd+=['--disable',f]
 return cmd+['-']

def audit_events(events):
 starts=[e for e in events if e.get('type')=='thread.started']
 c.require(len(starts)==1,'Expected one fresh session')
 c.require(sum(e.get('type')=='turn.completed' for e in events)==1,'Incomplete turn')
 c.require(not any(e.get('type') in ('error','turn.failed') for e in events),'Provider error')
 c.require(all(e['item'].get('type') in ('agent_message','reasoning') for e in events if 'item' in e),'Tool activity')
 found=[]
 def walk(v,path):
  if isinstance(v,dict):
   for k,x in v.items():
    if k in ('model','model_id','model_name') and isinstance(x,str): found.append({'value':x,'source':path+'.'+k})
    c.require(not ('fallback' in k.lower() and x),'Fallback event'); walk(x,path+'.'+k)
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,f'{path}[{i}]')
 walk(events,'events'); c.require(all(x['value']=='gpt-6-astra' for x in found),'Model substitution')
 return {'session_id':starts[0]['thread_id'],'returned_model_identifiers':sorted({x['value'] for x in found}),'model_metadata_provenance':found,'verified_served_snapshot':None,'usage':[e.get('usage') for e in events if e.get('type')=='turn.completed'],'internal_retry_events':[e for e in events if e.get('subtype')=='api_retry'],'retry_observability':'No harness retries. Unexposed provider retries cannot be ruled out.'}

def reconstructed_claim_packet(a):
 body={**candidate(a['case_id']),'atomic_claim':{k:a[k] for k in ['claim_id','source_field','exact_parent_text','exact_claim_span']}}
 return (H/'CLAIM-WARRANT.md').read_text()+'\nCASE PACKET\n'+json.dumps(body,indent=2,ensure_ascii=False)+'\n'

def delete_claims(mapping,atoms):
 result=dict(mapping)
 for f in mapping:
  rows=sorted([a for a in atoms if a['source_field']=='mapping.'+f],key=lambda a:a['span_start'],reverse=True)
  previous=len(mapping[f])
  for a in rows:
   x,y=a['span_start'],a['span_end']; c.require(y<=previous and mapping[f][x:y]==a['exact_claim_span'],'Invalid/overlapping deletion')
   result[f]=result[f][:x]+f'[DELETED {a["claim_id"]}]'+result[f][y:]; previous=x
 return result

def unsupported(cid): return [a for a in claims() if a['case_id']==cid and c.read(H/'judgments/claim-warrant'/f'{a["claim_id"]}.json')['status']=='UNSUPPORTED']
def ablation_body(cid):
 original=candidate(cid); atoms=unsupported(cid)
 return {'case_id':cid,**original,'unsupported_claims':[{k:a[k] for k in ['claim_id','source_field','exact_parent_text','exact_claim_span']} for a in atoms],'ablated_mapping':delete_claims(original['mapping'],atoms),'candidate_remainders':c.read(H/'remainder-candidates'/f'{cid}.json')['candidates']}
def ablation_text(cid):
 return (H/'VIABILITY.md').read_text()+'\nJudge this deletion counterfactual using only the supplied mapping and source. Return remainder_viability in the supplied schema. Copy each frozen candidate inference and source_spans exactly, mark origin frozen, and assess all four properties. Separately marked judge_added candidates must cite exact surviving mapping excerpts. Candidate inventory text is not a viability judgment. Citations use original mapping field names and separate exact contiguous excerpts, excluding deleted spans. Audit negative constraints and useful next inquiries, but do not invent repaired or replacement inferences. A valid source result about something other than the exact target is insufficient. Strongest inference text/spans must copy one assessed candidate, or be null if none exists. Empty deletion sets are valid: assess original scope. Diagnostic disagreements require structural_conflict explanation; unresolved contradictions mean uncertainty. Absent conflicts have present=false,resolved=true.\nCASE PACKET\n'+json.dumps(ablation_body(cid),indent=2,ensure_ascii=False)+'\n'
def verify(stage=None,commit=False):
 import pipeline
 return pipeline.verify(stage,commit)
def prepare(stage):
 import pipeline
 return pipeline.prepare(stage)

def state():
 files=sorted((RT/'states').glob('*.json')); return c.read(files[-1])['state'] if files else None

def transition(s,reason):
 files=sorted((RT/'states').glob('*.json'))
 write(RT/'states'/f'{len(files):04}.json',{'state':s,'reason':reason,'at':now(),'commit':head(),'previous_sha256':c.sha(files[-1]) if files else None})

def preflight(stage):
 import historical
 verify(stage,True); version=binary_check()
 results=historical.all_checks()
 cmd=['python','-B','-m','unittest','discover','-s',rel(H/'tests'),'-p','test_*.py']
 result=subprocess.run(cmd,cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
 results.append({'command':cmd,'exit_code':result.returncode,'output':result.stdout})
 write(H/'review'/f'{stage}-preflight.json',{'at':now(),'input_commit':head(),'prepared_sha256':c.sha(H/f'{stage}-prepared.json'),'cli_version':version,'provider_calls':0,'checks':results})
 for row in results:
  print(row['exit_code'],' '.join(row['command']),flush=True)
  if row['exit_code']:print(row['output'],flush=True)
 c.require(all(r['exit_code']==0 for r in results),'Preflight failed')
 verify(stage,True)

def validate_response(value,stage,identity):
 if stage=='claim-warrant':
  a=next(a for a in claims() if a['claim_id']==identity); c.validate(value,stage,identity,candidate(a['case_id']))
 else:c.validate(value,stage,identity,candidate(identity),unsupported=unsupported(identity),frozen_candidates=c.read(H/'remainder-candidates'/f'{identity}.json')['candidates'])

def execute(stage,identity):
 d=RT/'runs'/stage/identity; d.mkdir(parents=True,exist_ok=False)
 write(d/'attempt.json',{'at':now(),'stage':stage,'identity':identity,'input_commit':head(),'harness_attempt':1})
 prompt=packet(stage,identity).read_bytes(); raw(d/'prompt.txt',prompt); launched=False; metadata=None
 try:
  version=binary_check()
  with tempfile.TemporaryDirectory(prefix='h3-isolated-') as cwd:
   c.require(not list(Path(cwd).iterdir()),'Working directory not empty')
   cmd=command(cwd,d,stage)
   write(d/'reservation.json',{'at':now(),'input_commit':head(),'identity':identity,'stage':stage,'packet_sha256':c.digest(prompt),'schema_sha256':c.sha(H/'schemas'/f'{stage}.schema.json'),'configuration':cfg(),'cli_version':version,'command':cmd,'working_directory':cwd,'working_directory_initially_empty':True,'requested_session':'ephemeral','environment_policy':'Provider overrides and parent session markers removed; existing on-disk auth only.'})
   with (d/'events.jsonl').open('x') as out,(d/'stderr.txt').open('x') as err:
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=out,stderr=err,cwd=cwd,env=clean_env(),start_new_session=True); launched=True
    write(d/'process.json',{'pid':process.pid,'parent_pid':os.getpid(),'launched_at':now()})
    try:process.communicate(prompt,timeout=900)
    except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL); process.wait(); raise
   write(d/'exit.json',{'returncode':process.returncode,'at':now()}); c.require(process.returncode==0,'CLI nonzero exit')
   events=[json.loads(line,object_pairs_hook=c.unique) for line in (d/'events.jsonl').read_text().splitlines() if line.strip()]
   metadata=audit_events(events)
   for prev in (RT/'runs').rglob('validation.json'):
    old=c.read(prev).get('metadata'); c.require(not old or old['session_id']!=metadata['session_id'],'Session reused')
   finals=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
   c.require(len(finals)==1 and finals[0].strip()==(d/'response.json').read_text().strip(),'Final stream mismatch')
   validate_response(c.read(d/'response.json'),stage,identity)
  write(d/'validation.json',{'status':'valid','error':None,'finished_at':now(),'metadata':metadata})
 except Exception as e:
  write(d/'validation.json',{'status':'failed','error':type(e).__name__+': '+str(e),'finished_at':now(),'metadata':metadata})
  transition('TERMINATED_MEASUREMENT' if launched else 'PAUSED_AMBIGUOUS',str(e)); raise
 return d

def run(stage):
 c.require(not (H/'final-runtime-freeze.json').exists(),'Experiment already final'); c.require(state() in (None,'RUNNING','COMPLETE'),'Paused/terminated: recovery evidence required; no automatic resume')
 c.require(not list((RT/'runs'/stage).glob('*')),'Stage has reservations; no automatic retry/rescheduling')
 try:
  verify(stage,True); p=H/'review'/f'{stage}-preflight.json'; committed(p); v=c.read(p)
  c.require(v['prepared_sha256']==c.sha(H/f'{stage}-prepared.json') and all(x['exit_code']==0 for x in v['checks']),'Preflight binding')
  c.require(not git('status','--porcelain').strip(),'Unclean continuation')
  binary_check(); initial=head(); transition('RUNNING',stage)
  for index,identity in enumerate(order(stage),1):
   c.require(state()=='RUNNING' and head()==initial,'State/checkpoint changed'); verify(stage,True)
   execute(stage,identity); print(f'{stage} {index}/{len(order(stage))} {identity}: valid',flush=True)
  transition('COMPLETE',stage)
 except Exception as e:
  if state() not in ('TERMINATED_MEASUREMENT','TERMINATED_LINEAGE','PAUSED_AMBIGUOUS','PAUSED_RECOVERABLE'): transition('PAUSED_AMBIGUOUS',str(e))
  raise

def freeze(stage):
 c.require(state()=='COMPLETE','Incomplete/paused stage'); verify(stage,True); entries=[]
 for identity in order(stage):
  d=RT/'runs'/stage/identity; validation=c.read(d/'validation.json'); c.require(validation['status']=='valid','Failed response')
  validate_response(c.read(d/'response.json'),stage,identity)
  raw(H/'judgments'/stage/f'{identity}.json',(d/'response.json').read_bytes())
  entries.append({'identity':identity,'reservation':c.read(d/'reservation.json'),'validation':validation,'response_sha256':c.sha(d/'response.json'),'files':inventory(d.iterdir())})
 write(H/f'{stage}-freeze.json',{'at':now(),'prepared_sha256':c.sha(H/f'{stage}-prepared.json'),'runs':entries,'states':inventory((RT/'states').glob('*.json'))})

def verify_results(stage,commit=False):
 freeze=H/f'{stage}-freeze.json'; f=c.read(freeze)
 if commit:committed(freeze)
 c.require([e['identity'] for e in f['runs']]==order(stage),'Frozen result coverage')
 sessions=[]; previous=None
 for entry in f['runs']:
  identity=entry['identity']; hashes(entry['files']); d=RT/'runs'/stage/identity
  response=H/'judgments'/stage/f'{identity}.json'
  c.require(c.sha(response)==entry['response_sha256'],'Published response changed')
  c.require(response.read_bytes()==(d/'response.json').read_bytes(),'Model answer replaced')
  validate_response(c.read(response),stage,identity)
  r=entry['reservation']; c.require(r['packet_sha256']==c.sha(packet(stage,identity))==c.sha(d/'prompt.txt'),'Packet lineage')
  committed(packet(stage,identity),r['input_commit'])
  c.require(r['command']==command(r['working_directory'],d,stage) and r['configuration']==cfg(),'Execution configuration lineage')
  events=[json.loads(s,object_pairs_hook=c.unique) for s in (d/'events.jsonl').read_text().splitlines() if s.strip()]
  meta=audit_events(events); c.require(meta==entry['validation']['metadata'],'Event audit drift'); sessions.append(meta['session_id'])
  c.require(previous is None or previous<=r['at'],'Overlapping sessions'); previous=entry['validation']['finished_at']
 c.require(len(sessions)==len(set(sessions)),'Duplicate sessions')
 return {'stage':stage,'judgments':len(sessions),'unique_sessions':len(sessions)}

def failure():
 write(H/'failure-freeze.json',{'at':now(),'state':state(),'runtime_files':inventory(RT.rglob('*')),'policy':'Incomplete; sent observations cannot be retried or replaced.'})

def main():
 p=argparse.ArgumentParser(); p.add_argument('action',choices=['prepare','preflight','run','freeze','verify','verify-results','freeze-failure']); p.add_argument('--stage',choices=STAGES,default=STAGES[0]); a=p.parse_args()
 if a.action=='verify': print(json.dumps(verify()))
 elif a.action=='verify-results':print(json.dumps(verify_results(a.stage)))
 elif a.action=='freeze-failure':failure()
 else:globals()[a.action](a.stage)
if __name__=='__main__': main()
