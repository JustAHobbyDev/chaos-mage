"""Run unchanged G tests after live-byte checks, with only Git scope adapted."""
import importlib.util,subprocess,sys,unittest
from pathlib import Path
from unittest.mock import patch
H=Path(__file__).resolve().parents[2];R=H.parent.parent
spec=importlib.util.spec_from_file_location('h_history',H/'historical.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
counts=h.guard();original=subprocess.check_output

def scoped(command,*args,**kwargs):
 command=list(command)
 if command[:3]==['git','diff','--name-only'] and len(command)==5 and command[-1]=='--':command.insert(-1,h.BASE)
 result=original(command,*args,**kwargs)
 if command==['git','ls-files','--others','--exclude-standard']:
  binary=isinstance(result,bytes);lines=(result.decode() if binary else result).splitlines()
  result=''.join(x+'\n' for x in lines if not h.allowed(x))
  if binary:result=result.encode()
 return result

g=R/'distance/fault-localized-validity-v0.1';sys.path.insert(0,str(g))
with patch.object(subprocess,'check_output',scoped):
 suite=unittest.defaultTestLoader.discover(str(g/'tests'));result=unittest.TextTestRunner().run(suite)
assert h.guard()==counts
if not result.wasSuccessful():raise SystemExit(1)
print('All original G tests passed; historical source and runtime bytes unchanged.')
