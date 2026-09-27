#!/usr/bin/env python3
"""Independent boundary experiment; no imports from or writes to v0.1."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import uuid
import jsonschema
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RUNTIME = ROOT / '.runtime/boundary-v0.2'
DIMS = ('entities','relations','processes','operations','observables','inferences','failure_modes')
CLASSES = ('Native','Adjacent','Remote','Alien')


def require(ok, message):
    if not ok: raise ValueError(message)


def unique(pairs):
    value = {}
    for k,v in pairs:
        require(k not in value, f'Duplicate key: {k}')
        value[k] = v
    return value


class UniqueLoader(yaml.SafeLoader): pass
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader,node: unique([(loader.construct_object(k),loader.construct_object(v)) for k,v in node.value]))


def read(path):
    text = path.read_text()
    return json.loads(text, object_pairs_hook=unique, parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v))) if path.suffix in ('.json','.jsonl') else yaml.load(text, Loader=UniqueLoader)


def sha(data): return hashlib.sha256(data).hexdigest()
def now(): return datetime.now(timezone.utc).isoformat()
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)
def write_new(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as stream: stream.write(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def copy_new(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream: stream.write(data)
def config(): return read(HERE/'execution-config.json')
def order(): return read(HERE/'execution-order.json')


def validate_inputs():
    preserved = read(HERE/'preservation.json')
    for name,digest in preserved['files'].items():
        require(sha((ROOT/name).read_bytes())==digest, f'v0.1 changed: {name}')
    manifest=read(HERE/'operator-manifest.json')
    cases={p.stem:read(p) for p in sorted((HERE/'cases').glob('*.yaml'))}
    require(set(cases)=={f'{n:03}' for n in range(1,17)},'Expected sixteen cases')
    for cid,c in cases.items():
        require(set(c)=={'case_id','source','target'} and c['case_id']==cid,'Invalid case envelope')
        require(set(c['target'])=={'domain','problem'},'Invalid target')
        m=manifest['cases'][cid]; original=read(ROOT/m['source_path'])
        require(original['extraction']['status']=='accepted','Unaccepted instrument')
        require(c['source']=={**{k:original['extraction'][k] for k in ('name','practice')},'instrument':original['instrument']},'Source changed')
        if m['original_control']:
            old=read(ROOT/'distance/cases'/f'{m["original_control"]}.yaml')
            require(c['source']==old['source'] and c['target']==old['target'],'Control content changed')
    for a,b in manifest['identical_targets']: require(cases[a]['target']==cases[b]['target'],'Paired target changed')
    require(len(order())==38 and len({r['id'] for r in order()})==38,'Invalid order')
    expected={(condition,cid,f) for condition,ids in [('primary',cases),('control',['001','003','009'])] for cid in ids for f in ('A','B')}
    require({(r['condition'],r['case_id'],r['family']) for r in order()}==expected,'Run coverage changed')
    jsonschema.Draft202012Validator.check_schema(read(HERE/'output.schema.json'))
    return cases


def packet(run):
    if run['condition']=='control':
        cid=read(HERE/'operator-manifest.json')['cases'][run['case_id']]['original_control']
        return (ROOT/'distance/CLASSIFIER-v0.1.md').read_text()+'\n\nCASE PACKET\n'+(ROOT/'distance/cases'/f'{cid}.yaml').read_text()
    return (HERE/'CLASSIFIER-tested.md').read_text()+'\n\nCASE PACKET\n'+(HERE/'cases'/f'{run["case_id"]}.yaml').read_text()


def schema_path(run): return ROOT/'distance/output.schema.json' if run['condition']=='control' else HERE/'output.schema.json'
def response_id(run): return read(HERE/'operator-manifest.json')['cases'][run['case_id']]['original_control'] if run['condition']=='control' else run['case_id']


def validate_judgment(value,run):
    jsonschema.validate(value,read(schema_path(run)))
    c=value['classification']; require(c['case_id']==response_id(run),'Case ID mismatch')
    require(all(type(c['displacement'][d]['level']) is int for d in DIMS),'Noninteger dimension')
    return c  # Semantic inconsistencies are research data, never coerced.


def build_command(family,cwd,directory,schema,session):
    cfg=config(); model=cfg['families'][family]['requested_model']
    if family=='A':
        cmd=['codex','exec','--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check','--sandbox','read-only','--json','--color','never','--cd',cwd,'--model',model,'-c','model_reasoning_effort="high"','-c','project_doc_max_bytes=0','-c','web_search="disabled"','--output-schema',str(schema),'--output-last-message',str(directory/'response.json')]
        for feature in cfg['codex_disabled_features']:cmd+=['--disable',feature]
        return cmd+['-']
    return ['claude','--print','--safe-mode','--setting-sources','','--settings','{"disableAllHooks":true,"autoMemoryEnabled":false,"enabledPlugins":{"agents-md@builtin":false,"telemetry@builtin":false},"disableClaudeAiConnectors":true,"syncClaudeAiSkills":false,"syncClaudeAiPlugins":false}','--strict-mcp-config','--mcp-config','{"mcpServers":{}}','--tools','','--disable-slash-commands','--no-session-persistence','--session-id',session,'--model',model,'--effort','high','--output-format','stream-json','--verbose','--json-schema',schema.read_text()]


def audit_events(events,family,requested,expected_session=None):
    model_fields=[]
    if family=='A':
        starts=[e for e in events if e.get('type')=='thread.started']
        require(len(starts)==1,'Expected one fresh thread')
        require(sum(e.get('type')=='turn.completed' for e in events)==1,'Incomplete turn')
        require(not any(e.get('type') in ('error','turn.failed') for e in events),'Runner error')
        require(all(e['item'].get('type') in ('agent_message','reasoning') for e in events if 'item' in e),'Unexpected tool activity')
        session=starts[0]['thread_id']
        for i,e in enumerate(events):
            for key in ('model','model_id'):
                if e.get(key): model_fields.append({'value':e[key],'source':f'events[{i}].{key}'})
        retry={'observed_formatting_retries':0,'observability':'No structured retry event exposed; zero observed is not proof of zero internal retries'}
        payload=None
    else:
        init=[e for e in events if e.get('type')=='system' and e.get('subtype')=='init']
        results=[e for e in events if e.get('type')=='result']
        require(len(init)==len(results)==1,'Missing/duplicate init or result')
        session=init[0]['session_id']
        require(session==expected_session,'Session mismatch')
        require(all(not e.get('session_id') or e['session_id']==session for e in events),'Multiple sessions')
        require(not any(init[0].get(k) for k in ('mcp_servers','plugins','skills','slash_commands')),'External context enabled')
        require(not [t for t in init[0].get('tools',[]) if t!='StructuredOutput'],'Tools enabled')
        result=results[0]
        require(result.get('subtype')=='success' and not result.get('is_error'),'Claude unsuccessful')
        tool_calls=[]; tool_errors=[]
        for i,e in enumerate(events):
            if e.get('type')=='system' and e.get('subtype')=='init' and e.get('model'):
                model_fields.append({'value':e['model'],'source':f'events[{i}].model (runner init) '})
            msg=e.get('message',{})
            if isinstance(msg,dict):
                if msg.get('model'):model_fields.append({'value':msg['model'],'source':f'events[{i}].message.model'})
                for block in msg.get('content',[]) if isinstance(msg.get('content'),list) else []:
                    if block.get('type')=='tool_use':
                        require(block.get('name')=='StructuredOutput','Unexpected tool activity')
                        tool_calls.append(block)
                    if block.get('type')=='tool_result' and block.get('is_error'):tool_errors.append(block)
        for model in result.get('modelUsage',{}):model_fields.append({'value':model,'source':'result.modelUsage key'})
        retry={'structured_output_calls':len(tool_calls),'observed_formatting_retries':max(0,len(tool_calls)-1),'tool_error_count':len(tool_errors),'runner_turn_count':result.get('num_turns'),'observability':'Visible StructuredOutput calls/errors; hidden runner reprompts may not be exposed'}
        payload=result.get('structured_output'); require(isinstance(payload,dict),'Missing structured output')
    # Only accept the explicitly requested family/model. Context suffix is a request option.
    base=requested.removesuffix('[1m]')
    require(all(m['value'] in (requested,base) for m in model_fields),'Model fallback or unexpected model identifier')
    require(not any('fallback' in str(e.get('subtype','')).lower() for e in events),'Fallback event')
    returned=sorted({m['value'] for m in model_fields})
    return {'runner_init':{k:v for k,v in (init[0] if family=='B' else starts[0]).items() if k in ('type','subtype','model','tools','mcp_servers','plugins','skills','slash_commands','permissionMode','per_turn_effort_active','claude_code_version')},'internal_transport_retry_events':[{'attempt':e.get('attempt'),'error_status':e.get('error_status'),'retry_delay_ms':e.get('retry_delay_ms')} for e in events if e.get('subtype')=='api_retry'],'session_id':session,'requested_model':requested,'returned_model_identifiers':returned,'model_metadata_provenance':model_fields,'verified_served_snapshot':None,'served_snapshot_note':'Unavailable: returned identifiers, if present, are not a verified immutable serving snapshot','formatting_retries':retry},payload


def execute(family,directory,prompt,schema,run=None):
    directory.mkdir(parents=True,exist_ok=False)
    copy_new(directory/'prompt.txt',prompt.encode())
    session=str(uuid.uuid4()); cfg=config(); cli=cfg['families'][family]['cli']
    with tempfile.TemporaryDirectory(prefix='boundary-isolated-') as cwd:
        cmd=build_command(family,cwd,directory,schema,session)
        # Do not inherit parent-agent session markers or provider/model overrides.
        env={k:v for k,v in os.environ.items() if not k.startswith(('CODEX_','CLAUDE_','ANTHROPIC_','OPENAI_')) and k not in ('CLAUDECODE',)}
        # Auth stays with each CLI's existing on-disk subscription configuration.
        reservation={'run':run,'family':family,'started_at':now(),'packet_sha256':sha(prompt.encode()),'schema_sha256':sha(schema.read_bytes()),'configuration':cfg,'cli_version':subprocess.check_output([cli,'--version'],text=True).strip(),'command':cmd,'working_directory':cwd,'fresh_session_requested':session if family=='B' else 'ephemeral','environment_policy':'Provider overrides and parent session markers removed; subscription authentication on disk','prepared_commit':git('rev-parse','HEAD').decode().strip()}
        write_new(directory/'reservation.json',reservation)
        status='failed'; error=None; metadata=None
        try:
            with (directory/'events.jsonl').open('x') as stdout,(directory/'stderr.txt').open('x') as stderr:
                process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=stdout,stderr=stderr,text=True,cwd=cwd,env=env,start_new_session=True)
                try:process.communicate(prompt,timeout=cfg['timeout_seconds'])
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid,signal.SIGKILL);process.wait();raise
            require(process.returncode==0,f'CLI exit {process.returncode}')
            events=[json.loads(line,object_pairs_hook=unique) for line in (directory/'events.jsonl').read_text().splitlines() if line.strip()]
            metadata,payload=audit_events(events,family,cfg['families'][family]['requested_model'],session)
            if family=='B':write_new(directory/'response.json',payload)
            value=read(directory/'response.json')
            if run:validate_judgment(value,run)
            else:jsonschema.validate(value,read(schema))
            status='valid'
        except Exception as exc:
            error=f'{type(exc).__name__}: {exc}'
        result={'status':status,'error':error,'finished_at':now(),'metadata':metadata}
        write_new(directory/'validation.json',result)
        return result


def preflight(attempt):
    require(attempt.isalnum(), "Use an alphanumeric attempt identifier")
    base=RUNTIME/"preflight"/attempt
    schema=HERE/'probe.schema.json'
    summary={}
    for family in ('A','B'):
        result=execute(family,base/family,'Return JSON with probe equal to "boundary-adapter-ok" and count equal to 3. Use no tools or external context.',schema)
        summary[family]={**result,'cli_version':read(base/family/'reservation.json')['cli_version']}
        print(f'preflight {family}: {result["status"]}',flush=True)
        require(result['status']=='valid',result['error'])
    write_new(HERE/'preflight.json',{'completed_at':now(),'families':summary,'raw_files':{str(p.relative_to(RUNTIME)):sha(p.read_bytes()) for p in sorted((RUNTIME/'preflight').rglob('*')) if p.is_file()}})


def input_paths():
    paths=[p for p in HERE.iterdir() if p.is_file() and p.name not in ('prepared.json','results-freeze.json','metrics.json')]
    paths+=list((HERE/'cases').glob('*.yaml'))+[ROOT/'distance/CLASSIFIER-v0.2-draft.md',ROOT/'docs/PROBLEM_FRAMES.md']
    return sorted(paths)


def prepare():
    validate_inputs();require(all(v['status']=='valid' for v in read(HERE/'preflight.json')['families'].values()),'Preflight incomplete')
    require((HERE/'CLASSIFIER-tested.md').read_bytes()==(ROOT/'distance/CLASSIFIER-v0.2-draft.md').read_bytes(),'Tested snapshot differs')
    write_new(HERE/'prepared.json',{'prepared_at':now(),'files':{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in input_paths()},'packets':{r['id']:sha(packet(r).encode()) for r in order()}})


def verify(committed=False):
    validate_inputs(); m=read(HERE/'prepared.json')
    for name,digest in m['files'].items():require(sha((ROOT/name).read_bytes())==digest,f'Prepared input changed: {name}')
    require(m['packets']=={r['id']:sha(packet(r).encode()) for r in order()},'Packet hash changed')
    if committed:
        for name in [*m['files'],str((HERE/'prepared.json').relative_to(ROOT))]:
            require(git('show',f'HEAD:{name}')==(ROOT/name).read_bytes(),f'Input not committed: {name}')
    return m


def run_all():
    verify(committed=True)
    probes=read(HERE/'preflight.json')['families']
    for family in ('A','B'):
        version=subprocess.check_output([config()['families'][family]['cli'],'--version'],text=True).strip()
        require(version==probes[family]['cli_version'],'CLI version changed after preflight')
    # Exclusive experiment reservation blocks concurrent schedulers and reruns.
    write_new(RUNTIME/'execution-reservation.json',{'started_at':now(),'commit':git('rev-parse','HEAD').decode().strip()})
    for run in order():
        result=execute(run['family'],RUNTIME/'runs'/run['id'],packet(run),schema_path(run),run)
        print(f'{run["id"]}: {result["status"]}',flush=True)
        if result['status']!='valid':
            write_new(RUNTIME/'STOP.json',{'run':run,'error':result['error'],'action':'Scheduling stopped. Document an amendment before any further scheduling.'})
            raise ValueError(result['error'])


def check_runs(entries):
    require(len(entries)==38 and {e['id'] for e in entries}=={r['id'] for r in order()},'Missing/duplicate results')
    sessions=[e['audit']['metadata']['session_id'] for e in entries]
    require(len(set(sessions))==38,'Reused session')


def freeze_results():
    verify(committed=True); entries=[]
    for run in order():
        d=RUNTIME/'runs'/run['id']; audit=read(d/'validation.json')
        require(audit['status']=='valid',f'Invalid {run["id"]}')
        validate_judgment(read(d/'response.json'),run)
        reservation=read(d/'reservation.json')
        events=[json.loads(line,object_pairs_hook=unique) for line in (d/'events.jsonl').read_text().splitlines() if line.strip()]
        metadata,payload=audit_events(events,run['family'],config()['families'][run['family']]['requested_model'],reservation['fresh_session_requested'] if run['family']=='B' else None)
        require(metadata==audit['metadata'],'Audit metadata changed')
        if run['family']=='B':require(payload==read(d/'response.json'),'Structured payload changed')
        require(reservation['schema_sha256']==sha(schema_path(run).read_bytes()),'Schema hash changed')
        require(reservation['packet_sha256']==sha(packet(run).encode()),'Reservation hash changed')
        entries.append({**run,'audit':audit,'reservation':reservation,'files':{p.name:sha(p.read_bytes()) for p in sorted(d.iterdir()) if p.is_file()}})
    check_runs(entries)
    write_new(HERE/'results-freeze.json',{'frozen_at':now(),'prepared_sha256':sha((HERE/'prepared.json').read_bytes()),'runs':entries})


def frozen_results():
    verify();m=read(HERE/'results-freeze.json');require(m['prepared_sha256']==sha((HERE/'prepared.json').read_bytes()),'Preparation freeze changed');check_runs(m['runs']);return m


def publish():
    m=frozen_results()
    for entry in m['runs']:
        d=RUNTIME/'runs'/entry['id']
        for name,digest in entry['files'].items():require(sha((d/name).read_bytes())==digest,'Raw artifact changed')
    for entry in m['runs']:
        copy_new(HERE/'judgments'/f'{entry["id"]}.json',(RUNTIME/'runs'/entry['id']/'response.json').read_bytes())


def side(cls,boundary):return cls in (('Remote','Alien') if boundary=='Adjacent/Remote' else ('Alien',))
def agreement(values):
    n=len(values); c=sum(a==b for a,b in values);return {'n':n,'exact_count':c,'exact_rate':c/n}
def metrics(pairs,axes=True):
    result={'final_class':agreement([(a['final_class'],b['final_class']) for a,b in pairs]),'naturalization':agreement([(a['naturalization']['status'],b['naturalization']['status']) for a,b in pairs]),'dimensions':{d:{**agreement([(a['displacement'][d]['level'],b['displacement'][d]['level']) for a,b in pairs]),'mean_absolute_disagreement':sum(abs(a['displacement'][d]['level']-b['displacement'][d]['level']) for a,b in pairs)/len(pairs)} for d in DIMS},'class_distributions':{f:dict(Counter(pair[i]['final_class'] for pair in pairs)) for i,f in enumerate(('A','B'))},'confusion_matrix':{a:{b:sum(x['final_class']==a and y['final_class']==b for x,y in pairs) for b in CLASSES} for a in CLASSES}}
    if axes:result['axes']={axis:agreement([(a['axes'][axis][key],b['axes'][axis][key]) for a,b in pairs]) for axis,key in [('displacement','level'),('grounding','status')]}
    return result


def analyze():
    m=frozen_results(); data={}
    for entry in m['runs']:
        p=HERE/'judgments'/f'{entry["id"]}.json';require(sha(p.read_bytes())==entry['files']['response.json'],'Published judgment changed')
        data[entry['id']]=validate_judgment(read(p),entry)
    pairs={cid:tuple(data[f'primary-{cid}-{f}'] for f in ('A','B')) for cid in validate_inputs()}
    boundaries={}
    for boundary,ids in [('Adjacent/Remote',[f'{n:03}' for n in range(1,9)]),('Remote/Alien',[f'{n:03}' for n in range(9,17)])]:
        ps=[pairs[cid] for cid in ids]; s=agreement([(side(a['final_class'],boundary),side(b['final_class'],boundary)) for a,b in ps])
        boundaries[boundary]={'cases':ids,'side_agreement':s,'agreement_criterion_met':s['exact_count']>=6,'both_sides_exercised':len({side(c['final_class'],boundary) for p in ps for c in p})==2,'exact_and_dimensions':metrics(ps),'out_of_band':{cid:{f:pairs[cid][i]['final_class'] for i,f in enumerate(('A','B')) if pairs[cid][i]['final_class'] not in boundary.split('/')} for cid in ids if any(c['final_class'] not in boundary.split('/') for c in pairs[cid])},'side_disagreements':[cid for cid in ids if side(pairs[cid][0]['final_class'],boundary)!=side(pairs[cid][1]['final_class'],boundary)]}
    comparisons={}
    for cid in ('001','003','009'):
        old=read(HERE/'operator-manifest.json')['cases'][cid]['original_control']
        orig=[read(ROOT/'distance/judgments'/f'{old}-{f}.json')['classification']['final_class'] for f in ('A','B')]
        ctrl=[data[f'control-{cid}-{f}']['final_class'] for f in ('A','B')];new=[c['final_class'] for c in pairs[cid]]
        comparisons[cid]={'original_case':old,'original_v01_same_family_A_B':orig,'new_v01_cross_family_A_B':ctrl,'new_v02_cross_family_A_B':new,'new_v01_resolved':ctrl[0]==ctrl[1],'new_v02_resolved':new[0]==new[1]}
    return {'primary':metrics(list(pairs.values())),'boundaries':boundaries,'supplementary':metrics([tuple(data[f'control-{cid}-{f}'] for f in ('A','B')) for cid in ('001','003','009')],axes=False),'control_comparisons':comparisons}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['validate','preflight','prepare','verify','run','freeze-results','publish','analyze']);p.add_argument('--attempt',default='initial');args=p.parse_args()
    actions={'validate':validate_inputs,'preflight':lambda:preflight(args.attempt),'prepare':prepare,'verify':verify,'run':run_all,'freeze-results':freeze_results,'publish':publish,'analyze':analyze}
    value=actions[args.command]()
    if args.command=='analyze':write_new(HERE/'metrics.json',value)
    print(f'{args.command}: OK')
if __name__=='__main__':main()
