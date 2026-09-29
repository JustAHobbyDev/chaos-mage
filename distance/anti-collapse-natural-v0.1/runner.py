#!/usr/bin/env python3
"""Experiment E: immutable staged natural generation and neutral-only measurement."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import tempfile
import uuid
import yaml
import contracts as c

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OLD = HERE.parent / 'anti-collapse-v0.1'
RUNTIME = ROOT / '.runtime/anti-collapse-natural-v0.1'
STAGES = ('generation', 'neutralization', 'audit', 'validity', 'anti-collapse')
DOCS = dict(zip(STAGES, ('GENERATOR.md', 'NEUTRALIZER.md', 'AUDITOR.md', 'CLASSIFIER-validity.md', 'CLASSIFIER.md')))
OUT = dict(zip(STAGES, ('generations', 'neutralizations', 'neutralization-audit', 'validity', 'judgments')))
CHECKS = ('operation_preserved', 'signal_preserved', 'inference_preserved', 'limit_preserved', 'stopping_condition_preserved', 'next_inquiry_preserved', 'no_added_operational_content', 'no_source_imagery', 'no_verdict_language')
BANNED = ('ordinary', 'native', 'novel', 'unorthodox', 'merely', 'only formalizes', 'adds no warrant', 'new warrant', 'creative', 'same as standard practice', 'non-native', 'material departure', *c.STATUSES)
SELF_LABELS = ('novel', 'novelty', 'unorthodox', 'creative', 'creativity', 'non-native', 'material departure', *c.STATUSES)
read, require = c.read, c.require
spec = importlib.util.spec_from_file_location('e_frozen_event_audit', ROOT / 'distance/boundary-v0.2/harness.py')
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)


def now(): return datetime.now(timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()
def git(*args): return subprocess.check_output(['git', *args], cwd=ROOT)
def config(): return read(HERE / 'execution-config.json')
def manifest(): return read(HERE / 'operator-manifest.json')['mappings']
def row(cid): return next(x for x in manifest() if x['case_id'] == cid)
def source_input(cid): return read(HERE / 'generation-inputs' / f'{cid}.json')
def planned(stage): return read(HERE / 'execution-orders' / f'{stage}.json')
def canonical(stage): return HERE / 'schemas' / ('output.schema.json' if stage == 'anti-collapse' else stage + '.schema.json')
def public_path(stage, run): return HERE / OUT[stage] / (run['case_id'] + '.json' if stage in ('generation', 'neutralization') else run['id'] + '.json')


def write_new(path, value):
    copy_new(path, (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode())


def copy_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f: f.write(data)


def inventory(paths):
    return {str(p.relative_to(ROOT)): c.sha(p) for p in sorted(paths) if p.is_file() and '__pycache__' not in p.parts}


def verify_inventory(files):
    for name, digest in files.items(): require(c.sha(ROOT / name) == digest, 'Changed frozen file: ' + name)


def committed(path, revision='HEAD'):
    require(git('show', f'{revision}:{path.relative_to(ROOT)}') == path.read_bytes(), 'Uncommitted input: ' + str(path))


def checkpoint(path):
    committed(path)
    return git('log', '-1', '--format=%H', '--', str(path.relative_to(ROOT))).decode().strip()


def preservation(private=False):
    data = read(HERE / 'preservation.json')
    verify_inventory(data['files'])
    if private: verify_inventory(data['private_files'])


def normalize_words(text):
    return re.sub(r'\s+', ' ', re.sub(r'[-\u2010-\u2015_]', ' ', text.casefold()))


def wording_hits(value, phrases):
    # Inspect string values, not structural field names.
    def strings(x):
        if isinstance(x, str): return [x]
        if isinstance(x, dict): return [s for v in x.values() for s in strings(v)]
        if isinstance(x, list): return [s for v in x for s in strings(v)]
        return []
    texts = [normalize_words(t) for t in strings(value)]
    return [p for p in phrases if any(re.search(r'(?<!\w)' + re.escape(normalize_words(p)) + r'(?!\w)', t) for t in texts)]


def validate_response(value, stage, run=None):
    c.validate(value, stage, {'case_id': run['case_id']} if run and stage != 'validity' else candidate(run['case_id']) if run else None)
    if stage == 'generation':
        require(not wording_hits({'mapping': value['mapping'], 'explanation': value['explanation']}, SELF_LABELS), 'Generation self-label violation')
        if run:
            inp = source_input(run['case_id'])
            require(value['target'] == inp['target'], 'Generated target identity mismatch')
            require(value['source'] == {k: inp['source'][k] for k in ('name', 'practice')}, 'Generated source identity mismatch')
    elif stage == 'neutralization':
        require(not wording_hits(value['source_neutral'], BANNED), 'Neutralization evaluative wording violation')
    elif stage == 'audit':
        expected = 'pass' if all(x['status'] == 'pass' for x in value['checks'].values()) else 'exclude'
        require(value['overall'] == expected, 'Audit overall/check contradiction')
    return value


def published(stage):
    result = {}
    frozen = read(HERE / f'{stage}-freeze.json')
    for entry in frozen['runs']:
        if entry['validation']['status'] != 'valid': continue
        p = public_path(stage, entry)
        require(c.sha(p) == entry['response_sha256'], 'Published payload changed')
        result[(entry['case_id'], entry['family'])] = validate_response(read(p), stage, entry)
    return result


def single(stage, cid):
    values = [v for (case, _), v in published(stage).items() if case == cid]
    require(len(values) == 1, 'Missing unique upstream output')
    return values[0]


def successful_ids(stage): return {cid for cid, _ in published(stage)}


def candidate(cid):
    inp = source_input(cid)
    value = {'case_id': cid, 'source': inp['source'], 'target': {**inp['target'], 'evidence': []}, 'mapping': single('generation', cid)['mapping']}
    c.validate(value, 'candidate')
    return value


def order(stage):
    if stage == 'generation': return planned(stage)
    if stage in ('neutralization', 'validity'): ids = successful_ids('generation')
    elif stage == 'audit': ids = successful_ids('neutralization')
    else: ids = {r['case_id'] for r in read(HERE / 'admission.json')['cases'] if r['admitted']}
    return [r for r in planned(stage) if r['case_id'] in ids]


def packet_body(stage, cid):
    inp = source_input(cid)
    if stage == 'generation': return inp
    if stage == 'neutralization': return {'case_id': cid, 'target_question': inp['target']['question'], 'mapping': single('generation', cid)['mapping']}
    if stage == 'audit': return {**packet_body('neutralization', cid), 'source_neutral': single('neutralization', cid)['source_neutral']}
    if stage == 'validity': return candidate(cid)
    body = {'case_id': cid, 'target': {**inp['target'], 'evidence': []}, 'native_baseline': inp['native_baseline'], 'source_neutral': single('neutralization', cid)['source_neutral']}
    c.validate(body, 'packet')
    return body


def packet(stage, cid):
    body = packet_body(stage, cid)
    if stage in ('generation', 'anti-collapse'):
        # Embed exact baseline bytes, independent of JSON formatting of other fields.
        base = (HERE / 'baselines' / (row(cid)['target_id'] + '.json')).read_text()
        del body['native_baseline']
        payload = json.dumps(body, indent=2, ensure_ascii=False)[:-2] + ',\n  "native_baseline": ' + base + '}\n'
        json.loads(payload)
    else: payload = json.dumps(body, indent=2, ensure_ascii=False) + '\n'
    return (HERE / DOCS[stage]).read_text() + '\n\nCASE PACKET\n' + payload


def validate_inputs():
    rows = manifest()
    require(len(rows) == 30 and len({r['case_id'] for r in rows}) == 30, 'Thirty unique assignments required')
    require(Counter(r['generator_family'] for r in rows) == {'A': 15, 'B': 15}, 'Generator balance')
    require(Counter(r['target_id'] for r in rows) == {f'T{i:02}': 5 for i in range(1, 7)}, 'Target balance')
    sources = {r['source_path'] for r in rows}
    require(len(sources) == 14, 'Fourteen sources required')
    for src in sources:
        subset = [r for r in rows if r['source_path'] == src]
        require(len(subset) in (2, 3) and {r['generator_family'] for r in subset} == set('AB'), 'Source balance')
    for r in rows:
        require(set(r) == {'case_id', 'target_id', 'source_path', 'source_sha256', 'generator_family', 'neutralizer_family'}, 'Unexpected operator labels')
        require(r['generator_family'] != r['neutralizer_family'], 'Neutralizer must be cross-family')
        base_path = HERE / 'baselines' / (r['target_id'] + '.json')
        require(base_path.read_bytes() == (OLD / 'baselines' / base_path.name).read_bytes(), 'Baseline rescope')
        src = yaml.safe_load((ROOT / r['source_path']).read_text())
        require(src['extraction']['status'] == 'accepted' and c.sha(ROOT / r['source_path']) == r['source_sha256'], 'Source drift')
        inp = source_input(r['case_id'])
        require(inp == {'case_id': r['case_id'], 'target': {'domain': read(base_path)['target_domain'], 'question': read(base_path)['target_task']}, 'native_baseline': read(base_path), 'source': {'name': src['extraction']['name'], 'practice': src['extraction']['practice'], 'instrument': src['instrument']}}, 'Generation input drift')
        require(not wording_hits(packet('generation', r['case_id']), (*c.STATUSES, 'anti-collapse', 'ladder', 'diversity', 'novelty')), 'Generator prompt contaminated')
    for name in ('CLASSIFIER.md', 'CLASSIFIER-validity.md'):
        require((HERE / name).read_bytes() == (OLD / name).read_bytes(), 'Frozen classifier changed')
    for name in ('candidate', 'validity', 'output', 'validity-wire', 'anti-collapse-wire'):
        require((HERE / 'schemas' / (name + '.schema.json')).read_bytes() == (OLD / 'schemas' / (name + '.schema.json')).read_bytes(), 'Frozen schema changed')
    for stage in STAGES:
        schedule = planned(stage)
        expected = {(r['case_id'], f) for r in rows for f in ([r['generator_family']] if stage == 'generation' else [r['neutralizer_family']] if stage == 'neutralization' else 'AB')}
        require(len(schedule) == len(expected) and {(r['case_id'], r['family']) for r in schedule} == expected, 'Schedule coverage')
    return True


def prepare_stage(stage):
    verify(True)
    previous = STAGES[STAGES.index(stage) - 1]
    upstream = HERE / f'{previous}-freeze.json'
    upstream_commit = checkpoint(upstream)
    if stage == 'anti-collapse':
        verify_admission(True)
        require(read(HERE / 'admission.json')['viability']['viable'], 'Insufficient natural-output coverage')
        upstream = HERE / 'admission.json'; upstream_commit = checkpoint(upstream)
    _write_stage_inputs(stage, upstream, upstream_commit)


def _write_stage_inputs(stage, upstream=None, upstream_commit=None):
    runs = order(stage)
    for cid in sorted({r['case_id'] for r in runs}): copy_new(HERE / 'packets' / stage / (cid + '.txt'), packet(stage, cid).encode())
    write_new(HERE / 'stage-inputs' / (stage + '.json'), {'created_at': now(), 'stage': stage, 'upstream_path': str(upstream.relative_to(ROOT)) if upstream else None, 'upstream_commit': upstream_commit, 'upstream_sha256': c.sha(upstream) if upstream else None, 'runs': runs, 'files': inventory((HERE / 'packets' / stage).glob('*.txt'))})


def prepare():
    validate_inputs()
    tracked = [ROOT / p for p in git('ls-files').decode().splitlines()]
    require(not any(str(p).startswith(str(HERE)) for p in tracked), 'Already tracked preparation')
    private = [p for p in (ROOT / '.runtime').rglob('*') if p.is_file() and 'anti-collapse-natural-v0.1' not in p.parts and '__pycache__' not in p.parts]
    write_new(HERE / 'preservation.json', {'base_commit': git('rev-parse', 'HEAD').decode().strip(), 'files': inventory(tracked), 'private_files': inventory(private)})
    _write_stage_inputs('generation')
    paths = list(HERE.rglob('*')) + [ROOT / 'docs/PROBLEM_FRAMES-anti-collapse-natural-v0.1.md']
    write_new(HERE / 'prepared.json', {'created_at': now(), 'base_commit': git('rev-parse', 'HEAD').decode().strip(), 'files': inventory(paths)})


def verify(check_committed=False):
    validate_inputs(); preservation()
    prepared = read(HERE / 'prepared.json'); verify_inventory(prepared['files'])
    if check_committed:
        for name in [*prepared['files'], str((HERE / 'prepared.json').relative_to(ROOT))]: committed(ROOT / name)
    return prepared


def verify_stage_inputs(stage):
    verify(True)
    p = HERE / 'stage-inputs' / (stage + '.json'); committed(p)
    data = read(p); verify_inventory(data['files'])
    require(data['runs'] == order(stage), 'Filtered schedule drift')
    for name in data['files']: committed(ROOT / name)
    for cid in {r['case_id'] for r in data['runs']}:
        require((HERE / 'packets' / stage / (cid + '.txt')).read_text() == packet(stage, cid), 'Packet drift')
    if data['upstream_path']:
        upstream = ROOT / data['upstream_path']
        require(c.sha(upstream) == data['upstream_sha256'], 'Upstream freeze drift')
        committed(upstream, data['upstream_commit'])
        require(git('merge-base', data['upstream_commit'], 'HEAD').decode().strip() == data['upstream_commit'], 'Upstream ancestry')
    return data


def build_command(family, cwd, directory, session, stage):
    cfg = config(); model = cfg['families'][family]['requested_model']
    schema = HERE / 'schemas' / f'{stage}-wire.schema.json'
    if family == 'A':
        cmd = ['codex', 'exec', '--ignore-user-config', '--ignore-rules', '--ephemeral', '--skip-git-repo-check', '--sandbox', 'read-only', '--json', '--color', 'never', '--cd', str(cwd), '--model', model, '-c', 'model_reasoning_effort="high"', '-c', 'project_doc_max_bytes=0', '-c', 'web_search="disabled"', '--output-schema', str(schema), '--output-last-message', str(directory / 'response.json')]
        for feature in cfg['codex_disabled_features']: cmd += ['--disable', feature]
        return cmd + ['-']
    settings = {'disableAllHooks': True, 'autoMemoryEnabled': False, 'enabledPlugins': {'agents-md@builtin': False, 'telemetry@builtin': False}, 'disableClaudeAiConnectors': True, 'syncClaudeAiSkills': False, 'syncClaudeAiPlugins': False}
    return ['claude', '--print', '--safe-mode', '--setting-sources', '', '--settings', json.dumps(settings), '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}', '--tools', '', '--disable-slash-commands', '--no-session-persistence', '--session-id', session, '--model', model, '--effort', 'high', '--output-format', 'stream-json', '--verbose', '--json-schema', schema.read_text()]


def clean_environment():
    return {k: v for k, v in os.environ.items() if not k.startswith(('CODEX_', 'CLAUDE_', 'ANTHROPIC_', 'OPENAI_')) and k != 'CLAUDECODE'}


def check_fresh_session(session, directory):
    require(bool(session), 'Missing session')
    for p in RUNTIME.rglob('validation.json'):
        if p.parent != directory:
            metadata = read(p).get('metadata')
            require(not metadata or metadata['session_id'] != session, 'Session reused across stages/probes')


def probe_response(stage):
    if stage == 'generation':
        return {'case_id': 'PREFLIGHT', 'source': {'name': 'Container count', 'practice': 'Artificial fixture'}, 'target': {'domain': 'Artificial fixture', 'question': 'How many tokens are in the box?'}, 'mapping': {k: 'Count visible tokens; uncertainty remains if tokens are hidden.' for k in ('state', 'operation', 'signal', 'inference', 'limit')}, 'explanation': {k: 'Artificial formatting fixture.' for k in ('operational_chain', 'why_source_structure_applies', 'uncertainty')}}
    if stage == 'neutralization': return {'case_id': 'PREFLIGHT', 'source_neutral': {k: 'Artificial formatting fixture.' for k in ('procedure', 'action', 'observables', 'inferential_warrant', 'problem_decomposition', 'next_inquiry', 'limits')}}
    if stage == 'audit': return {'case_id': 'PREFLIGHT', 'checks': {k: {'status': 'pass', 'original_evidence': [], 'neutral_evidence': [], 'rationale': 'Artificial formatting fixture.'} for k in CHECKS}, 'overall': 'pass', 'uncertainty': []}
    if stage == 'validity': return {'case_id': 'PREFLIGHT', 'validity': {'mechanism_fidelity': {'status': 'preserved', 'rationale': 'Formatting fixture only.'}, 'target_fidelity': {'status': 'addressed', 'rationale': 'Formatting fixture only.'}, 'operational_coherence': {'status': 'coherent', 'rationale': 'Formatting fixture only.'}, 'target_reframe': {'occurred': False, 'original_question': None, 'reframed_question': None, 'relationship': None}, 'unresolved_conditions': [], 'final_status': 'Valid', 'rationale': 'Formatting fixture only.'}, 'uncertainty': []}
    return {'case_id': 'PREFLIGHT', 'anti_collapse': {'status': 'BORDERLINE_KEEP', 'departures': {k: {'status': 'uncertain', 'rationale': 'Formatting fixture only.'} for k in c.LOCI}, 'materiality': {'status': 'uncertain', 'rationale': 'Formatting fixture only.'}, 'native_reduction': {'collapses_without_loss': 'uncertain', 'closest_native_equivalent': 'Formatting fixture only.', 'lost_if_reduced': [], 'rationale': 'Formatting fixture only.'}, 'formalization': {'merely_makes_native_reasoning_explicit': 'uncertain', 'new_epistemic_constraint': None, 'rationale': 'Formatting fixture only.'}, 'decisive_reason': 'Formatting fixture only.', 'uncertainty': ['Artificial fixture.']}}


def execute(family, directory, prompt, stage, run=None):
    require(not directory.exists(), 'Attempt already reserved; no retry')
    directory.mkdir(parents=True)
    copy_new(directory / 'prompt.txt', prompt.encode())
    metadata = None; status = 'failed'; error = None; category = 'execution'
    session = str(uuid.uuid4())
    try:
        cfg = config(); version = subprocess.check_output([cfg['families'][family]['cli'], '--version'], text=True).strip()
        require(version == cfg['expected_cli_versions'][family], 'CLI version changed')
        with tempfile.TemporaryDirectory(prefix='e-isolated-') as cwd:
            require(not list(Path(cwd).iterdir()), 'Working directory not empty')
            cmd = build_command(family, cwd, directory, session, stage)
            write_new(directory / 'reservation.json', {'run': run, 'stage': stage, 'family': family, 'started_at': now(), 'input_commit': git('rev-parse', 'HEAD').decode().strip(), 'packet_sha256': sha(prompt.encode()), 'canonical_schema_sha256': c.sha(canonical(stage)), 'wire_schema_sha256': c.sha(HERE / 'schemas' / (stage + '-wire.schema.json')), 'configuration': cfg, 'cli_version': version, 'command': cmd, 'working_directory': cwd, 'working_directory_initially_empty': True, 'requested_session': session if family == 'B' else 'ephemeral', 'environment_policy': 'No inherited provider overrides or parent session; on-disk subscription authentication.'})
            with (directory / 'events.jsonl').open('x') as stdout, (directory / 'stderr.txt').open('x') as stderr:
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, text=True, cwd=cwd, env=clean_environment(), start_new_session=True)
                try: process.communicate(prompt, timeout=cfg['timeout_seconds'])
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL); process.wait(); raise
            events = [json.loads(line, object_pairs_hook=c.unique_object) for line in (directory / 'events.jsonl').read_text().splitlines() if line.strip()]
            if family == 'B':
                payloads = [e['structured_output'] for e in events if e.get('type') == 'result' and isinstance(e.get('structured_output'), dict)]
                if len(payloads) == 1: write_new(directory / 'response.json', payloads[0])
            require(process.returncode == 0, f'CLI exit {process.returncode}')
            metadata, payload = legacy.audit_events(events, family, cfg['families'][family]['requested_model'], session if family == 'B' else None)
            check_fresh_session(metadata['session_id'], directory)
            if family == 'A':
                finals = [e['item']['text'] for e in events if e.get('type') == 'item.completed' and e.get('item', {}).get('type') == 'agent_message']
                require(len(finals) == 1 and (directory / 'response.json').exists(), 'Missing unique final payload')
                # Transport identity precedes content parsing, so malformed text can be attrition.
                require(finals[0].strip() == (directory / 'response.json').read_text().strip(), 'Final stream/payload mismatch')
            else: require(read(directory / 'response.json') == payload, 'Structured stream/payload mismatch')
            category = 'content'
            value = read(directory / 'response.json')
            validate_response(value, stage, run)
            if run is None: require(value == probe_response(stage), 'Probe differs from artificial fixture')
            status = 'valid'; category = None
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
        if category == 'content' and run is not None and stage in ('generation', 'neutralization'): status = 'excluded'
    result = {'status': status, 'failure_category': category, 'error': error, 'finished_at': now(), 'metadata': metadata}
    write_new(directory / 'validation.json', result)
    return result


def stop(stage, error, run=None):
    write_new(RUNTIME / 'STOP.json', {'stage': stage, 'run': run, 'at': now(), 'error': str(error)})


def preflight(stage):
    verify_stage_inputs(stage)
    require(not (RUNTIME / 'STOP.json').exists(), 'Scheduling stopped')
    write_new(RUNTIME / f'{stage}-probe-reservation.json', {'at': now(), 'commit': git('rev-parse', 'HEAD').decode().strip()})
    entries = []
    for family in 'AB':
        directory = RUNTIME / 'probes' / stage / family
        result = execute(family, directory, 'Return exactly this artificial formatting fixture; no classification, tools or external context.\n' + json.dumps(probe_response(stage)), stage)
        entries.append({'family': family, 'validation': result, 'files': inventory(directory.iterdir()), 'reservation': read(directory / 'reservation.json') if (directory / 'reservation.json').exists() else None})
        print(f'probe {stage} {family}: {result["status"]}', flush=True)
        if result['status'] != 'valid':
            stop(stage, 'Provider probe failed'); raise ValueError('Provider probe failed; preserve and inspect failure')
    write_new(HERE / 'probes' / (stage + '.json'), {'at': now(), 'input_commit': git('rev-parse', 'HEAD').decode().strip(), 'stage_inputs_sha256': c.sha(HERE / 'stage-inputs' / (stage + '.json')), 'entries': entries})


def prerequisites(stage):
    verify_stage_inputs(stage)
    require(not (RUNTIME / 'STOP.json').exists(), 'Scheduling stopped; explicit recorded authorization required')
    path = HERE / 'probes' / (stage + '.json'); committed(path)
    probe = read(path)
    require(probe['stage_inputs_sha256'] == c.sha(HERE / 'stage-inputs' / (stage + '.json')), 'Probe input drift')
    require(len(probe['entries']) == 2 and all(x['validation']['status'] == 'valid' for x in probe['entries']), 'Two successful probes required')
    for entry in probe['entries']: verify_inventory(entry['files'])
    if stage == 'anti-collapse': verify_admission(True)


def run_all(stage):
    prerequisites(stage)
    write_new(RUNTIME / (stage + '-reservation.json'), {'at': now(), 'commit': git('rev-parse', 'HEAD').decode().strip()})
    for run in order(stage):
        try:
            prerequisites(stage)
            result = execute(run['family'], RUNTIME / stage / run['id'], packet(stage, run['case_id']), stage, run)
            print(f'{run["id"]}: {result["status"]}', flush=True)
            require(result['status'] in ('valid', 'excluded'), 'Fatal measurement failure')
        except Exception as exc:
            stop(stage, exc, run); raise


def freeze(stage):
    prerequisites(stage)
    entries = []
    stage_commit = read(RUNTIME / (stage + '-reservation.json'))['commit']
    for run in order(stage):
        directory = RUNTIME / stage / run['id']
        validation = read(directory / 'validation.json'); reservation = read(directory / 'reservation.json')
        require(validation['status'] in ('valid', 'excluded'), 'Fatal measurement cannot complete stage')
        require(reservation['input_commit'] == stage_commit, 'Commit changed during stage')
        require((directory / 'prompt.txt').read_text() == packet(stage, run['case_id']), 'Executed packet drift')
        require(reservation['packet_sha256'] == sha(packet(stage, run['case_id']).encode()), 'Reserved packet drift')
        response = directory / 'response.json'
        if validation['status'] == 'valid':
            validate_response(read(response), stage, run)
            copy_new(public_path(stage, run), response.read_bytes())
        else:
            require(stage in ('generation', 'neutralization') and validation['failure_category'] == 'content', 'Invalid content attrition')
            copy_new(HERE / 'failures' / stage / (run['id'] + '.txt'), response.read_bytes())
        entries.append({**run, 'validation': validation, 'reservation': reservation, 'response_sha256': c.sha(response), 'files': inventory(directory.iterdir())})
    write_new(HERE / (stage + '-freeze.json'), {'at': now(), 'stage': stage, 'prepared_sha256': c.sha(HERE / 'prepared.json'), 'stage_inputs_sha256': c.sha(HERE / 'stage-inputs' / (stage + '.json')), 'execution_commit': stage_commit, 'runs': entries})
    print(json.dumps({'stage': stage, 'frozen': len(entries), 'statuses': dict(Counter(x['validation']['status'] for x in entries))}))


def derive_admission():
    gen = successful_ids('generation'); neut = successful_ids('neutralization')
    audits = published('audit'); validity = published('validity'); rows = []
    for r in manifest():
        cid = r['case_id']; generated = cid in gen; neutralized = cid in neut
        a = {f: audits[(cid, f)]['overall'] if (cid, f) in audits else None for f in 'AB'}
        v = {f: validity[(cid, f)]['validity']['final_status'] if (cid, f) in validity else None for f in 'AB'}
        vv = generated and all(v[f] == 'Valid' and not validity[(cid, f)]['validity']['unresolved_conditions'] for f in 'AB')
        faithful = neutralized and all(a[f] == 'pass' for f in 'AB')
        reasons = ([] if generated else ['generation-failure']) + ([] if not generated or neutralized else ['neutralization-failure']) + ([] if not neutralized or faithful else ['neutralization-audit-exclusion']) + ([] if not generated or vv else ['validity-exclusion'])
        rows.append({'case_id': cid, 'target_id': r['target_id'], 'generation_success': generated, 'neutralization_success': neutralized, 'audit': a, 'validity': v, 'valid_valid': vv, 'audit_pass': faithful, 'admitted': bool(vv and faithful), 'exclusion_reasons': reasons})
    return rows


def viability(rows):
    admitted = [r for r in rows if r['admitted']]; targets = sorted({r['target_id'] for r in admitted})
    checks = {'at_least_18_cases': len(admitted) >= 18, 'at_least_5_targets': len(targets) >= 5}
    return {'viable': all(checks.values()), 'checks': checks, 'admitted_cases': len(admitted), 'represented_targets': targets}


def admit():
    checkpoint(HERE / 'validity-freeze.json'); checkpoint(HERE / 'audit-freeze.json')
    rows = derive_admission()
    write_new(HERE / 'admission.json', {'at': now(), 'validity_freeze_sha256': c.sha(HERE / 'validity-freeze.json'), 'audit_freeze_sha256': c.sha(HERE / 'audit-freeze.json'), 'cases': rows, 'viability': viability(rows), 'replacement_policy': 'No replacement or regeneration.'})
    print(json.dumps(viability(rows)))


def verify_admission(check_committed=False):
    data = read(HERE / 'admission.json'); rows = derive_admission()
    require(data['cases'] == rows and data['viability'] == viability(rows), 'Admission drift')
    for stage in ('validity', 'audit'): require(data[stage + '_freeze_sha256'] == c.sha(HERE / (stage + '-freeze.json')), 'Admission upstream drift')
    if check_committed: committed(HERE / 'admission.json')
    return data


def freeze_failure():
    write_new(HERE / 'failure-freeze.json', {'at': now(), 'stop': read(RUNTIME / 'STOP.json'), 'files': inventory(RUNTIME.rglob('*'))})


def fraction(n, d): return {'numerator': n, 'denominator': d, 'fraction': n / d if d else None}


def compute_metrics():
    rows = derive_admission(); meta = {r['case_id']: r for r in manifest()}
    gen = successful_ids('generation'); neut = successful_ids('neutralization'); audits = published('audit'); vv = published('validity')
    ids = sorted(r['case_id'] for r in rows if r['admitted'])
    measured = (HERE / 'anti-collapse-freeze.json').exists()
    values = published('anti-collapse') if measured else {}
    if measured: require(set(values) == {(cid, f) for cid in ids for f in 'AB'}, 'Missing or extra judgment; denominator cannot shrink')
    def statuses(cohort): return {f: {s: sum(values[(cid, f)]['anti_collapse']['status'] == s for cid in cohort) for s in c.STATUSES} for f in 'AB'}
    def agree(get): return fraction(sum(get(values[(cid, 'A')]['anti_collapse']) == get(values[(cid, 'B')]['anti_collapse']) for cid in ids), len(ids))
    def group(cohort):
        generated = [r for r in rows if r['case_id'] in cohort]; admitted = [r['case_id'] for r in generated if r['admitted']]
        return {'planned': len(generated), 'generation_successes': sum(r['generation_success'] for r in generated), 'valid_valid': sum(r['valid_valid'] for r in generated), 'primary_admitted': len(admitted), 'validity_admission_rate': fraction(sum(r['valid_valid'] for r in generated), sum(r['generation_success'] for r in generated)), 'status_distributions': statuses(admitted) if measured else None, 'departure_loci': {f: {l: dict(Counter(values[(cid, f)]['anti_collapse']['departures'][l]['status'] for cid in admitted)) for l in c.LOCI} for f in 'AB'} if measured else None}
    result = {'planned_generations': 30, 'generated_mappings': len(gen), 'generation_failures': 30 - len(gen), 'neutralization_successes': len(neut), 'neutralization_failures': len(gen) - len(neut), 'neutralization_audit_exclusions': sum(r['neutralization_success'] and not r['audit_pass'] for r in rows), 'audit_family_distributions': {f: dict(Counter(v['overall'] for (cid, ff), v in audits.items() if ff == f)) for f in 'AB'}, 'validity_family_distributions': {f: {s: sum(v['validity']['final_status'] == s for (cid, ff), v in vv.items() if ff == f) for s in ('Valid', 'Conditional', 'Invalid')} for f in 'AB'}, 'validity_admitted_mappings': sum(r['valid_valid'] for r in rows), 'validity_excluded_mappings': sum(r['generation_success'] and not r['valid_valid'] for r in rows), 'primary_admitted_mappings': len(ids), 'coverage': viability(rows), 'measurement_status': 'complete' if measured else 'insufficient natural-output coverage', 'generator_families': {f: group({cid for cid, r in meta.items() if r['generator_family'] == f}) for f in 'AB'}, 'source_instruments': {src: group({cid for cid, r in meta.items() if r['source_path'] == src}) for src in sorted({r['source_path'] for r in meta.values()})}, 'targets': {tid: group({cid for cid, r in meta.items() if r['target_id'] == tid}) for tid in sorted({r['target_id'] for r in meta.values()})}, 'attrition': rows, 'interpretation': {'accuracy_computed': False, 'joint_family_policy': None, 'population_estimate': False, 'generator_neutralizer_coupled': True}}
    if measured:
        result.update({'status_distributions': statuses(ids), 'survival_by_family': {f: fraction(sum(values[(cid, f)]['anti_collapse']['status'] != 'CLEAR_COLLAPSE' for cid in ids), len(ids)) for f in 'AB'}, 'status_agreement': agree(lambda v: v['status']), 'keep_reject_agreement': agree(lambda v: v['status'] != 'CLEAR_COLLAPSE'), 'departure_locus_agreement': {l: agree(lambda v: v['departures'][l]['status']) for l in c.LOCI}, 'materiality_agreement': agree(lambda v: v['materiality']['status']), 'native_reduction_agreement': agree(lambda v: v['native_reduction']['collapses_without_loss']), 'formalization_agreement': agree(lambda v: v['formalization']['merely_makes_native_reasoning_explicit']), 'confusion_matrix_A_rows_B_columns': {s: {t: sum(values[(cid, 'A')]['anti_collapse']['status'] == s and values[(cid, 'B')]['anti_collapse']['status'] == t for cid in ids) for t in c.STATUSES} for s in c.STATUSES}, 'clear_collapse_cases': [cid for cid in ids if any(values[(cid, f)]['anti_collapse']['status'] == 'CLEAR_COLLAPSE' for f in 'AB')], 'borderline_cases': [cid for cid in ids if any(values[(cid, f)]['anti_collapse']['status'] == 'BORDERLINE_KEEP' for f in 'AB')], 'status_disagreements': [cid for cid in ids if values[(cid, 'A')]['anti_collapse']['status'] != values[(cid, 'B')]['anti_collapse']['status']], 'same_status_locus_disagreements': [cid for cid in ids if values[(cid, 'A')]['anti_collapse']['status'] == values[(cid, 'B')]['anti_collapse']['status'] and any(values[(cid, 'A')]['anti_collapse']['departures'][l]['status'] != values[(cid, 'B')]['anti_collapse']['departures'][l]['status'] for l in c.LOCI)]})
    return result


def analyze():
    admission = verify_admission(True)
    terminal = HERE / ('anti-collapse-freeze.json' if admission['viability']['viable'] else 'admission.json')
    terminal_commit = checkpoint(terminal)
    write_new(HERE / 'review/result-binding.json', {'review_started_at': now(), 'terminal_commit': terminal_commit, 'terminal_path': str(terminal.relative_to(ROOT)), 'terminal_sha256': c.sha(terminal)})
    write_new(HERE / 'metrics.json', compute_metrics())


def execution_audit(private=False):
    sessions = []; previous = datetime.fromisoformat(read(HERE / 'prepared.json')['created_at']); stages = {}
    for stage in STAGES:
        freeze_path = HERE / (stage + '-freeze.json')
        if not freeze_path.exists(): continue
        verify_stage_inputs(stage)
        probe_path = HERE / 'probes' / (stage + '.json'); probe = read(probe_path)
        for entry in probe['entries']:
            sessions.append(entry['validation']['metadata']['session_id'])
            if private: verify_inventory(entry['files'])
        data = read(freeze_path)
        require(data['prepared_sha256'] == c.sha(HERE / 'prepared.json'), 'Prepared freeze binding')
        require(data['stage_inputs_sha256'] == c.sha(HERE / 'stage-inputs' / (stage + '.json')), 'Stage freeze binding')
        require([{k: x[k] for k in ('id', 'case_id', 'family')} for x in data['runs']] == order(stage), 'Freeze coverage drift')
        require(data['execution_commit'] == checkpoint(probe_path), 'Measurement not at probe checkpoint')
        returned = {f: set() for f in 'AB'}; retries = {f: 0 for f in 'AB'}
        for entry in data['runs']:
            v, reservation = entry['validation'], entry['reservation']; m = v['metadata']
            require(v['status'] in ('valid', 'excluded') and m, 'Unsuccessful execution')
            start = datetime.fromisoformat(reservation['started_at']); end = datetime.fromisoformat(v['finished_at'])
            require(previous <= start <= end and datetime.fromisoformat(probe['at']) <= start, 'Execution chronology')
            previous = end; sessions.append(m['session_id'])
            require(reservation['input_commit'] == data['execution_commit'], 'Stage spans commits')
            require(reservation['configuration'] == config(), 'Execution configuration drift')
            require(reservation['packet_sha256'] == sha(packet(stage, entry['case_id']).encode()), 'Executed packet drift')
            require(reservation['canonical_schema_sha256'] == c.sha(canonical(stage)) and reservation['wire_schema_sha256'] == c.sha(HERE / 'schemas' / (stage + '-wire.schema.json')), 'Executed schema drift')
            returned[entry['family']].update(m['returned_model_identifiers']); retries[entry['family']] += m['formatting_retries']['observed_formatting_retries']
            if private: verify_inventory(entry['files'])
        require(previous <= datetime.fromisoformat(data['at']), 'Freeze chronology'); previous = datetime.fromisoformat(data['at'])
        stages[stage] = {'attempts': len(data['runs']), 'valid': sum(x['validation']['status'] == 'valid' for x in data['runs']), 'excluded': sum(x['validation']['status'] == 'excluded' for x in data['runs']), 'execution_commit': data['execution_commit'], 'freeze_commit': checkpoint(freeze_path), 'returned_identifiers': {f: sorted(returned[f]) for f in 'AB'}, 'exposed_formatter_retries': retries}
    require(len(sessions) == len(set(sessions)), 'Session reused')
    return {'stages': stages, 'unique_sessions_including_probes': len(sessions), 'harness_retries': 0, 'replacement_measurements': 0, 'verified_served_snapshots': {'A': None, 'B': None}}


def verify_results(private=False):
    verify(True); preservation(private)
    if (HERE / 'failure-freeze.json').exists():
        data = read(HERE / 'failure-freeze.json')
        if private: verify_inventory(data['files'])
        return {'status': 'incomplete', 'failure': data['stop']}
    admission = verify_admission(True)
    require(read(HERE / 'metrics.json') == compute_metrics(), 'Metrics do not recompute')
    audit = execution_audit(private)
    if (HERE / 'review/execution-audit.json').exists(): require(read(HERE / 'review/execution-audit.json') == audit, 'Execution audit drift')
    binding = read(HERE / 'review/result-binding.json'); terminal = ROOT / binding['terminal_path']
    require(c.sha(terminal) == binding['terminal_sha256'], 'Review binding drift')
    committed(terminal, binding['terminal_commit'])
    require(datetime.fromisoformat(binding['review_started_at']) > datetime.fromisoformat(read(terminal)['at']), 'Review before freeze')
    return {'status': 'complete' if admission['viability']['viable'] else 'insufficient natural-output coverage', 'generated': len(successful_ids('generation')), 'primary_admitted': admission['viability']['admitted_cases'], 'targets': len(admission['viability']['represented_targets']), 'sessions': audit['unique_sessions_including_probes']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['validate', 'prepare', 'verify', 'prepare-stage', 'preflight', 'run', 'freeze', 'admit', 'analyze', 'verify-results', 'freeze-failure'])
    p.add_argument('--stage', choices=STAGES, default='generation'); p.add_argument('--private', action='store_true'); a = p.parse_args()
    if a.command == 'validate': print(validate_inputs())
    elif a.command == 'prepare': prepare()
    elif a.command == 'verify': verify(); print('Prepared inputs verified')
    elif a.command == 'prepare-stage': prepare_stage(a.stage)
    elif a.command == 'preflight': preflight(a.stage)
    elif a.command == 'run': run_all(a.stage)
    elif a.command == 'freeze': freeze(a.stage)
    elif a.command == 'admit': admit()
    elif a.command == 'analyze': analyze()
    elif a.command == 'verify-results': print(verify_results(a.private))
    else: freeze_failure()


if __name__ == '__main__': main()
