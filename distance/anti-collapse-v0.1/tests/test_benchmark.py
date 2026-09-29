import copy, importlib.util, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch, Mock
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE))
import contracts as c
import runner as r
import metrics
from build_schemas import projection

class Contracts(unittest.TestCase):
 def value(self,status='BORDERLINE_KEEP'):
  v=r.probe_response('anti-collapse');v['case_id']='test';v['anti_collapse']['status']=status;return v
 def test_all_three_statuses(self):
  for s in c.STATUSES:c.validate(self.value(s),'anti-collapse')
 def test_unknown_status(self):
  with self.assertRaises(Exception):c.validate(self.value('Remote'),'anti-collapse')
 def test_every_departure_required(self):
  for field in c.LOCI:
   v=self.value();del v['anti_collapse']['departures'][field]
   with self.assertRaises(Exception):c.validate(v,'anti-collapse')
 def test_formalization_and_native_reduction_required(self):
  for field in ('formalization','native_reduction'):
   v=self.value();del v['anti_collapse'][field]
   with self.assertRaises(Exception):c.validate(v,'anti-collapse')
 def test_no_scoring_usefulness_or_redundancy(self):
  for field in ('novelty_score','distance','usefulness','redundancy','accuracy'):
   v=self.value();v['anti_collapse'][field]=1
   with self.assertRaises(Exception):c.validate(v,'anti-collapse')
 def test_definite_contradictions(self):
  for status,field,key,val in [('CLEAR_COLLAPSE','materiality','status','material'),('CLEAR_COLLAPSE','native_reduction','collapses_without_loss','no'),('SUFFICIENT_DEPARTURE','materiality','status','immaterial'),('SUFFICIENT_DEPARTURE','native_reduction','collapses_without_loss','yes')]:
   v=self.value(status);v['anti_collapse'][field][key]=val
   with self.assertRaises(Exception):c.validate(v,'anti-collapse')
 def test_all_absent_cannot_be_sufficient(self):
  v=self.value('SUFFICIENT_DEPARTURE')
  for x in v['anti_collapse']['departures'].values():x['status']='absent'
  with self.assertRaises(Exception):c.validate(v,'anti-collapse')
 def test_one_departure_enough(self):
  for field in c.LOCI:
   v=self.value('SUFFICIENT_DEPARTURE')
   for key,x in v['anti_collapse']['departures'].items():x['status']='present' if key==field else 'absent'
   c.validate(v,'anti-collapse')
 def test_reasoned_uncertainty_not_forced(self):
  for s in c.STATUSES:c.validate(self.value(s),'anti-collapse')
 def test_no_blank_rationale(self):
  v=self.value();v['anti_collapse']['decisive_reason']=' '
  with self.assertRaises(Exception):c.validate(v,'anti-collapse')
 def test_response_identity(self):
  with self.assertRaises(ValueError):c.validate(self.value(),'anti-collapse',{'case_id':'different'})
 def test_duplicate_and_nonfinite_json(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x.json'
   for text in ('{"x":1,"x":2}','{"x":NaN}'):
    p.write_text(text)
    with self.assertRaises(ValueError):c.read(p)
 def test_wire_projects_only_constraints(self):
  for stage in r.STAGES:self.assertEqual(c.read(HERE/'schemas'/f'{stage}-wire.schema.json'),projection(c.read(r.canonical(stage))))
 def test_validity_classifier_schema_unchanged(self):
  self.assertEqual((HERE/'CLASSIFIER-validity.md').read_bytes(),(HERE.parent/'v0.3/CLASSIFIER-transfer-validity.md').read_bytes())
  self.assertEqual((HERE/'schemas/validity.schema.json').read_bytes(),(HERE.parent/'v0.3/validity.schema.json').read_bytes())

class Corpus(unittest.TestCase):
 def test_all_input_audits(self):self.assertTrue(r.validate_inputs())
 def test_allowlisted_packets(self):
  for row in r.manifest():
   body=r.packet_body(r.packet(row,'anti-collapse'))
   self.assertEqual(set(body),{'case_id','target','native_baseline','source_neutral'})
   for forbidden in ('design_metadata','ladder_level','intended_departure_type','adversary_tags','source','mapping','design_intention'):
    self.assertNotIn('"'+forbidden+'"',json.dumps(body))
 def test_no_source_framed_prefix_or_name(self):
  audit={a['case_id']:a for a in c.read(HERE/'neutralization-audit.json')['cases']}
  for row in r.manifest():
   text=json.dumps(r.packet_body(r.packet(row,'anti-collapse')))
   self.assertNotIn(r.candidate(row['case_id'])['source']['name'],text)
   self.assertNotIn(audit[row['case_id']]['removed_framing'],text)
 def test_neutralization_required(self):
  body=r.packet_body(r.packet(r.manifest()[0],'anti-collapse'));del body['source_neutral']
  with self.assertRaises(Exception):c.validate(body,'packet')
 def test_neutral_fields_required(self):
  value=c.read(HERE/'neutralizations/N001.json')
  for key in value:
   v=copy.deepcopy(value);del v[key]
   with self.assertRaises(Exception):c.validate(v,'neutralization')
 def test_baseline_bytes_and_shared_context(self):
  for tid in {x['target_id'] for x in r.manifest()}:
   rows=[x for x in r.manifest() if x['target_id']==tid];base=(HERE/'baselines'/f'{tid}.json').read_bytes();contexts=[]
   for row in rows:
    text=r.packet(row,'anti-collapse');self.assertIn(base,text.encode());contexts.append(r.packet_body(text)['target'])
   self.assertTrue(all(x==contexts[0] for x in contexts))
 def test_baselines_not_narrowed(self):
  for p in (HERE/'baselines').glob('*.json'):
   old=c.read(HERE.parent/'comparative-displacement-v0.3/baselines'/p.name);new=c.read(p)
   self.assertEqual({k:new[k] for k in old},old)
 def test_coverage_requires_all_levels(self):
  rows=copy.deepcopy(r.manifest());rows[0]['ladder_level']='D'
  with self.assertRaises(ValueError):r.design_coverage(rows)
 def test_coverage_requires_five_C_loci(self):
  rows=copy.deepcopy(r.manifest())
  for row in rows:
   if row['ladder_level']=='C':row['intended_departure_type']='action'
  with self.assertRaises(ValueError):r.design_coverage(rows)
 def test_adversaries_required(self):
  for tag in ('exotic-collapse','mundane-positive'):
   rows=copy.deepcopy(r.manifest())
   for row in rows:row['adversary_tags']=[x for x in row['adversary_tags'] if x!=tag]
   with self.assertRaises(ValueError):r.design_coverage(rows)
 def test_historical_files_unchanged(self):r.preservation(True)

class AdmissionMetrics(unittest.TestCase):
 def validity(self):
  out={}
  for row in r.manifest():
   for f in 'AB':v=r.probe_response();v['case_id']=row['case_id'];out[(row['case_id'],f)]=v
  return out
 def measurements(self):
  out={}
  for row in r.manifest():
   for f in 'AB':v=r.probe_response('anti-collapse');v['case_id']=row['case_id'];out[(row['case_id'],f)]=v
  return out
 def test_only_valid_valid(self):
  for status in ('Conditional','Invalid'):
   for family in 'AB':
    v=self.validity();v[('N001',family)]['validity']['final_status']=status
    rows=r.admission_rows(v);self.assertFalse(next(x for x in rows if x['case_id']=='N001')['admitted'])
 def test_unresolved_conditions_excluded(self):
  v=self.validity();v[('N001','A')]['validity']['unresolved_conditions']=['Unresolved']
  self.assertFalse(next(x for x in r.admission_rows(v) if x['case_id']=='N001')['admitted'])
 def test_viability_and_single_locus_attrition(self):
  rows=r.admission_rows(self.validity());self.assertTrue(r.viability(rows)['viable'])
  action=next(x['case_id'] for x in r.manifest() if x['ladder_level']=='C' and x['intended_departure_type']=='action')
  next(x for x in rows if x['case_id']==action)['admitted']=False
  self.assertFalse(r.viability(rows)['viable'])
 def test_case_and_ladder_attrition(self):
  rows=r.admission_rows(self.validity())
  for x in rows:
   if x['target_id'] in ('T01','T02'):x['admitted']=False
  v=r.viability(rows);self.assertFalse(v['checks']['at_least_18_cases']);self.assertFalse(v['checks']['at_least_5_targets'])
 def test_known_agreement_arithmetic(self):
  values=self.measurements();values[('N001','A')]['anti_collapse']['status']='CLEAR_COLLAPSE'
  m=metrics.compute(values,r.manifest(),r.admission_rows(self.validity()))
  self.assertEqual(m['status_agreement']['numerator'],23)
  self.assertEqual(m['status_agreement']['denominator'],24)
  self.assertEqual(m['per_status_agreement']['CLEAR_COLLAPSE']['joint_calls_over_either_calls'],metrics.fraction(0,1))
  self.assertIsNone(m['per_status_agreement']['SUFFICIENT_DEPARTURE']['joint_calls_over_either_calls']['fraction'])
 def test_missing_measurement_does_not_shrink_denominator(self):
  values=self.measurements();del values[('N001','A')]
  with self.assertRaises(ValueError):metrics.compute(values,r.manifest(),r.admission_rows(self.validity()))
 def test_excluded_case_cannot_enter_metrics(self):
  rows=r.admission_rows(self.validity());rows[0]['admitted']=False
  with self.assertRaises(ValueError):metrics.compute(self.measurements(),r.manifest(),rows)
 def test_intention_not_truth(self):
  v=self.measurements();rows=r.manifest();a=r.admission_rows(self.validity());m=metrics.compute(v,rows,a)
  altered=copy.deepcopy(rows)
  for row in altered:row['design_intention']='the opposite of everything'
  self.assertEqual(m,metrics.compute(v,altered,a));self.assertFalse(m['interpretation']['accuracy_computed'])
 def test_detect_suppression_and_ladder_pathology(self):
  v=self.measurements();rows=r.manifest();target='T01'
  cidA=next(x['case_id'] for x in rows if x['target_id']==target and x['ladder_level']=='A');cidC=next(x['case_id'] for x in rows if x['target_id']==target and x['ladder_level']=='C')
  for f in 'AB':v[(cidA,f)]['anti_collapse']['status']='SUFFICIENT_DEPARTURE';v[(cidC,f)]['anti_collapse']['status']='CLEAR_COLLAPSE'
  m=metrics.compute(v,rows,r.admission_rows(self.validity()));self.assertIn(cidC,[x['case_id'] for x in m['CD_design_suppression_cases']]);self.assertEqual(len(next(x for x in m['matched_ladders'] if x['target_id']==target)['strong_A_departure_CD_collapse']),2)
 def test_frozen_schedule_filter_preserves_order(self):
  schedule=[{'case_id':'b'},{'case_id':'a'},{'case_id':'c'}]
  with patch.object(r,'planned',return_value=schedule),patch.object(r,'read',return_value={'cases':[{'case_id':'a','admitted':True},{'case_id':'c','admitted':True}]}):self.assertEqual(r.order('anti-collapse'),schedule[1:])

class Execution(unittest.TestCase):
 def test_isolation_commands(self):
  for f in 'AB':
   cmd=r.build_command(f,Path('/tmp/empty'),Path('/tmp/results'),'session','anti-collapse');s=' '.join(cmd)
   self.assertIn(r.config()['families'][f]['requested_model'],cmd)
   for flag in (['--ephemeral','--ignore-user-config','--ignore-rules','--sandbox','--output-schema'] if f=='A' else ['--safe-mode','--strict-mcp-config','--no-session-persistence','--tools','--disable-slash-commands']):self.assertIn(flag,cmd)
   self.assertIn('anti-collapse',s) if f=='A' else self.assertIn('BORDERLINE_KEEP',s)
 def test_environment_filter(self):
  with patch.dict(os.environ,{'OPENAI_MODEL':'wrong','CLAUDECODE':'parent','CODEX_THREAD_ID':'parent','PATH':'/bin'}):
   env=r.clean_environment();self.assertFalse(any(k.startswith(('OPENAI_','CODEX_','CLAUDE_')) or k=='CLAUDECODE' for k in env));self.assertEqual(env['PATH'],'/bin')
 def test_exclusive_artifacts(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'x.json';r.write_new(p,{'a':1})
   with self.assertRaises(FileExistsError):r.write_new(p,{'a':2})
   self.assertEqual(c.read(p),{'a':1})
 def test_setup_failure_preserved_no_retry(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'attempt'
   with patch.object(r,'adapter_execute',side_effect=RuntimeError('setup failure')):v=r.execute('A',p,'original')
   self.assertEqual(v['status'],'failed');self.assertEqual((p/'prompt.txt').read_text(),'original')
   with self.assertRaises(ValueError):r.execute('A',p,'replacement')
 def test_scheduler_stops(self):
  with tempfile.TemporaryDirectory() as tmp:
   runs=[{'id':'first','case_id':'N001','family':'A'},{'id':'second','case_id':'N002','family':'B'}]
   with patch.object(r,'RUNTIME',Path(tmp)),patch.object(r,'prerequisites'),patch.object(r,'order',return_value=runs),patch.object(r,'execute',return_value={'status':'failed','error':'bad'}) as execute,patch.object(r,'git',return_value=b'commit'):
    with self.assertRaises(ValueError):r.run_all('validity')
    self.assertEqual(execute.call_count,1);self.assertTrue((Path(tmp)/'STOP.json').exists())
 def test_timeout_preserves_stream_and_partial_response(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp)/'attempt';process=Mock();process.pid=123;process.communicate.side_effect=subprocess.TimeoutExpired('fake',1)
   def launch(*args,**kwargs):
    kwargs['stdout'].write('{"partial":"retained"}\n');(d/'response.json').write_text('{"partial":');return process
   with patch.object(r.subprocess,'Popen',side_effect=launch),patch.object(r.subprocess,'check_output',return_value='codex-cli 0.157.1'),patch.object(r,'git',return_value=b'commit'),patch.object(r.os,'killpg') as kill:
    result=r.execute('A',d,'prompt',{'case_id':'N001'},'validity')
   self.assertEqual(result['status'],'failed');self.assertIn('partial',(d/'events.jsonl').read_text());self.assertEqual((d/'response.json').read_text(),'{"partial":');kill.assert_called_once()
 def test_malformed_output_preserved(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp)/'attempt';process=Mock();process.returncode=0
   def launch(*args,**kwargs):
    kwargs['stdout'].write('not JSON\n');(d/'response.json').write_text('not JSON');return process
   with patch.object(r.subprocess,'Popen',side_effect=launch),patch.object(r.subprocess,'check_output',return_value='codex-cli 0.157.1'),patch.object(r,'git',return_value=b'commit'):
    result=r.execute('A',d,'prompt',{'case_id':'N001'},'validity')
   self.assertEqual(result['status'],'failed');self.assertEqual((d/'response.json').read_text(),'not JSON')
 def test_duplicate_session(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);r.write_new(p/'old/validation.json',{'metadata':{'session_id':'same'}})
   with patch.object(r,'RUNTIME',p):
    with self.assertRaises(ValueError):r.check_fresh_session('same',p/'new')
 def test_tool_and_model_fallback_rejected(self):
  base=[{'type':'thread.started','thread_id':'new'},{'type':'item.completed','item':{'type':'agent_message','text':'{}'}},{'type':'turn.completed','usage':{}}]
  for extra in ({'type':'item.completed','item':{'type':'command_execution'}},{'type':'metadata','model':'other'},{'type':'system','subtype':'model_fallback'}):
   with self.assertRaises(ValueError):r.legacy.audit_events(base+[extra],'A','gpt-6-astra')

if __name__=='__main__':unittest.main()
