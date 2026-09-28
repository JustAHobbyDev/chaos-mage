import copy
import json
from pathlib import Path
import random
import re
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import runner as r
import contracts as c
import metrics as m

class Tests(unittest.TestCase):
 def output(self,relation='tie'):
  v=copy.deepcopy(r.probe_response('comparison'));v['case_id']='C001';v['overall_relation']=relation
  if relation not in ('tie','indeterminate'):v['decisive_basis']['primary_criterion']='action'
  if relation=='indeterminate':v['uncertainty']=['Missing common-state distinction.']
  return v
 def validity(self,status='Valid'):
  v=copy.deepcopy(r.probe_response());v['case_id']='001';v['validity']['final_status']=status
  if status=='Conditional':v['validity']['operational_coherence']['status']='conditional';v['validity']['unresolved_conditions']=['Establish repeatability.']
  if status=='Invalid':v['validity']['mechanism_fidelity']['status']='not-preserved'
  return v
 def admissions(self):return [{'mapping_id':x['mapping_id'],'target_id':x['target_id'],'admitted':True,'validity_A':'Valid','validity_B':'Valid'} for x in r.manifest()]
 def pairs(self):return r.construct_pairs(self.admissions())[0]
 def test_inputs_and_history(self):r.validate_inputs()
 def test_no_absolute_taxonomy(self):
  for name in ('CLASSIFIER.md','output.schema.json','comparison-wire.schema.json'):
   self.assertIsNone(re.search(r'\b(Native|Adjacent|Remote|Alien)\b',(r.HERE/name).read_text(),re.I))
 def test_criterion_enums(self):
  for key in c.CRITERIA:
   for relation in ('A','B','tie','indeterminate'):v=self.output();v['criteria'][key]['relation']=relation;c.validate(v,'comparison')
   for relation in ('mapping_1_more',0,True,'unknown'):v=self.output();v['criteria'][key]['relation']=relation;self.assertRaises(c.jsonschema.ValidationError,c.validate,v,'comparison')
 def test_overall_enums_and_decisive_requirement(self):
  for relation in ('A_more_displacing','B_more_displacing','tie','indeterminate'):c.validate(self.output(relation),'comparison')
  for relation in ('A','B',0,False,'unknown'):v=self.output();v['overall_relation']=relation;self.assertRaises(c.jsonschema.ValidationError,c.validate,v,'comparison')
  v=self.output('A_more_displacing');v['decisive_basis']['primary_criterion']='none';self.assertRaises(ValueError,c.validate,v,'comparison')
 def test_scope_counterfactual_and_no_score(self):
  for key in ('local_displacement','global_propagation'):
   for status in ('low','moderate','high'):v=self.output();v['mapping_A']['scope'][key]=status;c.validate(v,'comparison')
   for status in (0,1,True,'clear'):v=self.output();v['mapping_A']['scope'][key]=status;self.assertRaises(c.jsonschema.ValidationError,c.validate,v,'comparison')
  for key in ('score','composite','grounding','class','operator_intention'):v=self.output();v[key]=1;self.assertRaises(c.jsonschema.ValidationError,c.validate,v,'comparison')
  for status in ('likely','unlikely','uncertain'):v=self.output();v['mapping_A']['counterfactual_native']['status']=status;c.validate(v,'comparison')
 def test_rationale_and_indeterminate(self):
  v=self.output();v['criteria']['action']['rationale']='  ';self.assertRaises(c.jsonschema.ValidationError,c.validate,v,'comparison')
  v=self.output('indeterminate');v['uncertainty']=[];self.assertRaises(ValueError,c.validate,v,'comparison')
 def test_pair_identity_baseline_and_admission(self):
  p=self.pairs()[0];maps={x['mapping_id']:r.candidate(x['mapping_id']) for x in r.manifest()};bases={x['target_id']:r.read(r.HERE/'baselines'/f'{x["target_id"]}.json') for x in r.manifest()};ad={x['mapping_id']:x for x in self.admissions()}
  c.validate_pair(p,maps,bases,ad)
  for status in ('Conditional','Invalid'):
   broken=copy.deepcopy(ad);broken[p['mapping_1']]['validity_B']=status;self.assertRaises(ValueError,c.validate_pair,p,maps,bases,broken)
  broken=copy.deepcopy(ad);broken[p['mapping_1']]['admitted']=False;self.assertRaises(ValueError,c.validate_pair,p,maps,bases,broken)
  broken=copy.deepcopy(maps);broken[p['mapping_1']]['target']['question']='different';self.assertRaises(ValueError,c.validate_pair,p,broken,bases,ad)
  broken=copy.deepcopy(ad);broken[p['mapping_1']]['target_id']='wrong';self.assertRaises(ValueError,c.validate_pair,p,maps,bases,broken)
 def test_blinding_and_baseline_bytes(self):
  for p in self.pairs():
   packet=r.comparison_packet(p);body=json.loads(packet.split('\n\nCASE PACKET\n')[1])
   self.assertEqual(set(body),{'case_id','target_question','ordinary_practice_baseline','mapping_A','mapping_B'})
   self.assertIn((r.HERE/'baselines'/f'{p["target_id"]}.json').read_bytes(),packet.encode())
   for slot in 'AB':self.assertEqual(set(body['mapping_'+slot]),{'source','evidence_context','mapping'})
   for word in ('intended_band','historical_case_id','validity_A','expected','control_of','provisional','decisive_basis'):self.assertNotIn('"'+word+'"',packet)
 def test_reproducible_balanced_schedule(self):
  a=r.construct_pairs(self.admissions());b=r.construct_pairs(self.admissions());self.assertEqual(a,b);pairs,schedule,v=a
  self.assertEqual(v['primary_pairs'],28);self.assertTrue(v['passes']);self.assertEqual(len(schedule),68)
  primary=[p for p in pairs if p['cohort']=='primary'];self.assertEqual(sum(p['mapping_A']==p['mapping_1'] for p in primary),14)
  for target in v['targets']:
   ps=[p for p in primary if p['target_id']==target];self.assertLessEqual(abs(sum(p['mapping_A']==p['mapping_1'] for p in ps)*2-len(ps)),1)
  self.assertEqual(len({(p['case_id'],p['family']) for p in schedule}),68)
 def test_controls_only_reverse_content(self):
  pairs=self.pairs();lookup={p['case_id']:p for p in pairs}
  for p in pairs:
   if p['cohort']=='primary':continue
   o=lookup[p['control_of']];a=json.loads(r.comparison_packet(o).split('\n\nCASE PACKET\n')[1]);b=json.loads(r.comparison_packet(p).split('\n\nCASE PACKET\n')[1])
   a['case_id']=b['case_id'];a['mapping_A'],a['mapping_B']=a['mapping_B'],a['mapping_A'];self.assertEqual(a,b)
 def test_normalization_all_relations(self):
  for p in self.pairs():
   for slot in 'AB':
    expected='mapping_1_more' if p['mapping_'+slot]==p['mapping_1'] else 'mapping_2_more'
    self.assertEqual(c.normalize_relation(slot+'_more_displacing',p),expected);self.assertEqual(c.normalize_relation(slot,p,True),expected)
   self.assertEqual(c.normalize_relation('tie',p),'tie');self.assertEqual(c.normalize_relation('indeterminate',p),'indeterminate')
 def test_admission_viability_no_backfill(self):
  admissions=self.admissions()
  for x in admissions:
   if next(m for m in r.manifest() if m['mapping_id']==x['mapping_id'])['new']:x['admitted']=False
  pairs,schedule,v=r.construct_pairs(admissions);self.assertFalse(v['passes']);self.assertEqual(v['primary_pairs'],16);self.assertEqual(pairs,[]);self.assertEqual(schedule,[])
 def test_metrics_denominators_controls_and_missing(self):
  pairs=self.pairs();values={(p['case_id'],f):{**self.output(),'case_id':p['case_id']} for p in pairs for f in 'AB'};v=m.calculate(values,pairs)
  self.assertEqual(v['overall_agreement']['denominator'],28);self.assertEqual(v['ties']['tie_vs_tie'],28);self.assertEqual(v['counterfactual_agreement']['denominator'],56);self.assertEqual(len(v['orientation_controls']),6)
  p=next(p for p in pairs if p['cohort']=='primary');del values[(p['case_id'],'B')];v=m.calculate(values,pairs);self.assertEqual(v['planned_primary_pairs'],28);self.assertEqual(v['observed_primary_pairs'],27);self.assertEqual(v['missing_pair_ids'],[p['case_id']])
  self.assertIsNone(m.calculate({},[])['overall_agreement']['rate'])
 def test_known_directional_metrics(self):
  pairs=[{'case_id':str(i),'target_id':'T','mapping_1':'x'+str(i),'mapping_2':'y'+str(i),'mapping_A':'x'+str(i),'mapping_B':'y'+str(i),'cohort':'primary','control_of':None} for i in range(5)]
  answers=[('A_more_displacing','A_more_displacing'),('A_more_displacing','B_more_displacing'),('tie','B_more_displacing'),('tie','tie'),('indeterminate','A_more_displacing')]
  values={(str(i),f):self.output(answers[i][j]) for i in range(5) for j,f in enumerate('AB')};v=m.calculate(values,pairs)
  self.assertEqual(v['overall_agreement']['agreements'],2);self.assertEqual(v['directional'],{'same':1,'opposite':1,'denominator':2});self.assertEqual(v['ties'],{'direction_vs_tie':1,'tie_vs_tie':1});self.assertEqual(sum(v['indeterminate_combinations'].values()),1)
 def test_direction_tie_and_review_labels(self):
  p={'mapping_A':'x','mapping_B':'y','mapping_1':'x','mapping_2':'y'}
  n=lambda x:m.normalized(self.output(x),p)
  self.assertEqual(m.post_status(n('A_more_displacing'),n('B_more_displacing')),'contested-direction')
  self.assertEqual(m.post_status(n('A_more_displacing'),n('tie')),'order-vs-tie')
  self.assertEqual(m.post_status(n('tie'),n('tie')),'stable-tie')
  self.assertEqual(m.post_status(n('indeterminate'),n('tie')),'indeterminate')
  self.assertEqual(m.post_status(n('A_more_displacing'),n('A_more_displacing'),False),'close-order')
 def test_transitivity_fixtures(self):
  edges={('a','b'):'mapping_1_more',('b','c'):'mapping_1_more',('a','c'):'mapping_1_more'}
  self.assertEqual(m.triangle_status(edges),('transitive',False))
  edges[('a','c')]='mapping_2_more';self.assertEqual(m.triangle_status(edges),('cycle',False))
  edges[('a','c')]='tie';self.assertEqual(m.triangle_status(edges),('tie-compatible',True))
  edges[('a','c')]='indeterminate';self.assertEqual(m.triangle_status(edges),('indeterminate',False))
  self.assertEqual(m.cycles([('a','b'),('b','c'),('c','d'),('d','a')]),[['a','b','c','d']])
 def test_eight_complete_triangles(self):
  pairs=self.pairs();values={(p['case_id'],f):self.output() for p in pairs for f in 'AB'};v=m.calculate(values,pairs)
  for f in 'AB':self.assertEqual(len(v['transitivity'][f]['triangles']),8)
 def test_wire_projection(self):
  for stage in ('validity','comparison'):self.assertEqual(r.read(r.HERE/f'{stage}-wire.schema.json'),r.projection(r.read(r.canonical(stage))));c.validate(r.probe_response(stage),stage)
 def test_commands_isolation_and_schema(self):
  for stage in ('validity','comparison'):
   a=r.build_command('A','/tmp/empty',Path('/tmp/out'),'s',stage)
   for flag in ('--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check','shell_tool','plugins','apps','multi_agent'):self.assertIn(flag,a)
   self.assertIn(str(r.HERE/f'{stage}-wire.schema.json'),a)
   b=r.build_command('B','/tmp/empty',Path('/tmp/out'),'s',stage);self.assertEqual(b[b.index('--tools')+1],'');self.assertIn('--safe-mode',b)

 def test_duplicate_keys(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'x';p.write_text('{"case_id":"a","case_id":"b"}')
   with self.assertRaises(ValueError):c.read(p)
 def test_duplicate_session(self):
  with tempfile.TemporaryDirectory() as td,patch.object(r,'RUNTIME',Path(td)):
   r.write_new(Path(td)/'old/validation.json',{'metadata':{'session_id':'reused'}})
   with self.assertRaisesRegex(ValueError,'Duplicate session'):r.check_fresh_session('reused',Path(td)/'new')
 def test_timeout_preserves_attempt(self):
  class Process:
   pid=999999
   def communicate(self,*a,**k):raise subprocess.TimeoutExpired('fixture',900)
   def wait(self):return -9
  with tempfile.TemporaryDirectory() as td,patch.object(r.subprocess,'Popen',return_value=Process()),patch.object(r.subprocess,'check_output',return_value=r.config()['expected_cli_versions']['A']),patch.object(r,'git',return_value=b'commit'),patch.object(r.os,'killpg') as kill:
   result=r.execute('A',Path(td)/'attempt','fixture');self.assertEqual(result['status'],'failed');self.assertIn('TimeoutExpired',result['error']);kill.assert_called_once();self.assertTrue((Path(td)/'attempt/validation.json').exists())
 def events(self,value):
  return [{'type':'system','subtype':'init','session_id':'s','model':'claude-fable-5-1','tools':['StructuredOutput'],'plugins':[],'mcp_servers':[]},{'type':'assistant','message':{'model':'claude-fable-5-1','content':[{'type':'tool_use','name':'StructuredOutput','input':value}]}},{'type':'result','subtype':'success','session_id':'s','structured_output':value,'modelUsage':{'claude-fable-5-1':{}},'num_turns':2}]
 def test_fallback_tools_sessions(self):
  for kind in ('fallback','tool','plugin','session'):
   events=self.events(self.validity())
   if kind=='fallback':events[1]['message']['model']='wrong'
   if kind=='tool':events[0]['tools'].append('Read')
   if kind=='plugin':events[0]['plugins'].append('wrong')
   if kind=='session':events[0]['session_id']='wrong'
   with self.assertRaises(ValueError):r.legacy.audit_events(events,'B','claude-fable-5-1[1m]','s')
 def test_malformed_response_retained(self):
  cid=r.manifest()[0]['mapping_id'];invalid=self.validity();invalid['case_id']=cid;invalid['validity']['final_status']='Invalid';events=self.events(invalid)
  class Process:
   returncode=0
   def communicate(self,*a,**k):pass
  def popen(*a,**k):k['stdout'].write('\n'.join(map(json.dumps,events))+'\n');k['stdout'].flush();return Process()
  with tempfile.TemporaryDirectory() as td,patch.object(r.subprocess,'Popen',side_effect=popen),patch.object(r.subprocess,'check_output',return_value=r.config()['expected_cli_versions']['B']),patch.object(r,'git',return_value=b'commit'),patch.object(r.uuid,'uuid4',return_value='s'):
   d=Path(td)/'attempt';result=r.execute('B',d,'fixture',{'case_id':cid});self.assertEqual(result['status'],'failed');self.assertNotIn('FileNotFoundError',result['error']);self.assertEqual(r.read(d/'response.json'),invalid)
 def test_scheduler_stop_repeat_and_commit_gate(self):
  with tempfile.TemporaryDirectory() as td,patch.object(r,'RUNTIME',Path(td)),patch.object(r,'prerequisites'),patch.object(r,'git',return_value=b'commit'),patch.object(r,'execute',return_value={'status':'failed','error':'fixture'}) as execute:
   with self.assertRaises(ValueError):r.run_all('validity')
   self.assertEqual(execute.call_count,1);self.assertTrue((Path(td)/'STOP.json').exists())
   with self.assertRaises(FileExistsError):r.run_all('validity')
   self.assertEqual(execute.call_count,1)
  if (r.HERE/'prepared.json').exists():
   with patch.object(r,'git',return_value=b'wrong'):
    with self.assertRaises(ValueError):r.verify(True)
 def test_exclusive_writes(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'x';r.write_new(p,{})
   with self.assertRaises(FileExistsError):r.write_new(p,{})
 def test_internal_formatter_retries(self):
  e=self.events(self.validity());e.insert(2,copy.deepcopy(e[1]));meta,_=r.legacy.audit_events(e,'B','claude-fable-5-1[1m]','s');self.assertEqual(meta['formatting_retries']['observed_formatting_retries'],1)

if __name__=='__main__':unittest.main()
