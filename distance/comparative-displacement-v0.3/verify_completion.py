"""Read-only completion, provenance, review and historical preservation checks."""
import argparse
from datetime import datetime
import runner as r
import metrics
def execution_audit():
 sessions=[];out={};probe=r.read(r.HERE/'preflight.json')
 for x in probe['entries']:sessions.append(x['audit']['metadata']['session_id'])
 previous=datetime.fromisoformat(probe['frozen_at'])
 for stage in ('validity','comparison'):
  freeze=r.frozen(stage,True);returned={f:set() for f in 'AB'};retries={f:0 for f in 'AB'};by={}
  for x in freeze['runs']:
   res=x['reservation'];audit=x['audit'];meta=audit['metadata'];sessions.append(meta['session_id'])
   start=datetime.fromisoformat(res['started_at']);finish=datetime.fromisoformat(audit['finished_at'])
   r.require(previous<=start<=finish,'Execution chronology mismatch');previous=finish
   r.require(res['configuration']==r.config(),'Configuration changed');r.require(res['cli_version']==r.config()['expected_cli_versions'][x['family']],'CLI drift')
   by[(x['case_id'],x['family'])]=res['packet_sha256'];returned[x['family']].update(meta['returned_model_identifiers']);retries[x['family']]+=meta['formatting_retries']['observed_formatting_retries']
  for cid in {k[0] for k in by}:r.require(by[(cid,'A')]==by[(cid,'B')],'Different family packets')
  r.require(previous<=datetime.fromisoformat(freeze['at']),'Freeze before completion')
  out[stage]={'judgments':len(freeze['runs']),'first_started_at':freeze['runs'][0]['reservation']['started_at'],'last_finished_at':freeze['runs'][-1]['audit']['finished_at'],'returned_identifiers':{f:sorted(returned[f]) for f in 'AB'},'exposed_formatter_retries':retries,'served_snapshots':{'A':None,'B':None}}
  previous=datetime.fromisoformat(freeze['at'])
 r.require(len(sessions)==len(set(sessions)),'Reused session across stages/probes')
 prep=r.checkpoint('prepared.json');admit=r.checkpoint('admission-freeze.json');probes=r.checkpoint('preflight.json');result=r.checkpoint('comparison-freeze.json')
 for old,new in ((prep,probes),(probes,admit),(admit,result)):
  r.require(old!=new and r.subprocess.run(['git','merge-base','--is-ancestor',old,new],cwd=r.ROOT).returncode==0,'Checkpoint ancestry mismatch')
 r.require(datetime.fromisoformat(r.read(r.HERE/'prepared.json')['created_at'])<datetime.fromisoformat(probe['frozen_at']),'Probe before preparation')
 r.require(datetime.fromisoformat(r.read(r.HERE/'validity-freeze.json')['at'])<=datetime.fromisoformat(r.read(r.HERE/'admission.json')['at'])<datetime.fromisoformat(out['comparison']['first_started_at']),'Admission chronology mismatch')
 out.update(unique_sessions_including_probes=len(sessions),identical_family_packets=True,preparation_commit=prep,probe_commit=probes,admission_commit=admit,result_freeze_commit=result)
 return out
def historical_join():
 # This function is only callable after the comparative result freeze exists.
 r.frozen('comparison',True);values=r.published('comparison');rows={x['mapping_id']:x for x in r.manifest()};out=[]
 for p in r.pair_records():
  if p['cohort']!='primary' or any(rows[p[k]]['new'] for k in ('mapping_1','mapping_2')):continue
  labels={f:{k:r.read(r.PRIOR/'judgments/displacement'/f'displacement-{rows[p[k]]["historical_case_id"]}-{f}.json')['class'] for k in ('mapping_1','mapping_2')} for f in 'AB'}
  out.append({'case_id':p['case_id'],'target_id':p['target_id'],'historical_mapping_ids':{k:rows[p[k]]['historical_case_id'] for k in ('mapping_1','mapping_2')},'historical_classes':labels,'comparative_relations':{f:r.c.normalize_relation(values[(p['case_id'],f)]['overall_relation'],p) for f in 'AB'}})
 return out
def verify(private=False):
 result=r.verify_results(private)
 report=r.ROOT/'distance/review/comparative-displacement-v0.3.md';r.require(report.exists(),'Missing report')
 if result['status']!='complete':
  r.require('incomplete' in report.read_text().lower(),'Incomplete report required');return result
 audit=execution_audit();r.require(r.read(r.HERE/'review/execution-audit.json')==audit,'Audit changed')
 r.require(r.read(r.HERE/'review/historical-comparison.json')==historical_join(),'Historical comparison changed')
 reviews=r.read(r.HERE/'review/case-reviews.json');pairs={p['case_id']:p for p in r.pair_records() if p['cohort']=='primary'};values=r.published('comparison')
 r.require(len(reviews)==len(pairs) and {x['case_id'] for x in reviews}==set(pairs),'Review coverage mismatch')
 for row in reviews:
  p=pairs[row['case_id']];v={f:metrics.normalized(values[(p['case_id'],f)],p) for f in 'AB'}
  r.require(row['relations']=={f:v[f]['overall'] for f in 'AB'},'Review changed original relations')
  r.require(type(row['compatible_decisive_reasoning']) is bool,'Compatibility must be explicit')
  r.require(row['status']==metrics.post_status(v['A'],v['B'],row['compatible_decisive_reasoning']),'Review precedence changed')
  for key in ('decisive_reasoning','local_global','shortcut_audit','evidence_context','interpretation'):r.require(isinstance(row[key],str) and bool(row[key].strip()),'Missing review '+key)
 r.require(r.read(r.HERE/'review/result-binding.json')['comparison_freeze_sha256']==r.c.sha(r.HERE/'comparison-freeze.json'),'Review not bound to freeze')
 r.require(datetime.fromisoformat(r.read(r.HERE/'review/result-binding.json')['review_started_at'])>datetime.fromisoformat(r.read(r.HERE/'comparison-freeze.json')['at']),'Review started before freeze')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--private',action='store_true');a=p.parse_args();print(verify(a.private))
