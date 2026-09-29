"""Build strict canonical contracts and provider structural projections before freeze."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
S={'type':'string','minLength':1,'pattern':r'\S'}
LOCI=('action','observable','inferential_warrant','problem_decomposition','next_inquiry')
def obj(p):return {'type':'object','properties':p,'required':list(p),'additionalProperties':False}
def enum(*x):return {'type':'string','enum':list(x)}
def arr(x):return {'type':'array','items':x}
def projection(x):
 if isinstance(x,dict):return {k:projection(v) for k,v in x.items() if k not in ('$schema','$id','allOf')}
 if isinstance(x,list):return [projection(v) for v in x]
 return x
def write(name,x):
 (HERE/'schemas'/f'{name}.schema.json').write_text(json.dumps(x,indent=2)+'\n')
def main():
 departure=obj({'status':enum('present','absent','uncertain'),'rationale':S})
 body=obj({'status':enum('CLEAR_COLLAPSE','SUFFICIENT_DEPARTURE','BORDERLINE_KEEP'),
 'departures':obj({k:departure for k in LOCI}),
 'materiality':obj({'status':enum('material','immaterial','uncertain'),'rationale':S}),
 'native_reduction':obj({'collapses_without_loss':enum('yes','no','uncertain'),'closest_native_equivalent':S,'lost_if_reduced':arr(S),'rationale':S}),
 'formalization':obj({'merely_makes_native_reasoning_explicit':enum('yes','no','uncertain'),'new_epistemic_constraint':{'type':['string','null'],'minLength':1,'pattern':r'\S'},'rationale':S}),
 'decisive_reason':S,'uncertainty':arr(S)})
 body['allOf']=[
 {'if':{'properties':{'status':{'const':'CLEAR_COLLAPSE'}}},'then':{'properties':{'materiality':{'properties':{'status':{'enum':['immaterial','uncertain']}}},'native_reduction':{'properties':{'collapses_without_loss':{'enum':['yes','uncertain']}}}}}},
 {'if':{'properties':{'status':{'const':'SUFFICIENT_DEPARTURE'}}},'then':{'properties':{'materiality':{'properties':{'status':{'enum':['material','uncertain']}}},'native_reduction':{'properties':{'collapses_without_loss':{'enum':['no','uncertain']}}}},'not':{'properties':{'departures':{'properties':{k:{'properties':{'status':{'const':'absent'}}} for k in LOCI}}}}}}
 ]
 write('output',{'$schema':'https://json-schema.org/draft/2020-12/schema',**obj({'case_id':S,'anti_collapse':body})})
 for name in ('candidate','validity'):(HERE/'schemas'/f'{name}.schema.json').write_bytes((HERE.parent/'v0.3'/f'{name}.schema.json').read_bytes())
 for stage,name in [('validity','validity'),('anti-collapse','output')]:write(stage+'-wire',projection(json.loads((HERE/'schemas'/f'{name}.schema.json').read_text())))
 write('neutralization',obj({k:S for k in ('procedure','action','observables','inferential_warrant','problem_decomposition','next_inquiry')}))
 base=json.loads((HERE.parent/'displacement-v0.3/baseline.schema.json').read_text())
 for k in ('ordinary_inference_patterns','ordinary_next_actions'):base['properties'][k]=arr(S);base['required'].append(k)
 write('baseline',base)
 write('packet',obj({'case_id':S,'target':obj({'domain':S,'question':S,'evidence':arr(S)}),'native_baseline':base,'source_neutral':json.loads((HERE/'schemas/neutralization.schema.json').read_text())}))
 write('admission',obj({'case_id':S,'target_id':S,'validity_A':enum('Valid','Conditional','Invalid'),'validity_B':enum('Valid','Conditional','Invalid'),'admitted':{'type':'boolean'}}))
if __name__=='__main__':main()
