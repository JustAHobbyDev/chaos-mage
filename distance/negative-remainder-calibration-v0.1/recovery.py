"""Additive recovery of H.2's inapplicable absent-conflict representation check.

Frozen scientific packets/schema/configuration, original validator and failed records
remain unchanged. Only the unused resolved flag when present=false is tolerated.
"""
import argparse
import copy
import inspect
import json
from pathlib import Path
import subprocess
import sys
import contracts as c
import runner as r
from common import guard

H,R=r.H,r.R
REC=H/'recovery'
AFFECTED='H3-4d30014ef73c'
ORIGINAL_VALIDATE=c.validate
ORIGINAL_VERIFY_RESULTS=r.verify_results
LINE="    require(conflict['present'] or conflict['resolved'],'Absent conflict cannot be unresolved')\n"
SOURCE=inspect.getsource(ORIGINAL_VALIDATE)
c.require(SOURCE.count(LINE)==1,'Unexpected original validator')
NS=dict(vars(c));exec(SOURCE.replace(LINE,''),NS)
RELAXED=NS['validate']

def validate(value,stage,identity,candidate,unsupported=(),frozen_candidates=()):
    if stage!='artifact':return ORIGINAL_VALIDATE(value,stage,identity,candidate,unsupported)
    # Apply all original assertions except the one inapplicable metadata bit.
    # No JSON field is changed or defaulted, even in memory.
    return RELAXED(value,stage,identity,candidate,unsupported,frozen_candidates)

def install():
    c.validate=validate
    r.verify_results=verify_results

def proof_check():
    evidence=c.read(REC/'evidence.json');r.committed(REC/'evidence.json')
    r.hashes(evidence['frozen_inputs']);r.hashes(evidence['original_runtime_files'])
    c.require(c.sha(H/'contracts.py')==evidence['original_validator_sha256'],'Original validator changed')
    c.require(c.digest(SOURCE.encode())==evidence['original_validation_function_sha256'],'Original validation source changed')
    c.require(c.digest(SOURCE.replace(LINE,'').encode())==evidence['supplementary_validation_function_sha256'],'Supplement changed')
    c.require(evidence['classification']=='recoverable_integrity_violation','Not an engineering recovery')
    c.require(evidence['schema_valid'] and evidence['unchanged_scientific_derivation'],'Missing proof')
    return evidence

def record():
    c.require(r.state()=='TERMINATED_MEASUREMENT','Expected original stop')
    r.verify('artifact',True);guard()
    ids=r.order('artifact');reserved=sorted(p.name for p in (r.RT/'runs/artifact').iterdir())
    c.require(reserved==sorted(ids[:3]) and ids[2]==AFFECTED,'Unexpected reservations')
    d=r.RT/'runs/artifact'/AFFECTED;v=c.read(d/'response.json')
    c.jsonschema.Draft202012Validator(c.schema('artifact')).validate(v)
    c.require(v['remainder_viability']['structural_conflict']['present'] is False,'Conflict is not absent')
    c.require(c.read(d/'validation.json')['error']=='ValueError: Absent conflict cannot be unresolved','Different failure')
    try:r.validate_response(v,'artifact',AFFECTED)
    except ValueError as exc:c.require(str(exc)=='Absent conflict cannot be unresolved','Unexpected rejection')
    else:raise ValueError('Original rejection not reproduced')
    validate(v,'artifact',AFFECTED,r.candidate(AFFECTED),r.unsupported(AFFECTED),c.read(H/'negative-remainders'/f'{AFFECTED}.json')['candidates'])
    # Derivation's result is independent of both diagnostic metadata booleans.
    a=v['remainder_viability']
    for present in [False,True]:
        for resolved in [False,True]:
            c.require(c.derive(a['candidate_remainders'],a['scope_survival']['status'],{'present':present,'resolved':resolved})==a['artifact_status'],'Metadata affects science')
    frozen={**c.read(H/'claim-warrant-prepared.json')['files'],**c.read(H/'artifact-prepared.json')['files']}
    frozen[r.rel(H/'artifact-prepared.json')]=c.sha(H/'artifact-prepared.json')
    r.hashes(frozen)
    runtime=r.inventory(r.RT.rglob('*'))
    r.write(REC/'evidence.json',{'at':r.now(),'classification':'recoverable_integrity_violation',
        'original_stop':'TERMINATED_MEASUREMENT','classification_correction':'The scheduler classified a schema-valid inapplicable metadata-bit rejection as a sent measurement failure; scientific validation and lineage are intact.',
        'authority':'User H.3 handoff authorizes engineering recovery with demonstrated non-contamination; docs/EXPERIMENT-RECOVERY-POLICY.md explicitly permits verifier/metadata-representation recovery.',
        'affected_identity':AFFECTED,'original_validator_sha256':c.sha(H/'contracts.py'),
        'original_validation_function_sha256':c.digest(SOURCE.encode()),
        'supplementary_validation_function_sha256':c.digest(SOURCE.replace(LINE,'').encode()),
        'removed_check':LINE.strip(),'schema_valid':True,'unchanged_scientific_derivation':True,
        'dependency_analysis':'contracts.py is an integrity-manifest dependency but is not sent to the provider. The prompt, schema, config, order and contexts remain byte-identical. The removed assertion constrains only an unused diagnostic flag when no conflict exists. All other validation executes unchanged; no role/productivity judgment is repaired.',
        'frozen_inputs':frozen,'original_runtime_files':runtime,'completed_or_sent':ids[:3],'remaining_unreserved':ids[3:],
        'exact_resume_point':ids[3],'response_sha256':c.sha(d/'response.json'),
        'session_id':c.read(d/'validation.json')['metadata']['session_id'],'original_execution_commit':c.read(d/'reservation.json')['input_commit'],
        'input_allowlist':['PRODUCTIVITY.md','packets/artifact/<case>.txt','schemas/artifact.schema.json','execution-config.json'],
        'isolation_provenance':'Each original reservation records an empty ephemeral working directory, disabled tools/rules/config, exact command and model; raw event audit shows no tool activity or substitution.',
        'no_response_rewrite':True,'no_repeat_request':True})

