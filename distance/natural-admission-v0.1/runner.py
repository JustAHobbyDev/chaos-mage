#!/usr/bin/env python3
"""H.6 immutable staged runner; offline by default, no retries or semantic repair."""
import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import threading
from jsonschema import Draft202012Validator
import contracts as c
H=Path(__file__).resolve().parent;R=H.parents[1];RT=R/'.runtime/natural-admission-v0.1'
STAGES=['generation','claims','claim-judgments','remainder-inventory','artifact-judgments']
PROMPTS=['GENERATION.md','CLAIMS.md','CLAIM-WARRANT.md','REMAINDER.md','ARTIFACT.md']
LOCK=threading.Lock()
def now():return datetime.now(timezone.utc).isoformat()
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def head():return git('rev-parse','HEAD').decode().strip()
def rel(p):return str(p.relative_to(R))
def require(x,msg):
    if not x:raise ValueError(msg)
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(v,f,indent=2,ensure_ascii=False);f.write('\n')
def raw(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(v)
def inventory(paths):return {rel(p):sha(p) for p in sorted(paths) if p.is_file() and '__pycache__' not in p.parts}
def hashes(files):
    for p,h in files.items():require(sha(R/p)==h,'INTEGRITY: '+p)
def committed(p):require(git('show','HEAD:'+rel(p))==p.read_bytes(),'Uncommitted: '+rel(p))
def order():return read(H/'manifest.json')['packet_order']
def config():return read(H/'execution-config.json')
def binary_check():
    v=config();require(v['model']=='gpt-6-astra' and v['reasoning_effort']=='high','Model configuration')
    require(sha(Path(v['cli']))==v['cli_sha256'],'CLI drift')
    require(sha(Path(v['native_executable']['path']))==v['native_executable']['sha256'],'Native drift')
    require(subprocess.check_output([v['cli'],'--version'],text=True).strip()==v['cli_version'],'CLI version')
def clean_env():return {k:v for k,v in os.environ.items() if not k.startswith(('CODEX_','CLAUDE_','ANTHROPIC_','OPENAI_','AZURE_OPENAI_','GEMINI_','GOOGLE_GENAI_')) and k not in ('CLAUDECODE','MODEL_PROVIDER','MODEL','LLM_MODEL')}
def command(cwd,d,stage):
    cmd=[config()['cli'],'exec','--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check','--sandbox','read-only','--json','--color','never','--cd',str(cwd),'--model','gpt-6-astra','-c','model_reasoning_effort="high"','-c','project_doc_max_bytes=0','-c','web_search="disabled"','--output-schema',str(H/'schemas'/f'{stage}.schema.json'),'--output-last-message',str(d/'response.json')]
    for feature in config()['disabled_features']:cmd+=['--disable',feature]
    return cmd+['-']
def unique(pairs):
    d={}
    for k,v in pairs:require(k not in d,'Duplicate JSON key');d[k]=v
    return d
def audit_events(events):
    starts=[e for e in events if e.get('type')=='thread.started'];require(len(starts)==1,'Fresh session missing')
    require(sum(e.get('type')=='turn.completed' for e in events)==1,'Incomplete turn')
    require(not any(e.get('type') in ('error','turn.failed') for e in events),'Provider error')
    require(all(e['item'].get('type') in ('agent_message','reasoning') for e in events if 'item' in e),'Tool activity')
    models=[]
    def walk(x,path):
        if isinstance(x,dict):
            for k,v in x.items():
                if k in ('model','model_id','model_name') and isinstance(v,str):models.append({'value':v,'source':path+'.'+k})
                require(not ('fallback' in k.lower() and v),'Fallback event');walk(v,path+'.'+k)
        elif isinstance(x,list):
            for i,v in enumerate(x):walk(v,f'{path}[{i}]')
    walk(events,'events');require(all(m['value']=='gpt-6-astra' for m in models),'Model substitution')
    return {'session_id':starts[0]['thread_id'],'requested_model':'gpt-6-astra','requested_reasoning_effort':'high','returned_model_identifiers':models,'verified_served_snapshot':None,'usage':[e.get('usage') for e in events if e.get('type')=='turn.completed'],'retry_observability':'No harness retries; unexposed provider/CLI internal retries cannot be ruled out.'}
def state():
    paths=sorted((RT/'states').glob('*.json'));return read(paths[-1])['state'] if paths else None
def transition(status,reason):
    with LOCK:
        paths=sorted((RT/'states').glob('*.json'))
        write(RT/'states'/f'{len(paths):04}.json',{'state':status,'reason':reason,'at':now(),'commit':head(),'previous_sha256':sha(paths[-1]) if paths else None})
def verify(commits=False):
    hashes(read(H/'preservation.json')['files'])
    if (H/'prepared.json').exists():
        hashes(read(H/'prepared.json')['files'])
        if commits:committed(H/'prepared.json')
    for p in sorted(H.glob('*-freeze.json'))+sorted(H.glob('*-prepared.json')):
        hashes(read(p)['files'])
        if commits:committed(p)
    for p in (H/'span-tables').glob('*.json'):
        cid=p.stem;c.h5.verify_table(read(p),read(H/'generation'/f'{cid}.json')['instrument'])
    sessions=[]
    for p in (H/'raw').glob('*/*/validation.json'):sessions.append(read(p)['metadata']['session_id'])
    require(len(sessions)==len(set(sessions)),'Session reuse')
    return {'historical_files':len(read(H/'preservation.json')['files']),'historical_unchanged':True,'frozen_sessions':len(sessions)}
def initial_freeze():
    require(not (H/'prepared.json').exists(),'Already prepared');binary_check();verify()
    write(H/'prepared.json',{'at':now(),'parent_commit':head(),'files':inventory(H.rglob('*'))})
def packet_base(cid):
    return read(H/'generation-inputs'/f'{cid}.json')
def payload(stage,cid,claim=None):
    base=packet_base(cid)
    if stage=='generation':return base
    base['mapping']=read(H/'generation'/f'{cid}.json')['instrument']
    table=read(H/'span-tables'/f'{cid}.json')
    base['span_table']={'packet_id':cid,'spans':{sid:{k:v for k,v in s.items() if k not in ('source_range',)} for sid,s in table['spans'].items()}}
    if stage=='claims':return base
    if stage=='claim-judgments':base['claim']=claim;return base
    base['ablation']=read(H/'ablations'/f'{cid}.json')
    base['claim_statuses']={x['claim_id']:x['status'] for x in base['ablation']['lineage']}
    if stage=='artifact-judgments':base['inventory']=read(H/'remainder-inventory'/f'{cid}.json')
    return base

def prepare(stage):
    verify(True);i=STAGES.index(stage)
    if i:require((H/f'{STAGES[i-1]}-freeze.json').exists(),'Upstream stage not frozen')
    if stage=='remainder-inventory':
        for cid in order():
            atoms=read(H/'claims'/f'{cid}.json');judgments=[read(H/'claim-judgments'/f"{cid}--{a['claim_id']}.json") for a in atoms['claims']]
            write(H/'ablations'/f'{cid}.json',c.ablate(atoms,judgments))
    runs=[]
    for cid in order():
        atoms=read(H/'claims'/f'{cid}.json')['claims'] if stage=='claim-judgments' else [None]
        if stage=='claim-judgments':require(len({a['claim_id'] for a in atoms})==len(atoms),'Duplicate atom identities prevent unique judgment')
        for atom in atoms:
            uid=cid+'--'+atom['claim_id'] if atom else cid
            p=payload(stage,cid,atom);j=H/'packets'/stage/f'{uid}.json';write(j,p)
            text=(H/PROMPTS[i]).read_text()
            if stage!='generation':text+='\n'+(H/'PROVENANCE.md').read_text()+'\nUse only this frozen packet and general knowledge. No tools, files, browsing, other packets or external context. Return the schema JSON.\n'
            raw(H/'packets'/stage/f'{uid}.txt',(text+'\nFROZEN PACKET\n'+json.dumps(p,indent=2,ensure_ascii=False)+'\n').encode())
            runs.append({'id':uid,'packet_id':cid})
    files=inventory((H/'packets'/stage).glob('*'))
    if stage=='remainder-inventory':files.update(inventory((H/'ablations').glob('*')))
    write(H/f'{stage}-prepared.json',{'at':now(),'input_commit':head(),'runs':runs,'files':files})
    print(json.dumps({'prepared':stage,'units':len(runs)}))

def execute(stage,run,checkpoint,stop):
    uid=run['id'];cid=run['packet_id'];d=RT/'runs'/stage/uid;launched=False
    try:
        require(not stop.is_set(),'Scheduling stopped');verify(True);binary_check()
        require(head()==checkpoint and not git('status','--porcelain').strip(),'Unclean checkpoint')
        d.mkdir(parents=True,exist_ok=False)
        write(d/'attempt.json',{'at':now(),'id':uid,'stage':stage,'execution_commit':checkpoint,'harness_attempt':1})
        prompt=(H/'packets'/stage/f'{uid}.txt').read_bytes();raw(d/'request.txt',prompt)
        with tempfile.TemporaryDirectory(prefix='h6-isolated-') as cwd:
            cmd=command(cwd,d,stage)
            write(d/'reservation.json',{'at':now(),'execution_commit':checkpoint,'id':uid,'stage':stage,'packet_id':cid,'request_sha256':sha(d/'request.txt'),'schema_sha256':sha(H/'schemas'/f'{stage}.schema.json'),'configuration':config(),'command':cmd,'working_directory':cwd,'initially_empty':not list(Path(cwd).iterdir()),'available_mapping_packets':[cid],'collision_exposure':False,'requested_session':'ephemeral','environment_policy':'Parent/provider overrides removed; existing on-disk auth only.'})
            require(not stop.is_set(),'Stopped before launch')
            with (d/'events.jsonl').open('x') as out,(d/'stderr.txt').open('x') as err:
                process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=out,stderr=err,cwd=cwd,env=clean_env(),start_new_session=True);launched=True
                write(d/'process.json',{'pid':process.pid,'launched_at':now()})
                try:process.communicate(prompt,timeout=config()['timeout_seconds'])
                except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait();raise
            write(d/'exit.json',{'at':now(),'returncode':process.returncode});require(process.returncode==0,'CLI nonzero exit')
            events=[json.loads(l,object_pairs_hook=unique) for l in (d/'events.jsonl').read_text().splitlines() if l.strip()]
            metadata=audit_events(events)
            finals=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
            require(len(finals)==1 and finals[0].strip()==(d/'response.json').read_text().strip(),'Final stream mismatch')
            value=json.loads((d/'response.json').read_text(),object_pairs_hook=unique)
            Draft202012Validator(read(H/'schemas'/f'{stage}.schema.json')).validate(value)
            p=read(H/'packets'/stage/f'{uid}.json');diagnostics=[]
            if stage!='generation':diagnostics=c.citation_checks(read(H/'span-tables'/f'{cid}.json'),value)+c.semantic_checks(stage,value,p)
            with LOCK:
                previous=[read(f)['metadata']['session_id'] for f in (RT/'runs').glob('*/*/validation.json')]
                require(metadata['session_id'] not in previous,'Session reuse')
                write(d/'validation.json',{'at':now(),'metadata':metadata,'schema_valid':True,'diagnostics':diagnostics,'response_sha256':sha(d/'response.json')})
        print(f'{stage} {uid}: parsed; {len(diagnostics)} diagnostics',flush=True)
        return True
    except Exception as exc:
        stop.set()
        if d.exists():write(d/'failure.json',{'at':now(),'launched':launched,'error':type(exc).__name__+': '+str(exc)})
        transition('TERMINATED_MEASUREMENT' if launched else 'PAUSED_AMBIGUOUS',f'{stage}/{uid}: {exc}')
        print(f'STOP {stage} {uid}: {exc}',flush=True);return False

