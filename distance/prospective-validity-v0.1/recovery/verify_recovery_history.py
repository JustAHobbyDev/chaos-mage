"""Supplemental additive verification of committed pause/resume provenance."""
from datetime import datetime
import json
import continuation as r


def verify():
    events = r.state_events()
    c, old = r.c, r.old
    c.require(events and events[0]['state'] == 'RUNNING', 'Missing initial recovery transition')
    resumes = []
    for index, event in enumerate(events):
        if event['state'] != 'RUNNING': continue
        binding = event['evidence']
        path = r.ROOT / binding['path']
        old.committed(path, event['commit'])
        c.require(c.sha(path) == binding['sha256'], 'State recovery binding changed')
        record = c.read(path)
        c.require(record['classification'] == 'recoverable_integrity_violation', 'Unproved resumption')
        if index == 0:
            r.e.gate(record)
        else:
            previous = events[index-1]
            c.require(previous['state'] in ('PAUSED_RECOVERABLE', 'PAUSED_AMBIGUOUS'), 'Invalid resume transition')
            c.require(record['incident_sha256'] == event['previous_sha256'], 'Incident/state binding mismatch')
            c.require(record['authorization'] == old.rel(r.HERE/'AUTHORIZATION.md') and record['remediation'], 'Missing remediation authority')
            old.verify_hashes(record['files'])
            if record['incident']['kind'] == 'local_git_checkpoint_permission':
                c.require(record['incident']['prospective_primary_attempts'] == 0, 'Unexpected affected primary request')
                pause_at = datetime.fromisoformat(previous['at'])
                for directory in r.run_directories('prospective'):
                    c.require(datetime.fromisoformat(c.read(directory/'process.json')['launched_at']) > pause_at,
                              'Primary request existed at bookkeeping pause')
        resumes.append({'state_index':index,'record':binding['path'],'commit':event['commit'],'classification':record['classification']})
    launches = 0
    for stage in ('taxonomy','prospective'):
        for kind in ('runs','probes'):
            for directory in r.run_directories(stage,kind):
                process = directory/'process.json'
                if not process.exists(): continue
                launched = datetime.fromisoformat(c.read(process)['launched_at'])
                preceding = [event for event in events if datetime.fromisoformat(event['at']) <= launched]
                c.require(preceding and preceding[-1]['state']=='RUNNING','Provider launch during pause/terminal state')
                launches += 1
    return {'resumptions':resumes,'new_provider_launches':launches,'no_launch_during_pause':True,
            'original_stop_unchanged':r.c.sha(r.old.RUNTIME/'STOP.json') == r.c.read(r.F/'failure-freeze.json')['files'][r.old.rel(r.old.RUNTIME/'STOP.json')]}


if __name__=='__main__': print(json.dumps(verify(),indent=2))
