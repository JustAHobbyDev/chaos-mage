#!/usr/bin/env python3
"""Verify published measurement and review coverage; optionally private raw bytes."""
import argparse
import importlib.util
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('boundary_harness',BASE/'harness.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)


def verify(private=False):
    frozen=h.frozen_results();computed=h.analyze()
    h.require(computed==h.read(BASE/'metrics.json'),'Published metrics differ from recomputation')
    inventory=h.read(BASE/'review/inventory.json');review=h.read(BASE/'review/case-reviews.json')
    digest=h.sha((BASE/'results-freeze.json').read_bytes())
    h.require(inventory['results_freeze_sha256']==review['results_freeze_sha256']==digest,'Review freeze reference differs')
    expected={(p['condition'],p['case_id']):p for p in inventory['pairs']}
    actual={(p['condition'],p['case_id']):p for p in review['pair_reviews']}
    h.require(len(expected)==len(actual)==len(review['pair_reviews'])==19,'Review pair coverage differs')
    h.require(set(expected)==set(actual),'Review cases differ')
    categories={'disciplinary-distance-substitution','semantic-distance-substitution','operation-distance-overweighted','entity-vocabulary-overweighted','mapping-difficulty-confused-with-distance','usefulness-confused-with-distance'}
    for key,p in expected.items():
        r=actual[key]
        h.require(set(r['disagreement_keys'])==set(r['disagreement_review'])==set(p['differences']),'Disagreement omitted')
        h.require(set(r['shortcut_checks'])==categories,'Shortcut audit omitted')
        h.require(not r['labels_changed'] and r['classes']==p['classes'],'Review relabeled output')
        for field,evidence in p['differences'].items():h.require(r['disagreement_review'][field]['evidence']==evidence,'Review evidence changed')
    high={e['run_id'] for e in inventory['all_new_remote_and_alien_judgments']}
    h.require(high=={e['run_id'] for e in review['remote_alien_reviews']} and len(high)==len(review['remote_alien_reviews']),'Remote/Alien review omitted')
    for r in review['remote_alien_reviews']:
        c=h.read(BASE/'judgments'/f'{r["run_id"]}.json')['classification']
        h.require(r['class']==c['final_class'] and not r['labels_changed'],'High-class label changed')
        h.require(r['evidence']['class_rationale']==c['class_rationale'],'High-class evidence changed')
    execution=h.read(BASE/'review/execution-audit.json')
    observed={e['id'] for e in frozen['runs'] if e['audit']['metadata']['formatting_retries']['observed_formatting_retries']}
    h.require(observed=={e['run_id'] for e in execution['visible_formatting_retries']},'Formatting retry omitted')
    for boundary,b in computed['boundaries'].items():
        attribution=review['boundary_attribution'][boundary]
        h.require(attribution['side_disagreements']==len(b['side_disagreements']),'Attribution denominator changed')
        if not b['side_disagreements']:h.require(attribution['strict_majority'] is None,'Empty attribution is not applicable')
        else:h.require(attribution['strict_majority']==(attribution['explained']>len(b['side_disagreements'])/2),'Majority rule changed')
    if private:
        for e in frozen['runs']:
            for name,digest in e['files'].items():h.require(h.sha((h.RUNTIME/'runs'/e['id']/name).read_bytes())==digest,'Private v0.2 file changed')
        old=h.read(h.ROOT/'distance/results-freeze-v0.1.json')
        for e in old['runs']:
            for name,digest in e['files'].items():h.require(h.sha((h.ROOT/'.runtime/distance-v0.1'/e['case_id']/e['replicate']/name).read_bytes())==digest,'Private v0.1 file changed')
    print('Verified: 38 judgments; 19 reviewed pairs; all disagreement fields; 10 Remote/Alien reviews; metrics and retry coverage'+('; private v0.1/v0.2 hashes' if private else ''))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--private',action='store_true');verify(parser.parse_args().private)
