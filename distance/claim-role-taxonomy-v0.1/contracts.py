"""H6.R1 packet construction and validation; no provider or historical-label IO."""
from copy import deepcopy
from jsonschema import Draft202012Validator


def require(condition, message):
    if not condition:
        raise ValueError(message)


def claim_view(claim, mapping=True):
    keys = ['claim_id', 'packet_id', 'local_claim_id', 'value', 'scope']
    if mapping:
        keys.append('mapping_refs')
    return {key: deepcopy(claim[key]) for key in keys}


def role_packet(claim, evidence):
    return {'claim': claim_view(claim), 'target': deepcopy(evidence['target']),
            'source_instrument': deepcopy(evidence['source_instrument']),
            'mapping': deepcopy(evidence['mapping'])}


def evaluation_packet(claim, evidence, assignment, taxonomy):
    require(assignment['claim_id'] == claim['claim_id'], 'Assignment identity mismatch')
    require(assignment['atomicity'] == 'ATOMIC' and
            assignment['assignment_status'] == 'ASSIGNED', 'Ineligible assignment')
    role = assignment['primary_role']
    contract = taxonomy['routing'][role]
    packet = {'claim': claim_view(claim, role not in ('SUPPLIED_FACT', 'SOURCE_FACT')),
              'frozen_role': role, 'contract_id': contract,
              'contract_question': taxonomy['contracts'][contract]}
    if role != 'SOURCE_FACT':
        packet['target'] = deepcopy(evidence['target'])
    if role != 'SUPPLIED_FACT':
        packet['source_instrument'] = deepcopy(evidence['source_instrument'])
    if role not in ('SUPPLIED_FACT', 'SOURCE_FACT'):
        packet['mapping'] = {'packet_id': claim['packet_id'], 'spans': {
            sid: deepcopy(evidence['mapping']['spans'][sid])
            for sid in evidence['evaluation_mapping_ids']}}
    return packet


def validate(stage, value, packet, schema, taxonomy):
    Draft202012Validator(schema).validate(value)
    require(value['claim_id'] == packet['claim']['claim_id'], 'Response identity changed')
    if stage == 'role':
        atomic, status, role, competing = (value[k] for k in
            ('atomicity', 'assignment_status', 'primary_role', 'competing_roles'))
        valid = (
            atomic == 'ATOMIC' and status == 'ASSIGNED' and
            role in taxonomy['roles'] and not competing or
            atomic == 'SPLIT_REQUIRED' and status == 'ATOMIZATION_DEFECT' and
            role is None and not competing or
            atomic == 'ATOMIC' and status == 'ROLE_UNCERTAIN' and
            role is None and len(set(competing)) >= 2
        )
        require(valid, 'Invalid atomicity/status/role combination')
        refs = value['role_provenance']
    else:
        require(value['frozen_role'] == packet['frozen_role'], 'Frozen role changed')
        require(value['contract_id'] == packet['contract_id'] ==
                taxonomy['routing'][value['frozen_role']], 'Wrong contract')
        require(value['verdict'] != 'CONDITIONAL' or value['unresolved_conditions'],
                'CONDITIONAL requires explicit unresolved conditions')
        refs = value['evaluation_provenance']
    # Citation defects remain observations; never repair a judgment or retry it.
    allowed = {'TARGET': {packet['target']['target_id']} if 'target' in packet else set(),
               'SOURCE_INSTRUMENT': {packet['source_instrument']['source_id']}
               if 'source_instrument' in packet else set(),
               'MAPPING': set(packet.get('mapping', {}).get('spans', {}))}
    diagnostics = []
    if not refs:
        diagnostics.append({'code': 'EMPTY_PROVENANCE'})
    seen = set()
    for ref in refs:
        key = (ref['source_type'], ref['source_id'])
        if ref['source_id'] not in allowed[ref['source_type']]:
            diagnostics.append({'code': 'PROV_UNKNOWN_SOURCE_ID', **ref})
        if key in seen:
            diagnostics.append({'code': 'PROV_DUPLICATE_REF', **ref})
        seen.add(key)
    return diagnostics
