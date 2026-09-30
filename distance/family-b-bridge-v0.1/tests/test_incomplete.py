import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bridge_incomplete_verifier_test', HERE / 'verify_incomplete.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)


class IncompleteBridgeTests(unittest.TestCase):
    def test_public_failure_evidence(self):
        self.assertEqual(v.verify()['status'], 'inconclusive')

    def test_private_failure_evidence(self):
        self.assertEqual(v.verify(True)['primary_calls'], {'fable': 0, 'muse': 0})

    def test_stop_blocks_collection_and_preflight(self):
        for action in (v.r.guard, v.r.preflight, v.r.run_all):
            with self.assertRaisesRegex(ValueError, 'Scheduling stopped'): action()

    def test_no_comparison_of_partial_evidence(self):
        # Exercise the absent complete-freeze gate without noisy git diagnostics.
        original = v.r.git
        def git(*args):
            if args == ('show', 'HEAD:distance/family-b-bridge-v0.1/results-freeze.json'):
                raise ValueError('No complete freeze')
            return original(*args)
        with patch.object(v.r, 'git', side_effect=git):
            with self.assertRaisesRegex(ValueError, 'No complete freeze'): v.r.complete_results()


if __name__ == '__main__': unittest.main()
