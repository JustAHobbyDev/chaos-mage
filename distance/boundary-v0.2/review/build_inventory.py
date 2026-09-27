#!/usr/bin/env python3
"""Build review evidence only AFTER all results are frozen and published.

This inventories disagreements without labeling outputs correct/incorrect.
Research interpretations belong in separate case-review records.
"""
import importlib.util
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('boundary_harness',BASE/'harness.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)


def build():
    manifest=h.frozen_results()
    h.analyze()  # Verifies all published payload hashes and fixed denominators.
    judgments={e['id']:h.read(BASE/'judgments'/f'{e["id"]}.json')['classification'] for e in manifest['runs']}
    pairs=[]
    for condition,ids in [('primary',[f'{n:03}' for n in range(1,17)]),('control',['001','003','009'])]:
        for cid in ids:
            run_ids=[f'{condition}-{cid}-{family}' for family in ('A','B')]
            a,b=[judgments[rid] for rid in run_ids]
            differences={}
            if a['final_class']!=b['final_class']:
                differences['final_class']={f:{'value':c['final_class'],'rationale':c['class_rationale']} for f,c in zip(('A','B'),(a,b))}
            for d in h.DIMS:
                if a['displacement'][d]['level']!=b['displacement'][d]['level']:
                    differences[f'dimension.{d}']={f:c['displacement'][d] for f,c in zip(('A','B'),(a,b))}
            if a['naturalization']['status']!=b['naturalization']['status']:
                differences['naturalization']={f:c['naturalization'] for f,c in zip(('A','B'),(a,b))}
            if condition=='primary':
                for axis,key in [('displacement','level'),('grounding','status')]:
                    if a['axes'][axis][key]!=b['axes'][axis][key]:
                        differences[f'axis.{axis}']={f:c['axes'][axis] for f,c in zip(('A','B'),(a,b))}
            boundary=h.read(BASE/'operator-manifest.json')['cases'][cid]['boundary']
            pairs.append({'condition':condition,'case_id':cid,'run_ids':run_ids,'boundary_group':boundary,'classes':[a['final_class'],b['final_class']],'side_disagreement':h.side(a['final_class'],boundary)!=h.side(b['final_class'],boundary),'differences':differences,'uncertainty':{f:c['uncertainty'] for f,c in zip(('A','B'),(a,b))}})
    high_classes=[]
    for rid,c in judgments.items():
        if c['final_class'] not in ('Remote','Alien'):continue
        high_classes.append({'run_id':rid,'class':c['final_class'],'class_rationale':c['class_rationale'],'axes':c.get('axes'),'boundary_evidence':c.get('boundary_evidence'),'source_transfer_profile':c['source_transfer_profile'],'uncertainty':c['uncertainty'],'required_review':'Identify a substantive non-native change' if c['final_class']=='Remote' else 'Identify an essential independently unjustified counterpart and high reorganization'})
    return {'results_freeze_sha256':h.sha((BASE/'results-freeze.json').read_bytes()),'pair_count':len(pairs),'pairs':pairs,'all_new_remote_and_alien_judgments':high_classes,'note':'Mechanical inventory only. No automatic adjudication; human/agent research interpretations are separate.'}

if __name__=='__main__':
    value=build();h.write_new(BASE/'review/inventory.json',value)
    print(f'Inventory: {len(value["pairs"])} pairs, {len(value["all_new_remote_and_alien_judgments"])} Remote/Alien judgments')
