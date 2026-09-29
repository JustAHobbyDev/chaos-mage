"""Strict local contracts and immutable historical validity; no semantic repair."""
import hashlib, importlib.util, json
from pathlib import Path
import jsonschema
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('d_frozen_validity',HERE.parent/'v0.3/contracts.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
LOCI=('action','observable','inferential_warrant','problem_decomposition','next_inquiry')
STATUSES=('CLEAR_COLLAPSE','SUFFICIENT_DEPARTURE','BORDERLINE_KEEP')
read,require,unique_object=old.read,old.require,old.unique_object
sha=old.sha
def validate(value,kind,candidate=None):
 if kind in ('validity','candidate'):return old.validate(value,kind,candidate)
 schema='output' if kind=='anti-collapse' else kind
 jsonschema.Draft202012Validator(read(HERE/'schemas'/f'{schema}.schema.json')).validate(value)
 if candidate is not None:require(value['case_id']==candidate['case_id'],'Case identity mismatch')
 return value
