import copy
from decimal import Decimal
import importlib.util
import io
import json
import os
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('gemini_test_runner', HERE / 'runner.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


class QualificationTests(unittest.TestCase):
    def cfg(self): return r.config()['providers']['gemini']
    def response(self):
        return {'modelVersion': r.gemini.MODEL, 'responseId': 'synthetic',
            'candidates': [{'finishReason': 'STOP', 'content': {'parts': [{'text': '{}'}]}}],
            'usageMetadata': {'promptTokenCount': 100, 'candidatesTokenCount': 20,
                             'thoughtsTokenCount': 30, 'totalTokenCount': 150, 'serviceTier': 'standard'}}

    def test_start_provenance_preservation_contract_and_exact_cases(self):
        self.assertEqual(r.verify_inputs()['cases'], 12)
        self.assertEqual(r.config()['starting_sha'], 'cee19ee0c4c110df65de7c4380f0c271b298f30a')
        self.assertEqual({s: len([c for c in r.cases() if c['stage'] == s]) for s in r.IDS}, {'validity': 6, 'anti-collapse': 6})
        for c in r.cases(): self.assertTrue(r.raw_identity(c))

    def test_packet_masking(self):
        for c in r.cases():
            packet = r.packet(c['qualification_id']).decode()
            for banned in ('Muse', 'Fable', 'Astra', 'Gemini', 'historical_context', 'operator_rationale', 'coverage_intent'):
                self.assertNotIn(banned.lower(), packet.lower())

    def test_exact_model_high_no_fallback(self):
        for k, v in [('requested_model', 'gemini-flash'), ('endpoint', 'https://example.com'),
                     ('thinking_level', 'LOW'), ('max_output_tokens', 8192), ('temperature', 0)]:
            with self.assertRaises(ValueError): r.gemini.request_body('x', {}, {**self.cfg(), k: v})
        for model in (None, 'gemini-2.5-pro', 'gemini-3.1-pro-preview-customtools'):
            response = self.response(); response['modelVersion'] = model
            with self.assertRaises(ValueError): r.gemini.parse_response(response, 's')
        for provider in ('muse', 'astra', 'fable'):
            with self.assertRaises(ValueError): r.packet('E003', provider)

    def test_actual_v01_artificial_usage_now_accounts(self):
        usage = r.read(r.ROOT / 'distance/model-qualification-gemini-v0.1/preflight/validity/http-body.json')['usageMetadata']
        self.assertEqual(r.cost.account(usage, r.pricing())['estimated_usd'], '0.009476')

    def test_tier_casing_regression(self):
        for tier in (None, 'standard'):
            usage = self.response()['usageMetadata']; usage['serviceTier'] = tier
            self.assertEqual(r.cost.account(usage, r.pricing())['total_tokens'], 150)
        for tier in ('STANDARD', 'Standard', 'priority', 'flex', 'unknown'):
            usage = self.response()['usageMetadata']; usage['serviceTier'] = tier
            with self.assertRaises(ValueError): r.cost.account(usage, r.pricing())
            with self.assertRaises(ValueError): r.gemini.request_body('x', {}, {**self.cfg(), 'service_tier':tier})

    def test_stateless_serialization(self):
        body = r.gemini.request_body('exact', {}, self.cfg())
        self.assertEqual(body['contents'], [{'role': 'user', 'parts': [{'text': 'exact'}]}])
        self.assertEqual(set(body), {'serviceTier', 'contents', 'generationConfig'})
        self.assertEqual(body['serviceTier'], 'standard')
        cfg = body['generationConfig']
        self.assertEqual(cfg['thinkingConfig'], {'thinkingLevel': 'high'})
        self.assertEqual(cfg['maxOutputTokens'], 32768)
        self.assertEqual(set(cfg), {'thinkingConfig','maxOutputTokens','temperature','responseMimeType','responseJsonSchema'})

    def test_projection_canonical_and_cross_field_validation(self):
        for stage in r.IDS:
            self.assertEqual(r.read(r.wire(stage)), r.projection(r.read(r.canonical(stage))))
            r.validate(r.fixture(stage), stage)
            for bad in ({**r.fixture(stage), 'extra': 1}, {**r.fixture(stage), 'case_id': ''}):
                with self.assertRaises(Exception): r.validate(bad, stage)
        bad = r.fixture('validity'); bad['validity']['final_status'] = 'Invalid'
        with self.assertRaises(Exception): r.validate(bad, 'validity')
        bad = r.fixture('anti-collapse'); bad['anti_collapse']['status'] = 'CLEAR_COLLAPSE'; bad['anti_collapse']['materiality']['status'] = 'material'
        with self.assertRaises(Exception): r.validate(bad, 'anti-collapse')

    def test_random_order_and_limits(self):
        cfg = r.read(HERE/'execution-order.json'); rng = random.Random(cfg['seed'])
        groups = [[c for c in r.cases() if c['stage'] == s] for s in r.IDS]
        for g in groups: rng.shuffle(g)
        if rng.randrange(2): groups.reverse()
        self.assertEqual([c['qualification_id'] for pair in zip(*groups) for c in pair], [v['case_id'] for v in r.order()])
        self.assertEqual(r.config()['preflight_budget'], {'gemini': 2})
        self.assertEqual(r.config()['primary_budget'], {'gemini': 12})

    def test_exclusive_reservations_and_sticky_stop(self):
        with tempfile.TemporaryDirectory() as td, patch.object(r, 'RUNTIME', Path(td)):
            p = Path(td)/'once.json'; r.write(p,{})
            with self.assertRaises(FileExistsError): r.write(p,{})
            r.stop('test', 'failure'); before = (Path(td)/'STOP.json').read_bytes(); r.stop('another', 'failure')
            self.assertEqual(before, (Path(td)/'STOP.json').read_bytes())
            with self.assertRaises(ValueError): r.guard()

    def test_usage_thinking_no_double_count(self):
        v = r.cost.account(self.response()['usageMetadata'], r.pricing())
        self.assertEqual(v['billable_output_tokens'], 50)
        self.assertEqual(Decimal(v['estimated_usd']), Decimal('0.0008'))
        self.assertEqual(r.cost.estimate(200001, 100, r.pricing()), Decimal('0.801804'))
        for usage in (None, {}, {'promptTokenCount': -1}):
            with self.assertRaises(ValueError): r.cost.account(usage, r.pricing())
        bad = self.response()['usageMetadata']; bad['totalTokenCount'] = 120
        with self.assertRaises(ValueError): r.cost.account(bad, r.pricing())

    def test_cost_ceiling_prevents_network(self):
        with tempfile.TemporaryDirectory(dir=r.ROOT/'.runtime') as td:
            d = Path(td)/'attempt'
            with patch.object(r,'guard'), patch.object(r,'stop'), patch.object(r,'cumulative',return_value=Decimal('1.99')), patch.object(r.gemini,'request') as request:
                result = r.execute('validity', d, b'artificial')
            request.assert_not_called()
            self.assertEqual(result['status'], 'failed')
            self.assertEqual(result['failure_kind'], 'cost_or_usage_failure')
            self.assertFalse((d/'request-sent.json').exists())

    def test_unknown_sent_cost_retains_reservation(self):
        with tempfile.TemporaryDirectory() as td, patch.object(r,'HERE',Path(td)):
            d = Path(td)/'preflight/validity'; d.mkdir(parents=True)
            r.write(d/'reservation.json', {'cost_reservation': {'reserved_usd':'0.5'}})
            r.write(d/'request-sent.json', {})
            self.assertEqual(r.cumulative(), Decimal('0.5'))
            r.write(d/'cost.json', {'estimated_usd':'0.1'})
            self.assertEqual(r.cumulative(), Decimal('0.1'))

    def test_http_failure_once_secret_header_only(self):
        exc = urllib.error.HTTPError('https://example.com',429,'quota',{},io.BytesIO(b'{"error":"quota"}'))
        saved = {}
        with patch.dict(os.environ, {'GEMINI_API_KEY':'synthetic-not-a-key'}), patch.object(r.gemini.urllib.request,'build_opener') as opener:
            opener.return_value.open.side_effect = exc
            with self.assertRaises(ValueError): r.gemini.request({},1,saved.__setitem__,lambda:None)
            self.assertEqual(opener.return_value.open.call_count, 1)
            req = opener.return_value.open.call_args.args[0]
            self.assertNotIn('synthetic-not-a-key', req.full_url)
            self.assertNotIn(b'synthetic-not-a-key', req.data)
        self.assertEqual(saved['http-body.json'],b'{"error":"quota"}')

    def test_credential_reflection_and_error_sanitization(self):
        exc = urllib.error.HTTPError('https://example.com',400,'bad',{},io.BytesIO(b'synthetic-not-a-key'))
        saved = {}
        with patch.dict(os.environ, {'GEMINI_API_KEY':'synthetic-not-a-key'}), patch.object(r.gemini.urllib.request,'build_opener') as opener:
            opener.return_value.open.side_effect = exc
            with self.assertRaises(ValueError): r.gemini.request({},1,saved.__setitem__,lambda:None)
            self.assertNotIn('synthetic-not-a-key', r.safe_error(ValueError('synthetic-not-a-key')))
        self.assertNotIn(b'synthetic-not-a-key', b''.join(saved.values()))

    def test_no_tools_grounding_redirect_truncation(self):
        with self.assertRaises(ValueError): r.gemini.NoRedirect().redirect_request(None,None,302,'',{},'https://example.com')
        for k,v in [('finishReason','MAX_TOKENS'), ('groundingMetadata',{'x':1}), ('urlContextMetadata',{'x':1}), ('content',{'parts':[{'functionCall':{}}]})]:
            value = self.response(); value['candidates'][0][k] = v
            with self.assertRaises(ValueError): r.gemini.parse_response(value,'s')

    def test_freeze_and_preliminary_gate_historical_decoding(self):
        with patch.object(r,'complete_results',side_effect=ValueError('not frozen')), patch.object(r,'read') as read:
            with self.assertRaises(ValueError): r.historical()
            read.assert_not_called()
        with tempfile.TemporaryDirectory() as td, patch.object(r,'HERE',Path(td)), patch.object(r,'complete_results'):
            with self.assertRaises(ValueError): r.historical()

    def test_fresh_environment_no_comparison_models(self):
        with patch.object(r.subprocess,'run') as run, patch.dict(os.environ,{'GEMINI_API_KEY':'synthetic','META_API_KEY':'excluded','OPENAI_API_KEY':'excluded','ANTHROPIC_API_KEY':'excluded'}):
            run.return_value.returncode = 0; r.child('validity','E003')
            env = run.call_args.kwargs['env']
            self.assertIn('GEMINI_API_KEY', env)
            for key in ('META_API_KEY','OPENAI_API_KEY','ANTHROPIC_API_KEY'): self.assertNotIn(key,env)
        self.assertEqual(set(r.config()['providers']), {'gemini'})


if __name__ == '__main__': unittest.main()
