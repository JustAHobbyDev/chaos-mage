#!/usr/bin/env python3
"""H8: offline by default. Fixed slots, immutable observations, no retries."""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import tarfile
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile

from jsonschema import Draft202012Validator

H=Path(__file__).resolve().parent
R=H.parents[1]
RT=R/'.runtime/target-impact-v0.1'
sys.path.insert(0,str(R/'scripts'))
import experiment_budget as budget
import codex_usage as usage
BASE='c62b622b69ed900b9debcc9e41e133536287be59'
BRANCH='experiment-h8-target-impact'
CATEGORIES=['PROBLEM_REPRESENTATION_CHANGE','INQUIRY_CHANGE','PRIORITY_CHANGE','ACTION_CHANGE','DECISION_RULE_CHANGE','CONSTRAINT_CHANGE']
BANNED=re.compile(r'\b(?:ACH|Analysis of Competing Hypotheses|crossdating|dendrochronology|chain[ -]of[ -]custody|forensics|Chaos[ -]Mage|source ontology|source instrument)\b',re.I)


def require(ok,message):
 if not ok: raise ValueError(message)
def unique(pairs):
 d={}
 for k,v in pairs:
  require(k not in d,'Duplicate JSON key: '+k); d[k]=v
 return d
def read(p): return json.loads(p.read_text(),object_pairs_hook=unique)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f: json.dump(x,f,indent=2); f.write('\n')
def raw(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f: f.write(b)
def git(*args): return subprocess.check_output(['git',*args],cwd=R).decode().strip()
def head(): return git('rev-parse','HEAD')
def inventory(paths): return {str(p.relative_to(R)):sha(p) for p in sorted(paths) if p.is_file()}
def manifest(): return read(H/'manifest.json')
def config(): return read(H/'execution-config.json')
def slots(stage): return manifest()['stage_order'][stage]
def packet(stage,uid): return H/f'{stage}-packets'/f'{uid}.txt'
def response(stage,uid): return H/'responses'/stage/f'{uid}.json' if stage!='impact' else H/'impact-judgments'/f'{uid}.json'
def terminal(stage,uid): return response(stage,uid).exists() or (H/'review/quarantines'/f'{stage}--{uid}.json').exists()
def state():
 ps=sorted((RT/'states').glob('*.json'))
 return read(ps[-1])['state'] if ps else 'READY'
def transition(s,reason):
 ps=sorted((RT/'states').glob('*.json'))
 write(RT/'states'/f'{len(ps):04}.json',{'state':s,'reason':reason,'at':usage.stamp(),'commit':head(),'previous_sha256':sha(ps[-1]) if ps else None})
def freeze(name,paths):
 write(H/f'{name}-freeze.json',{'execution_parent':head(),'files':inventory(paths)})
def freeze_initial():
 require(head()==BASE or git('merge-base',BASE,'HEAD')==BASE,'Wrong ancestry')
 files=git('ls-tree','-r','--name-only',BASE).splitlines()
 archive=subprocess.check_output(['git','archive',BASE],cwd=R)
 with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
  hashes={m.name:hashlib.sha256(tf.extractfile(m).read()).hexdigest() for m in tf.getmembers() if m.isfile()}
 require(set(hashes)==set(files),'Archive did not cover all historical files')
 write(H/'preservation.json',{'base_sha':BASE,'files':hashes})
 paths=list(H.rglob('*'))+[R/'docs/PROBLEM_FRAMES-target-impact-v0.1.md']
 freeze('initial',paths)
 plan={'version':1,'experiment_id':'h8-target-impact-v0.1','description':'Fixed H8: 2 native, 3 augmented, 3 blinded judgments. No retries.',
  'execution_fingerprint':budget.digest(read(H/'initial-freeze.json')['files']),'execution_allowed':True,
  'stages':[{'id':s,'sessions':len(slots(s)),'estimated_cost_usd':None,
   'estimate_basis':'No matched itemized billing evidence for H8; unknown is not zero.',
   'usage_profile':f'astra-high-h8-{s}-v1'} for s in ('native','augmented','impact')]}
 write(H/'budget-plan.json',plan)
 freeze('budget',[H/'budget-plan.json'])

def verify():
 require(git('branch','--show-current')==BRANCH,'Wrong branch')
 require(git('merge-base',BASE,'HEAD')==BASE,'Wrong base')
 for p,d in read(H/'preservation.json')['files'].items(): require(sha(R/p)==d,'Historical drift: '+p)
 for f in sorted(H.glob('*-freeze.json')):
  for p,d in read(f)['files'].items(): require(sha(R/p)==d,'Frozen drift: '+p)
 c=config(); require(c['model']=='gpt-6-astra' and c['reasoning_effort']=='high','Model drift')
 require(sha(Path(c['cli']))==c['cli_sha256'],'CLI drift')
 require(sha(Path(c['native_executable']['path']))==c['native_executable']['sha256'],'Executable drift')
 require(subprocess.check_output([c['cli'],'--version'],text=True).strip()==c['cli_version'],'Version drift')
 plan=read(H/'budget-plan.json')
 require(plan['execution_fingerprint']==budget.digest(read(H/'initial-freeze.json')['files']),'Fingerprint drift')
 audit_packets()
 return {'historical_files':len(read(H/'preservation.json')['files']),'scientific_slots':8,'verified':True}

def audit_packets():
 m=manifest(); require(len(list((H/'survivor-packets').glob('*.json')))==3,'Survivor count')
 h7=R/'distance/natural-admission-v0.2'
 for sid in m['survivors']:
  j=read(h7/'artifact-judgments'/f'{sid}.json'); r=read(h7/'remainder-inventory'/f'{sid}.json')
  cs={c['candidate_id']:c for c in r['candidates']}; a=read(H/'survivor-audits'/f'{sid}.json')
  p=read(H/'survivor-packets'/f'{sid}.json'); ids=[x['candidate_id'] for x in a['crosswalk']]
  require(ids==j['definite_viable_candidate_ids'],'Allowlist mismatch')
  require(a['survivor_packet_audit']['passed'],'Fidelity failure')
  require(len(p['considerations'])==len(ids),'Missing candidate')
  deleted=set(read(h7/'ablations'/f'{sid}.json')['deleted_claim_ids'])
  for i,(v,k) in enumerate(zip(p['considerations'],ids),1):
   c=cs[k]; require(v=={'id':f'V{i:02}',**{q:c['component'][q] for q in ('value','scope')}},'Candidate value/scope drift')
   require(all(x['value']=='YES' for x in c['viability'].values()),'Nondefinite promotion')
   require(not set(c['surviving_claim_ids'])&deleted,'Deleted claim promotion')
  require(not BANNED.search(json.dumps(p)),'Source identity leak')
  ap=read(H/'augmented-packets'/f'{sid}.json')
  require(ap=={'target_frame':read(h7/'targets'/f'{sid.split("-")[1]}.json'),'additional_vetted_considerations':p},'Augmented content drift')
  require(not BANNED.search(packet('augmented',sid).read_text()),'Augmented identity leak')
 for tid in slots('native'):
  require(read(H/'native-packets'/f'{tid}.json')=={'target_frame':read(h7/'targets'/f'{tid}.json')},'Native contamination')
 require('K14' not in read(H/'survivor-audits/H7-T03-1.json')['survivor_packet_audit']['definite_candidates_present'],'K14 promoted')
 for schema in (H/'schemas').glob('*.json'): Draft202012Validator.check_schema(read(schema))


def command(cwd,out,stage):
 c=config(); schema='impact' if stage=='impact' else 'target'
 argv=[c['cli'],'exec','--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check',
  '--sandbox','read-only','--json','--color','never','--cd',str(cwd),'--model','gpt-6-astra',
  '-c','model_reasoning_effort="high"','-c','project_doc_max_bytes=0','-c','web_search="disabled"',
  '--output-schema',str(H/'schemas'/f'{schema}.schema.json'),'--output-last-message',str(out/'response.json')]
 for feature in c['disabled_features']: argv+=['--disable',feature]
 return argv+['-']
def clean_env():
 return {k:v for k,v in os.environ.items() if not k.startswith(('CODEX_','CLAUDE_','ANTHROPIC_','OPENAI_','AZURE_OPENAI_','GEMINI_','GOOGLE_GENAI_')) and k not in ('CLAUDECODE','MODEL_PROVIDER','MODEL','LLM_MODEL')}
def audit_events(events,response_text):
 starts=[e for e in events if e.get('type')=='thread.started']
 require(len(starts)==1 and starts[0].get('thread_id'),'Missing fresh session')
 require(sum(e.get('type')=='turn.completed' for e in events)==1,'Incomplete turn')
 require(not any(e.get('type') in ('error','turn.failed') for e in events),'Provider failure')
 require(all(e['item'].get('type') in ('agent_message','reasoning') for e in events if 'item' in e),'Tool activity')
 finals=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
 require(len(finals)==1 and finals[0].strip()==response_text.strip(),'Final stream mismatch')
 models=[]
 def walk(x):
  if isinstance(x,dict):
   for k,v in x.items():
    if k in ('model','model_id','model_name') and isinstance(v,str): models.append(v)
    require(not ('fallback' in k.lower() and v),'Fallback'); walk(v)
  elif isinstance(x,list):
   for v in x: walk(v)
 walk(events); require(all(x=='gpt-6-astra' for x in models),'Model substitution')
 return {'session_id':starts[0]['thread_id'],'requested_model':'gpt-6-astra','reasoning_effort':'high',
  'returned_model_identifiers':models,'served_snapshot':None,'usage':[e.get('usage') for e in events if e.get('type')=='turn.completed'],
  'retry_observability':'No harness retries; provider-internal behavior unavailable.'}

def validate(stage,uid,value):
 Draft202012Validator(read(H/'schemas'/('impact.schema.json' if stage=='impact' else 'target.schema.json'))).validate(value)
 if stage!='impact':
  if stage=='native': require(not value['survivor_basis'],'Native basis contamination')
  else:
   require(not BANNED.search(json.dumps(value['target_response'])),'Response source identity leak')
   vids={x['id'] for x in read(H/'survivor-packets'/f'{uid}.json')['considerations']}
   for b in value['survivor_basis']:
    items=value['target_response'][b['response_field']]
    require(b['item_index']<(len(items) if isinstance(items,list) else 1),'Invalid basis location')
    require(bool(b['consideration_ids']) and set(b['consideration_ids'])<=vids,'Invalid consideration')
 else:
  j=value['impact_judgment']; require(j['pair_id']==uid,'Pair identity')
  ds=j['differences']; require(len({d['difference_id'] for d in ds})==len(ds),'Duplicate difference')
  for d in ds:
   require(bool(d['categories']),'Empty categories')
   if d['materially_changes_target_reasoning']=='YES':
    sides=['response_a'] if d['introduced_in']=='A_ONLY' else ['response_b'] if d['introduced_in']=='B_ONLY' else ['response_a','response_b']
    require(any(d[s]['downstream_consequence'].strip() for s in sides),'Material consequence missing')
  if j['semantic_equivalence']=='YES': require(j['overall_material_difference']=='NO' and not ds,'Equivalence contradiction')
  if j['overall_material_difference']=='YES': require(any(d['materially_changes_target_reasoning']=='YES' for d in ds),'Overall YES without material difference')
  if j['overall_material_difference']=='NO': require(not ds,'NO requires empty differences')

def guard(stage,ids):
 require(state() in ('READY','BATCH_COMPLETE'),'Scheduling paused or terminal')
 require(1<=len(ids)<=2 and len(ids)==len(set(ids)),'Batch size')
 remaining=[x for x in slots(stage) if not terminal(stage,x)]
 require(ids==remaining[:len(ids)],'Order/duplicate')
 if stage=='augmented': require((H/'native-freeze.json').exists(),'Native stage not frozen')
 if stage=='impact': require((H/'impact-packets-freeze.json').exists(),'Comparison packets not frozen')
 for uid in ids:
  require(not (RT/'attempts'/stage/uid).exists(),'Attempt consumed; no retry')
  require(packet(stage,uid).exists(),'Missing packet')

def preflight(stage,ids):
 verify(); guard(stage,ids)
 stamp=usage.stamp().replace(':','-'); p=RT/'preflights'/stamp
 before=usage.normalize(usage.read_limits(cli=config()['cli']),'local-codex-account')
 calibration={'version':1,'samples':[]}
 # H8 profiles are new. Preserve batch observations, but never equate isolated contexts with isolated account usage.
 for f in sorted((RT/'batches').glob('*/calibration-record.json')): calibration['samples'].append(read(f))
 plan=read(H/'budget-plan.json'); remaining={'stages':[{**s,'sessions':sum(not terminal(s['id'],x) for x in slots(s['id']))} for s in plan['stages']]}
 batch_plan={'stages':[{**next(s for s in plan['stages'] if s['id']==stage),'sessions':len(ids)}]}
 write(p/'before.json',before); write(p/'calibration.json',calibration)
 report=usage.predict(remaining,before,calibration,reserve_points=10)
 write(p/'forecast.json',report); write(p/'batch-forecast.json',usage.predict(batch_plan,before,calibration,reserve_points=10))
 write(p/'review.json',{'stage':stage,'ids':ids,'plan_sha256':budget.digest(plan),'authorization':'User H8 handoff and Implement the plan; agreed direction and attribution rules.',
  'before_path':str(p/'before.json'),'calibration_path':str(p/'calibration.json'),'forecast_path':str(p/'forecast.json')})
 print(json.dumps({'review':str(p/'review.json'),'plan_sha256':budget.digest(plan),'forecast':report},indent=2))
 return 1 if report['refresh_required'] else 2 if report['approval_required'] else 0

def reserve_and_launch(gate,plan,policy,stage,uid,argv,launch):
 gate.reserve(plan,policy,stage,uid,argv)
 return launch()

def execute(stage,uid,plan):
 verify(); require(state()=='RUNNING','Scheduling paused')
 require(not git('status','--porcelain'),'Unclean launch checkpoint')
 d=RT/'attempts'/stage/uid
 d.mkdir(parents=True,exist_ok=False)
 request=packet(stage,uid).read_bytes(); raw(d/'request.txt',request)
 gate=budget.Gate(); policy=read(R/'docs/experiment-budget-policy.json'); session=stage+'/'+uid
 with tempfile.TemporaryDirectory(prefix='h8-isolated-') as cwd:
  argv=command(cwd,d,stage)
  write(d/'attempt.json',{'at':usage.stamp(),'execution_commit':head(),'stage':stage,'slot':uid,'command':argv,
   'request_sha256':sha(d/'request.txt'),'initially_empty':True,'harness_attempt':1,'configuration':config(),
   'schema_sha256':sha(H/'schemas'/('impact.schema.json' if stage=='impact' else 'target.schema.json'))})
  def launch():
   with (d/'events.jsonl').open('x') as out,(d/'stderr.txt').open('x') as err:
    proc=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=out,stderr=err,cwd=cwd,env=clean_env(),start_new_session=True)
    write(d/'process.json',{'pid':proc.pid,'at':usage.stamp()})
    timed_out=False
    try: proc.communicate(request,timeout=config()['timeout_seconds'])
    except subprocess.TimeoutExpired:
     timed_out=True; os.killpg(proc.pid,signal.SIGKILL); proc.wait()
    write(d/'exit.json',{'returncode':proc.returncode,'timeout':timed_out})
    gate.finish(plan['experiment_id'],session,proc.returncode)
    require(proc.returncode==0 and not timed_out,'Provider process failure; preserve and classify')
  reserve_and_launch(gate,plan,policy,stage,session,argv,launch)
 value=read(d/'response.json'); events=[json.loads(x,object_pairs_hook=unique) for x in (d/'events.jsonl').read_text().splitlines() if x.strip()]
 meta=audit_events(events,(d/'response.json').read_text())
 prior=[e.get('thread_id') for f in (RT/'attempts').glob('*/*/events.jsonl') if f.parent!=d for e in map(json.loads,f.read_text().splitlines()) if e.get('type')=='thread.started']
 require(meta['session_id'] not in prior,'Session reuse'); validate(stage,uid,value)
 write(d/'validation.json',{'response_sha256':sha(d/'response.json'),'schema_valid':True,'metadata':meta})
 print('VALIDATED '+stage+'/'+uid,flush=True)

