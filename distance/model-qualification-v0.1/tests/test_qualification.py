import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('qualification_test_runner', HERE / 'runner.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


class QualificationTests(unittest.TestCase):
    def test_exact_cases_sources_hashes_and_preservation(self):
        self.assertEqual(r.verify_inputs()['cases'], 12)
        self.assertEqual({s: len([c for c in r.cases() if c['stage'] == s]) for s in r.IDS}, {'validity': 6, 'anti-collapse': 6})

    def test_no_packet_labels_or_operator_rationale(self):
        for c in r.cases():
            raw = r.packet(c['qualification_id'])
            self.assertEqual(raw, (r.ROOT / c['input_path']).read_bytes())
            body = json.loads(raw.decode().split('\n\nCASE PACKET\n')[1])
            for key in ('historical_context', 'expected_result', 'coverage_intent', 'operator_rationale'):
                self.assertNotIn(key, body)
            if c['stage'] == 'anti-collapse':
                self.assertIn('native_baseline', body); self.assertIn('source_neutral', body)

    def test_muse_only_and_no_fallback(self):
        cfg = r.config()['providers']['muse']
        self.assertEqual(set(r.config()['providers']), {'muse'})
        for provider in ('astra', 'fable', 'other'):
            with self.assertRaises(ValueError): r.packet('E003', provider)
        for key, value in [('requested_model', 'muse-spark-1.3'), ('endpoint', 'https://example.com')]:
            bad = {**cfg, key: value}
            with self.assertRaises(ValueError): r.muse.request_body('x', {}, bad)
        for model in (None, 'muse-spark-1.3', 'claude-fable-5-1'):
            with self.assertRaises(ValueError): r.muse.parse_response({'model': model}, 's')

    def test_stateless_request(self):
        body = r.muse.request_body('isolated', {}, r.config()['providers']['muse'])
        self.assertEqual(body['messages'], [{'role': 'user', 'content': 'isolated'}])
        self.assertEqual(body['reasoning_effort'], 'high')
        for key in ('tools', 'previous_response_id', 'conversation', 'plugins', 'temperature'):
            self.assertNotIn(key, body)
        self.assertTrue(body['response_format']['json_schema']['strict'])

    def test_contributor_provenance(self):
        cfg = r.config()
        self.assertEqual(cfg['data_use']['tier'], 'Contributor')
        self.assertTrue(cfg['data_use']['training_eligible'])
        self.assertEqual(cfg['providers']['muse']['credential_source'], 'environment')
        self.assertEqual(cfg['providers']['muse']['requested_model'], 'muse-spark-1.3-contributor')

    def test_projection_preserves_fields_enums_required_nulls(self):
        for stage in r.IDS:
            self.assertEqual(r.read(r.wire(stage)), r.projection(r.read(r.canonical(stage))))
            def walk(a, b):
                if isinstance(a, dict):
                    for k in a:
                        if k not in ('$id', '$schema', 'allOf'): walk(a[k], b[k])
                elif isinstance(a, list):
                    self.assertEqual(len(a),len(b))
                    for x,y in zip(a,b):walk(x,y)
                else:self.assertEqual(a,b)
            walk(r.read(r.canonical(stage)),r.read(r.wire(stage)))

    def test_canonical_and_cross_field_validation(self):
        for stage in r.IDS:
            value = r.fixture(stage); r.validate(value, stage)
            for invalid in ({**value, 'extra': 1}, {**value, 'case_id': ''}):
                with self.assertRaises(Exception): r.validate(invalid, stage)
        bad = r.fixture('validity'); bad['validity']['final_status'] = 'Invalid'
        with self.assertRaises(Exception): r.validate(bad, 'validity')
        bad = r.fixture('anti-collapse'); bad['anti_collapse']['status'] = 'CLEAR_COLLAPSE'; bad['anti_collapse']['materiality']['status'] = 'material'
        with self.assertRaises(Exception): r.validate(bad, 'anti-collapse')

    def test_schedule_reproducible_interleaved_unique(self):
        import random
        cfg = r.read(HERE / 'execution-order.json'); rng = random.Random(cfg['seed'])
        groups = [[c for c in r.cases() if c['stage'] == s] for s in r.IDS]
        for g in groups:rng.shuffle(g)
        if rng.randrange(2):groups.reverse()
        ids=[c['qualification_id'] for pair in zip(*groups) for c in pair]
        self.assertEqual(ids,[x['case_id'] for x in r.order()])
        self.assertEqual(len(set(ids)),12)
        self.assertTrue(all(a['stage']!=b['stage'] for a,b in zip(r.order(),r.order()[1:])))

    def test_reservation_exclusive_stop_sticky(self):
        with tempfile.TemporaryDirectory() as td, patch.object(r, 'RUNTIME', Path(td)):
            p = Path(td)/'reservation.json';r.write(p,{})
            with self.assertRaises(FileExistsError):r.write(p,{})
            r.stop('test','timeout');before=(Path(td)/'STOP.json').read_bytes();r.stop('other','error')
            self.assertEqual(before,(Path(td)/'STOP.json').read_bytes())
            with self.assertRaises(ValueError):r.guard()

    def test_http_failure_preserved_once_no_secret(self):
        exc=urllib.error.HTTPError('https://api.meta.ai/v1/chat/completions',429,'quota',{},io.BytesIO(b'{"error":"quota"}'))
        saved={}
        with patch.dict(os.environ,{'META_API_KEY':'dummy-secret'}),patch.object(r.muse.urllib.request,'build_opener') as opener:
            opener.return_value.open.side_effect=exc
            with self.assertRaises(ValueError):r.muse.request('chat/completions',{},1,saved.__setitem__)
            self.assertEqual(opener.return_value.open.call_count,1)
        self.assertEqual(saved['http-body.json'],b'{"error":"quota"}')
        self.assertNotIn(b'dummy-secret',b''.join(saved.values()))

    def test_credential_reflection_withheld(self):
        exc=urllib.error.HTTPError('https://api.meta.ai/v1/chat/completions',400,'bad',{},io.BytesIO(b'{"error":"dummy-secret"}'))
        saved={}
        with patch.dict(os.environ,{'META_API_KEY':'dummy-secret'}),patch.object(r.muse.urllib.request,'build_opener') as opener:
            opener.return_value.open.side_effect=exc
            with self.assertRaises(ValueError):r.muse.request('chat/completions',{},1,saved.__setitem__)
        self.assertNotIn(b'dummy-secret',b''.join(saved.values()))
        self.assertNotIn('http-body.json',saved)

    def test_no_redirect_or_tool_activity(self):
        with self.assertRaises(ValueError):r.muse.NoRedirect().redirect_request(None,None,302,'',{},'https://example.com')
        value={'model':r.muse.MODEL,'choices':[{'finish_reason':'stop','message':{'content':'{}','tool_calls':[{}]}}]}
        with self.assertRaises(ValueError):r.muse.parse_response(value,'s')

    def test_historical_decode_blocked_before_complete_committed_freeze(self):
        with patch.object(r,'complete_results',side_effect=ValueError('not frozen')),patch.object(r,'read') as read:
            with self.assertRaises(ValueError):r.historical()
            read.assert_not_called()
        with tempfile.TemporaryDirectory() as td,patch.object(r,'HERE',Path(td)),patch.object(r,'verify',return_value={}):
            with self.assertRaises(Exception):r.complete_results()

    def test_review_categories_and_decision_enum(self):
        rows=[{'qualification_id':c['qualification_id'],'source_case_id':c['source_case_id'],
            'muse':{'status':'fixture','key_reasoning':'fixture'},'disagreement_class':'none',
            'capability_dimensions':{k:'pass' for k in r.DIMENSIONS},'downstream_consequence':'none','rationale':'fixture'} for c in r.cases()]
        for outcome in r.OUTCOMES:r.check_reviews(rows,outcome)
        with self.assertRaises(ValueError):r.check_reviews(rows,'equivalent')
        rows[0]['disagreement_class']='majority_correct'
        with self.assertRaises(ValueError):r.check_reviews(rows,'qualified')

    def test_real_evidence_isolated_no_repeats_and_no_credentials(self):
        sessions=[]
        for base in ('preflight','judgments'):
            for p in (HERE/base).rglob('reservation.json'):
                v=r.read(p)
                if 'session_id' in v:
                    sessions.append(v['session_id']);self.assertTrue(v['fresh_process']);self.assertTrue(v['working_directory_initially_empty'])
                    self.assertEqual(v['history_messages'],0);self.assertEqual(v['tools'],[])
                    body=r.read(p.parent/'request.json');self.assertEqual(len(body['messages']),1)
                    self.assertEqual(body['model'],r.muse.MODEL)
        self.assertEqual(len(sessions),len(set(sessions)))
        self.assertLessEqual(len(list((HERE/'judgments').glob('*/reservation.json'))),12)
        key=os.environ.get('META_API_KEY')
        for p in HERE.rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts and key:self.assertNotIn(key.encode(),p.read_bytes())

    def test_actual_freeze_review_and_metrics(self):
        if (HERE/'results-freeze.json').exists():self.assertEqual(len(r.complete_results()),12)
        if (HERE/'review/case-reviews.json').exists():
            v=r.read(HERE/'review/case-reviews.json')
            if v.get('cases'):r.check_reviews(v['cases'],v['qualification'])
        if (HERE/'metrics.json').exists():
            text=(HERE/'metrics.json').read_text().lower()
            for banned in ('accuracy','majority','consensus'):self.assertNotIn(banned,text)

    def test_policy_provenance_and_historical_scope(self):
        text=(r.ROOT/'docs/MODEL-AGNOSTICISM.md').read_text()
        self.assertIn('model-agnostic above a minimum reasoning',text)
        self.assertIn('Every experiment records exact requested and returned model identifiers',text)
        self.assertIn('not model interchangeability',text)
        r.verify_inventory(r.read(HERE/'preservation.json')['files'])
        self.assertFalse((r.RUNTIME/'experiment-f').exists())


if __name__=='__main__':unittest.main()
