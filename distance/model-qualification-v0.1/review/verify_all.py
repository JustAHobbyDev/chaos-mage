#!/usr/bin/env python3
"""Read-only historical and qualification verification, gated on the result freeze."""
import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('qualification_verification', HERE/'runner.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


def main():
    r.complete_results()
    inventory = r.read(r.ROOT/'distance/common-evidence-displacement-v0.3/review/verification.json')
    commands = [c['command'] for c in inventory['checks']]
    commands += [
        'python -B -m unittest discover -s distance/anti-collapse-v0.1/tests',
        'python -B distance/anti-collapse-v0.1/verify_completion.py --private',
        'python -B -m unittest discover -s distance/anti-collapse-natural-v0.1/tests',
        'python -B distance/anti-collapse-natural-v0.1/review/verify_incomplete.py --private',
        'python -B -m unittest discover -s distance/anti-collapse-natural-recovery-v0.1/tests',
        'python -B distance/anti-collapse-natural-recovery-v0.1/review/verify_completion.py --private',
        'python -B -m unittest discover -s distance/family-b-bridge-v0.1/tests',
        'python -B distance/family-b-bridge-v0.1/verify_incomplete.py --private',
        'python -B -m unittest discover -s distance/model-qualification-v0.1/tests',
        'python -B distance/model-qualification-v0.1/runner.py verify',
        'git diff --check',
    ]
    checks=[]
    for command in dict.fromkeys(commands):
        result=subprocess.run(shlex.split(command),cwd=r.ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        matches=re.findall(r'Ran (\d+) tests? in',result.stdout)
        checks.append({'command':command,'exit_code':result.returncode,'reported_tests':sum(map(int,matches)),'output':result.stdout})
        print(f'{result.returncode}: {command}',flush=True)
        if result.returncode:break
    record={'at':r.now(),'results_freeze_commit':r.checkpoint(HERE/'results-freeze.json'),
        'checks':checks,'total_tests':sum(c['reported_tests'] for c in checks),'new_provider_calls':0,
        'passed':all(c['exit_code']==0 for c in checks)}
    r.write(HERE/'review/verification.json',record)
    if not record['passed']:raise SystemExit(1)


if __name__=='__main__':main()
