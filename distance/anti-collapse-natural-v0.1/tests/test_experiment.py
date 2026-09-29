import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import runner as r
import contracts as c


class Preparation(unittest.TestCase):
    def test_inputs_and_assignments(self): self.assertTrue(r.validate_inputs())
    def test_exact_baselines(self):
        for p in (HERE / 'baselines').glob('*.json'): self.assertEqual(p.read_bytes(), (r.OLD / 'baselines' / p.name).read_bytes())
    def test_frozen_classifiers(self):
        for name in ('CLASSIFIER.md', 'CLASSIFIER-validity.md'): self.assertEqual((HERE / name).read_bytes(), (r.OLD / name).read_bytes())
    def test_frozen_response_contracts(self):
        for name in ('validity', 'output', 'validity-wire', 'anti-collapse-wire'): self.assertEqual((HERE / 'schemas' / (name + '.schema.json')).read_bytes(), (r.OLD / 'schemas' / (name + '.schema.json')).read_bytes())
    def test_generator_has_no_gate_terms(self):
        for row in r.manifest(): self.assertFalse(r.wording_hits(r.packet('generation', row['case_id']), (*c.STATUSES, 'anti-collapse', 'ladder', 'novelty', 'diversity')))
    def test_no_operator_labels(self):
        for row in r.manifest(): self.assertEqual(set(row), {'case_id','target_id','source_path','source_sha256','generator_family','neutralizer_family'})
    def test_every_source_crosses_families(self):
        for src in {x['source_path'] for x in r.manifest()}: self.assertEqual({x['generator_family'] for x in r.manifest() if x['source_path'] == src}, {'A','B'})
    def test_no_synthetic_facts(self):
        cid = r.manifest()[0]['case_id']
        with patch.object(r, 'single', return_value={'mapping': {k:'Fixture.' for k in ('state','operation','signal','inference','limit')}}): self.assertEqual(r.candidate(cid)['target']['evidence'], [])
    def test_freeze_required_before_next_stage(self):
        with patch.object(r,'verify'), patch.object(r,'checkpoint', side_effect=ValueError('Uncommitted upstream')), patch.object(r,'_write_stage_inputs') as write:
            with self.assertRaises(ValueError): r.prepare_stage('neutralization')
            write.assert_not_called()
    def test_generation_requires_committed_preparation(self):
        with patch.object(r,'verify_stage_inputs',side_effect=ValueError('Uncommitted baseline')), patch.object(r,'execute') as execute:
            with self.assertRaises(ValueError): r.preflight('generation')
            execute.assert_not_called()
    def test_upstream_hash_changed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'fixture';p.write_text('changed')
            with patch.object(r,'ROOT',Path(tmp)):
                with self.assertRaises(ValueError):r.verify_inventory({'fixture':r.sha(b'original')})
    def test_historical_preservation(self):
        if (HERE/'preservation.json').exists(): r.preservation(True)


