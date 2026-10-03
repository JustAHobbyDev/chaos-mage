"""H6.R3 pure routing, provenance projection, and mechanical aggregation."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
import re
from jsonschema import Draft202012Validator

DIAGNOSTICS = ('OBLIGATION_OMISSION', 'GOVERNANCE_LAUNDERING', 'OVERTRIGGER',
    'WRONG_SECONDARY_CONTRACT', 'DEPENDENCY_DUPLICATION', 'FAILURE_NONPROPAGATION',
    'SHORT_CIRCUIT', 'RECURSIVE_EXPLOSION', 'DEPENDENCY_CYCLE',
    'DEPENDENCY_UNCERTAIN', 'CLASSIFICATION_CONTRACT_FAILURE',
    'PROVENANCE_PROJECTION_FAILURE', 'GOVERNANCE_BOUNDARY_LEAK',
    'SUPPLIED_PREMISE_OVERTRIGGER', 'GROUNDING_REF_MISCLASSIFICATION')
RANK = {'SATISFIED': 0, 'CONDITIONAL': 1, 'UNCERTAIN': 2, 'VIOLATED': 3}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def canonical(refs):
    require(isinstance(refs, list), 'PROVENANCE_PROJECTION_FAILURE: missing reference bundle')
    for ref in refs:
        require(set(ref) == {'source_id', 'role'} and isinstance(ref['source_id'], str)
                and ref['source_id'] and ref['role'] in ('SUPPORT', 'CONTEXT'),
                'PROVENANCE_PROJECTION_FAILURE: invalid reference')
    require(len({r['source_id'] for r in refs}) == len(refs),
            'PROVENANCE_PROJECTION_FAILURE: duplicate/conflicting source ID')
    # Schema declares reference order semantically irrelevant; roles remain exact.
    return sorted((r['source_id'], r['role']) for r in refs)


def projection_check(obligation, packet):
    a, b = canonical(obligation['provenance_refs']), canonical(packet['provenance_refs'])
    result = {'obligation_id': obligation['obligation_id'], 'frozen_refs_hash': digest(a),
              'packet_refs_hash': digest(b), 'exact_match': a == b}
    require(a == b and result['frozen_refs_hash'] == result['packet_refs_hash'],
            'PROVENANCE_PROJECTION_FAILURE: ' + obligation['obligation_id'])
    require(canonical([{k: r[k] for k in ('source_id', 'role')}
                       for r in packet['evidence_bundle']]) == a,
            'PROVENANCE_PROJECTION_FAILURE: resolved evidence roles differ')
    return result


def eligible(a):
    return (a['atomicity'] == 'ATOMIC' and
            a['content_origin']['assignment_status'] == 'ASSIGNED' and
            a['epistemic_function']['assignment_status'] == 'ASSIGNED')


def route(origin, function, taxonomy):
    require(origin in taxonomy['origins'] and function in taxonomy['functions'],
            'Uncertain axes cannot derive a contract')
    return taxonomy['supplied_routing'][origin] if origin in taxonomy['supplied_routing'] else [taxonomy['generated_routing'][function]]


def routes(a, taxonomy):
    require(eligible(a), 'Ineligible classification')
    return route(a['content_origin']['kind'], a['epistemic_function']['kind'], taxonomy)


def classification_packet(claim, case):
    return {'claim': deepcopy(claim), **{k: deepcopy(case[k])
            for k in ('target', 'source_instrument', 'mapping')}}


def obligation_packet(claim, case, assignment, assignments):
    require(eligible(assignment), 'Ineligible classification')
    return {**classification_packet(claim, case), 'classification': deepcopy(assignment),
            'frozen_claim_inventory': [{'claim': deepcopy(item),
                'classification': deepcopy(assignments[item['claim_id']])}
                for item in case['claims']]}


def validate(stage, value, packet, schema, taxonomy):
    Draft202012Validator(schema).validate(value)
    cid = packet['claim_id'] if stage == 'evaluation' else packet['claim']['claim_id']
    require(value['claim_id'] == cid, 'Changed claim identity')
    events = []
    sources = {packet[k]['source_id'] for k in ('target', 'source_instrument', 'mapping') if k in packet}
    def refs_check(refs):
        canonical(refs)
        require(all(r['source_id'] in sources for r in refs), 'PROV_UNKNOWN_SOURCE_ID')
    def origin_check(origin, refs):
        supplied = {'TARGET_SUPPLIED': {'TARGET'}, 'SOURCE_SUPPLIED': {'SOURCE_INSTRUMENT'},
                    'BOTH_SUPPLIED': {'TARGET', 'SOURCE_INSTRUMENT'}}
        for r in refs:
            key = {'TARGET': 'target', 'SOURCE_INSTRUMENT': 'source_instrument'}[r['source_type']]
            require(r['source_id'] == packet[key]['source_id'], 'ORIGIN_PROVENANCE_FAILURE')
        require(supplied.get(origin, set()) <= {r['source_type'] for r in refs}, 'ORIGIN_PROVENANCE_FAILURE')
    if stage == 'classification':
        for key, alternatives in [('content_origin', 'competing_origins'), ('epistemic_function', 'competing_functions')]:
            axis = value[key]
            require(len(axis[alternatives]) == len(set(axis[alternatives])), 'Duplicate alternatives')
            require((axis['kind'] is not None and not axis[alternatives]) if axis['assignment_status'] == 'ASSIGNED'
                    else axis['kind'] is None, 'Inconsistent classification uncertainty')
        origin_check(value['content_origin']['kind'], value['content_origin']['origin_refs'])
    elif stage == 'dependency':
        refs_check(value['base_provenance_refs'])
        ids = [d['dependency_id'] for d in value['dependencies']]
        require(len(ids) == len(set(ids)), 'Duplicate dependency identity')
        known = {i['claim']['claim_id'] for i in packet['frozen_claim_inventory']}
        unresolved = []
        for d in value['dependencies']:
            a = d['dependency_classification']; resolution = d['resolution']
            origin_check(a['content_origin'], a['origin_refs']); refs_check(d['provenance_refs'])
            if resolution is None:
                unresolved.append(d['dependency_id'])
                require(d['claim_ref'] is None, 'Unresolved reference must not imply a claim')
                continue
            require(a['content_origin'] != 'ORIGIN_UNCERTAIN' and a['epistemic_function'] != 'FUNCTION_UNCERTAIN',
                    'Uncertain axes require unresolved closure')
            if resolution == 'GROUNDING_REF':
                require(a['content_origin'] in taxonomy['supplied_routing'] and a['assertion_mode'] == 'REFERENCED_PREMISE',
                        'GROUNDING_REF_MISCLASSIFICATION')
                require(d['claim_ref'] is None, 'Grounding is not CLAIM_REF')
            elif resolution == 'CLAIM_REF':
                require(d['claim_ref'] in known and d['claim_ref'] != cid, 'Unknown/self claim reference')
            else:
                require(a['assertion_mode'] == 'ASSERTED_COMPONENT', 'SUPPLIED_PREMISE_OVERTRIGGER')
                require(d['claim_ref'] is None, 'Inline includes claim reference')
        require(not (unresolved or value['unresolved_dependencies']) or value['closure_status'] != 'COMPLETE',
                'Unresolved complete closure')
        if value['closure_status'] == 'DEPENDENCY_UNCERTAIN':
            require(bool(value['unresolved_dependencies']), 'Uncertain closure needs explanation')
            events.append({'code': 'DEPENDENCY_UNCERTAIN', 'claim_id': cid, 'detail': value['unresolved_dependencies']})
    else:
        for key in ('obligation_id', 'contract', 'subject'):
            require(value[key] == packet[key], 'Frozen evaluation identity changed: ' + key)
        require(value['verdict'] != 'CONDITIONAL' or value['unresolved_conditions'], 'Conditional needs condition')
        allowed = set(tuple(x) for x in canonical(packet['provenance_refs']))
        require(set(tuple(x) for x in canonical(value['provenance_refs'])) <= allowed, 'Response cites unfrozen evidence/roles')
        if value['contract'] in ('TARGET_FIDELITY', 'SOURCE_FIDELITY') and value['verdict'] == 'VIOLATED':
            events.append({'code': 'CLASSIFICATION_CONTRACT_FAILURE', 'claim_id': cid, 'detail': value['contract']})
    return events


def resolve(claim, assignment, discovery, taxonomy):
    """Called only after Stage B classifications are committed; no model contract selection."""
    def obligation(oid, contract, subject, refs, kind):
        canonical(refs)
        return {'claim_id': claim['claim_id'], 'obligation_id': oid, 'contract': contract,
                'subject': subject, 'provenance_refs': deepcopy(refs),
                'provenance_hash': digest(canonical(refs)), 'kind': kind}
    base = [obligation('B'+str(i+1), contract, claim['value'], discovery['base_provenance_refs'], 'BASE')
            for i, contract in enumerate(routes(assignment, taxonomy))]
    deps = deepcopy(discovery['dependencies'])
    for d in deps:
        d['obligations'] = []
        if d['resolution'] == 'INLINE_OBLIGATION':
            a = d['dependency_classification']
            require(a['assertion_mode'] == 'ASSERTED_COMPONENT', 'SUPPLIED_PREMISE_OVERTRIGGER')
            for i, contract in enumerate(route(a['content_origin'], a['epistemic_function'], taxonomy)):
                d['obligations'].append(obligation(d['dependency_id']+'-O'+str(i+1), contract,
                                                  d['subject'], d['provenance_refs'], 'INLINE'))
    return {'claim_obligation_set': {'claim_id': claim['claim_id'], 'base_obligations': base,
             'dependencies': deps, 'closure_status': discovery['closure_status'],
             'unresolved_dependencies': deepcopy(discovery['unresolved_dependencies'])}}


def obligation_jobs(claim, assignment, output):
    require(eligible(assignment), 'Ineligible classification')
    s = output['claim_obligation_set']
    if s['closure_status'] == 'SPLIT_REQUIRED':
        return []
    return deepcopy(s['base_obligations'] + [o for d in s['dependencies'] for o in d['obligations']])


def evaluation_packet(claim, case, job, taxonomy):
    # No whole claim citation record or implicit target/source envelope crosses this boundary.
    packet = {k: deepcopy(job[k]) for k in ('claim_id', 'obligation_id', 'contract', 'subject', 'provenance_refs')}
    packet['contract_question'] = taxonomy['contracts'][job['contract']]
    packet['claim_context'] = {'value': claim['value'], 'scope': claim['scope']}
    sources = {case[k]['source_id']: case[k]['text'] for k in ('target', 'source_instrument', 'mapping')}
    canonical(job['provenance_refs'])
    require(job['provenance_hash'] == digest(canonical(job['provenance_refs'])), 'PROVENANCE_PROJECTION_FAILURE: frozen hash')
    require(all(r['source_id'] in sources for r in job['provenance_refs']), 'PROVENANCE_PROJECTION_FAILURE: unknown source')
    packet['evidence_bundle'] = [{**deepcopy(r), 'text': sources[r['source_id']]} for r in job['provenance_refs']]
    if job['contract'] == 'GOVERNANCE_STRUCTURE':
        packet['governance_boundary'] = taxonomy['governance_boundary']
    projection_check(job, packet)
    return packet


def projection_barrier(jobs, packets):
    require(set(jobs) == set(packets), 'PROVENANCE_PROJECTION_FAILURE: incomplete packet set')
    return {key: projection_check(jobs[key], packets[key]) for key in jobs}


def p2_preflight(output):
    s = output['claim_obligation_set']
    obligations = s['base_obligations'] + [o for d in s['dependencies'] for o in d['obligations']]
    require([o['contract'] for o in obligations] == ['GOVERNANCE_STRUCTURE'], 'SUPPLIED_PREMISE_OVERTRIGGER: P2')
    require(s['closure_status'] == 'COMPLETE', 'P2 closure incomplete')
    require(any(d['resolution'] == 'GROUNDING_REF' and
            all(d['dependency_classification'][k] == v for k, v in {
                'content_origin': 'TARGET_SUPPLIED', 'epistemic_function': 'FACT',
                'assertion_mode': 'REFERENCED_PREMISE'}.items()) for d in s['dependencies']),
            'P2 missing supplied agreement grounding reference')
    require(all(d['resolution'] == 'GROUNDING_REF' for d in s['dependencies']), 'P2 must remain grounding-only')
    return {'status': 'PASS', 'contracts': ['GOVERNANCE_STRUCTURE'], 'empirical_secondary_count': 0}


def dependency_order(sets, known_claims):
    visiting, done, order = set(), set(), []
    def visit(cid):
        require(cid in known_claims, 'Unknown claim reference: '+cid)
        require(cid not in visiting, 'DEPENDENCY_CYCLE: '+cid)
        if cid in done:
            return
        visiting.add(cid)
        for d in sets.get(cid, {}).get('dependencies', []):
            if d['resolution'] == 'CLAIM_REF':
                visit(d['claim_ref'])
        visiting.remove(cid); done.add(cid); order.append(cid)
    for cid in known_claims:
        visit(cid)
    return order


def aggregate(assignments, outputs, evaluations, taxonomy):
    sets = {cid: b['claim_obligation_set'] for cid, b in outputs.items()}
    result = {}
    for cid in dependency_order(sets, assignments):
        if not eligible(assignments[cid]) or cid not in sets or sets[cid]['closure_status'] == 'SPLIT_REQUIRED':
            result[cid] = {'claim_id': cid, 'status': 'EXCLUDED', 'overall': None, 'results': []}
            continue
        s = sets[cid]; results = []; missing = []; constraints = []
        for d in s['dependencies']:
            if d['resolution'] == 'CLAIM_REF':
                ref = result[d['claim_ref']]
                results.append({'dependency_id': d['dependency_id'], 'claim_ref': d['claim_ref'], 'verdict': ref['overall']})
                if ref['status'] == 'INCOMPLETE':
                    missing.append(d['dependency_id'])
                elif ref['overall'] is None:
                    constraints.append('UNCERTAIN')
        for o in s['base_obligations'] + [o for d in s['dependencies'] for o in d['obligations']]:
            ev = evaluations.get((cid, o['obligation_id']))
            if ev is None:
                missing.append(o['obligation_id'])
            else:
                require(ev['contract'] == o['contract'], 'Evaluation contract mismatch')
                results.append({'obligation_id': o['obligation_id'], 'contract': o['contract'], 'verdict': ev['verdict']})
        if s['closure_status'] == 'DEPENDENCY_UNCERTAIN':
            constraints.append('UNCERTAIN')
        verdicts = [x['verdict'] for x in results if x['verdict'] is not None] + constraints
        result[cid] = {'claim_id': cid, 'status': 'INCOMPLETE' if missing else 'MEASURED',
                      'overall': None if missing else max(verdicts or ['UNCERTAIN'], key=RANK.get),
                      'results': results, 'missing_obligations': missing,
                      'closure_status': s['closure_status'], 'closure_constraints': constraints}
    return result
