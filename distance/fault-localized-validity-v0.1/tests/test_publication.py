import copy,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import publication as p
class PublicationTests(unittest.TestCase):
 def test_complete_observations_and_freeze_chronology(self):
  result=p.verify()
  self.assertEqual(result['provider_calls'],53);self.assertEqual(result['unique_sessions'],53)
  self.assertEqual(result['recovered_response_representations'],2)
  self.assertTrue(result['no_launch_during_pause'])
 def test_recovered_terminals_do_not_auto_resume(self):
  with p.v2.context(),patch.object(p.k,'state',return_value='TERMINATED_MEASUREMENT'),patch.object(p.r,'execute') as execute:
   with self.assertRaisesRegex(ValueError,'No implicit terminal'):p.v2.run('claim-warrant')
   execute.assert_not_called()
 def test_changed_published_metrics_rejected(self):
  original=p.c.read
  def read(path):
   data=original(path)
   if Path(path)==p.H/'metrics.json':data['provider_calls']+=1
   return data
  with patch.object(p.c,'read',side_effect=read):
   with self.assertRaisesRegex(ValueError,'Metrics drift'):p.verify()
 def test_all_unsupported_claims_have_dependency_records(self):
  metrics=p.c.read(p.H/'metrics.json')
  for cid,row in metrics['cases'].items():
   a=row['artifact_viability'];ids={x['claim_id'] for x in metrics['unsupported_claims'] if x['case_id']==cid}
   self.assertEqual(ids,{x['claim_id'] for x in a['unsupported_claims']})
   self.assertEqual(ids,{x['claim_id'] for x in a['per_claim_dependencies']})
if __name__=='__main__':unittest.main()
