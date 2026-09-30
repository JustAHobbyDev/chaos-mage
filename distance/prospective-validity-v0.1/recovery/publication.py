"""Post-freeze preparation, metrics and completion verification. No provider calls."""
from collections import Counter
from datetime import datetime
import argparse
import json
import random
import continuation as r

c, old, e = r.c, r.old, r.e
HERE, F, ROOT = r.HERE, r.F, r.ROOT


def frozen(stage):
    path = HERE / f'{stage}-freeze.json'
    old.committed(path)
    result = c.read(path)
    c.require(result['order'] == r.order(stage), 'Frozen order mismatch')
    c.require([x['identity'] for x in result['runs']] == result['order'], 'Frozen coverage mismatch')
    for row in result['runs']:
        old.verify_hashes(row['files'])
        c.require(c.sha(ROOT / row['response_path']) == row['response_sha256'], 'Published response changed')
        r.validate(c.read(ROOT / row['response_path']), stage, row['identity'])
    return result


def responses(stage): return {row['identity']: c.read(ROOT / row['response_path']) for row in frozen(stage)['runs']}


def taxonomy_metrics():
    data = responses('taxonomy')
    return {'completed': len(data), 'distribution': {k: sum(x['category'] == k for x in data.values()) for k in c.CATEGORIES},
            'execution': [k for k,v in data.items() if v['category'] == 'execution_precondition'],
            'validity_relevant': [k for k,v in data.items() if v['category'] in c.CATEGORIES[1:4]],
            'mixed_uncertain': [k for k,v in data.items() if v['category'] in ('mixed','uncertain')]}


def prepare_prospective():
    frozen('taxonomy')
    audit_path = HERE / 'review/taxonomy-audit.json'
    old.committed(audit_path)
    audit = c.read(audit_path)
    c.require({x['condition_id'] for x in audit['findings']} == set(r.order('taxonomy')), 'Taxonomy review coverage')
    c.require(len(audit['findings']) == 196, 'Duplicate/missing taxonomy annotation')
    c.require(audit['taxonomy_freeze_sha256'] == c.sha(HERE / 'taxonomy-freeze.json'), 'Taxonomy review binding')
    classifier = (HERE / 'CLASSIFIER.md').read_text()
    c.require('Assume all execution prerequisites are satisfied and the stated signal occurs.' in classifier, 'Missing warrant diagnostic')
    c.require(not any(identity in classifier for identity in ('E006','E022','E030','Q0020')), 'Case key in classifier')
    for suffix, value in [('', c.schema('prospective')), ('-wire', c.wire(c.schema('prospective')))]:
        old.write(HERE / 'schemas' / ('prospective'+suffix+'.schema.json'), value)
    identities = [f'E{i:03}' for i in range(1,31)]
    for identity in identities:
        candidate = c.read(F / 'imports/candidates' / f'{identity}.json')
        prompt = classifier + '\nCASE PACKET\n' + json.dumps({'case_id':identity, **candidate}, indent=2, ensure_ascii=False) + '\n'
        old.copy(HERE / 'packets/prospective' / f'{identity}.txt', prompt.encode())
    random.Random(20260930073).shuffle(identities)
    old.write(HERE / 'execution-orders/prospective.json', {'seed':20260930073, 'order':identities})
    old.write(HERE / 'prospective-prepared.json', {'at':old.now(), 'parent_commit':old.head(),
        'taxonomy_freeze_sha256':c.sha(HERE/'taxonomy-freeze.json'), 'taxonomy_audit_sha256':c.sha(audit_path),
        'classifier_sha256':c.sha(HERE/'CLASSIFIER.md'), 'configuration_sha256':c.sha(F/'execution-config.json'),
        'files':old.inventory(HERE.rglob('*')), 'order':identities})
    r.verify_inputs('prospective')


