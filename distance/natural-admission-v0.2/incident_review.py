"""Offline incident preservation. No automatic state clearing or provider work."""
import json
import continuation as c


def preserve_and_review(r, stage, cid):
    r.require(r.state()=='PAUSED_AMBIGUOUS','Expected preserved scheduling pause')
    r.verify(); baseline=c.verify_evidence(r)
    event=c.inspect_attempt(r,stage,cid)
    r.require(event['classification']=='PROVIDER_NO_OBSERVATION','Material ambiguity/returned observation requires separate frozen-rule review')
    r.require(r.read(r.RT/'attempts'/stage/cid/'exit.json')['timeout'] is True,'Expected known timeout termination')
    rows=c.ledger(r);attempts=list((r.RT/'attempts').glob('*/*/attempt.json'))
    r.require(len(rows)==len(attempts),'Reservations and attempts differ')
    sessions=[];paths=[]
    failure_at=r.read(r.RT/'attempts'/stage/cid/'attempt.json')['at']
    for p in attempts:
        a=r.read(p);d=p.parent
        r.require(a['at']<=failure_at,'Post-failure launch')
        match=[row for row in rows if row['session']==a['stage']+'/'+a['packet_id']]
        r.require(len(match)==1 and match[0]['state']=='FINISHED' and json.loads(match[0]['command_json'])==a['command'],'Unresolved reservation')
        events=[json.loads(x) for x in (d/'events.jsonl').read_text().splitlines()]
        ss=[e['thread_id'] for e in events if e.get('type')=='thread.started']
        r.require(len(ss)==1,'Unknown session');sessions+=ss
        r.require(r.sha(d/'request.txt')==a['request_sha256']==r.sha(r.H/'packets'/a['stage']/(a['packet_id']+'.txt')),'Request drift')
        for q in d.iterdir():
            dest=r.H/'raw'/a['stage']/a['packet_id']/q.name
            if dest.exists():r.require(dest.read_bytes()==q.read_bytes(),'Raw drift')
            else:r.raw(dest,q.read_bytes())
            paths.append(dest)
    r.require(len(set(sessions))==len(sessions),'Session duplication')
    independence={}
    for other in r.order():
        if other==cid or other in c.quarantined(r):continue
        record=baseline['continuation_independence']['unaffected'][other]
        r.require(record['independent'] is True,'Original independence unresolved')
        # All discovery packets predate all failures; reverified exact hashes prevent leakage.
        p=r.H/'packets/discovery'/f'{other}.txt'
        r.require(cid not in p.read_text() and event['session_id'] not in p.read_text(),'Cross-mapping incident input')
        independence[other]={'independent':True,'frozen_discovery_request_sha256':r.sha(p),
            'evidence':'Original committed dependency/context proof reverified; unchanged pre-event packets; no response exists to propagate; no post-failure launch; all runtime attempts reconcile unique finished reservations and sessions.'}
    event['independence_review']={'status':'VERIFIED','unaffected':independence}
    path=r.H/'review/quarantines'/f'{cid}.json';r.write(path,event);paths.append(path)
    pause=sorted((r.RT/'states').glob('*.json'))[-1]
    dest=r.H/'review'/f'{cid}-{stage}-pause-state.json';r.raw(dest,pause.read_bytes());paths.append(dest)
    r.write(r.H/f'{cid}-{stage}-incident-freeze.json',{'parent_commit':r.head(),'authority':c.AUTHORITY,'files':r.inventory(paths)})
    return event


def resume(r,cid):
    r.verify();r.require(not r.git('status','--porcelain'),'Commit incident and positive independence evidence')
    r.require(r.state()=='PAUSED_AMBIGUOUS','Wrong pause state')
    event=r.read(r.H/'review/quarantines'/f'{cid}.json')
    current=c.inspect_attempt(r,event['stage'],cid)
    r.require(current['classification']=='PROVIDER_NO_OBSERVATION' and event['independence_review']['status']=='VERIFIED','Evidence changed')
    c.verify_evidence(r)
    r.transition('COMPLETE','Authorized independent continuation after '+cid+' local no-observation quarantine; incident and pause preserved; no retry/replacement. Not run completion.')
    p=sorted((r.RT/'states').glob('*.json'))[-1]
    r.raw(r.H/'review'/f'{cid}-resume-state.json',p.read_bytes())
