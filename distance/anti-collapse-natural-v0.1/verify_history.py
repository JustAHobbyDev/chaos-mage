"""Historical and new offline checks; exclusively write a new verification record."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent


def run(output):
    commands=[x['command'] for x in json.loads((ROOT/'distance/anti-collapse-v0.1/review/verification.json').read_text())['checks']]
    commands += ['python -B distance/anti-collapse-v0.1/runner.py verify', 'python -B distance/anti-collapse-v0.1/runner.py verify-results --private', 'python -B distance/anti-collapse-v0.1/verify_completion.py --private', 'python -B -m unittest discover -s distance/anti-collapse-natural-v0.1/tests']
    checks=[]
    for cmd in commands:
        p=subprocess.run(cmd,shell=True,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        checks.append({'command':cmd,'exit_code':p.returncode,'output':p.stdout});print(str(p.returncode)+': '+cmd,flush=True)
        if p.returncode:break
    with output.open('x') as f:json.dump({'at':datetime.now(timezone.utc).isoformat(),'historical_test_count':216,'checks':checks,'provider_calls':0},f,indent=2);f.write('\n')
    if any(x['exit_code'] for x in checks):raise SystemExit(1)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);a=p.parse_args();run(a.output)
