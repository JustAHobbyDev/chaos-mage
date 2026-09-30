"""Mechanical partial-result metrics; absent measurements stay null."""
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner as r
import contracts as c

def compute():
    parents=c.read(r.HERE/'condition-inventory/parents.json'); atoms=c.read(r.HERE/'condition-inventory/atomic.json')
    partial=c.read(r.HERE/'taxonomy-partial-freeze.json'); manifest=c.read(r.HERE/'operator-manifest.json')
    taxonomy=[c.read(r.HERE/'taxonomy-judgments'/f'{v["identity"]}.json') for v in partial['runs']]
    old={f:Counter(c.read(p)['validity']['final_status'] for p in (r.HERE/'imports/historical-judgments').glob(f'*-{f}.json')) for f in 'AB'}
    bycase={x['case_id']:x for x in manifest['cases']}
    def group(rows):
        return {'mappings':len(rows),'fidelity_pass':sum(x['fidelity_pass'] for x in rows),'historical_Astra':dict(Counter(c.read(r.HERE/'imports/historical-judgments'/f'validity-{x["case_id"]}-A.json')['validity']['final_status'] for x in rows)),'prospective_statuses':None,'prospective_eligible':None}
    vals=[]
    for d in r.RUNTIME.rglob('validation.json'): vals.append(c.read(d))
    metadata=[v['metadata'] for v in vals if v['metadata']]
    return {'status':'incomplete','reason':'Historical preservation failure in preparation; stopped without retry or replacement.',
        'mapping_count':30,'historical_judgments':60,'parent_conditions':len(parents),'parents_by_historical_family':dict(Counter(x['original_family'] for x in parents)),
        'atomic_conditions':len(atoms),'atomic_by_historical_family':dict(Counter(next(p['original_family'] for p in parents if p['parent_condition_id']==a['parent_condition_id']) for a in atoms)),
        'authorized_workload':len(atoms)+32,'provider_calls':len(vals),'successful_taxonomy_probes':1,'taxonomy_completed':len(taxonomy),'taxonomy_unmeasured':len(atoms)-len(taxonomy),'taxonomy_partial_category_distribution':{x:sum(v['category']==x for v in taxonomy) for x in c.CATEGORIES},
        'taxonomy_full_distribution':None,'taxonomy_cross_model_agreement':None,'taxonomy_within_model_stability':None,
        'taxonomy_partial_mixed_uncertain':[x['condition_id'] for x in taxonomy if x['category'] in ('mixed','uncertain')],
        'prospective_probes':0,'prospective_completed':0,'prospective_unmeasured':30,'prospective_status_distribution':None,'execution_readiness_distribution':None,'prospective_condition_distribution':None,
        'historical_validity_distributions':{f:dict(old[f]) for f in 'AB'},'old_to_new_transition_matrix':None,'status_changes':None,'execution_only_rescues':None,'old_invalid_prospective_outcomes':None,'single_model_prospective_eligible_count':None,'reaches_18':None,'new_valid_valid_count':None,'cross_model_robustness':None,'within_model_stability':None,'existing_fidelity_pass':sum(x['fidelity_pass'] for x in bycase.values()),
        'generator_origins':{f:group([x for x in bycase.values() if x['generator_family']==f]) for f in 'AB'},
        'source_instruments':{s:group([x for x in bycase.values() if x['source_path']==s]) for s in sorted({x['source_path'] for x in bycase.values()})},
        'sessions':len({x['session_id'] for x in metadata}),'returned_model_identifiers':sorted({i for x in metadata for i in x['returned_model_identifiers']}),'verified_served_snapshot':None,'usage':{key:sum((u or {}).get(key,0) for x in metadata for u in x['usage']) for key in ('input_tokens','cached_input_tokens','output_tokens')},'observed_provider_transport_retries':sum(len(x['internal_transport_retry_events']) for x in metadata),'observed_formatter_retries':sum(x['formatting_retries']['observed_formatting_retries'] for x in metadata),'harness_retries':0,'replacement_measurements':0,'E_remains_stopped':True,'conceptual_usability':'Not established by this incomplete measurement.'}
if __name__=='__main__':
    import json
    print(json.dumps(compute(),indent=2))
