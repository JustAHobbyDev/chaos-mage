"""Run the frozen B.2 verification inventory plus D tests; no provider calls."""
import argparse, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent

def run(output):
 commands=[x['command'] for x in json.loads((ROOT/'distance/common-evidence-displacement-v0.3/review/verification.json').read_text())['checks']]
 commands.append("python -B -m unittest discover -s distance/anti-collapse-v0.1/tests -p 'test_*.py'")
 results=[]
 for cmd in commands:
  proc=subprocess.run(cmd,shell=True,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  results.append({'command':cmd,'exit_code':proc.returncode,'output':proc.stdout})
  print(f'{proc.returncode}: {cmd}',flush=True)
  if proc.returncode:break
 record={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'historical_expected_tests':172,'checks':results,'provider_measurements_rerun':False}
 with output.open('x') as f:f.write(json.dumps(record,indent=2)+'\n')
 if any(x['exit_code'] for x in results):raise SystemExit(1)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('output',type=Path);a=p.parse_args();run(a.output)
