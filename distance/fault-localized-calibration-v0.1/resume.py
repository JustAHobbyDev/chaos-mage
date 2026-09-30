"""Committed daemon-restart recovery; never reschedules a reserved observation."""
import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
from pathlib import Path
import runner as r
import contracts as c
import continuation as k
REC=r.H/'recovery/daemon-restart'

def original_completion():
 incident=c.read(REC/'incident.json');r.hashes(incident['preserved_observation_files'])
 d=r.RT/'runs/ablation'/incident['interrupted_case']
 reserve=c.read(d/'reservation.json');events=[json.loads(x,object_pairs_hook=c.unique) for x in (d/'events.jsonl').read_text().splitlines() if x.strip()]
 metadata=r.audit_events(events)
 finals=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
 c.require(len(finals)==1 and finals[0].strip()==(d/'response.json').read_text().strip(),'Interrupted final mismatch')
 c.require(c.sha(d/'prompt.txt')==c.sha(r.packet('ablation',d.name))==reserve['packet_sha256'],'Interrupted prompt drift')
 c.require(c.sha(r.H/'schemas/ablation.schema.json')==reserve['schema_sha256'],'Interrupted schema drift')
 c.require(reserve['configuration']==r.cfg() and reserve['command']==r.command(reserve['working_directory'],d,'ablation'),'Interrupted command/config drift')
 r.validate_response(c.read(d/'response.json'),'ablation',d.name)
 c.require(c.read(d/'validation.json')['metadata']==metadata,'Supplementary audit drift')
 c.require(not (d/'exit.json').exists(),'Missing exit status must remain unavailable')
 return metadata

def gate():
 r.verify('ablation',True);r.binary_check();original_completion()
 incident=c.read(REC/'incident.json');r.hashes(incident['unchanged_scientific_files'])
 r.hashes(c.read(REC/'prepared.json')['files'])
 ids=sorted(p.name for p in (r.RT/'runs/ablation').iterdir())
 c.require(ids==sorted(incident['completed_prefix']),'New/ambiguous reservations since recovery audit')
 for cid in ids:
  d=r.RT/'runs/ablation'/cid;v=c.read(d/'validation.json')
  c.require(v['status']=='valid','Incomplete prior observation')
  r.validate_response(c.read(d/'response.json'),'ablation',cid)
 c.require(incident['completed_prefix']==r.order('ablation')[:len(ids)],'Not a completed prefix')
 return incident

def preflight():
 incident=gate();checks=[]
 commands=c.read(r.H/'recovery/premeasurement/historical-commands.json')+[['python','-B','-m','unittest','discover','-s',r.rel(r.H/'tests'),'-p','test_*.py'],['python','-B',r.rel(r.H/'resume.py'),'verify-recovery']]
 def check(command):
  x=subprocess.run(command,cwd=r.R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
  return {'command':command,'exit_code':x.returncode,'output':x.stdout}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for x in pool.map(check,commands):
   checks.append(x);print(f'recovery check {len(checks)}/{len(commands)} {x["exit_code"]}',flush=True)
 r.write(REC/'preflight.json',{'at':r.now(),'input_commit':r.head(),'prepared_sha256':c.sha(REC/'prepared.json'),'checks':checks,'provider_calls':0})
 c.require(all(x['exit_code']==0 for x in checks),'Recovery preflight failed');gate()

def run():
 incident=gate()
 for p in [REC/'incident.json',REC/'prepared.json',REC/'preflight.json',r.H/'resume.py']:
  r.committed(p)
 p=c.read(REC/'preflight.json');c.require(p['prepared_sha256']==c.sha(REC/'prepared.json') and all(x['exit_code']==0 for x in p['checks']),'Recovery preflight binding')
 for name in c.read(REC/'prepared.json')['files']:r.committed(r.R/name)
 c.require(r.state()=='PAUSED_RECOVERABLE','Not the authorized recovery pause')
 c.require(not r.git('status','--porcelain').strip(),'Unclean resume')
 initial=r.head();r.transition('RUNNING','Committed daemon recovery; preserve first four ablations, continue unreserved suffix')
 try:
  for index,cid in enumerate(r.order('ablation')):
   if index<len(incident['completed_prefix']):continue
   c.require(r.state()=='RUNNING' and r.head()==initial,'Resume state/checkpoint changed')
   r.verify('ablation',True);r.hashes(c.read(REC/'prepared.json')['files'])
   c.require(not (r.RT/'runs/ablation'/cid).exists(),'Refuse repeated reservation')
   r.execute('ablation',cid);print(f'ablation {index+1}/24 {cid}: valid',flush=True)
  r.transition('COMPLETE','ablation')
 except Exception as error:
  if r.state()=='RUNNING':r.transition('PAUSED_AMBIGUOUS',str(error))
  raise

def launch():
 gate()
 # Detach the scheduler, not a new or changed scientific request, from the daemon.
 with (r.RT/'resume-stdout.txt').open('x') as out,(r.RT/'resume-stderr.txt').open('x') as err:
  process=subprocess.Popen([sys.executable,'-B',str(r.H/'resume.py'),'run'],cwd=r.R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True)
 r.write(r.RT/'resume-launch.json',{'at':r.now(),'scheduler_pid':process.pid,'command':[sys.executable,'-B',str(r.H/'resume.py'),'run'],'detached_from_daemon':True,'input_commit':r.head()})
 print(json.dumps({'scheduler_pid':process.pid,'status':'launched; observe append-only states and original reservations'}))

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['preflight','run','launch','verify-recovery']);a=p.parse_args()
 if a.action=='verify-recovery':print(json.dumps({'original_completion':original_completion(),'scientific_inputs_unchanged':True}))
 else:globals()[a.action]()
if __name__=='__main__':main()
