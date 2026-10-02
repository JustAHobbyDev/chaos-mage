"""Offline H.5 authoring/publication gate. No provider adapter or network client."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import segment
import validate

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
OLD = H.with_name('inquiry-unitization-calibration-v0.1')
BASE = 'bdeeb973b794823a35257f472a020e12d816a8a9'
BRANCH = 'experiment-h5-span-provenance'
REPORT = ROOT / 'distance/review/span-provenance-calibration-v0.1.md'
FRAME = ROOT / 'docs/PROBLEM_FRAMES-span-provenance-calibration-v0.1.md'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return str(path.relative_to(ROOT))


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def allowed(path):
    return path.startswith(rel(H) + '/') or path in (rel(REPORT), rel(FRAME))


def hashes(files):
    for path, digest in files.items():
        file = ROOT / path
        require(file.is_file() and sha(file) == digest, 'INTEGRITY_FILE: ' + path)


def preservation():
    inventory = read(H / 'preservation.json')
    require(inventory['baseline'] == BASE, 'INTEGRITY_BASELINE')
    hashes(inventory['tracked']); hashes(inventory['runtime'])
    require(git('branch', '--show-current') == BRANCH, 'INTEGRITY_BRANCH')
    require(git('merge-base', BASE, 'HEAD') == BASE, 'INTEGRITY_ANCESTRY')
    changes = git('diff', '--name-only', BASE, '--').splitlines()
    changes += git('ls-files', '--others', '--exclude-standard').splitlines()
    require(all(allowed(path) for path in changes), 'INTEGRITY_CHANGED_PATHS')
    # Preserve pre-existing exact integrity machinery, not merely our own snapshot.
    for name in ('publication-manifest.json', 'final-runtime-freeze.json'):
        hashes(read(OLD / name)['files'])
    return {'tracked_files': len(inventory['tracked']), 'runtime_files': len(inventory['runtime']),
            'historical_integrity_manifests_verified': True, 'unchanged': True}


def evaluate():
    manifest = read(H / 'manifest.json')
    require(manifest['base_sha'] == BASE and manifest['provider_calls'] == 0, 'Manifest lineage')
    sources = manifest['sources']
    require(len(sources) == 20 and len({x['packet_id'] for x in sources}) == 20, 'Twenty unique mappings')
    historical = preservation()
    frozen_tables = read(H / 'span-tables-freeze.json')
    hashes(frozen_tables['files'])
    require(set(frozen_tables['files']) == {rel(p) for p in (H / 'span-tables').glob('*.json')}, 'Table inventory drift')
    tables, field_counts, distribution, ambiguities = {}, Counter(), [], []
    for source in sources:
        path = ROOT / source['path']
        require(sha(path) == source['sha256'], 'INTEGRITY_SOURCE')
        data = read(path); packet = source['packet_id']
        require(data['case_id'] == packet, 'Packet identity')
        table = read(H / 'span-tables' / (packet + '.json'))
        require(not validate.schema_errors('span-table', table), 'Table schema')
        segment.verify_table(table, data['mapping'])
        require(table == segment.segment(packet, data['mapping']), 'Determinism')
        require(json.loads(json.dumps(table, ensure_ascii=True)) == table, 'Round-trip')
        count = Counter(row['field'] for row in table['spans'].values())
        distribution.append({'packet_id': packet, 'total': len(table['spans']),
                             'by_field': {field: count[field] for field in segment.FIELDS}})
        field_counts.update(count); tables[packet] = table
        ambiguities.extend({'packet_id': packet, **item} for item in table['ambiguities'])
    require(sum(field_counts.values()) == frozen_tables['total_spans'], 'Span count drift')
    entries = read(H / 'fixtures-freeze.json')['fixtures']
    hashes({entry['path']: entry['sha256'] for entry in entries})
    require(set(entry['path'] for entry in entries) == {rel(p) for p in (H / 'fixtures').glob('*/*.json')}, 'Fixture inventory drift')
    results, failures, codes, statuses, categories = [], [], Counter(), Counter(), {}
    fixtures = {}
    for entry in entries:
        f = read(ROOT / entry['path']); fid = f['fixture_id']; fixtures[fid] = f
        review_path = H / 'review' / (fid + '.json')
        result = validate.validate_fixture(tables[entry['table_packet_id']], f,
                                          read(review_path) if review_path.exists() else None)
        actual_mechanical = [error['code'] for error in result['mechanical_errors']]
        matched = (not result['review_errors'] and sorted(actual_mechanical) == sorted(f['expected_mechanical_codes']))
        if result['mechanically_valid']:
            expected = {c['component_id']: (c['expected_support_status'], c['expected_codes']) for c in f['components']}
            actual = {c['component_id']: (c['support_status'], c['codes']) for c in result['components']}
            matched = matched and actual == expected
        else:
            matched = matched and all(c['expected_support_status'] is None for c in f['components'])
        if not matched:
            failures.append(fid)
        codes.update(actual_mechanical)
        for row in result['components']:
            statuses[row['support_status']] += 1; codes.update(row['codes'])
        categories.setdefault(f['category'], {'fixtures': 0, 'expectations_met': 0})
        categories[f['category']]['fixtures'] += 1
        categories[f['category']]['expectations_met'] += int(matched)
        results.append({**result, 'category': f['category'], 'expectations_met': bool(matched)})
    # Compare recorded unit interpretations with frozen H.4 expectations and H.3 counts.
    units = read(H / 'review/unit-semantics.json')['cases']
    historical_counts = {row['case_id']: row['expected_complete'] for row in read(OLD / 'manifest.json')['cases']}
    historical_counts.update({'H3-4d30014ef73c': 1, 'H3-d6134c9f4c74': 1})
    require(Counter(row['fixture_id'] for row in units) == Counter(historical_counts.keys()), 'Unit review coverage')
    for row in units:
        f = fixtures[row['fixture_id']]
        require(row['fixture_sha256'] == segment.canonical_hash(f), 'Unit review binding')
        require(row['complete_units'] == historical_counts[row['fixture_id']] == f['expected_complete_units'], 'Inquiry semantics changed')
        require(row['semantic_unit_ids'] == (['IQ1'] if row['complete_units'] else []), 'Unit identity/deduplication changed')
        require(row['role'] == ('INQUIRY_CONSTRAINT' if row['complete_units'] else 'NOT_INQUIRY_CONSTRAINT'), 'Inquiry role changed')
    regression_ids = ('H4-f070ba17a9b7', 'H4-86f4954813b3', 'H3-4d30014ef73c', 'H3-d6134c9f4c74')
    regressions = {fid: {'expectations_met': next(row['expectations_met'] for row in results if row['fixture_id'] == fid),
                         'recorded_complete_units': historical_counts[fid]} for fid in regression_ids}
    require(not failures, 'Unexpected fixture failures: ' + ', '.join(failures))
    metrics = {'status': 'COMPLETE', 'base_sha': BASE, 'branch': BRANCH, 'provider_calls': 0,
               'mappings_segmented': len(tables), 'total_spans': sum(field_counts.values()),
               'span_count_by_field': {field: field_counts[field] for field in segment.FIELDS},
               'span_count_distribution': distribution, 'segmentation_ambiguities': ambiguities,
               'fixture_results': categories, 'reviewed_component_statuses': dict(statuses),
               'validation_failure_occurrences': {code: codes[code] for code in validate.CODES},
               'regressions': regressions, 'unexpected_failures': failures,
               'h4_semantics_preserved': True, 'historical_preservation': historical,
               'semantic_assessment': 'Recorded Codex engineering review; not an automatic entailment test or independent rating.',
               'coarse_spans_caused_support_ambiguity': False,
               'uncertainty': 'The meaning of ordinary lock waits is plausible but undefined; the ambiguity is lexical, not caused by coarse spans.',
               'model_authored_exact_text_or_offsets_required': False,
               'semantic_reference_identity': 'opaque packet-local span IDs in a bound packet envelope',
               'exact_hashing_retained_for_integrity': True,
               'corpus_list_table_former_latter_coverage': False,
               'synthetic_harness_tests_excluded_from_corpus': True,
               'recommended_next_step': 'Design a separately authorized broader-language provenance challenge with independent semantic review; make no new provider calls or production integration as part of H.5.'}
    return metrics, results


def test_runs():
    results = []
    for directory in (H / 'tests', OLD / 'tests'):
        command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', rel(directory), '-p', 'test_*.py']
        process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
        output = process.stdout + process.stderr
        require(process.returncode == 0, 'Test failure: ' + output)
        match = re.search(r'Ran (\d+) tests?', output)
        results.append({'command': command, 'exit_code': process.returncode,
                        'test_count': int(match[1]) if match else None, 'output': output})
    return results


def render(metrics):
    m = metrics
    lines = ['# H.5 — Neutral span provenance calibration v0.1', '',
             'The bounded offline calibration passes its engineering expectations. All 20 frozen mappings resolve through opaque span IDs; historical scientific results remain unchanged. Semantic support was reviewed explicitly by Codex, not established by an automated semantic evaluator or independent rater.', '',
             f'Base: `{BASE}`. Branch: `{BRANCH}`. Provider calls: **0**. No main merge.', '',
             '## Checkpoints', '', '| Checkpoint | SHA |', '|---|---|']
    lines += [f'| {name} | `{value}` |' for name, value in m['checkpoints'].items()]
    lines += ['', 'The final SHA is the commit containing publication-manifest.json; resolve it with `git log -1 --format=%H -- distance/span-provenance-calibration-v0.1/publication-manifest.json`.', '',
              '## Segmentation and provenance contract', '',
              'One conservative Python splitter applies equally to state, operation, signal, inference and limit. It preserves explicit blocks first, splits prose only at safe sentence boundaries, and retains ambiguity. No clause-, role-, or length-based segmentation occurs. Lists retain item/parent structure; pipe tables retain rows and header context. Those structures are tested synthetically because none occur in the frozen corpus.', '',
              'Packet-local P001, P002, … IDs identify harness-owned text. Field, block, sentence and harness-only character ranges are separate metadata. The annotation envelope binds a packet; refs contain only source_id and SUPPORT/CONTEXT. A wrong envelope is rejected, but an accidentally copied local ID that also exists locally cannot reveal its foreign origin by itself.', '',
              'SUPPORT contributes substantive content; CONTEXT resolves identities, antecedents, conditions and scope. The cited bundle must recover the entire claimed component through ordinary comprehension. Multiple SUPPORT spans, extra propositions, reused spans and nonminimal context are allowed. Context cannot invent an outcome relation, and a claim cannot broaden qualifiers. Review returns only SUFFICIENT, INSUFFICIENT or UNCERTAIN.', '',
              'The mechanical validator checks schema, packet binding, ID existence, SUPPORT presence, duplicates and role conflicts. Separate frozen review records assess meaning. Replay validates the review binding and expected diagnostics; it is not independent confirmation of semantic judgments. Missing review remains unassessed.', '',
              '## Corpus and fixture results', '',
              f'Mappings: **{m["mappings_segmented"]}**. Total spans: **{m["total_spans"]}**.', '',
              '| Field | Spans | Min per mapping | Max per mapping |', '|---|---:|---:|---:|']
    for field, count in m['span_count_by_field'].items():
        values = [row['by_field'][field] for row in m['span_count_distribution']]
        lines.append(f'| {field} | {count} | {min(values)} | {max(values)} |')
    lines += ['', 'Full per-mapping distributions and retained-boundary diagnostics are in metrics.json.', '',
              '| Fixture group | Fixtures | Expectations met |', '|---|---:|---:|']
    lines += [f'| {name} | {row["fixtures"]} | {row["expectations_met"]} |' for name, row in m['fixture_results'].items()]
    lines += ['', 'Component review statuses: ' + json.dumps(m['reviewed_component_statuses'], sort_keys=True) + '.', '',
              'Positive coverage includes single propositions, coarse multi-proposition spans, reuse, joint support, distributed state/operation/signal bundles, pronouns and scoped relations. Negative fixtures deliberately isolate unknown IDs, absent SUPPORT, duplicate/conflicting refs, wrong packet, missing context, absent differential relations, an uncited substantive premise and scope overreach. These are engineering fixtures, not replacement provider observations.', '',
              '| Regression | Result | Complete inquiry units |', '|---|---|---:|']
    lines += [f'| {fid} | {"pass" if row["expectations_met"] else "FAIL"} | {row["recorded_complete_units"]} |' for fid, row in m['regressions'].items()]
    lines += ['', 'The punctuation control retains the generic request and its incomplete-inquiry interpretation despite the annotation omitting terminal punctuation. The duplicate-offset control cites both textual formulations by ID, preserving one IQ1. Both H.3 affirmative tests remain recoverable with case and scope context. None of the original H.4/H.3 judgments or historical failures was repaired.', '',
              '## Diagnostics and ambiguity', '',
              'Counts below are expected fixture diagnostics, not provider failure rates. Synthetic unit-test injections are excluded.', '',
              '| Code | Occurrences |', '|---|---:|']
    lines += [f'| {code} | {count} |' for code, count in m['validation_failure_occurrences'].items()]
    lines += ['', 'PROV_SCHEMA and PROV_CONFLICT_REVIEW have dedicated synthetic tests. A conflict signal requires an explicit reviewed incompatibility, matching component type and packet/target scope, and materially overlapping SUPPORT. It never automatically invalidates an annotation. REVIEW_* failures concern missing/stale/malformed review machinery; INTEGRITY_* failures concern changed artifacts, not semantic support.', '',
              f'Retained uncertain boundaries: {len(m["segmentation_ambiguities"])}. These arise from lowercase following sentences or single-digit numeric endings treated conservatively as possible initials. Some crossdating, delta and diagnosis spans consequently contain multiple sentences. No reviewed component became ambiguous because of this coarseness.', '',
              m['uncertainty'] + ' Its UNCERTAIN review is retained rather than forced to pass or fail.', '',
              '## Verification, limitations and next step', '',
              'Tests: ' + ', '.join(f'{row["test_count"]} passing in {row["command"][-3]}' for row in m['test_runs']) + '.', '',
              'Historical preservation: ' + json.dumps(m['historical_preservation'], sort_keys=True) + '.', '',
              'Model-authored exact-text and offset requirements are removed from the new citation schema and validator. Terminal punctuation, quote shape, whitespace, line endings and JSON escaping do not determine semantic citation validity. Exact comparison remains appropriate for frozen source, span-table, fixture, review, historical-result and raw-response integrity; a changed source is a changed input.', '',
              'H.5 establishes a usable bounded provenance mechanism for future separately authorized semantic experiments. It does not establish general semantic reliability, independent agreement, model compliance, robust parsing of arbitrary markup, or production readiness. The splitter deliberately under-segments and supports only explicit lightweight authored structures. Real lists/tables and former/latter language are absent from this corpus; their tests exercise plumbing only. Recorded semantic reviews remain fallible operator judgments. A valid ID alone cannot establish support.', '',
              '**Recommended next step:** ' + m['recommended_next_step'], '',
              'Recommendation not executed. Work stops after H.5: no new natural outputs, Experiment E, provider calls, historical rewrites, production integration or merge to main.', '']
    return '\n'.join(lines)


def record():
    require(not (H / 'publication-manifest.json').exists(), 'Publication already sealed')
    metrics, results = evaluate()
    paths = {'architecture_and_contract': H / 'PROTOCOL.md', 'segmentation_and_schemas': H / 'segment.py',
             'twenty_span_tables': H / 'span-tables-freeze.json', 'engineering_fixtures': H / 'fixtures-freeze.json',
             'reviews_validator_and_tests': H / 'validate.py'}
    checkpoints = {name: git('log', '-1', '--format=%H', '--', rel(path)) for name, path in paths.items()}
    require(all(checkpoints.values()), 'All implementation checkpoints must be committed before calibration')
    metrics['checkpoints'] = checkpoints
    metrics['test_runs'] = test_runs()
    for row in results:
        write(H / 'validation' / (row['fixture_id'] + '.json'), row)
    write(H / 'metrics.json', metrics)
    REPORT.write_text(render(metrics))
    return metrics


def seal():
    require(not (H / 'publication-manifest.json').exists(), 'Publication already sealed')
    files = sorted(p for p in H.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    files += [REPORT, FRAME]
    write(H / 'publication-manifest.json', {'status': 'COMPLETE', 'checkpoint_before_publication': git('rev-parse', 'HEAD'),
                                           'files': {rel(p): sha(p) for p in files}})


def verify():
    publication = read(H / 'publication-manifest.json')
    hashes(publication['files'])
    actual = {rel(p) for p in H.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name != 'publication-manifest.json'} | {rel(REPORT), rel(FRAME)}
    require(set(publication['files']) == actual, 'Publication inventory drift')
    current, results = evaluate(); frozen = read(H / 'metrics.json')
    require({k: value for k, value in frozen.items() if k not in ('test_runs', 'checkpoints')} == current, 'Metrics drift')
    require(REPORT.read_text() == render(frozen), 'Report drift')
    for row in results:
        require(read(H / 'validation' / (row['fixture_id'] + '.json')) == row, 'Validation drift')
    for checkpoint in frozen['checkpoints'].values():
        require(git('merge-base', checkpoint, 'HEAD') == checkpoint, 'Checkpoint ancestry')
    return frozen


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'record', 'seal', 'verify'])
    action = parser.parse_args().action
    result = evaluate()[0] if action == 'check' else globals()[action]()
    if result:
        print(json.dumps({key: result[key] for key in ('status', 'provider_calls', 'mappings_segmented', 'total_spans',
                                                       'fixture_results', 'regressions', 'unexpected_failures',
                                                       'historical_preservation')}, indent=2))
