"""Descriptive pair metrics without scores or inferred missing edges."""
from collections import Counter,defaultdict
from itertools import combinations
import contracts as c

def agreement(pairs):
 pairs=list(pairs);n=len(pairs);a=sum(x==y for x,y in pairs)
 return {'agreements':a,'denominator':n,'rate':a/n if n else None}
def normalized(value,pair):
 return {'overall':c.normalize_relation(value['overall_relation'],pair),'criteria':{k:c.normalize_relation(value['criteria'][k]['relation'],pair,True) for k in c.CRITERIA},'mappings':{mid:value[c.mapping_slot(pair,mid)] for mid in (pair['mapping_1'],pair['mapping_2'])},'primary_criterion':value['decisive_basis']['primary_criterion'],'confidence':value['confidence']}
def post_status(a,b,compatible=True):
 x,y=a['overall'],b['overall']
 if 'indeterminate' in (x,y):return 'indeterminate'
 if x==y=='tie':return 'stable-tie'
 if 'tie' in (x,y):return 'order-vs-tie'
 if x!=y:return 'contested-direction'
 if 'close' in (a['confidence'],b['confidence']) or a['primary_criterion']!=b['primary_criterion'] or not compatible:return 'close-order'
 return 'stable-order'
def triangle_status(edges):
 # edges keyed by ascending mapping identities, values normalized to those identities.
 if 'indeterminate' in edges.values():return 'indeterminate',False
 vertices=sorted({v for pair in edges for v in pair})
 out=Counter();arcs=[]
 for (a,b),rel in edges.items():
  if rel=='tie':continue
  winner,loser=(a,b) if rel=='mapping_1_more' else (b,a);out[winner]+=1;arcs.append((winner,loser))
 if 'tie' not in edges.values():return ('cycle' if all(out[v]==1 for v in vertices) else 'transitive'),False
 # Ties are descriptive tolerance, not asserted equality. List weak-order tensions.
 ties=[pair for pair,rel in edges.items() if rel=='tie'];tension=len(ties)==2
 if len(ties)==1:
  a,b=ties[0];z=next(v for v in vertices if v not in (a,b))
  tension=((a,z) in arcs)!=((b,z) in arcs)
 return 'tie-compatible',tension
def cycles(arcs):
 adj=defaultdict(set)
 for a,b in arcs:adj[a].add(b)
 found=set()
 def walk(path):
  for nxt in sorted(adj[path[-1]]):
   if nxt==path[0] and len(path)>=3:
    rotations=[tuple(path[i:]+path[:i]) for i in range(len(path))];found.add(min(rotations))
   elif nxt not in path:walk(path+[nxt])
 for node in sorted(list(adj)):walk([node])
 return [list(p) for p in sorted(found)]
def transitivity(rows,values):
 output={}
 for family in 'AB':
  triangles=[];graphs=[]
  for target in sorted({p['target_id'] for p in rows}):
   edges={(p['mapping_1'],p['mapping_2']):c.normalize_relation(values[(p['case_id'],family)]['overall_relation'],p) for p in rows if p['target_id']==target and (p['case_id'],family) in values}
   nodes=sorted({n for pair in edges for n in pair});arcs=[]
   for (a,b),rel in edges.items():
    if rel in ('mapping_1_more','mapping_2_more'):arcs.append((a,b) if rel=='mapping_1_more' else (b,a))
   for tri in combinations(nodes,3):
    pairs=list(combinations(tri,2))
    if not all(p in edges for p in pairs):continue
    subset={p:edges[p] for p in pairs};status,tension=triangle_status(subset)
    triangles.append({'target_id':target,'mappings':list(tri),'status':status,'tie_substitution_tension':tension,'edges':[{'mapping_1':p[0],'mapping_2':p[1],'relation':edges[p]} for p in pairs]})
   graphs.append({'target_id':target,'measured_edges':len(edges),'directed_cycles':cycles(arcs)})
  output[family]={'triangles':triangles,'counts':dict(Counter(t['status'] for t in triangles)),'tie_substitution_tensions':sum(t['tie_substitution_tension'] for t in triangles),'graphs':graphs}
 return output
