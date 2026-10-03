"""Offline only. All writes/providers use temporary roots/mocks, even post-completion."""
from copy import deepcopy
from contextlib import ExitStack
import importlib.util
from itertools import product
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

H=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(H))
import contracts as c
import audit
spec=importlib.util.spec_from_file_location('h6r2_runner',H/'runner.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
T=r.read(H/'taxonomy.json')


def assignment(cid='K01-C1',origin='MAPPING_GENERATED',function='GOVERNANCE_RULE'):
    refs=[]
    if origin in ('TARGET_SUPPLIED','BOTH_SUPPLIED'):refs.append({'source_type':'TARGET','source_id':cid[:3]+'-T'})
    if origin in ('SOURCE_SUPPLIED','BOTH_SUPPLIED'):refs.append({'source_type':'SOURCE_INSTRUMENT','source_id':cid[:3]+'-S'})
    return {'claim_id':cid,'atomicity':'ATOMIC','content_origin':{'assignment_status':'ASSIGNED',
       'kind':origin,'origin_refs':refs,'competing_origins':[],'rationale':'Offline fixture'},
       'epistemic_function':{'assignment_status':'ASSIGNED','kind':function,
       'competing_functions':[],'rationale':'Offline fixture'}}


def discovery(a, secondaries=(), ref=None, closure='COMPLETE'):
    deps=[];emb=[]
    for i,f in enumerate(secondaries,1):
        did=f'D{i}';subject=f'Embedded {f}'
        deps.append({'dependency_id':did,'trigger':'EMBEDDED_'+f,'resolution':'INLINE_OBLIGATION','claim_ref':None,
         'inline_obligation':{'contract':T['generated_routing'][f],'subject':subject,'provenance_refs':[]},
         'materiality':'REQUIRED','rationale':'Distinct material unevaluated fixture'})
        emb.append({'dependency_id':did,'subject':subject,'epistemic_function':f,'rationale':'Offline fixture'})
    if ref:
        did=f'D{len(deps)+1}'
        deps.append({'dependency_id':did,'trigger':'EMBEDDED_FACT','resolution':'CLAIM_REF','claim_ref':ref,
          'inline_obligation':{'contract':None,'subject':None,'provenance_refs':[]},'materiality':'REQUIRED','rationale':'Material reference'})
        emb.append({'dependency_id':did,'subject':'Reference content','epistemic_function':'FACT','rationale':'Offline fixture'})
    return {'claim_obligation_set':{'claim_id':a['claim_id'],'classification':{
      'content_origin':a['content_origin']['kind'],'epistemic_function':a['epistemic_function']['kind']},
      'base_obligations':[{'obligation_id':f'B{i}','contract':v,'subject':'WHOLE_CLAIM'} for i,v in enumerate(c.routes(a,T),1)],
      'dependencies':deps,'closure_status':closure,'unresolved_dependencies':['Ambiguous operation'] if closure=='DEPENDENCY_UNCERTAIN' else []},'embedded_classifications':emb}


def evals(a,b,verdicts):
    claim={'claim_id':a['claim_id'],'value':'Whole claim'}
    return {(a['claim_id'],job['obligation_id']):{**job,'verdict':v}
            for job,v in zip(c.obligation_jobs(claim,a,b),verdicts)}


class Classification(unittest.TestCase):
    def validate(self,a):
        claim,case=r.claims()[a['claim_id']]
        return c.validate('classification',a,c.classification_packet(claim,case),r.read(H/'schemas/classification.schema.json'),T)
    def test_all_24_axis_combinations_and_routes(self):
        for o,f in product(T['origins'],T['functions']):
            a=assignment(origin=o,function=f)
            self.assertEqual(self.validate(a),[])
            self.assertTrue(c.routes(a,T))
        self.assertEqual(len(c.regression_fixtures(T)),24)
    def test_source_limit_and_generated_fact(self):
        self.assertEqual(c.routes(assignment(origin='SOURCE_SUPPLIED',function='LIMIT'),T),['SOURCE_FIDELITY'])
        self.assertEqual(c.routes(assignment(function='FACT'),T),['FACT_WARRANT'])
    def test_origin_uncertainty_preserved(self):
        a=assignment();a['content_origin'].update(assignment_status='ORIGIN_UNCERTAIN',kind=None,competing_origins=['TARGET_SUPPLIED','MAPPING_GENERATED'])
        self.validate(a);self.assertFalse(c.eligible(a))
    def test_function_uncertainty_preserved(self):
        a=assignment();a['epistemic_function'].update(assignment_status='FUNCTION_UNCERTAIN',kind=None,competing_functions=['FACT','INFERENCE'])
        self.validate(a);self.assertFalse(c.eligible(a))
    def test_split_has_no_obligations(self):
        a=assignment();a['atomicity']='SPLIT_REQUIRED';self.validate(a)
        with self.assertRaises(ValueError):c.routes(a,T)
    def test_invalid_axes_and_old_labels_rejected(self):
        for key,val in [('content_origin','SUPPLIED_FACT'),('epistemic_function','SOURCE_FACT')]:
            a=assignment();a[key]['kind']=val
            with self.assertRaises(Exception):self.validate(a)
    def test_positive_supply_provenance_diagnostic(self):
        a=assignment(origin='BOTH_SUPPLIED');a['content_origin']['origin_refs'].pop()
        self.assertEqual(self.validate(a)[0]['code'],'ORIGIN_PROVENANCE_FAILURE')
    def test_uncertainty_cannot_keep_assignment(self):
        a=assignment();a['content_origin']['assignment_status']='ORIGIN_UNCERTAIN'
        with self.assertRaises(ValueError):self.validate(a)
    def test_schema_and_wire_accept_same_shapes(self):
        from jsonschema import Draft202012Validator
        for o,f in product(T['origins'],T['functions']):
            Draft202012Validator(r.read(H/'schemas/classification-wire.schema.json')).validate(assignment(origin=o,function=f))


class Obligations(unittest.TestCase):
    def validate(self,a,b):
        claim,case=r.claims()[a['claim_id']]
        assignments={x['claim_id']:assignment(x['claim_id']) for x in case['claims']};assignments[a['claim_id']]=a
        return c.validate('obligation',b,c.obligation_packet(claim,case,a,assignments),r.read(H/'schemas/obligation.schema.json'),T)
    def test_every_function_secondary_contract(self):
        a=assignment();b=discovery(a,T['functions']);self.assertEqual(self.validate(a,b),[])
    def test_normative_control_has_base_only(self):
        a=assignment('K08-C1');b=discovery(a);self.validate(a,b)
        self.assertEqual(len(c.obligation_jobs(r.claims()[a['claim_id']][0],a,b)),1)
    def test_missing_base_is_recorded_without_repair(self):
        a=assignment();b=discovery(a);b['claim_obligation_set']['base_obligations']=[];original=deepcopy(b)
        self.assertIn('OBLIGATION_OMISSION',[d['code'] for d in self.validate(a,b)]);self.assertEqual(b,original)
        self.assertEqual(c.aggregate({a['claim_id']:a},{a['claim_id']:b},{},T)[a['claim_id']]['overall'],'UNCERTAIN')
    def test_wrong_secondary_contract_preserved(self):
        a=assignment();b=discovery(a,['FACT']);b['claim_obligation_set']['dependencies'][0]['inline_obligation']['contract']='DERIVED_WARRANT'
        self.assertEqual(self.validate(a,b)[0]['code'],'WRONG_SECONDARY_CONTRACT')
    def test_claim_ref_no_duplicate_job(self):
        a=assignment('K09-C2');b=discovery(a,ref='K09-C1');self.validate(a,b)
        self.assertEqual(len(c.obligation_jobs(r.claims()['K09-C2'][0],a,b)),1)
    def test_ref_and_inline_cannot_coexist(self):
        a=assignment('K09-C2');b=discovery(a,ref='K09-C1')
        b['claim_obligation_set']['dependencies'][0]['inline_obligation']['contract']='FACT_WARRANT'
        with self.assertRaises(ValueError):self.validate(a,b)
    def test_unknown_referent_rejected(self):
        a=assignment();b=discovery(a,ref='missing')
        with self.assertRaises(ValueError):self.validate(a,b)
    def test_nested_structure_rejected(self):
        a=assignment();b=discovery(a,['OPERATION']);b['claim_obligation_set']['dependencies'][0]['dependencies']=[]
        with self.assertRaises(Exception):self.validate(a,b)
    def test_depth_requires_split_no_jobs(self):
        a=assignment();b=discovery(a,['OPERATION'],closure='SPLIT_REQUIRED');self.validate(a,b)
        self.assertEqual(c.obligation_jobs(r.claims()[a['claim_id']][0],a,b),[])
    def test_uncertain_dependency_closure(self):
        a=assignment('K12-C1');b=discovery(a,closure='DEPENDENCY_UNCERTAIN')
        self.assertEqual(self.validate(a,b)[0]['code'],'DEPENDENCY_UNCERTAIN')
        ev=evals(a,b,['SATISFIED'])
        self.assertEqual(c.aggregate({a['claim_id']:a},{a['claim_id']:b},ev,T)[a['claim_id']]['overall'],'UNCERTAIN')
    def test_cannot_hide_unresolved_in_complete(self):
        a=assignment();b=discovery(a);b['claim_obligation_set']['unresolved_dependencies']=['unresolved']
        with self.assertRaises(ValueError):self.validate(a,b)
    def test_unsafe_or_duplicate_ids_rejected(self):
        for key in ['../escape','B1']:
            a=assignment();b=discovery(a,['OPERATION']);b['claim_obligation_set']['dependencies'][0]['dependency_id']=key;b['embedded_classifications'][0]['dependency_id']=key
            with self.assertRaises(ValueError):self.validate(a,b)
    def test_frozen_embedded_function_cannot_change(self):
        a=assignment();b=discovery(a,['FACT']);b['embedded_classifications'][0]['epistemic_function']='INFERENCE'
        with self.assertRaises(ValueError):self.validate(a,b)


class Aggregation(unittest.TestCase):
    def test_all_64_three_obligation_verdict_combinations(self):
        a=assignment();b=discovery(a,['OPERATION','CONDITIONAL_RELATION'])
        for verdicts in product(c.RANK,repeat=3):
            v=c.aggregate({a['claim_id']:a},{a['claim_id']:b},evals(a,b,verdicts),T)[a['claim_id']]
            self.assertEqual(v['overall'],max(verdicts,key=c.RANK.get));self.assertEqual(len(v['results']),3)
    def test_n7_good_operation_cannot_rescue_governance(self):
        a=assignment('K10-C1');b=discovery(a,['OPERATION'])
        v=c.aggregate({a['claim_id']:a},{a['claim_id']:b},evals(a,b,['VIOLATED','SATISFIED']),T)[a['claim_id']]
        self.assertEqual(v['overall'],'VIOLATED')
    def test_n8_both_failures_preserved(self):
        a=assignment('K11-C1');b=discovery(a,['OPERATION','CONDITIONAL_RELATION'])
        v=c.aggregate({a['claim_id']:a},{a['claim_id']:b},evals(a,b,['SATISFIED','VIOLATED','VIOLATED']),T)[a['claim_id']]
        self.assertEqual(sum(x['verdict']=='VIOLATED' for x in v['results']),2)
    def test_missing_observation_not_fabricated(self):
        a=assignment();b=discovery(a,['OPERATION']);v=c.aggregate({a['claim_id']:a},{a['claim_id']:b},evals(a,b,['VIOLATED']),T)[a['claim_id']]
        self.assertIsNone(v['overall']);self.assertEqual(v['status'],'INCOMPLETE')
    def test_reference_reuse_and_failure(self):
        a1=assignment('K09-C1',function='FACT');a2=assignment('K09-C2');b1=discovery(a1);b2=discovery(a2,ref='K09-C1')
        for verdict in c.RANK:
            result=c.aggregate({'K09-C2':a2,'K09-C1':a1},{'K09-C1':b1,'K09-C2':b2},
             {**evals(a1,b1,[verdict]),**evals(a2,b2,['SATISFIED'])},T)
            self.assertEqual(result['K09-C2']['overall'],verdict)
    def test_cycles_and_self_cycles_rejected(self):
        for sets in [ {'a':{'dependencies':[{'resolution':'CLAIM_REF','claim_ref':'a'}]}},
                     {'a':{'dependencies':[{'resolution':'CLAIM_REF','claim_ref':'b'}]},'b':{'dependencies':[{'resolution':'CLAIM_REF','claim_ref':'a'}]}}]:
            with self.assertRaisesRegex(ValueError,'DEPENDENCY_CYCLE'):c.dependency_order(sets,sets)
    def test_split_ref_cannot_cleanly_pass(self):
        a1=assignment('K09-C1');a1['atomicity']='SPLIT_REQUIRED';a2=assignment('K09-C2');b2=discovery(a2,ref='K09-C1')
        self.assertEqual(c.aggregate({'K09-C1':a1,'K09-C2':a2},{'K09-C2':b2},evals(a2,b2,['SATISFIED']),T)['K09-C2']['overall'],'UNCERTAIN')
    def test_fidelity_failure_no_rerouting(self):
        a=assignment(origin='TARGET_SUPPLIED',function='LIMIT');b=discovery(a)
        self.assertEqual(c.aggregate({a['claim_id']:a},{a['claim_id']:b},evals(a,b,['VIOLATED']),T)[a['claim_id']]['overall'],'VIOLATED')
        self.assertEqual(a['content_origin']['kind'],'TARGET_SUPPLIED')


class Packets(unittest.TestCase):
    def test_corpus_exactly_twelve_thirteen(self):
        self.assertEqual(len(r.manifest()['case_order']),12);self.assertEqual(len(r.claims()),13)
    def test_blind_projection_discards_operator_fields(self):
        claim,case=r.claims()['K01-C1'];poison={**case,'hidden_operator_hypothesis':'SECRET_SENTINEL'}
        self.assertNotIn('SECRET_SENTINEL',json.dumps(c.classification_packet(claim,poison)))
        packet=r.build_packet('classification','K01-C1');prompt=r.prompt('classification',packet).decode()
        self.assertNotIn('expected_overall',prompt);self.assertNotIn('GOVERNANCE_COHERENCE',prompt)
    def test_fidelity_projection_and_evaluation_isolation(self):
        claim,case=r.claims()['K01-C1']
        for contract,key in [('TARGET_FIDELITY','target'),('SOURCE_FIDELITY','source_instrument')]:
            p=c.evaluation_packet(claim,case,{'claim_id':claim['claim_id'],'obligation_id':'B1','subject':claim['value'],'contract':contract},T)
            self.assertIn(key,p);self.assertNotIn('mapping',p);self.assertNotIn('classification',p)
            self.assertEqual(len([k for k in ('target','source_instrument') if k in p]),1)
    def test_one_evaluation_contract_and_no_old_verdict(self):
        claim,case=r.claims()['K01-C1'];p=c.evaluation_packet(claim,case,{'claim_id':claim['claim_id'],'obligation_id':'D1','subject':'inspect colors','contract':'OPERATION_LICENSE'},T)
        v={k:p[k] for k in ('claim_id','obligation_id','subject','contract')};v.update(verdict='SUPPORTED',provenance_refs=[],unresolved_conditions=[],rationale='Fixture')
        with self.assertRaises(Exception):c.validate('evaluation',v,p,r.read(H/'schemas/evaluation.schema.json'),T)
    def test_classification_failure_diagnostic(self):
        claim,case=r.claims()['K01-C1'];p=c.evaluation_packet(claim,case,{'claim_id':claim['claim_id'],'obligation_id':'B1','subject':claim['value'],'contract':'TARGET_FIDELITY'},T)
        v={k:p[k] for k in ('claim_id','obligation_id','subject','contract')};v.update(verdict='VIOLATED',provenance_refs=[],unresolved_conditions=[],rationale='Fixture')
        self.assertEqual(c.validate('evaluation',v,p,r.read(H/'schemas/evaluation.schema.json'),T)[0]['code'],'CLASSIFICATION_CONTRACT_FAILURE')


class Execution(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.study=self.root/'study';self.study.mkdir()
        for name in ('schemas','cases'):shutil.copytree(H/name,self.study/name)
        for name in ('manifest.json','taxonomy.json','execution-config.json','CLASSIFICATION-PROMPT.md','OBLIGATION-PROMPT.md','EVALUATION-PROMPT.md','OBLIGATIONS.md'):
            shutil.copy(H/name,self.study/name)
        self.stack=ExitStack();self.addCleanup(self.stack.close)
        for name,value in [('H',self.study),('RT',self.root/'runtime')]:self.stack.enter_context(patch.object(r,name,value))
        for name in ('verify','active_batch','binary_check'):self.stack.enter_context(patch.object(r,name))
        self.stack.enter_context(patch.object(r,'head',return_value='offline-fixture'))
        self.uid='K01-C1';packet=r.build_packet('classification',self.uid)
        r.write(r.packet_path('classification',self.uid),packet);r.raw(r.packet_path('classification',self.uid,'txt'),r.prompt('classification',packet))
    def test_budget_denial_prevents_launch(self):
        gate=Mock();gate.reserve.side_effect=r.budget.BudgetError('denied')
        with patch.object(r.subprocess,'Popen') as launch:
            with self.assertRaises(r.budget.BudgetError):r.run_one('classification',self.uid,{'experiment_id':'fixture'},gate)
            launch.assert_not_called();gate.reserve.assert_called_once()
    def test_failed_attempt_preserved_no_retry(self):
        gate=Mock()
        with patch.object(r.subprocess,'Popen',side_effect=OSError('fixture transport')) as launch:
            with self.assertRaises(OSError):r.run_one('classification',self.uid,{'experiment_id':'fixture'},gate)
            with self.assertRaisesRegex(ValueError,'no retry'):r.run_one('classification',self.uid,{'experiment_id':'fixture'},gate)
            self.assertEqual(launch.call_count,1);gate.reserve.assert_called_once()
        self.assertTrue((r.RT/'attempts/classification/K01-C1/failure.json').exists())
    def test_success_reserves_once_and_preserves_raw(self):
        gate=Mock();response=json.dumps(assignment());outer=self
        class Process:
            pid=999999999;returncode=0
            def __init__(self,cmd,**kwargs):
                gate.reserve.assert_called_once();self.out=kwargs['stdout'];self.dest=Path(cmd[cmd.index('--output-last-message')+1])
            def communicate(self,request,timeout):
                r.raw(self.dest,response.encode())
                for e in [{'type':'thread.started','thread_id':'offline-fixture'},
                  {'type':'item.completed','item':{'type':'agent_message','text':response}},
                  {'type':'turn.completed','usage':{'input_tokens':1,'output_tokens':1}}]:self.out.write((json.dumps(e)+'\n').encode())
            def poll(self):return 0
        with patch.object(r.subprocess,'Popen',side_effect=Process) as launch:
            r.run_one('classification',self.uid,{'experiment_id':'fixture'},gate)
            self.assertEqual(r.read(r.judgment('classification',self.uid)),assignment())
            with self.assertRaisesRegex(ValueError,'Judgment already exists'):r.run_one('classification',self.uid,{'experiment_id':'fixture'},gate)
            self.assertEqual(launch.call_count,1)
        gate.finish.assert_called_once_with('fixture','classification:K01-C1',0)
    def test_incomplete_freeze_writes_nothing_to_real_study(self):
        with patch.object(r,'scheduling_clear'):
            with self.assertRaisesRegex(ValueError,'incomplete'):r.freeze('classification')
        self.assertFalse((self.study/'classification-freeze.json').exists())
    def test_stage_barriers(self):
        for stage in ('obligation','evaluation'):
            with self.assertRaisesRegex(ValueError,'Missing complete stage freeze'):r.ids(stage)
    def test_pause_blocks_scheduling_and_active_batch(self):
        for state in ('PAUSED_EVENT','PAUSED_INTEGRITY','PAUSED_AMBIGUOUS','TERMINATED_LINEAGE','COMPLETE','RUNNING'):
            with patch.object(r,'latest_state',return_value={'state':state}):
                with self.assertRaises(ValueError):r.scheduling_clear()
    def test_batch_limit(self):
        for n in (0,4):
            with self.assertRaises(ValueError):r.run_batch('classification',Path('/unused'),n,None)
    def test_unknown_evaluation_forecast_retained(self):
        plan=r.financial_plan();self.assertEqual([s['sessions'] for s in plan['stages']],[13,13,None])
        self.assertIsNone(r.remaining_plan(plan)['stages'][2]['sessions'])
    def test_usage_approval_never_created(self):
        with self.assertRaises(ValueError):r.approve_usage_check({'approval_required':True},{},None,'classification',3)
    def test_tampered_hash_and_duplicate_json_rejected(self):
        p=self.root/'x';p.write_text('a');h=r.sha(p);p.write_text('b')
        with patch.object(r,'R',self.root):
            with self.assertRaises(ValueError):r.hashes({'x':h})
        with self.assertRaises(ValueError):json.loads('{"a":1,"a":2}',object_pairs_hook=r.unique)
    def test_isolation_flags_and_model(self):
        cmd=r.command('classification',self.root/'empty',self.root/'out')
        for flag in ('--ignore-user-config','--ignore-rules','--ephemeral','--sandbox','--disable'):self.assertIn(flag,cmd)
        self.assertEqual(cmd[cmd.index('--model')+1],'gpt-6-astra');self.assertIn('model_reasoning_effort="high"',cmd)
    def test_provider_events_no_substitution_or_tools(self):
        events=[{'type':'thread.started','thread_id':'fixture'},{'type':'item.completed','item':{'type':'agent_message','text':'{}'}},{'type':'turn.completed'}]
        for event in ({'type':'error'},{'model':'substitute'},{'fallback':True},{'item':{'type':'command_execution'}}):
            with self.assertRaises(ValueError):r.audit_events(events+[event],'{}')


class AuditAndLifecycle(unittest.TestCase):
    def fixture(self):
        hypotheses=r.read(H/'hidden-hypotheses/controls.json')
        assignments={};outputs={};evaluations={}
        for case in hypotheses:
            for h in case['hidden_operator_hypotheses']:
                cid=h['claim_id'];a=assignment(cid,h['content_origin'],h['epistemic_function'])
                b=discovery(a,[e['epistemic_function'] for e in h['expected_secondary_obligations']],
                            ref=h['claim_refs'][0] if h['claim_refs'] else None,closure=h['closure_status'])
                assignments[cid]=a;outputs[cid]=b
                evaluations.update(evals(a,b,[h['base_verdict']]+[e['verdict'] or 'SATISFIED' for e in h['expected_secondary_obligations']]))
        return hypotheses,assignments,outputs,evaluations
    def review(self,hypotheses):
        value=audit.operator_template(hypotheses);value['status']='COMPLETE'
        for row in value['claim_reviews']:
            for m in row['expected_dependency_matches']:
                m.update(finding='PRESENT',dependency_ids=[f"D{m['expected_index']+1}"],rationale='Offline matched fixture')
            for d in row['semantic_checks']:d.update(finding='ABSENT',rationale='Offline inspected fixture')
        return value
    def test_twelve_case_offline_replay_and_reference_count(self):
        h,a,b,e=self.fixture();agg=c.aggregate(a,b,e,T)
        for case in h:
            for expected in case['hidden_operator_hypotheses']:
                self.assertEqual(agg[expected['claim_id']]['overall'],expected['expected_overall'])
        m=audit.report(a,b,list(e.values()),agg,h,[],self.review(h))
        self.assertEqual(len(m['cases']),12);self.assertEqual(m['claim_ref_count'],1)
        self.assertEqual(m['diagnostic_counts']['DEPENDENCY_DUPLICATION'],0)
        self.assertEqual(len([x for x in e.values() if x['claim_id']=='K09-C1']),1)
    def test_omission_laundering_reported_without_repair(self):
        h,a,b,e=self.fixture();b['K01-C1']=discovery(a['K01-C1']);del e[('K01-C1','D1')]
        review=self.review(h);review['claim_reviews'][0]['expected_dependency_matches'][0].update(finding='OMITTED',dependency_ids=[],rationale='Missing operation')
        agg=c.aggregate(a,b,e,T);self.assertEqual(agg['K01-C1']['overall'],'SATISFIED')
        m=audit.report(a,b,list(e.values()),agg,h,[],review)
        self.assertEqual(m['diagnostic_counts']['OBLIGATION_OMISSION'],1)
        self.assertEqual(m['diagnostic_counts']['GOVERNANCE_LAUNDERING'],1)
    def test_every_diagnostic_count_and_evidence_retained(self):
        h,a,b,e=self.fixture();agg=c.aggregate(a,b,e,T)
        events=[{'code':code,'claim_id':'K01-C1','detail':'Offline injected detection'} for code in c.DIAGNOSTICS]
        m=audit.report(a,b,list(e.values()),agg,h,events,self.review(h))
        self.assertTrue(all(m['diagnostic_counts'][code]>=1 for code in c.DIAGNOSTICS))
    def test_semantic_audit_cannot_skip_checks(self):
        h,a,b,e=self.fixture();review=self.review(h);review['claim_reviews'][0]['semantic_checks']=[]
        with self.assertRaisesRegex(ValueError,'Semantic checks incomplete'):
            audit.report(a,b,list(e.values()),c.aggregate(a,b,e,T),h,[],review)
    def test_wrong_contract_overtrigger_duplication_and_recursion_auditable(self):
        h,a,b,e=self.fixture();review=self.review(h)
        for d in review['claim_reviews'][0]['semantic_checks']:
            d.update(finding='PRESENT',rationale='Offline counterexample')
        m=audit.report(a,b,list(e.values()),c.aggregate(a,b,e,T),h,[],review)
        for code in audit.SEMANTIC_CODES:self.assertGreater(m['diagnostic_counts'][code],0)
    def test_exact_duplicate_existing_claim_blocks_jobs(self):
        a1=assignment('K09-C1',function='FACT');a2=assignment('K09-C2')
        b1=discovery(a1);b2=discovery(a2,['FACT'])
        b2['claim_obligation_set']['dependencies'][0]['inline_obligation']['subject']=r.claims()['K09-C1'][0]['value']
        with patch.object(r,'assignments',return_value={'K09-C1':a1,'K09-C2':a2}), \
             patch.object(r,'discoveries',return_value={'K09-C1':b1,'K09-C2':b2}):
            with self.assertRaisesRegex(ValueError,'DEPENDENCY_DUPLICATION'):r.jobs()
    def test_invalid_graph_blocks_before_evaluation(self):
        a=assignment('K09-C1');b=discovery(a,ref='K09-C1')
        with patch.object(r,'assignments',return_value={'K09-C1':a}), \
             patch.object(r,'discoveries',return_value={'K09-C1':b}):
            with self.assertRaisesRegex(ValueError,'DEPENDENCY_CYCLE'):r.jobs()
    def test_batch_evaluates_all_three_despite_scientific_failure(self):
        with tempfile.TemporaryDirectory() as d, ExitStack() as stack:
            root=Path(d)
            for key,val in [('RT',root/'runtime'),('H',root/'study')]:stack.enter_context(patch.object(r,key,val))
            for key in ('scheduling_clear','verify','committed'):stack.enter_context(patch.object(r,key))
            stack.enter_context(patch.object(r,'head',return_value='fixture'))
            stack.enter_context(patch.object(r,'ids',return_value=['one','two','three']))
            stack.enter_context(patch.object(r,'check_plan',return_value={'stages':[{'id':'evaluation','usage_profile':'fixture'}]}))
            stack.enter_context(patch.object(r,'usage_check',return_value={'account_scope':'fixture'}))
            gate=Mock();gate.status.return_value={'allowed':True};stack.enter_context(patch.object(r.budget,'Gate',return_value=gate))
            stack.enter_context(patch.object(r.usage,'read_limits',side_effect=ValueError('offline snapshot unavailable')))
            run=stack.enter_context(patch.object(r,'run_one',side_effect=[{'verdict':'VIOLATED'},{'verdict':'VIOLATED'},{'verdict':'SATISFIED'}]))
            r.run_batch('evaluation',root/'preflight',3,None)
            self.assertEqual(run.call_count,3)
            self.assertEqual(r.latest_state()['state'],'BATCH_COMPLETE')


if __name__=='__main__':unittest.main()
