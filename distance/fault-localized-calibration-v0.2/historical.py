"""Read-only historical verification against H, after checking live inherited bytes."""
import argparse, concurrent.futures, json, runpy, subprocess, sys
from pathlib import Path
from unittest.mock import patch
import runner as h1
H=h1.H;R=h1.R

def one(command):
 counts=h1.guard();original=subprocess.check_output
 def scoped(cmd,*args,**kwargs):
  if isinstance(cmd,(list,tuple)):
   cmd=list(cmd)
   # Pin only an implicit working-tree comparison, never an explicit historical range.
   if cmd[:3]==['git','diff','--name-only'] and len(cmd)==5 and cmd[-1]=='--':cmd.insert(-1,h1.BASE)
   value=original(cmd,*args,**kwargs)
   if cmd==['git','ls-files','--others','--exclude-standard']:
    binary=isinstance(value,bytes);lines=(value.decode() if binary else value).splitlines();value=''.join(x+'\n' for x in lines if not h1.allowed(x))
    if binary:value=value.encode()
   return value
  return original(cmd,*args,**kwargs)
 args=command[1:]
 if args[0]=='-B':args=args[1:]
 sys.path=[x for x in sys.path if Path(x or '.').resolve()!=H]
 for name in ['runner','contracts']:sys.modules.pop(name,None)
 code=0
 try:
  with patch.object(subprocess,'check_output',scoped):
   if args[0]=='-m':
    sys.path.insert(0,str(R));sys.argv=[args[1],*args[2:]];runpy.run_module(args[1],run_name='__main__')
   else:
    script=R/args[0];sys.path.insert(0,str(script.parent));sys.argv=[str(script),*args[1:]];runpy.run_path(str(script),run_name='__main__')
 except SystemExit as e:code=e.code or 0
 finally:
  if h1.guard()!=counts:raise RuntimeError('Inherited verification changed evidence')
 if code:raise SystemExit(code)

def all_checks():
 old=H.with_name('fault-localized-calibration-v0.1')
 commands=json.loads((old/'recovery/premeasurement/historical-commands.json').read_text())
 commands+=[['python','-B','-m','unittest','discover','-s','distance/fault-localized-calibration-v0.1/tests','-p','test_*.py'],['python','-B','distance/fault-localized-calibration-v0.1/publication.py','verify']]
 def run(cmd):
  p=subprocess.run([sys.executable,'-B',str(H/'historical.py'),'--command-json',json.dumps(cmd)],cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
  return {'command':cmd,'exit_code':p.returncode,'output':p.stdout}
 rows=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for x in pool.map(run,commands):
   rows.append(x);print(f"historical check {len(rows)}/{len(commands)}: {x['exit_code']}",flush=True)
 out={'type':'read_only_historical_verification_not_measurement_preflight','input_commit':h1.git('rev-parse','HEAD').decode().strip(),'preservation':h1.guard(),'checks':rows,'provider_calls':0}
 with (H/'review/historical-verification.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
 if any(x['exit_code'] for x in rows):raise SystemExit(1)

def main():
 p=argparse.ArgumentParser();p.add_argument('--command-json');p.add_argument('--all',action='store_true');a=p.parse_args()
 if a.all:all_checks()
 elif a.command_json:one(json.loads(a.command_json))
 else:p.error('Choose --all or --command-json')
if __name__=='__main__':main()
