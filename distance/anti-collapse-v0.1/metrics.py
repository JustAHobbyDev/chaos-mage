"""Descriptive paired judgments; operator intentions select review cohorts, never truth."""
from collections import Counter
from itertools import combinations
import contracts as c

def fraction(n,d):return {'numerator':n,'denominator':d,'fraction':n/d if d else None}
def agreement(values,ids,get):return fraction(sum(get(values[(cid,'A')])==get(values[(cid,'B')]) for cid in ids),len(ids))
def compute(values,design,admissions):
 ids=sorted(r['case_id'] for r in admissions if r['admitted'])
 c.require(set(values)=={(cid,f) for cid in ids for f in 'AB'},'Missing or extra measured judgment; never shrink denominator')
 for (cid,_),value in values.items():c.validate(value,'anti-collapse',{'case_id':cid})
 bodies={k:v['anti_collapse'] for k,v in values.items()};meta={r['case_id']:r for r in design}
 c.require(set(ids)<=set(meta),'Missing design metadata')
 status=lambda v:v['status']
 confusion={s:{t:0 for t in c.STATUSES} for s in c.STATUSES}
 for cid in ids:confusion[status(bodies[(cid,'A')])][status(bodies[(cid,'B')])]+=1
 per_status={}
 for s in c.STATUSES:
  both=sum(all(status(bodies[(cid,f)])==s for f in 'AB') for cid in ids)
  either=sum(any(status(bodies[(cid,f)])==s for f in 'AB') for cid in ids)
  per_status[s]={'binary_agreement':agreement(bodies,ids,lambda v:status(v)==s),'joint_calls_over_either_calls':fraction(both,either)}
 def distributions(cohort):return {f:{s:sum(status(bodies[(cid,f)])==s for cid in cohort) for s in c.STATUSES} for f in 'AB'}
 def cohort_summary(cohort):return {'case_ids':cohort,'case_count':len(cohort),'status_distributions':distributions(cohort),'status_agreement':agreement(bodies,cohort,status)}
 levels={level:cohort_summary([cid for cid in ids if meta[cid]['ladder_level']==level]) for level in 'ABCD'}
 a_ids=levels['A']['case_ids'];cd_ids=[cid for cid in ids if meta[cid]['ladder_level'] in 'CD']
 retention={f:{'kept':fraction(sum(status(bodies[(cid,f)])!='CLEAR_COLLAPSE' for cid in a_ids),len(a_ids)),'cases':[cid for cid in a_ids if status(bodies[(cid,f)])!='CLEAR_COLLAPSE']} for f in 'AB'}
 suppression=[{'case_id':cid,'target_id':meta[cid]['target_id'],'design_level':meta[cid]['ladder_level'],'statuses':{f:status(bodies[(cid,f)]) for f in 'AB'},'rejecting_families':[f for f in 'AB' if status(bodies[(cid,f)])=='CLEAR_COLLAPSE']} for cid in cd_ids if any(status(bodies[(cid,f)])=='CLEAR_COLLAPSE' for f in 'AB')]
 ladders=[]
 for tid in sorted({r['target_id'] for r in design}):
  rows={meta[cid]['ladder_level']:cid for cid in ids if meta[cid]['target_id']==tid}
  states={level:{f:status(bodies[(cid,f)]) for f in 'AB'} for level,cid in rows.items()}
  inversions=[]
  for lo,hi in combinations('ABCD',2):
   if lo not in states or hi not in states:continue
   for f in 'AB':
    if states[lo][f]!='CLEAR_COLLAPSE' and states[hi][f]=='CLEAR_COLLAPSE':inversions.append({'lower_design':lo,'higher_design':hi,'family':f,'lower_status':states[lo][f],'higher_status':states[hi][f]})
  ladders.append({'target_id':tid,'cases':rows,'statuses':states,'retained_to_rejected_contrasts':inversions,'strong_A_departure_CD_collapse':[x for x in inversions if x['lower_design']=='A' and x['higher_design'] in 'CD' and x['lower_status']=='SUFFICIENT_DEPARTURE']})
 return {'primary_cases':len(ids),'primary_judgments':len(values),'status_distributions':distributions(ids),'status_agreement':agreement(bodies,ids,status),'confusion_matrix_A_rows_B_columns':confusion,'per_status_agreement':per_status,'departure_field_agreement':{l:agreement(bodies,ids,lambda v:v['departures'][l]['status']) for l in c.LOCI},'materiality_agreement':agreement(bodies,ids,lambda v:v['materiality']['status']),'native_reduction_agreement':agreement(bodies,ids,lambda v:v['native_reduction']['collapses_without_loss']),'formalization_agreement':agreement(bodies,ids,lambda v:v['formalization']['merely_makes_native_reasoning_explicit']),'design_level_diagnostics':levels,'A_design_retention':retention,'CD_design_suppression_cases':suppression,'adversaries':{tag:cohort_summary([cid for cid in ids if tag in meta[cid]['adversary_tags']]) for tag in ('exotic-collapse','mundane-positive')},'C_primary_locus_diagnostics':{l:cohort_summary([cid for cid in ids if meta[cid]['ladder_level']=='C' and meta[cid]['intended_departure_type']==l]) for l in c.LOCI},'matched_ladders':ladders,'interpretation':{'operator_intent_is_ground_truth':False,'accuracy_computed':False,'composite_score':None,'controls_in_primary':False,'source_framing_causal_effect':'Not measured: neutral-only protocol.','sampling':'One judgment per family/case; related authored cases; no population or within-family reliability estimate.'}}
