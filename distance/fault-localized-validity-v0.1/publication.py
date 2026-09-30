"""Post-freeze metrics and chronology audit; execute only after both freezes."""
import sys,json
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H));import runner as r;import contracts as c;import continuation as k;import continuation_v2 as v2

def compute():
 r.committed(H/'claim-warrant-freeze.json');r.committed(H/'ablation-freeze.json')
 checks=[k.verify_results(s,True) for s in r.STAGES]
 for check in checks:
  check['retained_representation_failure']=sum(row['original_validation']['status']=='failed' for row in c.read(H/f"{check['stage']}-freeze.json")['runs'])
 atoms=r.claims(); results={a['claim_id']:c.read(H/'judgments/claim-warrant'/f'{a["claim_id"]}.json') for a in atoms}
 metrics={'status':'complete','cases':{},'claim_counts':c.read(H/'manifest.json')['claims_by_case'],'claim_status_distribution':{s:sum(v['status']==s for v in results.values()) for s in c.CLAIM},'unsupported_claims':[],'uncertain_claims':[],'artifact_status_distribution':{},'provider_calls':0,'unique_sessions':0,'harness_retries':0,'replacement_judgments':0,'historical_files_preserved':r.verify()['historical_files_preserved'],'served_model_identifiers':[],'verified_served_snapshot':None,'within_model_stability':None,'cross_model_robustness':None,'premeasurement_recovery':'recovery/premeasurement.json','quote_representation_recovery':'recovery/quote-representation/incident.json','retained_quote_representation_observations':2,'excerpt_representation_recovery':'recovery/excerpt-representation/incident.json'}
 for cid in r.CASES:
  aa=[a for a in atoms if a['case_id']==cid]
  artifact=c.read(H/'judgments/ablation'/f'{cid}.json')['artifact_viability'] if cid in r.order('ablation') else None
  metrics['cases'][cid]={'claims':len(aa),'statuses':{s:sum(results[a['claim_id']]['status']==s for a in aa) for s in c.CLAIM},'artifact_viability':artifact,'no_defect_status':None if artifact else 'not_applicable_no_UNSUPPORTED_claims'}
 for a in atoms:
  v=results[a['claim_id']]
  if v['status'] in ['UNSUPPORTED','UNCERTAIN']:metrics['unsupported_claims' if v['status']=='UNSUPPORTED' else 'uncertain_claims'].append({**a,'judgment':v})
 metrics['artifact_status_distribution']=dict(Counter(v['artifact_viability']['artifact_status'] for v in metrics['cases'].values() if v['artifact_viability']))
 sessions=[];ids=[];usage=Counter();previous=None
 for stage in r.STAGES:
  prepared=H/f'{stage}-prepared.json';preflight=H/'review'/f'{stage}-preflight.json';freeze=H/f'{stage}-freeze.json'
  f=c.read(freeze);p=c.read(preflight)
  c.require(all(x['exit_code']==0 for x in p['checks']),'Unsuccessful preflight')
  c.require(p['prepared_sha256']==c.sha(prepared),'Preflight binding')
  for row in f['runs']:
   x=row['reservation'];v=row['validation'];identity=row['identity'];d=r.RT/'runs'/stage/identity
   r.committed(preflight,x['input_commit']);r.committed(prepared,x['input_commit'])
   if stage=='claim-warrant' and identity not in [a['identity'] for a in c.read(k.REC/'incident.json')['rows']]:
    r.committed(k.REC/'preflight.json',x['input_commit']);c.require(c.read(k.REC/'preflight.json')['at']<=x['at'],'Resume before preflight')
   if stage=='ablation':r.committed(H/'claim-warrant-freeze.json',x['input_commit'])
   c.require(p['at']<=x['at']<=v['finished_at']<=f['at'],'Measurement chronology')
   c.require(previous is None or previous<=x['at'],'Overlapping fresh sessions');previous=v['finished_at']
   a=c.read(d/'attempt.json');c.require(a['harness_attempt']==1,'Retry');ids.append((stage,identity))
   metadata=v['metadata'];sessions.append(metadata['session_id'])
   metrics['served_model_identifiers']+=metadata['returned_model_identifiers']
   for u in metadata['usage']:
    for usage_key,value in (u or {}).items():
     if isinstance(value,int):usage[usage_key]+=value
 c.require(len(sessions)==len(set(sessions)) and len(ids)==len(set(ids)),'Duplicate observation/session')
 attempts=list((r.RT/'runs').glob('*/*/attempt.json'));c.require(len(attempts)==len(ids),'Extra attempts')
 timeline=sorted([c.read(p) for p in (r.RT/'states').glob('*.json')]+[c.read(p) for p in (r.RT/'continuation/states').glob('*.json')],key=lambda x:x['at'])
 for stage,identity in ids:
  launched=c.read(r.RT/'runs'/stage/identity/'process.json')['launched_at']
  c.require([x for x in timeline if x['at']<=launched][-1]['state']=='RUNNING','Launch during pause or terminal state')
 for rec in [k.REC,v2.REC]:
  p=c.read(rec/'preflight.json');c.require(p['prepared_sha256']==c.sha(rec/'prepared.json'),'Recovery preflight binding')
 v2.gate()
 metrics.update(provider_calls=len(ids),unique_sessions=len(sessions),served_model_identifiers=sorted(set(metrics['served_model_identifiers'])),usage=dict(usage))
 return metrics,checks
def verify():
 with v2.context(): metrics,checks=compute()
 c.require(metrics==c.read(H/'metrics.json'),'Metrics drift')
 if (H/'final-runtime-freeze.json').exists():
  f=c.read(H/'final-runtime-freeze.json');r.hashes(f['files']);c.require(f['files']==r.inventory(r.RT.rglob('*')),'Execution after final freeze')
 return {'status':'complete','provider_calls':metrics['provider_calls'],'unique_sessions':metrics['unique_sessions'],'recovered_response_representations':metrics['retained_quote_representation_observations'],'checks':checks,'historical_files_preserved':metrics['historical_files_preserved'],'no_launch_during_pause':True}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('action',choices=['write','verify']);a=p.parse_args()
 if a.action=='verify':print(json.dumps(verify(),indent=2))
 else:
  with v2.context(): metrics,checks=compute()
  r.write(H/'metrics.json',metrics);r.write(H/'review/result-verification.json',{'at':r.now(),'checks':checks,'chronology_verified':True,'metrics_reconstructed':True,'summary_correction':'The v1 verification helper summary counted only its own recovered observation; this additive verification recomputes both original failed validations directly from frozen runs. No measurement or acceptance decision uses that summary field.'})
  print(json.dumps({key:value for key,value in metrics.items() if key not in ['cases','unsupported_claims','uncertain_claims']},indent=2))
