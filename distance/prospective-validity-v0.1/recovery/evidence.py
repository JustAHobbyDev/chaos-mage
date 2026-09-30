"""Read-only recovery gates, checkpoint-scoped legacy checks, and history suite."""
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
import concurrent.futures
import io
import json
import subprocess
import sys
import tarfile

HERE = Path(__file__).resolve().parent
F = HERE.parent
ROOT = F.parent.parent
sys.path.insert(0, str(F))
import runner as old
import contracts as c

ORIGINAL = '00a2bc81bf4d1f4c2e8b6827d7d50b060b544000'
PREP = '5539960'
BASE = 'da8cb8d91505d68e65ea8f2d3910f4ca34a03c3b'
POLICY = ROOT / 'docs/EXPERIMENT-RECOVERY-POLICY.md'
REPORT = ROOT / 'distance/review/prospective-validity-v0.1-recovery.md'
CLASSES = {'recoverable_integrity_violation', 'measurement_lineage_violation', 'ambiguous_impact'}


def original_manifest():
    data = old.git('archive', ORIGINAL)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        return {m.name: c.digest(archive.extractfile(m).read()) for m in archive if m.isfile()}


def preservation(manifest=None):
    manifest = manifest or original_manifest()
    old.verify_hashes(manifest)
    allowed = {old.rel(POLICY), old.rel(REPORT)}
    changed = old.git('diff', '--name-only', ORIGINAL, '--').decode().splitlines()
    untracked = old.git('ls-files', '--others', '--exclude-standard').decode().splitlines()
    for name in set(changed + untracked):
        c.require(name not in manifest, 'Original publication changed: ' + name)
        c.require(name in allowed or name.startswith(old.rel(HERE) + '/'), 'Unauthorized addition: ' + name)
    old.verify_hashes(c.read(F / 'failure-freeze.json')['files'])
    c.require(old.inventory(old.RUNTIME.rglob('*')) == c.read(F / 'failure-freeze.json')['files'],
              'Original execution inventory changed')
    return {'original_tracked_files': len(manifest), 'original_runtime_unchanged': True}


@contextmanager
def checkpoint_scope():
    """Only legacy Git diff is scoped; all original bytes/runtime are checked live."""
    git = old.git
    def scoped(*args):
        if args == ('diff', '--name-only', BASE, '--'):
            return git('diff', '--name-only', BASE, ORIGINAL, '--')
        return git(*args)
    with patch.object(old, 'git', scoped):
        yield


def legacy_check(tests=False):
    preservation()
    sys.path.insert(0, str(F / 'review'))
    import verify_incomplete
    with checkpoint_scope():
        result = verify_incomplete.verify()
        if tests:
            import unittest
            suite = unittest.defaultTestLoader.discover(str(F / 'tests'))
            run = unittest.TextTestRunner(verbosity=1).run(suite)
            c.require(run.wasSuccessful(), 'Original F tests failed')
            result['tests'] = run.testsRun
    return result


def history():
    commands = [x['command'] for x in c.read(F / 'review/historical-verification-restored.json')['checks']]
    def check(command):
        result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=600)
        return {'command': command, 'exit_code': result.returncode, 'output': result.stdout}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(check, commands))
    result = {'at': old.now(), 'input_commit': old.head(), 'provider_calls': 0,
              'checks': results, 'legacy_F': legacy_check(tests=True), 'preservation': preservation()}
    c.require(all(x['exit_code'] == 0 for x in results), 'Historical checks failed')
    return result


