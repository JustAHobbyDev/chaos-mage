"""Publish only the incomplete design-stage outcome; no invented model results."""
import argparse,json
from pathlib import Path
import runner as r
import contracts as c

def compute():
 checks=r.verify();audit=c.read(r.H/'review/authoring-audit.json')
 return {'status':checks['status'],'experiment_complete':False,'measurement_started':False,'base_sha':r.BASE,'base_branch':'experiment-h-calibration','branch':'experiment-h1-calibration','policy_checkpoint':r.POLICY,'planned_cases':16,'final_cases':0,'authored_drafts':36,'draft_revisions':3,'planned_primary_cases':12,'planned_controls':4,'claim_judgment_count':0,'artifact_judgment_count':0,'provider_calls':0,'claim_status_counts':{s:0 for s in c.CLAIM},'artifact_status_counts':{s:0 for s in c.ARTIFACT},'mechanism_survival_counts':{s:0 for s in c.MECHANISM},'target_contribution_counts':{s:0 for s in c.TARGET},'cascade_counts':{s:0 for s in c.CASCADE},'remainder_counts':{s:0 for s in c.REMAINDER},'distribution_interpretation':'No observations. Zero counts are not negative scientific findings.','primary_outcomes':{p:'NOT_MEASURED' for p in ['local','scope','core']},'controls':{key:{'hypothesis':hypothesis,'status':'NOT_AUTHORED_NOT_MEASURED'} for key,hypothesis in [('A','mechanism_death'),('B','generic_remainder'),('C','mechanism_uncertainty'),('D','target_uncertainty')]},'operator_review_categories':None,'judge_dependency_errors':None,'premeasurement_core_design_rejections':{'across_attempts':12,'latest_revision':4},'strongest_surviving_inference_audit':'Twelve operator deletion audits validate unchanged signal citations; not provider strongest-inference judgments.','revised_triple_checks':[g for g in checks['triple_checks'] if g['revision']=='conditional_reporting_only'],'historical_preservation':checks['historical_preservation'],'scoring_hashes':c.read(r.H/'instrument-reuse.json')['files'],'core_invalid_sensitivity':'NOT_TESTED','confidence_effect':'No new provider evidence; this construction failed the authoring gate. Policy confidence is not updated from model outcomes.','recommendation':'Resolve feasibility with one genuinely load-bearing same-focal triple before any provider measurement. If that requires changing invariants, obtain an explicitly revised protocol. Do not execute this recommendation here.','operator_audit_is_independent_rater_evidence':False,'audit_decision':audit['decision']}

def verify():
 data=compute();c.require(c.read(r.H/'metrics.json')==data,'Metrics drift')
 manifest=c.read(r.H/'manifest.json');c.require(manifest['status']==data['status'] and manifest['measurement_started'] is False,'Status drift')
 for name,digest in manifest['files'].items():c.require(c.sha(r.R/name)==digest,'Preserved authoring evidence changed: '+name)
 c.require(manifest['policy_checkpoint']==r.POLICY,'Policy checkpoint drift')
 history=c.read(r.H/'review/historical-verification.json');c.require(len(history['checks'])==44 and all(x['exit_code']==0 for x in history['checks']),'Historical verification incomplete')
 c.require(history['preservation']==data['historical_preservation'],'Historical counts drift')
 return {'status':data['status'],'experiment_complete':False,'provider_calls':0,'historical_checks':len(history['checks']),'historical_preservation':data['historical_preservation'],'authoring_evidence_files':len(manifest['files'])}

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['write','verify']);a=p.parse_args()
 if a.action=='write':
  with (r.H/'metrics.json').open('x') as f:json.dump(compute(),f,indent=2,ensure_ascii=False);f.write('\n')
 else:print(json.dumps(verify(),indent=2))
if __name__=='__main__':main()
