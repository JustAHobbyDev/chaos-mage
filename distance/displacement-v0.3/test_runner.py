import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import runner as r
import contracts as c
import metrics as m

class Tests(unittest.TestCase):
 def output(self,band='Native',level=0):
  v=r.probe_response('displacement');v['case_id']='001';v['class']=band
  for d in c.DIMS:v['dimensions'][d]['level']=level
  return v
 def validity(self,status='Valid'):
  v=r.probe_response();v['case_id']='001';v['validity']['final_status']=status
  if status=='Conditional':v['validity']['operational_coherence']['status']='conditional';v['validity']['unresolved_conditions']=['Establish measurement repeatability.']
  if status=='Invalid':v['validity']['mechanism_fidelity']['status']='not-preserved'
  return v
 def admission(self):return {'case_id':'001','cohort':'primary','reason':'Both pass.','conditions':[],'applicability_assumption':None}
 def test_inputs_and_preservation(self):r.validate_inputs()
 def test_integer_strictness(self):
  for value in (True,False,1.0,2.2,-1,4,'1'):
   v=self.output();v['dimensions']['entities']['level']=value
   with self.assertRaises((ValueError,c.jsonschema.ValidationError)):c.validate(v,'displacement')
 def test_extra_missing_and_prohibited_fields(self):
  for key in ('grounding','aggregate_distance','validity','operator_intention'):
   v=self.output();v[key]=0
   with self.assertRaises(c.jsonschema.ValidationError):c.validate(v,'displacement')
  v=self.output();v['class']='Alien'
  with self.assertRaises(c.jsonschema.ValidationError):c.validate(v,'displacement')
  v=self.output();del v['dimensions']['entities']
  with self.assertRaises(c.jsonschema.ValidationError):c.validate(v,'displacement')
 def test_boundaries(self):
  for band in c.BANDS:
   for alternative in (*c.BANDS,None):
    for status in ('clear','borderline'):
     v=self.output(band);v.update(boundary_status=status,nearest_alternative=alternative)
     valid=(status=='clear' and alternative is None) or (status=='borderline' and alternative is not None and abs(c.BANDS.index(band)-c.BANDS.index(alternative))==1)
     if valid:c.validate(v,'displacement')
     else:
      with self.assertRaises(ValueError):c.validate(v,'displacement')
 def test_duplicate_keys(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'x';p.write_text('{"case_id":"a","case_id":"b"}')
   with self.assertRaises(ValueError):c.read(p)
 def test_wire_projection(self):
  for stage in ('validity','displacement'):
   self.assertEqual(r.read(r.HERE/f'{stage}-wire.schema.json'),r.projection(r.read(r.canonical(stage))))
   c.validate(r.probe_response(stage),stage)
 def test_validity_blinding_and_identical_family_bytes(self):
  for run in r.order('validity'):
   a=r.packet(run);b=r.packet({**run,'family':'B' if run['family']=='A' else 'A'})
   self.assertEqual(a,b);self.assertEqual(set(json.loads(a.split('\n\nCASE PACKET\n')[1])),{'case_id','source','target','mapping'})
 def test_admission_guards(self):
  a=self.admission();candidate=r.candidate('001');j={'A':self.validity(),'B':self.validity()};c.validate_admission(a,j,candidate)
  j['B']=self.validity('Conditional')
  with self.assertRaises(ValueError):c.validate_admission(a,j,candidate)
  condition={'family':'B','index':0,'text':j['B']['validity']['unresolved_conditions'][0],'designation':'instantiation','compatible':True,'rationale':'Measurement availability only.'}
  a.update(cohort='provisional',conditions=[condition],applicability_assumption={'conditions':[condition['text']],'scope':c.SCOPE});c.validate_admission(a,j,candidate)
  for designation in ('ontology','mixed','uncertain'):
   v=copy.deepcopy(a);v['conditions'][0]['designation']=designation
   with self.assertRaises(ValueError):c.validate_admission(v,j,candidate)
  v=copy.deepcopy(a);v['conditions'][0]['compatible']=False
  with self.assertRaises(ValueError):c.validate_admission(v,j,candidate)
  v=copy.deepcopy(a);v['applicability_assumption']['conditions']=['Change the practitioner baseline.']
  with self.assertRaises(ValueError):c.validate_admission(v,j,candidate)
  v=copy.deepcopy(a);v['applicability_assumption']['native_baseline']={}
  with self.assertRaises(c.jsonschema.ValidationError):c.validate_admission(v,j,candidate)
  j['A']=self.validity('Invalid')
  with self.assertRaises(ValueError):c.validate_admission(a,j,candidate)
 def test_viability_excludes_variants_and_provisional(self):
  manifest=r.manifest();admissions=[{'case_id':x['case_id'],'cohort':'primary'} for x in manifest]
  self.assertTrue(c.viability(admissions,manifest)['passes'])
  for a in admissions[:15]:a['cohort']='provisional'
  self.assertFalse(c.viability(admissions,manifest)['passes'])
 def test_displacement_packet_and_holdouts(self):
  original=r.read;row=r.manifest()[0];cid=row['case_id'];a={'case_id':cid,'cohort':'primary','applicability_assumption':None}
  def read(path):return {'cases':[a]} if Path(path).name=='admission.json' else original(path)
  with patch.object(r,'read',side_effect=read):
   p=r.packet({'case_id':cid},'displacement');v=json.loads(p.split('\n\nCASE PACKET\n')[1]);self.assertNotIn('applicability_assumption',v)
   self.assertIn((r.HERE/'baselines'/f"{row['target_id']}.json").read_bytes(),p.encode())
   a['cohort']='provisional';a['applicability_assumption']={'conditions':['Measurement exists.'],'scope':c.SCOPE}
   v=json.loads(r.packet({'case_id':cid},'displacement').split('\n\nCASE PACKET\n')[1]);self.assertTrue(v['provisional'])
   a['cohort']='holdout'
   with self.assertRaisesRegex(ValueError,'Holdout'):r.packet({'case_id':cid},'displacement')
 def test_metrics_known_ties_steps_and_missing(self):
  rows=[{'case_id':str(i),'target_id':'T','core':True} for i in range(4)]
  values={('0','A'):self.output('Native'),('0','B'):self.output('Native'),('1','A'):self.output('Native'),('1','B'):self.output('Adjacent',1),('2','A'):self.output('Remote',3),('2','B'):self.output('Native')}
  v=m.cohort(values,rows);self.assertEqual(v['same_class'],1);self.assertEqual(v['one_step'],1);self.assertEqual(v['native_remote'],1);self.assertEqual(v['observed_pairs'],3);self.assertEqual(v['missing_pair_ids'],['3'])
  self.assertEqual(v['dimensions']['entities']['mean_absolute_ordinal_disagreement'],4/3)
  self.assertEqual(v['ordering']['planned_unordered_pairs'],6);self.assertEqual(v['ordering']['observed_unordered_pairs'],3)
  self.assertEqual(v['ordering']['relations'][0]['A'],'=');self.assertEqual(v['ordering']['relations'][0]['B'],'<')
  self.assertEqual(v['ordering']['agreement']['agreements'],0)
 def test_empty_cohorts(self):
  v=m.cohort({},[]);self.assertIsNone(v['class_agreement']['rate']);self.assertIsNone(v['dimensions']['entities']['mean_absolute_ordinal_disagreement']);self.assertIsNone(v['ordering']['agreement']['rate'])
 def test_post_status_precedence(self):
  a=self.output();b=self.output('Adjacent');a['boundary_status']='borderline'
  self.assertEqual(m.post_result_status(a,b),'contested');b['class']='Native';self.assertEqual(m.post_result_status(a,b),'boundary');a['boundary_status']='clear';self.assertEqual(m.post_result_status(a,b),'consensus')
 def test_commands_isolation_and_schema(self):
  for stage in ('validity','displacement'):
   a=r.build_command('A','/tmp/empty',Path('/tmp/out'),'s',stage)
   for flag in ('--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check','shell_tool','plugins','apps','multi_agent'):self.assertIn(flag,a)
   self.assertIn(str(r.HERE/f'{stage}-wire.schema.json'),a)
   b=r.build_command('B','/tmp/empty',Path('/tmp/out'),'s',stage);self.assertEqual(b[b.index('--tools')+1],'');self.assertIn('--safe-mode',b)
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
  invalid=self.validity();invalid['validity']['final_status']='Invalid';events=self.events(invalid)
  class Process:
   returncode=0
   def communicate(self,*a,**k):pass
  def popen(*a,**k):k['stdout'].write('\n'.join(map(json.dumps,events))+'\n');k['stdout'].flush();return Process()
  with tempfile.TemporaryDirectory() as td,patch.object(r.subprocess,'Popen',side_effect=popen),patch.object(r.subprocess,'check_output',return_value=r.config()['expected_cli_versions']['B']),patch.object(r,'git',return_value=b'commit'),patch.object(r.uuid,'uuid4',return_value='s'):
   d=Path(td)/'attempt';result=r.execute('B',d,'fixture',{'case_id':'001'});self.assertEqual(result['status'],'failed');self.assertEqual(r.read(d/'response.json'),invalid)
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
