"""Recompute B metrics and verify review coverage plus immutable historical artifacts."""
import argparse
import runner as r
import metrics

def verify(private=False):
 result=r.verify_results(private)
 report=r.ROOT/'distance/review/displacement-calibration-v0.3.md'
 r.require(report.exists(),'Missing publication report')
 if result['status']=='stopped':
  r.require('incomplete' in report.read_text().lower(),'Failure report must identify incompleteness')
  return result
 values=r.published('displacement') if r.order('displacement') else {}
 review=r.read(r.HERE/'review/case-reviews.json')
 admitted={x['case_id'] for x in r.read(r.HERE/'admission.json')['cases'] if x['cohort']!='holdout'} if r.order('displacement') else set()
 r.require(len(review)==len(admitted) and {x['case_id'] for x in review}==admitted,'Every admitted pair needs review')
 for x in review:
  a,b=(values[(x['case_id'],f)] for f in ('A','B'))
  r.require(x['original_classes']=={'A':a['class'],'B':b['class']},'Review changed class labels')
  r.require(x['post_result_status']==metrics.post_result_status(a,b),'Wrong status precedence')
  for k in ('epistemic_change','baseline_stability','shortcut_audit','interpretation'):r.require(bool(x[k].strip()),f'Missing review {k}')
 r.require(r.read(r.HERE/'metrics.json')==metrics.calculate(values,r.manifest(),r.read(r.HERE/'admission.json')['cases']),'Published metrics differ')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--private',action='store_true');a=p.parse_args();print(verify(a.private))
