"""Offline preparation and validation for H7 origin/function and dependency stages."""
import importlib.util
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def citations(value, allowed):
    if isinstance(value, dict):
        if 'source_id' in value:
            require(value['source_id'] in allowed, 'RESPONSE_SOURCE_UNKNOWN')
        for item in value.values():
            citations(item, allowed)
    elif isinstance(value, list):
        for item in value:
            citations(item, allowed)


def validate(stage, value, packet):
    require(value['packet_id'] == packet['packet_id'], 'Packet identity mismatch')
    key = 'classifications' if stage == 'classification' else 'claims'
    ids = [c['claim_id'] for c in value[key]]
    expected = [c['claim_id'] for c in packet['claims']['claims']]
    require(len(ids) == len(set(ids)) and set(ids) == set(expected), 'Frozen claim coverage mismatch')
    citations(value, set(packet['allowed_source_ids']))
    if stage == 'discovery':
        edges = {cid: [] for cid in ids}
        for claim in value['claims']:
            dep_ids = [d['dependency_id'] for d in claim['dependencies']]
            require(len(dep_ids) == len(set(dep_ids)), 'Duplicate dependency identity')
            for d in claim['dependencies']:
                if d['resolution'] == 'CLAIM_REF':
                    require(d['referenced_claim_id'] in expected, 'Unknown claim reference')
                    require(d['referenced_claim_id'] != claim['claim_id'], 'Self-referential dependency')
                    edges[claim['claim_id']].append(d['referenced_claim_id'])
        visited, active = set(), set()
        def visit(cid):
            require(cid not in active, 'Cyclic CLAIM_REF dependencies')
            if cid in visited:
                return
            active.add(cid)
            for parent in edges[cid]:
                visit(parent)
            active.remove(cid)
            visited.add(cid)
        for cid in edges:
            visit(cid)


def prepare(stage, runner):
    r = runner
    r.verify()
    upstream = 'claims' if stage == 'classification' else 'classification'
    require((r.H / f'{upstream}-freeze.json').exists(), 'Upstream stage not frozen')
    require(not r.git('status', '--porcelain'), 'Commit upstream freeze first')
    paths = []
    segment_spec = importlib.util.spec_from_file_location('h7_stage_h5', r.R / 'distance/span-provenance-calibration-v0.1/segment.py')
    h5 = importlib.util.module_from_spec(segment_spec)
    segment_spec.loader.exec_module(h5)
    for cid in r.order():
        packet = r.read(r.H / 'packets/claims' / f'{cid}.json')
        packet['claims'] = r.read(r.H / 'claims' / f'{cid}.json')
        packet['classification_definitions'] = r.read(r.H / 'classification-definitions.json')
        # Target frame stays intact as an authored record. Source and mapping use
        # unchanged H.5 segmentation; disjoint local IDs prevent source ambiguity.
        evidence = {'T001': {'role': 'SUPPORT', 'kind': 'target', 'value': packet['target_frame']}}
        source = h5.segment(cid, packet['source_instrument'])
        for sid, span in source['spans'].items():
            value = {k: v for k, v in span.items() if k != 'source_range'}
            for key in ('parent_id', 'header_id'):
                if key in value:
                    value[key] = 'S' + value[key][1:]
            evidence['S' + sid[1:]] = {'role': 'SUPPORT', 'kind': 'source', **value}
        for sid, span in packet.pop('spans').items():
            evidence[sid] = {'role': 'CONTEXT', 'kind': 'mapping', **span}
        packet['evidence_sources'] = evidence
        packet['allowed_source_ids'] = list(evidence)
        if stage == 'discovery':
            packet['classifications'] = r.read(r.H / 'classification' / f'{cid}.json')
        path = r.H / 'packets' / stage / f'{cid}.json'
        r.write(path, packet)
        paths.append(path)
        path = path.with_suffix('.txt')
        r.raw(path, ((r.H / 'prompts' / f'{stage}.md').read_text() + '\nFROZEN PACKET\n' + json.dumps(packet, indent=2) + '\n').encode())
        paths.append(path)
    r.write(r.H / f'{stage}-packets-freeze.json', {'parent_commit': r.head(), 'files': r.inventory(paths)})