def complete_metrics():
    taxonomy = taxonomy_metrics()
    data = responses('prospective')
    assessment_path = HERE / 'review/mapping-assessments.json'
    old.committed(assessment_path)
    assessments = c.read(assessment_path)
    c.require({x['case_id'] for x in assessments['findings']} == set(data) and len(assessments['findings']) == 30,
              'Mapping-only assessment coverage')
    manifest = c.read(F / 'operator-manifest.json')['cases']
    prior = {row['case_id']:c.read(F/'imports/historical-judgments'/f'validity-{row["case_id"]}-A.json')['validity']['final_status'] for row in manifest}
    statuses = ('Valid','Conditional','Invalid')
    rank = {'Invalid':0,'Conditional':1,'Valid':2}
    transitions = {a:{b:sum(prior[k] == a and v['final_status'] == b for k,v in data.items()) for b in statuses} for a in statuses}
    changes = [{'case_id':k,'old':prior[k],'new':v['final_status'],'more_permissive':rank[v['final_status']]>rank[prior[k]]}
               for k,v in sorted(data.items()) if prior[k] != v['final_status']]
    fidelity = {row['case_id'] for row in manifest if row['fidelity_pass']}
    eligible = sorted(k for k,v in data.items() if v['final_status'] == 'Valid' and k in fidelity)
    def group(rows):
        ids = [x['case_id'] for x in rows]
        return {'mappings':len(ids),'statuses':{s:sum(data[k]['final_status']==s for k in ids) for s in statuses},
                'eligible':sum(k in eligible for k in ids)}
    vals = [c.read(p) for parent in (old.RUNTIME,r.RUNTIME) for p in parent.rglob('validation.json')]
    metadata = [v['metadata'] for v in vals if v.get('metadata')]
    return {'status':'complete','original_incomplete_commit':e.ORIGINAL,'recovery_classification':'recoverable_integrity_violation',
        'retained_taxonomy':4,'retained_taxonomy_probe':True,'taxonomy':taxonomy,'prospective_completed':len(data),
        'prospective_status_distribution':{s:sum(v['final_status']==s for v in data.values()) for s in statuses},
        'execution_readiness_distribution':{s:sum(v['execution_readiness']['status']==s for v in data.values()) for s in ('ready','requires_preconditions','unknown')},
        'prospective_condition_distribution':dict(Counter(x['category'] for v in data.values() for x in v['conditions'])),
        'old_to_new_transitions':transitions,'status_changes':changes,'more_permissive_transitions':[x for x in changes if x['more_permissive']],
        'eligible_ids':eligible,'single_model_prospective_eligible_count':len(eligible),'reaches_18':len(eligible)>=18,
        'fidelity_pass_count':len(fidelity),'E_remains_stopped':True,'dual_family_rule_satisfied':False,
        'generator_origins':{k:group([x for x in manifest if x['generator_family']==k]) for k in ('A','B')},
        'source_instruments':{k:group([x for x in manifest if x['source_path']==k]) for k in sorted({x['source_path'] for x in manifest})},
        'provider_calls':len(vals),'harness_retries':0,'replacement_measurements':0,
        'sessions':len({x['session_id'] for x in metadata}),'returned_model_identifiers':sorted({i for x in metadata for i in x['returned_model_identifiers']}),
        'verified_served_snapshot':None,'cross_model_robustness':None,'within_model_stability':None,
        'usage':{k:sum((u or {}).get(k,0) for m in metadata for u in m['usage']) for k in ('input_tokens','cached_input_tokens','output_tokens')},
        'observed_provider_transport_retries':sum(len(m['internal_transport_retry_events']) for m in metadata)}


def verify_precheck(path, commit, before):
    check = c.read(path)
    c.require(check['input_commit'] == commit, 'Precheck execution commit mismatch')
    c.require(len(check['checks']) == 36 and all(x['exit_code'] == 0 for x in check['checks']), 'Incomplete historical precheck')
    c.require(check['legacy_F']['tests'] == 37, 'Original F precheck missing')
    c.require(datetime.fromisoformat(check['at']) <= datetime.fromisoformat(before), 'Historical check finished after provider launch')


