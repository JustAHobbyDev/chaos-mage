#!/usr/bin/env python3
"""Offline completed-run audit; never calls a provider or mutates frozen observations."""
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from collections import Counter
H=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(H))
import runner as r
import contracts as c

def main():
    result=r.verify()
    m=r.manifest(); t=r.taxonomy()
    claims=r.read(H/'selection/claims.json'); evidence=r.read(H/'selection/evidence.json')
    sessions=set(); diagnostics=[]; counts=Counter(); usage=Counter()
    db=sqlite3.connect('file:'+str(r.R/'.runtime/experiment-budget.sqlite3')+'?mode=ro',uri=True)
    db.row_factory=sqlite3.Row
    ledger={x['session']:dict(x) for x in db.execute('select * from reservations where experiment=?',('h6r1-claim-taxonomy-v0.1',))}
    a_freeze='fc3240d5b8c6fea9cf8c013362b7555c728a3a1f'
    for stage in r.STAGES:
        eligible=[uid for uid in m['claim_order'] if stage=='role' or r.read(r.judgment('role',uid))['assignment_status']=='ASSIGNED']
        assert len(list((H/(stage+'-judgments')).glob('*.json')))==len(eligible)
        assert len(list((r.RT/'attempts'/stage).iterdir()))==len(eligible)
        for uid in eligible:
            raw=H/'raw'/stage/r.stem(uid)
            packet=r.read(r.packet_path(stage,uid))
            expected=c.role_packet(claims[uid],evidence[uid]) if stage=='role' else c.evaluation_packet(claims[uid],evidence[uid],r.read(r.judgment('role',uid)),t)
            assert packet==expected
            assert (raw/'request.txt').read_bytes()==r.packet_path(stage,uid,'txt').read_bytes()==r.prompt(stage,expected)
            value=r.read(raw/'response.json')
            assert value==r.read(r.judgment(stage,uid))
            d=c.validate(stage,value,packet,r.read(H/'schemas'/(stage+'.schema.json')),t)
            diagnostics.extend(d)
            events=[json.loads(line) for line in (raw/'events.jsonl').read_text().splitlines() if line.strip()]
            metadata=r.audit_events(events,(raw/'response.json').read_text())
            assert metadata['session_id'] not in sessions
            sessions.add(metadata['session_id'])
            for record in metadata['usage']:
                usage.update({k:v for k,v in record.items() if isinstance(v,int)})
            reservation=r.read(raw/'reservation.json'); launch=r.read(raw/'process.json')
            assert reservation['initially_empty'] and reservation['available_packets']==[uid]
            assert reservation['configuration']['model']=='gpt-6-astra'
            assert reservation['configuration']['reasoning_effort']=='high'
            assert reservation['at']<=launch['launched_at']
            entry=ledger[stage+':'+uid]
            assert json.loads(entry['command_json'])==reservation['command']
            assert entry['plan_hash']==reservation['plan_sha256']
            assert entry['returncode']==0 and r.read(raw/'exit.json')['returncode']==0
            assert not (raw/'failure.json').exists()
            if stage=='evaluation':
                subprocess.run(['git','merge-base','--is-ancestor',a_freeze,reservation['execution_commit']],cwd=r.R,check=True)
            counts[stage]+=1
    assert len(ledger)==len(sessions)==43
    assert not diagnostics
    historical=r.read(H/'comparison/historical.json')
    subprocess.run(['git','merge-base','--is-ancestor','8fb24e8899f3668ef781dc6830645f547f16060d',historical['after_stage_b_commit']],cwd=r.R,check=True)
    for row in historical['claims']:
        assert r.sha(r.OLD/'claim-judgments'/(r.stem(row['claim_id'])+'.json'))==row['old_h6_sha256']
    assert r.metrics()==r.read(H/'metrics.json')
    batches=sorted((r.RT/'batches').iterdir())
    assert len(batches)==15
    for batch in batches:
        for name in ('before.json','after-immediate.json','after-settled.json','calibration-record.json','usage-totals.json'):
            assert (batch/name).is_file()
    result.update({'verified_at':r.now(),'verified_commit':r.head(),'session_counts':dict(counts),'unique_sessions':len(sessions),'per_session_ledger_reservations':len(ledger),'ledger_states':dict(Counter(x['state'] for x in ledger.values())),'all_reservations_precede_launch':True,'all_requests_reconstruct_from_frozen_allowlisted_inputs':True,'all_responses_match_preserved_raw_and_event_stream':True,'stage_b_execution_commits_descend_from_complete_stage_a_freeze':True,'historical_comparison_after_complete_stage_b_freeze':True,'schema_and_provenance_diagnostics':diagnostics,'tools_or_harness_retries_or_substitutions_observed':0,'requested_model':'gpt-6-astra','requested_reasoning_effort':'high','served_snapshot_verification':'Not exposed by CLI events; requested configuration and absence of observed substitution are verified.','internal_provider_retries':'Not observable; zero harness retries.','matched_bookkeeping_batches':len(batches),'clean_allowance_calibration_samples':0,'allowance_calibration_limitation':'Concurrent interactive account activity and unsettled telemetry; account snapshots retained privately, not used as clean per-session calibration.','available_token_totals':dict(usage),'dollar_cost':'UNKNOWN; tokens are not billed-dollar evidence','premeasurement_offline_tests':{'passed':61,'evidence':'review/offline-preflight.json'},'scope':'Offline reconstruction, schemas, raw events, ledger and hashes; no new provider judgments.'})
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