def calculate(values,pairs):
 primary=[p for p in pairs if p['cohort']=='primary'];controls=[p for p in pairs if p['cohort']=='orientation-control'];observed=[];missing=[]
 for p in primary:
  if all((p['case_id'],f) in values for f in 'AB'):observed.append((p,{f:normalized(values[(p['case_id'],f)],p) for f in 'AB'}))
  else:missing.append(p['case_id'])
 confusion={a:{b:0 for b in c.RELATIONS} for a in c.RELATIONS};direction=Counter();ties=Counter();ind=Counter();occ=[];inventory=[]
 for p,v in observed:
  a,b=v['A']['overall'],v['B']['overall'];confusion[a][b]+=1
  if a.startswith('mapping_') and b.startswith('mapping_'):direction['same' if a==b else 'opposite']+=1
  if a==b=='tie':ties['tie_vs_tie']+=1
  if (a=='tie' and b.startswith('mapping_')) or (b=='tie' and a.startswith('mapping_')):ties['direction_vs_tie']+=1
  if 'indeterminate' in (a,b):ind[a+' / '+b]+=1
  inventory.append({'case_id':p['case_id'],'target_id':p['target_id'],'mapping_1':p['mapping_1'],'mapping_2':p['mapping_2'],'A':a,'B':b,'default_review_status':post_status(v['A'],v['B']),'primary_criteria':{f:v[f]['primary_criterion'] for f in 'AB'},'confidence':{f:v[f]['confidence'] for f in 'AB'}})
  for mid in (p['mapping_1'],p['mapping_2']):occ.append({'case_id':p['case_id'],'mapping_id':mid,**{f:v[f]['mappings'][mid] for f in 'AB'}})
 repeated=[]
 for mid in sorted({o['mapping_id'] for o in occ}):
  cases=[o for o in occ if o['mapping_id']==mid]
  repeated.append({'mapping_id':mid,'case_ids':[o['case_id'] for o in cases],'families':{f:{'counterfactual':dict(Counter(o[f]['counterfactual_native']['status'] for o in cases)),'local':dict(Counter(o[f]['scope']['local_displacement'] for o in cases)),'global':dict(Counter(o[f]['scope']['global_propagation'] for o in cases))} for f in 'AB'}})
 reversed_results=[];lookup={p['case_id']:p for p in pairs}
 for p in controls:
  original=lookup[p['control_of']];families={}
  for f in 'AB':
   if (p['case_id'],f) not in values or (original['case_id'],f) not in values:families[f]=None;continue
   a=normalized(values[(original['case_id'],f)],original);b=normalized(values[(p['case_id'],f)],p)
   families[f]={'original':a['overall'],'reversed':b['overall'],'overall_unchanged':a['overall']==b['overall'],'criteria_unchanged':{k:a['criteria'][k]==b['criteria'][k] for k in c.CRITERIA},'mapping_diagnostics':{mid:{'counterfactual_unchanged':a['mappings'][mid]['counterfactual_native']['status']==b['mappings'][mid]['counterfactual_native']['status'],'local_unchanged':a['mappings'][mid]['scope']['local_displacement']==b['mappings'][mid]['scope']['local_displacement'],'global_unchanged':a['mappings'][mid]['scope']['global_propagation']==b['mappings'][mid]['scope']['global_propagation']} for mid in (p['mapping_1'],p['mapping_2'])}}
  reversed_results.append({'case_id':p['case_id'],'control_of':p['control_of'],'families':families})
 return {'planned_primary_pairs':len(primary),'observed_primary_pairs':len(observed),'missing_pair_ids':missing,'overall_agreement':agreement((v['A']['overall'],v['B']['overall']) for _,v in observed),'confusion_rows_A_columns_B':confusion,'directional':{'same':direction['same'],'opposite':direction['opposite'],'denominator':sum(direction.values())},'ties':{'direction_vs_tie':ties['direction_vs_tie'],'tie_vs_tie':ties['tie_vs_tie']},'indeterminate_combinations':dict(ind),'criterion_agreement':{k:agreement((v['A']['criteria'][k],v['B']['criteria'][k]) for _,v in observed) for k in c.CRITERIA},'counterfactual_agreement':agreement((o['A']['counterfactual_native']['status'],o['B']['counterfactual_native']['status']) for o in occ),'scope_agreement':{k:agreement((o['A']['scope'][k],o['B']['scope'][k]) for o in occ) for k in ('local_displacement','global_propagation')},'decisive_criterion_agreement':agreement((v['A']['primary_criterion'],v['B']['primary_criterion']) for _,v in observed),'pair_inventory':inventory,'mapping_occurrences':occ,'repeated_mapping_diagnostics':repeated,'transitivity':transitivity(primary,values),'orientation_controls':reversed_results,'orientation_summary':{f:{'unchanged':sum(x['families'][f]['overall_unchanged'] for x in reversed_results if x['families'][f] is not None),'observed':sum(x['families'][f] is not None for x in reversed_results),'planned':len(controls)} for f in 'AB'}}
