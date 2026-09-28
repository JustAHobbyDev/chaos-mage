"""Strict Experiment B contracts and deterministic admission constraints."""
import importlib.util
import json
from pathlib import Path
import jsonschema
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('historical_contracts',HERE.parent/'v0.3/contracts.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
read,require,sha,unique_object=old.read,old.require,old.sha,old.unique_object
DIMS=old.DIMS
BANDS=('Native','Adjacent','Remote')
SCOPE='Assume only that the listed instantiation conditions hold; retain source, mapping, target question and native baseline exactly.'

def validate(v,kind,candidate=None):
 if kind=='validity':return old.validate(v,kind,candidate)
 schema=read(HERE/f'{kind}.schema.json');jsonschema.Draft202012Validator.check_schema(schema);jsonschema.Draft202012Validator(schema).validate(v)
 if candidate is not None:require(v['case_id']==candidate['case_id'],'Identity changed')
 if kind=='displacement':
  require(all(type(v['dimensions'][d]['level']) is int for d in DIMS),'Levels must be true integers')
  a=v['nearest_alternative'];cls=v['class']
  require((v['boundary_status']=='clear' and a is None) or (v['boundary_status']=='borderline' and a is not None and abs(BANDS.index(a)-BANDS.index(cls))==1),'Invalid boundary alternative')
 if kind=='packet':
  require(('applicability_assumption' in v)==v['provisional'],'Assumption only for provisional packets')
  require(v['native_baseline']['target_domain']==v['target']['domain'] and v['native_baseline']['target_task']==v['target']['question'],'Baseline target changed')
 return v

def validate_admission(v,judgments,candidate):
 validate(v,'admission',candidate)
 for j in judgments.values():validate(j,'validity',candidate)
 expected=[(f,i,t) for f,j in judgments.items() for i,t in enumerate(j['validity']['unresolved_conditions'])]
 actual=[(x['family'],x['index'],x['text']) for x in v['conditions']]
 require(sorted(actual)==sorted(expected),'Every original condition must be reviewed exactly once')
 statuses=[j['validity']['final_status'] for j in judgments.values()]
 require(set(judgments)=={'A','B'},'Both families required')
 all_valid=statuses==['Valid','Valid']
 if v['cohort']=='primary':require(all_valid and not actual and v['applicability_assumption'] is None,'Primary requires two unconditional Valid judgments')
 elif v['cohort']=='provisional':
  require('Conditional' in statuses and 'Invalid' not in statuses,'Invalid cannot enter provisional')
  require(actual and all(x['designation']=='instantiation' and x['compatible'] for x in v['conditions']),'Only compatible instantiation conditions may enter')
  require(v['applicability_assumption'] is not None,'Missing assumption')
  require(v['applicability_assumption']['conditions']==[x['text'] for x in v['conditions']],'Assumption must cover exact conditions without additions')
 else:require(v['applicability_assumption'] is None,'Holdout cannot carry an assumption')
 # Review may conservatively withhold Valid/Valid, but cannot rewrite it.
 return v

def viability(admissions,manifest):
 ids={a['case_id'] for a in admissions if a['cohort']=='primary'}
 core=[m for m in manifest if m['core'] and m['case_id'] in ids]
 return {'primary_core_count':len(core),'baseline_count':len({m['target_id'] for m in core}),'intended_bands':sorted({m['intended_band'] for m in core}),'passes':len(core)>=12 and len({m['target_id'] for m in core})>=6 and {m['intended_band'] for m in core}==set(BANDS)}
