import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import admission as a
class AblationTests(unittest.TestCase):
 def inputs(self):
  claims={'packet_id':'M','claims':[{'claim_id':'C1','proposition':'bad operation'},{'claim_id':'C2','proposition':'dependent use'},{'claim_id':'C3','proposition':'independent survivor'}]}
  obs=[{'claim_id':x,'obligation_id':x+'-B-1','contract':'OPERATION_LICENSE','subject':x} for x in ['C1','C3']]
  inv={'obligations':obs,'references':[{'claim_id':'C2','resolution':'CLAIM_REF','referenced_claim_id':'C1'}]}
  js=[{**o,'verdict':'VIOLATED' if o['claim_id']=='C1' else 'CONDITIONAL'} for o in obs]
  return claims,inv,js
 def test_local_and_dependency_deletion_preserves_conditional(self):
  claims,inv,js=self.inputs();result=a.ablate_objects(claims,inv,js)
  self.assertEqual(result['deleted_claim_ids'],['C1','C2']);self.assertEqual(result['surviving_claims'],[claims['claims'][2]])
 def test_missing_required_judgment_blocks(self):
  claims,inv,js=self.inputs()
  with self.assertRaises(ValueError):a.ablate_objects(claims,inv,js[:-1])
 def test_fidelity_failure_never_deletes_supplied_fact(self):
  claims,inv,js=self.inputs();inv['obligations'][0]['contract']='SOURCE_FIDELITY';js[0]['contract']='SOURCE_FIDELITY'
  with self.assertRaisesRegex(ValueError,'fidelity'):a.ablate_objects(claims,inv,js)
 def test_uncertain_retained(self):
  claims,inv,js=self.inputs();js[0]['verdict']='UNCERTAIN'
  self.assertEqual(a.ablate_objects(claims,inv,js)['deleted_claim_ids'],[])
 def test_grounding_exemption_is_not_model_satisfied(self):
  claims={'packet_id':'M','claims':[{'claim_id':'C1','proposition':'supplied context'}]}
  value=a.ablate_objects(claims,{'obligations':[],'references':[{'claim_id':'C1','resolution':'GROUNDING_REF'}]},[])
  self.assertEqual(value['lineage'][0]['verdict'],'GROUNDING_REF')
 def test_evaluation_identity_and_source_membership(self):
  import runner as r
  packet={'packet_id':'M','allowed_source_ids':['T001'],'obligation':{'claim_id':'C1','obligation_id':'C1-B-1','contract':'OPERATION_LICENSE','subject':'Frozen subject'}}
  value={**packet['obligation'],'packet_id':'M','verdict':'SATISFIED','evidence_used':[{'source_id':'T001'}],'unresolved_conditions':[]}
  a.validate(r,'evaluation',value,packet)
  value['subject']='Changed subject'
  with self.assertRaisesRegex(ValueError,'Frozen obligation'):a.validate(r,'evaluation',value,packet)
  value['subject']='Frozen subject';value['evidence_used']=[{'source_id':'P999'}]
  with self.assertRaisesRegex(ValueError,'RESPONSE_SOURCE_UNKNOWN'):a.validate(r,'evaluation',value,packet)
  value['evidence_used']=[];value['verdict']='CONDITIONAL'
  with self.assertRaisesRegex(ValueError,'Conditional without'):a.validate(r,'evaluation',value,packet)
