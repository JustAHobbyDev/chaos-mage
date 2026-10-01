"""Read-only H.3 verification scoped to its exact publication; never runs providers."""
import json
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch
H=Path(__file__).resolve().parent;R=H.parents[1]
BASE='8f488b3b02973370e26fd970a5fd5a8d56e8bec6'
OLD=H.with_name('negative-remainder-calibration-v0.1')

def one(args):
    original=subprocess.check_output
    def scoped(cmd,*a,**kw):
        cmd=list(cmd)
        if cmd==['git','branch','--show-current']:return 'experiment-h3-negative-remainders\n' if kw.get('text') else b'experiment-h3-negative-remainders\n'
        if cmd[:3]==['git','diff','--name-only'] and len(cmd)==5 and cmd[-1]=='--':cmd.insert(-1,BASE)
        output=original(cmd,*a,**kw)
        if cmd==['git','ls-files','--others','--exclude-standard']:
            binary=isinstance(output,bytes);lines=(output.decode() if binary else output).splitlines()
            output=''.join(x+'\n' for x in lines if not (x.startswith('distance/inquiry-unitization-calibration-v0.1/') or x in ['distance/review/inquiry-unitization-calibration-v0.1.md','docs/PROBLEM_FRAMES-inquiry-unitization-calibration-v0.1.md']))
            if binary:output=output.encode()
        return output
    sys.path=[str(OLD)]+[p for p in sys.path if p and p!=str(H)]
    with patch.object(subprocess,'check_output',scoped):
        if args[0]=='-m':sys.argv=args[1:];runpy.run_module(args[1],run_name='__main__')
        else:sys.argv=args;runpy.run_path(args[0],run_name='__main__')

def checks():
    commands=[[str(OLD/'runner.py'),'verify'],[str(OLD/'recovery.py'),'verify'],
              ['-m','unittest','discover','-s',str(OLD/'tests'),'-p','test_*.py'],
              ['-m','unittest','discover','-s',str(OLD/'recovery/tests'),'-p','test_*.py']]
    rows=[]
    for args in commands:
        p=subprocess.run([sys.executable,'-B',str(H/'historical.py'),json.dumps(args)],cwd=R,text=True,capture_output=True,timeout=600)
        rows.append({'command':[sys.executable,'-B',*args],'exit_code':p.returncode,'output':p.stdout+p.stderr})
    return rows
if __name__=='__main__':one(json.loads(sys.argv[1]))