class Contracts(unittest.TestCase):
    def test_all_probe_schemas(self):
        for stage in r.STAGES: r.validate_response(r.probe_response(stage),stage)
    def test_all_fields_required(self):
        for stage in ('generation','neutralization','audit'):
            v=r.probe_response(stage)
            for field in v:
                bad=copy.deepcopy(v);del bad[field]
                with self.assertRaises(Exception):r.validate_response(bad,stage)
    def test_only_three_statuses(self):
        for status in (*c.STATUSES,'Remote','Novel'):
            v=r.probe_response('anti-collapse');v['anti_collapse']['status']=status
            if status in c.STATUSES:r.validate_response(v,'anti-collapse')
            else:
                with self.assertRaises(Exception):r.validate_response(v,'anti-collapse')
    def test_no_scores_rankings_or_usefulness(self):
        for stage in r.STAGES:
            for key in ('novelty_score','ranking','diversity','usefulness'):
                v=r.probe_response(stage);v[key]=1
                with self.assertRaises(Exception):r.validate_response(v,stage)
    def test_generation_self_labels(self):
        for phrase in r.SELF_LABELS:
            v=r.probe_response('generation');v['explanation']['operational_chain']='This is '+phrase+'.'
            with self.assertRaises(ValueError):r.validate_response(v,'generation')
    def test_operational_new_is_not_self_label(self):
        v=r.probe_response('generation');v['mapping']['signal']='A new measurement differs from the preceding measurement.';r.validate_response(v,'generation')
    def test_neutralizer_wording_ban(self):
        for phrase in r.BANNED:
            v=r.probe_response('neutralization');v['source_neutral']['procedure']=phrase.upper()
            with self.assertRaises(ValueError):r.validate_response(v,'neutralization')
    def test_word_boundaries_and_hyphens(self):
        self.assertFalse(r.wording_hits('A nativeish label; a novelist.',r.BANNED))
        self.assertTrue(r.wording_hits('a NON–NATIVE procedure',r.BANNED))
        self.assertTrue(r.wording_hits('adds\nno   warrant',r.BANNED))
    def test_neutralizer_packet_blind(self):
        cid=r.manifest()[0]['case_id']
        with patch.object(r,'single',return_value={'mapping':{'operation':'Count items.'}}):body=r.packet_body('neutralization',cid)
        self.assertEqual(set(body),{'case_id','target_question','mapping'})
        self.assertNotIn('native_baseline',body);self.assertNotIn('source',body)
    def test_auditor_packet_blind(self):
        cid=r.manifest()[0]['case_id']
        with patch.object(r,'single',side_effect=lambda s,cid:{'mapping':{'operation':'Count items.'}} if s=='generation' else {'source_neutral':{'action':'Count items.'}}):body=r.packet_body('audit',cid)
        self.assertEqual(set(body),{'case_id','target_question','mapping','source_neutral'})
    def test_anti_collapse_packet_allowlist(self):
        cid=r.manifest()[0]['case_id'];value=r.probe_response('neutralization')
        with patch.object(r,'single',return_value=value):
            body=r.packet_body('anti-collapse',cid);text=r.packet('anti-collapse',cid)
        self.assertEqual(set(body),{'case_id','target','native_baseline','source_neutral'})
        for key in ('source','mapping','generator_family','neutralizer_family','validity','review_labels'):self.assertNotIn(key,body)
        self.assertIn((HERE/'baselines'/ (r.row(cid)['target_id']+'.json')).read_text(),text)
    def test_audit_operation_signal_inference_limit_checks(self):
        for field in ('operation_preserved','signal_preserved','inference_preserved','limit_preserved','stopping_condition_preserved','next_inquiry_preserved','no_added_operational_content'):
            v=r.probe_response('audit');v['checks'][field]={'status':'fail','original_evidence':['Stop after three measurements.'],'neutral_evidence':['Continue measuring.'],'rationale':'The binding condition was changed.'}
            with self.assertRaises(ValueError):r.validate_response(v,'audit')
            v['overall']='exclude';r.validate_response(v,'audit')
    def test_uncertain_audit_excluded(self):
        v=r.probe_response('audit');v['checks']['inference_preserved']['status']='uncertain';v['overall']='exclude';r.validate_response(v,'audit')
    def test_status_contradictions_unchanged(self):
        v=r.probe_response('anti-collapse');v['anti_collapse']['status']='CLEAR_COLLAPSE';v['anti_collapse']['materiality']['status']='material'
        with self.assertRaises(Exception):r.validate_response(v,'anti-collapse')
    def test_single_locus_sufficient(self):
        for locus in c.LOCI:
            v=r.probe_response('anti-collapse');v['anti_collapse']['status']='SUFFICIENT_DEPARTURE'
            for k,item in v['anti_collapse']['departures'].items():item['status']='present' if k==locus else 'absent'
            r.validate_response(v,'anti-collapse')
    def test_duplicate_json_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bad.json';p.write_text('{"x":1,"x":2}')
            with self.assertRaises(ValueError):r.read(p)


class Admission(unittest.TestCase):
    def inputs(self):
        ids={x['case_id'] for x in r.manifest()};audits={(cid,f):{'overall':'pass'} for cid in ids for f in 'AB'};validity={(cid,f):r.probe_response('validity') for cid in ids for f in 'AB'}
        return ids,audits,validity
    def derive(self,ids,audits,validity):
        with patch.object(r,'successful_ids',return_value=ids),patch.object(r,'published',side_effect=lambda s:audits if s=='audit' else validity):return r.derive_admission()
    def test_valid_valid_required(self):
        for status in ('Conditional','Invalid'):
            for family in 'AB':
                ids,a,v=self.inputs();cid=sorted(ids)[0];v[(cid,family)]['validity']['final_status']=status
                self.assertFalse(next(x for x in self.derive(ids,a,v) if x['case_id']==cid)['admitted'])
    def test_both_audits_required(self):
        ids,a,v=self.inputs();cid=sorted(ids)[0];a[(cid,'B')]['overall']='exclude'
        result=next(x for x in self.derive(ids,a,v) if x['case_id']==cid)
        self.assertTrue(result['valid_valid']);self.assertFalse(result['admitted'])
    def test_minimum_cases(self):
        rows=[{'admitted':True,'target_id':f'T{i%6}'} for i in range(17)];self.assertFalse(r.viability(rows)['viable'])
        rows.append({'admitted':True,'target_id':'T0'});self.assertTrue(r.viability(rows)['viable'])
    def test_minimum_targets(self):
        self.assertFalse(r.viability([{'admitted':True,'target_id':f'T{i%4}'} for i in range(30)])['viable'])
    def test_schedule_filter_no_replacement(self):
        full=[{'case_id':'b'},{'case_id':'a'},{'case_id':'c'}]
        with patch.object(r,'planned',return_value=full),patch.object(r,'successful_ids',return_value={'a','c'}):self.assertEqual(r.order('neutralization'),full[1:])
    def test_empty_rate_null(self):self.assertIsNone(r.fraction(0,0)['fraction'])
    def test_missing_judgment_rejected(self):
        ids,a,v=self.inputs()
        with patch.object(r,'successful_ids',return_value=ids),patch.object(r,'published',side_effect=lambda s:a if s=='audit' else v if s=='validity' else {}),patch.object(Path,'exists',return_value=True):
            with self.assertRaises(ValueError):r.compute_metrics()
    def test_analyze_requires_result_commit(self):
        with patch.object(r,'verify_admission',return_value={'viability':{'viable':True}}),patch.object(r,'checkpoint',side_effect=ValueError('Uncommitted result')),patch.object(r,'write_new') as write:
            with self.assertRaises(ValueError):r.analyze()
            write.assert_not_called()


