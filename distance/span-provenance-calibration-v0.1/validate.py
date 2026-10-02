"""Mechanical citation checks plus explicitly labeled recorded-review replay.

This module contains no semantic entailment engine. It never compares a component
value to source text, and never derives support status from fixture expectations.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from segment import canonical_hash

HERE = Path(__file__).resolve().parent
MECHANICAL_CODES = ('PROV_UNKNOWN_SOURCE_ID', 'PROV_WRONG_PACKET', 'PROV_NO_SUPPORT',
                    'PROV_DUPLICATE_REF', 'PROV_ROLE_CONFLICT', 'PROV_SCHEMA')
SEMANTIC_CODES = ('PROV_MISSING_CONTEXT', 'PROV_UNSUPPORTED_COMPONENT',
                  'PROV_SCOPE_OVERREACH', 'PROV_UNCERTAIN_SUPPORT')
CODES = MECHANICAL_CODES + SEMANTIC_CODES + ('PROV_CONFLICT_REVIEW',)


def schema_errors(name, value):
    schema = json.loads((HERE / 'schemas' / f'{name}.schema.json').read_text())
    return [error.message for error in Draft202012Validator(schema).iter_errors(value)]


def annotation_from_fixture(fixture):
    return {'packet_id': fixture['packet_id'], 'components': [
        {key: value for key, value in component.items()
         if key not in ('expected_support_status', 'expected_codes')}
        for component in fixture['components']]}


def mechanical(table, annotation):
    """Validate references only; source integrity is the caller's separate gate."""
    errors = []

    def emit(code, component_id=None, source_id=None, detail=None):
        row = {'code': code}
        if component_id is not None:
            row['component_id'] = component_id
        if source_id is not None:
            row['source_id'] = source_id
        if detail is not None:
            row['detail'] = detail
        errors.append(row)

    malformed = schema_errors('annotation', annotation)
    if malformed:
        return [{'code': 'PROV_SCHEMA', 'detail': item} for item in malformed]
    if annotation['packet_id'] != table['packet_id']:
        return [{'code': 'PROV_WRONG_PACKET'}]
    component_ids = [component['component_id'] for component in annotation['components']]
    if len(set(component_ids)) != len(component_ids):
        emit('PROV_SCHEMA', detail='Duplicate component_id')
    for component in annotation['components']:
        cid = component['component_id']
        refs = component['provenance']['refs']
        if not any(ref['role'] == 'SUPPORT' for ref in refs):
            emit('PROV_NO_SUPPORT', cid)
        for sid, count in Counter(ref['source_id'] for ref in refs).items():
            if sid not in table['spans']:
                emit('PROV_UNKNOWN_SOURCE_ID', cid, sid)
            if count > 1:
                emit('PROV_DUPLICATE_REF', cid, sid)
            if len({ref['role'] for ref in refs if ref['source_id'] == sid}) > 1:
                emit('PROV_ROLE_CONFLICT', cid, sid)
    return errors


def validate_fixture(table, fixture, review=None):
    malformed = schema_errors('fixture', fixture)
    errors = ([{'code': 'PROV_SCHEMA', 'detail': item} for item in malformed]
              if malformed else mechanical(table, annotation_from_fixture(fixture)))
    result = {'fixture_id': fixture.get('fixture_id'), 'mechanical_errors': errors,
              'mechanically_valid': not errors, 'review_errors': [], 'components': [],
              'semantic_assessment_method': 'recorded_engineering_review'}
    if errors:
        return result
    if review is None:
        result['review_errors'].append('REVIEW_MISSING')
        return result
    if schema_errors('review', review):
        result['review_errors'].append('REVIEW_SCHEMA')
        return result
    if (review['fixture_id'] != fixture['fixture_id'] or review['packet_id'] != fixture['packet_id']
            or review['fixture_sha256'] != canonical_hash(fixture)):
        result['review_errors'].append('REVIEW_BINDING')
        return result
    rows = review['components']
    if (Counter(row['component_id'] for row in rows)
            != Counter(component['component_id'] for component in fixture['components'])):
        result['review_errors'].append('REVIEW_COVERAGE')
        return result
    for row in rows:
        status, codes = row['support_status'], row['codes']
        valid = ((status == 'SUFFICIENT' and not codes)
                 or (status == 'UNCERTAIN' and codes == ['PROV_UNCERTAIN_SUPPORT'])
                 or (status == 'INSUFFICIENT' and bool(codes)
                     and all(code in SEMANTIC_CODES[:3] for code in codes)))
        if not valid or len(codes) != len(set(codes)):
            result['review_errors'].append('REVIEW_STATUS_CODES')
    if not result['review_errors']:
        result['components'] = rows
    return result


def conflict_review(left_packet, left, right_packet, right, finding):
    """Emit a signal only for an explicit incompatibility review, never infer one."""
    if (not finding or finding.get('mutually_incompatible') is not True
            or finding.get('material_support_overlap') is not True or not finding.get('rationale')):
        return []
    if (left_packet != right_packet or left['component_type'] != right['component_type']
            or left['scope'] != right['scope']):
        return []
    support = lambda c: {ref['source_id'] for ref in c['provenance']['refs'] if ref['role'] == 'SUPPORT'}
    overlap = support(left) & support(right)
    if not overlap:
        return []
    return [{'code': 'PROV_CONFLICT_REVIEW', 'failing': False,
             'overlapping_support': sorted(overlap), 'rationale': finding['rationale']}]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('table', type=Path)
    parser.add_argument('fixture', type=Path)
    parser.add_argument('--review', type=Path)
    args = parser.parse_args()
    load = lambda path: json.loads(path.read_text())
    print(json.dumps(validate_fixture(load(args.table), load(args.fixture),
                                     load(args.review) if args.review else None), indent=2))
