import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bridge_test_runner', HERE / 'runner.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


class BridgeTests(unittest.TestCase):
    def test_exact_sources_hashes_and_historical_preservation(self):
        self.assertEqual(r.verify_inputs()['cases'], 12)
        self.assertEqual({s: len([c for c in r.cases() if c['stage'] == s]) for s in r.IDS}, {'validity': 6, 'anti-collapse': 6})

    def test_packets_identical_no_operator_labels(self):
        for c in r.cases():
            raw = r.packet(c['bridge_id'], 'fable')
            self.assertEqual(raw, r.packet(c['bridge_id'], 'muse'))
            self.assertEqual(raw, (r.ROOT / c['input_path']).read_bytes())
            body = json.loads(raw.decode().split('\n\nCASE PACKET\n')[1])
            self.assertNotIn('historical_fable', body)
            self.assertNotIn('bridge_rationale', body)
            self.assertNotIn('expected_result', body)

    def test_order_complete_unique_balanced(self):
        order = r.order()
        self.assertEqual(len(order), 24)
        self.assertEqual(len({v['id'] for v in order}), 24)
        self.assertEqual({(v['case_id'], v['provider']) for v in order}, {(c['bridge_id'], p) for c in r.cases() for p in ('muse', 'fable')})
        for i in range(0, 24, 4):
            self.assertEqual({(x['provider'], x['stage']) for x in order[i:i+4]}, {(p, s) for p in ('muse', 'fable') for s in r.IDS})

    def test_projection_preserves_contract(self):
        for stage in r.IDS:
            canonical = r.read(r.canonical(stage)); wire = r.read(r.wire(stage))
            self.assertEqual(wire, r.projection(canonical))
            def walk(a, b):
                if isinstance(a, dict):
                    for k in ('properties', 'required', 'enum', 'type', 'additionalProperties'):
                        if k in a and k != 'properties': self.assertEqual(a[k], b[k])
                    for k in a:
                        if k not in ('$schema', '$id', 'allOf'): walk(a[k], b[k])
                elif isinstance(a, list):
                    for x, y in zip(a, b): walk(x, y)
            walk(canonical, wire)

    def test_canonical_validation_for_both_providers(self):
        for provider in ('muse', 'fable'):
            for stage in r.IDS:
                v = r.fixture(stage); r.validate(v, stage)
                invalid = copy.deepcopy(v); invalid['extra'] = provider
                with self.assertRaises(Exception): r.validate(invalid, stage)
                invalid = copy.deepcopy(v); invalid['case_id'] = ''
                with self.assertRaises(Exception): r.validate(invalid, stage)
        v = r.fixture('validity'); v['validity']['final_status'] = 'Invalid'
        with self.assertRaises(Exception): r.validate(v, 'validity')
        v = r.fixture('anti-collapse'); v['anti_collapse']['status'] = 'CLEAR_COLLAPSE'; v['anti_collapse']['materiality']['status'] = 'material'
        with self.assertRaises(Exception): r.validate(v, 'anti-collapse')

    def test_fallback_rejected(self):
        cfg = copy.deepcopy(r.config()['providers']['muse']); cfg['requested_model'] = 'muse-spark-1.3'
        with self.assertRaises(ValueError): r.muse.request_body('x', {}, cfg)
        cfg = copy.deepcopy(r.config()['providers']['fable']); cfg['requested_model'] = 'another-model'
        with self.assertRaises(ValueError): r.fable.command(cfg, '{}', 'session')
        with self.assertRaises(ValueError): r.muse.parse_response({'model': 'muse-spark-1.3'}, 'session')
        events = [{'type':'system','subtype':'init','session_id':'s','model':'wrong-model','tools':['StructuredOutput']}, {'type':'result','subtype':'success','session_id':'s','structured_output':{},'modelUsage':{}}]
        with self.assertRaises(ValueError): r.legacy.audit_events(events, 'B', r.fable.MODEL, 's')

    def test_no_tools_history_or_third_judge(self):
        body = r.muse.request_body('packet', {}, r.config()['providers']['muse'])
        self.assertEqual(body['messages'], [{'role': 'user', 'content': 'packet'}])
        self.assertNotIn('tools', body)
        cmd = r.fable.command(r.config()['providers']['fable'], '{}', 's')
        self.assertIn('--safe-mode', cmd)
        self.assertEqual(cmd[cmd.index('--tools') + 1], '')
        self.assertIn('--no-session-persistence', cmd)
        with self.assertRaises(ValueError): r.packet('E003', 'astra')
        with patch.dict(r.os.environ, {'META_API_KEY':'dummy-secret', 'ANTHROPIC_MODEL':'wrong'}):
            env = r.fable.environment()
            self.assertNotIn('META_API_KEY', env); self.assertNotIn('ANTHROPIC_MODEL', env)

    def test_exclusive_reservation_and_stop(self):
        with tempfile.TemporaryDirectory() as td, patch.object(r, 'RUNTIME', Path(td)):
            p = Path(td) / 'reservation.json'; r.write(p, {})
            with self.assertRaises(FileExistsError): r.write(p, {})
            r.stop('quota', 'HTTP 429')
            before = (Path(td) / 'STOP.json').read_bytes()
            r.stop('another', 'later')
            self.assertEqual(before, (Path(td) / 'STOP.json').read_bytes())
            with self.assertRaises(ValueError): r.guard()

    def test_failed_http_is_preserved_without_retry(self):
        import io
        import urllib.error
        error = urllib.error.HTTPError('https://api.meta.ai/v1/chat/completions', 429, 'quota', {}, io.BytesIO(b'{"error":"quota"}'))
        saved = {}
        with patch.dict(r.os.environ, {'META_API_KEY':'dummy-secret'}), patch.object(r.muse.urllib.request, 'build_opener') as opener:
            opener.return_value.open.side_effect = error
            with self.assertRaises(ValueError): r.muse.request('chat/completions', {}, 1, saved.__setitem__)
            self.assertEqual(opener.return_value.open.call_count, 1)
        self.assertEqual(saved['http-body.json'], b'{"error":"quota"}')
        self.assertNotIn(b'dummy-secret', b''.join(saved.values()))

    def test_results_gate_blocks_both_comparisons(self):
        with tempfile.TemporaryDirectory() as td, patch.object(r, 'HERE', Path(td)), patch.object(r, 'verify', return_value={}):
            with self.assertRaises(Exception): r.complete_results()
        self.assertIn('data = complete_results()', (HERE / 'runner.py').read_text())

    def test_four_review_categories_only(self):
        rows = [{'bridge_id': c['bridge_id'], 'historical_vs_fresh_fable': {'category':'stable','rationale':'fixture'}, 'fresh_fable_vs_muse':{'category':'stable','rationale':'fixture'}, 'downstream_transition_effect':'none'} for c in r.cases()]
        r.check_reviews(rows)
        rows[0]['fresh_fable_vs_muse']['category'] = 'correct'
        with self.assertRaises(ValueError): r.check_reviews(rows)

    def test_unique_sessions_no_repeats_in_actual_evidence(self):
        sessions = [r.read(p)['session_id'] for p in r.RUNTIME.rglob('reservation.json') if 'session_id' in r.read(p)]
        self.assertEqual(len(sessions), len(set(sessions)))
        for provider in ('fable', 'muse'):
            calls = list((r.RUNTIME / 'judgments').glob(provider + '-*/reservation.json'))
            self.assertLessEqual(len(calls), 12)

    def test_no_accuracy_or_out_of_scope_execution(self):
        if (HERE / 'metrics.json').exists():
            self.assertNotIn('accuracy', (HERE / 'metrics.json').read_text().lower())
        self.assertEqual(set(r.config()['providers']), {'fable', 'muse'})
        self.assertFalse((r.RUNTIME / 'experiment-f').exists())

    def test_actual_freeze_and_post_freeze_review(self):
        if (HERE / 'results-freeze.json').exists():
            data = r.complete_results(); self.assertEqual(len(data), 24)
        if (HERE / 'review/case-reviews.json').exists():
            rows = r.read(HERE / 'review/case-reviews.json'); r.check_reviews(rows['cases'])
            self.assertEqual(rows['results_freeze_commit'], r.checkpoint(HERE / 'results-freeze.json'))


if __name__ == '__main__': unittest.main()
