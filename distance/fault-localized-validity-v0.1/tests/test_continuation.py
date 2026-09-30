import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import continuation as k
import contracts as c
class RecoveryTests(unittest.TestCase):
 def test_actual_response_schema_and_exact_blocks(self):
  d=k.RT/'runs/claim-warrant/C-add735401d4d';value=c.read(d/'response.json')
  c.jsonschema.Draft202012Validator(c.schema('claim-warrant')).validate(value)
  proof=k.validate(value,'claim-warrant',d.name)
  self.assertEqual(len(proof['spans']),2);self.assertEqual(proof['modified_source_words'],0)
  self.assertEqual(c.read(d/'validation.json')['status'],'failed')
 def test_nonexact_words_do_not_recover(self):
  v=c.read(k.RT/'runs/claim-warrant/C-add735401d4d/response.json');v['signal_basis']=v['signal_basis'].replace('matrix','repaired matrix',1)
  with self.assertRaises(ValueError):k.validate(v,'claim-warrant',v['claim_id'])
 def test_fragment_or_reordered_quotes_rejected(self):
  candidate=k.r.candidate('E006');signal=candidate['mapping']['signal'];parts=signal.split('\n\n')
  for quote in [parts[-1]+'\n\n'+parts[0],parts[0][5:]+'\n\n'+parts[-1]]:
   with self.assertRaises(ValueError):k.quote_proof(quote,candidate)
 def test_classifier_and_schema_failures_never_recover(self):
  v=c.read(k.RT/'runs/claim-warrant/C-add735401d4d/response.json')
  for mutation in [{'status':'invented'},{'claim_id':'wrong'},{'status':'CONDITIONAL_WARRANT','stated_empirical_relation':None},{'status':'UNCERTAIN','uncertainty':[]}]:
   with self.assertRaises(Exception):k.validate({**v,**mutation},'claim-warrant','C-add735401d4d')
 def test_unlaunched_and_other_failed_responses_not_reclassified(self):
  with self.assertRaises(FileNotFoundError):k.effective_validation('claim-warrant','not-launched')
if __name__=='__main__':unittest.main()
