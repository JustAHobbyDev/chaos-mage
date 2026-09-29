"""Read-only completion: frozen results, independent counts, all-case review and bindings."""
import argparse
from collections import Counter
from datetime import datetime
import runner as r

def verify(private=False):
 result=r.verify_results(private);report=r.ROOT/'distance/review/anti-collapse-benchmark-v0.1.md';r.require(report.exists(),'Missing report')
 if result['status']!='complete':
  r.require(result['status'].lower() in report.read_text().lower(),'Incomplete/coverage status missing from report');return result
 binding=r.read(r.HERE/'review/result-binding.json')
 r.require(binding['result_freeze_sha256']==r.c.sha(r.HERE/'anti-collapse-freeze.json'),'Review result binding')
 r.require(datetime.fromisoformat(binding['review_started_at'])>datetime.fromisoformat(r.read(r.HERE/'anti-collapse-freeze.json')['at']),'Review before result freeze')
 values=r.published('anti-collapse');ids={cid for cid,_ in values};reviews=r.read(r.HERE/'review/case-reviews.json')
 r.require(len(reviews)==len(ids) and {x['case_id'] for x in reviews}==ids,'Missing/duplicate case reviews')
 for row in reviews:
  r.require(row['statuses']=={f:values[(row['case_id'],f)]['anti_collapse']['status'] for f in 'AB'},'Review changed judgment')
  for key in ('operational_distinction','baseline_reading','formalization_and_reduction','single_rule_or_coordination','suppression_or_retention','interpretation'):
   r.require(isinstance(row[key],str) and bool(row[key].strip()),'Missing review: '+key)
 m=r.read(r.HERE/'metrics.json')
 # Independent count path, separate from metrics.compute.
 for f in 'AB':
  counts=Counter(v['anti_collapse']['status'] for (cid,family),v in values.items() if family==f)
  r.require(m['status_distributions'][f]=={s:counts[s] for s in r.c.STATUSES},'Independent distributions mismatch')
 r.require(m['status_agreement']['numerator']==sum(values[(cid,'A')]['anti_collapse']['status']==values[(cid,'B')]['anti_collapse']['status'] for cid in ids),'Independent agreement mismatch')
 design={x['case_id']:x for x in r.manifest()}
 expected={cid for cid in ids if design[cid]['ladder_level'] in 'CD' and any(values[(cid,f)]['anti_collapse']['status']=='CLEAR_COLLAPSE' for f in 'AB')}
 r.require({x['case_id'] for x in m['CD_design_suppression_cases']}==expected,'Suppression inventory incomplete')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--private',action='store_true');a=p.parse_args();print(verify(a.private))