def run(review_path):
 review=read(review_path); stage,ids=review['stage'],review['ids']; verify(); guard(stage,ids)
 plan=read(H/'budget-plan.json'); require(budget.digest(plan)==review['plan_sha256'],'Plan changed')
 before=read(Path(review['before_path'])); cal=read(Path(review['calibration_path']))
 remain={'stages':[{**s,'sessions':sum(not terminal(s['id'],x) for x in slots(s['id']))} for s in plan['stages']]}
 report=usage.predict(remain,before,cal,reserve_points=10)
 require(not report['refresh_required'],'Refresh usage')
 require(0<=datetime.now(timezone.utc).timestamp()-usage.epoch(before['captured_at'])<=300,'Stale preflight')
 gate=budget.Gate(); status=gate.status(plan,read(R/'docs/experiment-budget-policy.json'))
 require(status['allowed'],'Budget/usage gate: '+str(status['blocking_reasons']))
 require(not git('status','--porcelain'),'Commit before launch')
 b=RT/'batches'/f'{len(list((RT/"batches").glob("*"))):04}'
 write(b/'review.json',review); write(b/'before.json',before); write(b/'forecast.json',report)
 transition('RUNNING',stage+': '+','.join(ids))
 try:
  for uid in ids: execute(stage,uid,plan)
  transition('BATCH_COMPLETE','Validated fixed batch')
 except BaseException as exc:
  write(b/'failure.json',{'type':type(exc).__name__,'message':str(exc),'at':usage.stamp()})
  transition('PAUSED_AMBIGUOUS','Preserve and classify; no retry'); raise
 finally:
  try:
   after=usage.normalize(usage.read_limits(cli=config()['cli']),before['account_scope']); write(b/'after.json',after)
   ds=[RT/'attempts'/stage/uid for uid in ids]
   write(b/'calibration-record.json',{'usage_profile':next(s['usage_profile'] for s in plan['stages'] if s['id']==stage),
    'sessions':sum((d/'process.json').exists() for d in ds),'before':before,'after':after,
    'available_usage':[read(d/'validation.json')['metadata']['usage'] for d in ds if (d/'validation.json').exists()],
    'isolated_account_work':False,'included_as_clean_calibration':False,
    'exclusion_reason':'Concurrent interactive Codex work and unsettled/coarse telemetry; account isolation not attested.'})
  except Exception as exc:
   write(b/'bookkeeping-failure.json',{'error':str(exc)}); transition('PAUSED_RECOVERABLE','After-snapshot bookkeeping failed')

