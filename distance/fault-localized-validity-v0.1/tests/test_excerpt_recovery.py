import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import continuation_v2 as v
class ExcerptTests(unittest.TestCase):
 def test_actual_source_heading_and_bullet(self):
  x=v.c.read(v.RT/'runs/claim-warrant/C-6e35cd133b10/response.json')
  with v.context():proof=v.k.validate(x,'claim-warrant',x['claim_id'])
  self.assertEqual(len(proof['spans']),2);self.assertEqual(proof['modified_source_words'],0)
 def test_altered_reordered_or_inserted_words_rejected(self):
  x=v.c.read(v.RT/'runs/claim-warrant/C-6e35cd133b10/response.json');text=x['signal_basis'];candidate=v.r.candidate('E006')
  for bad in [text.replace('less expected','certainly excluded'), '\n'.join(reversed(text.splitlines())),text+'\nThis proves corruption.']:
   with self.assertRaises(ValueError):v.quote_proof(bad,candidate)
 def test_previous_proof_is_identical(self):
  x=v.c.read(v.RT/'runs/claim-warrant/C-add735401d4d/response.json')
  self.assertEqual(v.BASE_PROOF(x['signal_basis'],v.r.candidate('E006')),v.quote_proof(x['signal_basis'],v.r.candidate('E006')))
if __name__=='__main__':unittest.main()
