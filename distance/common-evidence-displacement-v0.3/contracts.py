"""Canonical validation and byte/provenance checks; no output repair."""
import hashlib
import importlib.util
import json
from pathlib import Path
import jsonschema
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('b2_frozen_validity',HERE.parent/'v0.3/contracts.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
CRITERIA=('action','observables','inferential_warrant','problem_decomposition','inquiry_trajectory')
DIAGNOSTICS=('local_depth','inquiry_propagation','task_reach','native_reducibility')
RELATIONS=('mapping_1_dominates','mapping_2_dominates','tradeoff','approximately_equal','insufficient_information')
def require(ok,message):
    if not ok:raise ValueError(message)
def unique_object(pairs):
    result={}
    for k,v in pairs:
        require(k not in result,'Duplicate JSON key: '+k);result[k]=v
    return result
def read(path):return json.loads(Path(path).read_text(),object_pairs_hook=unique_object)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def serialized(value):return (json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
def validate(value,kind,candidate=None):
    if kind=='validity':return old.validate(value,'validity',candidate)
    schema='output' if kind in ('prospective','consequence') else kind
    jsonschema.Draft202012Validator(read(HERE/'schemas'/f'{schema}.schema.json')).validate(value)
    if candidate is not None:require(value['case_id']==candidate['case_id'],'Response identity mismatch')
    if kind in ('prospective','consequence'):
        require(value['stage']==kind,'Stage mismatch')
        if value['overall_relation']=='insufficient_information':require(bool(value['uncertainty']),'Insufficiency needs missing information')
    return value
def normalize(relation,pair):
    if relation in ('balanced','indeterminate','tradeoff','approximately_equal','insufficient_information'):return relation
    slot=relation.split('_')[0]
    require(slot in ('A','B'),'Unknown relation')
    identity='mapping_1' if pair['mapping_'+slot]==pair['mapping_1'] else 'mapping_2'
    return identity+('_dominates' if relation.endswith('_dominates') else '')
def validate_outcome(row,value):
    import derive
    validate(value,'outcome');tid=row['target_id'];world=read(HERE/'worlds'/f'{tid}.json');common=read(HERE/'common-states'/f'{tid}.json')
    require(value['world_id']==world['world_id'],'Different world')
    require(set(value['world_facts_used'])<=set(world['facts']),'Undeclared world fact')
    require(bool(value['world_facts_used']) and bool(value['operation_performed']['steps']),'Missing derivation provenance')
    require(value==derive.derive(row),'Outcome derivation, world, mapping, engine, or resource ledger changed')
    for k,v in value['resource_use'].items():require(type(v) is int and v<=common['investigation_budget']['resource_ledger'][k],'Budget exceeded')
    return value
def validate_pair(pair,mappings,commons,admissions):
    validate(pair,'pair');tid=pair['target_id'];common=commons[tid]
    require(pair['mapping_1']<pair['mapping_2'],'Canonical identity order')
    require({pair['mapping_A'],pair['mapping_B']}=={pair['mapping_1'],pair['mapping_2']},'Invalid orientation')
    require(pair['world_id']=='W-'+tid,'Different world')
    for mid in (pair['mapping_1'],pair['mapping_2']):
        mapping=mappings[mid];gate=admissions[mid]
        require(gate['target_id']==tid,'Cross-target pair')
        require(gate['admitted'] and gate['validity_A']==gate['validity_B']=='Valid','Requires unconditional Valid/Valid')
        require(mapping['target']=={**common['target'],'evidence':[json.dumps(common,ensure_ascii=False,sort_keys=True)]},'Shared target/evidence drift')
    require(pair['common_state_sha256']==sha(HERE/'common-states'/f'{tid}.json'),'Common state drift')
    require((pair['control_of'] is None)==(pair['cohort']=='primary'),'Control designation mismatch')
    return pair