GENERATED_CONTRACTS = {'FACT': 'FACT_WARRANT', 'INFERENCE': 'DERIVED_WARRANT',
    'CONDITIONAL_RELATION': 'CONDITIONAL_LICENSE', 'OPERATION': 'OPERATION_LICENSE',
    'GOVERNANCE_RULE': 'GOVERNANCE_STRUCTURE', 'LIMIT': 'LIMIT_WARRANT'}
FIDELITY = {'TARGET_SUPPLIED': ['TARGET_FIDELITY'], 'SOURCE_SUPPLIED': ['SOURCE_FIDELITY'],
            'BOTH_SUPPLIED': ['TARGET_FIDELITY', 'SOURCE_FIDELITY']}


def contracts(assignment):
    origin, function, mode = (assignment[k] for k in ('content_origin', 'epistemic_function', 'assertion_mode'))
    require(origin is not None and function is not None, 'Unresolved origin/function')
    if origin == 'MAPPING_GENERATED':
        require(mode is None, 'Generated content cannot claim a supplied-premise exemption')
        return [GENERATED_CONTRACTS[function]]
    require(origin in FIDELITY and mode is not None, 'Unresolved supplied assertion mode')
    if mode == 'REFERENCED_PREMISE':
        return []  # GROUNDING_REF record; no unnecessary generated-warrant call.
    require(mode == 'ASSERTED_COMPONENT', 'Unknown assertion mode')
    return FIDELITY[origin] + (['OPERATION_LICENSE'] if function == 'OPERATION' else [])


def grounding(assignment, refs):
    require(assignment['content_origin'] in FIDELITY and
            assignment['assertion_mode'] == 'REFERENCED_PREMISE', 'Unlicensed GROUNDING_REF')
    ids = [x['source_id'] for x in refs]
    origin = assignment['content_origin']
    if origin in ('TARGET_SUPPLIED', 'BOTH_SUPPLIED'):
        require(any(i.startswith('T') for i in ids), 'Missing target grounding')
    if origin in ('SOURCE_SUPPLIED', 'BOTH_SUPPLIED'):
        require(any(i.startswith('S') for i in ids), 'Missing source grounding')


