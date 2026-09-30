#!/usr/bin/env python3
"""Experiment F: immutable inputs, one sequential attempt, fail-closed publication."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import argparse
import importlib.util
import json
import os
import signal
import subprocess
import tempfile
import contracts as c

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
RUNTIME=ROOT/'.runtime/prospective-validity-v0.1'
spec=importlib.util.spec_from_file_location('f_historical_event_audit',ROOT/'distance/boundary-v0.2/harness.py')
legacy=importlib.util.module_from_spec(spec); spec.loader.exec_module(legacy)

def now(): return datetime.now(timezone.utc).isoformat()
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)
def head(): return git('rev-parse','HEAD').decode().strip()
def rel(p): return str(p.relative_to(ROOT))
def config(): return c.read(HERE/'execution-config.json')
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f: json.dump(v,f,indent=2,ensure_ascii=False); f.write('\n')
def copy(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f: f.write(b)
def inventory(paths): return {rel(p):c.sha(p) for p in sorted(paths) if p.is_file() and '__pycache__' not in p.parts}
def verify_hashes(files):
    for name,h in files.items(): c.require(c.sha(ROOT/name)==h,'Frozen bytes changed: '+name)
def committed(p,commit='HEAD'): c.require(git('show',f'{commit}:{rel(p)}')==p.read_bytes(),'Uncommitted input: '+rel(p))
def checkpoint(p):
    committed(p)
    return git('log','-1','--format=%H','--',rel(p)).decode().strip()
def order(stage): return c.read(HERE/'execution-orders'/f'{stage}.json')['order']
def packet(stage,identity): return (HERE/'packets'/stage/f'{identity}.txt').read_text()

def clean_environment():
    # Preserve ordinary OS and subscription-auth discovery; never copy auth data.
    return {k:v for k,v in os.environ.items() if not k.startswith(('CODEX_','CLAUDE_','ANTHROPIC_','OPENAI_','AZURE_OPENAI_','GEMINI_','GOOGLE_GENAI_')) and k not in ('CLAUDECODE','MODEL_PROVIDER','MODEL','LLM_MODEL')}

def binary_check():
    cfg=config(); cli=cfg['families']['A']['cli']
    c.require(cfg['families']=={'A':{'cli':cli,'requested_model':'gpt-6-astra','effort':'high'}},'Only Astra/high authorized')
    c.require(c.sha(cli)==cfg['executable_sha256']['A'],'Pinned CLI changed')
    native=cfg['native_executable']; c.require(c.sha(native['path'])==native['sha256'],'Native CLI changed')
    version=subprocess.check_output([cli,'--version'],text=True).strip()
    c.require(version=='codex-cli 0.157.1','CLI version changed')
    return version

def command(cwd,d,stage):
    cfg=config()
    # Established E route and fixed flags; no historical runner mutation.
    cmd=[cfg['families']['A']['cli'],'exec','--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check','--sandbox','read-only','--json','--color','never','--cd',str(cwd),'--model','gpt-6-astra','-c','model_reasoning_effort="high"','-c','project_doc_max_bytes=0','-c','web_search="disabled"','--output-schema',str(HERE/'schemas'/f'{stage}-wire.schema.json'),'--output-last-message',str(d/'response.json')]
    for feature in cfg['codex_disabled_features']: cmd += ['--disable',feature]
    return cmd+['-']

def verify_imports():
    parents=c.read(HERE/'condition-inventory/parents.json'); atoms=c.read(HERE/'condition-inventory/atomic.json')
    c.require(len(parents)==139 and Counter(p['original_family'] for p in parents)=={'A':52,'B':87},'Parent coverage')
    byid={p['parent_condition_id']:p for p in parents}
    c.require(len(byid)==len(parents) and {a['parent_condition_id'] for a in atoms}==set(byid),'Parent/child coverage')
    c.require(len({a['atomic_condition_id'] for a in atoms})==len(atoms),'Atomic identity collision')
    for p in parents:
        j=c.read(ROOT/p['source']['path']); i=int(p['source_field'].split('/')[-1])
        c.require(j['validity']['unresolved_conditions'][i]==p['verbatim_condition'],'Parent source mismatch')
        c.require(c.sha(ROOT/p['source']['path'])==p['source']['sha256'],'Parent source hash')
        c.require(p['original_criterion'] is None,'Inferred criterion attribution')
    all_lists=sum(len(c.read(p)['validity']['unresolved_conditions']) for p in (HERE/'imports/historical-judgments').glob('*.json'))
    c.require(all_lists==len(parents),'Missing historical condition')
    c.require(len(list((HERE/'imports/historical-judgments').glob('*.json')))==60,'Historical judgment coverage')
    for a in atoms:
        p=byid[a['parent_condition_id']]; text=p['verbatim_condition']
        c.require(text[a['span_start']:a['span_end']]==a['atomic_text'] and a['shared_qualifying_context']==text,'Atomic span/context drift')
        c.require(not set(a).intersection({'category','classification','expected_category'}),'Extraction categorized')
        body={**c.read(HERE/'imports/candidates'/f'{a["case_id"]}.json'),'condition_id':a['atomic_condition_id'],'atomic_condition':a['atomic_text'],'necessary_source_excerpt':text}
        expected=(HERE/'TAXONOMY.md').read_text()+'\nCASE PACKET\n'+json.dumps(body,indent=2,ensure_ascii=False)+'\n'
        c.require(packet('taxonomy',a['atomic_condition_id'])==expected,'Taxonomy packet not allowlisted')
    c.require(set(order('taxonomy'))=={a['atomic_condition_id'] for a in atoms} and len(order('taxonomy'))==len(atoms),'Taxonomy schedule coverage')
    manifest=c.read(HERE/'operator-manifest.json')
    c.require(len(manifest['cases'])==30,'Mapping coverage')
    for row in manifest['cases']:
        cid=row['case_id']; src=ROOT/row['generation']['path']; imported=HERE/'imports/generations'/f'{cid}.json'
        c.require(src.read_bytes()==imported.read_bytes() and c.sha(imported)==row['generation']['sha256'],'Exact import mismatch')
        inp=c.read(ROOT/row['input']['path']); candidate=c.read(HERE/'imports/candidates'/f'{cid}.json')
        c.require(candidate=={'source':inp['source'],'target':{**inp['target'],'evidence':[]},'mapping':c.read(src)['mapping']},'Candidate drift')
    c.require('novelty effects' in json.dumps(c.read(HERE/'imports/candidates/E029.json')),'E029 wording lost')
    return len(atoms)

def verify(stage=None,check_committed=False):
    verify_hashes(c.read(HERE/'preservation.json')['files']); verify_imports()
    stages=[stage] if stage else [s for s in ('taxonomy','prospective') if (HERE/f'{s}-prepared.json').exists()]
    for s in stages:
        p=HERE/f'{s}-prepared.json'; prep=c.read(p); verify_hashes(prep['files'])
        if check_committed:
            committed(p)
            # A single tree snapshot covers immutable preparation without one git
            # process per packet on each measurement.
            for name in prep['files']: committed(ROOT/name)
        for name in ('','-wire'):
            schema=c.read(HERE/'schemas'/f'{s}{name}.schema.json')
            c.jsonschema.Draft202012Validator.check_schema(schema)
        c.require(c.read(HERE/'schemas'/f'{s}-wire.schema.json')==c.wire(c.read(HERE/'schemas'/f'{s}.schema.json')),'Wire projection changed')
    return {'parents':139,'atomic':len(c.read(HERE/'condition-inventory/atomic.json')),'historical_bytes_preserved':True}

def freeze_preparation(stage):
    c.require(stage=='taxonomy' or (HERE/'review/taxonomy-audit.json').exists(),'Taxonomy audit required')
    if stage=='prospective': committed(HERE/'review/taxonomy-audit.json')
    paths=list(HERE.rglob('*'))+[ROOT/'docs/PROBLEM_FRAMES.md', ROOT/'docs/HANDOFF-prospective-validity.md', ROOT/'distance/boundary-v0.2/harness.py']
    # Prior result freezes included for chronology; private runtime excluded.
    write(HERE/f'{stage}-prepared.json',{'at':now(),'parent_commit':head(),'stage':stage,'files':inventory(paths),'order':order(stage)})
    verify(stage)

def probe_fixture(stage):
    if stage=='taxonomy': return {'condition_id':'ARTIFICIAL','category':'execution_precondition','rationale':'A visible-token count is coherent before access is granted.','if_execution':{'verification_or_satisfaction_method':'Obtain access to the transparent token box.'},'if_validity_relevant':None,'uncertainty':[]}
    return {'case_id':'ARTIFICIAL','mechanism_fidelity':{'status':'preserved','rationale':'Count visible tokens.'},'warrant_validity':{'status':'supported','rationale':'A complete exact count supports the number of visible tokens.'},'target_fidelity':{'status':'addressed','rationale':'The question asks the token count.'},'conditions':[{'condition':'Obtain access to the box.','category':'execution_precondition','rationale':'Access enables counting.','effect_on_validity':'none'}],'execution_readiness':{'status':'requires_preconditions','preconditions':[{'condition':'Obtain access to the box.','how_to_establish':'Arrange access.','why_execution_only':'Does not change the counting inference.'}],'rationale':'The box is not yet accessible.'},'final_status':'Valid','uncertainty':[]}

def audit_events(events):
    metadata,_=legacy.audit_events(events,'A','gpt-6-astra')
    # Inspect nested returned identifiers too; preserve provenance, fail on substitution.
    found=[]
    def walk(v,path):
        if isinstance(v,dict):
            for k,x in v.items():
                if k in ('model','model_id','model_name') and isinstance(x,str): found.append({'value':x,'source':path+'.'+k})
                if 'fallback' in k.lower() and x: raise ValueError('Fallback event')
                walk(x,path+'.'+k)
        elif isinstance(v,list):
            for i,x in enumerate(v): walk(x,f'{path}[{i}]')
    walk(events,'events')
    c.require(all(x['value']=='gpt-6-astra' for x in found),'Observed model substitution')
    metadata['returned_model_identifiers']=sorted({x['value'] for x in found})
    metadata['model_metadata_provenance']=found
    metadata['served_model_identifier']=metadata['returned_model_identifiers'] or None
    metadata['usage']=[e.get('usage') for e in events if e.get('type')=='turn.completed']
    return metadata

def execute(stage,identity,prompt,kind):
    d=RUNTIME/kind/stage/identity
    # Atomic exclusive directory reservation precedes ALL launch preparation.
    d.mkdir(parents=True,exist_ok=False)
    write(d/'attempt.json',{'at':now(),'stage':stage,'identity':identity,'kind':kind,'input_commit':head(),'harness_attempt':1})
    copy(d/'prompt.txt',prompt.encode()); metadata=None; error=None; status='failed'
    try:
        version=binary_check(); cfg=config()
        with tempfile.TemporaryDirectory(prefix='f-isolated-') as cwd:
            c.require(not list(Path(cwd).iterdir()),'Nonempty working directory')
            cmd=command(cwd,d,stage)
            write(d/'reservation.json',{'started_at':now(),'input_commit':head(),'kind':kind,'identity':identity,'stage':stage,'packet_sha256':c.digest(prompt.encode()),'canonical_schema_sha256':c.sha(HERE/'schemas'/f'{stage}.schema.json'),'wire_schema_sha256':c.sha(HERE/'schemas'/f'{stage}-wire.schema.json'),'configuration':cfg,'cli_version':version,'command':cmd,'working_directory':cwd,'working_directory_initially_empty':True,'requested_session':'ephemeral','environment_policy':'Provider overrides and parent context removed; subscription authentication remains on disk.'})
            with (d/'events.jsonl').open('x') as out,(d/'stderr.txt').open('x') as err:
                process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=out,stderr=err,text=True,cwd=cwd,env=clean_environment(),start_new_session=True)
                write(d/'process.json',{'pid':process.pid,'parent_pid':os.getpid(),'launched_at':now()})
                try: process.communicate(prompt,timeout=900)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid,signal.SIGKILL); process.wait(); raise
            write(d/'exit.json',{'returncode':process.returncode,'at':now()})
            c.require(process.returncode==0,f'CLI exit {process.returncode}')
            events=[json.loads(line,object_pairs_hook=c.unique) for line in (d/'events.jsonl').read_text().splitlines() if line.strip()]
            metadata=audit_events(events)
            for p in RUNTIME.rglob('validation.json'):
                previous=c.read(p).get('metadata')
                c.require(not previous or previous['session_id']!=metadata['session_id'],'Reused session')
            finals=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
            c.require(len(finals)==1 and (d/'response.json').exists(),'Missing/duplicate final')
            c.require(finals[0].strip()==(d/'response.json').read_text().strip(),'Stream/response mismatch')
            value=c.read(d/'response.json'); c.validate(value,stage,identity)
            if kind=='probes': c.require(value==probe_fixture(stage),'Artificial fixture mismatch')
            status='valid'
    except Exception as exc: error=type(exc).__name__+': '+str(exc)
    result={'status':status,'error':error,'finished_at':now(),'metadata':metadata}
    write(d/'validation.json',result)
    return {'identity':identity,'kind':kind,'validation':result,'reservation':c.read(d/'reservation.json') if (d/'reservation.json').exists() else None,'files':inventory(d.iterdir())}

def stopped(): c.require(not (RUNTIME/'STOP.json').exists(),'Scheduling stopped; no retry/replacement authorized')
def stop(stage,error):
    if not (RUNTIME/'STOP.json').exists(): write(RUNTIME/'STOP.json',{'at':now(),'stage':stage,'error':str(error),'policy':'Stop all scheduling; publish incomplete evidence; no retry or replacement.'})

def preflight(stage):
    stopped()
    write(RUNTIME/f'{stage}-probe-reservation.json',{'at':now(),'commit':head()})
    try:
        verify(stage,True)
        value=probe_fixture(stage)
        result=execute(stage,'ARTIFICIAL','Return exactly this artificial schema fixture. No classification, tools or external context.\n'+json.dumps(value), 'probes')
        c.require(result['validation']['status']=='valid',result['validation']['error'])
        write(HERE/'probes'/f'{stage}.json',{'at':now(),'input_commit':head(),'prepared_sha256':c.sha(HERE/f'{stage}-prepared.json'),'entry':result})
        print('Successful artificial '+stage+' probe',flush=True)
    except Exception as exc: stop(stage,exc); raise

def run(stage):
    stopped()
    write(RUNTIME/f'{stage}-reservation.json',{'at':now(),'commit':head()})
    try:
        verify(stage,True); probe=HERE/'probes'/f'{stage}.json'; committed(probe)
        p=c.read(probe); c.require(p['entry']['validation']['status']=='valid' and p['prepared_sha256']==c.sha(HERE/f'{stage}-prepared.json'),'Preflight binding')
        verify_hashes(p['entry']['files']); initial=head()
        for i,identity in enumerate(order(stage),1):
            stopped(); c.require(head()==initial,'Commit changed during collection')
            verify_hashes(c.read(HERE/f'{stage}-prepared.json')['files'])
            result=execute(stage,identity,packet(stage,identity),'runs')
            print(f'{stage} {i}/{len(order(stage))} {identity}: {result["validation"]["status"]}',flush=True)
            c.require(result['validation']['status']=='valid',result['validation']['error'])
    except Exception as exc: stop(stage,exc); raise

def freeze(stage):
    stopped(); verify(stage,True); entries=[]
    for identity in order(stage):
        d=RUNTIME/'runs'/stage/identity; v=c.read(d/'validation.json')
        c.require(v['status']=='valid','Cannot complete partial stage')
        c.validate(c.read(d/'response.json'),stage,identity)
        copy(HERE/('taxonomy-judgments' if stage=='taxonomy' else 'judgments')/f'{identity}.json',(d/'response.json').read_bytes())
        entries.append({'identity':identity,'validation':v,'reservation':c.read(d/'reservation.json'),'files':inventory(d.iterdir()),'response_sha256':c.sha(d/'response.json')})
    write(HERE/f'{stage}-freeze.json',{'at':now(),'prepared_sha256':c.sha(HERE/f'{stage}-prepared.json'),'execution_commit':c.read(RUNTIME/f'{stage}-reservation.json')['commit'],'runs':entries})

def freeze_failure():
    write(HERE/'failure-freeze.json',{'at':now(),'stop':c.read(RUNTIME/'STOP.json'),'files':inventory(RUNTIME.rglob('*')),'attempts':[c.read(p) for p in sorted(RUNTIME.rglob('attempt.json'))],'successful_probes':[p.stem for p in (HERE/'probes').glob('*.json')],'status':'incomplete'})

def main():
    p=argparse.ArgumentParser(); p.add_argument('action',choices=['prepare-freeze','verify','preflight','run','freeze','freeze-failure']); p.add_argument('--stage',choices=['taxonomy','prospective'],default='taxonomy'); a=p.parse_args()
    if a.action=='prepare-freeze': freeze_preparation(a.stage)
    elif a.action=='verify': print(json.dumps(verify()))
    elif a.action=='preflight': preflight(a.stage)
    elif a.action=='run': run(a.stage)
    elif a.action=='freeze': freeze(a.stage)
    else: freeze_failure()
if __name__=='__main__': main()
