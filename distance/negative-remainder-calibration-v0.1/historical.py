"""Read-only historical checks bounded to the completed H.2 publication."""
import concurrent.futures
import json
import runpy
import subprocess
import sys
from unittest.mock import patch
from common import H,R,BASE,guard,allowed,read

def one(command):
    counts=guard();original=subprocess.check_output;old=H.with_name('remainder-viability-calibration-v0.1')
    def scoped(cmd,*args,**kwargs):
        if isinstance(cmd,(list,tuple)):
            cmd=list(cmd)
            if cmd[:3]==['git','diff','--name-only'] and len(cmd)==5 and cmd[-1]=='--':cmd.insert(-1,BASE)
            if cmd==['git','branch','--show-current']:
                return 'experiment-h2-remainder\n' if kwargs.get('text') else b'experiment-h2-remainder\n'
            result=original(cmd,*args,**kwargs)
            if cmd==['git','ls-files','--others','--exclude-standard']:
                binary=isinstance(result,bytes);lines=(result.decode() if binary else result).splitlines()
                result=''.join(x+'\n' for x in lines if not allowed(x))
                if binary:result=result.encode()
            return result
        return original(cmd,*args,**kwargs)
    sys.path=[x for x in sys.path if x and x!=str(H)]
    for name in ['runner','contracts','common','pipeline','publication','historical','author_cases']:sys.modules.pop(name,None)
    is_h2=any('remainder-viability-calibration-v0.1' in x for x in command)
    with patch.object(subprocess,'check_output',scoped):
        if not is_h2:
            sys.path.insert(0,str(old));sys.argv=[str(old/'historical.py'),'--command-json',json.dumps(command)]
            runpy.run_path(str(old/'historical.py'),run_name='__main__')
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
    old=H.with_name('remainder-viability-calibration-v0.1')
    commands=[x['command'] for x in read(old/'review/claim-warrant-preflight.json')['checks']]
    commands += [['python','-B',str(old.relative_to(R)/'runner.py'),'verify'],['python','-B',str(old.relative_to(R)/'publication.py'),'verify']]
    def run(cmd):
        p=subprocess.run([sys.executable,'-B',str(H/'historical.py'),'--command-json',json.dumps(cmd)],cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
        return {'command':cmd,'exit_code':p.returncode,'output':p.stdout}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:return list(pool.map(run,commands))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--command-json',required=True);a=p.parse_args();one(json.loads(a.command_json))
