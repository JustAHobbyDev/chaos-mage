#!/usr/bin/env python3
"""Check the completed report, reviews and full pre-existing tracked corpus."""
from collections import Counter
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('qualification_report_verification',HERE/'runner.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)


def verify():
    data=r.complete_results();history=r.historical()
    reviews=r.read(HERE/'review/case-reviews.json');r.check_reviews(reviews['cases'],reviews['qualification'])
    audit=r.read(HERE/'review/execution-audit.json')
    counts=dict(Counter(c['disagreement_class'] for c in reviews['cases']))
    r.require(counts==audit['disagreement_counts'],'Review/audit count mismatch')
    for c in reviews['cases']:
        cid=c['qualification_id'];stage=r.case(cid)['stage']
        r.require(c['muse']['status']==r.status(data[cid],stage),'Muse review mismatch')
        for model in ('astra','fable'):
            r.require(c['historical_context'][model+'_status']==r.status(history[cid][model],stage),'Historical context mismatch')
    r.require(reviews['systematic_pathology']['cases']==['E006','E022','E030'],'Failure pattern changed')
    base=r.read(HERE/'manifest.json')['base_commit']
    original=set(r.git('ls-tree','-r','--name-only',base).decode().splitlines())
    changed=set(r.git('diff',base,'--name-only').decode().splitlines())
    r.require(not original.intersection(changed),'Pre-existing tracked artifact changed')
    report=(r.ROOT/'distance/review/model-qualification-v0.1.md').read_text()
    r.require('**Qualification: `'+reviews['qualification']+'`.**' in report,'Report outcome mismatch')
    policy=(r.ROOT/'docs/MODEL-POLICY.md').read_text()
    r.require('**not_qualified**' in policy and 'No transition to Muse' in policy,'Policy mismatch')
    checks=r.read(HERE/'review/verification.json')
    r.require(checks['passed'] and checks['total_tests']==327 and len(checks['checks'])==32,'Historical checks incomplete')
    return {'at':r.now(),'qualification':reviews['qualification'],'results_freeze_commit':r.checkpoint(HERE/'results-freeze.json'),
        'disagreement_counts':counts,'pre_existing_tracked_files_verified':len(original),'root_readme_restored':True,
        'historical_artifacts_unchanged':True,'report_policy_and_review_consistent':True}


if __name__=='__main__':
    import json
    print(json.dumps(verify(),indent=2))
