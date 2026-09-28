"""Ordinal per-dimension and class comparisons, never an aggregate distance."""
from collections import Counter
from itertools import combinations
from contracts import BANDS,DIMS

def agreement(pairs):
 pairs=list(pairs);n=len(pairs);a=sum(x==y for x,y in pairs)
 return {'agreements':a,'pairs':n,'rate':a/n if n else None}
def relation(a,b):return '<' if a<b else '>' if a>b else '='
def cohort(values,rows):
 ids=[r['case_id'] for r in rows];pairs=[(cid,values[(cid,'A')],values[(cid,'B')]) for cid in ids if (cid,'A') in values and (cid,'B') in values]
 confusion={a:{b:0 for b in BANDS} for a in BANDS};steps=Counter();border=0
 for cid,a,b in pairs:
  confusion[a['class']][b['class']]+=1;steps[abs(BANDS.index(a['class'])-BANDS.index(b['class']))]+=1
  border+=a['class']!=b['class'] and 'borderline' in (a['boundary_status'],b['boundary_status'])
 dims={}
 for d in DIMS:
  scores=[(a['dimensions'][d]['level'],b['dimensions'][d]['level']) for _,a,b in pairs]
  dims[d]={**agreement(scores),'mean_absolute_ordinal_disagreement':sum(abs(a-b) for a,b in scores)/len(scores) if scores else None}
 ordering=[]
 for target in sorted({r['target_id'] for r in rows}):
  for a,b in combinations(sorted(r['case_id'] for r in rows if r['target_id']==target),2):
   rel={f:relation(BANDS.index(values[(a,f)]['class']),BANDS.index(values[(b,f)]['class'])) if (a,f) in values and (b,f) in values else None for f in ('A','B')}
   ordering.append({'target_id':target,'case_1':a,'case_2':b,**rel})
 observed=[(x['A'],x['B']) for x in ordering if x['A'] is not None and x['B'] is not None]
 return {'planned_pairs':len(ids),'observed_pairs':len(pairs),'missing_pair_ids':[cid for cid in ids if (cid,'A') not in values or (cid,'B') not in values],
 'distributions':{f:{band:sum(values[(cid,f)]['class']==band for cid in ids if (cid,f) in values) for band in BANDS} for f in ('A','B')},
 'class_agreement':agreement((a['class'],b['class']) for _,a,b in pairs),'confusion_rows_A_columns_B':confusion,'same_class':steps[0],'one_step':steps[1],'native_remote':steps[2],
 'boundary_status_agreement':agreement((a['boundary_status'],b['boundary_status']) for _,a,b in pairs),'class_disagreements_with_borderline':{'count':border,'denominator':steps[1]+steps[2],'rate':border/(steps[1]+steps[2]) if steps[1]+steps[2] else None},'dimensions':dims,
 'ordering':{'planned_unordered_pairs':len(ordering),'observed_unordered_pairs':len(observed),'agreement':agreement(observed),'relations':ordering}}

def calculate(values,manifest,admissions):
 lookup={a['case_id']:a for a in admissions};result={}
 for name in ('primary','provisional'):
  rows=[r for r in manifest if lookup[r['case_id']]['cohort']==name]
  result[name]={'all':cohort(values,rows),'core_only':cohort(values,[r for r in rows if r['core']])}
 variants=[]
 for row in manifest:
  if row['core']:continue
  cid=row['case_id'];base=row['variant_of'];families={}
  for f in ('A','B'):
   a=values.get((base,f));b=values.get((cid,f))
   families[f]={'base_class':a['class'] if a else None,'variant_class':b['class'] if b else None,'relation':relation(BANDS.index(a['class']),BANDS.index(b['class'])) if a and b else None,'base_boundary':a['boundary_status'] if a else None,'variant_boundary':b['boundary_status'] if b else None,'baseline_reinterpretation':'Requires qualitative review of rationales; fixed baseline bytes cannot change.'}
  variants.append({'base':base,'variant':cid,'target_id':row['target_id'],'base_cohort':lookup[base]['cohort'],'variant_cohort':lookup[cid]['cohort'],'families':families})
 result['evidence_variants']=variants
 return result

def post_result_status(a,b):
 if a['class']!=b['class']:return 'contested'
 if 'borderline' in (a['boundary_status'],b['boundary_status']):return 'boundary'
 return 'consensus'
