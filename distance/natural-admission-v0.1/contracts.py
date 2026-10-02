"""Pure offline checks. Semantic facts are observations, never inferred from ID existence."""
from collections import Counter
from pathlib import Path
import importlib.util
import json
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('h6_h5_segment',H.with_name('span-provenance-calibration-v0.1')/'segment.py')
h5=importlib.util.module_from_spec(spec);spec.loader.exec_module(h5)
FIELDS=h5.FIELDS

def components(value):
    if isinstance(value,dict):
        if {'component_id','value','scope','provenance'} <= set(value):
            yield value
        else:
            for child in value.values():yield from components(child)
    elif isinstance(value,list):
        for child in value:yield from components(child)

def citation_checks(table,value):
    errors=[]
    if value.get('packet_id')!=table['packet_id']:errors.append({'code':'PROV_WRONG_PACKET'})
    for c in components(value):
        refs=c['provenance']['refs'];cid=c['component_id']
        if c['value']=='NOT_APPLICABLE' and not refs:continue
        if not any(r['role']=='SUPPORT' for r in refs):errors.append({'code':'PROV_NO_SUPPORT','component_id':cid})
        for sid,n in Counter(r['source_id'] for r in refs).items():
            if sid not in table['spans']:errors.append({'code':'PROV_UNKNOWN_SOURCE_ID','component_id':cid,'source_id':sid})
            if n>1:errors.append({'code':'PROV_DUPLICATE_REF','component_id':cid,'source_id':sid})
            if len({r['role'] for r in refs if r['source_id']==sid})>1:errors.append({'code':'PROV_ROLE_CONFLICT','component_id':cid,'source_id':sid})
    return errors

def exposure(tables):
    ids=[set(t['spans']) for t in tables]
    return any(ids[i]&ids[j] for i in range(len(ids)) for j in range(i))

def collision_failure(*,simultaneous,reused,bare_citation,accepted_or_ambiguous,wrong_packet_material=False,reviewer_ambiguity_material=False,cross_packet_impossible=False):
    if cross_packet_impossible:return True # directly evidenced legitimate relation, rule 5c
    return all((simultaneous,reused,bare_citation,accepted_or_ambiguous,wrong_packet_material or reviewer_ambiguity_material))

def resolve(table,packet_id,source_id):
    if table['packet_id']!=packet_id:raise ValueError('PROV_WRONG_PACKET')
    return table['spans'][source_id]

def ablate(atoms,judgments):
    by={j['claim_id']:j for j in judgments}
    assert len(by)==len(judgments)==len(atoms['claims'])
    assert set(by)=={c['claim_id'] for c in atoms['claims']}
    deleted=[c for c in atoms['claims'] if by[c['claim_id']]['status']=='UNSUPPORTED']
    surviving=[c for c in atoms['claims'] if by[c['claim_id']]['status']!='UNSUPPORTED']
    return {'packet_id':atoms['packet_id'],'deleted_claim_ids':[c['claim_id'] for c in deleted],
            'deleted_claims':deleted,'surviving_claims':surviving,
            'lineage':[{'claim_id':c['claim_id'],'original_claim_sha256':h5.canonical_hash(c),'status':by[c['claim_id']]['status'],
                        'action':'DELETE' if by[c['claim_id']]['status']=='UNSUPPORTED' else 'RETAIN'} for c in atoms['claims']],
            'policy':'Simultaneous semantic-object deletion. Unchanged original spans are attribution evidence, not additional surviving premises.'}

def viable(c):return all(a['value']=='YES' for a in c['viability'].values())
def unresolved(c):
    values=[a['value'] for a in c['viability'].values()]
    return 'NO' not in values and 'UNCERTAIN' in values

def semantic_checks(stage,value,packet):
    """Relational inconsistencies are frozen observations, not provider parse failure."""
    errors=[]
    def emit(code,**kw):errors.append({'code':code,**kw})
    if value.get('packet_id')!=packet['packet_id']:emit('PROV_WRONG_PACKET')
    if stage=='claims':
        ids=[c['claim_id'] for c in value['claims']]
        if len(ids)!=len(set(ids)):emit('ATOM_DUPLICATE_ID')
        if Counter(c['field'] for c in value['coverage'])!=Counter(FIELDS):emit('ATOM_FIELD_COVERAGE')
    if stage=='claim-judgments':
        if value['claim_id']!=packet['claim']['claim_id']:emit('CLAIM_ID_MISMATCH')
    if stage=='remainder-inventory':
        survivors={c['claim_id'] for c in packet['ablation']['surviving_claims']}
        for c in value['candidates']:
            if not set(c['surviving_claim_ids'])<=survivors:emit('ABLATION_DELETED_OR_UNKNOWN_CLAIM',candidate_id=c['candidate_id'])
            if c['kind']=='INSUFFICIENCY_ONLY' and c['viability']['productive']['value']=='YES':emit('INSUFFICIENCY_PRODUCTIVITY',candidate_id=c['candidate_id'])
        if value['deleted_claims_used']:emit('ABLATION_DELETED_CLAIM_USED')
        if Counter(c['field'] for c in value['field_coverage'])!=Counter(FIELDS):emit('REMAINDER_FIELD_COVERAGE')
        for u in value['inquiry_units']:
            complete=(len(u['alternatives'])>=2 and u['unresolved_contrast']['value']!='NOT_APPLICABLE'
                      and u['next_operation']['value']!='NOT_APPLICABLE' and len(u['outcomes'])>=2
                      and u['outcomes_are_discriminating'] and u['provenance_complete'])
            if u['complete']!=complete:emit('IQ_COMPLETENESS_MISMATCH',unit_id=u['unit_id'])
            roles=[c for c in value['candidates'] if c['unit_id']==u['unit_id'] and c['kind']=='INQUIRY_CONSTRAINT']
            if complete and len(roles)!=1:emit('IQ_MISSING_OR_DUPLICATE_ROLE',unit_id=u['unit_id'])
    if stage=='artifact-judgments':
        cs=packet['inventory']['candidates'];yes={c['candidate_id'] for c in cs if viable(c)};maybe={c['candidate_id'] for c in cs if unresolved(c)}
        if set(value['definite_viable_candidate_ids'])!=yes:emit('ARTIFACT_VIABLE_SET')
        if set(value['unresolved_decisive_candidate_ids'])!=maybe:emit('ARTIFACT_UNRESOLVED_SET')
        expected=('KEEP_WITH_REDUCED_SCOPE' if value['scope_lost']=='YES' else 'KEEP_WITH_WARRANT_FLAGS') if yes else ('UNCERTAIN_LOAD_BEARING' if maybe else 'CORE_INVALID')
        if value['scientific_status']!=expected:emit('ARTIFACT_STATUS_RULE',expected=expected)
    return errors
