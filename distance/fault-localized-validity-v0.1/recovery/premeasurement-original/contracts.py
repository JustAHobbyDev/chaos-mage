"""Experiment G strict structural contracts; no semantic verdict rewriting."""
from pathlib import Path
import hashlib,json,jsonschema
H=Path(__file__).resolve().parent
CLAIM=['SUPPORTED','CONDITIONAL_WARRANT','UNSUPPORTED','UNCERTAIN']
ARTIFACT=['KEEP_WITH_WARRANT_FLAGS','KEEP_WITH_REDUCED_SCOPE','CORE_INVALID','UNCERTAIN_LOAD_BEARING']
def require(ok,msg):
 if not ok: raise ValueError(msg)
def unique(pairs):
 d={}
 for k,v in pairs:
  require(k not in d,'Duplicate JSON key'); d[k]=v
 return d
def read(p): return json.loads(Path(p).read_text(),object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(b): return hashlib.sha256(b).hexdigest()
def obj(p): return {'type':'object','additionalProperties':False,'required':list(p),'properties':p}
def arr(x): return {'type':'array','items':x}
def enum(x): return {'type':'string','enum':x}
T={'type':'string','minLength':1,'pattern':r'\S'}
def nullable(x): return {'anyOf':[x,{'type':'null'}]}
def component(status): return obj({'status':enum(status),'rationale':T})
def schema(stage):
 if stage=='claim-warrant': return obj({'claim_id':T,'status':enum(CLAIM),'rationale':T,'signal_basis':T,'stated_empirical_relation':nullable(T),'uncertainty':arr(T)})
 return obj({'artifact_viability':obj({'case_id':T,'unsupported_claims':arr(obj({'claim_id':T})),
 'mechanism_survival':component(['survives','partially_survives','does_not_survive','uncertain']),
 'target_contribution_survival':obj({'status':enum(['substantially_survives','reduced_but_material','no_material_contribution','uncertain']),'surviving_contributions':arr(T)}),
 'dependency_cascade':obj({'failed_downstream_claims':arr(T),'failed_actions_or_inquiries':arr(T),'surviving_actions_or_inquiries':arr(T),'rationale':T}),
 'per_claim_dependencies':arr(obj({'claim_id':T,'signal':T,'dependent_claims':arr(T),'dependent_actions_or_inquiries':arr(T),'rationale':T})),
 'artifact_status':enum(ARTIFACT),'rationale':T})})
def validate(v,stage,identity,candidate=None,unsupported=None):
 jsonschema.Draft202012Validator(schema(stage)).validate(v)
 if stage=='claim-warrant':
  require(v['claim_id']==identity,'Identity mismatch')
  require((v['status']=='CONDITIONAL_WARRANT')==(v['stated_empirical_relation'] is not None),'Conditional requires exact supplied empirical relation only')
  require(v['status']!='UNCERTAIN' or bool(v['uncertainty']),'Uncertainty explanation missing')
  if candidate:
   texts=list(candidate['mapping'].values())+list(candidate['source']['instrument'].values())
   require(any(v['signal_basis'] in t for t in texts),'Signal basis must be an exact quotation')
   if v['stated_empirical_relation'] is not None: require(any(v['stated_empirical_relation'] in t for t in candidate['mapping'].values()),'Relation absent from mapping')
  return
 a=v['artifact_viability']; require(a['case_id']==identity,'Identity mismatch')
 ids=[x['claim_id'] for x in a['unsupported_claims']]; deps=[x['claim_id'] for x in a['per_claim_dependencies']]
 require(bool(ids) and len(ids)==len(set(ids)) and sorted(ids)==sorted(deps),'Unsupported/dependency coverage')
 if unsupported is not None: require(set(ids)==set(unsupported),'Wrong deletion set')
 m=a['mechanism_survival']['status']; t=a['target_contribution_survival']['status']; s=a['artifact_status']
 valid={'KEEP_WITH_WARRANT_FLAGS':m=='survives' and t=='substantially_survives','KEEP_WITH_REDUCED_SCOPE':m in ['survives','partially_survives'] and t=='reduced_but_material','CORE_INVALID':m=='does_not_survive' or t=='no_material_contribution','UNCERTAIN_LOAD_BEARING':m=='uncertain' or t=='uncertain'}
 require(valid[s],'Artifact-status invariant violation')
 require(t not in ['substantially_survives','reduced_but_material'] or bool(a['target_contribution_survival']['surviving_contributions']),'Material survival needs contributions')
 require(t!='no_material_contribution' or not a['target_contribution_survival']['surviving_contributions'],'No material contribution contradicts survivors')
