"""Read-only H.6 count recomputation; output destination explicitly supplied."""
from collections import Counter
import json
from pathlib import Path
import sys
import contracts as c
H=Path(__file__).resolve().parent

def read(p):return json.loads(p.read_text())
def counts(values,universe=()):
    out={key:0 for key in universe};out.update(Counter(values));return out

def compute():
    stages=['generation','claims','claim-judgments','remainder-inventory','artifact-judgments']
    values={s:{p.stem:read(p) for p in sorted((H/s).glob('*.json'))} for s in stages}
    claim_status=['SUPPORTED','CONDITIONAL_WARRANT','UNSUPPORTED','UNCERTAIN']
    kinds=['POSITIVE_INFERENCE','TARGET_CONSTRAINT','INQUIRY_CONSTRAINT','INSUFFICIENCY_ONLY','UNCERTAIN']
    statuses=['KEEP_WITH_WARRANT_FLAGS','KEEP_WITH_REDUCED_SCOPE','CORE_INVALID','UNCERTAIN_LOAD_BEARING']
    prov={};prov_issues=[];anomalies=[];diagnostics=[]
    for s,rows in values.items():
        comps=[]
        for cid,v in rows.items():
            for item in c.components(v):
                if item['value']=='NOT_APPLICABLE' and not item['provenance']['refs']:continue
                comps.append(item)
                if item['provenance']['support_status']!='SUFFICIENT':prov_issues.append({'stage':s,'id':cid,'component':item})
            anomalies.extend({'stage':s,'id':cid,**a} for a in v.get('anomalies',[]))
        prov[s]=counts([x['provenance']['support_status'] for x in comps],['SUFFICIENT','INSUFFICIENT','UNCERTAIN'])
        for p in (H/'raw'/s).glob('*/validation.json'):
            diagnostics.extend({'stage':s,'id':p.parent.name,**d} for d in read(p)['diagnostics'])
    candidates=[x for v in values['remainder-inventory'].values() for x in v['candidates']]
    units=[x for v in values['remainder-inventory'].values() for x in v['inquiry_units']]
    rows=[]
    for cid in read(H/'manifest.json')['packet_order']:
        js=[j for k,j in values['claim-judgments'].items() if k.startswith(cid+'--')]
        atoms=values['claims'].get(cid,{}).get('claims',[])
        inventory=values['remainder-inventory'].get(cid,{})
        cs=inventory.get('candidates',[])
        audit=H/'instrumentation'/f'{cid}.json'
        rows.append({'packet_id':cid,'generation_parsed':cid in values['generation'],'atomic_claims':len(atoms),
                     'claim_statuses':counts([j['status'] for j in js],claim_status),
                     'unsupported_claims_observed':sum(j['status']=='UNSUPPORTED' for j in js),
                     'claims_deleted':len(read(H/'ablations'/f'{cid}.json')['deleted_claim_ids']) if (H/'ablations'/f'{cid}.json').exists() else None,
                     'remainder_candidates':len(cs),'candidate_kinds':counts([x['kind'] for x in cs],kinds),
                     'productive':counts([x['viability']['productive']['value'] for x in cs],['YES','NO','UNCERTAIN']),
                     'scientific_status':values['artifact-judgments'].get(cid,{}).get('scientific_status'),
                     'instrumentation_status':read(audit)['instrumentation_status'] if audit.exists() else 'NOT_REVIEWED'})
    reservations=[read(p) for p in (H/'raw').glob('*/*/reservation.json')]
    collision_review=H/'review/collision-contexts.json'
    contexts=read(collision_review)['contexts'] if collision_review.exists() else []
    instrumentation=[read(p) for p in (H/'instrumentation').glob('*.json')]
    partial=read(H/'claim-judgments-partial-freeze.json') if (H/'claim-judgments-partial-freeze.json').exists() else None
    return {'measurement_status':'TERMINATED_MEASUREMENT_INCOMPLETE' if partial else 'COMPLETE',
            'planned_generations':18,'completed_calls_by_stage':{s:len(v) for s,v in values.items()},
            'failed_provider_calls':len(partial['failed_provider_observations']) if partial else 0,
            'reserved_but_unlaunched':len(partial['reserved_but_unlaunched']) if partial else 0,
            'never_reserved_claim_judgments':len(partial['never_reserved']) if partial else 0,
            'unmeasured_claim_judgments':1042-len(values['claim-judgments']) if partial else 0,
            'end_to_end_mappings_complete':len(values['artifact-judgments']),
            'unassessed_artifacts':18-len(values['artifact-judgments']),
            'unassessed_full_pipeline_instrumentation':18-len(instrumentation),
            'downstream_zero_count_meaning':'Not measured, not evidence of absence' if partial else 'Observed counts',
            'parsed_mappings':len(values['generation']),'atomic_claims':sum(len(v['claims']) for v in values['claims'].values()),
            'claim_statuses':counts([v['status'] for v in values['claim-judgments'].values()],claim_status),
            'remainder_candidates':len(candidates),'candidate_kinds':counts([x['kind'] for x in candidates],kinds),
            'productive':counts([x['viability']['productive']['value'] for x in candidates],['YES','NO','UNCERTAIN']),
            'inquiry_units_enumerated':len(units),'inquiry_units_complete':sum(x['complete'] for x in units),
            'artifact_statuses':counts([v['scientific_status'] for v in values['artifact-judgments'].values()],statuses),
            'provenance_by_stage':prov,'provenance_total_component_assessments':{s:sum(v[s] for v in prov.values()) for s in ['SUFFICIENT','INSUFFICIENT','UNCERTAIN']},
            'all_provenance_insufficiencies_and_uncertainties':prov_issues,
            'all_model_reported_anomalies':anomalies,'all_mechanical_and_relational_diagnostics':diagnostics,
            'instrumentation_statuses':counts([v['instrumentation_status'] for v in instrumentation],['CLEAN','WARNING','FAILURE']),
            'h5_observed_signals':counts([s for v in instrumentation for s in v.get('h5_signals',[])]),
            'packet_collision_exposure_contexts':sum(v['collision_exposure'] for v in reservations)+sum(v['exposure'] for v in contexts),
            'packet_collision_failure_contexts':sum(v.get('failure',False) for v in contexts),
            'per_mapping':rows,'provenance_count_note':'Component assessment occurrences by stage, not unique propositions; NOT_APPLICABLE empty components excluded. Scientific warrant and provenance support are separate.'}
if __name__=='__main__':
    result=compute()
    if len(sys.argv)>1:
        with Path(sys.argv[1]).open('x') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
    else:print(json.dumps(result,indent=2,ensure_ascii=False))
