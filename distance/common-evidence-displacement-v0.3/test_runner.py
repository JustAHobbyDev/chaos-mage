import copy
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import contracts as c
import derive
import metrics as m
import runner as r

class Tests(unittest.TestCase):
    def admissions(self):return [{'mapping_id':x['mapping_id'],'target_id':x['target_id'],'admitted':True,'validity_A':'Valid','validity_B':'Valid'} for x in r.manifest()]
    def pairs(self):return r.construct_pairs(self.admissions())[0]
    def output(self,relation='approximately_equal',stage='prospective',case_id='C001'):
        value=r.probe_response(stage);value['case_id']=case_id;value['overall_relation']=relation
        value['meaningful_difference']['status']='no' if relation=='approximately_equal' else 'uncertain' if relation=='insufficient_information' else 'yes'
        if relation=='insufficient_information':value['uncertainty']=['Missing observable distinction.']
        return value
    def all_values(self,pairs,stage):return {(p['case_id'],f):self.output(stage=stage,case_id=p['case_id']) for p in pairs for f in 'AB'}
    def test_inputs_history_world_commit(self):r.validate_inputs();r.preservation(True)
    def test_common_state_components_identical(self):
        for p in self.pairs():
            a,b=[json.loads(r.candidate(p['mapping_'+slot])['target']['evidence'][0]) for slot in 'AB']
            for k in ('target','native_baseline','shared_state','investigation_budget'):self.assertEqual(c.serialized(a[k]),c.serialized(b[k]))
            for k in ('facts','artifacts','initial_observations','known_uncertainties','available_affordances','constraints'):
                self.assertEqual(c.serialized(a['shared_state'][k]),c.serialized(b['shared_state'][k]))
    def test_exact_packet_common_bytes_both_stages(self):
        for p in self.pairs():
            common=(r.HERE/'common-states'/f'{p["target_id"]}.json').read_bytes()
            for stage in ('prospective','consequence'):self.assertIn(common,r.comparison_packet(p,stage).encode())
    def test_packet_allowlist_blinding(self):
        for p in self.pairs():
            for stage in ('prospective','consequence'):
                packet=r.comparison_packet(p,stage);body=json.loads(packet.split('\n\nCASE PACKET\n')[1])
                self.assertEqual(set(body),{'case_id','stage','mapping_A','mapping_B','common_start'})
                for slot in 'AB':self.assertEqual(set(body['mapping_'+slot]),{'source','mapping'}|({'realized'} if stage=='consequence' else set()))
                for token in ('world_facts_used','operator_intention','control_of','historical_case_id','decisive_basis','world_sha256','validity_A'):self.assertNotIn('"'+token+'"',packet)
                self.assertIsNone(re.search(r'\b(Native|Adjacent|Remote|Alien)\b',packet))
    def test_stage_a_contains_no_realized_field(self):
        for p in self.pairs():self.assertNotIn('"realized"',r.comparison_packet(p,'prospective'))
    def test_consequence_builder_cannot_read_stage_a(self):
        original=r.read
        def guarded(path):
            self.assertNotIn('judgments',Path(path).parts);self.assertNotIn('prospective',Path(path).parts)
            return original(path)
        with patch.object(r,'read',side_effect=guarded):
            for p in self.pairs():r.comparison_packet(p,'consequence')
    def test_outcomes_recompute(self):
        for row in r.manifest():c.validate_outcome(row,r.read(r.HERE/'outcomes'/f'{row["mapping_id"]}.json'))
    def test_outcome_rejects_world_facts_signal_and_budget_drift(self):
        row=r.manifest()[0];original=r.read(r.HERE/'outcomes'/f'{row["mapping_id"]}.json')
        for field,value in [('world_id','other'),('world_sha256','wrong'),('world_facts_used',['invented']),('resulting_signal',[{'fake':'decisive'}]),('derivation',{'engine_sha256':'wrong','method':'fake'}),('resource_use',{'endpoint_trials':999})]:
            v=copy.deepcopy(original);v[field]=value
            with self.subTest(field=field),self.assertRaises((ValueError,c.jsonschema.ValidationError)):c.validate_outcome(row,v)
    def test_mapping_cannot_introduce_privileged_evidence(self):
        p=self.pairs()[0];maps={x['mapping_id']:r.candidate(x['mapping_id']) for x in r.manifest()};commons={x['target_id']:r.read(r.HERE/'common-states'/f'{x["target_id"]}.json') for x in r.manifest()};ads={x['mapping_id']:x for x in self.admissions()}
        for target_key in ('question','evidence'):
            broken=copy.deepcopy(maps);broken[p['mapping_1']]['target'][target_key]='different' if target_key=='question' else ['privileged fact']
            with self.assertRaises(ValueError):c.validate_pair(p,broken,commons,ads)
    def test_only_valid_valid(self):
        p=self.pairs()[0];maps={x['mapping_id']:r.candidate(x['mapping_id']) for x in r.manifest()};commons={x['target_id']:r.read(r.HERE/'common-states'/f'{x["target_id"]}.json') for x in r.manifest()}
        for family in 'AB':
            for status in ('Conditional','Invalid'):
                ads={x['mapping_id']:x for x in self.admissions()};ads[p['mapping_1']]['validity_'+family]=status
                with self.assertRaises(ValueError):c.validate_pair(p,maps,commons,ads)
    def test_attrition_no_backfill(self):
        ads=self.admissions();removed=next(x for x in ads if x['target_id']=='T03');removed['admitted']=False
        pairs,_=r.construct_pairs(ads);self.assertEqual(sum(x['cohort']=='primary' for x in pairs),14)
        self.assertTrue(all(removed['mapping_id'] not in (p['mapping_1'],p['mapping_2']) for p in pairs))
        for x in ads:x['admitted']=False
        self.assertEqual(r.construct_pairs(ads)[0],[])
    def test_meaningful_gate_all_combinations(self):
        allowed={'yes':{'A_dominates','B_dominates','tradeoff'},'no':{'approximately_equal'},'uncertain':{'insufficient_information'}}
        for status in allowed:
            for rel in ('A_dominates','B_dominates','tradeoff','approximately_equal','insufficient_information'):
                v=self.output(rel);v['meaningful_difference']['status']=status
                if rel in allowed[status]:c.validate(v,'prospective')
                else:
                    with self.assertRaises(c.jsonschema.ValidationError):c.validate(v,'prospective')
    def test_tradeoff_distinct_from_equality(self):
        a=self.output('tradeoff');b=self.output();self.assertNotEqual(a['meaningful_difference']['status'],b['meaningful_difference']['status'])
        self.assertEqual(m.disagreement('tradeoff','approximately_equal'),'tradeoff-vs-approximately_equal')
    def test_no_old_enums_intrinsic_fields_or_composite(self):
        for rel in ('Native','Adjacent','Remote','Alien','tie','A_more_displacing',True,0):
            v=self.output();v['overall_relation']=rel
            with self.assertRaises(c.jsonschema.ValidationError):c.validate(v,'prospective')
        for key in ('score','composite','mapping_A','counterfactual_native','global_propagation'):
            v=self.output();v[key]=1
            with self.assertRaises(c.jsonschema.ValidationError):c.validate(v,'prospective')
    def test_criterion_and_diagnostic_enums(self):
        for section,keys in [('criteria',c.CRITERIA),('consequence_structure',c.DIAGNOSTICS)]:
            for key in keys:
                for rel in ('A','B','balanced','indeterminate'):
                    v=self.output();v[section][key]['relation']=rel;c.validate(v,'prospective')
                for rel in ('tie','high',1):
                    v=self.output();v[section][key]['relation']=rel
                    with self.assertRaises(c.jsonschema.ValidationError):c.validate(v,'prospective')
    def test_no_majority_rule(self):
        v=self.output('A_dominates')
        for k in c.CRITERIA:v['criteria'][k]['relation']='B'
        c.validate(v,'prospective') # centrality is qualitative, not a criterion-vote validator
    def test_blank_rationale_and_missing_information(self):
        v=self.output();v['decisive_basis']['rationale']=' '
        with self.assertRaises(c.jsonschema.ValidationError):c.validate(v,'prospective')
        v=self.output('insufficient_information');v['uncertainty']=[]
        with self.assertRaises(ValueError):c.validate(v,'prospective')
    def test_stage_and_identity_checks(self):
        with self.assertRaises(ValueError):c.validate(self.output(),'consequence')
        with self.assertRaises(ValueError):c.validate(self.output(),'prospective',{'case_id':'wrong'})
    def test_wire_projection(self):
        for stage in r.STAGES:self.assertEqual(r.read(r.HERE/'schemas'/f'{stage}-wire.schema.json'),r.projection(r.read(r.canonical(stage))));c.validate(r.probe_response(stage),stage)
    def test_schedule_counts_seeds_balance(self):
        a=r.construct_pairs(self.admissions());self.assertEqual(a,r.construct_pairs(self.admissions()));pairs,schedules=a
        self.assertEqual(len(pairs),20);primary=[p for p in pairs if p['cohort']=='primary'];self.assertEqual(len(primary),16)
        self.assertEqual(sum(p['mapping_A']==p['mapping_1'] for p in primary),8)
        for stage in ('prospective','consequence'):self.assertEqual(len(schedules[stage]),40);self.assertEqual(len({(r['case_id'],r['family']) for r in schedules[stage]}),40)
        self.assertNotEqual([x['case_id'] for x in schedules['prospective']],[x['case_id'] for x in schedules['consequence']])
    def test_reversals_only_swap(self):
        pairs=self.pairs();by={p['case_id']:p for p in pairs}
        for p in pairs:
            if p['cohort']=='primary':continue
            for stage in ('prospective','consequence'):
                a,b=[json.loads(r.comparison_packet(x,stage).split('\n\nCASE PACKET\n')[1]) for x in (by[p['control_of']],p)]
                a['case_id']=b['case_id'];a['mapping_A'],a['mapping_B']=a['mapping_B'],a['mapping_A'];self.assertEqual(a,b)
    def test_normalization(self):
        for p in self.pairs():
            for slot in 'AB':
                expected='mapping_1' if p['mapping_'+slot]==p['mapping_1'] else 'mapping_2'
                self.assertEqual(c.normalize(slot,p),expected);self.assertEqual(c.normalize(slot+'_dominates',p),expected+'_dominates')
            for relation in ('balanced','indeterminate','tradeoff','approximately_equal','insufficient_information'):self.assertEqual(c.normalize(relation,p),relation)
    def test_primary_denominators_and_missing_results(self):
        pairs=self.pairs();v=self.all_values(pairs,'prospective');result=m.stage_metrics(v,pairs,['T01','T03','T05','T08'])
        self.assertEqual(result['overall_agreement']['denominator'],16);self.assertEqual(result['approximately_equal']['both'],16)
        self.assertEqual(result['orientation_summary']['A']['denominator'],4);del v[next(iter(v))]
        with self.assertRaises(ValueError):m.stage_metrics(v,pairs,[])
    def test_known_agreement(self):
        self.assertEqual(m.agreement([('tradeoff','tradeoff'),('tradeoff','approximately_equal')]),{'agreements':1,'denominator':2,'rate':0.5})
        self.assertIsNone(m.agreement([])['rate']);self.assertIsNone(m.category([],'tradeoff')['positive_agreement']['rate'])
    def test_all_disagreement_categories(self):
        a='mapping_1_dominates';b='mapping_2_dominates'
        self.assertEqual(m.disagreement(a,b),'opposite-dominance')
        self.assertEqual(m.disagreement(a,'tradeoff'),'dominance-vs-tradeoff')
        self.assertEqual(m.disagreement(a,'approximately_equal'),'dominance-vs-approximately_equal')
        self.assertEqual(m.disagreement('tradeoff','insufficient_information'),'relation-vs-insufficient_information')
    def test_transitions(self):
        cases=[('mapping_1_dominates','mapping_1_dominates','stable'),('approximately_equal','mapping_1_dominates','strengthened'),
          ('mapping_1_dominates','approximately_equal','weakened'),('mapping_1_dominates','tradeoff','changed-to-tradeoff'),
          ('tradeoff','mapping_2_dominates','tradeoff-resolved'),('mapping_1_dominates','mapping_2_dominates','direction-reversal'),
          ('insufficient_information','tradeoff','other'),('tradeoff','approximately_equal','other')]
        for a,b,expected in cases:self.assertEqual(m.transition(a,b),expected)
    def test_graph_cycles_tensions_and_sparse_denominators(self):
        pairs=[{'case_id':str(i),'target_id':'T','mapping_1':a,'mapping_2':b,'mapping_A':a,'mapping_B':b,'cohort':'primary'} for i,(a,b) in enumerate([('a','b'),('b','c'),('a','c')])]
        v={(str(i),'A'):self.output('A_dominates') for i in range(3)}
        graph=m.graph(pairs,v,'A',['T'])[0];self.assertEqual(graph['directed_cycles'],[]);self.assertEqual(graph['chain_closures'][0]['status'],'supported')
        v[('2','A')]=self.output('B_dominates');self.assertEqual(m.graph(pairs,v,'A',['T'])[0]['directed_cycles'],[['a','b','c']])
        for relation in ('tradeoff','approximately_equal'):
            v[('2','A')]=self.output(relation);self.assertEqual(m.graph(pairs,v,'A',['T'])[0]['chain_closures'][0]['status'],'transitivity-tension')
        self.assertIsNone(m.graph(pairs[:1],v,'A',['T'])[0]['directed_cycles'])
    def test_exactly_four_eligible_triangles(self):
        pairs=self.pairs();v=self.all_values(pairs,'prospective');graphs=m.stage_metrics(v,pairs,['T01','T03','T05','T08'])['graphs']
        for f in 'AB':self.assertEqual(sum(g['cycle_evidence_eligible'] for g in graphs[f]),4)
    def test_isolation_commands(self):
        for stage in r.STAGES:
            a=r.build_command('A','/tmp/empty',Path('/tmp/out'),'session',stage)
            for flag in ('--ignore-user-config','--ignore-rules','--ephemeral','shell_tool','plugins','apps','multi_agent'):self.assertIn(flag,a)
            b=r.build_command('B','/tmp/empty',Path('/tmp/out'),'session',stage);self.assertEqual(b[b.index('--tools')+1],'');self.assertIn('--safe-mode',b);self.assertIn('--no-session-persistence',b)
    def test_duplicate_session_across_stages(self):
        with tempfile.TemporaryDirectory() as td,patch.object(r,'RUNTIME',Path(td)):
            r.write_new(Path(td)/'prospective/old/validation.json',{'metadata':{'session_id':'same'}})
            with self.assertRaises(ValueError):r.check_fresh_session('same',Path(td)/'consequence/new')
    def test_exclusive_writes_and_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'value';r.write_new(p,{})
            with self.assertRaises(FileExistsError):r.write_new(p,{})
            p.write_text('{"x":1,"x":2}')
            with self.assertRaises(ValueError):r.read(p)
    def test_setup_failure_preserved(self):
        with tempfile.TemporaryDirectory() as td,patch.object(r,'adapter_execute',side_effect=RuntimeError('fixture')):
            d=Path(td)/'attempt';v=r.execute('A',d,'prompt');self.assertEqual(v['status'],'failed');self.assertEqual((d/'prompt.txt').read_text(),'prompt')
            with self.assertRaises(ValueError):r.execute('A',d,'prompt')
    def test_timeout_preserves_attempt(self):
        class Process:
            pid=999999
            def communicate(self,*a,**k):raise subprocess.TimeoutExpired('fixture',900)
            def wait(self):return -9
        with tempfile.TemporaryDirectory() as td,patch.object(r.subprocess,'Popen',return_value=Process()),patch.object(r.subprocess,'check_output',return_value=r.config()['expected_cli_versions']['A']),patch.object(r,'git',return_value=b'commit'),patch.object(r.os,'killpg'):
            d=Path(td)/'attempt';v=r.execute('A',d,'fixture');self.assertEqual(v['status'],'failed');self.assertIn('TimeoutExpired',v['error']);self.assertTrue((d/'events.jsonl').exists())
    def test_stop_scheduler_no_retry(self):
        with tempfile.TemporaryDirectory() as td,patch.object(r,'RUNTIME',Path(td)),patch.object(r,'prerequisites'),patch.object(r,'order',return_value=[{'id':'one','case_id':'one','family':'A'},{'id':'two','case_id':'two','family':'B'}]),patch.object(r,'packet',return_value='fixture'),patch.object(r,'git',return_value=b'commit'),patch.object(r,'execute',return_value={'status':'failed','error':'fixture'}) as execute:
            with self.assertRaises(ValueError):r.run_all('prospective')
            self.assertEqual(execute.call_count,1);self.assertTrue((Path(td)/'STOP.json').exists())
            with self.assertRaises(FileExistsError):r.run_all('prospective')
    def test_consequence_requires_committed_prospective(self):
        source=Path(r.__file__).read_text();segment=source[source.index('def prerequisites'):source.index('def run_all')]
        self.assertIn("committed(HERE/'prospective-freeze.json')",segment);self.assertNotIn("published('prospective')",segment)
    def test_malformed_response_and_formatter_audit(self):
        invalid=r.probe_response('prospective');invalid['overall_relation']='A_dominates'
        events=[{'type':'system','subtype':'init','session_id':'s','model':'claude-fable-5-1','tools':['StructuredOutput'],'plugins':[],'mcp_servers':[]},
                {'type':'assistant','message':{'model':'claude-fable-5-1','content':[{'type':'tool_use','name':'StructuredOutput','input':invalid}]}},
                {'type':'result','subtype':'success','session_id':'s','structured_output':invalid,'modelUsage':{'claude-fable-5-1':{}},'num_turns':2}]
        class Process:
            returncode=0
            def communicate(self,*a,**k):pass
        def popen(*a,**k):k['stdout'].write('\n'.join(map(json.dumps,events))+'\n');k['stdout'].flush();return Process()
        with tempfile.TemporaryDirectory() as td,patch.object(r.subprocess,'Popen',side_effect=popen),patch.object(r.subprocess,'check_output',return_value=r.config()['expected_cli_versions']['B']),patch.object(r,'git',return_value=b'commit'),patch.object(r.uuid,'uuid4',return_value='s'):
            d=Path(td)/'attempt';v=r.execute('B',d,'fixture',stage='prospective');self.assertEqual(v['status'],'failed');self.assertEqual(r.read(d/'response.json'),invalid)
        events.insert(2,copy.deepcopy(events[1]));meta,_=r.legacy.audit_events(events,'B','claude-fable-5-1[1m]','s');self.assertEqual(meta['formatting_retries']['observed_formatting_retries'],1)
    def test_model_tool_plugin_rejection(self):
        for field,value in [('model','wrong'),('tools',['Read']),('plugins',['bad'])]:
            e={'type':'system','subtype':'init','session_id':'s','model':'claude-fable-5-1','tools':[],'plugins':[],'mcp_servers':[]};e[field]=value
            with self.assertRaises(ValueError):r.legacy.audit_events([e],'B','claude-fable-5-1[1m]','s')

if __name__=='__main__':unittest.main()
