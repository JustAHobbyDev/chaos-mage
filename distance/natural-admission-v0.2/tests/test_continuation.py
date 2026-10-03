"""Offline policy acceptance; synthetic data, no model calls."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import continuation as c

class RecoveryTests(unittest.TestCase):
    def clean(self):
        return dict(request_launched=True, launch_identity_certain=True, request_match=True,
            configuration_match=True, context_intact=True, unique_attempt=True,
            response_present=False, scientific_observation_present=False, completion_event_present=False,
            substitution=False, retry_count=0, frozen_request_sha256='same', executed_request_sha256='same')
    def test_clean_no_observation(self):
        self.assertEqual(c.classify(self.clean()), 'PROVIDER_NO_OBSERVATION')
    def test_response_exists_invalid(self):
        e=self.clean(); e['response_present']=True
        self.assertEqual(c.classify(e), 'PROVIDER_OBSERVATION_FAILURE')
    def test_launch_ambiguous(self):
        e=self.clean(); e['request_launched']=None
        self.assertEqual(c.classify(e), 'PROVIDER_OBSERVATION_AMBIGUOUS')
    def test_partial_response_ambiguous(self):
        e=self.clean(); e['scientific_observation_present']=None
        self.assertEqual(c.classify(e), 'PROVIDER_OBSERVATION_AMBIGUOUS')
    def test_every_positive_required(self):
        for key in ['unique_attempt','context_intact','configuration_match','request_match','launch_identity_certain']:
            e=self.clean(); e[key]=False
            self.assertEqual(c.classify(e), 'PROVIDER_OBSERVATION_AMBIGUOUS')
    def test_no_retry(self):
        self.assertFalse(c.schedulable('A',['A','B'],{'A'},{'A':{'independent':True}}))
        self.assertFalse(c.schedulable('B',['A','B'],{'A'},{'B':{'independent':True}}, attempted=True))
    def test_independent_continuation(self):
        self.assertTrue(c.schedulable('B',['A','B'],{'A'},{'B':{'independent':True}}))
        self.assertFalse(c.schedulable('B',['A','B'],{'A'},{'B':{'independent':'uncertain'}}))
    def test_no_replacement(self):
        self.assertFalse(c.schedulable('C',['A','B'],{'A'},{'C':{'independent':True}}))
    def test_scientific_separation(self):
        d=c.disposition(self.clean())
        self.assertEqual(d['admission'],'UNMEASURED'); self.assertEqual(d['instrumentation'],'FAILURE')
        self.assertFalse(d['end_to_end_complete'])
        e=self.clean(); e['completion_event_present']=True
        with self.assertRaises(ValueError): c.disposition(e)
