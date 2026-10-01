#!/usr/bin/env python3
"""H.4 isolated one-sample inquiry-only runner. No repair or retry path."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import authoring as a
import validation as v
H=a.H;R=a.R;RT=R/'.runtime/inquiry-unitization-calibration-v0.1'
read=a.read;sha=a.sha;require=a.require

def now():return datetime.now(timezone.utc).isoformat()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def head():return git('rev-parse','HEAD').decode().strip()
def rel(p):return str(p.relative_to(R))
def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')
def raw(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(data)
def inventory(paths):return {rel(p):sha(p) for p in sorted(paths) if p.is_file() and '__pycache__' not in p.parts}
def hashes(files):
    for p,h in files.items():require(sha(R/p)==h,'Frozen bytes changed: '+p)
def committed(p,commit='HEAD'):require(git('show',f'{commit}:{rel(p)}')==p.read_bytes(),'Uncommitted input: '+rel(p))
def config():return read(H/'execution-config.json')
def order():return read(H/'manifest.json')['case_order']
def case(cid):return read(H/'cases'/f'{cid}.json')
def packet(cid):return H/'packets'/f'{cid}.txt'
def packet_text(cid):return (H/'INQUIRY-UNIT.md').read_text()+'\n'+(H/'JUDGE.md').read_text()+'\nSURVIVING MAPPING\n'+json.dumps(case(cid),indent=2,ensure_ascii=False)+'\n'
def clean_env():return {k:x for k,x in os.environ.items() if not k.startswith(('CODEX_','CLAUDE_','ANTHROPIC_','OPENAI_','AZURE_OPENAI_','GEMINI_','GOOGLE_GENAI_')) and k not in ('CLAUDECODE','MODEL_PROVIDER','MODEL','LLM_MODEL')}
def binary_check():
    c=config();require(c['model']=='gpt-6-astra' and c['reasoning_effort']=='high','Wrong requested model/effort')
    require(sha(Path(c['cli']))==c['cli_sha256'],'CLI drift');require(sha(Path(c['native_executable']['path']))==c['native_executable']['sha256'],'Native drift')
    version=subprocess.check_output([c['cli'],'--version'],text=True).strip();require(version==c['cli_version'],'Version drift');return version

def command(cwd,d):
    cmd=[config()['cli'],'exec','--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check','--sandbox','read-only','--json','--color','never','--cd',str(cwd),'--model','gpt-6-astra','-c','model_reasoning_effort="high"','-c','project_doc_max_bytes=0','-c','web_search="disabled"','--output-schema',str(H/'schemas/assessment.schema.json'),'--output-last-message',str(d/'response.json')]
    for feature in config()['disabled_features']:cmd+=['--disable',feature]
    return cmd+['-']

def unique(pairs):
    result={}
    for k,x in pairs:
        require(k not in result,'Duplicate JSON key');result[k]=x
    return result

def audit_events(events):
    starts=[e for e in events if e.get('type')=='thread.started'];require(len(starts)==1,'One fresh context required')
    require(sum(e.get('type')=='turn.completed' for e in events)==1,'Incomplete turn')
    require(not any(e.get('type') in ('error','turn.failed') for e in events),'Provider error')
    require(all(e['item'].get('type') in ('agent_message','reasoning') for e in events if 'item' in e),'Tool activity')
    models=[]
    def walk(x,path):
        if isinstance(x,dict):
            for k,value in x.items():
                if k in ('model','model_id','model_name') and isinstance(value,str):models.append({'value':value,'source':path+'.'+k})
                require(not ('fallback' in k.lower() and value),'Fallback event');walk(value,path+'.'+k)
        elif isinstance(x,list):
            for i,value in enumerate(x):walk(value,f'{path}[{i}]')
    walk(events,'events');require(all(x['value']=='gpt-6-astra' for x in models),'Model substitution')
    return {'session_id':starts[0]['thread_id'],'returned_model_identifiers':models,'verified_served_snapshot':None,
            'usage':[e.get('usage') for e in events if e.get('type')=='turn.completed'],
            'internal_retry_events':[e for e in events if e.get('subtype')=='api_retry'],
            'retry_observability':'No harness retries; unexposed provider retries cannot be ruled out.'}

def prepare():
    require(not RT.exists(),'Runtime already exists');a.gate();binary_check()
    for cid in order():raw(packet(cid),packet_text(cid).encode())
    write(H/'prepared.json',{'at':now(),'parent_commit':head(),'order':order(),'files':inventory(H.rglob('*'))})

def verify(commits=False):
    a.preserve();f=read(H/'prepared.json');hashes(f['files']);require(f['order']==order(),'Order drift')
    for cid in order():require(packet(cid).read_text()==packet_text(cid),'Packet drift')
    require(a.gate()==read(H/'review/authoring-gate.json'),'Authoring gate drift')
    if commits:
        committed(H/'prepared.json')
        for p in f['files']:committed(R/p)
    return {'cases':18,'primary_complete':12,'calibration_complete':13,'historical_preservation':True}

def preflight():
    import historical
    verify(True);version=binary_check();checks=historical.checks()
    cmd=[sys.executable,'-B','-m','unittest','discover','-s',str(H/'tests'),'-p','test_*.py']
    p=subprocess.run(cmd,cwd=R,capture_output=True,text=True,timeout=600)
    checks.append({'command':cmd,'exit_code':p.returncode,'output':p.stdout+p.stderr})
    write(H/'review/preflight.json',{'at':now(),'input_commit':head(),'prepared_sha256':sha(H/'prepared.json'),'cli_version':version,'provider_calls':0,'checks':checks})
    for row in checks:print(row['exit_code'],' '.join(row['command']),flush=True)
    require(all(row['exit_code']==0 for row in checks),'Preflight failed')

def state():
    files=sorted((RT/'states').glob('*.json'));return read(files[-1])['state'] if files else None

def transition(status,reason):
    files=sorted((RT/'states').glob('*.json'))
    write(RT/'states'/f'{len(files):04}.json',{'state':status,'reason':reason,'at':now(),'commit':head(),'previous_sha256':sha(files[-1]) if files else None})

def execute(cid):
    d=RT/'runs'/cid;d.mkdir(parents=True,exist_ok=False);launched=False
    write(d/'attempt.json',{'at':now(),'case_id':cid,'input_commit':head(),'harness_attempt':1})
    prompt=packet(cid).read_bytes();raw(d/'prompt.txt',prompt)
    try:
        version=binary_check()
        with tempfile.TemporaryDirectory(prefix='h4-isolated-') as cwd:
            require(not list(Path(cwd).iterdir()),'Nonempty context');cmd=command(cwd,d)
            write(d/'reservation.json',{'at':now(),'input_commit':head(),'case_id':cid,'packet_sha256':sha(packet(cid)),
              'schema_sha256':sha(H/'schemas/assessment.schema.json'),'configuration':config(),'command':cmd,'cli_version':version,
              'working_directory':cwd,'working_directory_initially_empty':True,'requested_session':'ephemeral',
              'environment_policy':'Provider overrides and parent markers removed; existing on-disk auth only.'})
            with (d/'events.jsonl').open('x') as out,(d/'stderr.txt').open('x') as err:
                process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=out,stderr=err,cwd=cwd,env=clean_env(),start_new_session=True);launched=True
                write(d/'process.json',{'pid':process.pid,'parent_pid':os.getpid(),'launched_at':now()})
                try:process.communicate(prompt,timeout=config()['timeout_seconds'])
                except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait();raise
            write(d/'exit.json',{'at':now(),'returncode':process.returncode});require(process.returncode==0,'CLI nonzero exit')
            events=[json.loads(line,object_pairs_hook=unique) for line in (d/'events.jsonl').read_text().splitlines() if line.strip()]
            metadata=audit_events(events)
            for previous in (RT/'runs').glob('*/validation.json'):require(read(previous)['metadata']['session_id']!=metadata['session_id'],'Reused session')
            finals=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
            require(len(finals)==1 and finals[0].strip()==(d/'response.json').read_text().strip(),'Final stream mismatch')
            value=json.loads((d/'response.json').read_text(),object_pairs_hook=unique);result=v.validate(case(cid),value)
            require(not any(x['code']=='IQ_SCHEMA' for x in result['errors']),'Invalid response schema')
        write(d/'validation.json',{'at':now(),'metadata':metadata,'result':result,'status':'valid' if result['validation_passed'] else 'scientific_validation_failure'})
        return result
    except Exception as exc:
        write(d/'failure.json',{'at':now(),'launched':launched,'error':type(exc).__name__+': '+str(exc)})
        transition('TERMINATED_MEASUREMENT' if launched else 'PAUSED_AMBIGUOUS',str(exc));raise

def run():
    require(state() is None,'No automatic restart');require(not (H/'judgments-freeze.json').exists(),'Sealed')
    require(not list((RT/'runs').glob('*')),'Existing reservation');verify(True);binary_check()
    pre=H/'review/preflight.json';committed(pre);p=read(pre)
    require(p['prepared_sha256']==sha(H/'prepared.json') and all(x['exit_code']==0 for x in p['checks']),'Preflight binding')
    require(not git('status','--porcelain').strip(),'Unclean continuation');initial=head();transition('RUNNING','18 frozen inquiry cases')
    try:
        for i,cid in enumerate(order(),1):
            require(state()=='RUNNING' and head()==initial,'State or checkpoint changed');require(not git('status','--porcelain').strip(),'Unclean boundary')
            verify(True);result=execute(cid)
            print(f'{i}/18 {cid}: '+('valid' if result['validation_passed'] else ','.join(x['code'] for x in result['errors'])),flush=True)
        transition('COMPLETE','All 18 distinct observations preserved; scientific acceptance is reported separately')
    except Exception as exc:
        if state()=='RUNNING':transition('PAUSED_AMBIGUOUS',str(exc))
        raise

def freeze():
    require(state()=='COMPLETE','Incomplete measurement');verify(True);rows=[]
    for cid in order():
        d=RT/'runs'/cid;validation=read(d/'validation.json');raw(H/'judgments'/f'{cid}.json',(d/'response.json').read_bytes())
        rows.append({'case_id':cid,'response_sha256':sha(d/'response.json'),'reservation':read(d/'reservation.json'),'validation':validation,'files':inventory(d.iterdir())})
    write(H/'judgments-freeze.json',{'at':now(),'prepared_sha256':sha(H/'prepared.json'),'runs':rows,'states':inventory((RT/'states').glob('*'))})

def verify_results():
    verify(True);f=read(H/'judgments-freeze.json');require(f['prepared_sha256']==sha(H/'prepared.json'),'Freeze binding')
    require([r['case_id'] for r in f['runs']]==order(),'Result coverage');sessions=[];previous=None
    require(sorted(p.name for p in (RT/'runs').iterdir())==sorted(order()),'Extra reservation')
    hashes(f['states'])
    for row in f['runs']:
        cid=row['case_id'];d=RT/'runs'/cid;hashes(row['files']);reservation=read(d/'reservation.json')
        require(row['reservation']==reservation and row['validation']==read(d/'validation.json'),'Runtime mismatch')
        require((H/'judgments'/f'{cid}.json').read_bytes()==(d/'response.json').read_bytes(),'Judgment replaced')
        require(sha(d/'response.json')==row['response_sha256'],'Response digest')
        require(reservation['packet_sha256']==sha(packet(cid))==sha(d/'prompt.txt'),'Packet lineage')
        require(reservation['schema_sha256']==sha(H/'schemas/assessment.schema.json'),'Schema lineage')
        require(reservation['configuration']==config() and reservation['command']==command(reservation['working_directory'],d),'Execution lineage')
        committed(packet(cid),reservation['input_commit']);committed(H/'prepared.json',reservation['input_commit'])
        events=[json.loads(s,object_pairs_hook=unique) for s in (d/'events.jsonl').read_text().splitlines() if s.strip()]
        meta=audit_events(events);require(meta==row['validation']['metadata'],'Metadata drift');sessions.append(meta['session_id'])
        require(v.validate(case(cid),read(d/'response.json'))==row['validation']['result'],'Validation drift')
        require(previous is None or previous<=reservation['at'],'Overlapping sessions');previous=row['validation']['at']
    require(len(sessions)==len(set(sessions))==18,'18 fresh sessions')
    return {'observations':18,'fresh_sessions':18,'historical_preservation':a.preserve()}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','preflight','run','freeze','verify','verify-results']);x=p.parse_args()
    result=verify_results() if x.action=='verify-results' else globals()[x.action]()
    if result:print(json.dumps(result,indent=2))
