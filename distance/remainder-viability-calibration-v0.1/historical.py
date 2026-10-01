"""H.2-only outer scope; inherited verifier code and evidence remain unchanged."""
import concurrent.futures
import json
import runpy
import subprocess
import sys
from unittest.mock import patch
from common import H,R,BASE,guard,allowed,read

def one(command):
    counts=guard();original=subprocess.check_output
    def scoped(cmd,*args,**kwargs):
        if isinstance(cmd,(list,tuple)):
            cmd=list(cmd)
            if cmd[:3]==['git','diff','--name-only'] and len(cmd)==5 and cmd[-1]=='--':cmd.insert(-1,BASE)
            result=original(cmd,*args,**kwargs)
            if cmd==['git','ls-files','--others','--exclude-standard']:
                binary=isinstance(result,bytes);lines=(result.decode() if binary else result).splitlines()
                result=''.join(x+'\n' for x in lines if not allowed(x))
                if binary:result=result.encode()
            return result
        return original(cmd,*args,**kwargs)
    is_h1=any('fault-localized-calibration-v0.2/' in x or x.endswith('fault-localized-calibration-v0.2') for x in command)
    h1=H.with_name('fault-localized-calibration-v0.2')
    # H.1's adapter pins its inherited queries to H. Our outer adapter only pins
    # still-implicit live comparisons to the H.1 publication after byte checks.
    sys.path=[x for x in sys.path if x and str(H)!=x]
    for name in ['runner','contracts']:sys.modules.pop(name,None)
    with patch.object(subprocess,'check_output',scoped):
        if not is_h1:
            sys.path.insert(0,str(h1));sys.argv=[str(h1/'historical.py'),'--command-json',json.dumps(command)]
            runpy.run_path(str(h1/'historical.py'),run_name='__main__')
        else:
            args=command[1:]
            if args[0]=='-B':args=args[1:]
            if args[0]=='-m':
                sys.path.insert(0,str(R));sys.argv=[args[1],*args[2:]]
                try:runpy.run_module(args[1],run_name='__main__')
                except SystemExit as e:
                    if e.code:raise
            else:
                script=R/args[0];sys.path.insert(0,str(script.parent));sys.argv=[str(script),*args[1:]]
                runpy.run_path(str(script),run_name='__main__')
    assert guard()==counts

def all_checks():
    commands=[r['command'] for r in read(H.with_name('fault-localized-calibration-v0.2')/'review/historical-verification.json')['checks']]
    commands += [['python','-B','-m','unittest','discover','-s','distance/fault-localized-calibration-v0.2/tests','-p','test_*.py'],['python','-B','distance/fault-localized-calibration-v0.2/publication.py','verify']]
    def run(cmd):
        p=subprocess.run([sys.executable,'-B',str(H/'historical.py'),'--command-json',json.dumps(cmd)],cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
        return {'command':cmd,'exit_code':p.returncode,'output':p.stdout}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(run,commands))
    return rows

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--command-json',required=True);a=p.parse_args();one(json.loads(a.command_json))
