"""Strict canonical contracts; wire projections never replace local invariants."""
from pathlib import Path
import hashlib
import json
import jsonschema

HERE = Path(__file__).resolve().parent
CATEGORIES = ['execution_precondition', 'mechanism_condition', 'warrant_condition', 'target_fidelity_condition', 'mixed', 'uncertain']
LINKS = ['state_operation_signal', 'signal_inference', 'inference_target', 'multiple']

def require(ok, message):
    if not ok: raise ValueError(message)

def unique(pairs):
    out = {}
    for k, v in pairs:
        require(k not in out, 'Duplicate JSON key: ' + k)
        out[k] = v
    return out

def read(p):
    return json.loads(Path(p).read_text(), object_pairs_hook=unique, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(b): return hashlib.sha256(b).hexdigest()
def obj(properties): return {'type': 'object', 'additionalProperties': False, 'required': list(properties), 'properties': properties}
def enum(values): return {'type': 'string', 'enum': values}
def arr(items): return {'type': 'array', 'items': items}
TEXT = {'type': 'string', 'minLength': 1, 'pattern': r'\S'}
def nullable(x): return {'anyOf': [x, {'type': 'null'}]}
def component(statuses): return obj({'status': enum(statuses), 'rationale': TEXT})

def schema(stage):
    if stage == 'taxonomy':
        s = obj({'condition_id': TEXT, 'category': enum(CATEGORIES), 'rationale': TEXT,
                 'if_execution': nullable(obj({'verification_or_satisfaction_method': TEXT})),
                 'if_validity_relevant': nullable(obj({'affected_link': enum(LINKS)})), 'uncertainty': arr(TEXT)})
        s['allOf'] = [
            {'if': {'properties': {'category': {'const': 'execution_precondition'}}},
             'then': {'properties': {'if_execution': {'type': 'object'}, 'if_validity_relevant': {'type': 'null'}}}},
            {'if': {'properties': {'category': {'enum': CATEGORIES[1:4]}}},
             'then': {'properties': {'if_execution': {'type': 'null'}, 'if_validity_relevant': {'type': 'object'}}}}]
    else:
        s = obj({'case_id': TEXT,
                 'mechanism_fidelity': component(['preserved','conditional','not_preserved']),
                 'warrant_validity': component(['supported','conditional','unsupported']),
                 'target_fidelity': component(['addressed','conditional','not_addressed']),
                 'conditions': arr(obj({'condition': TEXT, 'category': enum(CATEGORIES), 'rationale': TEXT, 'effect_on_validity': enum(['none','conditional','invalidating'])})),
                 'execution_readiness': obj({'status': enum(['ready','requires_preconditions','unknown']), 'preconditions': arr(obj({'condition': TEXT, 'how_to_establish': TEXT, 'why_execution_only': TEXT})), 'rationale': TEXT}),
                 'final_status': enum(['Valid','Conditional','Invalid']), 'uncertainty': arr(TEXT)})
        fail = {'anyOf': [{'properties': {k: {'properties': {'status': {'const': v}}}}} for k,v in [('mechanism_fidelity','not_preserved'),('warrant_validity','unsupported'),('target_fidelity','not_addressed')]]}
        conditional = {'anyOf': [{'properties': {k: {'properties': {'status': {'const': 'conditional'}}}}} for k in ('mechanism_fidelity','warrant_validity','target_fidelity')]}
        s['allOf'] = [
            {'if': fail, 'then': {'properties': {'final_status': {'const': 'Invalid'}}}, 'else': {'if': conditional, 'then': {'properties': {'final_status': {'const': 'Conditional'}}}, 'else': {'properties': {'final_status': {'const': 'Valid'}}}}},
            {'properties': {'conditions': {'items': {'if': {'properties': {'category': {'const': 'execution_precondition'}}}, 'then': {'properties': {'effect_on_validity': {'const': 'none'}}}}}}}]
    return {'$schema': 'https://json-schema.org/draft/2020-12/schema', **s}

def wire(s):
    if isinstance(s, dict): return {k: wire(v) for k,v in s.items() if k not in ('$schema', '$id', 'allOf')}
    if isinstance(s, list): return [wire(v) for v in s]
    return s

def validate(v, stage, identity):
    jsonschema.Draft202012Validator(read(HERE/'schemas'/f'{stage}.schema.json')).validate(v)
    require(v['condition_id' if stage == 'taxonomy' else 'case_id'] == identity, 'Response identity mismatch')
    if stage == 'taxonomy':
        cat = v['category']
        if cat in CATEGORIES[1:4]:
            require(v['if_validity_relevant']['affected_link'] == LINKS[CATEGORIES.index(cat)-1], 'Category/link contradiction')
        if cat == 'uncertain': require(bool(v['uncertainty']), 'Uncertain requires explanation')
        return v
    statuses = [v[k]['status'] for k in ('mechanism_fidelity','warrant_validity','target_fidelity')]
    final = 'Invalid' if any(x in statuses for x in ('not_preserved','unsupported','not_addressed')) else 'Conditional' if 'conditional' in statuses else 'Valid'
    require(v['final_status'] == final, 'Final derivation contradiction')
    cond = v['conditions']; ready = v['execution_readiness']
    execution = [c for c in cond if c['category'] == 'execution_precondition']
    require(all(c['effect_on_validity'] == 'none' for c in execution), 'Execution cannot change validity')
    require({c['condition'] for c in execution} == {c['condition'] for c in ready['preconditions']}, 'Precondition lists inconsistent')
    require(len({c['condition'] for c in cond}) == len(cond), 'Duplicate condition')
    require(len({c['condition'] for c in ready['preconditions']}) == len(ready['preconditions']), 'Duplicate precondition')
    if ready['status'] == 'requires_preconditions': require(bool(execution), 'Missing execution prerequisites')
    else: require(not execution, 'Known prerequisites require requires_preconditions')
    require(not any(c['effect_on_validity']=='invalidating' for c in cond) or final=='Invalid', 'Invalidating condition without failure')
    require(not any(c['effect_on_validity']=='conditional' for c in cond) or final!='Valid', 'Conditional condition with Valid')
    for key, category in [('mechanism_fidelity','mechanism_condition'),('warrant_validity','warrant_condition'),('target_fidelity','target_fidelity_condition')]:
        if v[key]['status']=='conditional': require(any(c['category'] in (category,'mixed') and c['effect_on_validity']=='conditional' for c in cond), 'Conditional component needs corresponding unresolved condition')
    return v
