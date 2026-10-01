"""H.2 identity, immutable IO and historical preservation helpers."""
import hashlib
import json
import subprocess
from pathlib import Path

H = Path(__file__).resolve().parent
R = H.parent.parent
BASE = '5d22364465c8183581452cc720b21f9bd0cc38b4'
ALLOWED = ['distance/remainder-viability-calibration-v0.1/',
           'distance/review/remainder-viability-calibration-v0.1.md',
           'docs/PROBLEM_FRAMES-remainder-viability-calibration-v0.1.md']

def require(ok, message):
    if not ok:
        raise ValueError(message)

def read(path):
    return json.loads(Path(path).read_text())

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as out:
        json.dump(value, out, indent=2, ensure_ascii=False)
        out.write('\n')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=R)

def allowed(path):
    return any(path.startswith(p) if p.endswith('/') else path == p for p in ALLOWED)

def guard():
    p = read(H/'preservation.json')
    require(p['baseline'] == BASE, 'Wrong historical baseline')
    expected = git('show', '0874cb6:distance/remainder-viability-calibration-v0.1/preservation.json')
    require(expected == (H/'preservation.json').read_bytes(), 'Preservation manifest changed')
    for name, digest in {**p['files'], **p['historical_runtime']}.items():
        require(sha(R/name) == digest, 'Historical bytes changed: ' + name)
    changes = git('diff','--name-only',BASE,'--').decode().splitlines()
    changes += git('ls-files','--others','--exclude-standard').decode().splitlines()
    require(all(allowed(name) for name in changes), 'Out-of-scope changes')
    return {'tracked': len(p['files']), 'runtime': len(p['historical_runtime'])}

def span(case, field, text):
    parent = case['mapping'][field]
    start = parent.index(text)
    require(parent.count(text) == 1, 'Ambiguous citation')
    return {'source_field':'mapping.'+field, 'start':start, 'end':start+len(text), 'exact_text':text}

def verify_span(case, item):
    parent = case['mapping'][item['source_field'].split('.')[1]]
    require(parent[item['start']:item['end']] == item['exact_text'], 'Citation drift')

def viable(candidate):
    return all(candidate[k] == 'YES' for k in ['warranted','source_derived','material','target_relevant'])

def unresolved(candidate):
    values = [candidate[k] for k in ['warranted','source_derived','material','target_relevant']]
    return 'NO' not in values and 'UNCERTAIN' in values