def publish(stage,uid):
 verify(); require(state()=='BATCH_COMPLETE','Cannot publish during pause')
 d=RT/'attempts'/stage/uid; require(sha(d/'response.json')==read(d/'validation.json')['response_sha256'],'Response drift')
 validate(stage,uid,read(d/'response.json'))
 paths=[]
 for p in sorted(d.iterdir()):
  dest=H/'raw'/stage/uid/p.name; raw(dest,p.read_bytes()); paths.append(dest)
 dest=response(stage,uid); raw(dest,(d/'response.json').read_bytes()); paths.append(dest)
 freeze(stage+'--'+uid,paths)
 if all(terminal(stage,x) for x in slots(stage)): freeze(stage,[response(stage,x) for x in slots(stage) if response(stage,x).exists()])

def ordering(pair_id):
 digest=hashlib.sha256(f'H8|{BASE}|{pair_id}'.encode()).hexdigest()
 return {'hash':digest,'A':'NATIVE' if int(digest[:2],16)%2==0 else 'SURVIVOR_AUGMENTED',
         'B':'SURVIVOR_AUGMENTED' if int(digest[:2],16)%2==0 else 'NATIVE'}
def comparisons():
 verify(); require((H/'augmented-freeze.json').exists(),'Augmented stage not frozen')
 require(not git('status','--porcelain'),'Commit responses first')
 paths=[]
 for p in manifest()['pairs']:
  if not response('native',p['native_slot']).exists() or not response('augmented',p['augmented_slot']).exists(): continue
  order=ordering(p['pair_id']); n=read(response('native',p['native_slot']))['target_response']; a=read(response('augmented',p['augmented_slot']))['target_response']
  payload={'target_frame':read(H/'native-packets'/f'{p["target_id"]}.json')['target_frame'],
           'response_a':n if order['A']=='NATIVE' else a,'response_b':a if order['A']=='NATIVE' else n}
  op=H/'comparison-order'/f'{p["pair_id"]}.json'
  write(op,{**p,**order,'native_response_sha256':sha(response('native',p['native_slot'])),'augmented_response_sha256':sha(response('augmented',p['augmented_slot']))}); paths.append(op)
  jp=H/'impact-packets'/f'{p["pair_id"]}.json'; write(jp,payload); paths.append(jp)
  tp=packet('impact',p['pair_id']); raw(tp,((H/'impact-instruction.txt').read_text()+'\nPair identifier: '+p['pair_id']+'\n\nINPUT\n'+json.dumps(payload,indent=2)+'\n').encode()); paths.append(tp)
 freeze('impact-packets',paths)

