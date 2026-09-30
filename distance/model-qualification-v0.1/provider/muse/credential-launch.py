#!/usr/bin/env python3
"""Authorized single-secret loading; runner sees an environment credential only."""
import argparse
from pathlib import Path
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('catalog', 'preflight', 'run'))
    args = parser.parse_args()
    result = subprocess.run(['bws-4-agents', 'get', 'META_API_KEY'], capture_output=True, text=True)
    if result.returncode:
        raise SystemExit('Muse credential helper failed; secret output suppressed')
    path = Path(result.stdout.strip())
    if not path.is_absolute() or not path.is_file():
        raise SystemExit('Credential helper did not return a file')
    try:
        key = path.read_text().strip()
    finally:
        path.unlink()
    if not key:
        raise SystemExit('Empty Muse credential')
    env = dict(os.environ, META_API_KEY=key)
    runner = Path(__file__).resolve().parents[2] / 'runner.py'
    raise SystemExit(subprocess.run([sys.executable, '-B', str(runner), args.action], env=env).returncode)


if __name__ == '__main__': main()
