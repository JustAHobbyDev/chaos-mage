"""Offline terminal-run evidence audit; launches no provider sessions."""
from pathlib import Path
import json,sqlite3,sys
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H))
import runner as r
import recovery as x


def verify():
    result=r.verify();r.binary_check();x.proof()
    sessions=[];stage_counts={};executions=[];diagnostics=[]
    previous_freeze=None
    for stage in r.STAGES:
        if stage=='evaluation':
            frozen=r.read(H/'evaluation-partial-freeze.json');r.hashes(frozen['files'],True)
            keys=frozen['completed_items']
            r.c.require(not r.frozen_path('evaluation').exists(),'Incomplete stage mislabeled complete')
        else:
            frozen=r.require_freeze(stage);keys=r.ids(stage)
            r.c.require(frozen['claim_ids']==keys,'Freeze roster mismatch')
        stage_counts[stage]=len(keys)
        paths=list((H/(stage+'-judgments')).glob('*.json'))
        r.c.require({p.stem for p in paths}==set(keys),'Unexpected/missing observations')
        for uid in keys:
            source=r.RT/'attempts'/stage/uid
            sessions.append(r.verify_attempt(stage,uid,source))
            reservation=r.read(source/'reservation.json');execution=reservation['execution_commit']
            if previous_freeze:
                r.c.require(r.git('merge-base',previous_freeze,execution)==previous_freeze,'Cross-stage freeze violation')
            value=r.read(r.judgment(stage,uid));packet=r.read(r.packet_path(stage,uid))
            r.c.require(value==r.read(source/'response.json'),'Changed observation')
            r.c.require(packet==r.build_packet(stage,uid),'Packet reconstruction mismatch')
            r.c.require(r.prompt(stage,packet)==r.packet_path(stage,uid,'txt').read_bytes(),'Prompt reconstruction mismatch')
            for p in (H/'raw'/stage/uid).iterdir():
                r.c.require(p.read_bytes()==(source/p.name).read_bytes(),'Published raw evidence mismatch')
            diagnostics.extend(x.validate(stage,value,packet,r.read(H/'schemas'/(stage+'.schema.json')),r.taxonomy()))
            executions.append({'stage':stage,'item':uid,'execution_commit':execution,'response_sha256':r.sha(source/'response.json')})
        if stage!='evaluation':
            previous_freeze=r.git('log','--diff-filter=A','--format=%H','--',r.rel(r.frozen_path(stage))).splitlines()[0]
    r.c.require(len(sessions)==len(set(sessions))==47,'Session count/reuse failure')
    with sqlite3.connect('file:'+str(r.budget.DEFAULT_LEDGER)+'?mode=ro',uri=True) as db:
        rows=db.execute('SELECT session,stage,returncode FROM reservations WHERE experiment=?',(r.manifest()['experiment_id'],)).fetchall()
    r.c.require(len(rows)==47 and all(row[2]==0 for row in rows),'Ledger count/completion mismatch')
    r.c.require({(stage,p.stem) for stage in r.STAGES for p in (H/(stage+'-judgments')).glob('*.json')}==
                {(stage,session.split(':',1)[1]) for session,stage,code in rows},'Reservation roster mismatch')
    evaluations={(v['claim_id'],v['obligation_id']):v for v in
                [r.read(p) for p in sorted((H/'evaluation-judgments').glob('*.json'))]}
    aggregate=r.c.aggregate(r.assignments(),r.discoveries(),evaluations,r.taxonomy())
    r.c.require(aggregate==r.read(H/'review/partial-aggregation.json')['results'],'Aggregation replay mismatch')
    r.c.require(sum(cid=='K09-C1' for cid,oid in evaluations)==1,'P3 premise was not evaluated exactly once')
    batches=sorted((r.RT/'batches').glob('*'))
    for b in batches:
        record=r.read(b/'batch.json');before=r.read(b/'before.json');cal=r.read(b/'calibration-record.json')
        r.c.require(len(record['claim_ids'])<=3,'Batch exceeded bound')
        r.c.require(before==r.read(Path(record['preflight'])/'before.json'),'Batch snapshot mismatch')
        r.c.require(cal['before']==before,'Calibration snapshot mismatch')
        r.c.require((b/'after-immediate.json').exists() and (b/'after-settled.json').exists(),'Missing after snapshots')
    r.c.require(r.latest_state()['state']=='TERMINATED_LINEAGE','Terminal status lost')
    missing=[uid for uid in r.ids('evaluation') if not r.judgment('evaluation',uid).exists()]
    r.c.require(len(missing)==6 and all(not (r.RT/'attempts/evaluation'/uid).exists() for uid in missing),'Unmeasured request launched')
    r.c.require(r.budget.Gate().status(r.check_plan(),r.read(r.budget.DEFAULT_POLICY))['allowed'] is False,'Terminal budget block missing')
    return {**result,'status':'PASS_PRESERVATION_ONLY','scientific_status':'TERMINATED_LINEAGE','calibration_complete':False,'unmeasured_evaluations':missing,'stage_counts':stage_counts,'unique_provider_sessions':len(sessions),
        'ledger_reservations':len(rows),'bounded_batches':len(batches),'all_raw_responses_preserved':True,
        'all_requests_reconstructed':True,'all_stage_barriers_verified':True,'as_run_partial_aggregation_replayed':True,
        'p3_premise_provider_judgments':1,'engineering_recoveries':1,'provider_incidents':0,
        'harness_retries':0,'substitutions_observed':0,'verified_served_snapshot':None,
        'diagnostics':diagnostics,'executions':executions}


if __name__=='__main__':
    result=verify();r.write(H/'review/final-verification.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('executions','diagnostics')},indent=2))
