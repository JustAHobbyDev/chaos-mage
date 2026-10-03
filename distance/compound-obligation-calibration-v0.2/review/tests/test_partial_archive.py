from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import freeze_stage
import runner


class PartialArchiveTests(unittest.TestCase):
    def test_reuse_identical_and_preserve_conflicting_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            put = freeze_stage.archive_writer(runner.raw, root / 'raw')
            p = root / 'raw' / 'case' / 'response.json'
            put(p, b'original')
            put(p, b'original')
            with self.assertRaisesRegex(ValueError, 'Archived evidence differs'):
                put(p, b'changed')
            self.assertEqual(p.read_bytes(), b'original')

    def test_other_artifacts_remain_exclusive_create(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            put = freeze_stage.archive_writer(runner.raw, root / 'raw')
            p = root / 'classification-freeze.json'
            put(p, b'original')
            with self.assertRaises(FileExistsError):
                put(p, b'original')


if __name__ == '__main__':
    unittest.main()
