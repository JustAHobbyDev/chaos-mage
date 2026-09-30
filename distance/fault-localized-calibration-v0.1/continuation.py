"""Additive premeasurement verifier routing; scientific inputs/runner unchanged."""
import argparse,json
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
import runner as r
import contracts as c
REC=r.H/'recovery/premeasurement'

@contextmanager
def context():
 original_read=c.read;original_write=r.write
 def read(path):
  p=Path(path)
  if p==r.H/'historical-commands.json':return original_read(REC/'historical-commands.json')
  if p==r.H/'review/claim-warrant-preflight.json':return original_read(REC/'claim-warrant-preflight.json')
  return original_read(p)
 def write(path,value):
  p=Path(path)
  if p==r.H/'review/claim-warrant-preflight.json':p=REC/'claim-warrant-preflight.json'
  return original_write(p,value)
 with patch.object(c,'read',read),patch.object(r,'write',write):yield

def gate(stage):
 incident=c.read(REC/'incident.json');r.hashes(incident['unchanged_scientific_files'])
 for p in [REC/'incident.json',REC/'historical-commands.json',REC/'g_tests.py',r.H/'continuation.py']:
  r.committed(p)
 if stage=='claim-warrant':
  p=REC/'claim-warrant-preflight.json';r.committed(p)
  c.require(all(x['exit_code']==0 for x in c.read(p)['checks']),'Recovery preflight incomplete')

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['preflight','run']);p.add_argument('--stage',choices=r.STAGES,default='claim-warrant');a=p.parse_args()
 if a.action=='run':
  gate(a.stage)
  if r.state()=='PAUSED_RECOVERABLE':
   c.require(not list((r.RT/'runs').glob('*/*/reservation.json')),'Unexpected premeasurement reservation')
   r.transition('RUNNING','Committed premeasurement recovery; inputs unchanged and all verifiers pass')
 with context():getattr(r,a.action)(a.stage)
if __name__=='__main__':main()