def verify_completion():
    r.verify_inputs('prospective', True)
    attempts = r.verify_attempts()
    e.gate(c.read(HERE / 'recovery-record.json'))
    tf, pf = frozen('taxonomy'), frozen('prospective')
    for row in tf['runs'][:4]:
        c.require(row['retained_original'], 'Retained observation replaced')
    c.require(tf['retained_count']==4 and len(tf['runs'])==196 and len(pf['runs'])==30, 'Final denominator mismatch')
    audit = c.read(HERE / 'review/taxonomy-audit.json')
    c.require(audit['taxonomy_freeze_sha256']==c.sha(HERE/'taxonomy-freeze.json'), 'Audit binding')
    old.committed(HERE/'taxonomy-freeze.json', audit['input_commit'])
    prepared = c.read(HERE/'prospective-prepared.json')
    old.committed(HERE/'review/taxonomy-audit.json',prepared['parent_commit'])
    probe = c.read(HERE/'probes/prospective.json')
    c.require(probe['prepared_sha256']==c.sha(HERE/'prospective-prepared.json'), 'Probe/preparation binding')
    old.committed(HERE/'prospective-prepared.json',probe['input_commit'])
    old.verify_hashes(probe['entry']['files'])
    verify_precheck(ROOT/probe['precheck'], probe['input_commit'], probe['entry']['reservation']['started_at'])
    segments = [c.read(path) for path in sorted((r.RUNTIME/'segments').glob('*.json'))]
    for segment in segments:
        verify_precheck(ROOT/segment['precheck'], segment['commit'], segment['at'])
    for stage, freeze in [('taxonomy',tf),('prospective',pf)]:
        last = max(datetime.fromisoformat(x['validation']['finished_at']) for x in freeze['runs'])
        c.require(last <= datetime.fromisoformat(freeze['at']), 'Freeze precedes response')
        for row in freeze['runs']:
            if not row.get('retained_original'):
                old.committed(HERE/('continuation-prepared.json' if stage=='taxonomy' else 'probes/prospective.json'),row['reservation']['input_commit'])
                old.committed(HERE/'recovery-record.json',row['reservation']['input_commit'])
                matches = [s for s in segments if s['stage']==stage and s['commit']==row['reservation']['input_commit']
                           and datetime.fromisoformat(s['at'])<=datetime.fromisoformat(row['reservation']['started_at'])]
                c.require(matches, 'Measurement has no verified execution segment')
    assessments = c.read(HERE/'review/mapping-assessments.json')
    old.committed(HERE/'prospective-freeze.json',assessments['input_commit'])
    comparison = c.read(HERE/'review/comparison-audit.json')
    old.committed(HERE/'review/mapping-assessments.json',comparison['input_commit'])
    metrics = complete_metrics()
    c.require(metrics==c.read(HERE/'metrics.json'),'Metrics do not reconstruct')
    changed = {x['case_id'] for x in metrics['status_changes']}
    c.require(changed <= {x['case_id'] for x in comparison['findings']}, 'Changed-status review incomplete')
    c.require({'E006','E022','E030'} <= {x['case_id'] for x in comparison['diagnostics']}, 'Mandatory diagnostics missing')
    c.require(metrics['provider_calls']==228 and metrics['sessions']==228,'Call/session count mismatch')
    c.require(r.state()=='COMPLETE','Completion state missing')
    final = c.read(HERE/'final-runtime-freeze.json')
    old.verify_hashes(final['files'])
    c.require(final['files']==old.inventory(r.RUNTIME.rglob('*')),'Execution after final freeze')
    return {'status':'complete','taxonomy':196,'prospective':30,'attempts':attempts,'preservation':e.preservation(),
            'recovery_gate':'pass','metrics_reconstructed':True,'E_remains_stopped':True}


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare-prospective','taxonomy-metrics','metrics','verify']);a=p.parse_args()
    if a.action=='prepare-prospective': prepare_prospective()
    else: print(json.dumps(taxonomy_metrics() if a.action=='taxonomy-metrics' else complete_metrics() if a.action=='metrics' else verify_completion(),indent=2))
