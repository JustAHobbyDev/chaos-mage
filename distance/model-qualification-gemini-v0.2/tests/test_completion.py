import importlib.util
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gemini_complete_contracts',HERE/'review/contracts.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
r=c.r


@unittest.skipUnless((HERE/'results-freeze.json').exists(),'Complete results not yet frozen')
class CompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=r.complete_results();cls.frozen=r.read(HERE/'results-freeze.json')
    def test_fourteen_unique_requests_sequential(self):
        pre=r.read(HERE/'preflight/freeze.json');records=pre['entries']+self.frozen['runs']
        self.assertEqual(len(records),14)
        for key in ('session_id','process_id','working_directory'):
            self.assertEqual(len({x['reservation'][key] for x in records}),14)
        previous=None
        for v in records:
            start=datetime.fromisoformat(v['reservation']['at']);end=datetime.fromisoformat(v['validation']['at'])
            self.assertGreater(end,start)
            if previous:self.assertGreaterEqual(start,previous)
            previous=end
    def test_preflight_then_primary_commit_binding(self):
        precommit=r.checkpoint(HERE/'preflight/freeze.json')
        for v in self.frozen['runs']:self.assertEqual(v['reservation']['input_commit'],precommit)
        self.assertEqual(len(self.frozen['runs']),12)
    def test_serialized_inputs_schemas_high_standard(self):
        for v in self.frozen['runs']:
            d=HERE/'judgments'/v['case_id'];body=r.read(d/'request.json')
            self.assertEqual(body,r.gemini.request_body(r.packet(v['case_id']).decode(),r.read(r.wire(v['stage'])),r.config()['providers']['gemini']))
            self.assertEqual(body['serviceTier'],'standard')
            self.assertEqual(body['generationConfig']['thinkingConfig'],{'thinkingLevel':'high'})
            self.assertEqual(set(body),{'contents','generationConfig','serviceTier'})
    def test_no_response_repair(self):
        for v in self.frozen['runs']:
            d=HERE/'judgments'/v['case_id'];raw=r.read(d/'http-body.json')
            text,meta=r.gemini.parse_response(raw,v['reservation']['session_id'])
            self.assertEqual(text.encode(),(d/'response.json').read_bytes())
            self.assertEqual(meta,v['validation']['metadata'])
            self.assertEqual(raw['usageMetadata']['serviceTier'],'standard')
    def test_costs_reconstruct_and_ceiling(self):
        total=Decimal(0)
        for base in ('preflight','judgments'):
            for p in (HERE/base).glob('*/cost.json'):
                raw=r.read(p.parent/'http-body.json');cost=r.cost.account(raw['usageMetadata'],r.pricing())
                saved=r.read(p)
                for k,v in cost.items():self.assertEqual(saved[k],v)
                total+=Decimal(saved['estimated_usd'])
        self.assertEqual(total,r.cumulative());self.assertLessEqual(total,Decimal('2'))
    def test_independent_preliminary_review(self):
        p=HERE/'review/preliminary.json'
        if not p.exists():self.skipTest('Independent review pending')
        v=r.read(p);self.assertTrue(c.check_reviews(v))
        self.assertEqual(v['results_freeze_commit'],r.checkpoint(HERE/'results-freeze.json'))
        for row in v['cases']:
            cid=row['qualification_id'];self.assertEqual(row['gemini']['status'],r.status(self.data[cid],r.case(cid)['stage']))
    def test_final_review_categories_and_history(self):
        p=HERE/'review/case-reviews.json'
        if not p.exists():self.skipTest('Contextual review pending')
        v=r.read(p);self.assertTrue(c.check_reviews(v,True));hist=r.historical()
        for row in v['cases']:
            cid=row['qualification_id'];stage=r.case(cid)['stage']
            for model in ('astra','fable','muse'):self.assertEqual(row['historical_context'][model+'_status'],r.status(hist[cid][model],stage))
    def test_no_unauthorized_models_or_f(self):
        self.assertEqual(set(r.config()['providers']),{'gemini'})
        for v in self.frozen['runs']:
            self.assertEqual(v['provider'],'gemini');self.assertEqual(v['reservation']['harness_retries'],0)
    def test_historical_artifacts_unchanged(self):r.verify_inventory(r.read(HERE/'preservation.json')['files'])
    def test_allowed_review_outcomes(self):
        self.assertEqual(set(r.OUTCOMES),{'qualified','not_qualified','qualification_inconclusive'})
        self.assertEqual(set(r.CATEGORIES),{'none','ontology_specification_ambiguity','legitimate_reasoning_variation','model_failure'})


if __name__=='__main__':unittest.main()
