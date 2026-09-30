"""Read-only F verification adapter; scopes legacy Git additions, never source bytes.

F's completion uses a historical allowlist that predates G. First validate every
live pre-G file against its starting checkpoint, then evaluate F's legacy Git
queries at that checkpoint. Original F code, scientific inputs and raw responses
are never edited or redirected. Original incomplete-F verification uses its
existing recovery-aware legacy_check(), not the intentionally failed runner.
"""
import argparse,hashlib,json,subprocess,sys,unittest
from pathlib import Path
from unittest.mock import patch
H=Path(__file__).resolve().parent; ROOT=H.parent.parent
BASE='ac79a379938ae07d5a0a5a65e14c6145b60ed08b'

def guard():
 preserved=json.loads((H/'preservation.json').read_text())
 assert preserved['baseline']==BASE
 for name,digest in preserved['files'].items():
  assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'Live historical bytes changed: '+name
 added=subprocess.check_output(['git','diff','--name-only',BASE,'--'],cwd=ROOT,text=True).splitlines()
 added+=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
 for name in added:assert name.startswith('distance/fault-localized-validity-v0.1/') or name in ['docs/PROBLEM_FRAMES-fault-localized-validity-v0.1.md','distance/review/fault-localized-validity-v0.1.md'],'Unauthorized current change: '+name
 return len(preserved['files'])

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['legacy','recovery-tests','completion','recovery-history']); a=p.parse_args()
 count=guard()
 sys.path.insert(0,str(ROOT/'distance/prospective-validity-v0.1'))
 sys.path.insert(0,str(ROOT/'distance/prospective-validity-v0.1/recovery'))
 import evidence as e
 original=e.old.git
 def scoped(*args):
  if args==('diff','--name-only',e.ORIGINAL,'--'):return original('diff','--name-only',e.ORIGINAL,BASE,'--')
  if args==('ls-files','--others','--exclude-standard'):
   lines=original(*args).decode().splitlines()
   lines=[x for x in lines if not x.startswith('distance/fault-localized-validity-v0.1/') and x not in ['docs/PROBLEM_FRAMES-fault-localized-validity-v0.1.md','distance/review/fault-localized-validity-v0.1.md']]
   return ('\n'.join(lines)+('\n' if lines else '')).encode()
  return original(*args)
 with patch.object(e.old,'git',scoped):
  if a.action=='legacy': result=e.legacy_check(tests=True)
  elif a.action=='recovery-tests':
   suite=unittest.defaultTestLoader.discover(str(e.HERE/'tests')); run=unittest.TextTestRunner().run(suite); assert run.wasSuccessful();result={'tests':run.testsRun}
  elif a.action=='completion':
   import publication;result=publication.verify_completion()
  else:
   import verify_recovery_history;result=verify_recovery_history.verify()
 assert guard()==count
 print(json.dumps({'action':a.action,'historical_checkpoint':BASE,'live_preserved_files':count,'result':result},indent=2))
if __name__=='__main__':main()
