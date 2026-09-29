"""Read-only public/private completion and independent review coverage checks."""
import argparse
from collections import Counter
from datetime import datetime
import runner as r


def verify(private=False):
    result=r.verify_results(private)
    report=r.ROOT/'distance/review/anti-collapse-natural-v0.1.md'
    r.require(report.exists(),'Missing report')
    if result['status']=='incomplete':
        r.require('incomplete' in report.read_text().lower(),'Missing incomplete status');return result
    rows=r.read(r.HERE/'review/case-reviews.json')
    r.require(len(rows)==30 and {x['case_id'] for x in rows}=={x['case_id'] for x in r.manifest()},'Missing/duplicate case review')
    for row in rows:
        for field in ('operational_summary','neutralization_review','validity_review','interpretation'):
            r.require(isinstance(row.get(field),str) and row[field].strip(),'Missing substantive review field: '+field)
        r.require(isinstance(row.get('labels'),list),'Missing descriptive labels')
    if result['status']=='complete':
        values=r.published('anti-collapse');ids={cid for cid,_ in values};metrics=r.read(r.HERE/'metrics.json');review={x['case_id']:x for x in rows}
        for family in 'AB':
            counts=Counter(v['anti_collapse']['status'] for (cid,f),v in values.items() if f==family)
            r.require(metrics['status_distributions'][family]=={s:counts[s] for s in r.c.STATUSES},'Independent status counts differ')
        r.require(metrics['keep_reject_agreement']['numerator']==sum((values[(cid,'A')]['anti_collapse']['status']=='CLEAR_COLLAPSE')==(values[(cid,'B')]['anti_collapse']['status']=='CLEAR_COLLAPSE') for cid in ids),'Independent keep agreement differs')
        for cid in ids:
            statuses={f:values[(cid,f)]['anti_collapse']['status'] for f in 'AB'}
            r.require(review[cid]['statuses']==statuses,'Review changed observed statuses')
            for field in ('formalization_review','one_rule_review','mechanism_review','suppression_or_retention_review'):
                r.require(isinstance(review[cid].get(field),str) and review[cid][field].strip(),'Missing review: '+field)
            if 'CLEAR_COLLAPSE' in statuses.values():r.require(bool(review[cid].get('dangerous_suppression_review')),'Missing rejection audit')
        r.require(set(metrics['clear_collapse_cases'])=={cid for cid in ids if any(values[(cid,f)]['anti_collapse']['status']=='CLEAR_COLLAPSE' for f in 'AB')},'Incomplete rejection inventory')
    else:r.require('insufficient natural-output coverage' in report.read_text().lower(),'Coverage failure not reported')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--private',action='store_true');a=p.parse_args();print(verify(a.private))
