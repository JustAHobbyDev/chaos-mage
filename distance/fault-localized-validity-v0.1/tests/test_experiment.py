import copy,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner as r
import contracts as c

class ExperimentTests(unittest.TestCase):
 def test_full_source_coverage_and_preservation(self): self.assertEqual(r.verify()['claims'],50)
 def test_threshold_precedes_inventory(self):
  m=c.read(r.H/'manifest.json')
  for p in ['CORE-INVALIDITY.md','CLAIM-WARRANT.md','PROTOCOL.md']: r.committed(r.H/p,m['policy_checkpoint'])
  import subprocess
  result=subprocess.run(['git','cat-file','-e',m['policy_checkpoint']+':distance/fault-localized-validity-v0.1/claims/inventory.json'],cwd=r.R,stderr=subprocess.PIPE)
  self.assertNotEqual(result.returncode,0)
 def test_only_diagnostic_corpus(self): self.assertEqual({a['case_id'] for a in r.claims()},set(r.CASES))
 def test_every_inference_unit_accounted(self):
  audit=c.read(r.H/'claims/extraction-audit.json')
  for cid in r.CASES:
   text=r.candidate(cid)['mapping']['inference']
   rows=[x for x in audit if x['case_id']==cid and x['source_field']=='mapping.inference']
   for row in reversed(rows): text=text[:row['start']]+text[row['end']:]
   self.assertFalse(text.strip())
 def test_exact_spans_and_no_labels(self):
  for a in r.claims():
   text=r.candidate(a['case_id'])['mapping'][a['source_field'].split('.')[1]]
   self.assertEqual(text[a['span_start']:a['span_end']],a['exact_claim_span'])
   self.assertFalse(set(a)&{'status','support','warrant','expected_status'})
 def test_packet_allowlist_and_no_diagnostics(self):
  banned=['historical Astra','historical Fable','Experiment F findings','E006 is local','E022 is partial','E030 is partial/core','Muse/Gemini','operator expectations']
  for a in r.claims():
   text=r.packet('claim-warrant',a['claim_id']).read_text()
   self.assertEqual(text,r.reconstructed_claim_packet(a))
   body=json.loads(text.split('\nCASE PACKET\n')[1]); self.assertEqual(set(body),{'source','target','mapping','atomic_claim'})
   for s in banned:self.assertNotIn(s,text)
 def test_fresh_astra_high_toolless_command(self):
  cmd=r.command('/tmp/empty',Path('/tmp/output'),'claim-warrant')
  for x in ['gpt-6-astra','--ephemeral','--ignore-user-config','--ignore-rules','project_doc_max_bytes=0','model_reasoning_effort="high"','web_search="disabled"']:self.assertIn(x,cmd)
  self.assertTrue({'apps','plugins','memories','multi_agent','shell_tool','unified_exec','browser_use','hooks','skill_search'}<=set(r.cfg()['codex_disabled_features']))
 def test_environment_drops_parent_context(self):
  with patch.dict(r.os.environ,{'CODEX_THREAD_ID':'secret','OPENAI_MODEL':'other','CLAUDECODE':'1'}):
   self.assertFalse({'CODEX_THREAD_ID','OPENAI_MODEL','CLAUDECODE'}&set(r.clean_env()))
 def test_simultaneous_deletion_without_replacement(self):
  mapping={'state':'unchanged','inference':'one two three four'}
  atoms=[{'source_field':'mapping.inference','span_start':0,'span_end':3,'exact_claim_span':'one','claim_id':'X'},{'source_field':'mapping.inference','span_start':8,'span_end':13,'exact_claim_span':'three','claim_id':'Y'}]
  self.assertEqual(r.delete_claims(mapping,atoms),{'state':'unchanged','inference':'[DELETED X] two [DELETED Y] four'})
  self.assertEqual(mapping['inference'],'one two three four')
 def test_delete_rejects_drift(self):
  with self.assertRaises(ValueError):r.delete_claims({'inference':'abc'},[{'source_field':'mapping.inference','span_start':0,'span_end':2,'exact_claim_span':'xx','claim_id':'X'}])
 def test_real_deletion_preserves_all_remaining_bytes(self):
  for cid in r.CASES:
   atoms=[a for a in r.claims() if a['case_id']==cid]; m=r.candidate(cid)['mapping']; deleted=r.delete_claims(m,atoms)
   for field,text in m.items():
    for a in sorted([a for a in atoms if a['source_field']=='mapping.'+field],key=lambda a:a['span_start'],reverse=True): text=text[:a['span_start']]+f'[DELETED {a["claim_id"]}]'+text[a['span_end']:]
    self.assertEqual(deleted[field],text)
 def test_event_audit_rejects_tools_and_substitution(self):
  base=[{'type':'thread.started','thread_id':'fresh'},{'type':'turn.completed'}]
  r.audit_events(base)
  for e in [{'type':'item.completed','item':{'type':'command_execution'}},{'type':'init','model':'different'},{'type':'turn.failed'}]:
   with self.assertRaises(ValueError):r.audit_events(base+[e])
 def test_claim_conditions_and_uncertainty(self):
  v={'claim_id':'X','status':'SUPPORTED','rationale':'r','signal_basis':'s','stated_empirical_relation':None,'uncertainty':[]}; c.validate(v,'claim-warrant','X')
  for status in ['CONDITIONAL_WARRANT','UNCERTAIN']:
   with self.assertRaises(ValueError):c.validate({**v,'status':status},'claim-warrant','X')
 def fixture(self,m='survives',t='substantially_survives',s='KEEP_WITH_WARRANT_FLAGS'):
  return {'artifact_viability':{'case_id':'X','unsupported_claims':[{'claim_id':'C'}],'mechanism_survival':{'status':m,'rationale':'r'},'target_contribution_survival':{'status':t,'surviving_contributions':[] if t=='no_material_contribution' else ['r']},'dependency_cascade':{'failed_downstream_claims':[],'failed_actions_or_inquiries':[],'surviving_actions_or_inquiries':['r'],'rationale':'r'},'per_claim_dependencies':[{'claim_id':'C','signal':'s','dependent_claims':[],'dependent_actions_or_inquiries':[],'rationale':'r'}],'artifact_status':s,'rationale':'r'}}
 def test_all_status_invariants(self):
  valid=[('survives','substantially_survives',c.ARTIFACT[0]),('partially_survives','reduced_but_material',c.ARTIFACT[1]),('does_not_survive','no_material_contribution',c.ARTIFACT[2]),('uncertain','reduced_but_material',c.ARTIFACT[3])]
  for m,t,s in valid:c.validate(self.fixture(m,t,s),'ablation','X',unsupported=['C'])
  invalid=[('partially_survives','substantially_survives',c.ARTIFACT[0]),('survives','substantially_survives',c.ARTIFACT[1]),('survives','reduced_but_material',c.ARTIFACT[2]),('survives','substantially_survives',c.ARTIFACT[3])]
  for m,t,s in invalid:
   with self.assertRaises(ValueError):c.validate(self.fixture(m,t,s),'ablation','X')
 def test_all_bad_claims_must_be_covered(self):
  with self.assertRaises(ValueError):c.validate(self.fixture(),'ablation','X',unsupported=['C','D'])
 def test_no_historical_mutation_or_execution(self):
  r.hashes(c.read(r.H/'preservation.json')['files'])
  commands=c.read(r.H/'historical-commands.json')
  for cmd in commands:
   self.assertFalse(set(cmd)&{'run','preflight','resume','recover','freeze','prepare','generate'})
 def test_unique_reservation_refuses_replacement(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x'; r.write(p,{'original':True})
   with self.assertRaises(FileExistsError):r.write(p,{'original':False})
   self.assertEqual(c.read(p),{'original':True})
 def test_paused_and_terminal_states_block(self):
  for state in ['PAUSED_AMBIGUOUS','PAUSED_RECOVERABLE','TERMINATED_LINEAGE','TERMINATED_MEASUREMENT']:
   with patch.object(r,'state',return_value=state),patch.object(r,'execute') as execute:
    with self.assertRaises(ValueError):r.run('claim-warrant')
    execute.assert_not_called()
 def test_ablation_requires_committed_claim_freeze(self):
  with patch.object(r,'committed',side_effect=ValueError('not committed')),patch.object(r,'write') as write:
   with self.assertRaises(ValueError):r.prepare('ablation')
   write.assert_not_called()
 def test_historical_adapter_checks_live_bytes(self):
  import historical
  self.assertGreater(historical.guard(),0)
  original=Path.read_bytes
  target=r.R/'docs/PROBLEM_FRAMES.md'
  with patch.object(Path,'read_bytes',lambda p: b'corrupt' if p==target else original(p)):
   with self.assertRaisesRegex(AssertionError,'Live historical bytes changed'):historical.guard()
 def test_preflight_recovery_retains_original(self):
  p=r.H/'recovery/premeasurement-original/review/claim-warrant-preflight.json'
  self.assertEqual(c.read(p)['provider_calls'],0)
  self.assertEqual(sum(x['exit_code']!=0 for x in c.read(p)['checks']),5)
  original=c.read(r.H/'recovery/premeasurement-original/claims/inventory.json')
  self.assertEqual(len(original),45)
 def test_no_provider_probes_or_subsets(self):
  self.assertEqual(r.cfg()['probe_limit_per_stage'],0)
  self.assertEqual(r.cfg()['authorized_claim_measurements'],50)
  self.assertEqual(r.cfg()['max_concurrent_processes'],1)
  if (r.H/'ablation-manifest.json').exists():
   m=c.read(r.H/'ablation-manifest.json'); self.assertFalse(m['subsets']); self.assertEqual(len(m['case_order']),len(set(m['case_order'])))
if __name__=='__main__':unittest.main()
