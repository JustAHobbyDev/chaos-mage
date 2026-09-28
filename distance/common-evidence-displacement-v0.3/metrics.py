"""Recomputable descriptive relations; no scalar ranking or inferred edges."""
from collections import Counter, defaultdict
import contracts as c

def agreement(rows):
    rows=list(rows);n=len(rows);a=sum(x==y for x,y in rows)
    return {'agreements':a,'denominator':n,'rate':a/n if n else None}
def dominant(x):return x in ('mapping_1_dominates','mapping_2_dominates')
def normalized(value,pair):
    return {'overall':c.normalize(value['overall_relation'],pair),'meaningful_difference':value['meaningful_difference']['status'],
            'criteria':{k:c.normalize(value['criteria'][k]['relation'],pair) for k in c.CRITERIA},
            'diagnostics':{k:c.normalize(value['consequence_structure'][k]['relation'],pair) for k in c.DIAGNOSTICS},'confidence':value['confidence']}
def disagreement(a,b):
    if a==b:return 'agreement'
    if 'insufficient_information' in (a,b):return 'relation-vs-insufficient_information'
    if dominant(a) and dominant(b):return 'opposite-dominance'
    values={a,b}
    if 'tradeoff' in values and 'approximately_equal' in values:return 'tradeoff-vs-approximately_equal'
    return 'dominance-vs-'+('tradeoff' if 'tradeoff' in values else 'approximately_equal')
def transition(a,b):
    if a==b:return 'stable'
    if dominant(a) and dominant(b):return 'direction-reversal'
    if a=='approximately_equal' and dominant(b):return 'strengthened'
    if dominant(a) and b=='approximately_equal':return 'weakened'
    if b=='tradeoff' and (dominant(a) or a=='approximately_equal'):return 'changed-to-tradeoff'
    if a=='tradeoff' and dominant(b):return 'tradeoff-resolved'
    return 'other'
def category(rows,label):
    rows=list(rows);both=sum(a==b==label for a,b in rows);either=sum(label in (a,b) for a,b in rows)
    return {'family_A':sum(a==label for a,b in rows),'family_B':sum(b==label for a,b in rows),'both':both,'either':either,
            'positive_agreement':{'agreements':both,'denominator':either,'rate':both/either if either else None},
            'binary_agreement':agreement((a==label,b==label) for a,b in rows)}
def graph(rows,values,family,triangle_targets):
    result=[]
    for target in sorted({p['target_id'] for p in rows}):
        pairs=[p for p in rows if p['target_id']==target];edges=[];relations={};adj=defaultdict(set)
        for p in pairs:
            rel=normalized(values[(p['case_id'],family)],p)['overall'];relations[(p['mapping_1'],p['mapping_2'])]=rel
            if dominant(rel):
                a,b=(p['mapping_1'],p['mapping_2']) if rel=='mapping_1_dominates' else (p['mapping_2'],p['mapping_1'])
                edges.append([a,b]);adj[a].add(b)
        nodes=sorted({n for p in pairs for n in (p['mapping_1'],p['mapping_2'])});cycles=set();chains=set()
        def visit(path):
            if len(path)>1:chains.add(tuple(path))
            for nxt in sorted(adj[path[-1]]):
                if nxt==path[0] and len(path)>=3:cycles.add(min(tuple(path[i:]+path[:i]) for i in range(len(path))))
                elif nxt not in path:visit(path+[nxt])
        for n in nodes:visit([n])
        eligible=target in triangle_targets and len(pairs)==3 and len(nodes)==3
        closure=[]
        if eligible:
            for chain in sorted(chains):
                if len(chain)!=3:continue
                a,_,b=chain;k=tuple(sorted((a,b)));rel=relations[k]
                expected='mapping_1_dominates' if a==k[0] else 'mapping_2_dominates'
                status='supported' if rel==expected else 'cycle' if dominant(rel) else 'unresolved' if rel=='insufficient_information' else 'transitivity-tension'
                closure.append({'chain':list(chain),'closure':rel,'status':status})
        counts=Counter(relations.values());n=len(pairs)
        result.append({'target_id':target,'measured_pairs':n,'dominance_edges':sorted(edges),'dominance_chains':[list(x) for x in sorted(chains)],
                       'cycle_evidence_eligible':eligible,'directed_cycles':[list(x) for x in sorted(cycles)] if eligible else None,
                       'cycle_evidence_limit':None if eligible else 'No complete preregistered triangle; structurally uninformative.',
                       'chain_closures':closure,'tradeoff_density':counts['tradeoff']/n,'approximately_equal_density':counts['approximately_equal']/n})
    return result
