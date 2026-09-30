"""H-only adapter: live byte checks precede scoped historical Git queries."""
import json, subprocess, sys, runpy
from pathlib import Path
from unittest.mock import patch
H=Path(__file__).resolve().parent;R=H.parent.parent
BASE='c3eefbbd5388c74445b552f7089c6da99dafe491'
ALLOWED=['distance/fault-localized-calibration-v0.1/', 'docs/PROBLEM_FRAMES-fault-localized-calibration-v0.1.md','distance/review/fault-localized-calibration-v0.1.md']
def allowed(path):return any(path.startswith(p) if p.endswith('/') else path==p for p in ALLOWED)
def guard():
 import hashlib
 p=json.loads((H/'preservation.json').read_text())
 assert p['baseline']==BASE
 for name,digest in {**p['files'],**p['historical_runtime']}.items():
  assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest,'Historical bytes changed: '+name
 changed=subprocess.check_output(['git','diff','--name-only',BASE,'--'],cwd=R,text=True).splitlines()
 changed+=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines()
 assert all(allowed(x) for x in changed), 'Out-of-scope change'
 return {'tracked':len(p['files']),'runtime':len(p['historical_runtime'])}
def main():
 action=sys.argv[1];counts=guard();original=subprocess.check_output
 def scoped(command,*args,**kwargs):
  command=list(command)
  if command[:3]==['git','diff','--name-only'] and len(command)==5 and command[-1]=='--':
   command.insert(-1,BASE)
  result=original(command,*args,**kwargs)
  if command==['git','ls-files','--others','--exclude-standard']:
   binary=isinstance(result,bytes);lines=(result.decode() if binary else result).splitlines()
   result=''.join(x+'\n' for x in lines if not allowed(x))
   if binary:result=result.encode()
  return result
 g=R/'distance/fault-localized-validity-v0.1'
 sys.path.insert(0,str(g));sys.argv=[str(g/'historical.py'),action]
 with patch.object(subprocess,'check_output',scoped):runpy.run_path(str(g/'historical.py'),run_name='__main__')
 assert guard()==counts
if __name__=='__main__':main()