def affected_pairs(stage,uid):
 return [p['pair_id'] for p in manifest()['pairs'] if
         (stage=='native' and p['native_slot']==uid) or
         (stage=='augmented' and p['augmented_slot']==uid) or
         (stage=='impact' and p['pair_id']==uid)]

def no_observation_evidence(d,expected_request_hash):
 """Conservative qualification; caller must still prove independent continuation."""
 require((d/'process.json').exists() and (d/'exit.json').exists(),'Launch/exit unknown')
 attempt=read(d/'attempt.json')
 require(attempt['harness_attempt']==1 and attempt['initially_empty'],'Attempt/isolation unknown')
 require(sha(d/'request.txt')==expected_request_hash==attempt['request_sha256'],'Input mismatch')
 require(not (d/'response.json').exists() or not (d/'response.json').read_bytes(),'Scientific/partial response exists')
 events=[json.loads(x,object_pairs_hook=unique) for x in (d/'events.jsonl').read_text().splitlines() if x.strip()]
 starts=[e for e in events if e.get('type')=='thread.started']
 require(len(starts)==1 and starts[0].get('thread_id'),'Session unknown')
 require(not any('item' in e or e.get('type')=='turn.completed' for e in events),'Observation/partial content requires investigation')
 require(all(e.get('type') in ('thread.started','turn.started','error','turn.failed') for e in events),'Unrecognized provider event')
 return {'classification':'PROVIDER_NO_OBSERVATION','session_id':starts[0]['thread_id'],
         'request_sha256':expected_request_hash,'attempt_consumed':True,'retry_allowed':False}

