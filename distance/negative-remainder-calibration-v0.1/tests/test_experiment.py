import copy
import itertools
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import contracts as c
import runner as r
import pipeline as p
from author_cases import verify as gate

def assessment(values):return {k:{'status':v,'rationale':'fixture'} for k,v in zip(c.DIMENSIONS,values)}

class ViabilityTests(unittest.TestCase):
    def test_all_243_combinations(self):
        for values in itertools.product(c.YESNO,repeat=5):
            expected='CORE_INVALID' if 'NO' in values else 'UNCERTAIN_LOAD_BEARING' if 'UNCERTAIN' in values else 'KEEP_WITH_REDUCED_SCOPE'
            self.assertEqual(c.derive([assessment(values)],'reduced' if expected.startswith('KEEP') else 'none'),expected)
    def test_uncertainty_cannot_rescue_no(self):
        self.assertEqual(c.derive([assessment(['YES','YES','YES','NO','UNCERTAIN'])],'none'),'CORE_INVALID')
    def test_mixed_and_scope(self):
        yes=assessment(['YES']*5);unknown=assessment(['YES']*3+['UNCERTAIN','YES']);no=assessment(['YES']*3+['NO','YES'])
        self.assertEqual(c.derive([no,unknown],'uncertain'),'UNCERTAIN_LOAD_BEARING')
        self.assertEqual(c.derive([no,unknown,yes],'substantially_intact'),'KEEP_WITH_WARRANT_FLAGS')
        self.assertEqual(c.derive([yes],'reduced',{'present':True,'resolved':False}),'KEEP_WITH_REDUCED_SCOPE')
        self.assertEqual(c.derive([],'none'),'CORE_INVALID')
        with self.assertRaises(ValueError):c.derive([yes],'none')
    def test_schema_and_duplicates(self):
        for stage in r.STAGES:c.jsonschema.Draft202012Validator.check_schema(c.schema(stage))
        with self.assertRaises(ValueError):c.unique([('role','YES'),('role','NO')])

class ProductivityTests(unittest.TestCase):
    def fixture(self,effect=None):
        text='Compare X: low supports A, high supports B.';case={'mapping':{'signal':text}}
        spans=[{'source_field':'mapping.signal','exact_text':text}]
        effect=effect or {}
        yes='changed' in effect.values();uncertain='uncertain' in effect.values()
        status='YES' if yes else 'UNCERTAIN' if uncertain else 'NO'
        role='INQUIRY_CONSTRAINT' if any(effect.get(k)=='changed' for k in c.EFFECTS[3:]) else 'TARGET_CONSTRAINT' if yes else 'UNCERTAIN' if uncertain else 'INSUFFICIENCY_ONLY'
        row={'remainder_id':'R1','negative_inference':True,'productive':{'status':status,'rationale':'fixture'}}
        a={'remainder_id':'R1','role':role,'productive':status,'rationale':'fixture',
           'counterfactual_effect':{k:effect.get(k,'unchanged') for k in c.EFFECTS},
           'inquiry_specificity':{'unresolved_contrast':'A/B','concrete_operation':'Compare X',
             'differential_outcome_relation':'low/high','all_present_in_surviving_mapping':True,'source_spans':spans}}
        return {'negative_remainder_assessment':{'candidates':[a]}},[row],case,[]
    def test_every_effect_and_uncertainty(self):
        for k in c.EFFECTS:c.validate_negative(*self.fixture({k:'changed'}))
        c.validate_negative(*self.fixture());c.validate_negative(*self.fixture({'next_inquiry':'uncertain'}))
    def test_missing_inquiry_components(self):
        for key in ['unresolved_contrast','concrete_operation','differential_outcome_relation','source_spans','all_present_in_surviving_mapping']:
            args=self.fixture({'next_inquiry':'changed'});q=args[0]['negative_remainder_assessment']['candidates'][0]['inquiry_specificity'];q[key]=False if key=='all_present_in_surviving_mapping' else [] if key=='source_spans' else None
            with self.assertRaises(ValueError):c.validate_negative(*args)
    def test_no_keyword_or_jargon_rule(self):
        args=self.fixture({'bounds':'changed'});args[0]['negative_remainder_assessment']['candidates'][0]['rationale']='Insufficient for uniqueness but excludes two offsets.'
        c.validate_negative(*args)
        args=self.fixture();args[0]['negative_remainder_assessment']['candidates'][0]['rationale']='ddmin complement-vector jargon alone.';c.validate_negative(*args)
    def test_disagreement_and_missing_assessment(self):
        args=self.fixture();args[0]['negative_remainder_assessment']['candidates'][0]['productive']='YES'
        with self.assertRaises(ValueError):c.validate_negative(*args)
        args=self.fixture();args[0]['negative_remainder_assessment']['candidates']=[]
        with self.assertRaises(ValueError):c.validate_negative(*args)
    def test_deleted_or_invented_provenance(self):
        args=self.fixture({'next_inquiry':'changed'});args[-1].append({'source_field':'mapping.signal','span_start':0,'span_end':10})
        with self.assertRaises(ValueError):c.validate_negative(*args)
        args=self.fixture({'next_inquiry':'changed'});args[0]['negative_remainder_assessment']['candidates'][0]['inquiry_specificity']['source_spans'][0]['exact_text']='Invented'
        with self.assertRaises(ValueError):c.validate_negative(*args)

class CorpusTests(unittest.TestCase):
    def test_gate_and_complete_inventory(self):
        self.assertEqual(gate(),{'passed':True,'cases':15});self.assertEqual(p.verify()['claims'],40)
    def test_packets_no_hidden_content(self):
        for atom in r.claims():
            packet=r.packet('claim-warrant',atom['claim_id']).read_text()
            self.assertEqual(packet,r.reconstructed_claim_packet(atom))
            for forbidden in ['intended_role','is_control','hidden-design','supported_by_operator_audit','TARGET_CONSTRAINT']:
                self.assertNotIn(forbidden,packet)
    def test_simultaneous_exact_deletion_and_overlap(self):
        mapping={'signal':'alpha beta gamma'}
        atoms=[{'claim_id':'a','source_field':'mapping.signal','span_start':0,'span_end':5,'exact_claim_span':'alpha'},
               {'claim_id':'b','source_field':'mapping.signal','span_start':11,'span_end':16,'exact_claim_span':'gamma'}]
        self.assertEqual(r.delete_claims(mapping,atoms),{'signal':'[DELETED a] beta [DELETED b]'})
        self.assertEqual(r.delete_claims(mapping,[]),mapping)
        with self.assertRaises(ValueError):r.delete_claims(mapping,[atoms[0],atoms[0]])
    def test_provider_isolation_and_no_tools(self):
        cmd=r.command('/tmp/fixture',Path('/tmp/result'),'artifact')
        for token in ['--ephemeral','--ignore-user-config','--ignore-rules','gpt-6-astra','model_reasoning_effort="high"']:self.assertIn(token,cmd)
        self.assertEqual(r.cfg()['harness_retries'],0);self.assertEqual(r.cfg()['max_concurrent_processes'],1)
        with self.assertRaises(ValueError):r.audit_events([{'type':'thread.started','thread_id':'x'},{'type':'turn.completed'},{'type':'item.completed','item':{'type':'command_execution'}}])

if __name__=='__main__':unittest.main()
