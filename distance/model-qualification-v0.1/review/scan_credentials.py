#!/usr/bin/env python3
"""Scan publication bytes for the authorized Muse credential; never print its value."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parent.parent


def main():
    result=subprocess.run(['bws-4-agents','get','META_API_KEY'],capture_output=True,text=True)
    if result.returncode:raise SystemExit('Credential helper failed; diagnostics suppressed')
    path=Path(result.stdout.strip())
    if not path.is_absolute() or not path.is_file():raise SystemExit('Credential path unavailable')
    try:key=path.read_bytes().strip()
    finally:path.unlink()
    if not key:raise SystemExit('Empty credential')
    paths=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    paths += [ROOT/'docs/MODEL-AGNOSTICISM.md',ROOT/'docs/MODEL-POLICY.md',
              ROOT/'docs/PROBLEM_FRAMES-model-qualification-v0.1.md',ROOT/'distance/review/model-qualification-v0.1.md']
    files={}
    for p in paths:
        raw=p.read_bytes()
        if key in raw:raise SystemExit('Credential scan failed; publication must stop')
        files[str(p.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest()
    record={'at':datetime.now(timezone.utc).isoformat(),'credential_source':'authorized bws-4-agents fetch of META_API_KEY',
            'secret_value_recorded':False,'matches':0,'files':files,'provider_calls':0}
    with (HERE/'review/credential-scan.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
    print(json.dumps({'scanned_files':len(files),'credential_matches':0,'provider_calls':0}))


if __name__=='__main__':main()