def direction(d,order):
 return 'BOTH_DIFFERENT' if d['introduced_in']=='BOTH_DIFFERENT' else order[d['introduced_in'][0]]
def unblind():
 verify(); require((H/'impact-freeze.json').exists(),'All judgments must freeze first')
 require(all(terminal('impact',x) for x in slots('impact')),'Judgment slots not terminal')
 paths=[]
 for p in manifest()['pairs']:
  if not response('impact',p['pair_id']).exists(): continue
  order=read(H/'comparison-order'/f'{p["pair_id"]}.json'); j=read(response('impact',p['pair_id']))['impact_judgment']
  ds=[{'difference_id':d['difference_id'],'introduced_by':direction(d,order),
       'material':d['materially_changes_target_reasoning'],'categories':d['categories'],
       'augmented_side':'response_a' if order['A']=='SURVIVOR_AUGMENTED' else 'response_b'} for d in j['differences']]
  out=H/'unblinded'/f'{p["pair_id"]}.json'; write(out,{'pair_id':p['pair_id'],'order':order,'judgment_sha256':sha(response('impact',p['pair_id'])),'directed_differences':ds}); paths.append(out)
 freeze('unblinded',paths)

def impact_status(j,directed,audits,nonmaterial_additions=False):
 if j is None: return 'UNMEASURED'
 eligible=[d for d in directed if d['introduced_by'] in ('SURVIVOR_AUGMENTED','BOTH_DIFFERENT') and d['material']=='YES']
 if any(a['classification']=='ATTRIBUTABLE_TO_SURVIVOR' and a['augmented_consequence_established'] for a in audits if a['difference_id'] in {d['difference_id'] for d in eligible}): return 'MATERIAL_TARGET_CHANGE'
 if eligible or j['overall_material_difference']=='UNCERTAIN' or any(d['material']=='UNCERTAIN' for d in directed): return 'UNCERTAIN_TARGET_CHANGE'
 if nonmaterial_additions: return 'MINOR_OR_NONMATERIAL_CHANGE'
 if j['semantic_equivalence']=='YES' or not j['differences']: return 'NO_MATERIAL_CHANGE'
 return 'MINOR_OR_NONMATERIAL_CHANGE'

