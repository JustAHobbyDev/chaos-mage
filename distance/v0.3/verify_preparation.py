#!/usr/bin/env python3
"""Read-only verifier for the preparation-only v0.3 handoff."""
import json
from pathlib import Path
import subprocess

import yaml

from contracts import HERE, ROOT, read, require, sha, validate, verify_preservation

MARKER = 'RETROSPECTIVE / NON-EXPERIMENTAL'
ADVERSARIES = {
    'generic-metaphor substitution', 'source-mechanism loss', 'target-question drift',
    'unsupported signal→inference leap', 'missing-but-possible measurement',
    'invented counterpart', 'creative reframe mistaken for faithful answer',
    'literalism about source materials',
}


def judge_packet(candidate):
    """Allowlisted in-memory payload; intentionally no execution or file-write API."""
    validate(candidate, 'candidate')
    payload = {k: candidate[k] for k in ('case_id', 'source', 'target', 'mapping')}
    return ((HERE / 'CLASSIFIER-transfer-validity.md').read_text() +
            '\n\nCASE PACKET\n' + json.dumps(payload, indent=2, ensure_ascii=False) + '\n')


def verify_freeze():
    frozen = read(HERE / 'model-freeze.json')
    for name, expected in frozen['files'].items():
        require(sha(ROOT / name) == expected, f'Model freeze changed: {name}')
    transfer = read(HERE / 'transfer.schema.json')['$defs']
    validity = read(HERE / 'validity.schema.json')['$defs']['validity']
    require(transfer['validity'] == validity, 'Validity contracts diverged')
    preserved = read(HERE / 'preservation.json')['files']
    for manifest_path in (ROOT / 'distance/freeze-v0.1.json',
                          ROOT / 'distance/boundary-v0.2/prepared.json'):
        historical = read(manifest_path)['files']
        require(set(historical).issubset(preserved),
                'Historical freeze includes a path missing from preservation')
        for name, expected in historical.items():
            require(sha(ROOT / name) == expected, f'Historical frozen input changed: {name}')
    candidate = read(HERE / 'candidate.schema.json')['$defs']
    require(all(candidate[k] == transfer[k] for k in candidate), 'Candidate definitions diverged')


def verify_cases():
    manifest = read(HERE / 'operator-manifest.json')
    require(manifest['status'] == 'PREPARED / UNEXECUTED', 'Not preparation-only')
    cases = {p.stem: read(p) for p in (HERE / 'cases').glob('*.json')}
    require(set(cases) == {f'{n:03}' for n in range(1, 25)}, 'Expected 24 blinded cases')
    require(set(cases) == set(manifest['cases']), 'Operator coverage differs')
    seen_adversaries = set()
    for cid, candidate in cases.items():
        validate(candidate, 'candidate')
        require(candidate['case_id'] == cid, 'Case filename/ID mismatch')
        meta = manifest['cases'][cid]
        source_path = ROOT / meta['source_path']
        source = yaml.safe_load(source_path.read_text())
        require(source['extraction']['status'] == 'accepted', 'Unaccepted source')
        require(sha(source_path) == meta['source_sha256'], 'Source hash changed')
        expected = {k: source['extraction'][k] for k in ('name', 'practice')}
        expected['instrument'] = source['instrument']
        require(candidate['source'] == expected, 'Source instrument changed')
        require(meta['synthetic'] is True, 'Authored fixture provenance missing')
        require(meta['design_intent'] in ('Valid', 'Conditional', 'Invalid'), 'Unknown intention')
        require(meta['difficulty'] in ('obvious', 'borderline'), 'Unknown difficulty')
        seen_adversaries.update(meta['adversaries'])
        # Judge context is built from candidate only, not operator fields.
        judge_packet(candidate)
    require(seen_adversaries == ADVERSARIES, 'Adversary coverage differs')
    require(len(manifest['groups']) == 8, 'Expected eight contrast groups')
    membership = []
    for name, group in manifest['groups'].items():
        members = group['members']; membership.extend(members)
        require(len(members) == 3 and len(set(members)) == 3, 'Expected a triplet')
        require({manifest['cases'][cid]['design_intent'] for cid in members} ==
                {'Valid', 'Conditional', 'Invalid'}, 'Intended contrast coverage differs')
        require({manifest['cases'][cid]['difficulty'] for cid in members} ==
                {'obvious', 'borderline'}, 'Triplet needs obvious and borderline cases')
        original = cases[group['base_candidate']]
        for cid in members:
            require(manifest['cases'][cid]['group'] == name, 'Group membership mismatch')
            require(cases[cid]['source'] == original['source'], 'Source changed within triplet')
            changed = sorted(f'{section}.{field}' for section in ('target', 'mapping')
                             for field in original[section]
                             if cases[cid][section][field] != original[section][field])
            require(changed == manifest['cases'][cid]['changed_fields_from_group_base'],
                    f'Unrecorded contrast changes: {cid}')
    require(len(membership) == 24 and set(membership) == set(cases), 'Group partition differs')
    order = read(HERE / 'execution-order.json')
    expected = {(cid, family) for cid in cases for family in ('A', 'B')}
    require(len(order) == 48 and {(r['case_id'], r['family']) for r in order} == expected,
            'Expected exactly 48 planned judgments')
    require(all(set(r) == {'id', 'case_id', 'family'} and
                r['id'] == f"validity-{r['case_id']}-{r['family']}" for r in order),
            'Invalid execution entry')
    return cases


