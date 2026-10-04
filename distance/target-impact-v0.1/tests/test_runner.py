"""Offline acceptance; no provider calls."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

H=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('h8',H/'runner.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

class Boundaries(unittest.TestCase):
 def test_all_packets_match_allowlists_scopes_and_deletions(self): r.audit_packets()
 def test_all_positive_values_unchanged_and_cautions_present(self):
  for sid,n in zip(r.manifest()['survivors'],[15,9,8]):
   p=r.read(H/'survivor-packets'/f'{sid}.json')
   self.assertEqual(len(p['considerations']),n); self.assertTrue(p['cautions'])
  self.assertIn('does not by itself',r.read(H/'survivor-packets/H7-T03-1.json')['cautions'][0])
  self.assertIn('do not select an intervention',r.read(H/'survivor-packets/H7-T03-2.json')['cautions'][0])
 def test_shared_prompt_target_and_schema(self):
  instruction=(H/'target-instruction.txt').read_text().strip()
  for stage in ['native','augmented']:
   for uid in r.slots(stage): self.assertTrue(r.packet(stage,uid).read_text().startswith(instruction))
  pairs=r.manifest()['pairs']; self.assertEqual(pairs[1]['native_slot'],pairs[2]['native_slot'])
  n=r.read(H/'native-packets/T03.json')['target_frame']
  for sid in ['H7-T03-1','H7-T03-2']: self.assertEqual(n,r.read(H/'augmented-packets'/f'{sid}.json')['target_frame'])
  self.assertEqual(r.command('/tmp/a',Path('/tmp/out'),'native'),r.command('/tmp/a',Path('/tmp/out'),'augmented'))
 def test_schema_cardinalities(self):
  schema=r.read(H/'schemas/target.schema.json')['properties']['target_response']['properties']
  for k,v in schema.items():
   if v['type']=='array': self.assertEqual(v['maxItems'],4 if k=='important_distinctions' else 3)
 def test_identity_scanner(self):
  for name in ['ACH','crossdating','chain-of-custody','Chaos Mage','source instrument']: self.assertTrue(r.BANNED.search(name))
  self.assertFalse(r.BANNED.search('compare competing explanations; preserve order-specific continuity'))
 def test_order_is_deterministic_and_direction_is_mechanical(self):
  for p in r.manifest()['pairs']:
   o=r.ordering(p['pair_id']); self.assertEqual(o,r.ordering(p['pair_id']))
   self.assertEqual({o['A'],o['B']},{'NATIVE','SURVIVOR_AUGMENTED'})
   self.assertEqual(r.direction({'introduced_in':'A_ONLY'},o),o['A'])
   self.assertEqual(r.direction({'introduced_in':'BOTH_DIFFERENT'},o),'BOTH_DIFFERENT')
 def test_blinded_schema_has_no_condition_labels(self):
  s=json.dumps(r.read(H/'schemas/impact.schema.json'))
  for term in ['SURVIVOR_AUGMENTED','NATIVE','survivor_basis','h7_admission']: self.assertNotIn(term,s)
 def test_comparison_construction_only_visible_projection(self):
  source=(H/'runner.py').read_text().split('def comparisons():')[1].split('def direction')[0]
  self.assertIn("['target_response']",source); self.assertNotIn('survivor_basis',source)
 def test_unblinding_requires_judgment_freeze(self):
  with patch.object(r,'verify'),patch.object(r,'H',Path('/tmp/h8-nonexistent-fixture')):
   with self.assertRaisesRegex(ValueError,'judgments must freeze'): r.unblind()
 def test_append_only_writer(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'judgment.json'; r.write(p,{'original':True})
   with self.assertRaises(FileExistsError): r.write(p,{'original':False})
   self.assertEqual(r.read(p),{'original':True})
 def test_gate_denial_never_launches(self):
  gate,launch=Mock(),Mock(); gate.reserve.side_effect=r.budget.BudgetError('denied')
  with self.assertRaises(r.budget.BudgetError): r.reserve_and_launch(gate,{}, {},'native','T01',['fixture'],launch)
  launch.assert_not_called()
 def test_real_reservation_prevents_duplicate_after_failure(self):
  with tempfile.TemporaryDirectory() as tmp:
   gate=r.budget.Gate(Path(tmp)/'ledger.db',usage_reader=lambda:r.usage.normalize({'rateLimits':{'primary':{'usedPercent':70,'windowDurationMins':10080,'resetsAt':4102444800}}},'fixture'))
   plan={'version':1,'experiment_id':'fixture','description':'offline','execution_fingerprint':'fixture','execution_allowed':True,'stages':[{'id':'native','sessions':2,'estimated_cost_usd':None}]}
   policy={'version':1}; launch=Mock(side_effect=RuntimeError('transport'))
   with self.assertRaises(RuntimeError): r.reserve_and_launch(gate,plan,policy,'native','T01',['fixture'],launch)
   with self.assertRaises(r.budget.BudgetError): r.reserve_and_launch(gate,plan,policy,'native','T01',['fixture'],launch)
   self.assertEqual(launch.call_count,1)
 def test_events_tool_substitution_and_incomplete(self):
  es=[{'type':'thread.started','thread_id':'fixture'},{'type':'item.completed','item':{'type':'agent_message','text':'{}'}},{'type':'turn.completed'}]
  self.assertEqual(r.audit_events(es,'{}')['session_id'],'fixture')
  for extra in [{'type':'item.completed','item':{'type':'command_execution'}},{'model':'other'},{'type':'error'}]:
   with self.assertRaises(ValueError): r.audit_events(es+[extra],'{}')
  with self.assertRaises(ValueError): r.audit_events(es[:-1],'{}')
 def test_isolation_and_no_retry_command(self):
  cmd=r.command('/tmp/a',Path('/tmp/out'),'native')
  for flag in ['--ephemeral','--ignore-user-config','--ignore-rules','read-only','gpt-6-astra','model_reasoning_effort="high"']: self.assertIn(flag,cmd)
  for flag in ['resume','fork']: self.assertNotIn(flag,cmd)
 def test_augmented_stage_barrier(self):
  with patch.object(r,'state',return_value='READY'), patch.object(r,'H',Path('/tmp/h8-missing-barrier-fixture')), patch.object(r,'slots',return_value=['H7-T01-1']), patch.object(r,'terminal',return_value=False):
   with self.assertRaisesRegex(ValueError,'Native stage not frozen'): r.guard('augmented',['H7-T01-1'])
 def test_dependency_consequences(self):
  self.assertEqual(r.affected_pairs('native','T01'),['PAIR-01'])
  self.assertEqual(r.affected_pairs('native','T03'),['PAIR-02','PAIR-03'])
  self.assertEqual(r.affected_pairs('augmented','H7-T03-1'),['PAIR-02'])
  self.assertEqual(r.affected_pairs('impact','PAIR-03'),['PAIR-03'])
 def test_no_observation_excludes_partial_response(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp); r.raw(d/'request.txt',b'fixture'); digest=r.sha(d/'request.txt')
   r.write(d/'attempt.json',{'harness_attempt':1,'initially_empty':True,'request_sha256':digest})
   r.write(d/'process.json',{'pid':1}); r.write(d/'exit.json',{'returncode':-9})
   r.raw(d/'events.jsonl',b'{"type":"thread.started","thread_id":"fixture"}\n{"type":"turn.started"}\n')
   self.assertEqual(r.no_observation_evidence(d,digest)['classification'],'PROVIDER_NO_OBSERVATION')
   r.raw(d/'response.json',b'{')
   with self.assertRaisesRegex(ValueError,'partial response'): r.no_observation_evidence(d,digest)
 def test_duplicate_keys(self):
  with self.assertRaises(ValueError): json.loads('{"x":1,"x":2}',object_pairs_hook=r.unique)
 def test_outcomes_attribution_both_and_uncertainty(self):
  j={'overall_material_difference':'YES','semantic_equivalence':'NO','differences':[{}]}
  ds=[{'difference_id':'D1','introduced_by':'BOTH_DIFFERENT','material':'YES'}]
  audit=[{'difference_id':'D1','classification':'ATTRIBUTABLE_TO_SURVIVOR','augmented_consequence_established':True}]
  self.assertEqual(r.impact_status(j,ds,audit),'MATERIAL_TARGET_CHANGE')
  self.assertEqual(r.impact_status(j,ds,[]),'UNCERTAIN_TARGET_CHANGE')
  audit[0]['augmented_consequence_established']=False
  self.assertEqual(r.impact_status(j,ds,audit),'UNCERTAIN_TARGET_CHANGE')
  no={'overall_material_difference':'NO','semantic_equivalence':'YES','differences':[]}
  self.assertEqual(r.impact_status(no,[],[]),'NO_MATERIAL_CHANGE')
  self.assertEqual(r.impact_status(no,[],[],True),'MINOR_OR_NONMATERIAL_CHANGE')
  self.assertEqual(r.impact_status(None,[],[]),'UNMEASURED')
 def test_material_representation_requires_consequence(self):
  side={'content':'fixture','response_locations':[],'downstream_consequence':''}
  d={'difference_id':'D1','introduced_in':'B_ONLY','categories':['PROBLEM_REPRESENTATION_CHANGE'],'response_a':side,'response_b':side,'materially_changes_target_reasoning':'YES','rationale':'fixture'}
  j={'impact_judgment':{'pair_id':'PAIR-01','semantic_equivalence':'NO','differences':[d],'overall_material_difference':'YES','rationale':'fixture'}}
  with self.assertRaisesRegex(ValueError,'consequence'): r.validate('impact','PAIR-01',j)
  d['response_b']={**side,'downstream_consequence':'Gather a different observation'}
  r.validate('impact','PAIR-01',j)

if __name__=='__main__': unittest.main()
