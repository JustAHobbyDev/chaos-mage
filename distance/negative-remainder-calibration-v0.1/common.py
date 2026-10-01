"""H.3 identities and read-only historical preservation."""
import hashlib
import json
import subprocess
from pathlib import Path

H=Path(__file__).resolve().parent
R=H.parent.parent
BASE='e35948a601fefabb648218cde728aa7fdc1651d2'
ALLOWED=['distance/negative-remainder-calibration-v0.1/',
         'distance/review/negative-remainder-calibration-v0.1.md',
         'docs/PROBLEM_FRAMES-negative-remainder-calibration-v0.1.md']
def require(ok,message):
    if not ok: raise ValueError(message)
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(v,f,indent=2,ensure_ascii=False);f.write('\n')
def allowed(p):return any(p.startswith(x) if x.endswith('/') else p==x for x in ALLOWED)
def guard():
    p=read(H/'preservation.json')
    require(p['baseline']==BASE,'Wrong preservation base')
    require(git('show','ebc9ea0:distance/negative-remainder-calibration-v0.1/preservation.json')==(H/'preservation.json').read_bytes(),'Preservation manifest drift')
    for name,digest in {**p['files'],**p['historical_runtime']}.items():require(sha(R/name)==digest,'Historical bytes changed: '+name)
    changes=git('diff','--name-only',BASE,'--').decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines()
    require(all(allowed(n) for n in changes),'Out-of-scope change')
    require(git('branch','--show-current').decode().strip()=='experiment-h3-negative-remainders','Wrong branch')
    subprocess.check_call(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=R)
    return {'tracked':len(p['files']),'runtime':len(p['historical_runtime'])}
