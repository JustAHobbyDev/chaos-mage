#!/usr/bin/env python3
"""Run historical checks only after complete freeze and independent assessment."""
import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gemini_checks',HERE/'runner.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)


def main():
    r.complete_results()
    r.require((HERE/'review/preliminary.json').exists(),'Independent assessment must precede historical checks')
    commands=[v['command'] for v in r.read(r.ROOT/'distance/common-evidence-displacement-v0.3/review/verification.json')['checks']]
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
        'python -B distance/model-qualification-v0.1/review/verify_report.py',
        'python -B -m unittest discover -s distance/model-qualification-gemini-v0.1/tests',
        'python -B distance/model-qualification-gemini-v0.1/review/verify_incomplete.py',
        'python -B -m unittest discover -s distance/model-qualification-gemini-v0.2/tests',
        'python -B distance/model-qualification-gemini-v0.2/runner.py verify',
        'git diff --check']
    checks=[]
    for cmd in dict.fromkeys(commands):
        p=subprocess.run(shlex.split(cmd),cwd=r.ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        tests=sum(map(int,re.findall(r'Ran (\d+) tests? in',p.stdout)))
        checks.append({'command':cmd,'exit_code':p.returncode,'reported_tests':tests,'output':p.stdout})
        print(str(p.returncode)+': '+cmd,flush=True)
        if p.returncode:break
    r.write(HERE/'review/verification.json',{'at':r.now(),'results_freeze_commit':r.checkpoint(HERE/'results-freeze.json'),
        'checks':checks,'total_tests':sum(x['reported_tests'] for x in checks),'passed':all(x['exit_code']==0 for x in checks),
        'new_provider_calls':0,'historical_policy_checked_before_any_authorized_family_update':True})
    if any(x['exit_code'] for x in checks):sys.exit(1)


if __name__=='__main__':main()
