"""Strict pairwise contracts; no absolute-displacement dependency."""
import hashlib
import importlib.util
import json
from pathlib import Path
import jsonschema
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('b1_frozen_validity',HERE.parent/'v0.3/contracts.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
CRITERIA=('action','observables','inferential_warrant','problem_decomposition','inquiry_trajectory')
RELATIONS=('mapping_1_more','mapping_2_more','tie','indeterminate')
def require(ok,message):
 if not ok:raise ValueError(message)
def unique_object(pairs):
 out={}
 for k,v in pairs:
  require(k not in out,'Duplicate JSON key: '+k);out[k]=v
 return out
def read(path):return json.loads(Path(path).read_text(),object_pairs_hook=unique_object)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def validate(value,kind,candidate=None):
 if kind=='validity':return old.validate(value,'validity',candidate)
 name='output' if kind=='comparison' else kind
 schema=read(HERE/f'{name}.schema.json');jsonschema.Draft202012Validator(schema).validate(value)
 if candidate is not None:require(value['case_id']==candidate['case_id'],'Response identity mismatch')
 if kind=='comparison':
  if value['overall_relation'] in ('A_more_displacing','B_more_displacing'):
   require(value['decisive_basis']['primary_criterion'] in CRITERIA,'Direction needs decisive criterion')
  if value['overall_relation']=='indeterminate':require(bool(value['uncertainty']),'Indeterminate needs missing-information explanation')
 return value
def normalize_relation(relation,pair,criterion=False):
 if relation in ('tie','indeterminate'):return relation
 slot=relation if criterion else relation.split('_')[0]
 require(slot in ('A','B'),'Unknown presentation relation')
 return 'mapping_1_more' if pair['mapping_'+slot]==pair['mapping_1'] else 'mapping_2_more'
def mapping_slot(pair,mapping):
 require(mapping in (pair['mapping_1'],pair['mapping_2']),'Unknown mapping')
 return 'mapping_A' if pair['mapping_A']==mapping else 'mapping_B'
def validate_pair(pair,mappings,baselines,admissions):
 validate(pair,'pair');a,b=(mappings[pair[k]] for k in ('mapping_1','mapping_2'))
 require(pair['mapping_1']<pair['mapping_2'],'Canonical identity order')
 require({pair['mapping_A'],pair['mapping_B']}=={pair['mapping_1'],pair['mapping_2']},'Invalid orientation')
 baseline=baselines[pair['target_id']]
 for d in (a,b):
  require(d['target']['question']==baseline['target_task'] and d['target']['domain']==baseline['target_domain'],'Target or baseline mismatch')
  gate=admissions[d['case_id']]
  require(gate['admitted'] and gate['validity_A']==gate['validity_B']=='Valid','Both mappings must be unconditional Valid/Valid')
  require(gate['target_id']==pair['target_id'],'Target identity mismatch')
 require((pair['control_of'] is None)==(pair['cohort']=='primary'),'Invalid control designation')
 return pair
