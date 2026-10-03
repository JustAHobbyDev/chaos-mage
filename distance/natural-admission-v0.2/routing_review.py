"""Preserve a valid but routing-incomplete discovery under the frozen H7 stop."""
import json
import continuation as c
import stages


def review(r, cid):
    r.verify(); baseline=c.verify_evidence(r)
    r.require(r.state()=='COMPLETE','Finish/preserve in-flight batch first')
    d=r.RT/'attempts/discovery'/cid
    v=r.read(d/'validation.json');r.require(r.sha(d/'response.json')==v['response_sha256'],'Response drift')
    inv=stages.obligation_inventory(r.read(r.H/'claims'/f'{cid}.json'),r.read(r.H/'classification'/f'{cid}.json'),r.read(d/'response.json'))
    r.require(not inv['ready_for_evaluation'] and inv['routing_issues'],'No routing issue to quarantine')
    r.transition('PAUSED_RECOVERABLE','Preserve observed discovery routing issue in '+cid+' before next batch; no scientific repair.')
    paths=[]
    for q in d.iterdir():
        dest=r.H/'raw/discovery'/cid/q.name
        if dest.exists():r.require(dest.read_bytes()==q.read_bytes(),'Raw drift')
        else:r.raw(dest,q.read_bytes())
        paths.append(dest)
    dest=r.H/'discovery'/f'{cid}.json'
    r.write(dest,r.read(d/'response.json'));paths.append(dest)
    rows=c.ledger(r)
    attempts=list((r.RT/'attempts').glob('*/*/attempt.json'))
    r.require(len(rows)==len(attempts),'Reservation/attempt mismatch')
    for p in attempts:
        a=r.read(p);match=[x for x in rows if x['session']==a['stage']+'/'+a['packet_id']]
        r.require(len(match)==1 and match[0]['state']=='FINISHED' and json.loads(match[0]['command_json'])==a['command'],'Unresolved scheduler identity')
        r.require(r.sha(p.parent/'request.txt')==a['request_sha256']==r.sha(r.H/'packets'/a['stage']/(a['packet_id']+'.txt')),'Executed request drift')
    sessions=[]
    for p in (r.RT/'attempts').glob('*/*/events.jsonl'):
        es=[json.loads(x) for x in p.read_text().splitlines()]
        ss=[e['thread_id'] for e in es if e.get('type')=='thread.started'];r.require(len(ss)==1,'Session ambiguity');sessions+=ss
    r.require(len(set(sessions))==len(sessions),'Duplicate context')
    independence={}
    for other in r.order():
        if other==cid or other in c.quarantined(r):continue
        p=r.H/'packets/discovery'/f'{other}.txt'
        r.require(cid not in p.read_text() and v['metadata']['session_id'] not in p.read_text(),'Cross-mapping input')
        independence[other]={'independent':True,'request_sha256':r.sha(p),'evidence':'Original committed independence proof and all input hashes reverified; other discovery packets frozen before this observation; source/target/schema/model/reasoning unchanged; fresh distinct ephemeral contexts; no routing result supplied to another packet.'}
    e={'mapping_id':cid,'stage':'discovery','classification':'OBSERVED_ROUTING_UNRESOLVED',
       'provider_response_status':'VALID_DISCOVERY_OBSERVATION','response_sha256':v['response_sha256'],
       'session_id':v['metadata']['session_id'],'routing_issues':inv['routing_issues'],
       'authority':'Existing H7 PROTOCOL.md atomization/obligations and UNMEASURED recovery boundary items 1–3; user continuation handoff.',
       'mapping_disposition':{'instrumentation':'FAILURE','admission':'UNMEASURED','end_to_end_complete':False,'retry':'FORBIDDEN','replacement':'FORBIDDEN'},
       'retry_count':0,'independence_review':{'status':'VERIFIED','unaffected':independence},
       'scientific_rejection':False,'scientific_verdict':None,
       'scheduler':'Two-session batch finished before disposition; second discovery already in flight when first routing issue inspected; no further batch launched; no dependency on first response.'}
    dest=r.H/'review/quarantines'/f'{cid}.json';r.write(dest,e);paths.append(dest)
    pause=sorted((r.RT/'states').glob('*.json'))[-1]
    dest=r.H/'review'/f'{cid}-routing-pause-state.json';r.raw(dest,pause.read_bytes());paths.append(dest)
    r.write(r.H/f'{cid}-routing-incident-freeze.json',{'parent_commit':r.head(),'files':r.inventory(paths)})
    return e


def resume(r,cid):
    r.verify();r.require(not r.git('status','--porcelain'),'Commit isolation evidence')
    r.require(r.state()=='PAUSED_RECOVERABLE','Unexpected state')
    e=r.read(r.H/'review/quarantines'/f'{cid}.json')
    r.require(e['classification']=='OBSERVED_ROUTING_UNRESOLVED' and e['independence_review']['status']=='VERIFIED','Unresolved incident')
    c.verify_evidence(r)
    r.transition('COMPLETE','Authorized independent continuation after '+cid+' observed-routing quarantine; preserved original discovery, no repair/retry. Not run completion.')
    p=sorted((r.RT/'states').glob('*.json'))[-1]
    r.raw(r.H/'review'/f'{cid}-routing-resume-state.json',p.read_bytes())
