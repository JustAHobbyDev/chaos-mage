"""Offline-only additive validation of U1's unresolved-dependency metadata.
No provider launch, budget approval, response editing, or general retry capability.
"""
from pathlib import Path
import argparse
import inspect
import json
import re
import sys
from copy import deepcopy
import contracts as c
import runner as r

REC=r.H/'review/recovery/unresolved-metadata'
UID='K12-C1'
SOURCE=inspect.getsource(c.validate)
OLD="require(set(emb) == {d['dependency_id'] for d in s['dependencies']}, 'Embedded classification identity mismatch')"
NEW="require(unresolved_linkage(value), 'Embedded classification identity mismatch')"
c.require(SOURCE.count(OLD)==1,'Frozen validator assertion changed')
ORIGINAL=c.validate


def unresolved_linkage(value):
    s=value['claim_obligation_set']
    resolved={d['dependency_id'] for d in s['dependencies']}
    embedded={e['dependency_id'] for e in value['embedded_classifications']}
    if resolved==embedded:return True
    extras=embedded-resolved
    return (resolved<=embedded and bool(extras) and s['closure_status']=='DEPENDENCY_UNCERTAIN'
            and all(re.fullmatch(r'[A-Za-z0-9_-]+',key) and
                    any(re.match(re.escape(key)+r'\b',text) for text in s['unresolved_dependencies'])
                    for key in extras))

namespace=dict(c.__dict__);namespace['unresolved_linkage']=unresolved_linkage
exec(compile(SOURCE.replace(OLD,NEW),str(Path(__file__))+'::supplementary_validate','exec'),namespace)
SUPPLEMENT=namespace['validate']


def validate(stage,value,packet,schema,taxonomy):
    """Accept only this unchanged observed response via the metadata supplement."""
    try:return ORIGINAL(stage,value,packet,schema,taxonomy)
    except ValueError as exc:
        if str(exc)!='Embedded classification identity mismatch':raise
        evidence=r.read(REC/'evidence.json')
        c.require(stage=='obligation' and value==r.read(REC/'original/response.json'),
                  'Supplement is bound to the unchanged U1 observation')
        c.require(r.sha(REC/'original/response.json')==evidence['response_sha256'],'Original response changed')
        return SUPPLEMENT(stage,value,packet,schema,taxonomy)


def proof():
    r.verify();r.binary_check()
    e=r.read(REC/'evidence.json');r.hashes(e['preserved_files'],True)
    c.require(r.sha(r.H/'contracts.py')==e['original_validator_sha256'],'Frozen validator changed')
    c.require(r.sha(Path(__file__))==e['adapter_sha256'],'Adapter changed')
    source=r.RT/'attempts/obligation'/UID
    for name in e['original_attempt_files']:
        c.require((source/name).read_bytes()==(REC/'original'/name).read_bytes(),'Original attempt artifact changed: '+name)
    packet=r.read(r.packet_path('obligation',UID))
    c.require(packet==r.build_packet('obligation',UID),'Executed packet no longer reproducible')
    c.require((source/'request.txt').read_bytes()==r.prompt('obligation',packet)==r.packet_path('obligation',UID,'txt').read_bytes(),
              'Provider-visible request changed')
    value=r.read(source/'response.json')
    for schema in ('obligation.schema.json','obligation-wire.schema.json'):
        c.Draft202012Validator(r.read(r.H/'schemas'/schema)).validate(value)
    events=[json.loads(line,object_pairs_hook=r.unique) for line in (source/'events.jsonl').read_text().splitlines() if line.strip()]
    metadata=r.audit_events(events,(source/'response.json').read_text())
    c.require(metadata['session_id']==e['session_id'],'Original session changed')
    c.require(r.read(source/'exit.json')['returncode']==0,'Provider did not complete successfully')
    diagnostics=validate('obligation',value,packet,r.read(r.H/'schemas/obligation.schema.json'),r.taxonomy())
    # Supplement cannot turn unresolved closure into a pass or invent an operation.
    a=r.assignments()[UID]
    jobs=c.obligation_jobs(r.claims()[UID][0],a,value)
    c.require(len(jobs)==1 and jobs[0]['contract']=='GOVERNANCE_COHERENCE','Supplement added/removed scientific evaluation jobs')
    fake={(UID,jobs[0]['obligation_id']):{**jobs[0],'verdict':'SATISFIED'}}
    c.require(c.aggregate({UID:a},{UID:value},fake,r.taxonomy())[UID]['overall']=='UNCERTAIN','Uncertainty lost')
    return {'metadata':metadata,'diagnostics':diagnostics,'response_sha256':r.sha(source/'response.json'),
            'execution_commit':r.read(source/'reservation.json')['execution_commit'],'schema_valid':True,
            'provider_calls':0,'scientific_fields_changed':False}


def supplement():
    info=proof();source=r.RT/'attempts/obligation'/UID
    c.require(r.latest_state()['state']=='PAUSED_EVENT','Not the original paused checkpoint')
    c.require(r.latest_state()['detail']['error']=='ValueError: Embedded classification identity mismatch','Different incident')
    record={'at':r.now(),**info,'supplementary':True,'supplement_commit':r.head(),
            'adapter_sha256':r.sha(Path(__file__)),'original_failure_sha256':r.sha(source/'failure.json')}
    r.write(source/'supplementary-validation.json',record)
    # No validation.json existed: original failed validation remains in failure.json.
    r.write(source/'validation.json',record)
    r.verify_attempt('obligation',UID,source)
    r.raw(r.judgment('obligation',UID),(source/'response.json').read_bytes())
    r.write(REC/'resolution.json',{'at':r.now(),**info,'classification':'recoverable_integrity_violation',
        'adapter_sha256':r.sha(Path(__file__)),'original_pause_preserved':True,'next_checkpoint':'Freeze Stage B; Stage C only after gates',
        'authority':'H6.R2 recovery policy and user completion approval; no retry or observation repair.'})


def resume_freeze():
    proof();r.committed(REC/'resolution.json')
    c.require(r.latest_state()['state']=='PAUSED_EVENT','Unexpected scheduling state')
    c.require(r.read(r.judgment('obligation',UID))==r.read(REC/'original/response.json'),'Observation changed')
    r.transition('BATCH_COMPLETE',{'engineering_recovery':r.rel(REC/'resolution.json'),
        'resolution_sha256':r.sha(REC/'resolution.json'),'original_pause_sha256':r.read(REC/'evidence.json')['pause_sha256'],
        'provider_calls':0,'next_stage':'evaluation after complete Stage B freeze and new gates'})
    c.validate=validate
    try:r.freeze('obligation')
    finally:c.validate=ORIGINAL


def metrics():
    proof()
    c.validate=validate
    try:r.metrics()
    finally:c.validate=ORIGINAL


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['verify','supplement','resume-freeze','metrics'])
    a=p.parse_args()
    if a.action=='verify':print(json.dumps(proof(),indent=2))
    elif a.action=='supplement':supplement()
    elif a.action=='resume-freeze':resume_freeze()
    else:metrics()


if __name__=='__main__':main()
