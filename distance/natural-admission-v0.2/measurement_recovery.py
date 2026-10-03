"""Additive local recovery for later H7 measurements; never retries or launches."""
import json
import continuation as c
import admission


def review(r,stage,uid):
    r.verify();r.require(r.state()=='PAUSED_AMBIGUOUS','Preserve runner pause first')
    baseline=c.verify_evidence(r);cid=admission.mapping_id(uid)
    event=c.inspect_attempt(r,stage,uid)
    if event['classification']=='PROVIDER_OBSERVATION_FAILURE':
        d=r.RT/'attempts'/stage/uid
        # A complete captured scientific response is preserved, even if invalid.
        # Provenance/model/context failures are NOT auto-cleared by this adapter.
        events=[json.loads(x) for x in (d/'events.jsonl').read_text().splitlines()]
        r.audit(events,(d/'response.json').read_text())
        r.require(event['request_match'] and event['configuration_match'] and event['context_intact'] and event['unique_attempt'],'Observation lineage unresolved')
        r.require(not (d/'validation.json').exists(),'Valid observation is not a failure')
        event['request_launched']=True
        event['mapping_disposition']={'instrumentation':'FAILURE','admission':'UNMEASURED','end_to_end_complete':False,'retry':'FORBIDDEN','replacement':'FORBIDDEN'}
        event['stage_rule']='Existing H7 UNMEASURED recovery boundary item 1: local response/routing failure. No no-observation semantics applied.'
    else:r.require(event['classification']=='PROVIDER_NO_OBSERVATION','Unresolved observation/launch ambiguity; no continuation')
    rows=c.ledger(r);attempts=list((r.RT/'attempts').glob('*/*/attempt.json'));sessions=[];paths=[]
    r.require(len(rows)==len(attempts),'Reservations/attempts mismatch')
    failure_at=r.read(r.RT/'attempts'/stage/uid/'attempt.json')['at']
    for p in attempts:
        a=r.read(p);d=p.parent
        r.require(a['at']<=failure_at,'Unexpected post-failure launch')
        match=[x for x in rows if x['session']==a['stage']+'/'+a['packet_id']]
        r.require(len(match)==1 and match[0]['state']=='FINISHED' and json.loads(match[0]['command_json'])==a['command'],'Unresolved budget/launch identity')
        es=[json.loads(x) for x in (d/'events.jsonl').read_text().splitlines()]
        ss=[e['thread_id'] for e in es if e.get('type')=='thread.started'];r.require(len(ss)==1,'Unresolved session');sessions+=ss
        r.require(r.sha(d/'request.txt')==a['request_sha256']==r.sha(r.H/'packets'/a['stage']/(a['packet_id']+'.txt')),'Request lineage drift')
        for q in d.iterdir():
            dest=r.H/'raw'/a['stage']/a['packet_id']/q.name
            if dest.exists():r.require(dest.read_bytes()==q.read_bytes(),'Raw changed')
            else:r.raw(dest,q.read_bytes())
            paths.append(dest)
    r.require(len(set(sessions))==len(sessions),'Duplicate session')
    independence={}
    for other in r.order():
        if other==cid or other in c.quarantined(r):continue
        r.require(baseline['continuation_independence']['unaffected'][other]['independent'] is True,'Baseline independence unresolved')
        inputs=[]
        for p in (r.H/'packets').glob('*/*.json'):
            if p.stem.split('--')[0]!=other:continue
            packet=r.read(p)
            r.require(packet['packet_id']==other and event['session_id'] not in p.read_text(),'Contaminated scientific input')
            inputs += [p,p.with_suffix('.txt')]
        independence[other]={'independent':True,'files':r.inventory(inputs),'evidence':'Frozen packet inputs reverified; mapping-only builders exclude foreign responses; fresh unique sessions; no shared prompt/schema/model/reasoning/input change; no post-failure launch. All reservations and attempts reconciled.'}
    event['independence_review']={'status':'VERIFIED','unaffected':independence}
    event['authority']=c.AUTHORITY
    p=r.H/'review/quarantines'/f'{cid}.json';r.write(p,event);paths.append(p)
    pause=sorted((r.RT/'states').glob('*.json'))[-1]
    p=r.H/'review'/f'{uid}-{stage}-pause-state.json';r.raw(p,pause.read_bytes());paths.append(p)
    r.write(r.H/f'{uid}-{stage}-incident-freeze.json',{'parent_commit':r.head(),'files':r.inventory(paths)})
    return event


def resume(r,cid):
    r.verify();r.require(not r.git('status','--porcelain'),'Commit incident and independence evidence')
    r.require(r.state()=='PAUSED_AMBIGUOUS','Wrong pause state')
    event=r.read(r.H/'review/quarantines'/f'{cid}.json')
    r.require(event['classification'] in ('PROVIDER_NO_OBSERVATION','PROVIDER_OBSERVATION_FAILURE') and event['independence_review']['status']=='VERIFIED','Unresolved event')
    c.verify_evidence(r)
    r.transition('COMPLETE','Authorized independent continuation after final local quarantine of '+cid+'; no retry/replacement; not run completion.')
    p=sorted((r.RT/'states').glob('*.json'))[-1]
    r.raw(r.H/'review'/f'{cid}-measurement-resume-state.json',p.read_bytes())
