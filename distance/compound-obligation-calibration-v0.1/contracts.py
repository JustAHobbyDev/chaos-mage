"""Pure H6.R2 contracts: no provider, filesystem, historical, or hypothesis access."""
from collections import Counter
from copy import deepcopy
from itertools import product
import re
from jsonschema import Draft202012Validator

DIAGNOSTICS = ('OBLIGATION_OMISSION', 'GOVERNANCE_LAUNDERING', 'OVERTRIGGER',
    'WRONG_SECONDARY_CONTRACT', 'DEPENDENCY_DUPLICATION', 'FAILURE_NONPROPAGATION',
    'SHORT_CIRCUIT', 'RECURSIVE_EXPLOSION', 'DEPENDENCY_CYCLE',
    'DEPENDENCY_UNCERTAIN', 'CLASSIFICATION_CONTRACT_FAILURE')
RANK = {'SATISFIED': 0, 'CONDITIONAL': 1, 'UNCERTAIN': 2, 'VIOLATED': 3}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def eligible(a):
    return (a['atomicity'] == 'ATOMIC' and
            a['content_origin']['assignment_status'] == 'ASSIGNED' and
            a['epistemic_function']['assignment_status'] == 'ASSIGNED')


def routes(a, taxonomy):
    require(eligible(a), 'Ineligible classification')
    origin, function = a['content_origin']['kind'], a['epistemic_function']['kind']
    return taxonomy['supplied_routing'].get(origin, [taxonomy['generated_routing'][function]])


def classification_packet(claim, case):
    return {'claim': deepcopy(claim), **{k: deepcopy(case[k])
            for k in ('target', 'source_instrument', 'mapping')}}


def obligation_packet(claim, case, assignment, assignments):
    require(eligible(assignment), 'Ineligible classification')
    return {**classification_packet(claim, case), 'classification': deepcopy(assignment),
            'frozen_claim_inventory': [{'claim': deepcopy(item),
                'classification': deepcopy(assignments[item['claim_id']])}
                for item in case['claims']]}


def obligation_jobs(claim, assignment, output):
    """Only the frozen discovery record determines measured jobs, never hypotheses."""
    require(eligible(assignment), 'Ineligible classification')
    s = output['claim_obligation_set']
    if s['closure_status'] == 'SPLIT_REQUIRED':
        return []
    jobs = []
    for b in s['base_obligations']:
        jobs.append({'claim_id': claim['claim_id'], 'obligation_id': b['obligation_id'],
                     'contract': b['contract'], 'subject': claim['value'], 'kind': 'BASE'})
    for d in s['dependencies']:
        inline = d['inline_obligation']
        if d['resolution'] == 'INLINE_OBLIGATION' and inline['contract'] and inline['subject']:
            jobs.append({'claim_id': claim['claim_id'], 'obligation_id': d['dependency_id'],
                         'contract': inline['contract'], 'subject': inline['subject'], 'kind': 'INLINE'})
    return jobs


def evaluation_packet(claim, case, job, taxonomy):
    packet = {k: deepcopy(job[k]) for k in ('claim_id', 'obligation_id', 'contract', 'subject')}
    packet['contract_question'] = taxonomy['contracts'][job['contract']]
    if job['contract'] == 'TARGET_FIDELITY':
        packet['target'] = deepcopy(case['target'])
    elif job['contract'] == 'SOURCE_FIDELITY':
        packet['source_instrument'] = deepcopy(case['source_instrument'])
    else:
        packet.update(classification_packet(claim, case))
    return packet