def run(stage):
    require(state() in (None,'STAGE_FROZEN'),'No automatic restart');verify(True);binary_check()
    prepared=read(H/f'{stage}-prepared.json');committed(H/f'{stage}-prepared.json')
    require(not (H/f'{stage}-freeze.json').exists(),'Already frozen')
    require(not list((RT/'runs'/stage).glob('*')),'Existing reservation')
    require(not git('status','--porcelain').strip(),'Unclean continuation')
    require((H/'review/preflight.json').exists(),'Preflight absent');committed(H/'review/preflight.json')
    require(read(H/'review/preflight.json')['passed'],'Preflight failed')
    checkpoint=head();transition('RUNNING',stage);stop=threading.Event();runs=iter(prepared['runs'])
    with ThreadPoolExecutor(max_workers=config()['max_concurrent_processes']) as pool:
        active={}
        def submit():
            item=next(runs,None)
            if item is not None:active[pool.submit(execute,stage,item,checkpoint,stop)]=item
        for _ in range(config()['max_concurrent_processes']):submit()
        while active:
            done,_=wait(active,return_when=FIRST_COMPLETED)
            for future in done:
                future.result();del active[future]
                if not stop.is_set():submit()
    if stop.is_set():raise SystemExit('Measurement paused/terminated; evidence preserved, no automatic retry')
    transition('STAGE_COMPLETE',stage)