def stage_metrics(values,pairs,triangle_targets):
    primary=[p for p in pairs if p['cohort']=='primary'];controls=[p for p in pairs if p['cohort']!='primary']
    expected={(p['case_id'],f) for p in pairs for f in 'AB'}
    c.require(set(values)==expected,'Incomplete or unexpected measurements; do not shrink denominator')
    rows=[(p,{f:normalized(values[(p['case_id'],f)],p) for f in 'AB'}) for p in primary]
    relations=[(v['A']['overall'],v['B']['overall']) for _,v in rows]
    directional=[(a,b) for a,b in relations if dominant(a) and dominant(b)]
    confusion={a:{b:0 for b in c.RELATIONS} for a in c.RELATIONS}
    for a,b in relations:confusion[a][b]+=1
    byid={p['case_id']:p for p in pairs};reversals=[]
    for p in controls:
        original=byid[p['control_of']];families={}
        for f in 'AB':
            a=normalized(values[(original['case_id'],f)],original);b=normalized(values[(p['case_id'],f)],p)
            families[f]={'original':a,'reversed':b,'overall_unchanged':a['overall']==b['overall'],
                         'meaningful_difference_unchanged':a['meaningful_difference']==b['meaningful_difference'],
                         'criteria_unchanged':{k:a['criteria'][k]==b['criteria'][k] for k in c.CRITERIA},
                         'diagnostics_unchanged':{k:a['diagnostics'][k]==b['diagnostics'][k] for k in c.DIAGNOSTICS}}
        reversals.append({'case_id':p['case_id'],'control_of':p['control_of'],'families':families})
    return {'primary_pairs':len(primary),'overall_agreement':agreement(relations),'confusion_rows_A_columns_B':confusion,
       'relation_frequencies':{f:dict(Counter(v[f]['overall'] for _,v in rows)) for f in 'AB'},
       'dominance_direction':{'same':sum(a==b for a,b in directional),'opposite':sum(a!=b for a,b in directional),'denominator':len(directional)},
       'tradeoff':category(relations,'tradeoff'),'approximately_equal':category(relations,'approximately_equal'),
       'meaningful_difference_agreement':agreement((v['A']['meaningful_difference'],v['B']['meaningful_difference']) for _,v in rows),
       'meaningful_difference_frequencies':{f:dict(Counter(v[f]['meaningful_difference'] for _,v in rows)) for f in 'AB'},
       'criterion_agreement':{k:agreement((v['A']['criteria'][k],v['B']['criteria'][k]) for _,v in rows) for k in c.CRITERIA},
       'diagnostic_agreement':{k:agreement((v['A']['diagnostics'][k],v['B']['diagnostics'][k]) for _,v in rows) for k in c.DIAGNOSTICS},
       'confidence_agreement':agreement((v['A']['confidence'],v['B']['confidence']) for _,v in rows),
       'disagreements':dict(Counter(disagreement(a,b) for a,b in relations)),
       'pair_inventory':[{'case_id':p['case_id'],'target_id':p['target_id'],'mapping_1':p['mapping_1'],'mapping_2':p['mapping_2'],
                          'families':v,'category':disagreement(v['A']['overall'],v['B']['overall'])} for p,v in rows],
       'graphs':{f:graph(primary,values,f,triangle_targets) for f in 'AB'},'orientation_controls':reversals,
       'orientation_summary':{f:{'unchanged':sum(r['families'][f]['overall_unchanged'] for r in reversals),'denominator':len(reversals)} for f in 'AB'}}
def calculate(stages,pairs):
    targets=c.read(c.HERE/'design.json')['triangle_targets'];transitions={}
    for f in 'AB':
        rows=[];matrix={a:{b:0 for b in c.RELATIONS} for a in c.RELATIONS}
        for p in pairs:
            if p['cohort']!='primary':continue
            a,b=[normalized(stages[s][(p['case_id'],f)],p) for s in ('prospective','consequence')]
            matrix[a['overall']][b['overall']]+=1
            rows.append({'case_id':p['case_id'],'prospective':a['overall'],'consequence':b['overall'],'transition':transition(a['overall'],b['overall']),
                         'confidence':{'prospective':a['confidence'],'consequence':b['confidence']}})
        transitions[f]={'counts':dict(Counter(r['transition'] for r in rows)),'matrix':matrix,'pairs':rows}
    return {'stages':{s:stage_metrics(v,pairs,targets) for s,v in stages.items()},'transitions':transitions,
            'interpretation':'Descriptive independent measures; no composite, accuracy, total ranking, or success percentage.'}
