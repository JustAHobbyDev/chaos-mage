"""Post-freeze analysis checks; these never alter experimental inputs."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner as r
import metrics as m
import diagnostics

class ReviewTests(unittest.TestCase):
 def test_reversed_diagnostics_follow_identity(self):
  p={'mapping_1':'one','mapping_2':'two','mapping_A':'one','mapping_B':'two'}
  q={**p,'mapping_A':'two','mapping_B':'one'}
  a=copy.deepcopy(r.probe_response('comparison'));a['mapping_A']['counterfactual_native']['status']='likely';a['mapping_A']['scope']['local_displacement']='high';a['mapping_B']['counterfactual_native']['status']='unlikely'
  # Probe fixture shares mapping objects before deepcopy; replace the slots independently.
  a['mapping_A']=copy.deepcopy(a['mapping_A']);a['mapping_B']=copy.deepcopy(a['mapping_B'])
  a['mapping_A']['counterfactual_native']['status']='likely';a['mapping_B']['counterfactual_native']['status']='unlikely';a['mapping_A']['scope']['local_displacement']='high';a['mapping_B']['scope']['local_displacement']='low'
  b=copy.deepcopy(a);b['mapping_A'],b['mapping_B']=b['mapping_B'],b['mapping_A']
  self.assertEqual(m.normalized(a,p)['mappings'],m.normalized(b,q)['mappings'])
  self.assertEqual(m.normalized(a,p)['mappings']['one']['counterfactual_native']['status'],'likely')
  self.assertEqual(m.normalized(b,q)['mappings']['two']['scope']['local_displacement'],'low')
 def test_counterfactual_changes_from_raw_identity_groups(self):
  values=r.published('comparison');pairs=[p for p in r.pair_records() if p['cohort']=='primary'];computed=diagnostics.compute()
  for family in 'AB':
   by={}
   for p in pairs:
    for slot in 'AB':by.setdefault(p['mapping_'+slot],[]).append(values[(p['case_id'],family)]['mapping_'+slot]['counterfactual_native']['status'])
   changed=sorted(mid for mid,v in by.items() if len(set(v))>1)
   self.assertEqual(changed,sorted(x['mapping_id'] for x in computed['repeated_mapping_diagnostics'][family]['changed']['counterfactual']))
 def test_frozen_primary_and_control_partition(self):
  pairs=r.pair_records();self.assertEqual(len(pairs),34);self.assertEqual(sum(p['cohort']=='primary' for p in pairs),28)
  r.frozen('comparison',True);actual=m.calculate(r.published('comparison'),pairs);self.assertEqual(actual,r.read(r.HERE/'metrics.json'));self.assertEqual(diagnostics.compute(),r.read(r.HERE/'review/diagnostics.json'))

if __name__=='__main__':unittest.main()
