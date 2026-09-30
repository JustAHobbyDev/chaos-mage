"""Review-only checks; no provider access and no historical consensus criterion."""
import importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gemini_review_runner',HERE/'runner.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)


def check_reviews(record, contextual=False):
    r.require(record['qualification'] in r.OUTCOMES,'Invalid qualification outcome')
    rows=record['cases']
    r.require(len(rows)==12 and {v['qualification_id'] for v in rows}=={c['qualification_id'] for c in r.cases()},'Review coverage')
    for v in rows:
        r.require(v['source_case_id']==v['qualification_id'],'Review case mismatch')
        r.require(set(v['capability_dimensions'])==set(r.DIMENSIONS),'Dimension coverage')
        r.require(all(x in ('pass','concern','fail') for x in v['capability_dimensions'].values()),'Invalid assessment')
        r.require(v['preliminary_disagreement_class'] in r.CATEGORIES,'Invalid preliminary class')
        r.require(v['downstream_consequence'] in ('none','minor','material'),'Invalid consequence')
        r.require(bool(v['gemini']['key_reasoning'].strip()) and bool(v['rationale'].strip()),'Missing independent rationale')
        if contextual:
            r.require(v['final_disagreement_class'] in r.CATEGORIES,'Invalid final class')
            changed=v['preliminary_disagreement_class']!=v['final_disagreement_class']
            r.require(v['historical_context_changed_classification']==changed,'Change flag mismatch')
            if changed:r.require(bool(v['classification_change_explanation'].strip()),'Missing change explanation')
            r.require(set(v['historical_context'])=={'astra_status','fable_status','muse_status'},'Historical context coverage')
    return True