def obligation_inventory(claims, assignments, discovery):
    """Mechanical routes only; unresolved cases are preserved, never judged here."""
    by_id = {x['claim_id']: x for x in claims['claims']}
    classified = {x['claim_id']: x for x in assignments['classifications']}
    obligations, refs, watch, issues = [], [], [], []

    def add(cid, oid, subject, scope, assignment, evidence):
        routes = contracts(assignment)
        if not routes:
            grounding(assignment, evidence)
            refs.append({'claim_id': cid, 'dependency_id': oid, 'resolution': 'GROUNDING_REF',
                         'subject': subject, 'evidence_used': evidence})
            return
        for index, contract in enumerate(routes, 1):
            obligations.append({'claim_id': cid, 'obligation_id': f'{oid}-{index}',
                'subject': subject, 'scope': scope, 'contract': contract,
                'content_origin': assignment['content_origin'],
                'epistemic_function': assignment['epistemic_function'],
                'assertion_mode': assignment['assertion_mode'], 'evidence_used': evidence})
        if assignment['content_origin'] in FIDELITY and assignment['epistemic_function'] == 'OPERATION':
            watch.append({'claim_id': cid, 'component_id': oid, 'content_origin': assignment['content_origin'],
                'fidelity_contract': FIDELITY[assignment['content_origin']], 'fidelity_verdict': None,
                'operation_license_present': 'OPERATION_LICENSE' in routes,
                'operation_license_verdict': None, 'routing_clean': True, 'admission_effect': 'PENDING_EVALUATION'})

    for item in discovery['claims']:
        cid = item['claim_id']
        try:
            a = classified[cid]
            require(a['atomicity'] == 'ATOMIC', 'Primary SPLIT_REQUIRED or UNCERTAIN')
            require(item['closure'] == 'COMPLETE', 'Dependency SPLIT_REQUIRED or UNCERTAIN')
            add(cid, cid + '-B', by_id[cid]['proposition'], by_id[cid]['scope'], a, item['base_evidence_used'])
            for dep in item['dependencies']:
                require(not dep['another_independent_level_required'], 'SPLIT_REQUIRED: another level')
                if not (dep['distinct'] and dep['material'] and dep['unevaluated']):
                    # Already evaluated content may reuse a frozen claim; do not
                    # create new obligations for immaterial/non-distinct content.
                    require(dep['resolution'] != 'INLINE_OBLIGATION', 'Inline obligation lacks DISTINCT/MATERIAL/UNEVALUATED')
                if dep['resolution'] == 'GROUNDING_REF':
                    grounding(dep, dep['evidence_used'])
                    refs.append({'claim_id': cid, 'dependency_id': dep['dependency_id'],
                                 'resolution': 'GROUNDING_REF', 'evidence_used': dep['evidence_used']})
                elif dep['resolution'] == 'CLAIM_REF':
                    require(dep['referenced_claim_id'] in by_id, 'Unknown CLAIM_REF')
                    routes = contracts(dep)
                    target_routes = contracts(classified[dep['referenced_claim_id']])
                    require(routes == target_routes, 'CLAIM_REF classification/contract mismatch')
                    if dep['content_origin'] in FIDELITY and dep['epistemic_function'] == 'OPERATION' and dep['assertion_mode'] == 'ASSERTED_COMPONENT':
                        watch.append({'claim_id': cid, 'component_id': dep['dependency_id'],
                            'content_origin': dep['content_origin'], 'fidelity_contract': FIDELITY[dep['content_origin']],
                            'fidelity_verdict': None, 'operation_license_present': 'OPERATION_LICENSE' in target_routes,
                            'operation_license_verdict': None, 'routing_clean': True,
                            'admission_effect': 'PENDING_REFERENCED_EVALUATION',
                            'referenced_claim_id': dep['referenced_claim_id']})
                    refs.append({'claim_id': cid, 'dependency_id': dep['dependency_id'],
                                 'resolution': 'CLAIM_REF', 'referenced_claim_id': dep['referenced_claim_id']})
                elif dep['resolution'] == 'INLINE_OBLIGATION':
                    require(dep['assertion_mode'] != 'REFERENCED_PREMISE', 'Referenced premise is not inline')
                    add(cid, cid + '-' + dep['dependency_id'], dep['subject'], dep['scope'], dep, dep['evidence_used'])
                else:
                    raise ValueError('Unresolved dependency resolution')
        except (KeyError, ValueError) as exc:
            issues.append({'claim_id': cid, 'reason': str(exc)})
    # This inventory never silently treats unresolved routing as an admission verdict.
    return {'obligations': obligations, 'references': refs, 'supplied_operation_watch': watch,
            'routing_issues': issues, 'evaluation_session_count': len(obligations) if not issues else None,
            'ready_for_evaluation': not issues}


def freeze_obligations(r):
    r.verify()
    require((r.H / 'discovery-freeze.json').exists(), 'Freeze all discovery responses first')
    require(not r.git('status', '--porcelain'), 'Commit discovery freeze first')
    paths, counts, issues = [], {}, {}
    for cid in r.order():
        claims = r.read(r.H / 'claims' / f'{cid}.json')
        assignments = r.read(r.H / 'classification' / f'{cid}.json')
        discovery = r.read(r.H / 'discovery' / f'{cid}.json')
        validate('discovery', discovery, r.read(r.H / 'packets/discovery' / f'{cid}.json'))
        value = obligation_inventory(claims, assignments, discovery)
        path = r.H / 'obligations' / f'{cid}.json'
        r.write(path, {'packet_id': cid, **value})
        paths.append(path)
        counts[cid] = value['evaluation_session_count']
        if value['routing_issues']:
            issues[cid] = value['routing_issues']
    path = r.H / 'evaluation-fanout.json'
    r.write(path, {'sessions_by_mapping': counts,
        'exact_sessions': sum(counts.values()) if not issues else None,
        'routing_issues': issues, 'ready_for_evaluation': not issues,
        'provider_calls': 0, 'next_gate': 'Cumulative budget/usage reforecast and required user approval before evaluation.'})
    paths.append(path)
    r.write(r.H / 'obligations-freeze.json', {'parent_commit': r.head(), 'files': r.inventory(paths)})
