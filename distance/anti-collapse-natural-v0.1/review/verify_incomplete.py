"""Read-only independent verification of Experiment E's interrupted execution."""
import argparse
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import re
import sys
import jsonschema
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
import runner as r


def verify(private=False):
    r.require(r.verify_results(private)['status']=='incomplete','Expected failed-run status')
    failure=r.read(HERE/'failure-freeze.json');partial=r.read(HERE/'audit-partial-freeze.json');m=r.read(HERE/'metrics.json')
    r.require(partial['terminal_failure_sha256']==r.c.sha(HERE/'failure-freeze.json'),'Partial freeze binding')
    r.require(partial['status']=='incomplete' and partial['not_primary_admission'],'Partial run misrepresented')
    r.require(failure['stop']['stage']=='audit' and failure['stop']['run']['id']=='audit-E021-A','Wrong failure')
    scheduled=r.order('audit');attempts=partial['attempts']
    r.require([{k:e[k] for k in ('id','case_id','family')} for e in attempts]==scheduled[:len(attempts)],'Audit prefix differs from schedule')
    r.require(partial['unscheduled_run_ids']==[e['id'] for e in scheduled[len(attempts):]],'Missing unscheduled runs')
    r.require(len(scheduled)==54 and len(attempts)==22,'Audit coverage mismatch')
    success=[e for e in attempts if e['validation']['status']=='valid'];failed=[e for e in attempts if e['validation']['status']=='failed']
    r.require(len(success)==21 and len(failed)==1,'Partial execution mismatch')
    blocked=failed[0]
    r.require(blocked['validation']['error']=='ValueError: CLI version changed' and blocked['validation']['metadata'] is None and blocked['reservation'] is None,'Prelaunch failure mismatch')
    r.require(not any(Path(name).name in ('reservation.json','events.jsonl','response.json') for name in blocked['files']),'Blocked call launched')
    sessions=[];retries={f:0 for f in 'AB'};returns={f:set() for f in 'AB'}
    chronological=[]
    for stage in ('generation','neutralization'):
        data=r.read(HERE/(stage+'-freeze.json'))
        r.require(data['execution_commit']==r.checkpoint(HERE/'probes'/(stage+'.json')),'Wrong stage execution commit')
        r.require([{k:e[k] for k in ('id','case_id','family')} for e in data['runs']]==r.order(stage),'Complete schedule mismatch')
        for e in data['runs']:
            chronological.append((stage,e))
            path=r.public_path(stage,e) if e['validation']['status']=='valid' else HERE/'failures'/stage/(e['id']+'.txt')
            r.require(r.c.sha(path)==e['response_sha256'],'Published payload changed')
            if stage=='generation':jsonschema.Draft202012Validator(r.read(r.canonical(stage))).validate(r.read(path))
            else:r.validate_response(r.read(path),stage,e)
    gen=r.read(HERE/'generation-freeze.json')['runs'];neut=r.read(HERE/'neutralization-freeze.json')['runs']
    r.require(len(gen)==30 and len(neut)==27,'Generation/neutralization coverage mismatch')
    for e in success:
        r.require(r.c.sha(r.public_path('audit',e))==e['response_sha256'],'Published audit changed')
        r.validate_response(r.read(r.public_path('audit',e)),'audit',e)
        r.require(e['reservation']['input_commit']==r.checkpoint(HERE/'probes/audit.json'),'Partial audit execution commit')
        chronological.append(('audit',e))
    for stage in ('generation','neutralization','audit'):
        r.verify_stage_inputs(stage)
        probe=r.read(HERE/'probes'/(stage+'.json'))
        for entry in probe['entries']:
            meta=entry['validation']['metadata'];sessions.append(meta['session_id'])
            if private:r.verify_inventory(entry['files'])
    last=None
    for stage,e in chronological:
        meta=e['validation']['metadata'];reservation=e['reservation'];sessions.append(meta['session_id'])
        start=datetime.fromisoformat(reservation['started_at']);end=datetime.fromisoformat(e['validation']['finished_at'])
        r.require((last is None or last<=start) and start<=end,'Overlapping/out-of-order calls');last=end
        r.require(reservation['configuration']==r.config(),'Frozen execution configuration differs')
        r.require(reservation['cli_version']==r.config()['expected_cli_versions'][e['family']],'Completed call used different CLI')
        r.require(reservation['packet_sha256']==r.sha(r.packet(stage,e['case_id']).encode()),'Executed packet drift')
        r.require(reservation['canonical_schema_sha256']==r.c.sha(r.canonical(stage)),'Canonical schema drift')
        r.require(reservation['wire_schema_sha256']==r.c.sha(HERE/'schemas'/(stage+'-wire.schema.json')),'Wire schema drift')
        r.require(datetime.fromisoformat(r.read(HERE/'probes'/(stage+'.json'))['at'])<=start,'Call before probes')
        retries[e['family']]+=meta['formatting_retries']['observed_formatting_retries'];returns[e['family']].update(meta['returned_model_identifiers'])
        if private:r.verify_inventory(e['files'])
    r.require(len(sessions)==len(set(sessions))==84,'Unique-session coverage')
    r.require(last<=datetime.fromisoformat(failure['at']),'Failure freeze precedes partial calls')
    for stage in ('validity','anti-collapse'):
        for suffix in ('-freeze.json',''):
            p=HERE/(stage+suffix) if suffix else r.RUNTIME/stage
            r.require(not p.exists() or (p.is_dir() and not list(p.iterdir())),'Unexpected downstream execution')
        r.require(not (HERE/'probes'/(stage+'.json')).exists(),'Unexpected downstream probe')
    r.require(not (HERE/'admission.json').exists(),'Derived admission after failed audit')
    counter=Counter(e['validation']['status'] for e in gen)
    expected={'status':'incomplete','planned_generations':len(gen),'generation_provider_outputs':len(gen),'generation_schema_valid_outputs':len(gen),'generated_mappings_passing_frozen_checks':counter['valid'],'generation_failures_as_recorded':counter['excluded'],'generator_family_attempts':dict(Counter(e['family'] for e in gen)),'generator_family_passed_checks':dict(Counter(e['family'] for e in gen if e['validation']['status']=='valid')),'target_count':len({x['target_id'] for x in r.manifest()}),'accepted_source_count':len({x['source_path'] for x in r.manifest()}),'neutralization_attempts':len(neut),'neutralization_successes':sum(e['validation']['status']=='valid' for e in neut),'neutralization_failures':sum(e['validation']['status']!='valid' for e in neut),'audit_judgments_planned':len(scheduled),'audit_judgments_collected':len(success),'audit_prelaunch_failures':len(failed),'audit_calls_not_launched':len(scheduled)-len(success),'audit_completed_family_counts':dict(Counter(e['family'] for e in success)),'partial_audit_verdicts':{f:dict(Counter(r.read(r.public_path('audit',e))['overall'] for e in success if e['family']==f)) for f in 'AB'},'complete_audit_pairs':sorted(cid for cid,n in Counter(e['case_id'] for e in success).items() if n==2),'validity_judgments':0,'primary_anti_collapse_count':0,'provider_probe_calls':6,'unique_provider_sessions':len(sessions),'harness_retries':0,'replacement_measurements':0,'model_substitutions_observed':0}
    for key,value in expected.items():r.require(m[key]==value,'Independent metric mismatch: '+key)
    for key in ('neutralization_audit_exclusion_count','validity_admission_count','validity_exclusion_count','anti_collapse_status_distributions','keep_reject_agreement','departure_locus_agreement','materiality_agreement','native_reduction_agreement','formalization_agreement','clear_collapse_cases','borderline_cases','natural_formalization_findings','natural_one_rule_findings','mechanism_disagreements'):r.require(m[key] is None,'Unmeasured field is not null: '+key)
    excluded=r.read(HERE/'review/content-exclusion-review.json')
    r.require({x['case_id'] for x in excluded['cases']}=={e['case_id'] for e in gen if e['validation']['status']=='excluded'},'Exclusion review coverage')
    r.require(m['post_freeze_false_positive_generation_exclusions']==len(excluded['cases'])==3,'Exclusion count')
    for item in excluded['cases']:
        e=next(x for x in gen if x['case_id']==item['case_id']);p=HERE/'failures/generation'/(e['id']+'.txt');v=r.read(p)
        r.require(r.c.sha(p)==item['raw_sha256'],'Excluded payload drift')
        group,key=item['field'].split('.');r.require(item['excerpt'] in v[group][key],'Review excerpt not in original')
        try:r.validate_response(v,'generation',e)
        except ValueError as exc:r.require(str(exc)=='Generation self-label violation','Different generation exclusion')
        else:raise ValueError('Original lexical exclusion no longer reproducible')
        r.require(item['original_exclusion_retained'] and not item['readmitted'],'Post-freeze cohort repair')
    binding=r.read(HERE/'review/result-binding.json');r.committed(r.ROOT/binding['terminal_path'],binding['terminal_commit'])
    r.require(binding['terminal_sha256']==r.c.sha(HERE/'failure-freeze.json'),'Review not bound to failure')
    r.require(datetime.fromisoformat(binding['review_started_at'])>datetime.fromisoformat(failure['at']),'Review chronology')
    report=r.ROOT/'distance/review/anti-collapse-natural-v0.1.md';text=report.read_text()
    r.require('incomplete' in text.lower() and 'false positives' in text and 'no answer' in text,'Report lacks central limitations')
    commits=re.findall(r'`([0-9a-f]{40})`',text)
    for commit in commits:r.require(r.git('merge-base',commit,'HEAD').decode().strip()==commit,'Report checkpoint is not ancestor')
    for old,new in zip(commits,commits[1:]):r.require(old!=new and r.git('merge-base',old,new).decode().strip()==old,'Checkpoint order')
    return {'status':'incomplete','generation_outputs':30,'passed_generation_checks':27,'neutralizations':27,'completed_audits':21,'unlaunched_audits':33,'unique_provider_sessions':84,'false_positive_generation_exclusions':3,'validity_calls':0,'anti_collapse_calls':0,'exposed_measurement_formatter_retries':retries,'returned_identifiers':{f:sorted(returns[f]) for f in 'AB'},'historical_files_unchanged':True,'private_hashes_checked':private}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--private',action='store_true');a=p.parse_args();print(json.dumps(verify(a.private),indent=2))
