"""Host launcher: a detached child cannot outlive a tool PID namespace teardown."""
import argparse
import subprocess
import sys
from pathlib import Path
import runner as r
import contracts as c

def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=r.STAGES);a=p.parse_args()
    pid1=Path('/proc/1/comm').read_text().strip()
    c.require(pid1=='systemd','Launch from host namespace (PID 1 systemd), not a tool sandbox')
    r.verify(a.stage,True)
    c.require(not r.git('status','--porcelain').strip(),'Unclean launch')
    if r.state()=='PAUSED_RECOVERABLE':
        proof=r.H/'recovery/premeasurement-launch.json';r.committed(proof);data=c.read(proof)
        c.require(data['classification']=='recoverable_integrity_violation','Invalid recovery classification')
        c.require(not list((r.RT/'runs').rglob('attempt.json')),'This recovery applies only before any attempt')
        c.require(all(x['exit_code']==0 for x in data['checks']),'Recovery preflight failed')
        c.require(data['prepared_sha256']==c.sha(r.H/'claim-warrant-prepared.json'),'Recovery preparation binding')
        r.transition('RUNNING','Committed premeasurement host-launch recovery; no request previously reserved or sent')
    log=r.RT/f'{a.stage}-host-scheduler.log';r.RT.mkdir(parents=True,exist_ok=True)
    with log.open('x') as out:
        process=subprocess.Popen([sys.executable,'-B',str(r.H/'runner.py'),'run','--stage',a.stage],
            cwd=r.R,stdin=subprocess.DEVNULL,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
    r.write(r.RT/f'{a.stage}-host-scheduler.json',{'pid':process.pid,'stage':a.stage,'detached':True,
        'pid1_comm':pid1,'launch_commit':r.head(),'launcher_sha256':c.sha(Path(__file__))})
    print('Detached host scheduler:',process.pid,flush=True)

if __name__=='__main__':main()
