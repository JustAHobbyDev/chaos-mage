"""H7 offline admission preparation using the frozen scientific protocol."""
import importlib.util
import json
import continuation
import stages

LATER = ('evaluation', 'remainder-inventory', 'artifact-judgments')
RANK = {'GROUNDING_REF': 0, 'SATISFIED': 0, 'CONDITIONAL': 1, 'UNCERTAIN': 2, 'VIOLATED': 3}


def mapping_id(uid):
    return uid.split('--')[0]


def stage_ids(r, stage):
    excluded = continuation.quarantined(r)
    if stage not in LATER:
        return [cid for cid in r.order() if cid not in excluded]
    freeze = r.read(r.H / f'{stage}-packets-freeze.json')
    return [x for x in freeze['packet_order'] if mapping_id(x) not in excluded]


def emit_packet(r, stage, uid, value):
    p = r.H / 'packets' / stage / (uid + '.json')
    r.write(p, value)
    text = (r.H / 'prompts' / (stage+'.md')).read_text() + '\nFROZEN PACKET\n' + json.dumps(value, indent=2) + '\n'
    r.raw(p.with_suffix('.txt'), text.encode())
    return [p, p.with_suffix('.txt')]


def prepare(r, stage):
    r.verify(); r.require(not r.git('status','--porcelain'), 'Commit upstream measurements first')
    upstream = {'evaluation':'obligations', 'remainder-inventory':'ablations', 'artifact-judgments':'remainder-inventory'}[stage]
    r.require((r.H / (upstream+'-freeze.json')).exists(), 'Upstream not frozen')
    paths, ids = [], []
    for cid in r.order():
        if cid in continuation.quarantined(r): continue
        original = r.read(r.H/'packets/discovery'/f'{cid}.json')
        # Explicit packet allowlist: one mapping, its original source/target evidence.
        base = {k: original[k] for k in ('packet_id','target_frame','source_instrument','evidence_sources','allowed_source_ids')}
        if stage == 'evaluation':
            defs = r.read(r.H/'evaluation-contracts.json')
            inv = r.read(r.H/'obligations'/f'{cid}.json')
            r.require(inv['ready_for_evaluation'], 'Unresolved routing')
            for obligation in inv['obligations']:
                uid = cid + '--' + obligation['obligation_id']
                packet = {**base, 'obligation':obligation,
                    'contract_question':defs['contracts'][obligation['contract']], 'verdict_meanings':defs['verdicts'],
                    'mapping_claim_context':original['claims']}
                paths += emit_packet(r,stage,uid,packet); ids.append(uid)
        else:
            ablation = r.read(r.H/'ablations'/f'{cid}.json')
            packet = {**base,'ablation':ablation,'claim_statuses':{x['claim_id']:x['verdict'] for x in ablation['lineage']}}
            if stage == 'artifact-judgments': packet['inventory'] = r.read(r.H/'remainder-inventory'/f'{cid}.json')
            paths += emit_packet(r,stage,cid,packet);ids.append(cid)
    r.write(r.H/f'{stage}-packets-freeze.json',{'parent_commit':r.head(),'packet_order':ids,'files':r.inventory(paths)})


def validate(r, stage, value, packet):
    r.require(value['packet_id']==packet['packet_id'],'Packet identity mismatch')
    stages.citations(value,set(packet['allowed_source_ids']))
    if stage=='evaluation':
        for key in ('claim_id','obligation_id','contract','subject'):
            r.require(value[key]==packet['obligation'][key],'Frozen obligation mismatch: '+key)
        r.require(value['verdict']!='CONDITIONAL' or value['unresolved_conditions'],'Conditional without conditions')
        return
    spec=importlib.util.spec_from_file_location('h7_prior_semantics',r.R/'distance/natural-admission-v0.1/contracts.py')
    c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    errors=c.semantic_checks(stage,value,packet)
    r.require(not errors,'Frozen admission contract inconsistency: '+json.dumps(errors))


def publish(r, stage):
    r.verify();r.require(r.state()=='COMPLETE','Paused measurements require adjudication')
    paths=[]
    all_ids = r.order() if stage not in LATER else r.read(r.H/f'{stage}-packets-freeze.json')['packet_order']
    for uid in all_ids:
        d=r.RT/'attempts'/stage/uid
        if not (d/'validation.json').exists():
            r.require(mapping_id(uid) in continuation.quarantined(r), 'Unmeasured pending attempt: '+uid)
            continue
        v=r.read(d/'validation.json')
        r.require(r.sha(d/'response.json')==v['response_sha256'],'Response drift')
        for p in sorted(d.iterdir()):
            dest=r.H/'raw'/stage/uid/p.name
            if dest.exists():r.require(dest.read_bytes()==p.read_bytes(),'Published raw differs')
            else:r.raw(dest,p.read_bytes())
            paths.append(dest)
        dest=r.H/stage/f'{uid}.json'
        if dest.exists():r.require(r.read(dest)==r.read(d/'response.json'),'Published observation differs')
        else:r.write(dest,r.read(d/'response.json'))
        paths.append(dest)
    r.write(r.H/f'{stage}-freeze.json',{'parent_commit':r.head(),'quarantined':sorted(continuation.quarantined(r)),'files':r.inventory(paths)})


