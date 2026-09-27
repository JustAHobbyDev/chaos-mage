#!/usr/bin/env python3
"""Offline v0.3 contracts. No provider, execution, repair, or publication API."""
import argparse
import hashlib
import json
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DIMS = ('entities', 'relations', 'processes', 'operations', 'observables',
        'inferences', 'failure_modes')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, f'Duplicate key: {key}')
        value[key] = item
    return value


def read(path):
    def invalid_constant(value):
        raise ValueError(f'Nonfinite JSON constant: {value}')
    return json.loads(Path(path).read_text(), object_pairs_hook=unique_object,
                      parse_constant=invalid_constant)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate(value, kind, candidate=None):
    require(kind in ('candidate', 'transfer', 'validity'), 'Unknown contract')
    schema = read(HERE / f'{kind}.schema.json')
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(schema).validate(value)
    record = value['transfer'] if kind == 'transfer' else value
    if candidate is not None:
        validate(candidate, 'candidate')
        require(record['case_id'] == candidate['case_id'], 'Case ID mismatch')
        if kind == 'transfer':
            for key in ('source', 'target', 'mapping'):
                require(record[key] == candidate[key], f'Candidate {key} changed')
    if kind != 'candidate':
        reframe = record['validity']['target_reframe']
        target = record['target'] if kind == 'transfer' else (
            candidate['target'] if candidate is not None else None)
        if target is not None and reframe['occurred']:
            require(reframe['original_question'] == target['question'],
                    'Reframe original question must equal retained target question')
    if kind == 'transfer':
        baseline = record['native_baseline']
        if baseline is not None:
            require(baseline['target_domain'] == record['target']['domain'],
                    'Baseline domain differs from retained target')
            require(baseline['target_task'] == record['target']['question'],
                    'Baseline task differs from retained target')
        if record['displacement'] is not None:
            require(all(type(record['displacement']['dimensions'][d]['level']) is int
                        for d in DIMS), 'Dimension levels must be actual integers')
        if record['grounding'] is not None:
            roles = [x['source_role'] for x in record['grounding']['essential_counterparts']]
            require(len(roles) == len(set(roles)), 'Duplicate essential source role')
    return record


def verify_preservation():
    manifest = read(HERE / 'preservation.json')
    for name, expected in manifest['files'].items():
        require(sha(ROOT / name) == expected, f'Historical file changed: {name}')
    require(sum(p.startswith('distance/') for p in manifest['files']) ==
            manifest['historical_distance_count'], 'Historical count mismatch')
    return len(manifest['files'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind', choices=('candidate', 'transfer', 'validity', 'preservation'))
    parser.add_argument('path', nargs='?', type=Path)
    parser.add_argument('--candidate', type=Path)
    args = parser.parse_args()
    if args.kind == 'preservation':
        print(f'Preserved {verify_preservation()} historical/source files')
    else:
        parser.error('a JSON path is required') if args.path is None else None
        validate(read(args.path), args.kind,
                 read(args.candidate) if args.candidate else None)
        print(f'{args.kind}: OK')


if __name__ == '__main__':
    main()