def validate(stage, value, packet, schema, taxonomy):
    Draft202012Validator(schema).validate(value)
    events = []
    cid = packet['claim_id'] if stage == 'evaluation' else packet['claim']['claim_id']
    def diagnostic(code, detail):
        events.append({'code': code, 'claim_id': cid, 'detail': detail})
    if stage == 'classification':
        require(value['claim_id'] == cid, 'Changed claim identity')
        for key, alternatives in [('content_origin', 'competing_origins'),
                                   ('epistemic_function', 'competing_functions')]:
            axis = value[key]
            require(len(axis[alternatives]) == len(set(axis[alternatives])), 'Duplicate alternatives')
            if axis['assignment_status'] == 'ASSIGNED':
                require(axis['kind'] is not None and not axis[alternatives], 'Inconsistent assigned axis')
            else:
                require(axis['kind'] is None, 'Uncertainty must preserve null kind')
        refs = value['content_origin']['origin_refs']
        supplied = {'TARGET_SUPPLIED': {'TARGET'}, 'SOURCE_SUPPLIED': {'SOURCE_INSTRUMENT'},
                    'BOTH_SUPPLIED': {'TARGET', 'SOURCE_INSTRUMENT'}}
        present = {r['source_type'] for r in refs if r['source_id'] ==
                   packet[{'TARGET':'target','SOURCE_INSTRUMENT':'source_instrument'}[r['source_type']]]['source_id']}
        if not supplied.get(value['content_origin']['kind'], set()) <= present:
            diagnostic('ORIGIN_PROVENANCE_FAILURE', 'Supplied origin lacks positive matching input provenance')
        for ref in refs:
            if ref['source_id'] != packet[{'TARGET':'target','SOURCE_INSTRUMENT':'source_instrument'}[ref['source_type']]]['source_id']:
                diagnostic('PROV_UNKNOWN_SOURCE_ID', ref)
    elif stage == 'obligation':
        s = value['claim_obligation_set']
        require(s['claim_id'] == cid, 'Changed claim identity')
        a = packet['classification']
        require(s['classification'] == {'content_origin': a['content_origin']['kind'],
                                        'epistemic_function': a['epistemic_function']['kind']}, 'Frozen classification changed')
        expected = Counter(routes(a, taxonomy))
        actual = Counter(b['contract'] for b in s['base_obligations'])
        if expected != actual:
            diagnostic('BASE_ROUTING_FAILURE', {'expected': dict(expected), 'observed': dict(actual)})
        if expected - actual:
            diagnostic('OBLIGATION_OMISSION', {'missing_base_contracts': list((expected-actual).elements())})
        keys = [b['obligation_id'] for b in s['base_obligations']] + [d['dependency_id'] for d in s['dependencies']]
        require(len(keys) == len(set(keys)), 'Duplicate obligation/dependency identity')
        require(all(re.fullmatch(r'[A-Za-z0-9_-]+',key) for key in keys), 'Unsafe obligation identity')
        emb = {e['dependency_id']: e for e in value['embedded_classifications']}
        require(len(emb) == len(value['embedded_classifications']), 'Duplicate embedded classification')
        require(set(emb) == {d['dependency_id'] for d in s['dependencies']}, 'Embedded classification identity mismatch')
        known = {i['claim']['claim_id'] for i in packet['frozen_claim_inventory']}
        for d in s['dependencies']:
            e = emb[d['dependency_id']]
            require(d['trigger'] == 'EMBEDDED_'+e['epistemic_function'], 'Embedded trigger/function mismatch')
            inline = d['inline_obligation']
            known_sources = {packet[k]['source_id'] for k in ('target','source_instrument','mapping')}
            for ref in inline['provenance_refs']:
                if ref['source_id'] not in known_sources:
                    diagnostic('PROV_UNKNOWN_SOURCE_ID', ref)
            if d['resolution'] == 'CLAIM_REF':
                require(d['claim_ref'] in known, 'Unknown claim reference')
                require(inline == {'contract': None, 'subject': None, 'provenance_refs': []}, 'Reference includes duplicate inline evaluation')
            else:
                require(d['claim_ref'] is None, 'Inline dependency carries reference')
                if not inline['contract'] or not inline['subject']:
                    require(s['closure_status'] == 'DEPENDENCY_UNCERTAIN' and s['unresolved_dependencies'], 'Unresolved inline requires uncertain closure')
                else:
                    require(inline['subject'] == e['subject'], 'Embedded subject changed')
                    if inline['contract'] != taxonomy['generated_routing'][e['epistemic_function']]:
                        diagnostic('WRONG_SECONDARY_CONTRACT', d['dependency_id'])
        require(not s['unresolved_dependencies'] or s['closure_status'] != 'COMPLETE', 'Unresolved complete closure')
        if s['closure_status'] == 'DEPENDENCY_UNCERTAIN':
            require(bool(s['unresolved_dependencies']), 'Uncertain closure needs explanation')
            diagnostic('DEPENDENCY_UNCERTAIN', s['unresolved_dependencies'])
    else:
        for key in ('claim_id', 'obligation_id', 'contract', 'subject'):
            require(value[key] == packet[key], 'Frozen evaluation identity changed: '+key)
        require(value['verdict'] != 'CONDITIONAL' or value['unresolved_conditions'], 'Conditional needs explicit condition')
        if value['contract'] in ('TARGET_FIDELITY', 'SOURCE_FIDELITY') and value['verdict'] == 'VIOLATED':
            diagnostic('CLASSIFICATION_CONTRACT_FAILURE', value['contract'])
        known = {packet[k]['source_id'] for k in ('target','source_instrument','mapping') if k in packet}
        if 'claim' in packet:
            known.add(packet['claim']['claim_id'])
        for ref in value['provenance_refs']:
            if ref['source_id'] not in known:
                diagnostic('PROV_UNKNOWN_SOURCE_ID', ref)
    return events


