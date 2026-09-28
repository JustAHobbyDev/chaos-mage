"""Generate canonical B.2 contracts before preparation freeze."""
import copy
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
S={'type':'string','minLength':1,'pattern':r'\S'}
def obj(properties):return {'type':'object','properties':properties,'required':list(properties),'additionalProperties':False}
def arr(items):return {'type':'array','items':items}
def enum(*values):return {'type':'string','enum':list(values)}
def projection(v):
    if isinstance(v,dict):return {k:projection(x) for k,x in v.items() if k not in ('$schema','$id','allOf')}
    if isinstance(v,list):return [projection(x) for x in v]
    return v
def write(name,schema):
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema',**schema}
    (HERE/'schemas'/f'{name}.schema.json').write_text(json.dumps(schema,indent=2)+'\n')
    return schema
def main():
    relation=obj({'relation':enum('A','B','balanced','indeterminate'),'rationale':S})
    criteria=('action','observables','inferential_warrant','problem_decomposition','inquiry_trajectory')
    diagnostics=('local_depth','inquiry_propagation','task_reach','native_reducibility')
    out=obj({'case_id':S,'stage':enum('prospective','consequence'),
      'meaningful_difference':obj({'status':enum('yes','no','uncertain'),'rationale':S}),
      'criteria':obj({k:relation for k in criteria}), 'consequence_structure':obj({k:relation for k in diagnostics}),
      'decisive_basis':obj({k:S for k in ('most_important_difference',*diagnostics,'rationale')}),
      'overall_relation':enum('A_dominates','B_dominates','tradeoff','approximately_equal','insufficient_information'),
      'confidence':enum('clear','close'),'uncertainty':arr(S)})
    out['allOf']=[{'if':{'properties':{'meaningful_difference':{'properties':{'status':{'const':status}}}}},
                  'then':{'properties':{'overall_relation':{'enum':values}}}} for status,values in
                  [('yes',['A_dominates','B_dominates','tradeoff']),('no',['approximately_equal']),('uncertain',['insufficient_information'])]]
    canonical=write('output',out)
    for stage in ('prospective','consequence'):
        (HERE/'schemas'/f'{stage}-wire.schema.json').write_text(json.dumps(projection(canonical),indent=2)+'\n')
    for name in ('candidate','validity'):
        (HERE/'schemas'/f'{name}.schema.json').write_bytes((HERE.parent/'v0.3'/f'{name}.schema.json').read_bytes())
    validity=json.loads((HERE/'schemas/validity.schema.json').read_text())
    (HERE/'schemas/validity-wire.schema.json').write_text(json.dumps(projection(validity),indent=2)+'\n')
    baseline=json.loads((HERE.parent/'displacement-v0.3/baseline.schema.json').read_text())
    numbers={'type':'object','additionalProperties':{'type':'integer','minimum':0},'minProperties':1}
    common=obj({'target':obj({'domain':S,'question':S}),'native_baseline':baseline,
       'shared_state':obj({'facts':arr(S),'artifacts':{'type':'object'},'initial_observations':arr(S),'known_uncertainties':arr(S),
         'available_affordances':arr(S),'constraints':arr(S)}),
       'investigation_budget':obj({'primary_operations':{'const':1},'immediate_followups':{'const':1},'new_external_sources':{'const':0},
                                  'resource_ledger':numbers,'other_constraints':arr(S)})})
    write('common-state',common)
    write('world',obj({'world_id':S,'target_id':S,'observable_start':common,'facts':{'type':'object','minProperties':1},'mutation_policy':S,'authorship_limit':S}))
    step=obj({'phase':enum('primary','followup'),'affordance':S,'parameters':{'type':'object'},'resulting_signal':{'type':'object'},'resource_use':{'type':'object','additionalProperties':{'type':'integer','minimum':0}}})
    write('outcome',obj({'mapping_id':S,'target_id':S,'world_id':S,'world_sha256':S,'common_state_sha256':S,'mapping_sha256':S,
      'operation_performed':obj({'recipe':S,'steps':arr(step)}),'world_facts_used':arr(S),'resulting_signal':arr({'type':'object'}),
      'derivation':obj({'engine_sha256':S,'method':S}),'resource_use':numbers,'limits':S}))
    write('pair',obj({**{k:S for k in ('case_id','target_id','mapping_1','mapping_2','mapping_A','mapping_B','world_id','common_state_sha256')},
                      'cohort':enum('primary','orientation-control'),'control_of':{'type':['string','null']}}))
    write('admission',obj({'mapping_id':S,'target_id':S,'validity_A':enum('Valid','Conditional','Invalid'),
                         'validity_B':enum('Valid','Conditional','Invalid'),'admitted':{'type':'boolean'}}))

if __name__=='__main__':main()
