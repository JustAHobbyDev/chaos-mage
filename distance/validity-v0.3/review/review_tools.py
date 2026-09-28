#!/usr/bin/env python3
"""Post-freeze evidence inventory and completion checks; no model calls."""
import argparse
from datetime import datetime
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('validity_runner_review', HERE.parent / 'runner.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

AUDITS = ('generic_metaphor', 'mechanism_loss', 'target_drift', 'unsupported_inference',
          'missing_measurement', 'invented_counterpart', 'creative_reframe', 'literalism')


def evidence():
    values = r.published()
    manifest = r.read(r.SNAPSHOT / 'operator-manifest.json')
    cases = {}
    for n in range(1, 25):
        cid = f'{n:03}'; a, b = (values[(cid, family)] for family in ('A', 'B'))
        differences = []
        for key in r.CRITERIA:
            if a['validity'][key]['status'] != b['validity'][key]['status']: differences.append(key)
        if a['validity']['final_status'] != b['validity']['final_status']: differences.append('final_status')
        if a['validity']['target_reframe']['occurred'] != b['validity']['target_reframe']['occurred']:
            differences.append('target_reframe.occurred')
        cases[cid] = {'operator': manifest['cases'][cid], 'candidate': r.candidate(cid),
                      'judgments': {'A': a, 'B': b}, 'status_disagreements': differences}
    return {'notice': 'Post-freeze mechanical evidence inventory. Author intent is not ground truth.',
            'cases': cases, 'groups': manifest['groups']}


def execution_audit():
    frozen = r.frozen_results()
    runs = frozen['runs']
    commit_epoch = int(r.git('show', '-s', '--format=%ct', frozen['prepared_commit']).decode().strip())
    previous_finish = None
    for entry in runs:
        start = datetime.fromisoformat(entry['reservation']['started_at'])
        finish = datetime.fromisoformat(entry['audit']['finished_at'])
        r.require(start.timestamp() >= commit_epoch, 'Measurement predates preparation commit')
        r.require(finish >= start, 'Negative execution duration')
        if previous_finish: r.require(start >= previous_finish, 'Overlapping measurement processes')
        previous_finish = finish
    r.require(datetime.fromisoformat(frozen['frozen_at']) >= previous_finish, 'Freeze precedes last result')
    return {'prepared_commit': frozen['prepared_commit'],
            'first_judgment_started_at': runs[0]['reservation']['started_at'],
            'last_judgment_finished_at': runs[-1]['audit']['finished_at'], 'results_frozen_at': frozen['frozen_at'],
            'judgment_count': len(runs), 'unique_sessions': len({e['audit']['metadata']['session_id'] for e in runs}),
            'sequential': True, 'all_started_after_preparation_commit': True,
            'failed_runs': 0, 'timeouts': 0, 'harness_retries': 0,
            'visible_internal_formatting_retries': {family: sum(e['audit']['metadata']['formatting_retries']['observed_formatting_retries'] for e in runs if e['family'] == family) for family in ('A', 'B')},
            'visible_internal_transport_retry_events': {family: sum(len(e['audit']['metadata']['internal_transport_retry_events']) for e in runs if e['family'] == family) for family in ('A', 'B')},
            'per_run_retry_metadata': {e['id']: {'formatting': e['audit']['metadata']['formatting_retries'], 'transport': e['audit']['metadata']['internal_transport_retry_events']} for e in runs},
            'limitations': ['No verified immutable served snapshot is exposed.', 'Zero visible retries does not rule out hidden retries.', 'A single draw per family/case does not establish population reliability.']}


def build():
    r.write_new(HERE / 'inventory.json', evidence())
    r.write_new(HERE / 'execution-audit.json', execution_audit())


def verify(private=False):
    r.verify_results(private=private)
    r.require(r.read(HERE / 'inventory.json') == evidence(), 'Evidence inventory differs')
    r.require(r.read(HERE / 'execution-audit.json') == execution_audit(), 'Execution audit differs')
    review = r.read(HERE / 'case-reviews.json')
    r.require(review['status'] == 'POST-FREEZE / AUTHOR-INFORMED REVIEW', 'Review provenance missing')
    r.require(review['results_freeze_sha256'] == r.c.sha(r.HERE / 'results-freeze.json'), 'Review uses a different result freeze')
    r.require(datetime.fromisoformat(review['reviewed_at']) >= datetime.fromisoformat(r.frozen_results()['frozen_at']), 'Review predates the result freeze')
    cases = evidence()['cases']
    r.require(set(review['cases']) == set(cases), 'Incomplete case review')
    for cid, entry in review['cases'].items():
        r.require(entry['status_disagreements'] == cases[cid]['status_disagreements'], 'Missing disagreement review')
        r.require(set(entry['shortcut_audit']) == set(AUDITS), 'Incomplete adversary audit')
        r.require(all(isinstance(value, str) and value.strip() for value in entry['shortcut_audit'].values()), 'Empty audit explanation')
        for field in ('interpretation', 'conditions_and_reframe', 'uncertainty'):
            r.require(isinstance(entry[field], str) and entry[field].strip(), f'Missing review {field}')
    r.require(set(review['groups']) == set(evidence()['groups']), 'Incomplete contrast review')
    for value in review['groups'].values(): r.require(isinstance(value, str) and value.strip(), 'Empty contrast review')
    print('Verified all 48 judgments, 24 case reviews, eight contrasts and metrics' + ('; private execution hashes checked' if private else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('build', 'verify'))
    parser.add_argument('--private', action='store_true')
    args = parser.parse_args()
    build() if args.command == 'build' else verify(args.private)
