#!/usr/bin/env python3
"""Experiment B: committed inputs, sequential isolated stages, immutable raw evidence."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import uuid
import random
import contracts as c
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SNAPSHOT=ROOT/'distance/v0.3'
RUNTIME=ROOT/'.runtime/displacement-v0.3'
spec=importlib.util.spec_from_file_location('frozen_boundary_audit',ROOT/'distance/boundary-v0.2/harness.py')
legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
read,require=c.read,c.require

def now():return datetime.now(timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def config():return read(HERE/'execution-config.json')
def candidate(cid):return read(HERE/'cases'/f'{cid}.json')
def manifest():return read(HERE/'operator-manifest.json')['cases']
def canonical(stage):return SNAPSHOT/'validity.schema.json' if stage=='validity' else HERE/'displacement.schema.json'
def order(stage):return read(HERE/f'{stage}-order.json')
def write_new(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('x') as stream:stream.write(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def copy_new(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('xb') as stream:stream.write(data)
def projection(value):
 if isinstance(value,dict):return {k:projection(v) for k,v in value.items() if k not in ('$schema','$id','allOf')}
 if isinstance(value,list):return [projection(v) for v in value]
 return value

def committed(path,revision='HEAD'):
 require(git('show',f'{revision}:{path.relative_to(ROOT)}')==path.read_bytes(),f'Uncommitted input: {path}')
def verify_inventory(values):
 for name,digest in values.items():require(c.sha(ROOT/name)==digest,f'Preservation mismatch: {name}')
def preservation(private=True):
 inv=read(HERE/'preservation.json');verify_inventory(inv['files'])
 if private:verify_inventory(inv['private_files'])
 verify_inventory(read(HERE/'baselines-freeze.json')['files'])

def validate_inputs():
 preservation()
 for stage in ('validity','displacement'):require(read(HERE/f'{stage}-wire.schema.json')==projection(read(canonical(stage))),'Wire projection changed')
 require((HERE/'CLASSIFIER-validity.md').read_bytes()==(SNAPSHOT/'CLASSIFIER-transfer-validity.md').read_bytes(),'Validity classifier changed')
 cfg=config();prior=read(ROOT/'distance/validity-v0.3/execution-config.json');require({k:v for k,v in cfg.items() if k!='expected_cli_versions'}=={k:v for k,v in prior.items() if k!='expected_cli_versions'},'A settings changed; amendment required')
 m=manifest();require(len(m)==26 and sum(x['core'] for x in m)==24,'Expected 24 core plus two variants')
 require(len({x['case_id'] for x in m})==26,'Duplicate case ID')
 for target in {x['target_id'] for x in m}:
  core=[x for x in m if x['target_id']==target and x['core']]
  require(len(core)==3 and {x['intended_band'] for x in core}==set(c.BANDS),'Missing intended contrast')
 import yaml
 for row in m:
  v=c.validate(candidate(row['case_id']),'candidate');base=c.validate(read(HERE/'baselines'/f"{row['target_id']}.json"),'baseline')
  require(base['target_task']==v['target']['question'] and base['target_domain']==v['target']['domain'],'Baseline drift')
  source=yaml.safe_load((ROOT/row['source_path']).read_text())
  require(source['extraction']['status']=='accepted' and v['source']=={'name':source['extraction']['name'],'practice':source['extraction']['practice'],'instrument':source['instrument']},'Source fields changed')
  if not row['core']:
   parent=candidate(row['variant_of']);parent['case_id']=v['case_id'];parent['target']['evidence']=v['target']['evidence'];require(parent==v,'Variant changes more than evidence')
 require(len({x['target_id'] for x in m if not x['core']})==2,'Variants require different groups')
 planned={(x['case_id'],f) for x in m for f in ('A','B')}
 require(len(order('validity'))==52 and {(x['case_id'],x['family']) for x in order('validity')}==planned,'Invalid validity schedule')

def packet(run,stage='validity'):
 v=candidate(run['case_id'])
 if stage=='validity':return (HERE/'CLASSIFIER-validity.md').read_text()+'\n\nCASE PACKET\n'+json.dumps(v,indent=2,ensure_ascii=False)+'\n'
 a=next(x for x in read(HERE/'admission.json')['cases'] if x['case_id']==run['case_id'])
 require(a['cohort']!='holdout','Holdout blocked')
 row=next(x for x in manifest() if x['case_id']==run['case_id'])
 baseline=(HERE/'baselines'/f"{row['target_id']}.json").read_bytes()
 v['native_baseline']=read(HERE/'baselines'/f"{row['target_id']}.json");v['provisional']=a['cohort']=='provisional'
 if v['provisional']:v['applicability_assumption']=a['applicability_assumption']
 c.validate(v,'packet')
 # Insert the EXACT baseline file bytes as the JSON value, without reindentation.
 native=v.pop('native_baseline');prefix=json.dumps(v,indent=2,ensure_ascii=False)[:-2]
 body=prefix+',\n  "native_baseline": '+baseline.decode()+'}\n'
 require(json.loads(body)=={**v,'native_baseline':native},'Packet serialization mismatch')
 require(baseline in body.encode(),'Exact baseline bytes absent')
 return (HERE/'CLASSIFIER-displacement.md').read_text()+'\n\nCASE PACKET\n'+body

def validate_response(value,stage,run):
 c.validate(value,stage,candidate(run['case_id']) if run else None)
 if stage=='displacement' and run:
  p=json.loads(packet(run,stage).split('\n\nCASE PACKET\n')[1]);require(value['provisional']==p['provisional'],'Provisional flag changed')

def check_fresh_session(session,directory):
 require(bool(session),'Missing session ID')
 for p in RUNTIME.rglob('validation.json'):
  if p.parent==directory:continue
  value=read(p)
  require(not value.get('metadata') or value['metadata']['session_id']!=session,'Duplicate session')

def build_command(family, cwd, directory, session, stage="validity"):
    cfg = config(); model = cfg['families'][family]['requested_model']
    schema = HERE / f'{stage}-wire.schema.json'
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


def execute(family, directory, prompt, run=None, stage="validity"):
    directory.mkdir(parents=True, exist_ok=False)
    copy_new(directory / 'prompt.txt', prompt.encode())
    session = str(uuid.uuid4()); cfg = config(); cli = cfg['families'][family]['cli']
    with tempfile.TemporaryDirectory(prefix='displacement-isolated-') as cwd:
        cmd = build_command(family, cwd, directory, session, stage)
        version = subprocess.check_output([cli, '--version'], text=True).strip()
        require(version == cfg['expected_cli_versions'][family], 'CLI version changed')
        reservation = {'run': run, 'family': family, 'started_at': now(),
                       'packet_sha256': sha(prompt.encode()),
                       'schema_sha256': c.sha(HERE / f'{stage}-wire.schema.json'),
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
 if stage=='validity':
  return {'case_id':'PREFLIGHT','validity':{'mechanism_fidelity':{'status':'preserved','rationale':'Formatting fixture only.'},'target_fidelity':{'status':'addressed','rationale':'Formatting fixture only.'},'operational_coherence':{'status':'coherent','rationale':'Formatting fixture only.'},'target_reframe':{'occurred':False,'original_question':None,'reframed_question':None,'relationship':None},'unresolved_conditions':[],'final_status':'Valid','rationale':'Formatting fixture only.'},'uncertainty':[]}
 return {'case_id':'PREFLIGHT','provisional':False,'class':'Native','dimensions':{d:{'level':0,'rationale':'Formatting fixture only.'} for d in c.DIMS},'rationale':'Formatting fixture only.','epistemic_changes':{k:'Formatting fixture only.' for k in ('practitioner_actions','noticed_features','evidential_warrants','next_inquiry')},'most_consequential_baseline_difference':'Formatting fixture only.','boundary_status':'clear','nearest_alternative':None,'uncertainty':[]}

def prepare():
 validate_inputs();baseline_commit=read(HERE/'checkpoint.json')['baseline_commit']
 require(git('show','-s','--format=%s',baseline_commit).decode().strip()=='Freeze Experiment B target-native baselines','Baseline commit missing')
 for name in read(HERE/'baselines-freeze.json')['files']:committed(ROOT/name,baseline_commit)
 files=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='prepared.json']
 files+=[ROOT/'docs/PROBLEM_FRAMES-displacement-v0.3.md',ROOT/'docs/PLAN-displacement-v0.3.md']
 write_new(HERE/'prepared.json',{'created_at':now(),'baseline_commit':baseline_commit,'files':{str(p.relative_to(ROOT)):c.sha(p) for p in sorted(files)},'validity_packets':{r['id']:sha(packet(r).encode()) for r in order('validity')}})

def verify(committed_inputs=False):
 validate_inputs();v=read(HERE/'prepared.json');verify_inventory(v['files'])
 require(v['validity_packets']=={r['id']:sha(packet(r).encode()) for r in order('validity')},'Packet drift')
 if committed_inputs:
  for name in [*v['files'],str((HERE/'prepared.json').relative_to(ROOT))]:committed(ROOT/name)
  commit=git('log','-1','--format=%H','--',str(HERE/'prepared.json')).decode().strip()
  require(git('show','-s','--format=%s',commit).decode().strip()=='Prepare ontological displacement Experiment B','Preparation commit checkpoint missing')
  require(subprocess.run(['git','merge-base','--is-ancestor',v['baseline_commit'],commit],cwd=ROOT).returncode==0 and v['baseline_commit']!=commit,'Baseline must precede preparation')
 return v

def preflight():
 verify(True)
 write_new(RUNTIME/'preflight-reservation.json',{'started_at':now(),'commit':git('rev-parse','HEAD').decode().strip()})
 entries=[]
 try:
  for stage in ('validity','displacement'):
   for family in ('A','B'):
    verify(True);directory=RUNTIME/'preflight'/stage/family
    prompt='Return exactly this artificial formatting fixture; no classification, tools or external context.\n'+json.dumps(probe_response(stage))
    result=execute(family,directory,prompt,stage=stage);print(f'probe {stage} {family}: {result["status"]}',flush=True)
    entries.append({'stage':stage,'family':family,'audit':result})
    require(result['status']=='valid',result['error'])
 except Exception as exc:
  write_new(RUNTIME/'STOP.json',{'stage':'preflight','at':now(),'error':str(exc)});raise
 write_new(HERE/'preflight.json',{'frozen_at':now(),'prepared_sha256':c.sha(HERE/'prepared.json'),'entries':entries,'files':{str(p.relative_to(ROOT)):c.sha(p) for p in sorted((RUNTIME/'preflight').rglob('*')) if p.is_file()}})

def prerequisites(stage):
 verify(True);p=read(HERE/'preflight.json');committed(HERE/'preflight.json')
 require(p['prepared_sha256']==c.sha(HERE/'prepared.json'),'Probe preparation drift');verify_inventory(p['files'])
 require(len(p['entries'])==4 and all(x['audit']['status']=='valid' for x in p['entries']),'Four probes required')
 require(not (RUNTIME/'STOP.json').exists(),'Scheduling stopped; explicit recovery authorization required')
 if stage=='displacement':
  verify_admission(True);require(read(HERE/'admission.json')['viability']['passes'],'Admission viability failed')

def run_all(stage):
 prerequisites(stage)
 write_new(RUNTIME/f'{stage}-reservation.json',{'at':now(),'commit':git('rev-parse','HEAD').decode().strip()})
 for run in order(stage):
  try:
   prerequisites(stage)
   result=execute(run['family'],RUNTIME/stage/run['id'],packet(run,stage),run,stage)
   print(f'{run["id"]}: {result["status"]}',flush=True)
   require(result['status']=='valid',result['error'])
  except Exception as exc:
   write_new(RUNTIME/'STOP.json',{'stage':stage,'run':run,'at':now(),'error':str(exc)});raise

def freeze(stage):
 prerequisites(stage);entries=[]
 for run in order(stage):
  directory=RUNTIME/stage/run['id'];result=read(directory/'validation.json');reservation=read(directory/'reservation.json')
  require(result['status']=='valid','Failed run')
  require(reservation['prepared_commit']==read(RUNTIME/f'{stage}-reservation.json')['commit'],'Commit changed during measurement')
  require((directory/'prompt.txt').read_text()==packet(run,stage),'Prompt changed')
  require(reservation['packet_sha256']==sha(packet(run,stage).encode()),'Reserved packet changed')
  require(reservation['schema_sha256']==c.sha(HERE/f'{stage}-wire.schema.json') and reservation['canonical_schema_sha256']==c.sha(canonical(stage)),'Schema changed')
  require(audit(directory,run['family'],reservation['fresh_session_requested'])==result['metadata'],'Audit changed')
  validate_response(read(directory/'response.json'),stage,run)
  entries.append({**run,'audit':result,'reservation':reservation,'files':{str(p.relative_to(ROOT)):c.sha(p) for p in sorted(directory.iterdir()) if p.is_file()}})
 sessions=[x['audit']['metadata']['session_id'] for x in entries]
 require(len(sessions)==len(set(sessions)),'Duplicate sessions')
 write_new(HERE/f'{stage}-freeze.json',{'at':now(),'prepared_sha256':c.sha(HERE/'prepared.json'),'planned_judgments':len(order(stage)),'runs':entries})

def frozen(stage,private=False):
 verify();v=read(HERE/f'{stage}-freeze.json')
 require(v['prepared_sha256']==c.sha(HERE/'prepared.json'),'Freeze preparation changed')
 require([{k:x[k] for k in ('id','case_id','family')} for x in v['runs']]==order(stage),'Frozen schedule differs')
 if private:
  for entry in v['runs']:verify_inventory(entry['files'])
 return v

def publish(stage):
 for entry in frozen(stage,True)['runs']:
  copy_new(HERE/'judgments'/stage/f'{entry["id"]}.json',(RUNTIME/stage/entry['id']/'response.json').read_bytes())

def published(stage):
 values={}
 for entry in frozen(stage)['runs']:
  path=HERE/'judgments'/stage/f'{entry["id"]}.json'
  require(c.sha(path)==entry['files'][str((RUNTIME/stage/entry['id']/'response.json').relative_to(ROOT))],'Published response changed')
  v=read(path);validate_response(v,stage,entry);values[(entry['case_id'],entry['family'])]=v
 return values

def admit():
 frozen('validity',True);values=published('validity');reviews=read(HERE/'admission-review.json')
 require(len(reviews)==26 and {x['case_id'] for x in reviews}=={x['case_id'] for x in manifest()},'Admission coverage')
 for a in reviews:c.validate_admission(a,{f:values[(a['case_id'],f)] for f in ('A','B')},candidate(a['case_id']))
 v=c.viability(reviews,manifest())
 schedule=[{'id':f'displacement-{a["case_id"]}-{f}','case_id':a['case_id'],'family':f} for a in reviews if a['cohort']!='holdout' for f in ('A','B')] if v['passes'] else []
 random.Random(20260929).shuffle(schedule)
 write_new(HERE/'displacement-order.json',schedule)
 write_new(HERE/'admission.json',{'at':now(),'validity_freeze_sha256':c.sha(HERE/'validity-freeze.json'),'review_sha256':c.sha(HERE/'admission-review.json'),'viability':v,'cases':reviews})
 write_new(HERE/'admission-freeze.json',{'files':{str(p.relative_to(ROOT)):c.sha(p) for p in [HERE/'admission.json',HERE/'admission-review.json',HERE/'displacement-order.json',HERE/'validity-freeze.json',*(HERE/'judgments/validity').glob('*.json')]},'packets':{r['id']:sha(packet(r,'displacement').encode()) for r in schedule}})

def verify_admission(check_commit=False):
 values=published('validity');a=read(HERE/'admission.json');f=read(HERE/'admission-freeze.json');verify_inventory(f['files'])
 require(a['validity_freeze_sha256']==c.sha(HERE/'validity-freeze.json') and a['review_sha256']==c.sha(HERE/'admission-review.json'),'Admission provenance changed')
 require(len(a['cases'])==26 and {x['case_id'] for x in a['cases']}=={x['case_id'] for x in manifest()},'Admission coverage')
 for x in a['cases']:c.validate_admission(x,{fam:values[(x['case_id'],fam)] for fam in ('A','B')},candidate(x['case_id']))
 require(a['viability']==c.viability(a['cases'],manifest()),'Viability mismatch')
 expected={(x['case_id'],fam) for x in a['cases'] if x['cohort']!='holdout' for fam in ('A','B')} if a['viability']['passes'] else set()
 require(len(order('displacement'))==len(expected) and {(x['case_id'],x['family']) for x in order('displacement')}==expected,'Displacement schedule invalid')
 require(f['packets']=={r['id']:sha(packet(r,'displacement').encode()) for r in order('displacement')},'Displacement packet changed')
 if check_commit:
  for name in [*f['files'],str((HERE/'admission-freeze.json').relative_to(ROOT))]:committed(ROOT/name)
  commit=git('log','-1','--format=%H','--',str(HERE/'admission-freeze.json')).decode().strip()
  require(git('show','-s','--format=%s',commit).decode().strip()=='Freeze Experiment B displacement admission','Admission commit missing')


def freeze_failure():
 verify();stop=read(RUNTIME/'STOP.json')
 write_new(HERE/'failure-freeze.json',{'at':now(),'stop':stop,'planned_validity_judgments':52,'planned_displacement_judgments':len(order('displacement')) if (HERE/'displacement-order.json').exists() else None,'files':{str(p.relative_to(ROOT)):c.sha(p) for p in sorted(RUNTIME.rglob('*')) if p.is_file()}})

def analyze():
 import metrics
 verify_admission();values=published('displacement') if order('displacement') else {}
 result=metrics.calculate(values,manifest(),read(HERE/'admission.json')['cases'])
 write_new(HERE/'metrics.json',result)

def verify_results(private=False):
 import metrics
 verify(True)
 if (HERE/'failure-freeze.json').exists():
  if private:verify_inventory(read(HERE/'failure-freeze.json')['files'])
  require((RUNTIME/'STOP.json').exists(),'Missing failure marker');return {'status':'stopped','planned_validity':52}
 verify_admission(True);frozen('validity',private)
 values=published('displacement') if order('displacement') else {}
 if order('displacement'):frozen('displacement',private)
 require(read(HERE/'metrics.json')==metrics.calculate(values,manifest(),read(HERE/'admission.json')['cases']),'Metrics mismatch')
 return {'status':'complete' if order('displacement') else 'inconclusive admission','validity_judgments':52,'displacement_judgments':len(values)}

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['validate','prepare','verify','preflight','run','freeze','publish','admit','analyze','verify-results','freeze-failure']);parser.add_argument('--stage',choices=['validity','displacement'],default='validity');parser.add_argument('--private',action='store_true');args=parser.parse_args()
 actions={'validate':validate_inputs,'prepare':prepare,'verify':lambda:verify(True),'preflight':preflight,'run':lambda:run_all(args.stage),'freeze':lambda:freeze(args.stage),'publish':lambda:publish(args.stage),'admit':admit,'analyze':analyze,'verify-results':lambda:verify_results(args.private),'freeze-failure':freeze_failure}
 print(actions[args.command]() or f'{args.command}: OK')
if __name__=='__main__':main()