def ablate_objects(claims, inventory, judgments):
    """Aggregate frozen obligations and CLAIM_REF DAG; delete semantic objects once."""
    by={j['obligation_id']:j for j in judgments}
    expected={o['obligation_id'] for o in inventory['obligations']}
    if set(by)!=expected or len(by)!=len(judgments):raise ValueError('Required judgments incomplete/duplicated')
    own={c['claim_id']:[] for c in claims['claims']}; edges={k:[] for k in own}
    for o in inventory['obligations']:
        j=by[o['obligation_id']]
        if any(j[k]!=o[k] for k in ('claim_id','contract','subject')):raise ValueError('Judgment identity drift')
        if o['contract'] in ('TARGET_FIDELITY','SOURCE_FIDELITY') and j['verdict']!='SATISFIED':
            raise ValueError('Required supplied-origin fidelity unresolved/failed; quarantine, no scientific deletion')
        own[o['claim_id']].append(j)
    for ref in inventory['references']:
        if ref['resolution']=='CLAIM_REF':edges[ref['claim_id']].append(ref['referenced_claim_id'])
    done={};active=set()
    def verdict(cid):
        if cid in done:return done[cid]
        if cid in active:raise ValueError('Cyclic claim dependencies')
        active.add(cid)
        values=[j['verdict'] for j in own[cid]]+[verdict(x) for x in edges[cid]]
        done[cid]=max(values,key=RANK.get) if values else 'GROUNDING_REF'
        active.remove(cid);return done[cid]
    for cid in own:verdict(cid)
    deleted=[c for c in claims['claims'] if done[c['claim_id']]=='VIOLATED']
    surviving=[c for c in claims['claims'] if done[c['claim_id']]!='VIOLATED']
    return {'packet_id':claims['packet_id'],'deleted_claim_ids':[c['claim_id'] for c in deleted],
        'deleted_claims':deleted,'surviving_claims':surviving,
        'lineage':[{'claim_id':cid,'verdict':done[cid],'action':'DELETE_MAPPING_ASSERTION_OR_USE' if done[cid]=='VIOLATED' else 'RETAIN',
            'verdict_origin':'MODEL_CONTRACT_AGGREGATE' if own[cid] or edges[cid] else 'SUPPLIED_PREMISE_GROUNDING_EXEMPTION_NO_MODEL_VERDICT',
            'obligation_verdicts':[dict(j) for j in own[cid]],'claim_refs':edges[cid]} for cid in own],
        'policy':'Simultaneous deletion of frozen semantic claim objects under H7. Source/target facts unchanged. CONTEXT spans are attribution only; no deleted premise may be reused. Conditional/uncertain claims retained with flags.'}


def ablate(r):
    r.verify();r.require(not r.git('status','--porcelain'),'Commit judgments first')
    r.require((r.H/'evaluation-freeze.json').exists(),'Freeze all measurable judgments first')
    paths=[]
    for cid in r.order():
        if cid in continuation.quarantined(r):continue
        inv=r.read(r.H/'obligations'/f'{cid}.json')
        js=[r.read(r.H/'evaluation'/f"{cid}--{o['obligation_id']}.json") for o in inv['obligations']]
        value=ablate_objects(r.read(r.H/'claims'/f'{cid}.json'),inv,js)
        path=r.H/'ablations'/f'{cid}.json';r.write(path,value);paths.append(path)
    r.write(r.H/'ablations-freeze.json',{'parent_commit':r.head(),'files':r.inventory(paths)})


def freeze_obligations(r):
    r.verify();r.require(not r.git('status','--porcelain'),'Commit discovery freeze first')
    r.require((r.H/'discovery-freeze.json').exists(),'Discovery not frozen')
    paths=[];counts={};unavailable={}
    for cid in r.order():
        if cid in continuation.quarantined(r):
            counts[cid]=None;unavailable[cid]='Unavailable due to final local quarantine; not zero scientific claims.';continue
        d=r.read(r.H/'discovery'/f'{cid}.json')
        inv=stages.obligation_inventory(r.read(r.H/'claims'/f'{cid}.json'),r.read(r.H/'classification'/f'{cid}.json'),d)
        r.require(inv['ready_for_evaluation'],'Preserve/quarantine unresolved routing before evaluation')
        oids=[o['obligation_id'] for o in inv['obligations']]
        r.require(len(oids)==len(set(oids)),'Duplicate required obligation identity')
        p=r.H/'obligations'/f'{cid}.json';r.write(p,{'packet_id':cid,**inv});paths.append(p)
        counts[cid]=inv['evaluation_session_count']
    p=r.H/'evaluation-fanout.json'
    r.write(p,{'sessions_by_mapping':counts,'unavailable':unavailable,
        'exact_sessions':sum(v for v in counts.values() if v is not None),
        'ready_for_evaluation':True,'scientific_packet_count':sum(v is not None for v in counts.values()),
        'earlier_attempts_preserved':len(continuation.ledger(r)),
        'next_gate':'Freeze evaluation packets, cumulative forecast, fresh usage/budget preflight; explicit approval only below 30%.'})
    paths.append(p)
    r.write(r.H/'obligations-freeze.json',{'parent_commit':r.head(),'files':r.inventory(paths)})


def guard(r,uid,stage):
    evidence=continuation.verify_evidence(r)
    cid=mapping_id(uid)
    r.require(uid in stage_ids(r,stage),'Attempt not in frozen stage inventory')
    r.require(continuation.schedulable(cid,r.order(),continuation.quarantined(r),
        evidence['continuation_independence']['unaffected'],(r.RT/'attempts'/stage/uid).exists()),
        'Consumed, quarantined, replacement or unverified mapping')