def supplement():
    evidence=proof_check();install()
    for cid in evidence['completed_or_sent']:
        d=r.RT/'runs/artifact'/cid;value=c.read(d/'response.json');r.validate_response(value,'artifact',cid)
        events=[json.loads(s,object_pairs_hook=c.unique) for s in (d/'events.jsonl').read_text().splitlines() if s.strip()]
        metadata=r.audit_events(events);original=c.read(d/'validation.json')
        c.require(metadata==original['metadata'],'Metadata drift')
        c.require((d/'prompt.txt').read_bytes()==r.packet('artifact',cid).read_bytes(),'Prompt drift')
        finals=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
        c.require(len(finals)==1 and finals[0].strip()==(d/'response.json').read_text().strip(),'Final stream mismatch')
        r.write(d/'supplementary-validation.json',{'status':'valid','at':r.now(),'original_validation_sha256':c.sha(d/'validation.json'),
            'response_sha256':c.sha(d/'response.json'),'recovery_adapter_sha256':c.sha(Path(__file__)),
            'evidence_sha256':c.sha(REC/'evidence.json'),'original_status':original['status'],'metadata':metadata,
            'check':'All original schema, citations, candidate coverage, productivity, viability, scope and status checks pass. Only absent-conflict resolved metadata is inapplicable.'})
    r.transition('PAUSED_RECOVERABLE','Committed positive non-contamination evidence classifies the absent-conflict validator rejection as engineering; original terminal record preserved.')