def audit():
    """Reconstruct all ten gates; exceptions refuse a recoverable classification."""
    preserved = preservation()
    terminal = legacy_check()
    old.binary_check()
    fix = c.read(F / 'review/preservation-correction.json')
    restored = (ROOT / fix['historical_path']).read_bytes()
    bad = (ROOT / fix['executed_preparation_document_archive']).read_bytes()
    c.require(restored == old.git('show', BASE + ':' + fix['historical_path']), 'Historical restoration mismatch')
    c.require(bad == old.git('show', PREP + ':' + fix['historical_path']), 'Archive mismatch')
    c.require(bad.startswith(restored), 'Unexpected document modification shape')
    addition = bad[len(restored):].strip()
    # Rebuild every packet from the original taxonomy and explicit source allowlist.
    old.verify_imports()
    taxonomy = old.git('show', PREP + ':' + old.rel(F / 'TAXONOMY.md'))
    entries = [c.read(F / 'probes/taxonomy.json')['entry'], *c.read(F / 'taxonomy-partial-freeze.json')['runs']]
    results = []
    for entry in entries:
        reservation = entry['reservation']
        identity, kind = reservation['identity'], reservation['kind']
        directory = old.RUNTIME / kind / 'taxonomy' / identity
        prompt = (directory / 'prompt.txt').read_bytes()
        if kind == 'runs':
            packet = F / 'packets/taxonomy' / (identity + '.txt')
            expected = old.git('show', PREP + ':' + old.rel(packet))
            c.require(prompt.startswith(taxonomy), 'Executed taxonomy definitions differ')
        else:
            expected = ('Return exactly this artificial schema fixture. No classification, tools or external context.\n'
                        + json.dumps(old.probe_fixture('taxonomy'))).encode()
        c.require(prompt == expected and c.digest(prompt) == reservation['packet_sha256'], 'Prompt identity mismatch')
        c.require(bad not in prompt and addition not in prompt, 'Changed document reached prompt')
        c.require(not any(line.strip() in prompt for line in addition.splitlines() if len(line.strip()) > 60),
                  'Changed document excerpt reached prompt')
        for suffix, key in [('', 'canonical_schema_sha256'), ('-wire', 'wire_schema_sha256')]:
            schema = F / 'schemas' / ('taxonomy' + suffix + '.schema.json')
            c.require(c.digest(old.git('show', PREP + ':' + old.rel(schema))) == reservation[key], 'Executed schema mismatch')
        cfg = json.loads(old.git('show', PREP + ':' + old.rel(F / 'execution-config.json')))
        c.require(reservation['configuration'] == cfg, 'Executed configuration mismatch')
        c.require(reservation['working_directory_initially_empty'] and reservation['requested_session'] == 'ephemeral',
                  'Missing isolation evidence')
        c.require(reservation['command'] == old.command(reservation['working_directory'], directory, 'taxonomy'),
                  'Isolation command mismatch')
        old.verify_hashes(entry['files'])
        process = c.read(directory / 'process.json')
        metadata = entry['validation']['metadata']
        results.append({'identity': identity, 'kind': kind, 'prompt_sha256': c.digest(prompt),
                        'canonical_schema_sha256': reservation['canonical_schema_sha256'],
                        'wire_schema_sha256': reservation['wire_schema_sha256'],
                        'configuration_sha256': c.sha(F / 'execution-config.json'),
                        'taxonomy_sha256': c.digest(taxonomy), 'response_sha256': c.sha(directory / 'response.json'),
                        'validation_sha256': c.sha(directory / 'validation.json'), 'files': entry['files'],
                        'pid': process['pid'], 'session_id': metadata['session_id'], 'gates_1_through_7': 'pass'})
    c.require(len({x['pid'] for x in results}) == 5 and len({x['session_id'] for x in results}) == 5, 'Isolation identity reuse')
    source_checks = {}
    for name in ('prepare.py', 'runner.py', 'contracts.py'):
        path = F / name
        c.require(path.read_bytes() == old.git('show', PREP + ':' + old.rel(path)), 'Executed code changed')
        source_checks[old.rel(path)] = c.sha(path)
    graph = {
        'taxonomy_prompt': ['TAXONOMY.md', 'imports/candidates/<case>.json', 'atomic condition exact span', 'parent exact excerpt'],
        'candidate': ['frozen Experiment E generation source, target, five-field mapping'],
        'schema': ['contracts.schema(taxonomy)', 'contracts.wire(canonical schema)'],
        'artificial_prompt': ['runner.probe_fixture(taxonomy)', 'fixed serialization prefix'],
        'provider_input': ['stdin prompt', 'wire schema', 'pinned CLI and command', 'filtered environment'],
        'historical_document': ['preparation integrity hash only; no value flows to prompt, schema or configuration'],
        'isolation': ['fresh Popen/start_new_session', 'empty temporary cwd', 'ephemeral thread',
                      'ignore user config/rules', 'project_doc_max_bytes=0', 'disabled tools/plugins/memories',
                      'clean_environment removes provider and parent-context overrides', 'raw event audit permits no tool activity'],
        'executed_source_hashes': source_checks,
        'proof_method': 'Exact reconstruction of every frozen packet; exact executed stdin comparison; frozen source dataflow and launch audit; immutable event/response hashes.'}
    return {'original_incomplete_commit': ORIGINAL, 'classification': 'recoverable_integrity_violation',
            'violation': {'path': fix['historical_path'], 'type': 'historical_preservation',
                          'detected_at': c.read(F / 'failure-freeze.json')['stop']['at'], 'provider_calls_already_completed_or_in_flight': 5},
            'remediation': fix, 'measurements': results, 'dependency_graph': graph,
            'measurement_dependency_audit': {'affected_packets': [], 'affected_configs': [], 'affected_schemas': [],
                                           'affected_responses': [], 'model_context_exposure': False},
            'gates_8_through_10': {'historical_restoration': 'pass', 'historical_checks': 'separate bound history report required',
                                 'dependency_analysis': 'pass'},
            'preservation': preserved, 'original_terminal_verification': terminal,
            'resume_authorization': old.rel(HERE / 'AUTHORIZATION.md'), 'resume_from': old.order('taxonomy')[4],
            'limitations': ['Served model snapshot not exposed; requested alias is not proof of immutable backend identity.',
                           'Isolation proof is based on pinned executed code/configuration and captured events, not unobservable provider internals.']}


def gate(record):
    c.require(record['classification'] in CLASSES, 'Unknown recovery classification')
    c.require(record['classification'] == 'recoverable_integrity_violation', 'Recovery does not permit resume')
    proof = audit()
    c.require(record['audit'] == proof, 'Recovery audit no longer reproduces')
    report = ROOT / record['historical_checks']['path']
    c.require(c.sha(report) == record['historical_checks']['sha256'], 'Historical report binding changed')
    checks = c.read(report)
    c.require(len(checks['checks']) == 36 and all(x['exit_code'] == 0 for x in checks['checks']), 'Historical checks incomplete')
    c.require(checks['legacy_F']['tests'] == 37, 'Legacy F tests missing')
    return proof


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('action', choices=['history', 'audit', 'legacy-tests']); p.add_argument('--output')
    args = p.parse_args()
    value = history() if args.action == 'history' else legacy_check(True) if args.action == 'legacy-tests' else audit()
    if args.output: old.write(Path(args.output), value)
    else: print(json.dumps(value, indent=2))
