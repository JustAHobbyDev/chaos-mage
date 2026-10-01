"""Post-freeze H audit and publication. Never a provider input."""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
import contracts as c
import runner as r
import continuation as k
H=r.H
CATEGORIES=['STRUCTURALLY_CONCORDANT','PLAUSIBLE_ALTERNATIVE','CASE_DESIGN_PROBLEM','JUDGE_DEPENDENCY_ERROR','AMBIGUOUS']

def compute():
 for stage in r.STAGES:r.committed(H/f'{stage}-freeze.json')
 import resume
 resume.original_completion()
 recovery=c.read(H/'recovery/daemon-restart/preflight.json')
 c.require(all(x['exit_code']==0 for x in recovery['checks']),'Failed restart preflight')
 with k.context():
  checks=[r.verify_results(stage,True) for stage in r.STAGES]
  r.verify()
 manifest=c.read(H/'manifest.json');atoms=r.claims()
 c.require({p.stem for p in (H/'cases').glob('*.json')}==set(manifest['case_order']),'Extra/missing case files')
 graphs=c.read(H/'review/reconstructed-dependencies.json')
 c.require(set(graphs)==set(manifest['case_order']),'Reconstructed graph coverage')
 for cid,graph in graphs.items():
  nodes={node['id'] for node in graph['nodes']}
  c.require(len(nodes)==len(graph['nodes']),'Duplicate graph node')
  for node in graph['nodes']:
   c.cited_spans([{'source_field':node['source_field'],'exact_text':node['exact_text']}],r.candidate(cid))
  c.require(all(edge['from'] in nodes and edge['to'] in nodes for edge in graph['edges']),'Unanchored graph edge')
 judgments={a['claim_id']:c.read(H/'judgments/claim-warrant'/f'{a["claim_id"]}.json') for a in atoms}
 reviews=c.read(H/'review/operator-audit.json')
 c.require(set(reviews)==set(manifest['case_order']),'Review coverage')
 rows=[];sessions=[];usage=Counter();returned=set();previous=None
 for stage in r.STAGES:
  preflight=H/'recovery/premeasurement/claim-warrant-preflight.json' if stage=='claim-warrant' else H/'review/ablation-preflight.json'
  p=c.read(preflight);c.require(all(x['exit_code']==0 for x in p['checks']),'Failed effective preflight')
  f=c.read(H/f'{stage}-freeze.json')
  for entry in f['runs']:
   reserve=entry['reservation'];validation=entry['validation'];identity=entry['identity']
   r.committed(preflight,reserve['input_commit'])
   r.committed(H/f'{stage}-prepared.json',reserve['input_commit'])
   if stage=='ablation':
    r.committed(H/'claim-warrant-freeze.json',reserve['input_commit'])
    if identity in c.read(H/'recovery/daemon-restart/incident.json')['remaining_unreserved']:
     r.committed(H/'recovery/daemon-restart/preflight.json',reserve['input_commit'])
     c.require(recovery['at']<=reserve['at'],'Resume before preflight')
   c.require(p['at']<=reserve['at']<=validation['finished_at']<=f['at'],'Freeze chronology')
   c.require(previous is None or previous<=reserve['at'],'Session overlap');previous=validation['finished_at']
   sessions.append(validation['metadata']['session_id']);returned.update(validation['metadata']['returned_model_identifiers'])
   for item in validation['metadata']['usage']:
    for key,value in (item or {}).items():
     if isinstance(value,int):usage[key]+=value
 c.require(len(sessions)==len(set(sessions)),'Repeated sessions')
 c.require(len(list((r.RT/'runs').glob('*/*/attempt.json')))==len(sessions),'Extra attempts')
 timeline=[c.read(p) for p in sorted((r.RT/'states').glob('*.json'))]
 for p in (r.RT/'runs').glob('*/*/process.json'):
  process=c.read(p);c.require([s for s in timeline if s['at']<=process['launched_at']][-1]['state']=='RUNNING','Launch while stopped')
 for cid in manifest['case_order']:
  design=c.read(H/'hidden-design'/f'{cid}.json');case=r.candidate(cid)
  case_atoms=[a for a in atoms if a['case_id']==cid];unsupported=[a for a in case_atoms if judgments[a['claim_id']]['status']=='UNSUPPORTED']
  artifact=c.read(H/'judgments/ablation'/f'{cid}.json')['artifact_viability'] if unsupported else None
  review=reviews[cid];c.require(review['category'] in CATEGORIES,'Unknown review category')
  c.require(set(review['checks'])=={'intended_claim_unsupported','hidden_graph_omitted_survivor','judge_invented_dependency','judge_overlooked_dependency','operations_only_retention','strongest_citation_survives'},'Missing six review checks')
  c.require(bool(review['rationale']) and all(x['rationale'] for x in review['checks'].values()),'Missing review evidence')
  intended=[x['claim_id'] for x in c.read(H/'claims/hidden-design-links.json') if x['case_id']==cid]
  proof=c.cited_spans(artifact['strongest_surviving_target_inference']['source_spans'],case,unsupported,surviving=True,mapping_only=True) if artifact else []
  total=sum(len(x) for x in case['mapping'].values());deleted=sum(a['span_end']-a['span_start'] for a in unsupported)
  rows.append({'case_id':cid,'mechanism':design['mechanism'],'intended_position':design['intended_structural_position'],'is_control':design['is_control'],'control_number':design['control_number'],'claims':len(case_atoms),'claim_statuses':{s:sum(judgments[a['claim_id']]['status']==s for a in case_atoms) for s in c.CLAIM},'intended_claim_measurements':{identity:judgments[identity]['status'] for identity in intended},'unsupported_ids':[a['claim_id'] for a in unsupported],'deleted_characters':deleted,'original_mapping_characters':total,'deleted_fraction':deleted/total,'artifact':artifact,'no_defect_outcome':None if artifact else 'not_applicable_no_UNSUPPORTED_claims','review':review,'strongest_source_proof':proof})
 distributions={name:dict(Counter(row['artifact'][name]['status'] for row in rows if row['artifact'])) for name in ['mechanism_survival','target_contribution_survival','dependency_cascade','remainder_check']}
 distributions['artifact_status']=dict(Counter(row['artifact']['artifact_status'] for row in rows if row['artifact']))
 for name,values in [('mechanism_survival',c.MECHANISM),('target_contribution_survival',c.TARGET),('dependency_cascade',c.CASCADE),('remainder_check',c.REMAINDER),('artifact_status',c.ARTIFACT)]:
  distributions[name]={value:distributions[name].get(value,0) for value in values}
 by_position={p:dict(Counter(row['artifact']['artifact_status'] if row['artifact'] else 'NOT_APPLICABLE' for row in rows if not row['is_control'] and row['intended_position']==p)) for p in ['local','scope','core']}
 by_mechanism={m:dict(Counter(row['artifact']['artifact_status'] if row['artifact'] else 'NOT_APPLICABLE' for row in rows if not row['is_control'] and row['mechanism']==m)) for m in sorted({row['mechanism'] for row in rows})}
 return {'status':'complete','cases':rows,'claim_count':len(atoms),'claim_warrant_distribution':{status:sum(v['status']==status for v in judgments.values()) for status in c.CLAIM},'distributions':distributions,'primary_by_position':by_position,'primary_by_mechanism':by_mechanism,'review_categories':{category:sum(row['review']['category']==category for row in rows) for category in CATEGORIES},'provider_calls':len(sessions),'unique_sessions':len(set(sessions)),'harness_retries':0,'replacement_judgments':0,'verified_served_snapshot':None,'returned_model_identifiers':sorted(returned),'usage':dict(usage),'historical_tracked_files':len(c.read(H/'preservation.json')['files']),'historical_runtime_files':len(c.read(H/'preservation.json')['historical_runtime']),'checks':checks,'no_launch_while_paused':True,'operator_review_is_independent_rater_evidence':False,'recovered_bookkeeping_observations':1,'unavailable_process_exit_codes':1,'recovery_preflight_checks':len(recovery['checks']),'runtime_files':r.inventory(r.RT.rglob('*'))}

def verify():
 result=compute();c.require(result==c.read(H/'metrics.json'),'Metrics drift')
 frozen=c.read(H/'final-runtime-freeze.json');r.hashes(frozen['files'])
 c.require(frozen['files']==r.inventory(r.RT.rglob('*')),'Execution after final freeze')
 return {k:result[k] for k in ['status','claim_count','provider_calls','unique_sessions','historical_tracked_files','historical_runtime_files','distributions','review_categories']}

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['write','verify']);a=p.parse_args()
 if a.action=='write':
  result=compute();r.write(H/'metrics.json',result);r.write(H/'final-runtime-freeze.json',{'at':r.now(),'files':r.inventory(r.RT.rglob('*'))});print(json.dumps({'cases':len(result['cases']),'calls':result['provider_calls']}))
 else:print(json.dumps(verify(),indent=2))
if __name__=='__main__':main()
