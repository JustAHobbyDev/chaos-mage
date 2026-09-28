"""Post-freeze independent inventories and exact common-state proof."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner as r

def identity_relation(value,pair):
    rel=value['overall_relation']
    return pair['mapping_'+rel[0]] if rel in ('A_dominates','B_dominates') else rel

def calculate():
    for stage in ('prospective','consequence'):r.frozen(stage,True)
    pairs=r.pair_records();primary=[p for p in pairs if p['cohort']=='primary'];maps={m['mapping_id']:m for m in r.manifest()}
    proof=[]
    for p in pairs:
        a,b=[json.loads(r.candidate(p['mapping_'+s])['target']['evidence'][0]) for s in 'AB']
        hashes={}
        components={**{k:(a[k],b[k]) for k in ('target','native_baseline','investigation_budget')},
                    **{k:(a['shared_state'][k],b['shared_state'][k]) for k in ('facts','artifacts','initial_observations','known_uncertainties','available_affordances','constraints')}}
        for key,(left,right) in components.items():
            lb,rb=r.c.serialized(left),r.c.serialized(right);r.require(lb==rb,'Unequal component '+key);hashes[key]=r.sha(lb)
        common=(r.HERE/'common-states'/f'{p["target_id"]}.json').read_bytes()
        for stage in ('prospective','consequence'):
            raw=(r.HERE/'packets'/stage/f'{p["case_id"]}.txt').read_bytes();r.require(common in raw,'Missing common bytes')
        proof.append({'case_id':p['case_id'],'target_id':p['target_id'],'world_id':p['world_id'],'common_state_sha256':r.sha(common),'equal_component_hashes':hashes})
    stages={};raws={}
    for stage in ('prospective','consequence'):
        values=r.published(stage);raws[stage]=values
        same=0;opposites=[];both_dom=0;reversals=[];changes={'criteria':{f:0 for f in 'AB'},'diagnostics':{f:0 for f in 'AB'}}
        for p in primary:
            a,b=[identity_relation(values[(p['case_id'],f)],p) for f in 'AB'];same+=a==b
            if a.startswith('M') and b.startswith('M'):
                both_dom+=1
                if a!=b:opposites.append(p['case_id'])
        by={p['case_id']:p for p in pairs}
        for p in pairs:
            if p['cohort']=='primary':continue
            original=by[p['control_of']]
            for f in 'AB':
                a,b=values[(original['case_id'],f)],values[(p['case_id'],f)]
                if identity_relation(a,original)!=identity_relation(b,p):reversals.append({'family':f,'primary':original['case_id'],'reversal':p['case_id']})
                for section,keys,label in [('criteria',r.c.CRITERIA,'criteria'),('consequence_structure',r.c.DIAGNOSTICS,'diagnostics')]:
                    for k in keys:
                        def normal(v,q):
                            rel=v[section][k]['relation'];return q['mapping_'+rel] if rel in ('A','B') else rel
                        changes[label][f]+=normal(a,original)!=normal(b,p)
        stages[stage]={'independent_overall_agreement':{'agreements':same,'denominator':len(primary)},'joint_dominance_pairs':both_dom,
                       'opposite_dominance_cases':opposites,'orientation_changes':reversals,'orientation_field_changes':changes}
    occurrence=Counter(mid for p in primary for mid in (p['mapping_1'],p['mapping_2']))
    source_same=sum(maps[p['mapping_1']]['source_path']==maps[p['mapping_2']]['source_path'] for p in primary)
    return {'shared_state_proof':proof,'stages':stages,'coverage':{'planned_targets':8,'measured_targets':sorted({p['target_id'] for p in primary}),
       'planned_pairs':16,'primary_pairs':len(primary),'orientation_controls':len(pairs)-len(primary),
       'admitted_mappings':sum(x['admitted'] for x in r.read(r.HERE/'admission.json')['mappings']),'measured_unique_mappings':len(occurrence),
       'repeated_mapping_ids':sorted(k for k,v in occurrence.items() if v>1),'same_source_pairs':source_same,'different_source_pairs':len(primary)-source_same,
       'complete_triangle_targets':[t for t in r.read(r.HERE/'design.json')['triangle_targets'] if sum(p['target_id']==t for p in primary)==3],
       'controls_targets':sorted({p['target_id'] for p in pairs if p['cohort']!='primary'})}}

def verify():
    expected=calculate();r.require(r.read(r.HERE/'review/diagnostics.json')==expected,'Diagnostics drift')
    metrics=r.read(r.HERE/'metrics.json')
    for stage,d in expected['stages'].items():
        a=metrics['stages'][stage]['overall_agreement'];r.require({k:a[k] for k in ('agreements','denominator')}==d['independent_overall_agreement'],'Independent agreement mismatch')
    return expected['coverage']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['build','verify']);a=p.parse_args()
    if a.command=='build':r.write_new(r.HERE/'review/diagnostics.json',calculate())
    else:print(verify())
