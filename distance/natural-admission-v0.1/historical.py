"""Read-only historical publication scope; live historical bytes checked first."""
import json
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch
H=Path(__file__).resolve().parent;R=H.parents[1]
PUBLICATIONS={
'negative-remainder-calibration-v0.1':('8f488b3b02973370e26fd970a5fd5a8d56e8bec6','experiment-h3-negative-remainders'),
'inquiry-unitization-calibration-v0.1':('bdeeb973b794823a35257f472a020e12d816a8a9','experiment-h4-inquiry-unitization'),
'span-provenance-calibration-v0.1':('fae0c0b742cd3bcbc7b54599fa9f6234b0ffdc4b','experiment-h5-span-provenance')}
def main(name):
    import hashlib
    for path, expected in json.loads((H/"preservation.json").read_text())["files"].items():
        assert hashlib.sha256((R/path).read_bytes()).hexdigest()==expected, path
    commit,branch=PUBLICATIONS[name];original=subprocess.check_output
    def scoped(cmd,*args,**kwargs):
        cmd=list(cmd)
        if cmd==['git','branch','--show-current']:return branch+'\n' if kwargs.get('text') else (branch+'\n').encode()
        if cmd[:3]==['git','diff','--name-only'] and len(cmd)==5 and cmd[-1]=='--':cmd.insert(-1,commit)
        result=original(cmd,*args,**kwargs)
        if cmd==['git','ls-files','--others','--exclude-standard']:
            binary=isinstance(result,bytes);text=result.decode() if binary else result
            text=''.join(p+'\n' for p in text.splitlines() if p.startswith('distance/'+name+'/'))
            return text.encode() if binary else text
        return result
    sys.path.insert(0,str(H.with_name(name)))
    sys.argv=['unittest','discover','-s',str(H.with_name(name)/'tests'),'-p','test_*.py']
    with patch.object(subprocess,'check_output',scoped):runpy.run_module('unittest',run_name='__main__')
if __name__=='__main__':main(sys.argv[1])
