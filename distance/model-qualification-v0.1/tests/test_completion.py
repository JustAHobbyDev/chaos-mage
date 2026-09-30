"""Independent evidence audit. Executes only after a complete committed freeze."""
from collections import Counter
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('qualification_completion_tests',HERE/'runner.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)


@unittest.skipUnless((HERE/'results-freeze.json').exists(),'Results not frozen yet')
class CompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=r.complete_results()
        cls.frozen=r.read(HERE/'results-freeze.json')

    def test_exactly_twelve_once_sequential_after_preflight(self):
        preflight_commit=r.checkpoint(HERE/'preflight/freeze.json')
        self.assertEqual(len(self.frozen['runs']),12)
        previous=datetime.fromisoformat(r.read(HERE/'preflight/freeze.json')['at'])
        for run in self.frozen['runs']:
            reservation=run['reservation'];finished=datetime.fromisoformat(run['validation']['at'])
            started=datetime.fromisoformat(reservation['at'])
            self.assertGreaterEqual(started,previous);self.assertGreater(finished,started)
            self.assertEqual(reservation['input_commit'],preflight_commit)
            previous=finished
        self.assertGreater(datetime.fromisoformat(self.frozen['at']),previous)

    def test_unique_processes_sessions_and_empty_contexts(self):
        records=[e['reservation'] for e in r.read(HERE/'preflight/freeze.json')['entries']]+[e['reservation'] for e in self.frozen['runs']]
        self.assertEqual(len(records),14)
        for key in ('process_id','session_id','working_directory'):
            self.assertEqual(len({v[key] for v in records}),14)
        for v in records:
            self.assertTrue(v['fresh_process']);self.assertTrue(v['working_directory_initially_empty'])
            self.assertEqual(v['provider'],'muse');self.assertEqual(v['harness_retries'],0)

    def test_exact_packet_and_wire_reach_model_without_annotations(self):
        for run in self.frozen['runs']:
            d=HERE/'judgments'/run['case_id'];body=r.read(d/'request.json')
            expected=r.muse.request_body(r.packet(run['case_id']).decode(),r.read(r.wire(run['stage'])),r.config()['providers']['muse'])
            self.assertEqual(body,expected)
            self.assertEqual((d/'prompt.txt').read_bytes(),r.packet(run['case_id']))
            self.assertEqual(run['reservation']['packet_sha256'],hashlib.sha256(r.packet(run['case_id'])).hexdigest())

    def test_response_identity_and_no_semantic_repair(self):
        for run in self.frozen['runs']:
            d=HERE/'judgments'/run['case_id'];raw=r.read(d/'http-body.json')
            text,metadata=r.muse.parse_response(raw,run['reservation']['session_id'])
            self.assertEqual(text.encode(),(d/'response.json').read_bytes())
            self.assertEqual(metadata,run['validation']['metadata'])
            self.assertEqual(r.read(d/'http-metadata.json')['status'],200)
            self.assertEqual(metadata['requested_model'],r.muse.MODEL)
            self.assertEqual(metadata['returned_model_identifiers'],[r.muse.MODEL])
            self.assertEqual(metadata['tier'],'Contributor')

    def test_frozen_result_ancestry_and_review_binding(self):
        commit=r.checkpoint(HERE/'results-freeze.json')
        self.assertEqual(r.git('merge-base',commit,'HEAD').decode().strip(),commit)
        p=HERE/'review/case-reviews.json'
        if p.exists():
            reviews=r.read(p);self.assertEqual(reviews['results_freeze_commit'],commit)
            self.assertGreater(datetime.fromisoformat(reviews['review_started_at']),datetime.fromisoformat(self.frozen['at']))
            r.check_reviews(reviews['cases'],reviews['qualification'])

    def test_independent_metrics_and_historical_description(self):
        p=HERE/'metrics.json'
        if not p.exists():self.skipTest('Metrics not created yet')
        m=r.read(p);history=r.historical()
        self.assertEqual(m['requested_judgments'],12);self.assertEqual(m['successful_judgments'],12)
        self.assertEqual(m['provider_failures'],0);self.assertEqual(m['schema_failures'],0)
        for s,ids in r.IDS.items():
            self.assertEqual(m['status_distributions'][s],dict(Counter(r.status(self.data[c],s) for c in ids)))
        rejects=sum(self.data[c]['anti_collapse']['status']=='CLEAR_COLLAPSE' for c in r.IDS['anti-collapse'])
        self.assertEqual(m['anti_collapse_gate'],{'keep':6-rejects,'reject':rejects})
        matches=Counter()
        for c in r.cases():
            cid=c['qualification_id'];s=c['stage'];same=sum(r.status(self.data[cid],s)==r.status(v,s) for v in history[cid].values())
            matches[{0:'different_from_both',1:'same_as_one',2:'same_as_both'}[same]]+=1
        self.assertEqual(m['descriptive_historical_status_comparison'],{k:matches[k] for k in ('same_as_both','same_as_one','different_from_both')})
        for word in ('accuracy','majority','consensus'):self.assertNotIn(word,p.read_text().lower())

    def test_credential_launcher_provenance_bound(self):
        v=r.read(HERE/'provider/muse/credential-provenance.json')
        self.assertEqual(r.sha(r.ROOT/v['launcher_path']),v['launcher_sha256'])
        self.assertFalse(v['secret_value_recorded']);self.assertTrue(v['temporary_helper_file_removed_before_provider_call'])


if __name__=='__main__':unittest.main()
