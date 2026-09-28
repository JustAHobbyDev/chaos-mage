"""Post-freeze descriptive diagnostics; never used to select cases or call judges."""
import argparse
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner as r
import metrics as m
def compute():
 r.frozen('comparison',True);values=r.published('comparison');pairs=r.pair_records();primary=[p for p in pairs if p['cohort']=='primary'];metrics=m.calculate(values,pairs)
 designs={(d['mapping_1'],d['mapping_2']):d for d in r.read(r.HERE/'operator-manifest.json')['pair_designs']}
 repeated=[x for x in metrics['repeated_mapping_diagnostics'] if len(x['case_ids'])>1]
 repeat={f:{'repeated_mapping_count':len(repeated),'changed':{key:[{'mapping_id':x['mapping_id'],'case_ids':x['case_ids'],'statuses':x['families'][f][key]} for x in repeated if len(x['families'][f][key])>1] for key in ('counterfactual','local','global')},'likely_unlikely_reversals':[x['mapping_id'] for x in repeated if {'likely','unlikely'}<=set(x['families'][f]['counterfactual'])]} for f in 'AB'}
 family={}
 for f in 'AB':
  raw=[values[(p['case_id'],f)] for p in primary];norm=[m.normalized(d,p) for d,p in zip(raw,primary)]
  family[f]={'overall_distribution':dict(Counter(x['overall'] for x in norm)),'confidence':dict(Counter(x['confidence'] for x in raw)),'decisive_criterion':dict(Counter(x['decisive_basis']['primary_criterion'] for x in raw)),'criterion_ties':{k:sum(x['criteria'][k]['relation']=='tie' for x in raw) for k in r.c.CRITERIA},'mapping_occurrence_scope':{k:dict(Counter(x['mapping_'+s]['scope'][k] for x in raw for s in 'AB')) for k in ('local_displacement','global_propagation')}}
 control={}
 for f in 'AB':
  rows=[x['families'][f] for x in metrics['orientation_controls']]
  control[f]={'overall':{'unchanged':sum(x['overall_unchanged'] for x in rows),'denominator':len(rows)},'criteria':{'unchanged':sum(sum(x['criteria_unchanged'].values()) for x in rows),'denominator':len(rows)*5},'mapping_diagnostics':{key:{'unchanged':sum(v[key] for x in rows for v in x['mapping_diagnostics'].values()),'denominator':len(rows)*2} for key in ('counterfactual_unchanged','local_unchanged','global_unchanged')}}
 coverage={}
 for tag in r.read(r.HERE/'design.json')['required_tags']:
  rows=[p for p in primary if tag in designs[(p['mapping_1'],p['mapping_2'])]['tags']]
  coverage[tag]={'case_ids':[p['case_id'] for p in rows],'agreement':m.agreement((r.c.normalize_relation(values[(p['case_id'],'A')]['overall_relation'],p),r.c.normalize_relation(values[(p['case_id'],'B')]['overall_relation'],p)) for p in rows)}
 historical=r.read(r.HERE/'review/historical-comparison.json');same_both=[x for x in historical if all(x['historical_classes'][f]['mapping_1']==x['historical_classes'][f]['mapping_2'] for f in 'AB')]
 resolved=[x['case_id'] for x in same_both if x['comparative_relations']['A']==x['comparative_relations']['B'] and x['comparative_relations']['A'].startswith('mapping_')]
 added_by_family={f:[x['case_id'] for x in historical if x['historical_classes'][f]['mapping_1']==x['historical_classes'][f]['mapping_2'] and x['comparative_relations']['A']==x['comparative_relations']['B'] and x['comparative_relations']['A'].startswith('mapping_')] for f in 'AB'}
 different_but_tie={f:[x['case_id'] for x in historical if x['historical_classes'][f]['mapping_1']!=x['historical_classes'][f]['mapping_2'] and x['comparative_relations'][f]=='tie'] for f in 'AB'}
 return {'families':family,'repeated_mapping_diagnostics':repeat,'orientation':control,'design_coverage':coverage,'historical':{'eligible_reused_pairs':len(historical),'direct_pairwise_agreement':m.agreement((x['comparative_relations']['A'],x['comparative_relations']['B']) for x in historical),'same_class_in_both_families':[x['case_id'] for x in same_both],'same_class_both_stable_direction':resolved,'same_class_family_stable_direction':added_by_family,'different_class_then_tie':different_but_tie},'interpretation':'Descriptive, dependent authored cases; coverage tags are operator intentions, not correctness labels.'}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('command',choices=['build','verify']);a=parser.parse_args();path=r.HERE/'review/diagnostics.json';value=compute()
 if a.command=='build':r.write_new(path,value)
 else:r.require(r.read(path)==value,'Diagnostic recomputation differs')
 print(a.command+': OK')
