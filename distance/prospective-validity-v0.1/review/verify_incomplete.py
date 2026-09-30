"""Verify terminal F while retaining, not rewriting, the executed faulty freeze."""
from datetime import datetime
from pathlib import Path
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner as r
import contracts as c
sys.path.insert(0,str(Path(__file__).resolve().parent))
import metrics
BASE='da8cb8d91505d68e65ea8f2d3910f4ca34a03c3b'

def verify():
    fix=c.read(r.HERE/'review/preservation-correction.json')
    prep=c.read(r.HERE/'taxonomy-prepared.json'); pc=r.checkpoint(r.HERE/'taxonomy-prepared.json')
    # Check the actual executed document, not a repaired preparation manifest.
    for name,h in prep['files'].items():
        p=r.ROOT/name
        if name==fix['historical_path']: p=r.ROOT/fix['executed_preparation_document_archive']
        c.require(c.sha(p)==h,'Executed preparation bytes changed: '+name)
        c.require(c.digest(r.git('show',pc+':'+name))==h,'Preparation commit mismatch: '+name)
    c.require(c.sha(r.ROOT/fix['historical_path'])==fix['restored_sha256'],'Restored history changed')
    c.require((r.ROOT/fix['historical_path']).read_bytes()==r.git('show',BASE+':'+fix['historical_path']),'History not restored exactly')
    r.verify_hashes(c.read(r.HERE/'preservation.json')['files']); r.verify_imports()
    # Original inventory omitted the shared design log: explicitly check it now.
    for name in r.git('diff','--name-only',BASE,'--').decode().splitlines():
        c.require(name=='docs/HANDOFF-prospective-validity.md' or name=='docs/PROBLEM_FRAMES-prospective-validity-v0.1.md' or name.startswith('distance/prospective-validity-v0.1/') or name=='distance/review/prospective-validity-v0.1.md','Historical change outside authorized new artifacts: '+name)
    frozen=c.read(r.HERE/'failure-freeze.json'); r.verify_hashes(frozen['files'])
    c.require(frozen['files']==r.inventory(r.RUNTIME.rglob('*')),'Execution after terminal freeze')
    partial=c.read(r.HERE/'taxonomy-partial-freeze.json'); terminal=r.checkpoint(r.HERE/'taxonomy-partial-freeze.json')
    c.require(partial['failure_freeze_sha256']==c.sha(r.HERE/'failure-freeze.json'),'Failure binding')
    c.require(partial['preparation_sha256']==c.sha(r.HERE/'taxonomy-prepared.json'),'Preparation binding')
    c.require([x['identity'] for x in partial['runs']]==r.order('taxonomy')[:4],'Partial order/coverage')
    probe=c.read(r.HERE/'probes/taxonomy.json'); c.require(probe['input_commit']==pc,'Probe checkpoint')
    probe_commit=r.checkpoint(r.HERE/'probes/taxonomy.json')
    c.require(c.read(r.RUNTIME/'taxonomy-reservation.json')['commit']==probe_commit,'Measurement checkpoint')
    events_entries=[probe['entry'],*partial['runs']]; sessions=[]; last=None
    stop=datetime.fromisoformat(frozen['stop']['at'])
    for entry in events_entries:
        x=entry['reservation']; v=entry['validation']; r.verify_hashes(entry['files'])
        d=r.RUNTIME/('probes' if x['kind']=='probes' else 'runs')/'taxonomy'/x['identity']
        a=c.read(d/'attempt.json'); c.require(a['harness_attempt']==1,'Repeated harness attempt')
        c.require(x['input_commit']==(pc if x['kind']=='probes' else probe_commit),'Execution commit drift')
        c.require(x['configuration']==r.config() and x['command']==r.command(x['working_directory'],d,'taxonomy'),'Execution config drift')
        start=datetime.fromisoformat(x['started_at']); end=datetime.fromisoformat(v['finished_at'])
        c.require(start<stop and start<=end and (last is None or last<=start),'Launch after stop or overlapping calls'); last=end
        c.require(c.sha(d/'prompt.txt')==x['packet_sha256'],'Packet drift')
        for suffix,key in [('', 'canonical_schema_sha256'),('-wire','wire_schema_sha256')]: c.require(x[key]==c.sha(r.HERE/'schemas'/f'taxonomy{suffix}.schema.json'),'Schema drift')
        events=[json.loads(s,object_pairs_hook=c.unique) for s in (d/'events.jsonl').read_text().splitlines() if s.strip()]
        m=r.audit_events(events); c.require(m==v['metadata'] and v['status']=='valid','Event metadata drift')
        sessions.append(m['session_id']); c.validate(c.read(d/'response.json'),'taxonomy',x['identity'])
        final=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
        c.require(len(final)==1 and final[0].strip()==(d/'response.json').read_text().strip(),'Stream/response mismatch')
        if x['kind']=='probes': c.require(c.read(d/'response.json')==r.probe_fixture('taxonomy'),'Probe fixture drift')
        else:
            c.require((d/'prompt.txt').read_text()==r.packet('taxonomy',x['identity']),'Packet reconstruction drift')
            p=r.HERE/'taxonomy-judgments'/f'{x["identity"]}.json'
            c.require(p.read_bytes()==(d/'response.json').read_bytes(),'Published response changed')
    c.require(last<=datetime.fromisoformat(frozen['at']),'Freeze before final in-flight completion')
    c.require(len(sessions)==len(set(sessions))==5,'Session count/reuse')
    c.require(len(list(r.RUNTIME.rglob('attempt.json')))==5,'Extra attempt')
    for forbidden in ('prospective-prepared.json','prospective-freeze.json','taxonomy-freeze.json','CLASSIFIER.md'):
        c.require(not (r.HERE/forbidden).exists(),'Forbidden continuation after failure')
    c.require(c.read(r.HERE/'metrics.json')==metrics.compute(),'Metrics do not reconstruct')
    review=c.read(r.HERE/'review/partial-taxonomy-audit.json')
    c.require(review['terminal_commit']==terminal,'Review binding')
    c.require(datetime.fromisoformat(review['at'])>datetime.fromisoformat(partial['at']),'Premature review')
    c.require({x['condition_id'] for x in review['findings']}=={x['identity'] for x in partial['runs']},'Partial review coverage')
    return {'status':'incomplete','historical_bytes_preserved':True,'executed_preparation_preserved':True,'atomic_conditions':196,'taxonomy_completed':4,'taxonomy_unmeasured':192,'prospective_completed':0,'unique_sessions':5,'attempts_after_stop':0,'metrics_reconstructed':True,'terminal_commit':terminal}
if __name__=='__main__': print(json.dumps(verify(),indent=2))
