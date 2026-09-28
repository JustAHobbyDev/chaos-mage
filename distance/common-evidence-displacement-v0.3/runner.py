#!/usr/bin/env python3
"""B.2 guarded authoring freezes, admission, and isolated two-stage measurement."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import tempfile
import uuid
import contracts as c
import derive
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
RUNTIME=ROOT/'.runtime/common-evidence-displacement-v0.3'
spec=importlib.util.spec_from_file_location('b2_frozen_event_audit',ROOT/'distance/boundary-v0.2/harness.py')
legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
read,require=c.read,c.require
STAGES=('validity','prospective','consequence')
TITLES={'worlds':'Freeze B.2 common worlds and baselines','prepared':'Prepare common-evidence displacement Experiment B.2',
        'preflight':'Freeze B.2 provider probes','admission':'Freeze B.2 validity admission and pair packets',
        'prospective':'Freeze B.2 prospective results','consequence':'Freeze B.2 consequence results'}
def now():return datetime.now(timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def config():return read(HERE/'execution-config.json')
def manifest():return read(HERE/'operator-manifest.json')['mappings']
def candidate(mid):return read(HERE/'mappings'/f'{mid}.json')
def canonical(stage):return HERE/'schemas'/('validity.schema.json' if stage=='validity' else 'output.schema.json')
def order_path(stage):return HERE/({'validity':'validity-order.json','prospective':'execution-order-stage-a.json','consequence':'execution-order-stage-b.json'}[stage])
def order(stage):return read(order_path(stage))
def write_new(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as f:f.write(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def copy_new(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:f.write(data)
def projection(value):
    if isinstance(value,dict):return {k:projection(v) for k,v in value.items() if k not in ('$schema','$id','allOf')}
    if isinstance(value,list):return [projection(v) for v in value]
    return value
def inventory(paths):return {str(p.relative_to(ROOT)):c.sha(p) for p in sorted(paths) if p.is_file() and '__pycache__' not in p.parts}
def verify_inventory(files):
    for name,digest in files.items():require(c.sha(ROOT/name)==digest,'Changed frozen file: '+name)
def preservation(private=False):
    value=read(HERE/'preservation.json');verify_inventory(value['files'])
    if private:verify_inventory(value['private_files'])
def committed(path,revision='HEAD'):require(git('show',f'{revision}:{path.relative_to(ROOT)}')==path.read_bytes(),'Uncommitted input: '+str(path))
def checkpoint(name):return git('log','-1','--format=%H','--',str(HERE/name)).decode().strip()
def check_commit(name,title):
    revision=checkpoint(name);require(git('show','-s','--format=%s',revision).decode().strip()==title,'Missing checkpoint: '+title);return revision
def validate_inputs():
    import yaml
    preservation();wf=read(HERE/'worlds-freeze.json');verify_inventory(wf['files']);world_commit=check_commit('worlds-freeze.json',TITLES['worlds'])
    rows=manifest();require(len(rows)==20 and len({x['mapping_id'] for x in rows})==20,'Twenty unique mappings required')
    for row in rows:
        tid,mid=row['target_id'],row['mapping_id'];common=c.validate(read(HERE/'common-states'/f'{tid}.json'),'common-state')
        world=c.validate(read(HERE/'worlds'/f'{tid}.json'),'world')
        require(world['observable_start']==common,'World/common state mismatch')
        require(row['world_commit']==world_commit,'Mapping not bound to world checkpoint')
        base=(HERE/'baselines'/f'{tid}.json').read_bytes()
        require(base==(HERE.parent/'comparative-displacement-v0.3/baselines'/f'{tid}.json').read_bytes(),'Baseline changed')
        require(json.loads(base)==common['native_baseline'],'Common baseline changed')
        require(common['target']['question']==common['native_baseline']['target_task'] and common['target']['domain']==common['native_baseline']['target_domain'],'Baseline identity mismatch')
        value=c.validate(candidate(mid),'candidate')
        require(value['case_id']==mid,'Mapping identity mismatch')
        require(value['target']=={**common['target'],'evidence':[json.dumps(common,ensure_ascii=False,sort_keys=True)]},'Non-common initial evidence')
        source=yaml.safe_load((ROOT/row['source_path']).read_text())
        require(source['extraction']['status']=='accepted' and value['source']=={'name':source['extraction']['name'],'practice':source['extraction']['practice'],'instrument':source['instrument']},'Source changed')
        c.validate_outcome(row,read(HERE/'outcomes'/f'{mid}.json'))
    require((HERE/'CLASSIFIER-validity.md').read_bytes()==(HERE.parent/'v0.3/CLASSIFIER-transfer-validity.md').read_bytes(),'Validity classifier changed')
    require((HERE/'schemas/validity.schema.json').read_bytes()==(HERE.parent/'v0.3/validity.schema.json').read_bytes(),'Validity schema changed')
    for stage in STAGES:require(read(HERE/'schemas'/f'{stage}-wire.schema.json')==projection(read(canonical(stage))),'Wire projection mismatch')
    require(len(read(HERE/'operator-manifest.json')['pair_designs'])==16,'Sixteen planned pairs required')
    return True
def pair_records():return read(HERE/'pairs/pairs.json')
def comparison_packet(pair,stage):
    require(stage in ('prospective','consequence'),'Unknown displacement stage')
    body={'case_id':pair['case_id'],'stage':stage}
    for slot in 'AB':
        mid=pair['mapping_'+slot];value=candidate(mid)
        body['mapping_'+slot]={'source':value['source'],'mapping':value['mapping']}
        if stage=='consequence':body['mapping_'+slot]['realized']=derive.public_outcome(read(HERE/'outcomes'/f'{mid}.json'))
    # Exact common-state file bytes appear once, shared by both branches and stages.
    common=(HERE/'common-states'/f'{pair["target_id"]}.json').read_bytes()
    packet=json.dumps(body,indent=2,ensure_ascii=False)[:-2]+',\n  "common_start": '+common.decode()+'}\n'
    require(common in packet.encode(),'Missing exact common-state bytes');json.loads(packet)
    return (HERE/'CLASSIFIER.md').read_text()+'\n\nCASE PACKET\n'+packet
def packet(run,stage='validity'):
    if stage=='validity':return (HERE/'CLASSIFIER-validity.md').read_text()+'\n\nCASE PACKET\n'+json.dumps(candidate(run['case_id']),indent=2,ensure_ascii=False)+'\n'
    pair=next(p for p in pair_records() if p['case_id']==run['case_id'])
    return comparison_packet(pair,stage)
def validate_response(value,stage,run):
    return c.validate(value,stage,candidate(run['case_id']) if run and stage=='validity' else {'case_id':run['case_id']} if run else None)
def check_fresh_session(session,directory):
    require(bool(session),'Missing session')
    for p in RUNTIME.rglob('validation.json'):
        if p.parent!=directory:
            meta=read(p).get('metadata');require(not meta or meta['session_id']!=session,'Duplicate session across stages')

# Provider adapter definitions copied from frozen B.1 with B.2 schema paths.
def build_command(family, cwd, directory, session, stage="validity"):
    cfg = config(); model = cfg['families'][family]['requested_model']
    schema = HERE / 'schemas' / f'{stage}-wire.schema.json'
    if family == 'A':
        cmd = ['codex', 'exec', '--ignore-user-config', '--ignore-rules', '--ephemeral',
               '--skip-git-repo-check', '--sandbox', 'read-only', '--json', '--color', 'never',
               '--cd', str(cwd), '--model', model, '-c', 'model_reasoning_effort="high"',
               '-c', 'project_doc_max_bytes=0', '-c', 'web_search="disabled"',
               '--output-schema', str(schema), '--output-last-message', str(directory / 'response.json')]
        for feature in cfg['codex_disabled_features']: cmd += ['--disable', feature]
        return cmd + ['-']
    settings = {'disableAllHooks': True, 'autoMemoryEnabled': False,
                'enabledPlugins': {'agents-md@builtin': False, 'telemetry@builtin': False},
                'disableClaudeAiConnectors': True, 'syncClaudeAiSkills': False,
                'syncClaudeAiPlugins': False}
    return ['claude', '--print', '--safe-mode', '--setting-sources', '', '--settings', json.dumps(settings),
            '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}', '--tools', '',
            '--disable-slash-commands', '--no-session-persistence', '--session-id', session,
            '--model', model, '--effort', 'high', '--output-format', 'stream-json', '--verbose',
            '--json-schema', schema.read_text()]


def clean_environment():
    return {k: v for k, v in os.environ.items()
            if not k.startswith(('CODEX_', 'CLAUDE_', 'ANTHROPIC_', 'OPENAI_'))
            and k not in ('CLAUDECODE',)}


def events_at(directory):
    return [json.loads(line, object_pairs_hook=c.unique_object)
            for line in (directory / 'events.jsonl').read_text().splitlines() if line.strip()]


def audit(directory, family, session):
    events = events_at(directory)
    metadata, payload = legacy.audit_events(events, family,
        config()['families'][family]['requested_model'], session if family == 'B' else None)
    response = read(directory / 'response.json')
    if family == 'B':
        require(payload == response, 'Structured payload differs from retained response')
    else:
        finals = [e['item']['text'] for e in events if e.get('type') == 'item.completed'
                  and e.get('item', {}).get('type') == 'agent_message']
        require(len(finals) == 1, 'Expected one completed final response')
        require(json.loads(finals[0], object_pairs_hook=c.unique_object) == response,
                'Final event differs from retained response')
    return metadata


def adapter_execute(family, directory, prompt, run=None, stage="validity"):
    directory.mkdir(parents=True, exist_ok=False)
    copy_new(directory / 'prompt.txt', prompt.encode())
    session = str(uuid.uuid4()); cfg = config(); cli = cfg['families'][family]['cli']
    with tempfile.TemporaryDirectory(prefix='b2-isolated-') as cwd:
        cmd = build_command(family, cwd, directory, session, stage)
        version = subprocess.check_output([cli, '--version'], text=True).strip()
        require(version == cfg['expected_cli_versions'][family], 'CLI version changed')
        reservation = {'run': run, 'family': family, 'started_at': now(),
                       'packet_sha256': sha(prompt.encode()),
                       'schema_sha256': c.sha(HERE / 'schemas' / f'{stage}-wire.schema.json'),
                       'canonical_schema_sha256': c.sha(canonical(stage)),
                       'configuration': cfg, 'cli_version': version, 'command': cmd,
                       'working_directory': cwd, 'fresh_session_requested': session if family == 'B' else 'ephemeral',
                       'environment_policy': 'Provider/model overrides and parent agent markers removed; existing on-disk subscription authentication',
                       'prepared_commit': git('rev-parse', 'HEAD').decode().strip()}
        write_new(directory / 'reservation.json', reservation)
        status = 'failed'; error = None; metadata = None
        try:
            with (directory / 'events.jsonl').open('x') as stdout, (directory / 'stderr.txt').open('x') as stderr:
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                                           text=True, cwd=cwd, env=clean_environment(), start_new_session=True)
                try: process.communicate(prompt, timeout=cfg['timeout_seconds'])
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL); process.wait(); raise
            # Preserve an available structured response before any validation, even on failure.
            if family == 'B':
                payloads = [e['structured_output'] for e in events_at(directory)
                            if e.get('type') == 'result' and isinstance(e.get('structured_output'), dict)]
                if len(payloads) == 1: write_new(directory / 'response.json', payloads[0])
            require(process.returncode == 0, f'CLI exit {process.returncode}')
            metadata = audit(directory, family, session)
            value = read(directory / 'response.json')
            validate_response(value, stage, run)
            if run is None: require(value == probe_response(stage), 'Preflight response differs from specified fixture')
            check_fresh_session(metadata['session_id'], directory)
            status = 'valid'
        except Exception as exc:
            error = f'{type(exc).__name__}: {exc}'
        result = {'status': status, 'error': error, 'finished_at': now(), 'metadata': metadata}
        write_new(directory / 'validation.json', result)
        return result




def probe_response(stage='validity'):
    if stage=='validity':return {'case_id':'PREFLIGHT','validity':{'mechanism_fidelity':{'status':'preserved','rationale':'Formatting fixture only.'},'target_fidelity':{'status':'addressed','rationale':'Formatting fixture only.'},'operational_coherence':{'status':'coherent','rationale':'Formatting fixture only.'},'target_reframe':{'occurred':False,'original_question':None,'reframed_question':None,'relationship':None},'unresolved_conditions':[],'final_status':'Valid','rationale':'Formatting fixture only.'},'uncertainty':[]}
    return {'case_id':'PREFLIGHT','stage':stage,'meaningful_difference':{'status':'no','rationale':'Formatting fixture only.'},
            'criteria':{k:{'relation':'balanced','rationale':'Formatting fixture only.'} for k in c.CRITERIA},
            'consequence_structure':{k:{'relation':'balanced','rationale':'Formatting fixture only.'} for k in c.DIAGNOSTICS},
            'decisive_basis':{k:'Formatting fixture only.' for k in ('most_important_difference',*c.DIAGNOSTICS,'rationale')},
            'overall_relation':'approximately_equal','confidence':'clear','uncertainty':[]}
def prepare():
    validate_inputs();preservation(True)
    schedule=[{'id':f'validity-{row["mapping_id"]}-{f}','case_id':row['mapping_id'],'family':f} for row in manifest() for f in 'AB']
    random.Random(read(HERE/'design.json')['seeds']['validity']).shuffle(schedule);write_new(order_path('validity'),schedule)
    paths=list(HERE.rglob('*'))+[ROOT/'docs/PROBLEM_FRAMES-common-evidence-displacement-v0.3.md']
    write_new(HERE/'prepared.json',{'created_at':now(),'world_commit':checkpoint('worlds-freeze.json'),'files':inventory(paths),
              'validity_packets':{r['id']:sha(packet(r).encode()) for r in schedule}})
def verify(committed_inputs=False):
    validate_inputs();value=read(HERE/'prepared.json');verify_inventory(value['files'])
    require(value['validity_packets']=={r['id']:sha(packet(r).encode()) for r in order('validity')},'Validity packet changed')
    require(len(order('validity'))==40 and {(r['case_id'],r['family']) for r in order('validity')}=={(m['mapping_id'],f) for m in manifest() for f in 'AB'},'Validity coverage')
    if committed_inputs:
        for name in [*value['files'],str((HERE/'prepared.json').relative_to(ROOT))]:committed(ROOT/name)
        prep=check_commit('prepared.json',TITLES['prepared']);require(git('merge-base',value['world_commit'],prep).decode().strip()==value['world_commit'],'World checkpoint ancestry')
    return value
def execute(family,directory,prompt,run=None,stage='validity'):
    # Also preserve setup/version failures that occur before the adapter's process try.
    require(not directory.exists(),'Attempt already reserved; no retry')
    try:return adapter_execute(family,directory,prompt,run,stage)
    except Exception as exc:
        directory.mkdir(parents=True,exist_ok=True)
        if not (directory/'prompt.txt').exists():copy_new(directory/'prompt.txt',prompt.encode())
        value={'status':'failed','error':f'{type(exc).__name__}: {exc}','finished_at':now(),'metadata':None}
        write_new(directory/'validation.json',value);return value
def preflight():
    verify(True);write_new(RUNTIME/'preflight-reservation.json',{'at':now(),'commit':git('rev-parse','HEAD').decode().strip()});entries=[]
    try:
        for stage in STAGES:
            for family in 'AB':
                verify(True);d=RUNTIME/'preflight'/stage/family
                result=execute(family,d,'Return exactly this artificial formatting fixture; no classification, tools or external context.\n'+json.dumps(probe_response(stage)),stage=stage)
                print(f'probe {stage} {family}: {result["status"]}',flush=True);entries.append({'stage':stage,'family':family,'audit':result})
                require(result['status']=='valid',result['error'])
    except Exception as exc:
        write_new(RUNTIME/'STOP.json',{'stage':'preflight','at':now(),'error':str(exc)});raise
    write_new(HERE/'preflight.json',{'frozen_at':now(),'prepared_sha256':c.sha(HERE/'prepared.json'),'entries':entries,'files':inventory((RUNTIME/'preflight').rglob('*'))})
def prerequisites(stage):
    verify(True);probe=read(HERE/'preflight.json');committed(HERE/'preflight.json');check_commit('preflight.json',TITLES['preflight'])
    verify_inventory(probe['files']);require(len(probe['entries'])==6 and all(x['audit']['status']=='valid' for x in probe['entries']),'Six successful probes required')
    require(not (RUNTIME/'STOP.json').exists(),'Scheduling stopped; explicit recorded recovery required')
    if stage!='validity':verify_admission(True);require(bool(pair_records()),'No eligible pairs')
    if stage=='consequence':
        # Metadata-only gate: no Stage A judgment file is read by this path.
        frozen('prospective');committed(HERE/'prospective-freeze.json');check_commit('prospective-freeze.json',TITLES['prospective'])
def run_all(stage):
    prerequisites(stage);write_new(RUNTIME/f'{stage}-reservation.json',{'at':now(),'commit':git('rev-parse','HEAD').decode().strip()})
    for run in order(stage):
        try:
            prerequisites(stage);result=execute(run['family'],RUNTIME/stage/run['id'],packet(run,stage),run,stage)
            print(f'{run["id"]}: {result["status"]}',flush=True);require(result['status']=='valid',result['error'])
        except Exception as exc:
            write_new(RUNTIME/'STOP.json',{'stage':stage,'run':run,'at':now(),'error':str(exc)});raise
def freeze(stage):
    prerequisites(stage);entries=[]
    for run in order(stage):
        d=RUNTIME/stage/run['id'];audit_value=read(d/'validation.json');reservation=read(d/'reservation.json')
        require(audit_value['status']=='valid','Failed judgment')
        require(reservation['prepared_commit']==read(RUNTIME/f'{stage}-reservation.json')['commit'],'Commit changed during stage')
        require((d/'prompt.txt').read_bytes()==packet(run,stage).encode(),'Prompt drift')
        require(reservation['packet_sha256']==sha(packet(run,stage).encode()),'Reserved prompt drift')
        require(reservation['schema_sha256']==c.sha(HERE/'schemas'/f'{stage}-wire.schema.json') and reservation['canonical_schema_sha256']==c.sha(canonical(stage)),'Schema drift')
        require(audit(d,run['family'],reservation['fresh_session_requested'])==audit_value['metadata'],'Audit drift')
        validate_response(read(d/'response.json'),stage,run)
        entries.append({**run,'audit':audit_value,'reservation':reservation,'files':inventory(d.iterdir())})
    require(len({x['audit']['metadata']['session_id'] for x in entries})==len(entries),'Duplicate sessions')
    write_new(HERE/f'{stage}-freeze.json',{'at':now(),'prepared_sha256':c.sha(HERE/'prepared.json'),'planned_judgments':len(order(stage)),'runs':entries})
def frozen(stage,private=False):
    value=read(HERE/f'{stage}-freeze.json');require(value['prepared_sha256']==c.sha(HERE/'prepared.json'),'Freeze input drift')
    require([{k:r[k] for k in ('id','case_id','family')} for r in value['runs']]==order(stage),'Freeze coverage mismatch')
    require(all(r['audit']['status']=='valid' for r in value['runs']),'Unsuccessful freeze')
    if private:
        for run in value['runs']:verify_inventory(run['files'])
    return value
def publish(stage):
    for run in frozen(stage,True)['runs']:copy_new(HERE/'judgments'/stage/f'{run["id"]}.json',(RUNTIME/stage/run['id']/'response.json').read_bytes())
def published(stage):
    values={}
    for run in frozen(stage)['runs']:
        p=HERE/'judgments'/stage/f'{run["id"]}.json'
        require(c.sha(p)==run['files'][str((RUNTIME/stage/run['id']/'response.json').relative_to(ROOT))],'Published payload changed')
        value=read(p);validate_response(value,stage,run);values[(run['case_id'],run['family'])]=value
    return values
def admission_rows():
    values=published('validity');rows=[]
    for m in manifest():
        statuses={f:values[(m['mapping_id'],f)]['validity']['final_status'] for f in 'AB'}
        row={'mapping_id':m['mapping_id'],'target_id':m['target_id'],'validity_A':statuses['A'],'validity_B':statuses['B'],
             'admitted':all(statuses[f]=='Valid' and not values[(m['mapping_id'],f)]['validity']['unresolved_conditions'] for f in 'AB')}
        c.validate(row,'admission');rows.append(row)
    return rows
def construct_pairs(admissions):
    design=read(HERE/'design.json');ids={r['mapping_id'] for r in admissions if r['admitted']}
    specs=[p for p in read(HERE/'operator-manifest.json')['pair_designs'] if {p['mapping_1'],p['mapping_2']}<=ids]
    rng=random.Random(design['seeds']['orientation']);pairs=[];odd=0
    for target in sorted({p['target_id'] for p in specs}):
        group=sorted((p for p in specs if p['target_id']==target),key=lambda p:(p['mapping_1'],p['mapping_2']))
        flags=[False]*(len(group)//2)+[True]*(len(group)//2)
        if len(group)%2:flags.append(bool(odd%2));odd+=1
        rng.shuffle(flags)
        for p,flip in zip(group,flags):
            pairs.append({k:p[k] for k in ('target_id','mapping_1','mapping_2')}|{'case_id':f'C{len(pairs)+1:03}',
              'mapping_A':p['mapping_2'] if flip else p['mapping_1'],'mapping_B':p['mapping_1'] if flip else p['mapping_2'],
              'world_id':'W-'+target,'common_state_sha256':c.sha(HERE/'common-states'/f'{target}.json'),'cohort':'primary','control_of':None})
    crng=random.Random(design['seeds']['controls']);remaining=pairs.copy();crng.shuffle(remaining);tags=set();targets=set();controls=[]
    by={(p['mapping_1'],p['mapping_2']):p for p in specs}
    for i in range(min(4,len(pairs))):
        best=max(remaining,key=lambda p:(len(set(by[(p['mapping_1'],p['mapping_2'])]['tags'])-tags),p['target_id'] not in targets))
        remaining.remove(best);tags.update(by[(best['mapping_1'],best['mapping_2'])]['tags']);targets.add(best['target_id'])
        controls.append({**best,'case_id':f'C{len(pairs)+i+1:03}','mapping_A':best['mapping_B'],'mapping_B':best['mapping_A'],'cohort':'orientation-control','control_of':best['case_id']})
    result=pairs+controls;labels=[p['case_id'] for p in result];crng.shuffle(labels);rename={p['case_id']:label for p,label in zip(result,labels)}
    for p in result:
        p['case_id']=rename[p['case_id']]
        if p['control_of']:p['control_of']=rename[p['control_of']]
    result.sort(key=lambda p:p['case_id']);schedules={}
    for stage in ('prospective','consequence'):
        schedule=[{'id':f'{stage}-{p["case_id"]}-{f}','case_id':p['case_id'],'family':f} for p in result for f in 'AB']
        random.Random(design['seeds'][stage]).shuffle(schedule);schedules[stage]=schedule
    return result,schedules
def admit():
    frozen('validity',True);rows=admission_rows();pairs,schedules=construct_pairs(rows)
    write_new(HERE/'admission.json',{'at':now(),'validity_freeze_sha256':c.sha(HERE/'validity-freeze.json'),'mappings':rows,
      'planned_pairs':16,'surviving_pairs':sum(p['cohort']=='primary' for p in pairs),'surviving_targets':sorted({p['target_id'] for p in pairs})})
    write_new(HERE/'pairs/pairs.json',pairs)
    for stage,schedule in schedules.items():
        write_new(order_path(stage),schedule)
        for p in pairs:copy_new(HERE/'packets'/stage/f'{p["case_id"]}.txt',comparison_packet(p,stage).encode())
    paths=[HERE/'admission.json',HERE/'pairs/pairs.json',HERE/'validity-freeze.json',*(HERE/'judgments/validity').glob('*.json'),
           *(HERE/'packets').rglob('*.txt'),order_path('prospective'),order_path('consequence')]
    write_new(HERE/'admission-freeze.json',{'at':now(),'files':inventory(paths),
      'packets':{stage:{r['id']:sha(packet(r,stage).encode()) for r in schedule} for stage,schedule in schedules.items()}})
def verify_admission(check_committed=False):
    rows=admission_rows();a=read(HERE/'admission.json');require(rows==a['mappings'],'Admission changed')
    require(a['validity_freeze_sha256']==c.sha(HERE/'validity-freeze.json'),'Validity freeze changed')
    pairs,schedules=construct_pairs(rows);require(pair_records()==pairs,'Pairs changed')
    mappings={r['mapping_id']:candidate(r['mapping_id']) for r in manifest()};commons={r['target_id']:read(HERE/'common-states'/f'{r["target_id"]}.json') for r in manifest()}
    for p in pairs:c.validate_pair(p,mappings,commons,{r['mapping_id']:r for r in rows})
    for stage,schedule in schedules.items():
        require(order(stage)==schedule,'Execution order changed')
        for p in pairs:require((HERE/'packets'/stage/f'{p["case_id"]}.txt').read_bytes()==comparison_packet(p,stage).encode(),'Packet changed')
    value=read(HERE/'admission-freeze.json');verify_inventory(value['files'])
    require(value['packets']=={s:{r['id']:sha(packet(r,s).encode()) for r in schedules[s]} for s in schedules},'Packet manifest changed')
    if check_committed:
        for name in [*value['files'],str((HERE/'admission-freeze.json').relative_to(ROOT))]:committed(ROOT/name)
        check_commit('admission-freeze.json',TITLES['admission'])
def freeze_failure():
    write_new(HERE/'failure-freeze.json',{'at':now(),'stop':read(RUNTIME/'STOP.json'),'files':inventory(RUNTIME.rglob('*'))})
def analyze():
    import metrics
    verify(True);verify_admission(True)
    for stage in ('prospective','consequence'):frozen(stage,True);committed(HERE/f'{stage}-freeze.json')
    write_new(HERE/'metrics.json',metrics.calculate({s:published(s) for s in ('prospective','consequence')},pair_records()))
def verify_results(private=False):
    import metrics
    verify(True);preservation(private)
    if (HERE/'failure-freeze.json').exists():
        if private:verify_inventory(read(HERE/'failure-freeze.json')['files'])
        return {'status':'stopped'}
    verify_admission(True)
    if not pair_records():return {'status':'no eligible pairs'}
    for stage in STAGES:frozen(stage,private)
    require(read(HERE/'metrics.json')==metrics.calculate({s:published(s) for s in ('prospective','consequence')},pair_records()),'Metrics changed')
    return {'status':'complete','primary_pairs':sum(p['cohort']=='primary' for p in pair_records()),'orientation_controls':sum(p['cohort']!='primary' for p in pair_records())}
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['validate','prepare','verify','preflight','run','freeze','publish','admit','analyze','verify-results','freeze-failure'])
    parser.add_argument('--stage',choices=STAGES,default='validity');parser.add_argument('--private',action='store_true');a=parser.parse_args()
    actions={'validate':validate_inputs,'prepare':prepare,'verify':lambda:verify(True),'preflight':preflight,'run':lambda:run_all(a.stage),'freeze':lambda:freeze(a.stage),'publish':lambda:publish(a.stage),
             'admit':admit,'analyze':analyze,'verify-results':lambda:verify_results(a.private),'freeze-failure':freeze_failure}
    print(actions[a.command]() or a.command+': OK')
if __name__=='__main__':main()