def preflight():
    evidence=proof_check();install();r.verify('artifact',True);r.binary_check()
    import historical
    checks=historical.all_checks()
    for directory in [H/'tests',REC/'tests']:
        cmd=[sys.executable,'-B','-m','unittest','discover','-s',str(directory),'-p','test_*.py']
        p=subprocess.run(cmd,cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
        checks.append({'command':cmd,'exit_code':p.returncode,'output':p.stdout})
    c.require(sorted(p.name for p in (r.RT/'runs/artifact').iterdir())==sorted(evidence['completed_or_sent']),'Unexpected reservation')
    r.write(REC/'preflight.json',{'at':r.now(),'input_commit':r.head(),'evidence_sha256':c.sha(REC/'evidence.json'),
        'adapter_sha256':c.sha(Path(__file__)),'checks':checks,'remaining':evidence['remaining_unreserved'],'provider_calls':0})
    for x in checks:
        print(x['exit_code'],' '.join(x['command']),flush=True)
        if x['exit_code']:print(x['output'],flush=True)
    c.require(all(x['exit_code']==0 for x in checks),'Recovery preflight failed')

def run():
    evidence=proof_check();install();pre=c.read(REC/'preflight.json');r.committed(REC/'preflight.json');r.committed(Path(__file__))
    c.require(pre['adapter_sha256']==c.sha(Path(__file__)) and pre['evidence_sha256']==c.sha(REC/'evidence.json'),'Recovery binding')
    c.require(all(x['exit_code']==0 for x in pre['checks']),'Recovery checks failed')
    c.require(r.state()=='PAUSED_RECOVERABLE','Explicit classified pause required')
    c.require(not r.git('status','--porcelain').strip(),'Unclean recovery')
    c.require(sorted(p.name for p in (r.RT/'runs/artifact').iterdir())==sorted(evidence['completed_or_sent']),'Reservation drift')
    r.verify('artifact',True);r.binary_check();initial=r.head();r.transition('RUNNING','artifact: committed metadata-validator recovery, only never-reserved cases')
    for index,cid in enumerate(evidence['remaining_unreserved'],4):
        c.require(r.state()=='RUNNING' and r.head()==initial,'Recovery state/checkpoint changed')
        c.require(not r.git('status','--porcelain').strip(),'Unclean call boundary');proof_check();r.verify('artifact',True)
        d=r.execute('artifact',cid)
        r.write(d/'validator-provenance.json',{'adapter_sha256':c.sha(Path(__file__)),'evidence_sha256':c.sha(REC/'evidence.json'),'execution_commit':initial})
        print(f'artifact {index}/15 {cid}: valid',flush=True)
    r.transition('COMPLETE','artifact after additive metadata-validator recovery')

def launch():
    c.require(Path('/proc/1/comm').read_text().strip()=='systemd','Host namespace required');proof_check()
    c.require(not r.git('status','--porcelain').strip(),'Unclean launch')
    with (r.RT/'artifact-recovery-scheduler.log').open('x') as out:
        p=subprocess.Popen([sys.executable,'-B',str(Path(__file__).resolve()),'run'],cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
    r.write(r.RT/'artifact-recovery-scheduler.json',{'pid':p.pid,'launch_commit':r.head(),'adapter_sha256':c.sha(Path(__file__))})
    print('Recovery scheduler:',p.pid)

def freeze():
    proof_check();install();c.require(r.state()=='COMPLETE','Incomplete stage');r.verify('artifact',True);entries=[]
    for cid in r.order('artifact'):
        d=r.RT/'runs/artifact'/cid;validation=c.read(d/'validation.json');extra=d/'supplementary-validation.json'
        c.require(validation['status']=='valid' or extra.exists(),'Failed unsupplemented response')
        if extra.exists():c.require(c.read(extra)['status']=='valid' and c.read(extra)['response_sha256']==c.sha(d/'response.json'),'Invalid supplement')
        r.validate_response(c.read(d/'response.json'),'artifact',cid)
        r.raw(H/'judgments/artifact'/f'{cid}.json',(d/'response.json').read_bytes())
        entries.append({'identity':cid,'reservation':c.read(d/'reservation.json'),'validation':validation,
            'supplementary_validation':c.read(extra) if extra.exists() else None,
            'response_sha256':c.sha(d/'response.json'),'files':r.inventory(d.iterdir())})
    r.write(H/'artifact-freeze.json',{'at':r.now(),'prepared_sha256':c.sha(H/'artifact-prepared.json'),'runs':entries,
        'states':r.inventory((r.RT/'states').glob('*.json')),'recovery_evidence_sha256':c.sha(REC/'evidence.json')})

def verify_results(stage,commit=False):
    if stage=='artifact':
        evidence=proof_check()
        for cid in evidence['completed_or_sent']:
            d=r.RT/'runs/artifact'/cid;s=c.read(d/'supplementary-validation.json')
            c.require(s['original_validation_sha256']==c.sha(d/'validation.json') and s['response_sha256']==c.sha(d/'response.json'),'Supplement lineage changed')
        f=c.read(H/'artifact-freeze.json');c.require(f['recovery_evidence_sha256']==c.sha(REC/'evidence.json'),'Recovery freeze changed')
    return ORIGINAL_VERIFY_RESULTS(stage,commit)

def publication(action):
    install();proof_check();import publication as pub
    result=getattr(pub,'write' if action=='publish' else 'seal' if action=='seal' else 'verify')()
    if result:print(json.dumps(result,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['record','supplement','preflight','run','launch','freeze','verify','publish','seal']);a=p.parse_args()
    if a.action in ['verify','publish','seal']:publication(a.action)
    else:globals()[a.action]()
