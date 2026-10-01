import copy,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner as r
import contracts as c

class AuthoringTests(unittest.TestCase):
 def test_failed_gate_blocks_measurement(self):
  with self.assertRaisesRegex(ValueError,'authoring gate failed'):r.measurement_gate()
 def test_drafts_are_not_final_cases_or_observations(self):
  value=r.verify();self.assertEqual(value['final_cases'],0);self.assertEqual(value['provider_calls'],0);self.assertEqual(value['drafts'],36)
 def test_revised_length_balance_and_rank(self):
  groups=[g for g in r.verify()['triple_checks'] if g['revision']=='conditional_reporting_only']
  self.assertEqual(len(groups),4);shortest=set()
  for g in groups:
   self.assertLessEqual(g['ratio'],1.10);shortest.update(k for k,v in g['lengths'].items() if v==min(g['lengths'].values()))
  self.assertEqual(shortest,{'local','scope','core'})
 def test_actual_survivors_are_unchanged_mapping_spans(self):
  for a in c.read(r.H/'review/authoring-audit.json')['core_candidate_audits']:
   self.assertFalse(a['passed']);survivor=a['surviving_material_answer'];case=r.draft(a['case_id'])
   self.assertEqual(case['mapping']['signal'],a['ablated_mapping']['signal']);self.assertIn(survivor['exact_text'],a['ablated_mapping']['signal']);self.assertTrue(survivor['why_material_and_source_derived'])
 def test_source_instruments_are_frozen_and_accepted(self):
  import yaml
  sources=[yaml.safe_load(p.read_text()) for p in (r.R/'instruments').glob('*.yaml')]
  for target in c.read(r.H/'targets.json'):
   source=target['source'];matches=[x for x in sources if x['extraction']['name']==source['name']]
   self.assertEqual(len(matches),1);self.assertEqual(matches[0]['extraction']['status'],'accepted');self.assertEqual(matches[0]['instrument'],source['instrument'])
 def test_case_text_has_no_hidden_graph_metadata(self):
  for row in r.design_rows():
   case=r.draft(row['case_id']);self.assertEqual(set(case),{'source','target','mapping'})
   text=json.dumps(case)
   for key in ['intended_position','claim_graph_hypothesis','focal_identity_check','unsupported_span_chars']:self.assertNotIn(key,text)
 def test_balanced_lengths_do_not_override_semantic_gate(self):
  self.assertTrue(all(g['length_gate_passed'] for g in r.verify()['triple_checks'] if g['revision']=='conditional_reporting_only'))
  with self.assertRaises(ValueError):r.measurement_gate()
 def test_nonselected_slot_changes_are_rejected(self):
  original=r.draft
  row=next(x for x in r.design_rows() if x['revision']=='conditional_reporting_only' and x['intended_position']=='local')
  def changed(cid):
   case=copy.deepcopy(original(cid))
   if cid==row['case_id']:case['mapping']['inference']=case['mapping']['inference'].replace('\n',' changed.\n',1)
   return case
  with patch.object(r,'draft',changed),self.assertRaises(ValueError):r.verify()
if __name__=='__main__':unittest.main()
