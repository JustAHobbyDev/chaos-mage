"""Offline counts from preserved observations; does not create model judgments."""
from collections import Counter
import continuation


def summarize(r):
    rows=[];contracts=Counter();watch=[];all_judgments={}
    for p in (r.H/'evaluation').glob('*.json'):
        j=r.read(p);contracts[j['contract']+':'+j['verdict']]+=1;all_judgments[p.stem]=j
    quarantine=continuation.quarantined(r)
    for cid in r.order():
        item={'mapping_id':cid,'scientific_admission':'UNMEASURED' if cid in quarantine else 'PENDING',
              'instrumentation':'FAILURE' if cid in quarantine else 'PENDING','end_to_end_complete':False,
              'local_violated_claims':None,'viable_candidates':None,'ablation':None}
        if cid in quarantine:
            item['reason']=r.read(r.H/'review/continuation-evidence.json')['provider_no_observation'] if cid==continuation.AFFECTED else r.read(r.H/'review/quarantines'/f'{cid}.json')
        ap=r.H/'artifact-judgments'/f'{cid}.json'
        if ap.exists() and cid not in quarantine:
            a=r.read(ap);item.update(scientific_admission=a['scientific_status'],instrumentation='WARNING' if a['anomalies'] else 'CLEAN',end_to_end_complete=True)
            inv=r.read(r.H/'remainder-inventory'/f'{cid}.json');abl=r.read(r.H/'ablations'/f'{cid}.json')
            if inv['anomalies']:item['instrumentation']='WARNING'
            item['local_violated_claims']=abl['deleted_claim_ids'];item['ablation']=abl
            item['viable_candidates']=[c for c in inv['candidates'] if all(d['value']=='YES' for d in c['viability'].values())]
            item['remainder_inventory']=inv;item['artifact_judgment']=a
        ip=r.H/'obligations'/f'{cid}.json'
        # A quarantined discovery may still establish watch routing, but not verdicts.
        if not ip.exists() and cid=='H7-T01-1':ip=r.H/'review/partial-routing-inventory.json'
        if ip.exists():
            for w in r.read(ip)['supplied_operation_watch']:
                w=dict(w);w['mapping_id']=cid
                component=w.get('referenced_claim_id', '')+'-B' if w.get('referenced_claim_id') else w['component_id']
                js=[j for uid,j in all_judgments.items() if uid.startswith(cid+'--'+component+'-')]
                w['fidelity_verdict']={j['contract']:j['verdict'] for j in js if j['contract'] in ('TARGET_FIDELITY','SOURCE_FIDELITY')}
                op=[j['verdict'] for j in js if j['contract']=='OPERATION_LICENSE']
                w['operation_license_verdict']=op[0] if len(op)==1 else None
                w['admission_effect']='UNMEASURED' if cid in quarantine else ('MAPPING_USE_REMOVED' if op==['VIOLATED'] else 'RETAINED_WITH_FLAGS' if op else 'PENDING')
                watch.append(w)
        rows.append(item)
    complete=sum(x['end_to_end_complete'] for x in rows);unmeasured=len(quarantine)
    finished=complete+unmeasured==6
    attempts=list((r.RT/'attempts').glob('*/*/attempt.json'))
    tokens=Counter();successes=0
    for p in (r.RT/'attempts').glob('*/*/validation.json'):
        successes+=1
        for u in r.read(p)['metadata']['usage']:
            if u:tokens.update({k:v for k,v in u.items() if isinstance(v,int)})
    noobs=[r.read(r.H/'review/continuation-evidence.json')['provider_no_observation']]
    noobs += [r.read(p) for p in (r.H/'review/quarantines').glob('*.json') if r.read(p)['classification']=='PROVIDER_NO_OBSERVATION']
    return {'run_status':'COMPLETE' if finished else 'INCOMPLETE','end_to_end_mappings_complete':complete,'fixed_mapping_slots':6,'UNMEASURED':unmeasured,
        'artifact_status_counts':dict(Counter(x['scientific_admission'] for x in rows)),
        'instrumentation_status_counts':dict(Counter(x['instrumentation'] for x in rows)),
        'contract_verdict_counts':dict(contracts),'supplied_operation_watch':watch,'mappings':rows,
        'provider_no_observation_events':noobs,'provider_attempts':len(attempts),'successful_provider_responses':successes,
        'available_token_totals':dict(tokens),'token_limitations':'Only completed validated observations; missing responses and provider-internal use unknown. Not billed costs or quota calibration.',
        'scientific_judgments_rewritten':False,'new_evaluator_calibration':False,'historical_preservation':r.verify()}