def aggregate():
 verify(); require((H/'attribution-freeze.json').exists(),'Attribution not frozen')
 rows=[]; all_counts={c:0 for c in CATEGORIES}; attributed_counts={c:0 for c in CATEGORIES}
 for p in manifest()['pairs']:
  measured=response('impact',p['pair_id']).exists()
  j=read(response('impact',p['pair_id']))['impact_judgment'] if measured else None
  ds=read(H/'unblinded'/f'{p["pair_id"]}.json')['directed_differences'] if measured else []
  audit=read(H/'attribution-audit'/f'{p["pair_id"]}.json') if measured else {'differences':[]}
  eligible=[d for d in ds if d['introduced_by'] in ('SURVIVOR_AUGMENTED','BOTH_DIFFERENT') and d['material']=='YES']
  good=[d for d in eligible if any(a['difference_id']==d['difference_id'] and a['classification']=='ATTRIBUTABLE_TO_SURVIVOR' and a['augmented_consequence_established'] for a in audit['differences'])]
  for d in ds:
   if d['material']=='YES':
    for c in set(d['categories']): all_counts[c]+=1
  for d in good:
   for c in set(d['categories']): attributed_counts[c]+=1
  rows.append({'survivor_id':p['survivor_id'],'pair_id':p['pair_id'],
   'h7_admission':read(H/'survivor-audits'/f'{p["survivor_id"]}.json')['admission'],
   'comparison_result':j['overall_material_difference'] if j else 'UNMEASURED',
   'augmented_material_changes':[d['difference_id'] for d in eligible],
   'survivor_attributable_material_changes':[d['difference_id'] for d in good],
   'impact_status':impact_status(j,ds,audit['differences'],audit.get('nonmaterial_augmented_additions',False))})
 statuses=['MATERIAL_TARGET_CHANGE','MINOR_OR_NONMATERIAL_CHANGE','NO_MATERIAL_CHANGE','UNCERTAIN_TARGET_CHANGE','UNMEASURED']
 out={'survivor_impact':rows,'counts':{s:sum(r['impact_status']==s for r in rows) for s in statuses},
  'material_category_counts_all_directions':all_counts,'survivor_attributable_category_counts':attributed_counts,
  'survivor_attributable_material_changes':sum(len(r['survivor_attributable_material_changes']) for r in rows),
  'scientific_calls_planned':8,'scientific_calls_completed':len(list((H/'raw').glob('*/*/validation.json'))),
  'scientific_attempts_launched':len(list((RT/'attempts').glob('*/*/process.json'))),
  'independent_samples':False,'shared_T03_baseline':True}
 write(H/'metrics.json',out); freeze('outcomes',[H/'metrics.json']); print(json.dumps(out,indent=2))

def main():
 p=argparse.ArgumentParser(description=__doc__); s=p.add_subparsers(dest='action',required=True)
 for a in ('verify','freeze-initial','comparisons','unblind','aggregate'): s.add_parser(a)
 for a in ('preflight','publish'):
  q=s.add_parser(a); q.add_argument('stage',choices=['native','augmented','impact']); q.add_argument('ids',nargs='+')
 q=s.add_parser('run'); q.add_argument('review',type=Path)
 a=p.parse_args()
 if a.action=='verify': print(json.dumps(verify()))
 elif a.action=='freeze-initial': freeze_initial()
 elif a.action=='preflight': return preflight(a.stage,a.ids)
 elif a.action=='run': run(a.review)
 elif a.action=='publish':
  for uid in a.ids: publish(a.stage,uid)
 elif a.action=='comparisons': comparisons()
 elif a.action=='unblind': unblind()
 elif a.action=='aggregate': aggregate()
 return 0
if __name__=='__main__': sys.exit(main())
