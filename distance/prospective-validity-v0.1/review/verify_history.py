"""Run established offline historical checks without historical-directory writes."""
import concurrent.futures
import json
from pathlib import Path
import shlex
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner as r
import contracts as c

def main():
    old=c.read(r.ROOT/'distance/anti-collapse-natural-recovery-v0.1/review/historical-verification.json')
    commands=[shlex.split(x['command']) for x in old['checks'] if x['command']!='git diff --check']
    # Include recovery, qualification and bridge suites added since historical E.
    dirs=sorted({str(p.parent.relative_to(r.ROOT)) for p in r.ROOT.glob('distance/**/test_*.py') if 'prospective-validity-v0.1' not in p.parts})
    existing={cmd[cmd.index('-s')+1] for cmd in commands if '-s' in cmd}
    for d in dirs:
        if d not in existing: commands.append(['python','-B','-m','unittest','discover','-s',d,'-p','test_*.py'])
    commands += [['python','-B','distance/anti-collapse-natural-v0.1/review/verify_incomplete.py','--private'],['python','-B','distance/anti-collapse-natural-recovery-v0.1/review/verify_completion.py','--private']]
    for name in ['distance/model-qualification-v0.1/review/verify_report.py','distance/model-qualification-gemini-v0.1/review/verify_incomplete.py','distance/family-b-bridge-v0.1/verify_incomplete.py']:
        commands.append(['python','-B',name,'--private'])
    def check(cmd):
        result=subprocess.run(cmd,cwd=r.ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300)
        return {'command':cmd,'exit_code':result.returncode,'output':result.stdout}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(check,commands))
    r.verify_hashes(c.read(r.HERE/'preservation.json')['files'])
    r.write(r.HERE/'review/historical-verification-restored.json',{'at':r.now(),'checks':results,'historical_bytes_preserved':True,'provider_calls':0})
    print(json.dumps({'checks':len(results),'failed':[x['command'] for x in results if x['exit_code']]}))
    if any(x['exit_code'] for x in results): sys.exit(1)
if __name__=='__main__': main()