def verify_retrospectives():
    folder = HERE / 'examples/retrospective'
    expected = {f'{cid}-{family}' for cid in ('003', '004', '009', '012', '013', '016')
                for family in ('A', 'B')}
    paths = {p.stem: p for p in folder.glob('*.json')}
    require(set(paths) == expected, 'Retrospective coverage differs')
    require(MARKER in (folder / 'README.md').read_text(), 'Index lacks retrospective marker')
    records = {}
    for key, path in paths.items():
        entry = read(path)
        require(set(entry) == {'status', 'provenance', 'transfer'} and entry['status'] == MARKER,
                'Invalid retrospective envelope or marker')
        provenance = entry['provenance']
        require(set(provenance) == {'case', 'judgment', 'model_commit',
                                  'model_freeze_sha256', 'reconstruction'},
                'Invalid retrospective provenance')
        require(provenance['model_freeze_sha256'] == sha(HERE / 'model-freeze.json'),
                'Retrospective uses another model freeze')
        require(bool(provenance['reconstruction'].strip()), 'Reconstruction explanation missing')
        cid, family = key.split('-')
        for field, expected_path in (
            ('case', f'distance/boundary-v0.2/cases/{cid}.yaml'),
            ('judgment', f'distance/boundary-v0.2/judgments/primary-{key}.json')):
            item = provenance[field]
            require(set(item) == {'path', 'sha256'} and item['path'] == expected_path,
                    'Wrong historical provenance')
            require(sha(ROOT / item['path']) == item['sha256'], 'Historical provenance changed')
        # Verify the recorded preparation commit really contains the model freeze.
        committed = subprocess.check_output(['git', 'show',
            f"{provenance['model_commit']}:distance/v0.3/model-freeze.json"], cwd=ROOT)
        require(committed == (HERE / 'model-freeze.json').read_bytes(), 'Uncommitted model freeze')
        old_case = yaml.safe_load((ROOT / provenance['case']['path']).read_text())
        old = read(ROOT / provenance['judgment']['path'])['classification']['source_transfer_profile']
        mapping = {'state': ' '.join(old[k] for k in ('entities', 'relations', 'processes')),
                   'operation': old['operations'], 'signal': old['observables'],
                   'inference': old['inferences'], 'limit': old['failure_modes']}
        if cid in ('003', '004', '009'):
            question = 'Explain the textual organization and what, if anything, supports claims about its formation.'
        elif cid in ('012', '013'):
            question = 'Determine which components can be distinguished and what evidence supports that decomposition.'
        else:
            question = 'Explain the brand identity expressed by these current materials.'
        before, after = old_case['target']['problem'].split(question)
        evidence = [part.strip() for part in (before, after) if part.strip()]
        candidate = {'case_id': f'RETRO-{key}', 'source': old_case['source'],
                     'target': {'domain': old_case['target']['domain'],
                                'question': question, 'evidence': evidence},
                     'mapping': mapping}
        records[key] = validate({'transfer': entry['transfer']}, 'transfer', candidate)
    for group in (('003', '004', '009'), ('012', '013')):
        profiles = [records[f'{cid}-{family}']['native_baseline']
                    for cid in group for family in ('A', 'B')]
        for field in ('target_domain', 'target_task', 'reference_practitioner', 'ordinary_methods', 'ordinary_evidence'):
            require(all(x[field] == profiles[0][field] for x in profiles),
                    f'Baseline moved with supplied evidence: {field}')
    return records


def verify_inventory():
    prepared = read(HERE / 'preparation.json')
    require(prepared['status'] == 'PREPARED / UNEXECUTED', 'Not a preparation-only snapshot')
    for name, expected in prepared['files'].items():
        require(sha(ROOT / name) == expected, f'Prepared artifact changed: {name}')
    actual = {str(p.relative_to(ROOT)) for p in HERE.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p.name != 'preparation.json'}
    listed = {name for name in prepared['files'] if name.startswith('distance/v0.3/')}
    require(actual == listed, 'Unexpected or missing v0.3 artifact; no experiment results allowed')
    for name in actual:
        parts = Path(name).parts
        require(not any(x in parts for x in ('judgments', 'results', 'runs', 'metrics')),
                'Experimental output directory exists')
        require(not any(x in Path(name).name for x in ('results-freeze', 'metrics', '.jsonl')),
                'Experimental result artifact exists')
    require(not (ROOT / '.runtime/transfer-validity-v0.3').exists(),
            'A v0.3 experiment runtime exists during preparation-only handoff')


def verify():
    count = verify_preservation()
    verify_freeze()
    cases = verify_cases()
    retrospectives = verify_retrospectives()
    verify_inventory()
    return {'preserved_files': count, 'prepared_cases': len(cases),
            'retrospective_examples': len(retrospectives), 'planned_judgments': 48,
            'status': 'PREPARED / UNEXECUTED'}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
