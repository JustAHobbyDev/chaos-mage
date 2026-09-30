#!/usr/bin/env python3
"""Consume only the authorized helper secret; pass it through environment."""
import argparse
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('preflight', 'run', 'scan'))
    args = parser.parse_args()
    result = subprocess.run(['bws-4-agents', 'get', 'GEMINI_API_KEY'], capture_output=True, text=True)
    if result.returncode:
        raise SystemExit('Gemini credential helper failed; output suppressed')
    path = Path(result.stdout.strip())
    if not path.is_absolute() or not path.is_file():
        raise SystemExit('Credential helper did not return a file')
    try:
        key = path.read_text().strip()
    finally:
        path.unlink()
    if not key:
        raise SystemExit('Empty Gemini credential')
    env = dict(os.environ, GEMINI_API_KEY=key)
    runner = Path(__file__).resolve().parents[2] / 'runner.py'
    raise SystemExit(subprocess.run([sys.executable, '-B', str(runner), args.action], env=env).returncode)


if __name__ == '__main__':
    main()
