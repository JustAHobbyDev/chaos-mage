"""Postmeasurement evidence checks; never launches or modifies observations."""
import importlib.util
import json
from pathlib import Path
import unittest

H=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('h8_results',H/'runner.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

class FrozenResults(unittest.TestCase):
 def test_complete_eight_unique_unchanged_observations(self):
  sessions=[]; counts={}
  for stage in ['native','augmented','impact']:
   counts[stage]=0
   for uid in r.slots(stage):
    d=H/'raw'/stage/uid
    self.assertEqual((d/'request.txt').read_bytes(),r.packet(stage,uid).read_bytes())
    self.assertEqual((d/'response.json').read_bytes(),r.response(stage,uid).read_bytes())
    self.assertEqual(r.sha(d/'response.json'),r.read(d/'validation.json')['response_sha256'])
    self.assertEqual(r.read(d/'exit.json'),{'returncode':0,'timeout':False})
    sessions.append(r.read(d/'validation.json')['metadata']['session_id']); counts[stage]+=1
  self.assertEqual(counts,{'native':2,'augmented':3,'impact':3})
  self.assertEqual(len(set(sessions)),8)
 def test_actual_blind_projection_and_shared_baseline(self):
  hashes=[]
  for p in r.manifest()['pairs']:
   order=r.read(H/'comparison-order'/f'{p["pair_id"]}.json'); packet=r.read(H/'impact-packets'/f'{p["pair_id"]}.json')
   self.assertEqual(set(packet),{'target_frame','response_a','response_b'})
   for side in ('A','B'):
    stage='native' if order[side]=='NATIVE' else 'augmented'; slot=p['native_slot'] if stage=='native' else p['augmented_slot']
    self.assertEqual(packet['response_'+side.lower()],r.read(r.response(stage,slot))['target_response'])
   for forbidden in ['survivor_basis','H7-T','KEEP_WITH','SURVIVOR_AUGMENTED','NATIVE']:
    self.assertNotIn(forbidden,r.packet('impact',p['pair_id']).read_text())
   if p['target_id']=='T03': hashes.append(order['native_response_sha256'])
  self.assertEqual(len(set(hashes)),1)
 def test_stage_barriers_in_execution_commits(self):
  for stage,prereq in [('augmented','native-freeze.json'),('impact','impact-packets-freeze.json')]:
   for uid in r.slots(stage):
    commit=r.read(H/'raw'/stage/uid/'attempt.json')['execution_commit']
    r.git('cat-file','-e',commit+':distance/target-impact-v0.1/'+prereq)
  unblind_parent=r.read(H/'unblinded-freeze.json')['execution_parent']
  r.git('cat-file','-e',unblind_parent+':distance/target-impact-v0.1/impact-freeze.json')
 def test_direction_and_attribution_full_coverage(self):
  for p in r.manifest()['pairs']:
   pid=p['pair_id']; j=r.read(r.response('impact',pid))['impact_judgment']; u=r.read(H/'unblinded'/f'{pid}.json')
   self.assertEqual(u['judgment_sha256'],r.sha(r.response('impact',pid)))
   for d,x in zip(j['differences'],u['directed_differences']):
    self.assertEqual(x['introduced_by'],r.direction(d,u['order']))
    self.assertEqual(x['material'],d['materially_changes_target_reasoning'])
   a=r.read(H/'attribution-audit'/f'{pid}.json')
   needed={d['difference_id'] for d in u['directed_differences'] if d['material']=='YES' and d['introduced_by'] in ('SURVIVOR_AUGMENTED','BOTH_DIFFERENT')}
   self.assertTrue(needed<={x['difference_id'] for x in a['differences']})
   for x in a['differences']:
    if x['classification']=='ATTRIBUTABLE_TO_SURVIVOR':
     self.assertTrue(x['support']); self.assertTrue(x['checks']['support_candidates_definite'])
     self.assertFalse(x['checks']['deleted_claim_needed_for_credited_change'])
     self.assertFalse(x['checks']['unresolved_candidate_promoted_in_credited_change'])
     self.assertTrue(x['checks']['credited_change_within_frozen_scope'])
     cited={v for b in x['frozen_model_basis'] for v in b['consideration_ids']}
     self.assertTrue({v['consideration_id'] for v in x['support']}<=cited)
 def test_metrics_rederive_without_writing(self):
  m=r.read(H/'metrics.json'); count=0; categories={c:0 for c in r.CATEGORIES}
  for row in m['survivor_impact']:
   pid=row['pair_id']; j=r.read(r.response('impact',pid))['impact_judgment']; ds=r.read(H/'unblinded'/f'{pid}.json')['directed_differences']; a=r.read(H/'attribution-audit'/f'{pid}.json')
   self.assertEqual(row['impact_status'],r.impact_status(j,ds,a['differences'],a['nonmaterial_augmented_additions']))
   for d in ds:
    if d['difference_id'] in row['survivor_attributable_material_changes']:
     count+=1
     for c in set(d['categories']): categories[c]+=1
  self.assertEqual(count,m['survivor_attributable_material_changes'])
  self.assertEqual(categories,m['survivor_attributable_category_counts'])
 def test_all_historical_and_frozen_bytes(self):
  self.assertEqual(r.verify()['historical_files'],18477)

if __name__=='__main__': unittest.main()
