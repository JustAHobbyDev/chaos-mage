#!/usr/bin/env python3
"""Experiment D: exclusive frozen preparation, admission, isolated measurement and audit."""
import argparse
from datetime import datetime, timezone
import hashlib, importlib.util, json, os, random, signal, subprocess, tempfile, uuid
from pathlib import Path
import contracts as c
from build_schemas import projection
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
RUNTIME=ROOT/'.runtime/anti-collapse-v0.1'
read,require=c.read,c.require
STAGES=('validity','anti-collapse')
TITLES={'baselines':'Freeze anti-collapse target baselines','ladders':'Freeze anti-collapse matched ladders and neutralizations','prepared':'Prepare anti-collapse benchmark v0.1','preflight':'Freeze anti-collapse provider probes','admission':'Freeze anti-collapse validity admission','anti-collapse':'Freeze anti-collapse benchmark results'}
spec=importlib.util.spec_from_file_location('d_frozen_event_audit',ROOT/'distance/boundary-v0.2/harness.py')
legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
def now():return datetime.now(timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def config():return read(HERE/'execution-config.json')
def manifest():return read(HERE/'operator-manifest.json')['mappings']
def candidate(cid):return read(HERE/'cases'/f'{cid}.json')
def canonical(stage):return HERE/'schemas'/('validity.schema.json' if stage=='validity' else 'output.schema.json')
def write_new(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('x') as f:f.write(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def copy_new(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('xb') as f:f.write(data)
def inventory(paths):return {str(p.relative_to(ROOT)):c.sha(p) for p in sorted(paths) if p.is_file() and '__pycache__' not in p.parts}
def verify_inventory(files):
 for name,digest in files.items():require(c.sha(ROOT/name)==digest,'Changed frozen file: '+name)
def preservation(private=False):
 v=read(HERE/'preservation.json');verify_inventory(v['files'])
 if private:verify_inventory(v['private_files'])
def committed(path,revision='HEAD'):require(git('show',f'{revision}:{path.relative_to(ROOT)}')==path.read_bytes(),'Uncommitted input: '+str(path))
def checkpoint(name):return git('log','-1','--format=%H','--',str(HERE/name)).decode().strip()
def check_commit(name,title):
 revision=checkpoint(name);require(git('show','-s','--format=%s',revision).decode().strip()==title,'Missing checkpoint: '+title);return revision

def design_coverage(rows):
 require(len(rows)==24 and len({r['case_id'] for r in rows})==24,'24 unique cases required')
 targets={r['target_id'] for r in rows};require(len(targets)==6,'Six targets required')
 for target in targets:require(sorted(r['ladder_level'] for r in rows if r['target_id']==target)==list('ABCD'),'A/B/C/D ladder required')
 require({r['intended_departure_type'] for r in rows if r['ladder_level']=='C'}==set(c.LOCI),'All five C loci required')
 for tag,levels in [('exotic-collapse','A'),('mundane-positive','CD')]:
  require(sum(tag in r['adversary_tags'] and r['ladder_level'] in levels for r in rows)>=3,'Adversary coverage missing: '+tag)
 return True

def validate_inputs():
 import yaml
 preservation();bf=read(HERE/'baselines-freeze.json');lf=read(HERE/'ladders-freeze.json')
 verify_inventory(bf['files']);verify_inventory(lf['files'])
 baseline_commit=check_commit('baselines-freeze.json',TITLES['baselines'])
 require(lf['baseline_commit']==baseline_commit,'Baseline commit mismatch')
 rows=manifest();design_coverage(rows)
 audits={a['case_id']:a for a in read(HERE/'neutralization-audit.json')['cases']}
 require(set(audits)=={r['case_id'] for r in rows},'Missing neutralization audit')
 for row in rows:
  tid,cid=row['target_id'],row['case_id'];base=c.validate(read(HERE/'baselines'/f'{tid}.json'),'baseline')
  old=read(ROOT/bf['historical_sources'][tid]['path']);require({k:base[k] for k in old}==old,'Historical baseline rescope')
  require(row['baseline_commit']==baseline_commit,'Case not bound to baseline freeze')
  value=c.validate(candidate(cid),'candidate');neutral=c.validate(read(HERE/'neutralizations'/f'{cid}.json'),'neutralization')
  require(value['case_id']==cid and value['target']=={'domain':base['target_domain'],'question':base['target_task'],'evidence':read(HERE/'contexts'/f'{tid}.json')['facts']},'Target/context mismatch')
  source=yaml.safe_load((ROOT/row['source_path']).read_text())
  require(source['extraction']['status']=='accepted' and value['source']=={'name':source['extraction']['name'],'practice':source['extraction']['practice'],'instrument':source['instrument']},'Accepted source changed')
  audit=audits[cid];require(audit['framing_only_removed'],'Neutralization failed')
  require(audit['source_mapping_sha256']==c.sha(HERE/'cases'/f'{cid}.json') and audit['neutralization_sha256']==c.sha(HERE/'neutralizations'/f'{cid}.json'),'Audit hash mismatch')
  for key in ('operations','signals','warrants','conditions_and_stopping','next_inquiry','decomposition'):require(audit[key+'_preserved']['pass'],'Audit failed: '+key)
  mapping=value['mapping']
  require(mapping['operation']==neutral['action']+' Next inquiry: '+neutral['next_inquiry'],'Operation/follow-up changed in neutralization')
  require(mapping['signal']==neutral['observables'] and mapping['inference']==neutral['inferential_warrant'],'Signal/warrant changed')
  require(mapping['limit'] in neutral['procedure'] and mapping['state'].endswith('Decomposition: '+neutral['problem_decomposition']),'Limit/decomposition lost')
  require(mapping['state'].startswith(audit['removed_framing']+' Operational target state: '),'Framing prefix mismatch')
  raw_state=mapping['state'].removeprefix(audit['removed_framing']+' Operational target state: ').removesuffix(' Decomposition: '+neutral['problem_decomposition'])
  require(neutral['procedure']=='State: '+raw_state+' Procedure: '+neutral['action']+' Limits and stopping conditions: '+mapping['limit'],'Neutral procedure changed operational content')
  packet_text=packet({'case_id':cid},'anti-collapse');body=packet_body(packet_text)
  c.validate(body,'packet');require((HERE/'baselines'/f'{tid}.json').read_bytes() in packet_text.encode(),'Baseline bytes missing')
  require(audit['removed_framing'] not in packet_text and value['source']['name'] not in json.dumps(body),'Source framing leaked')
 require((HERE/'CLASSIFIER-validity.md').read_bytes()==(HERE.parent/'v0.3/CLASSIFIER-transfer-validity.md').read_bytes(),'Validity classifier changed')
 for name in ('candidate','validity'):require((HERE/'schemas'/f'{name}.schema.json').read_bytes()==(HERE.parent/'v0.3'/f'{name}.schema.json').read_bytes(),'Historical contract changed')
 for stage in STAGES:require(read(HERE/'schemas'/f'{stage}-wire.schema.json')==projection(read(canonical(stage))),'Wire projection mismatch')
 return True

def packet_body(text):return json.loads(text.split('\n\nCASE PACKET\n',1)[1],object_pairs_hook=c.unique_object)
def packet(run,stage='validity'):
 cid=run['case_id']
 if stage=='validity':return (HERE/'CLASSIFIER-validity.md').read_text()+'\n\nCASE PACKET\n'+json.dumps(candidate(cid),indent=2,ensure_ascii=False)+'\n'
 require(stage=='anti-collapse','Unknown stage');row=next(r for r in manifest() if r['case_id']==cid)
 # The native baseline's exact serialized bytes are embedded once.
 body={'case_id':cid,'target':candidate(cid)['target'],'source_neutral':read(HERE/'neutralizations'/f'{cid}.json')}
 base=(HERE/'baselines'/f'{row["target_id"]}.json').read_text()
 payload=json.dumps(body,indent=2,ensure_ascii=False)[:-2]+',\n  "native_baseline": '+base+'}\n'
 json.loads(payload)
 return (HERE/'CLASSIFIER.md').read_text()+'\n\nCASE PACKET\n'+payload

def planned(stage):return read(HERE/'execution-order.json')[stage]
def order(stage):
 if stage=='validity':return planned(stage)
 admitted={r['case_id'] for r in read(HERE/'admission.json')['cases'] if r['admitted']}
 return [r for r in planned(stage) if r['case_id'] in admitted]
def validate_response(value,stage,run):
 return c.validate(value,stage,candidate(run['case_id']) if run and stage=='validity' else {'case_id':run['case_id']} if run else None)
def check_fresh_session(session,directory):
 require(bool(session),'Missing session')
 for p in RUNTIME.rglob('validation.json'):
  if p.parent!=directory:
   meta=read(p).get('metadata');require(not meta or meta['session_id']!=session,'Duplicate session across stages')

# Provider adapter copied from frozen B.2; only experiment paths/prefix differ.
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
    with tempfile.TemporaryDirectory(prefix='d-isolated-') as cwd:
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
 return {'case_id':'PREFLIGHT','anti_collapse':{'status':'BORDERLINE_KEEP','departures':{k:{'status':'uncertain','rationale':'Formatting fixture only.'} for k in c.LOCI},'materiality':{'status':'uncertain','rationale':'Formatting fixture only.'},'native_reduction':{'collapses_without_loss':'uncertain','closest_native_equivalent':'Formatting fixture only.','lost_if_reduced':[],'rationale':'Formatting fixture only.'},'formalization':{'merely_makes_native_reasoning_explicit':'uncertain','new_epistemic_constraint':None,'rationale':'Formatting fixture only.'},'decisive_reason':'Formatting fixture only.','uncertainty':['Artificial fixture; no benchmark classification.']}}

def prepare():
 validate_inputs();preservation(True)
 seeds=read(HERE/'operator-manifest.json')['seeds'];schedules={}
 for stage,key in [('validity','validity'),('anti-collapse','anti_collapse')]:
  schedule=[{'id':f'{stage}-{r["case_id"]}-{f}','case_id':r['case_id'],'family':f} for r in manifest() for f in 'AB']
  random.Random(seeds[key]).shuffle(schedule);schedules[stage]=schedule
  for row in manifest():copy_new(HERE/'packets'/stage/f'{row["case_id"]}.txt',packet(row,stage).encode())
 write_new(HERE/'execution-order.json',schedules)
 paths=list(HERE.rglob('*'))+[ROOT/'docs/PROBLEM_FRAMES-anti-collapse-v0.1.md']
 write_new(HERE/'prepared.json',{'created_at':now(),'baselines_commit':checkpoint('baselines-freeze.json'),'ladders_commit':check_commit('ladders-freeze.json',TITLES['ladders']),'files':inventory(paths),'packet_hashes':{stage:{r['id']:sha(packet(r,stage).encode()) for r in schedule} for stage,schedule in schedules.items()}})
def verify(committed_inputs=False):
 validate_inputs();value=read(HERE/'prepared.json');verify_inventory(value['files'])
 for stage in STAGES:
  schedule=planned(stage)
  require(len(schedule)==48 and len({r['id'] for r in schedule})==48 and {(r['case_id'],r['family']) for r in schedule}=={(r['case_id'],f) for r in manifest() for f in 'AB'},'Schedule coverage mismatch')
  require(value['packet_hashes'][stage]=={r['id']:sha(packet(r,stage).encode()) for r in schedule},'Packet drift')
  for row in manifest():require((HERE/'packets'/stage/f'{row["case_id"]}.txt').read_bytes()==packet(row,stage).encode(),'Stored packet drift')
 if committed_inputs:
  for name in [*value['files'],str((HERE/'prepared.json').relative_to(ROOT))]:committed(ROOT/name)
  prep=check_commit('prepared.json',TITLES['prepared']);require(git('merge-base',value['ladders_commit'],prep).decode().strip()==value['ladders_commit'],'Checkpoint ancestry')
 return value

def execute(family,directory,prompt,run=None,stage='validity'):
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
    verify(True);directory=RUNTIME/'preflight'/stage/family
    result=execute(family,directory,'Return exactly this artificial formatting fixture; no classification, tools or external context.\n'+json.dumps(probe_response(stage)),stage=stage)
    print(f'probe {stage} {family}: {result["status"]}',flush=True);entries.append({'stage':stage,'family':family,'audit':result})
    require(result['status']=='valid',result['error'])
 except Exception as exc:
  write_new(RUNTIME/'STOP.json',{'stage':'preflight','at':now(),'error':str(exc)});raise
 write_new(HERE/'preflight.json',{'frozen_at':now(),'prepared_sha256':c.sha(HERE/'prepared.json'),'entries':entries,'files':inventory((RUNTIME/'preflight').rglob('*'))})

def prerequisites(stage):
 verify(True);probe=read(HERE/'preflight.json');committed(HERE/'preflight.json');check_commit('preflight.json',TITLES['preflight'])
 verify_inventory(probe['files']);require(len(probe['entries'])==4 and all(e['audit']['status']=='valid' for e in probe['entries']),'Four successful probes required')
 require(not (RUNTIME/'STOP.json').exists(),'Scheduling stopped; explicit authorization required')
 if stage=='anti-collapse':verify_admission(True);require(read(HERE/'admission.json')['viability']['viable'],'Insufficient benchmark coverage')

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
  directory=RUNTIME/stage/run['id'];audit_value=read(directory/'validation.json');reservation=read(directory/'reservation.json')
  require(audit_value['status']=='valid','Failed judgment')
  require(reservation['prepared_commit']==read(RUNTIME/f'{stage}-reservation.json')['commit'],'Commit changed during stage')
  require((directory/'prompt.txt').read_bytes()==packet(run,stage).encode() and reservation['packet_sha256']==sha(packet(run,stage).encode()),'Prompt drift')
  require(reservation['schema_sha256']==c.sha(HERE/'schemas'/f'{stage}-wire.schema.json') and reservation['canonical_schema_sha256']==c.sha(canonical(stage)),'Schema drift')
  require(audit(directory,run['family'],reservation['fresh_session_requested'])==audit_value['metadata'],'Audit drift')
  validate_response(read(directory/'response.json'),stage,run)
  entries.append({**run,'audit':audit_value,'reservation':reservation,'files':inventory(directory.iterdir())})
 require(len({r['audit']['metadata']['session_id'] for r in entries})==len(entries),'Duplicate stage sessions')
 write_new(HERE/f'{stage}-freeze.json',{'at':now(),'prepared_sha256':c.sha(HERE/'prepared.json'),'planned_judgments':len(order(stage)),'runs':entries})

def frozen(stage,private=False):
 value=read(HERE/f'{stage}-freeze.json');require(value['prepared_sha256']==c.sha(HERE/'prepared.json'),'Freeze input drift')
 require([{k:r[k] for k in ('id','case_id','family')} for r in value['runs']]==order(stage),'Freeze coverage mismatch')
 require(all(r['audit']['status']=='valid' for r in value['runs']),'Unsuccessful result freeze')
 if private:
  for run in value['runs']:verify_inventory(run['files'])
 return value

def publish(stage):
 for run in frozen(stage,True)['runs']:copy_new(HERE/'judgments'/stage/f'{run["id"]}.json',(RUNTIME/stage/run['id']/'response.json').read_bytes())
def published(stage):
 result={}
 for run in frozen(stage)['runs']:
  p=HERE/'judgments'/stage/f'{run["id"]}.json';raw=str((RUNTIME/stage/run['id']/'response.json').relative_to(ROOT))
  require(c.sha(p)==run['files'][raw],'Published payload changed');value=read(p);validate_response(value,stage,run);result[(run['case_id'],run['family'])]=value
 return result

def admission_rows(values):
 rows=[]
 for row in manifest():
  statuses={f:values[(row['case_id'],f)]['validity']['final_status'] for f in 'AB'}
  admitted=all(statuses[f]=='Valid' and not values[(row['case_id'],f)]['validity']['unresolved_conditions'] for f in 'AB')
  value={'case_id':row['case_id'],'target_id':row['target_id'],'validity_A':statuses['A'],'validity_B':statuses['B'],'admitted':admitted};c.validate(value,'admission');rows.append(value)
 return rows

def viability(admissions,design=None):
 design=manifest() if design is None else design;ids={r['case_id'] for r in admissions if r['admitted']};rows=[r for r in design if r['case_id'] in ids]
 targets=sorted({r['target_id'] for r in rows});levels={k:sum(r['ladder_level']==k for r in rows) for k in 'ABCD'}
 loci=sorted({r['intended_departure_type'] for r in rows if r['ladder_level']=='C'})
 checks={'at_least_18_cases':len(rows)>=18,'at_least_5_targets':len(targets)>=5,'at_least_4_A':levels['A']>=4,'at_least_4_CD':levels['C']+levels['D']>=4,'all_5_C_loci':set(loci)==set(c.LOCI)}
 ladders={t:[r['ladder_level'] for r in sorted(rows,key=lambda r:r['ladder_level']) if r['target_id']==t] for t in sorted({r['target_id'] for r in design})}
 return {'viable':all(checks.values()),'checks':checks,'admitted_cases':len(rows),'represented_targets':targets,'levels':levels,'C_loci':loci,'ladders':ladders,'complete_ladders':[t for t,x in ladders.items() if x==list('ABCD')],'missing_adjacent_contrasts':{t:[a+'-'+b for a,b in zip('ABC','BCD') if a not in x or b not in x] for t,x in ladders.items()}}

def admit():
 frozen('validity',True);values=published('validity');rows=admission_rows(values);coverage=viability(rows)
 write_new(HERE/'admission.json',{'at':now(),'validity_freeze_sha256':c.sha(HERE/'validity-freeze.json'),'cases':rows,'viability':coverage,'replacement_policy':'No replacement or post-result authoring.'})
 write_new(HERE/'admitted-order.json',order('anti-collapse'))
 paths=[HERE/'admission.json',HERE/'admitted-order.json',HERE/'validity-freeze.json',*(HERE/'judgments/validity').glob('*.json')]
 write_new(HERE/'admission-freeze.json',{'at':now(),'files':inventory(paths),'anti_collapse_packets':{r['id']:sha(packet(r,'anti-collapse').encode()) for r in order('anti-collapse')}})
 print(json.dumps(coverage,indent=2))
def verify_admission(check_committed=False):
 rows=admission_rows(published('validity'));admission=read(HERE/'admission.json')
 require(rows==admission['cases'] and viability(rows)==admission['viability'],'Admission/coverage drift')
 require(admission['validity_freeze_sha256']==c.sha(HERE/'validity-freeze.json'),'Validity freeze changed')
 require(read(HERE/'admitted-order.json')==order('anti-collapse'),'Admission reshuffled schedule')
 value=read(HERE/'admission-freeze.json');verify_inventory(value['files'])
 require(value['anti_collapse_packets']=={r['id']:sha(packet(r,'anti-collapse').encode()) for r in order('anti-collapse')},'Admitted packet drift')
 if check_committed:
  for name in [*value['files'],str((HERE/'admission-freeze.json').relative_to(ROOT))]:committed(ROOT/name)
  check_commit('admission-freeze.json',TITLES['admission'])
 return admission

def freeze_failure():
 write_new(HERE/'failure-freeze.json',{'at':now(),'stop':read(RUNTIME/'STOP.json'),'files':inventory(RUNTIME.rglob('*'))})
def analyze():
 import metrics
 verify(True);verify_admission(True);frozen('anti-collapse',True);committed(HERE/'anti-collapse-freeze.json');check_commit('anti-collapse-freeze.json',TITLES['anti-collapse'])
 write_new(HERE/'metrics.json',metrics.compute(published('anti-collapse'),manifest(),read(HERE/'admission.json')['cases']))

def execution_audit(private=False):
 prep=verify(True);probe=read(HERE/'preflight.json');sessions=[r['audit']['metadata']['session_id'] for r in probe['entries']]
 previous=datetime.fromisoformat(probe['frozen_at']);result={}
 for stage in STAGES:
  freeze_value=frozen(stage,private);returns={f:set() for f in 'AB'};retries={f:0 for f in 'AB'};commits=set();packets={}
  for run in freeze_value['runs']:
   reservation,validation=run['reservation'],run['audit'];meta=validation['metadata'];sessions.append(meta['session_id'])
   start=datetime.fromisoformat(reservation['started_at']);finish=datetime.fromisoformat(validation['finished_at'])
   require(previous<=start<=finish,'Execution overlap/chronology');previous=finish
   require(reservation['configuration']==config() and reservation['cli_version']==config()['expected_cli_versions'][run['family']],'Execution config drift')
   require(reservation['schema_sha256']==c.sha(HERE/'schemas'/f'{stage}-wire.schema.json') and reservation['canonical_schema_sha256']==c.sha(canonical(stage)),'Execution schema drift')
   require(reservation['packet_sha256']==sha(packet(run,stage).encode()),'Executed packet mismatch')
   packets[(run['case_id'],run['family'])]=reservation['packet_sha256'];commits.add(reservation['prepared_commit'])
   returns[run['family']].update(meta['returned_model_identifiers']);retries[run['family']]+=meta['formatting_retries']['observed_formatting_retries']
  require(len(commits)==1,'Stage spans commits')
  for cid in {k[0] for k in packets}:require(packets[(cid,'A')]==packets[(cid,'B')],'Family packet mismatch')
  require(previous<=datetime.fromisoformat(freeze_value['at']),'Freeze precedes collection');previous=datetime.fromisoformat(freeze_value['at'])
  result[stage]={'judgments':len(freeze_value['runs']),'first_started_at':freeze_value['runs'][0]['reservation']['started_at'],'last_finished_at':freeze_value['runs'][-1]['audit']['finished_at'],'execution_commit':next(iter(commits)),'returned_identifiers':{f:sorted(returns[f]) for f in 'AB'},'exposed_formatter_retries':retries,'verified_served_snapshots':{'A':None,'B':None}}
 require(len(sessions)==len(set(sessions)),'Session reused across stages/probes')
 paths={'baselines':'baselines-freeze.json','ladders':'ladders-freeze.json','prepared':'prepared.json','preflight':'preflight.json','admission':'admission-freeze.json','anti-collapse':'anti-collapse-freeze.json'}
 checkpoints={k:check_commit(p,TITLES[k]) for k,p in paths.items()};chain=list(checkpoints.values())
 for old,new in zip(chain,chain[1:]):require(old!=new and git('merge-base',old,new).decode().strip()==old,'Checkpoint ancestry/order')
 require(result['validity']['execution_commit']==checkpoints['preflight'] and result['anti-collapse']['execution_commit']==checkpoints['admission'],'Wrong execution checkpoint')
 require(datetime.fromisoformat(prep['created_at'])<datetime.fromisoformat(probe['frozen_at']),'Preflight before preparation')
 require(datetime.fromisoformat(read(HERE/'validity-freeze.json')['at'])<=datetime.fromisoformat(read(HERE/'admission.json')['at'])<datetime.fromisoformat(result['anti-collapse']['first_started_at']),'Admission chronology')
 return {'checkpoints':checkpoints,'stages':result,'unique_sessions_including_probes':len(sessions),'family_packets_identical':True,'harness_retries':0,'replacement_measurements':0,'control_judgments':0}

def verify_results(private=False):
 import metrics
 verify(True);preservation(private)
 if (HERE/'failure-freeze.json').exists():
  fail=read(HERE/'failure-freeze.json')
  if private:verify_inventory(fail['files'])
  return {'status':'incomplete','reason':'measurement failure','failure':fail['stop']}
 admission=verify_admission(True)
 if not admission['viability']['viable']:return {'status':'insufficient benchmark coverage','viability':admission['viability']}
 frozen('anti-collapse',private);values=published('anti-collapse')
 require(read(HERE/'metrics.json')==metrics.compute(values,manifest(),admission['cases']),'Metrics differ from frozen judgments')
 audit_value=execution_audit(private)
 require(read(HERE/'review/execution-audit.json')==audit_value,'Execution audit drift')
 return {'status':'complete','targets':len(admission['viability']['represented_targets']),'designed_cases':24,'admitted_cases':admission['viability']['admitted_cases'],'judgments':len(values),'sessions':audit_value['unique_sessions_including_probes']}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['validate','prepare','verify','preflight','run','freeze','publish','admit','analyze','verify-results','freeze-failure']);p.add_argument('--stage',choices=STAGES,default='validity');p.add_argument('--private',action='store_true');a=p.parse_args()
 if a.command=='validate':print(validate_inputs())
 elif a.command=='prepare':prepare()
 elif a.command=='verify':verify();print('Prepared inputs verified')
 elif a.command=='preflight':preflight()
 elif a.command=='run':run_all(a.stage)
 elif a.command=='freeze':freeze(a.stage)
 elif a.command=='publish':publish(a.stage)
 elif a.command=='admit':admit()
 elif a.command=='analyze':analyze()
 elif a.command=='verify-results':print(verify_results(a.private))
 else:freeze_failure()
if __name__=='__main__':main()