class Execution(unittest.TestCase):
    def test_isolation_flags(self):
        for stage in r.STAGES:
            for f in 'AB':
                cmd=r.build_command(f,Path('/tmp/empty'),Path('/tmp/output'),'session',stage)
                for flag in (['--ephemeral','--ignore-user-config','--ignore-rules','--sandbox','--output-schema'] if f=='A' else ['--safe-mode','--strict-mcp-config','--tools','--no-session-persistence','--disable-slash-commands']):self.assertIn(flag,cmd)
                self.assertIn(r.config()['families'][f]['requested_model'],cmd)
    def test_environment_clean(self):
        with patch.dict(os.environ,{'CODEX_THREAD_ID':'old','OPENAI_MODEL':'wrong','CLAUDECODE':'parent'}):self.assertFalse(any(k in r.clean_environment() for k in ('CODEX_THREAD_ID','OPENAI_MODEL','CLAUDECODE')))
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'x';r.write_new(p,{'first':1})
            with self.assertRaises(FileExistsError):r.write_new(p,{'second':2})
    def test_duplicate_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);r.write_new(p/'old/validation.json',{'metadata':{'session_id':'same'}})
            with patch.object(r,'RUNTIME',p):
                with self.assertRaises(ValueError):r.check_fresh_session('same',p/'new')
    def schedule(self,status):
        with tempfile.TemporaryDirectory() as tmp:
            runs=[{'id':'first','case_id':'E001','family':'A'},{'id':'second','case_id':'E002','family':'B'}]
            with patch.object(r,'RUNTIME',Path(tmp)),patch.object(r,'prerequisites'),patch.object(r,'order',return_value=runs),patch.object(r,'packet',return_value='fixture'),patch.object(r,'git',return_value=b'commit'),patch.object(r,'execute',return_value={'status':status}) as execute:
                if status=='failed':
                    with self.assertRaises(ValueError):r.run_all('generation')
                    self.assertEqual(execute.call_count,1);self.assertTrue((Path(tmp)/'STOP.json').exists())
                else:r.run_all('generation');self.assertEqual(execute.call_count,2)
    def test_content_exclusion_continues(self):self.schedule('excluded')
    def test_fatal_failure_stops(self):self.schedule('failed')
    def fake_execute(self,stage,raw,timeout=False):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)/'attempt';process=Mock();process.pid=123;process.returncode=0
            if timeout:process.communicate.side_effect=subprocess.TimeoutExpired('fake',1)
            def launch(*args,**kwargs):
                for event in [{'type':'thread.started','thread_id':'fresh'},{'type':'item.completed','item':{'type':'agent_message','text':raw}},{'type':'turn.completed'}]:kwargs['stdout'].write(json.dumps(event)+'\n')
                (directory/'response.json').write_text(raw);return process
            with patch.object(r.subprocess,'Popen',side_effect=launch),patch.object(r.subprocess,'check_output',return_value=r.config()['expected_cli_versions']['A']),patch.object(r,'git',return_value=b'commit'),patch.object(r,'check_fresh_session'),patch.object(r.os,'killpg'):
                result=r.execute('A',directory,'fixture',stage,{'case_id':'E001'})
            self.assertEqual((directory/'response.json').read_text(),raw)
            self.assertTrue((directory/'events.jsonl').exists());return result
    def test_generation_malformed_retained_excluded(self):self.assertEqual(self.fake_execute('generation','not JSON')['status'],'excluded')
    def test_neutralization_malformed_retained_excluded(self):self.assertEqual(self.fake_execute('neutralization','not JSON')['status'],'excluded')
    def test_judge_malformed_fatal(self):
        for stage in ('audit','validity','anti-collapse'):self.assertEqual(self.fake_execute(stage,'not JSON')['status'],'failed')
    def test_timeout_fatal_even_generation(self):self.assertEqual(self.fake_execute('generation','partial',timeout=True)['status'],'failed')
    def test_models_and_tools_rejected(self):
        base=[{'type':'thread.started','thread_id':'new'},{'type':'item.completed','item':{'type':'agent_message','text':'{}'}},{'type':'turn.completed'}]
        for extra in ({'type':'item.completed','item':{'type':'command_execution'}},{'type':'metadata','model':'other'},{'type':'system','subtype':'model_fallback'}):
            with self.assertRaises(ValueError):r.legacy.audit_events(base+[extra],'A','gpt-6-astra')


if __name__=='__main__':unittest.main()