def freeze(stage):
    require(state()=='STAGE_COMPLETE','Stage incomplete');verify(True)
    runs=read(H/f'{stage}-prepared.json')['runs'];files={}
    for run in runs:
        uid=run['id'];d=RT/'runs'/stage/uid;require((d/'validation.json').exists(),'Missing result')
        for p in d.iterdir():
            dest=H/'raw'/stage/uid/p.name;raw(dest,p.read_bytes());files[rel(dest)]=sha(dest)
        dest=H/stage/f'{uid}.json';raw(dest,(d/'response.json').read_bytes());files[rel(dest)]=sha(dest)
        if stage=='generation':
            table=c.h5.segment(run['packet_id'],read(dest)['instrument']);p=H/'span-tables'/f'{uid}.json';write(p,table);files[rel(p)]=sha(p)
    write(H/f'{stage}-freeze.json',{'at':now(),'execution_commit':read(RT/'runs'/stage/runs[0]['id']/'attempt.json')['execution_commit'] if runs else None,'runs':runs,'files':files})
    transition('STAGE_FROZEN',stage)

def preflight():
    verify();binary_check();checks=[]
    for directory in ['negative-remainder-calibration-v0.1','inquiry-unitization-calibration-v0.1','span-provenance-calibration-v0.1','natural-admission-v0.1']:
        cmd=([sys.executable,'-B',str(H/'historical.py'),directory] if directory!='natural-admission-v0.1' else [sys.executable,'-B','-m','unittest','discover','-s',str(H/'tests'),'-p','test_*.py'])
        p=subprocess.run(cmd,cwd=R,capture_output=True,text=True,timeout=600)
        checks.append({'command':cmd,'exit_code':p.returncode,'output':p.stdout+p.stderr})
        print(directory,p.returncode,flush=True)
    write(H/'review/preflight.json',{'at':now(),'input_commit':head(),'provider_calls':0,'passed':all(x['exit_code']==0 for x in checks),'checks':checks,'historical_preservation':verify(),'collision_test':'tests/test_h6.py: CollisionTests; synthetic engineering cases excluded from natural counts','official_cli_reference':'https://learn.chatgpt.com/docs/developer-commands?surface=cli','model_reasoning_reference':'https://developers.openai.com/api/docs/guides/reasoning'})
    require(all(x['exit_code']==0 for x in checks),'Preflight failed')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['initial-freeze','prepare','run','freeze','preflight','verify']);p.add_argument('stage',nargs='?',choices=STAGES);a=p.parse_args()
    if a.action in ('prepare','run','freeze'):globals()[a.action](a.stage)
    elif a.action=='initial-freeze':initial_freeze()
    elif a.action=='preflight':preflight()
    else:print(json.dumps(verify(),indent=2))
