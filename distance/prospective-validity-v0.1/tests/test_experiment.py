import copy
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
import contracts as c
import runner as r
import prepare as prep

class InventoryTests(unittest.TestCase):
    def test_exact_imports_and_all_parent_atomic_coverage(self): self.assertEqual(r.verify_imports(),196)
    def test_exact_source_spans_and_operator_decomposition(self):
        parents=c.read(HERE/'condition-inventory/parents.json'); atoms=c.read(HERE/'condition-inventory/atomic.json')
        for p in parents:
            expected=prep.SPLITS.get(p['extraction_key'],[p['verbatim_condition']])
            actual=[a['atomic_text'] for a in atoms if a['parent_condition_id']==p['parent_condition_id']]
            self.assertEqual(actual,expected)
    def test_sources_committed_at_base(self):
        for row in c.read(HERE/'operator-manifest.json')['cases']:
            for key in ('generation','input'):
                source=row[key]
                self.assertEqual(c.digest(r.git('show',source['source_commit']+':'+source['path'])),source['sha256'])
    def test_semantic_exclusion_preserves_domain_wording(self):
        for p in (HERE/'packets/taxonomy').glob('*.txt'):
            body=json.loads(p.read_text().split('\nCASE PACKET\n')[1])
            self.assertEqual(set(body),{'source','target','mapping','condition_id','atomic_condition','necessary_source_excerpt'})
            self.assertEqual(set(body['mapping']),{'state','operation','signal','inference','limit'})
            self.assertEqual(set(body['source']),{'name','practice','instrument'})
            self.assertNotIn('CLEAR_COLLAPSE',p.read_text())
            self.assertNotIn('SUFFICIENT_DEPARTURE',p.read_text())
            self.assertNotIn('BORDERLINE_KEEP',p.read_text())
        self.assertIn('novelty effects',json.dumps(c.read(HERE/'imports/candidates/E029.json')))
    def test_no_categories_or_explicit_criterion_invented(self):
        for p in c.read(HERE/'condition-inventory/parents.json'): self.assertIsNone(p['original_criterion'])
        for p in c.read(HERE/'condition-inventory/atomic.json'): self.assertNotIn('category',p)
    def test_fidelity_pass_unchanged(self):
        rows=c.read(HERE/'operator-manifest.json')['cases']
        self.assertEqual(sum(x['fidelity_pass'] for x in rows),23)
    def test_independent_random_order_reconstructs(self):
        import random
        ids=[x['atomic_condition_id'] for x in c.read(HERE/'condition-inventory/atomic.json')]
        random.Random(20260930072).shuffle(ids)
        self.assertEqual(r.order('taxonomy'),ids)

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        root=Path(self.temp.name); (root/'schemas').mkdir()
        for stage in ('taxonomy','prospective'):
            (root/'schemas'/f'{stage}.schema.json').write_text(json.dumps(c.schema(stage)))
        self.patcher=patch.object(c,'HERE',root); self.patcher.start(); self.addCleanup(self.patcher.stop)
    def test_probes_use_only_artificial_identity(self):
        for s in ('taxonomy','prospective'): c.validate(r.probe_fixture(s),s,'ARTIFICIAL')
    def test_valid_procedure_with_unmet_execution_prerequisites(self):
        v=r.probe_fixture('prospective'); c.validate(v,'prospective','ARTIFICIAL')
        self.assertEqual(v['final_status'],'Valid')
    def test_unsupported_warrant_invalid_despite_execution(self):
        v=r.probe_fixture('prospective'); v['warrant_validity']={'status':'unsupported','rationale':'Counting blue tokens does not establish their maker; access cannot supply that bridge.'}; v['final_status']='Invalid'
        c.validate(v,'prospective','ARTIFICIAL')
        v['final_status']='Valid'
        with self.assertRaises(Exception): c.validate(v,'prospective','ARTIFICIAL')
    def test_conditional_empirical_relation(self):
        v=r.probe_fixture('prospective'); v['warrant_validity']={'status':'conditional','rationale':'The mapping explicitly requires a separately checkable calibration relation to infer volume from height.'}; v['final_status']='Conditional'
        v['conditions'].append({'condition':'Specified calibration relates height to volume.','category':'warrant_condition','rationale':'A named relation in the mapping supplies the inference if established.','effect_on_validity':'conditional'})
        c.validate(v,'prospective','ARTIFICIAL')
    def test_failure_precedes_conditional(self):
        v=r.probe_fixture('prospective'); v['warrant_validity']['status']='unsupported'; v['target_fidelity']['status']='conditional'; v['final_status']='Invalid'
        v['conditions'].append({'condition':'The counted objects must be the requested population.','category':'target_fidelity_condition','rationale':'The relationship is unresolved.','effect_on_validity':'conditional'})
        c.validate(v,'prospective','ARTIFICIAL')
    def test_execution_cannot_make_conditional(self):
        v=r.probe_fixture('prospective'); v['final_status']='Conditional'
        with self.assertRaises(Exception): c.validate(v,'prospective','ARTIFICIAL')
    def test_execution_effect_cannot_change_validity(self):
        v=r.probe_fixture('prospective'); v['conditions'][0]['effect_on_validity']='conditional'
        with self.assertRaises(Exception): c.validate(v,'prospective','ARTIFICIAL')
    def test_ready_forbids_unmet_prerequisites(self):
        for status in ('ready','unknown'):
            v=r.probe_fixture('prospective'); v['execution_readiness']['status']=status
            with self.assertRaises(Exception): c.validate(v,'prospective','ARTIFICIAL')
    def test_requires_preconditions_requires_both_lists(self):
        v=r.probe_fixture('prospective'); v['execution_readiness']['preconditions']=[]
        with self.assertRaises(Exception): c.validate(v,'prospective','ARTIFICIAL')
    def test_ready_and_unknown_valid(self):
        for status in ('ready','unknown'):
            v=r.probe_fixture('prospective'); v['conditions']=[]; v['execution_readiness']['preconditions']=[]; v['execution_readiness']['status']=status
            c.validate(v,'prospective','ARTIFICIAL')
    def test_conditional_needs_substantive_condition(self):
        v=r.probe_fixture('prospective'); v['warrant_validity']['status']='conditional'; v['final_status']='Conditional'
        with self.assertRaises(Exception): c.validate(v,'prospective','ARTIFICIAL')
    def test_no_extra_fields_or_categories(self):
        v=r.probe_fixture('taxonomy'); v['category']='other'
        with self.assertRaises(Exception): c.validate(v,'taxonomy','ARTIFICIAL')
        v=r.probe_fixture('prospective'); v['novelty']=True
        with self.assertRaises(Exception): c.validate(v,'prospective','ARTIFICIAL')
    def test_link_consistency(self):
        v=r.probe_fixture('taxonomy'); v.update(category='warrant_condition',if_execution=None,if_validity_relevant={'affected_link':'inference_target'})
        with self.assertRaises(Exception): c.validate(v,'taxonomy','ARTIFICIAL')
    def test_wire_projection_preserves_fields(self):
        for s in ('taxonomy','prospective'):
            x=c.schema(s); w=c.wire(x)
            self.assertEqual(x['required'],w['required']); self.assertNotIn('allOf',w)
            c.jsonschema.Draft202012Validator.check_schema(w)
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError): json.loads('{"a":1,"a":2}',object_pairs_hook=c.unique)

