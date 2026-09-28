#!/usr/bin/env python3
"""B.1: immutable two-stage admission and direct comparison collection."""
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
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
PRIOR=ROOT/'distance/displacement-v0.3'
RUNTIME=ROOT/'.runtime/comparative-displacement-v0.3'
spec=importlib.util.spec_from_file_location('b1_frozen_event_audit',ROOT/'distance/boundary-v0.2/harness.py')
legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
read,require=c.read,c.require
def now():return datetime.now(timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def config():return read(HERE/'execution-config.json')
def manifest():return read(HERE/'operator-manifest.json')['mappings']
def candidate(cid):return read(HERE/'mappings'/f'{cid}.json')
def order(stage):return read(HERE/f'{stage}-order.json')
def canonical(stage):return HERE/('validity.schema.json' if stage=='validity' else 'output.schema.json')
def write_new(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('x') as f:f.write(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def copy_new(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('xb') as f:f.write(data)
def projection(v):
 if isinstance(v,dict):return {k:projection(x) for k,x in v.items() if k not in ('$schema','$id','allOf')}
 if isinstance(v,list):return [projection(x) for x in v]
 return v
def verify_inventory(files):
 for name,digest in files.items():require(c.sha(ROOT/name)==digest,'Hash changed: '+name)
def committed(path,revision='HEAD'):require(git('show',f'{revision}:{path.relative_to(ROOT)}')==path.read_bytes(),'Uncommitted input: '+str(path))
def preservation(private=False):
 inv=read(HERE/'preservation.json');verify_inventory(inv['files'])
 if private:verify_inventory(inv['private_files'])
def checkpoint(name):return git('log','-1','--format=%H','--',str(HERE/name)).decode().strip()
def check_commit(name,title):
 commit=checkpoint(name);require(git('show','-s','--format=%s',commit).decode().strip()==title,'Missing checkpoint: '+title);return commit
def validate_inputs():
 preservation();m=manifest();require(len(m)==28 and sum(x['new'] for x in m)==8,'Expected 20 old and eight new mappings')
 require(len({x['mapping_id'] for x in m})==28,'Duplicate mapping ID')
 import yaml
 for row in m:
  d=c.validate(candidate(row['mapping_id']),'candidate');base=read(HERE/'baselines'/f'{row["target_id"]}.json')
  require(d['case_id']==row['mapping_id'],'Candidate ID mismatch')
  require(d['target']['domain']==base['target_domain'] and d['target']['question']==base['target_task'],'Baseline target drift')
  require((HERE/'baselines'/f'{row["target_id"]}.json').read_bytes()==(PRIOR/'baselines'/f'{row["target_id"]}.json').read_bytes(),'Baseline bytes changed')
  src=yaml.safe_load((ROOT/row['source_path']).read_text())
  require(src['extraction']['status']=='accepted' and d['source']=={'name':src['extraction']['name'],'practice':src['extraction']['practice'],'instrument':src['instrument']},'Instrument changed')
  if not row['new']:
   original=read(PRIOR/'cases'/f'{row["historical_case_id"]}.json');original['case_id']=row['mapping_id'];require(d==original,'Historical candidate changed')
   for family in 'AB':
    j=read(PRIOR/'judgments/validity'/f'validity-{row["historical_case_id"]}-{family}.json')
    c.validate(j,'validity',read(PRIOR/'cases'/f'{row["historical_case_id"]}.json'));require(j['validity']['final_status']=='Valid' and not j['validity']['unresolved_conditions'],'Historical mapping ineligible')
 for stage in ('validity','comparison'):require(read(HERE/f'{stage}-wire.schema.json')==projection(read(canonical(stage))),'Wire projection changed')
 require((HERE/'CLASSIFIER-validity.md').read_bytes()==(ROOT/'distance/v0.3/CLASSIFIER-transfer-validity.md').read_bytes(),'Validity instructions changed')
 require((HERE/'validity.schema.json').read_bytes()==(ROOT/'distance/v0.3/validity.schema.json').read_bytes(),'Validity schema changed')
 expected={(x['mapping_id'],f) for x in m if x['new'] for f in 'AB'}
 require(len(order('validity'))==16 and {(x['case_id'],x['family']) for x in order('validity')}==expected,'Validity schedule coverage')
 designs=read(HERE/'operator-manifest.json')['pair_designs'];require(len(designs)==28 and len({(x['mapping_1'],x['mapping_2']) for x in designs})==28,'Pair design coverage')
 by={x['mapping_id']:x for x in m}
 for x in designs:require(by[x['mapping_1']]['target_id']==by[x['mapping_2']]['target_id']==x['target_id'],'Cross-target design')
def pair_records():return read(HERE/'pairs.json')
def comparison_packet(pair):
 a,b=(candidate(pair['mapping_'+slot]) for slot in 'AB')
 # Only allowlisted fields enter the judge context; provenance remains outside.
 content={'case_id':pair['case_id'],'target_question':a['target']['question']}
 for slot,d in zip('AB',(a,b)):
  content['mapping_'+slot]={'source':d['source'],'evidence_context':d['target']['evidence'],'mapping':d['mapping']}
 baseline=(HERE/'baselines'/f'{pair["target_id"]}.json').read_bytes()
 body=json.dumps(content,indent=2,ensure_ascii=False)[:-2]+',\n  "ordinary_practice_baseline": '+baseline.decode()+'}\n'
 require(baseline in body.encode(),'Missing exact baseline bytes');json.loads(body)
 return (HERE/'CLASSIFIER.md').read_text()+'\n\nCASE PACKET\n'+body
def packet(run,stage='validity'):
 if stage=='validity':return (HERE/'CLASSIFIER-validity.md').read_text()+'\n\nCASE PACKET\n'+json.dumps(candidate(run['case_id']),indent=2,ensure_ascii=False)+'\n'
 return comparison_packet(next(x for x in pair_records() if x['case_id']==run['case_id']))
def validate_response(value,stage,run):
 c.validate(value,stage,candidate(run['case_id']) if run and stage=='validity' else ({'case_id':run['case_id']} if run else None))
def check_fresh_session(session,directory):
 require(bool(session),'Missing session ID')
 for p in RUNTIME.rglob('validation.json'):
  if p.parent!=directory:
   v=read(p);require(not v.get('metadata') or v['metadata']['session_id']!=session,'Duplicate session')

# Provider invocation functions below are copied from the audited Experiment B
# adapter, with stage schema paths supplied by this module. No old runner is edited.

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
    with tempfile.TemporaryDirectory(prefix='comparative-isolated-') as cwd:
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
 if stage=='validity':return {'case_id':'PREFLIGHT','validity':{'mechanism_fidelity':{'status':'preserved','rationale':'Formatting fixture only.'},'target_fidelity':{'status':'addressed','rationale':'Formatting fixture only.'},'operational_coherence':{'status':'coherent','rationale':'Formatting fixture only.'},'target_reframe':{'occurred':False,'original_question':None,'reframed_question':None,'relationship':None},'unresolved_conditions':[],'final_status':'Valid','rationale':'Formatting fixture only.'},'uncertainty':[]}
 mapping={'counterfactual_native':{'status':'uncertain','rationale':'Formatting fixture only.'},'scope':{'local_displacement':'low','global_propagation':'low','rationale':'Formatting fixture only.'}}
 return {'case_id':'PREFLIGHT','criteria':{d:{'relation':'tie','rationale':'Formatting fixture only.'} for d in c.CRITERIA},'mapping_A':mapping,'mapping_B':mapping,'decisive_basis':{'primary_criterion':'none',**{k:'Formatting fixture only.' for k in ('centrality','propagation','irreducibility','rationale')}},'overall_relation':'tie','confidence':'clear','uncertainty':[]}
def prepare():
 validate_inputs();preservation(True)
 files=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='prepared.json']
 files+=[ROOT/'docs/PROBLEM_FRAMES-comparative-displacement-v0.3.md']
 write_new(HERE/'prepared.json',{'created_at':now(),'starting_commit':git('rev-parse','HEAD').decode().strip(),'files':{str(p.relative_to(ROOT)):c.sha(p) for p in sorted(files)},'validity_packets':{r['id']:sha(packet(r).encode()) for r in order('validity')}})
def verify(committed_inputs=False):
 validate_inputs();v=read(HERE/'prepared.json');verify_inventory(v['files'])
 require(v['validity_packets']=={r['id']:sha(packet(r).encode()) for r in order('validity')},'Validity packet drift')
 if committed_inputs:
  for name in [*v['files'],str((HERE/'prepared.json').relative_to(ROOT))]:committed(ROOT/name)
  commit=check_commit('prepared.json','Prepare comparative displacement Experiment B.1')
  require(subprocess.run(['git','merge-base','--is-ancestor',v['starting_commit'],commit],cwd=ROOT).returncode==0,'Starting ancestry mismatch')
 return v
def preflight():
 verify(True);write_new(RUNTIME/'preflight-reservation.json',{'started_at':now(),'commit':git('rev-parse','HEAD').decode().strip()});entries=[]
 try:
  for stage in ('validity','comparison'):
   for family in 'AB':
    verify(True);d=RUNTIME/'preflight'/stage/family
    result=execute(family,d,'Return exactly this artificial formatting fixture; no classification, tools or external context.\n'+json.dumps(probe_response(stage)),stage=stage)
    print(f'probe {stage} {family}: {result["status"]}',flush=True);entries.append({'stage':stage,'family':family,'audit':result});require(result['status']=='valid',result['error'])
 except Exception as exc:
  write_new(RUNTIME/'STOP.json',{'stage':'preflight','at':now(),'error':str(exc)});raise
 write_new(HERE/'preflight.json',{'frozen_at':now(),'prepared_sha256':c.sha(HERE/'prepared.json'),'entries':entries,'files':{str(p.relative_to(ROOT)):c.sha(p) for p in sorted((RUNTIME/'preflight').rglob('*')) if p.is_file()}})
def prerequisites(stage):
 verify(True);p=read(HERE/'preflight.json');committed(HERE/'preflight.json');check_commit('preflight.json','Freeze comparative displacement provider probes')
 require(p['prepared_sha256']==c.sha(HERE/'prepared.json'),'Probe preparation mismatch');verify_inventory(p['files'])
 require(len(p['entries'])==4 and all(x['audit']['status']=='valid' for x in p['entries']),'Four successful probes required')
 require(not (RUNTIME/'STOP.json').exists(),'Scheduling stopped; explicit recorded recovery required')
 if stage=='comparison':verify_admission(True);require(read(HERE/'admission.json')['viability']['passes'],'Admission viability failed')
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
  d=RUNTIME/stage/run['id'];result=read(d/'validation.json');reservation=read(d/'reservation.json')
  require(result['status']=='valid','Failed run');require(reservation['prepared_commit']==read(RUNTIME/f'{stage}-reservation.json')['commit'],'Commit changed during collection')
  require((d/'prompt.txt').read_bytes()==packet(run,stage).encode(),'Prompt changed');require(reservation['packet_sha256']==sha(packet(run,stage).encode()),'Reserved prompt changed')
  require(reservation['schema_sha256']==c.sha(HERE/f'{stage}-wire.schema.json') and reservation['canonical_schema_sha256']==c.sha(canonical(stage)),'Schema changed')
  require(audit(d,run['family'],reservation['fresh_session_requested'])==result['metadata'],'Audit changed');validate_response(read(d/'response.json'),stage,run)
  entries.append({**run,'audit':result,'reservation':reservation,'files':{str(p.relative_to(ROOT)):c.sha(p) for p in sorted(d.iterdir()) if p.is_file()}})
 require(len({x['audit']['metadata']['session_id'] for x in entries})==len(entries),'Duplicate sessions')
 write_new(HERE/f'{stage}-freeze.json',{'at':now(),'prepared_sha256':c.sha(HERE/'prepared.json'),'planned_judgments':len(order(stage)),'runs':entries})
def frozen(stage,private=False):
 v=read(HERE/f'{stage}-freeze.json');require(v['prepared_sha256']==c.sha(HERE/'prepared.json'),'Freeze input changed')
 require([{k:x[k] for k in ('id','case_id','family')} for x in v['runs']]==order(stage),'Frozen schedule changed')
 if private:
  for x in v['runs']:verify_inventory(x['files'])
 return v
def publish(stage):
 for x in frozen(stage,True)['runs']:copy_new(HERE/'judgments'/stage/f'{x["id"]}.json',(RUNTIME/stage/x['id']/'response.json').read_bytes())
def published(stage):
 values={}
 for x in frozen(stage)['runs']:
  p=HERE/'judgments'/stage/f'{x["id"]}.json';require(c.sha(p)==x['files'][str((RUNTIME/stage/x['id']/'response.json').relative_to(ROOT))],'Published payload changed')
  v=read(p);validate_response(v,stage,x);values[(x['case_id'],x['family'])]=v
 return values
def admission_rows():
 frozen('validity',True);values=published('validity');rows=[]
 for m in manifest():
  judgments={};paths={}
  for f in 'AB':
   path=HERE/'judgments/validity'/f'validity-{m["mapping_id"]}-{f}.json' if m['new'] else PRIOR/'judgments/validity'/f'validity-{m["historical_case_id"]}-{f}.json'
   judgments[f]=values[(m['mapping_id'],f)] if m['new'] else read(path);paths[f]=str(path.relative_to(ROOT))
  statuses={f:judgments[f]['validity']['final_status'] for f in 'AB'}
  admitted=all(statuses[f]=='Valid' and not judgments[f]['validity']['unresolved_conditions'] for f in 'AB')
  row={'mapping_id':m['mapping_id'],'target_id':m['target_id'],'admitted':admitted,'origin':'new' if m['new'] else 'historical','validity_A':statuses['A'],'validity_B':statuses['B'],'judgment_files':paths,'judgment_sha256':{f:c.sha(ROOT/paths[f]) for f in 'AB'}}
  c.validate(row,'admission');rows.append(row)
 return rows
def construct_pairs(admissions):
 design=read(HERE/'design.json');ids={x['mapping_id'] for x in admissions if x['admitted']}
 specs=[x for x in read(HERE/'operator-manifest.json')['pair_designs'] if x['mapping_1'] in ids and x['mapping_2'] in ids]
 tags={t for x in specs for t in x['tags']};targets={x['target_id'] for x in specs}
 viability={'primary_pairs':len(specs),'targets':sorted(targets),'coverage_tags':sorted(tags),'different_source_pairs':sum('different-source' in x['tags'] for x in specs)}
 viability['passes']=design['minimum_pairs']<=len(specs)<=design['maximum_pairs'] and targets==set(design['targets']) and set(design['required_tags'])<=tags and viability['different_source_pairs']>len(specs)/2
 if not viability['passes']:return [],[],viability
 rng=random.Random(design['seeds']['orientation']);pairs=[]
 for attempt in range(1000):
  pairs=[];odd=0
  for target in sorted(targets):
   group=sorted((x for x in specs if x['target_id']==target),key=lambda x:(x['mapping_1'],x['mapping_2']))
   flags=[False]*(len(group)//2)+[True]*(len(group)//2)
   if len(group)%2:flags.append(bool(odd%2));odd+=1
   rng.shuffle(flags)
   for s,flip in zip(group,flags):
    pairs.append({'target_id':target,'mapping_1':s['mapping_1'],'mapping_2':s['mapping_2'],'mapping_A':s['mapping_2'] if flip else s['mapping_1'],'mapping_B':s['mapping_1'] if flip else s['mapping_2'],'baseline_sha256':c.sha(HERE/'baselines'/f'{target}.json'),'cohort':'primary','control_of':None})
  orientations=[]
  for p in pairs:
   s=next(s for s in specs if (s['mapping_1'],s['mapping_2'])==(p['mapping_1'],p['mapping_2']))
   if s['expected'] in ('mapping_1_more','mapping_2_more'):orientations.append(p['mapping_A']==p[s['expected'].removesuffix('_more')])
  if len(orientations)<2 or len(set(orientations))==2:break
 else:raise ValueError('Cannot counterbalance intended directions')
 rng.shuffle(pairs)
 for i,p in enumerate(pairs,1):p['case_id']=f'C{i:03}'
 crng=random.Random(design['seeds']['controls']);remaining=pairs.copy();crng.shuffle(remaining);seen_tags=set();seen_targets=set();controls=[]
 lookup={(x['mapping_1'],x['mapping_2']):x for x in specs}
 for i in range(design['orientation_controls']):
  best=max(remaining,key=lambda p:(len(set(lookup[(p['mapping_1'],p['mapping_2'])]['tags'])-seen_tags),p['target_id'] not in seen_targets))
  remaining.remove(best);seen_tags.update(lookup[(best['mapping_1'],best['mapping_2'])]['tags']);seen_targets.add(best['target_id'])
  controls.append({**best,'case_id':f'C{len(pairs)+i+1:03}','mapping_A':best['mapping_B'],'mapping_B':best['mapping_A'],'cohort':'orientation-control','control_of':best['case_id']})
 # IDs do not reveal cohort: shuffle a neutral permutation across all cases.
 allpairs=pairs+controls;labels=[p['case_id'] for p in allpairs];crng.shuffle(labels);rename={p['case_id']:label for p,label in zip(allpairs,labels)}
 for p in allpairs:
  old=p['case_id'];p['case_id']=rename[old]
  if p['control_of']:p['control_of']=rename[p['control_of']]
 allpairs.sort(key=lambda p:p['case_id'])
 schedule=[{'id':f'comparison-{p["case_id"]}-{f}','case_id':p['case_id'],'family':f} for p in allpairs for f in 'AB'];random.Random(design['seeds']['schedule']).shuffle(schedule)
 return allpairs,schedule,viability
def admit():
 rows=admission_rows();pairs,schedule,viability=construct_pairs(rows)
 write_new(HERE/'admission.json',{'at':now(),'validity_freeze_sha256':c.sha(HERE/'validity-freeze.json'),'mappings':rows,'viability':viability})
 write_new(HERE/'pairs.json',pairs);write_new(HERE/'comparison-order.json',schedule)
 for p in pairs:copy_new(HERE/'packets'/f'{p["case_id"]}.txt',comparison_packet(p).encode())
 files=[HERE/'admission.json',HERE/'pairs.json',HERE/'comparison-order.json',HERE/'validity-freeze.json',*(HERE/'judgments/validity').glob('*.json'),*(HERE/'packets').glob('*.txt')]
 write_new(HERE/'admission-freeze.json',{'at':now(),'files':{str(p.relative_to(ROOT)):c.sha(p) for p in sorted(files)},'packets':{r['id']:sha(packet(r,'comparison').encode()) for r in schedule}})
def verify_admission(check_committed=False):
 rows=admission_rows();a=read(HERE/'admission.json');require(a['mappings']==rows,'Admission changed');require(a['validity_freeze_sha256']==c.sha(HERE/'validity-freeze.json'),'Validity freeze changed')
 pairs,schedule,viability=construct_pairs(rows);require(pair_records()==pairs and order('comparison')==schedule and a['viability']==viability,'Pair derivation changed')
 mappings={r['mapping_id']:candidate(r['mapping_id']) for r in manifest()};baselines={r['target_id']:read(HERE/'baselines'/f'{r["target_id"]}.json') for r in manifest()}
 for p in pairs:
  c.validate_pair(p,mappings,baselines,{r['mapping_id']:r for r in rows})
  require(p['baseline_sha256']==c.sha(HERE/'baselines'/f'{p["target_id"]}.json'),'Pair baseline hash mismatch')
  require((HERE/'packets'/f'{p["case_id"]}.txt').read_bytes()==comparison_packet(p).encode(),'Published packet changed')
 f=read(HERE/'admission-freeze.json');verify_inventory(f['files']);require(f['packets']=={r['id']:sha(packet(r,'comparison').encode()) for r in schedule},'Packet freeze changed')
 if check_committed:
  for name in [*f['files'],str((HERE/'admission-freeze.json').relative_to(ROOT))]:committed(ROOT/name)
  check_commit('admission-freeze.json','Freeze comparative displacement admission and pairs')
def freeze_failure():
 verify();stop=read(RUNTIME/'STOP.json')
 write_new(HERE/'failure-freeze.json',{'at':now(),'stop':stop,'planned_validity_judgments':16,'planned_comparison_judgments':len(order('comparison')) if (HERE/'comparison-order.json').exists() else None,'files':{str(p.relative_to(ROOT)):c.sha(p) for p in sorted(RUNTIME.rglob('*')) if p.is_file()}})
def analyze():
 import metrics
 verify(True);verify_admission(True);frozen('comparison',True)
 write_new(HERE/'metrics.json',metrics.calculate(published('comparison'),pair_records()))
def verify_results(private=False):
 import metrics
 verify(True);preservation(private)
 if (HERE/'failure-freeze.json').exists():
  if private:verify_inventory(read(HERE/'failure-freeze.json')['files'])
  return {'status':'stopped'}
 verify_admission(True);frozen('validity',private)
 if not read(HERE/'admission.json')['viability']['passes']:return {'status':'incomplete admission'}
 frozen('comparison',private);require(read(HERE/'metrics.json')==metrics.calculate(published('comparison'),pair_records()),'Metrics changed')
 return {'status':'complete','primary_pairs':sum(p['cohort']=='primary' for p in pair_records()),'orientation_controls':sum(p['cohort']=='orientation-control' for p in pair_records()),'comparison_judgments':len(published('comparison'))}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['validate','prepare','verify','preflight','run','freeze','publish','admit','analyze','verify-results','freeze-failure']);p.add_argument('--stage',choices=['validity','comparison'],default='validity');p.add_argument('--private',action='store_true');a=p.parse_args()
 actions={'validate':validate_inputs,'prepare':prepare,'verify':lambda:verify(True),'preflight':preflight,'run':lambda:run_all(a.stage),'freeze':lambda:freeze(a.stage),'publish':lambda:publish(a.stage),'admit':admit,'analyze':analyze,'verify-results':lambda:verify_results(a.private),'freeze-failure':freeze_failure}
 print(actions[a.command]() or a.command+': OK')
if __name__=='__main__':main()
