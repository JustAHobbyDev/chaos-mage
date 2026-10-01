"""H.3 schema and four-part viability derivation. Diagnostics never override it."""
from claim_contracts import (require, unique, read, digest, sha, obj, arr, enum,
                            component, T, BOOL, SPANS, FIELDS, CLAIM, ARTIFACT,
                            MECHANISM, TARGET, CASCADE, REMAINDER, cited_spans, jsonschema)
import claim_contracts as old

DIMENSIONS=['warranted','source_derived','material','target_relevant']
YESNO=['YES','NO','UNCERTAIN']
REASONS=['mechanism_death','generic_remainder','target_payoff_loss','epistemically_empty','none','uncertain']
SCOPE=['substantially_intact','reduced','none','uncertain']
NULL_TEXT={'anyOf':[T,{'type':'null'}]}

def schema(stage):
    if stage=='claim-warrant': return old.schema(stage)
    require(stage=='artifact','Unknown stage')
    candidate=obj({'remainder_id':T,'origin':enum(['frozen','judge_added']),
        'inference':T,'source_spans':SPANS,
        **{d:component(YESNO) for d in DIMENSIONS}})
    return obj({'remainder_viability':obj({
        'case_id':T,'unsupported_claim_ids':arr(T),'candidate_remainders':arr(candidate),
        'viable_remainders':arr(T),
        'strongest_surviving_target_inference':obj({'remainder_id':NULL_TEXT,'text':NULL_TEXT,'source_spans':SPANS,'why_warranted':T}),
        'scope_survival':component(SCOPE),'mechanism_survival':component(MECHANISM),
        'remainder_check':component(REMAINDER),'target_contribution_survival':component(TARGET),
        'dependency_cascade':component(CASCADE),
        'central_bridge':obj({'deleted_claim_is_required_for_all_material_contributions':enum(['yes','no','uncertain']),'rationale':T}),
        'no_viable_remainder_reason':enum(REASONS),'artifact_status':enum(ARTIFACT),
        'structural_conflict':obj({'present':BOOL,'resolved':BOOL,'explanation':T}),
        'uncertainty':arr(T)})})

def statuses(candidate):return [candidate[d]['status'] for d in DIMENSIONS]
def viable(candidate):return all(x=='YES' for x in statuses(candidate))
def unresolved(candidate):
    values=statuses(candidate)
    return 'NO' not in values and 'UNCERTAIN' in values

def derive(candidates,scope,conflict=None):
    require(scope in SCOPE,'Invalid scope')
    if conflict and conflict['present'] and not conflict['resolved']:
        return 'UNCERTAIN_LOAD_BEARING'
    if any(viable(r) for r in candidates):
        require(scope in ['substantially_intact','reduced'],'Viable remainder with inconsistent scope requires unresolved conflict')
        return 'KEEP_WITH_WARRANT_FLAGS' if scope=='substantially_intact' else 'KEEP_WITH_REDUCED_SCOPE'
    if any(unresolved(r) for r in candidates):return 'UNCERTAIN_LOAD_BEARING'
    return 'CORE_INVALID'

def projection(a):
    return {'candidates':[{'remainder_id':r['remainder_id'],'inference':r['inference'],
        'source_spans':r['source_spans'],**{d:r[d]['status'] for d in DIMENSIONS},
        'rationale':{d:r[d]['rationale'] for d in DIMENSIONS}} for r in a['candidate_remainders']],
        'viable_remainders':a['viable_remainders'],'scope_survival':a['scope_survival']['status'],
        'no_viable_remainder_reason':a['no_viable_remainder_reason']}

def validate(value,stage,identity,candidate,unsupported=(),frozen_candidates=()):
    if stage=='claim-warrant':return old.validate(value,stage,identity,candidate)
    jsonschema.Draft202012Validator(schema(stage)).validate(value)
    a=value['remainder_viability'];require(a['case_id']==identity,'Wrong case identity')
    require(sorted(a['unsupported_claim_ids'])==sorted(x['claim_id'] for x in unsupported),'Wrong deletion set')
    rows=a['candidate_remainders'];ids=[r['remainder_id'] for r in rows]
    require(len(ids)==len(set(ids)),'Duplicate candidate ID')
    supplied={r['remainder_id']:r for r in frozen_candidates}
    require({r['remainder_id'] for r in rows if r['origin']=='frozen'}==set(supplied),'Frozen inventory coverage')
    for r in rows:
        if r['origin']=='frozen':
            f=supplied[r['remainder_id']]
            require(r['inference']==f['inference'] and r['source_spans']==f['source_spans'],'Frozen candidate changed')
        else: require(r['remainder_id'] not in supplied,'Addition reused frozen ID')
        require(bool(r['source_spans']),'Unanchored candidate')
        cited_spans(r['source_spans'],candidate,unsupported,surviving=True,mapping_only=True)
    expected=[r['remainder_id'] for r in rows if viable(r)]
    require(len(a['viable_remainders'])==len(set(a['viable_remainders'])) and set(a['viable_remainders'])==set(expected),'Incorrect viable IDs')
    conflict=a['structural_conflict']
    require(conflict['present'] or conflict['resolved'],'Absent conflict cannot be unresolved')
    status=derive(rows,a['scope_survival']['status'],conflict)
    require(a['artifact_status']==status,'Incorrect deterministic artifact status')
    reason=a['no_viable_remainder_reason']
    if status.startswith('KEEP_'):require(reason=='none','Keep requires reason none')
    elif status=='CORE_INVALID':
        require(not expected and not any(unresolved(r) for r in rows),'Core has viable/unresolved remainder')
        require(reason in REASONS[:4] and a['scope_survival']['status']=='none','Core reason/scope mismatch')
    else:
        require(reason=='uncertain' and bool(a['uncertainty']),'Uncertainty requires reason and explanation')
    issues=[]
    if reason=='mechanism_death' and a['mechanism_survival']['status']!='DOES_NOT_SURVIVE':issues.append('mechanism death diagnostic')
    if reason=='generic_remainder' and a['remainder_check']['status']!='GENERIC_REMAINDER':issues.append('generic remainder diagnostic')
    target=a['target_contribution_survival']['status']
    if status=='CORE_INVALID' and target!='NO_MATERIAL_CONTRIBUTION':issues.append('core target contribution')
    if status=='KEEP_WITH_REDUCED_SCOPE' and target!='REDUCED_BUT_MATERIAL':issues.append('reduced target contribution')
    if status=='KEEP_WITH_WARRANT_FLAGS' and target!='SUBSTANTIALLY_SURVIVES':issues.append('intact target contribution')
    require(not issues or conflict['present'],'Diagnostic conflict requires explanation: '+','.join(issues))
    strongest=a['strongest_surviving_target_inference']
    require((strongest['remainder_id'] is None)==(strongest['text'] is None),'Strongest identity/text mismatch')
    if strongest['remainder_id'] is not None:
        require(strongest['remainder_id'] in ids,'Unknown strongest candidate')
        row=next(r for r in rows if r['remainder_id']==strongest['remainder_id'])
        require(strongest['text']==row['inference'] and strongest['source_spans']==row['source_spans'],'Strongest differs from assessed candidate')
    else:require(not strongest['source_spans'],'Null strongest has citations')
    require(not expected or strongest['remainder_id'] is not None,'Viable artifact lacks strongest inference')