class IsolationTests(unittest.TestCase):
    def test_pinned_model_high_and_forbidden_capabilities(self):
        cmd=r.command('/tmp/empty',Path('/tmp/output'),'taxonomy')
        for arg in ('--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check','model_reasoning_effort="high"','project_doc_max_bytes=0','web_search="disabled"'): self.assertIn(arg,cmd)
        self.assertEqual(cmd[cmd.index('--model')+1],'gpt-6-astra'); self.assertEqual(cmd[-1],'-')
        for feature in ('apps','plugins','memories','multi_agent','shell_tool','unified_exec','browser_use','computer_use','image_generation','view_image','hooks','skill_search'):
            self.assertIn(feature,cmd)
        self.assertEqual(r.config()['timeout_seconds'],900); self.assertEqual(r.config()['probe_limit_per_stage'],1)
        self.assertEqual(r.config()['max_concurrent_processes'],1); self.assertEqual(r.config()['harness_retries'],0)
    def test_environment_removes_parent_provider_overrides(self):
        with patch.dict(os.environ,{'CODEX_THREAD_ID':'parent','OPENAI_BASE_URL':'override','ANTHROPIC_API_KEY':'fixture','MODEL':'other'}):
            env=r.clean_environment()
            for k in ('CODEX_THREAD_ID','OPENAI_BASE_URL','ANTHROPIC_API_KEY','MODEL'): self.assertNotIn(k,env)
    def events(self): return [{'type':'thread.started','thread_id':'artificial'},{'type':'item.completed','item':{'type':'agent_message','text':'{}'}},{'type':'turn.completed','usage':{'input_tokens':5,'output_tokens':2}}]
    def test_tool_and_fallback_rejected(self):
        for change in ({'type':'item.completed','item':{'type':'command_execution'}},{'type':'meta','model':'other'},{'type':'meta','subtype':'fallback'}):
            with self.assertRaises(ValueError): r.audit_events(self.events()+[change])
    def test_nested_substitution_rejected(self):
        with self.assertRaises(ValueError): r.audit_events(self.events()+[{'type':'meta','message':{'model':'other'}}])
    def test_missing_model_is_unavailable(self): self.assertIsNone(r.audit_events(self.events())['served_model_identifier'])
    def test_usage_and_provider_retry_visible(self):
        m=r.audit_events(self.events()+[{'type':'system','subtype':'api_retry','attempt':2}])
        self.assertEqual(len(m['internal_transport_retry_events']),1); self.assertEqual(m['usage'][0]['input_tokens'],5)
    def test_unique_attempt_preserves_failure_and_prevents_relaunch(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(r,'RUNTIME',Path(tmp)),patch.object(r,'binary_check',side_effect=ValueError('artificial prelaunch failure')),patch.object(r,'inventory',return_value={}):
            first=r.execute('taxonomy','ARTIFICIAL','fixture','probes')
            self.assertEqual(first['validation']['status'],'failed')
            self.assertTrue((Path(tmp)/'probes/taxonomy/ARTIFICIAL/attempt.json').exists())
            with self.assertRaises(FileExistsError): r.execute('taxonomy','ARTIFICIAL','fixture','probes')
    def test_stop_blocks_schedule(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(r,'RUNTIME',Path(tmp)):
            r.stop('taxonomy','fixture')
            with self.assertRaises(ValueError): r.stopped()

if __name__=='__main__': unittest.main()
