"""Read-only independent execution/freeze chronology and result verification."""
from datetime import datetime
from pathlib import Path
import json
import runner as r
import contracts as c

def verify(private=True):
    inputs=r.verify(); sessions=[]; attempts=[]; stage_counts={}
    for stage in ('taxonomy','prospective'):
        prepared=r.HERE/f'{stage}-prepared.json'
        if not prepared.exists(): continue
        pc=r.checkpoint(prepared)
        probe=r.HERE/'probes'/f'{stage}.json'
        if probe.exists():
            p=c.read(probe); c.require(p['input_commit']==pc,'Probe not at preparation checkpoint')
            c.require(p['prepared_sha256']==c.sha(prepared),'Probe/preparation drift')
            r.committed(prepared,p['input_commit'])
        stage_res=r.RUNTIME/f'{stage}-reservation.json'
        if stage_res.exists():
            c.require(probe.exists(),'Measurements without probe')
            c.require(c.read(stage_res)['commit']==r.checkpoint(probe),'Measurements not at successful probe checkpoint')
        ds=[]
        for kind in ('probes','runs'):
            parent=r.RUNTIME/kind/stage
            ds += list(parent.glob('*')) if parent.exists() else []
        ds.sort(key=lambda d:c.read(d/'attempt.json')['at'])
        last=None; completed=[]
        for d in ds:
            a=c.read(d/'attempt.json'); attempts.append(a)
            c.require(a['harness_attempt']==1,'Harness retry')
            v=c.read(d/'validation.json'); end=datetime.fromisoformat(v['finished_at']); start=datetime.fromisoformat(a['at'])
            c.require(start<=end and (last is None or last<=start),'Nonsequential execution'); last=end
            reservation=d/'reservation.json'
            if reservation.exists():
                x=c.read(reservation)
                c.require(x['input_commit']==a['input_commit'],'Commit provenance mismatch')
                c.require(x['configuration']==r.config(),'Config drift')
                c.require(x['command']==r.command(x['working_directory'],d,stage),'Command drift')
                c.require(x['packet_sha256']==c.sha(d/'prompt.txt'),'Packet hash drift')
                for suffix,key in [('', 'canonical_schema_sha256'),('-wire','wire_schema_sha256')]: c.require(x[key]==c.sha(r.HERE/'schemas'/f'{stage}{suffix}.schema.json'),'Schema drift')
            if v['status']=='valid':
                events=[json.loads(s,object_pairs_hook=c.unique) for s in (d/'events.jsonl').read_text().splitlines() if s.strip()]
                c.require(r.audit_events(events)==v['metadata'],'Event audit drift')
                sessions.append(v['metadata']['session_id'])
                c.validate(c.read(d/'response.json'),stage,a['identity'])
                if a['kind']=='probes': c.require(c.read(d/'response.json')==r.probe_fixture(stage),'Probe fixture drift')
                else:
                    c.require((d/'prompt.txt').read_text()==r.packet(stage,a['identity']),'Executed packet changed')
                    completed.append(a['identity'])
        stage_counts[stage]={'attempts':len(ds),'measurements':len(completed)}
        c.require(sum(a['kind']=='probes' and a['stage']==stage for a in attempts)<=1,'Extra probe')
        observed=[a['identity'] for a in attempts if a['kind']=='runs' and a['stage']==stage]
        c.require(observed==r.order(stage)[:len(observed)],'Execution order / prefix mismatch')
        f=r.HERE/f'{stage}-freeze.json'
        if f.exists():
            x=c.read(f); c.require(completed==r.order(stage),'Incomplete successful freeze')
            c.require([v['identity'] for v in x['runs']]==completed,'Frozen order changed')
            c.require(last<=datetime.fromisoformat(x['at']),'Freeze precedes completion')
            r.committed(f)
            for entry in x['runs']:
                p=r.HERE/('taxonomy-judgments' if stage=='taxonomy' else 'judgments')/f'{entry["identity"]}.json'
                c.require(c.sha(p)==entry['response_sha256'],'Published response changed')
                if private: r.verify_hashes(entry['files'])
        if stage=='prospective':
            audit=r.HERE/'review/taxonomy-audit.json'; r.committed(audit,c.read(prepared)['parent_commit'])
            r.committed(r.HERE/'taxonomy-freeze.json',c.read(prepared)['parent_commit'])
    c.require(len(sessions)==len(set(sessions)),'Session reuse')
    c.require(len(attempts)==len({(a['kind'],a['stage'],a['identity']) for a in attempts}),'Duplicate attempt')
    f=r.HERE/'failure-freeze.json'
    if f.exists():
        frozen=c.read(f); r.verify_hashes(frozen['files'])
        c.require(frozen['files']==r.inventory(r.RUNTIME.rglob('*')),'New execution after failure freeze')
        status='incomplete'
    else: status='complete' if (r.HERE/'prospective-freeze.json').exists() else 'prepared or collecting'
    return {**inputs,'status':status,'stages':stage_counts,'unique_sessions':len(sessions),'attempts':len(attempts),'harness_retries':0}

if __name__=='__main__': print(json.dumps(verify(),indent=2))
