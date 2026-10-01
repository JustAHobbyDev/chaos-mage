"""Persistent host-only launcher; no automatic retry or resume."""
import argparse
import subprocess
import sys
from pathlib import Path
import runner as r
import contracts as c

def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=r.STAGES);a=p.parse_args()
    c.require(Path('/proc/1/comm').read_text().strip()=='systemd','Host namespace required')
    r.verify(a.stage,True)
    c.require(not r.git('status','--porcelain').strip(),'Unclean launch')
    r.RT.mkdir(parents=True,exist_ok=True)
    with (r.RT/f'{a.stage}-host-scheduler.log').open('x') as out:
        process=subprocess.Popen([sys.executable,'-B',str(r.H/'runner.py'),'run','--stage',a.stage],cwd=r.R,
            stdin=subprocess.DEVNULL,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
    r.write(r.RT/f'{a.stage}-host-scheduler.json',{'pid':process.pid,'stage':a.stage,'detached':True,
        'pid1_comm':'systemd','launch_commit':r.head(),'launcher_sha256':c.sha(Path(__file__))})
    print('Detached host scheduler:',process.pid,flush=True)

if __name__=='__main__':main()
