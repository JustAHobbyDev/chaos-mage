"""Additive preservation of terminal H.6 evidence. No launch or retry capability."""
from pathlib import Path
import json
import sys
from jsonschema import Draft202012Validator
import runner as r
import contracts as c
H=r.H;RT=r.RT

def freeze():
    r.verify(True)
    states=[r.read(p) for p in sorted((RT/'states').glob('*.json'))]
    r.require(any(s['state']=='TERMINATED_MEASUREMENT' for s in states),'No terminal observation')
    # A later prelaunch cancellation wrote PAUSED_AMBIGUOUS. Preserve it and make
    # the already-recorded terminal scientific outcome authoritative again.
    r.transition('TERMINATED_MEASUREMENT','Publication adjudication: original C027 provider-capacity failure remains terminal; C028 prelaunch cancellation cannot reopen it. No resume.')
    files={};success=[];failed=[];unlaunched=[]
    stage='claim-judgments'
    for d in sorted((RT/'runs'/stage).iterdir()):
        for p in sorted(d.iterdir()):
            dst=H/'raw'/stage/d.name/p.name;r.raw(dst,p.read_bytes());files[r.rel(dst)]=r.sha(dst)
        if (d/'validation.json').exists():
            dst=H/stage/(d.name+'.json');r.raw(dst,(d/'response.json').read_bytes());files[r.rel(dst)]=r.sha(dst);success.append(d.name)
        elif r.read(d/'failure.json')['launched']:failed.append(d.name)
        else:unlaunched.append(d.name)
    planned=[x['id'] for x in r.read(H/f'{stage}-prepared.json')['runs']]
    reserved=success+failed+unlaunched
    r.write(H/'claim-judgments-partial-freeze.json',{'at':r.now(),'status':'TERMINATED_MEASUREMENT','execution_commit':'31c560d5f41ccda9cd857db07f670e1b9f70b323','planned_claim_judgments':len(planned),'successful':success,'failed_provider_observations':failed,'reserved_but_unlaunched':unlaunched,'never_reserved':[x for x in planned if x not in reserved],'files':files})
    state_files={}
    for p in sorted((RT/'states').glob('*.json')):
        dst=H/'execution-states'/p.name;r.raw(dst,p.read_bytes());state_files[r.rel(dst)]=r.sha(dst)
    r.write(H/'terminal-state-freeze.json',{'at':r.now(),'files':state_files})
    r.write(H/'final-runtime-freeze.json',{'at':r.now(),'status':'TERMINATED_MEASUREMENT','files':r.inventory(RT.rglob('*'))})
    print(json.dumps({'success':len(success),'provider_failures':failed,'unlaunched':unlaunched,'never_reserved':len(planned)-len(reserved)}))

def verify():
    result=r.verify();sessions=[];completed=0;diagnostics=[]
    for stage in ['generation','claims','claim-judgments']:
        for path in sorted((H/stage).glob('*.json')):
            uid=path.stem;cid=uid.split('--')[0];d=H/'raw'/stage/uid
            r.require((d/'request.txt').read_bytes()==(H/'packets'/stage/f'{uid}.txt').read_bytes(),'Request drift')
            r.require((d/'response.json').read_bytes()==path.read_bytes(),'Response drift')
            events=[json.loads(l,object_pairs_hook=r.unique) for l in (d/'events.jsonl').read_text().splitlines() if l.strip()]
            meta=r.audit_events(events);sessions.append(meta['session_id']);v=r.read(d/'validation.json')
            r.require(v['metadata']==meta,'Metadata replay drift')
            finals=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
            r.require(len(finals)==1 and finals[0].strip()==path.read_text().strip(),'Final stream mismatch')
            value=r.read(path);Draft202012Validator(r.read(H/'schemas'/f'{stage}.schema.json')).validate(value)
            if stage!='generation':
                actual=c.citation_checks(r.read(H/'span-tables'/f'{cid}.json'),value)+c.semantic_checks(stage,value,r.read(H/'packets'/stage/f'{uid}.json'))
                r.require(actual==v['diagnostics'],'Diagnostic replay drift');diagnostics.extend(actual)
            reservation=r.read(d/'reservation.json')
            r.require(reservation['available_mapping_packets']==[cid] and not reservation['collision_exposure'],'Packet context mismatch')
            r.require(reservation['configuration']==r.config(),'Configuration drift')
            completed+=1
    part=r.read(H/'claim-judgments-partial-freeze.json');failed=part['failed_provider_observations'];r.require(failed==['H6-T05-1--C027'],'Unexpected failed observation')
    d=H/'raw/claim-judgments'/failed[0];events=[json.loads(l) for l in (d/'events.jsonl').read_text().splitlines()]
    r.require(any(e.get('type')=='turn.failed' and e['error']['message']=='Selected model is at capacity. Please try a different model.' for e in events),'Provider failure mismatch')
    sessions.extend(e['thread_id'] for e in events if e.get('type')=='thread.started')
    stopped_at=r.read(d/'failure.json')['at']
    for process_record in (H/'raw/claim-judgments').glob('*/process.json'):
        r.require(r.read(process_record)['launched_at']<=stopped_at,'Provider launch after observed terminal failure')
    for uid in part['reserved_but_unlaunched']:
        d=H/'raw/claim-judgments'/uid;r.require(not (d/'process.json').exists() and not (d/'events.jsonl').exists(),'Unlaunched evidence mismatch')
        r.require(r.read(d/'failure.json')['launched'] is False,'Unlaunched flag mismatch')
    r.require(len(sessions)==len(set(sessions)),'Reused session')
    for stage in ['remainder-inventory','artifact-judgments']:
        r.require(not list((H/stage).glob('*.json')) and not list((RT/'runs'/stage).glob('*')),'Unauthorized downstream measurement')
    r.require(not (H/'claim-judgments-freeze.json').exists(),'Incomplete stage represented as complete')
    r.require(r.state()=='TERMINATED_MEASUREMENT','Terminal state not authoritative')
    result.update(completed_observations=completed,provider_failure_observations=len(failed),unique_started_sessions=len(sessions),mechanical_or_relational_diagnostics=len(diagnostics),downstream_calls=0,partial_evidence_verified=True)
    return result
if __name__=='__main__':
    if sys.argv[1]=='freeze':freeze()
    else:print(json.dumps(verify(),indent=2))
