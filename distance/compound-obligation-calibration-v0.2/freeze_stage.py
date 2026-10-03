#!/usr/bin/env python3
"""Offline whole-stage freeze after partial archives; never launches a provider.

The frozen runner uses exclusive-create archival. A completed partial batch may
already have archived identical raw bytes. Reuse only exact matches within that
stage's raw archive; retain the frozen runner's validation and freeze logic.
"""
import argparse
from pathlib import Path
import runner


def archive_writer(original, archive_root):
    def write(path, data):
        path = Path(path)
        if path.exists() and path.resolve().is_relative_to(archive_root.resolve()):
            runner.c.require(path.is_file() and path.read_bytes() == data,
                             'Archived evidence differs; preserve and investigate: ' + str(path))
            return
        original(path, data)
    return write


def freeze(stage):
    runner.c.require(not runner.frozen_path(stage).exists(), 'Stage already frozen')
    original = runner.raw
    runner.raw = archive_writer(original, runner.H / 'raw' / stage)
    try:
        runner.freeze(stage)
    finally:
        runner.raw = original


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=runner.STAGES)
    freeze(parser.parse_args().stage)
