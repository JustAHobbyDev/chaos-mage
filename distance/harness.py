#!/usr/bin/env python3
"""Offline validation and explicit, fresh-process distance measurements."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

import jsonschema
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RUNTIME = ROOT / '.runtime/distance-v0.1'
DIMS = ('entities', 'relations', 'processes', 'operations', 'observables', 'inferences', 'failure_modes')
CLASSES = ('Native', 'Adjacent', 'Remote', 'Alien')


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node):
    result = {}
    for key, value in node.value:
        key = loader.construct_object(key)
        if key in result:
            raise ValueError(f'Duplicate key: {key}')
        result[key] = loader.construct_object(value)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read(path):
    return yaml.load(path.read_text(), Loader=UniqueLoader)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def keys(value, expected):
    require(isinstance(value, dict) and set(value) == set(expected), f'Expected keys: {expected}')


def validate_case(case):
    keys(case, ('case_id', 'source', 'target'))
    keys(case['source'], ('name', 'practice', 'instrument'))
    keys(case['source']['instrument'], ('state', 'operation', 'signal', 'inference', 'limit'))
    keys(case['target'], ('domain', 'problem'))
    def strings(value):
        if isinstance(value, dict):
            for child in value.values():
                strings(child)
        else:
            require(isinstance(value, str) and bool(value.strip()), 'Expected nonempty string')
    strings(case)


def cases():
    result = {}
    provenance = read(HERE / 'provenance.yaml')
    for path in sorted((HERE / 'cases').glob('CASE-*.yaml')):
        case = read(path)
        validate_case(case)
        require(case['case_id'] == path.stem, 'Case ID differs from filename')
        require(path.stem not in result, 'Duplicate case')
        original = read(ROOT / provenance[path.stem]['path'])
        require(original['extraction']['status'] == 'accepted', 'Unaccepted source')
        require(original['extraction']['id'] == provenance[path.stem]['extraction_id'], 'Source ID mismatch')
        require(case['source']['instrument'] == original['instrument'], 'Instrument content changed')
        for key in ('name', 'practice'):
            require(case['source'][key] == original['extraction'][key], 'Source identity changed')
        result[path.stem] = case
    require(16 <= len(result) <= 24, 'Expected 16–24 calibration cases')
    require(set(result) == set(provenance), 'Provenance coverage differs')
    source_counts = Counter(c['source']['name'] for c in result.values())
    target_counts = Counter(json.dumps(c['target'], sort_keys=True) for c in result.values())
    require(sum(n for n in source_counts.values() if n > 1) >= len(result)/2, 'Too few source contrasts')
    require(max(target_counts.values()) > 1, 'No identical-target contrast')
    return result


def validate_judgment(value, case_id):
    jsonschema.validate(value, read(HERE / 'output.schema.json'))
    require(value['classification']['case_id'] == case_id, 'Judgment case ID differs')
    # jsonschema considers 1.0 an integer; require actual integer ordinal values.
    for entry in value['classification']['displacement'].values():
        require(type(entry['level']) is int, 'Level must be an integer, not bool or float')
    return value['classification']


def packet(case_id):
    return ((HERE / 'CLASSIFIER-v0.1.md').read_text() + '\n\nCASE PACKET\n' +
            (HERE / 'cases' / f'{case_id}.yaml').read_text())


def frozen_paths():
    paths = [HERE / p for p in ('CLASSIFIER-v0.1.md', 'PROTOCOL-v0.1.md', 'output.schema.json',
             'execution-config.json', 'provenance.yaml', 'harness.py', 'requirements.txt')]
    paths += sorted((HERE / 'cases').glob('CASE-*.yaml'))
    paths += sorted({ROOT / v['path'] for v in read(HERE / 'provenance.yaml').values()})
    return paths


def freeze():
    records = cases()
    write_new(HERE / 'freeze-v0.1.json', {'frozen_at': now(),
        'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'files': {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in frozen_paths()},
        'packets': {cid: sha(packet(cid).encode()) for cid in records}})


def verify():
    manifest = read(HERE / 'freeze-v0.1.json')
    for path, digest in manifest['files'].items():
        require(sha((ROOT / path).read_bytes()) == digest, f'Frozen file changed: {path}')
    records = cases()
    require(set(records) == set(manifest['packets']), 'Frozen case coverage differs')
    for cid in records:
        require(sha(packet(cid).encode()) == manifest['packets'][cid], 'Packet changed')
    return records


def run_one(cid, replicate):
    verify()
    config = read(HERE / 'execution-config.json')
    directory = RUNTIME / cid / replicate
    directory.mkdir(parents=True, exist_ok=False)
    prompt = packet(cid)
    (directory / 'prompt.txt').write_text(prompt)
    with tempfile.TemporaryDirectory(prefix='distance-isolated-') as cwd:
        command = ['codex', 'exec', '--ignore-user-config', '--ephemeral', '--skip-git-repo-check',
            '--sandbox', 'read-only', '--json', '--color', 'never', '--cd', cwd,
            '--model', config['model'], '-c', f'model_reasoning_effort="{config["reasoning_effort"]}"',
            '-c', 'project_doc_max_bytes=0', '-c', 'web_search="disabled"',
            '--output-schema', str(HERE / 'output.schema.json'),
            '--output-last-message', str(directory / 'response.json')]
        for feature in config['disabled_features']:
            command += ['--disable', feature]
        command += ['-']
        reservation = {'case_id': cid, 'replicate': replicate, 'started_at': now(),
            'packet_sha256': sha(prompt.encode()), 'configuration': config, 'command': command,
            'cli_version': subprocess.check_output(['codex', '--version'], text=True).strip()}
        write_new(directory / 'reservation.json', reservation)
        status, error = 'failed', None
        try:
            with (directory / 'events.jsonl').open('x') as stdout, (directory / 'stderr.txt').open('x') as stderr:
                process = subprocess.run(command, input=prompt, text=True, stdout=stdout, stderr=stderr,
                                         timeout=config['timeout_seconds'], check=False)
            require(process.returncode == 0, f'CLI exit {process.returncode}')
            events = [json.loads(line) for line in (directory / 'events.jsonl').read_text().splitlines() if line.strip()]
            require(sum(e['type'] == 'thread.started' for e in events) == 1, 'Expected one fresh thread')
            require(sum(e['type'] == 'turn.completed' for e in events) == 1, 'Expected one completed turn')
            require(not any(e['type'] in ('error', 'turn.failed') for e in events), 'Execution error')
            allowed = {'agent_message', 'reasoning'}
            require(all(e.get('item', {}).get('type') in allowed for e in events if 'item' in e),
                    'Tool or unexpected item detected; isolation invalid')
            value = read(directory / 'response.json')
            validate_judgment(value, cid)
            status = 'valid'
        except (ValueError, OSError, subprocess.TimeoutExpired, jsonschema.ValidationError, yaml.YAMLError) as exc:
            error = str(exc)
        write_new(directory / 'validation.json', {'status': status, 'error': error, 'finished_at': now()})
        return f'{cid}/{replicate}: {status}'


def freeze_results():
    records = verify()
    entries, threads = [], set()
    for cid in records:
        for replicate in ('A', 'B'):
            directory = RUNTIME / cid / replicate
            require(read(directory / 'validation.json')['status'] == 'valid', f'Invalid or missing {cid}/{replicate}')
            validate_judgment(read(directory / 'response.json'), cid)
            reservation = read(directory / 'reservation.json')
            require(reservation['packet_sha256'] == sha(packet(cid).encode()), 'Reservation packet mismatch')
            events = [json.loads(line) for line in (directory / 'events.jsonl').read_text().splitlines()]
            thread = next(e['thread_id'] for e in events if e['type'] == 'thread.started')
            require(thread not in threads, 'Thread reused')
            threads.add(thread)
            entries.append({'case_id': cid, 'replicate': replicate, 'thread_id': thread,
                'files': {p.name: sha(p.read_bytes()) for p in sorted(directory.iterdir()) if p.is_file()}})
    write_new(HERE / 'results-freeze-v0.1.json', {'frozen_at': now(),
        'protocol_freeze_sha256': sha((HERE / 'freeze-v0.1.json').read_bytes()), 'runs': entries})


def publish():
    verify()
    manifest = read(HERE / 'results-freeze-v0.1.json')
    for entry in manifest['runs']:
        cid, replicate = entry['case_id'], entry['replicate']
        directory = RUNTIME / cid / replicate
        for name, digest in entry['files'].items():
            require(sha((directory / name).read_bytes()) == digest, f'Raw artifact changed: {cid}/{replicate}/{name}')
        dest = HERE / 'judgments' / f'{cid}-{replicate}.json'
        with dest.open('xb') as stream:
            stream.write((directory / 'response.json').read_bytes())


def metrics(pairs):
    n = len(pairs)
    require(n > 0, 'No pairs')
    steps = Counter(abs(CLASSES.index(a['final_class']) - CLASSES.index(b['final_class'])) for a, b in pairs)
    boundaries = Counter(' ↔ '.join(sorted((a['final_class'], b['final_class']), key=CLASSES.index))
                         for a, b in pairs if a['final_class'] != b['final_class'])
    return {'n': n, 'final_class': {'exact_count': steps[0], 'exact_rate': steps[0]/n,
        'one_step_count': steps[1], 'one_step_rate': steps[1]/n,
        'within_one_step_count': steps[0]+steps[1], 'within_one_step_rate': (steps[0]+steps[1])/n,
        'larger_disagreement_count': sum(v for k,v in steps.items() if k > 1)},
        'dimensions': {d: {'exact_count': sum(a['displacement'][d]['level'] == b['displacement'][d]['level'] for a,b in pairs),
            'exact_rate': sum(a['displacement'][d]['level'] == b['displacement'][d]['level'] for a,b in pairs)/n,
            'mean_absolute_disagreement': sum(abs(a['displacement'][d]['level'] - b['displacement'][d]['level']) for a,b in pairs)/n}
            for d in DIMS},
        'naturalization': {'exact_count': sum(a['naturalization']['status'] == b['naturalization']['status'] for a,b in pairs),
            'exact_rate': sum(a['naturalization']['status'] == b['naturalization']['status'] for a,b in pairs)/n},
        'disagreement_boundaries': dict(boundaries),
        'confusion_matrix': {a: {b: sum(x['final_class']==a and y['final_class']==b for x,y in pairs) for b in CLASSES} for a in CLASSES},
        'boundary_dimensions': {boundary: {d: {'disagreement_count': sum(x['displacement'][d]['level'] != y['displacement'][d]['level'] for x,y in pairs if ' ↔ '.join(sorted((x['final_class'],y['final_class']),key=CLASSES.index)) == boundary),
            'absolute_disagreement': sum(abs(x['displacement'][d]['level'] - y['displacement'][d]['level']) for x,y in pairs if ' ↔ '.join(sorted((x['final_class'],y['final_class']),key=CLASSES.index)) == boundary)} for d in DIMS} for boundary in boundaries}}


def analyze():
    records = verify()
    manifest = read(HERE / 'results-freeze-v0.1.json')
    require(manifest['protocol_freeze_sha256'] == sha((HERE / 'freeze-v0.1.json').read_bytes()), 'Freeze mismatch')
    expected = {(cid, rep) for cid in records for rep in ('A','B')}
    require({(e['case_id'], e['replicate']) for e in manifest['runs']} == expected and len(manifest['runs']) == len(expected), 'Run coverage mismatch')
    for entry in manifest['runs']:
        path = HERE / 'judgments' / f'{entry["case_id"]}-{entry["replicate"]}.json'
        require(sha(path.read_bytes()) == entry['files']['response.json'], 'Published judgment changed')
    pairs = [(validate_judgment(read(HERE/'judgments'/f'{cid}-A.json'), cid),
              validate_judgment(read(HERE/'judgments'/f'{cid}-B.json'), cid)) for cid in records]
    return metrics(pairs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate','freeze','verify','run','freeze-results','publish','analyze'])
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--case')
    parser.add_argument('--replicate', choices=['A','B'])
    args = parser.parse_args()
    if args.command == 'validate':
        print(f'{len(cases())} valid cases')
    elif args.command == 'freeze':
        freeze()
    elif args.command == 'verify':
        print(f'{len(verify())} frozen cases verified')
    elif args.command == 'run':
        records = verify()
        require(not args.case or args.case in records, 'Unknown case')
        jobs = [(cid, rep) for cid in records for rep in ('A','B')
                if (not args.case or cid==args.case) and (not args.replicate or rep==args.replicate)]
        if not args.execute:
            print(f'Offline: {len(jobs)} fresh runs requested; pass --execute to launch')
            return
        # Resume only by skipping successfully completed reservations. Failures stop.
        pending = []
        for cid, rep in jobs:
            directory = RUNTIME/cid/rep
            if directory.exists():
                require((directory/'validation.json').exists() and read(directory/'validation.json')['status']=='valid', f'Failed/incomplete reservation: {cid}/{rep}')
            else:
                pending.append((cid,rep))
        with ThreadPoolExecutor(max_workers=3) as pool:
            for result in pool.map(lambda job: run_one(*job), pending):
                print(result, flush=True)
    elif args.command == 'freeze-results':
        freeze_results()
    elif args.command == 'publish':
        publish()
    else:
        print(json.dumps(analyze(), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