def dependency_order(sets, known_claims):
    """Detect cycles first; order DAGs without making any new scientific inference."""
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
    sets = {cid: b['claim_obligation_set'] for cid,b in outputs.items()}
    order = dependency_order(sets, assignments)
    result = {}
    for cid in order:
        a = assignments[cid]
        if not eligible(a) or cid not in sets or sets[cid]['closure_status'] == 'SPLIT_REQUIRED':
            result[cid] = {'claim_id': cid, 'status': 'EXCLUDED', 'overall': None, 'results': [],
                           'reason': 'classification uncertainty/split or split-required discovery'}
            continue
        s = sets[cid]; results = []; missing = []; constraints = []
        actual = Counter(b['contract'] for b in s['base_obligations'])
        if Counter(routes(a,taxonomy)) != actual:
            constraints.append('UNCERTAIN')
        required = [(b['obligation_id'], b['contract']) for b in s['base_obligations']]
        for d in s['dependencies']:
            if d['resolution'] == 'CLAIM_REF':
                ref = result[d['claim_ref']]
                results.append({'dependency_id':d['dependency_id'], 'claim_ref':d['claim_ref'],
                                'verdict':ref['overall'], 'referenced_status':ref['status']})
                if ref['status'] == 'INCOMPLETE':
                    missing.append(d['dependency_id'])
                elif ref['overall'] is None:
                    constraints.append('UNCERTAIN')
            elif d['inline_obligation']['contract'] and d['inline_obligation']['subject']:
                required.append((d['dependency_id'], d['inline_obligation']['contract']))
        for oid,contract in required:
            ev = evaluations.get((cid,oid))
            if ev is None:
                missing.append(oid)
            else:
                require(ev['contract'] == contract, 'Evaluation contract mismatch')
                results.append({'obligation_id':oid, 'contract':contract, 'verdict':ev['verdict']})
        if s['closure_status'] == 'DEPENDENCY_UNCERTAIN':
            constraints.append('UNCERTAIN')
        verdicts = [x['verdict'] for x in results if x['verdict'] is not None]+constraints
        # Never make a scientific aggregate from missing required observations.
        overall = None if missing else max(verdicts or ['UNCERTAIN'],key=RANK.get)
        result[cid] = {'claim_id':cid,'status':'INCOMPLETE' if missing else 'MEASURED',
                       'overall':overall,'results':results,'missing_obligations':missing,
                       'closure_status':s['closure_status'],'closure_constraints':constraints}
    return result


def regression_fixtures(taxonomy):
    """All 24 independent combinations, including the five required named fixtures."""
    return [{'origin':o,'function':f,'contracts':taxonomy['supplied_routing'].get(o,
            [taxonomy['generated_routing'][f]])} for o,f in product(taxonomy['origins'],taxonomy['functions'])]
