"""Read-only provenance, execution, analysis and review verification."""
import argparse
from datetime import datetime
import runner as r
import metrics

def execution_audit():
    probe=r.read(r.HERE/'preflight.json');sessions=[];result={};previous=datetime.fromisoformat(probe['frozen_at'])
    for entry in probe['entries']:sessions.append(entry['audit']['metadata']['session_id'])
    for stage in r.STAGES:
        freeze=r.frozen(stage,True);returned={f:set() for f in 'AB'};retries={f:0 for f in 'AB'};packets={};commits=set()
        for run in freeze['runs']:
            reservation,audit=run['reservation'],run['audit'];meta=audit['metadata'];sessions.append(meta['session_id'])
            start=datetime.fromisoformat(reservation['started_at']);finish=datetime.fromisoformat(audit['finished_at'])
            r.require(previous<=start<=finish,'Overlapping or reversed execution');previous=finish
            r.require(reservation['configuration']==r.config(),'Configuration drift')
            r.require(reservation['cli_version']==r.config()['expected_cli_versions'][run['family']],'CLI drift')
            packets[(run['case_id'],run['family'])]=reservation['packet_sha256'];commits.add(reservation['prepared_commit'])
            returned[run['family']].update(meta['returned_model_identifiers']);retries[run['family']]+=meta['formatting_retries']['observed_formatting_retries']
        r.require(len(commits)==1,'Stage ran across multiple commits')
        for cid in {k[0] for k in packets}:r.require(packets[(cid,'A')]==packets[(cid,'B')],'Different family packets')
        r.require(previous<=datetime.fromisoformat(freeze['at']),'Freeze before completion');previous=datetime.fromisoformat(freeze['at'])
        result[stage]={'judgments':len(freeze['runs']),'first_started_at':freeze['runs'][0]['reservation']['started_at'],
          'last_finished_at':freeze['runs'][-1]['audit']['finished_at'],'execution_commit':next(iter(commits)),
          'returned_identifiers':{f:sorted(returned[f]) for f in 'AB'},'exposed_formatter_retries':retries,'served_snapshots':{'A':None,'B':None}}
    r.require(len(sessions)==len(set(sessions)),'Reused session across stages/probes')
    paths={'worlds':'worlds-freeze.json','prepared':'prepared.json','preflight':'preflight.json','admission':'admission-freeze.json','prospective':'prospective-freeze.json','consequence':'consequence-freeze.json'}
    checkpoints={key:r.check_commit(path,r.TITLES[key]) for key,path in paths.items()};chain=list(checkpoints.values())
    for old,new in zip(chain,chain[1:]):r.require(old!=new and r.git('merge-base',old,new).decode().strip()==old,'Checkpoint ancestry')
    r.require(result['validity']['execution_commit']==checkpoints['preflight'],'Validity checkpoint mismatch')
    r.require(result['prospective']['execution_commit']==checkpoints['admission'],'Prospective checkpoint mismatch')
    r.require(result['consequence']['execution_commit']==checkpoints['prospective'],'Consequence checkpoint mismatch')
    r.require(datetime.fromisoformat(r.read(r.HERE/'prepared.json')['created_at'])<datetime.fromisoformat(probe['frozen_at']),'Preparation chronology')
    r.require(datetime.fromisoformat(r.read(r.HERE/'validity-freeze.json')['at'])<=datetime.fromisoformat(r.read(r.HERE/'admission.json')['at'])<datetime.fromisoformat(result['prospective']['first_started_at']),'Admission chronology')
    r.require(datetime.fromisoformat(r.read(r.HERE/'prospective-freeze.json')['at'])<datetime.fromisoformat(result['consequence']['first_started_at']),'Stage B began before Stage A freeze')
    result.update(checkpoints=checkpoints,unique_sessions_including_probes=len(sessions),identical_family_packets=True)
    return result

def verify(private=False):
    result=r.verify_results(private);report=r.ROOT/'distance/review/common-evidence-displacement-v0.3.md';r.require(report.exists(),'Missing report')
    if result['status']!='complete':
        r.require('incomplete' in report.read_text().lower(),'Incomplete report required');return result
    r.require(r.read(r.HERE/'review/execution-audit.json')==execution_audit(),'Execution audit changed')
    binding=r.read(r.HERE/'review/result-binding.json')
    for stage in ('prospective','consequence'):r.require(binding[stage+'_freeze_sha256']==r.c.sha(r.HERE/f'{stage}-freeze.json'),'Review freeze binding')
    r.require(datetime.fromisoformat(binding['review_started_at'])>datetime.fromisoformat(r.read(r.HERE/'consequence-freeze.json')['at']),'Review before final result freeze')
    pairs={p['case_id']:p for p in r.pair_records() if p['cohort']=='primary'}
    reviews=r.read(r.HERE/'review/case-reviews.json');r.require(len(reviews)==len(pairs) and {x['case_id'] for x in reviews}==set(pairs),'Incomplete case review')
    values={s:r.published(s) for s in ('prospective','consequence')}
    for row in reviews:
        p=pairs[row['case_id']]
        for stage in values:
            expected={f:metrics.normalized(values[stage][(p['case_id'],f)],p)['overall'] for f in 'AB'}
            r.require(row['relations'][stage]==expected,'Review changed original relation')
        for key in ('decisive_reasoning','evidence_context','local_depth_propagation_reach','opponent_consistency','outcome_rigging','stage_transition','interpretation'):
            r.require(isinstance(row[key],str) and bool(row[key].strip()),'Missing case review: '+key)
    audits=r.read(r.HERE/'review/outcome-audit.json')
    r.require(len(audits)==len(pairs) and {x['case_id'] for x in audits}==set(pairs),'Incomplete outcome audit')
    required=('authored_signal_asymmetry','unjustified_decisiveness','hidden_assumptions','world_fact_favoritism','resource_use','world_consistency')
    for row in audits:
        for key in required:r.require(isinstance(row[key],str) and bool(row[key].strip()),'Missing outcome concern')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--private',action='store_true');a=p.parse_args();print(verify(a.private))
