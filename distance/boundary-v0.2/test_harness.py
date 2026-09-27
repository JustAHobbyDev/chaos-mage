import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('boundary_harness',Path(__file__).with_name('harness.py'))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)

class BoundaryTests(unittest.TestCase):
    def sample(self,cid='001'):
        c=copy.deepcopy(h.read(h.ROOT/'distance/judgments/CASE-008-A.json'))
        c['classification']['case_id']=cid
        c['classification']['axes']={'displacement':{'level':'low','rationale':'test'},'grounding':{'status':'grounded','rationale':'test'}}
        c['classification']['boundary_evidence']={k:'test' for k in ('changes_what_is_done','changes_what_is_observed','changes_what_is_inferred','invented_counterparts')}
        return c
    def run_spec(self):return {'id':'primary-001-A','condition':'primary','case_id':'001','family':'A'}
    def test_preservation_sources_controls(self):self.assertEqual(len(h.validate_inputs()),16)
    def test_exact_control_packets_and_schema(self):
        for run in h.order():
            if run['condition']!='control':continue
            cid=h.response_id(run)
            expected=(h.ROOT/'distance/CLASSIFIER-v0.1.md').read_text()+'\n\nCASE PACKET\n'+(h.ROOT/'distance/cases'/f'{cid}.yaml').read_text()
            self.assertEqual(h.packet(run),expected)
            self.assertEqual(h.schema_path(run).read_bytes(),(h.ROOT/'distance/output.schema.json').read_bytes())
    def test_pair_differences(self):
        cs=h.validate_inputs()
        for a,b in [('004','005'),('006','007')]:self.assertEqual(cs[a]['target'],cs[b]['target'])
        for a,b,prefix,suffix in [('010','011','An organization investigates how internal coordination produces delays and bottlenecks in requests moving among teams. ',' Explain which coordination structures account for the observed outcomes and the limits of that explanation.'),('012','013','A team studies a proposal composed of interwoven idea fragments. ',' Determine which components can be distinguished and what evidence supports that decomposition.'),('014','015','A leadership team investigates which persistent strategic assumptions shape its decisions. ',' Identify the assumptions and what evidence supports claims that they persist.')]:
            self.assertEqual(cs[a]['source'],cs[b]['source'])
            self.assertEqual(cs[a]['target']['domain'],cs[b]['target']['domain'])
            for cid in (a,b):
                self.assertTrue(cs[cid]['target']['problem'].startswith(prefix));self.assertTrue(cs[cid]['target']['problem'].endswith(suffix))
            self.assertNotEqual(cs[a]['target']['problem'],cs[b]['target']['problem'])
        self.assertEqual(cs['003']['target']['problem'].replace('Only the final text and limited publication context survive.','The final text, limited publication context, dated draft fragments, and publication correspondence survive.'),cs['004']['target']['problem'])
    def test_original_dimensions_unchanged(self):
        old=h.read(h.ROOT/'distance/output.schema.json')['properties']['classification']['properties'];new=h.read(h.HERE/'output.schema.json')['properties']['classification']['properties']
        for k in old:self.assertEqual(old[k],new[k])
        oldtext=(h.ROOT/'distance/CLASSIFIER-v0.1.md').read_text();newtext=(h.HERE/'CLASSIFIER-tested.md').read_text()
        self.assertEqual(oldtext[oldtext.index('## Profiles:'):oldtext.index('## Naturalization')],newtext[newtext.index('## Profiles:'):newtext.index('## Naturalization')])
    def test_schema_and_semantic_tensions(self):
        value=self.sample();run=self.run_spec();h.validate_judgment(value,run)
        value['classification']['final_class']='Alien' # Inconsistent but structural validity retained.
        h.validate_judgment(value,run)
        for change in ('missing','extra','range','bool','float','enum','empty','wrong_id'):
            bad=copy.deepcopy(value);c=bad['classification']
            if change=='missing':del c['axes']
            if change=='extra':c['extra']=1
            if change=='range':c['displacement']['entities']['level']=4
            if change=='bool':c['displacement']['entities']['level']=True
            if change=='float':c['displacement']['entities']['level']=1.0
            if change=='enum':c['axes']['displacement']['level']='medium'
            if change=='empty':c['boundary_evidence']['invented_counterparts']=''
            if change=='wrong_id':c['case_id']='999'
            with self.assertRaises((ValueError,h.jsonschema.ValidationError)):h.validate_judgment(bad,run)
    def test_duplicate_json_yaml_and_nonfinite(self):
        with tempfile.TemporaryDirectory() as td:
            for name,text in [('a.json','{"a":1,"a":2}'),('b.yaml','a: 1\na: 2'),('c.json','{"a":NaN}')]:
                p=Path(td)/name;p.write_text(text)
                with self.assertRaises(ValueError):h.read(p)
    def test_known_metrics_and_off_band(self):
        a=self.sample()['classification'];b=copy.deepcopy(a);a['final_class']='Native';b['final_class']='Alien'
        for d in h.DIMS:a['displacement'][d]['level']=0;b['displacement'][d]['level']=2
        m=h.metrics([(a,a),(a,b)])
        self.assertEqual(m['final_class']['exact_rate'],.5)
        self.assertEqual(m['dimensions']['entities']['mean_absolute_disagreement'],1)
        self.assertEqual(m['class_distributions']['B'],{'Native':1,'Alien':1})
        self.assertFalse(h.side('Native','Adjacent/Remote'));self.assertTrue(h.side('Alien','Adjacent/Remote'))
        self.assertFalse(h.side('Remote','Remote/Alien'));self.assertTrue(h.side('Alien','Remote/Alien'))
        self.assertNotIn('axes',h.metrics([(a,b)],axes=False))
    def test_run_coverage_and_reused_sessions(self):
        entries=[{'id':r['id'],'audit':{'metadata':{'session_id':r['id']}}} for r in h.order()]
        h.check_runs(entries)
        with self.assertRaises(ValueError):h.check_runs(entries[:-1])
        entries[-1]['audit']['metadata']['session_id']=entries[0]['audit']['metadata']['session_id']
        with self.assertRaises(ValueError):h.check_runs(entries)
    def test_codex_metadata_unavailable_and_fallback(self):
        events=[{'type':'thread.started','thread_id':'one'},{'type':'turn.completed'}]
        meta,_=h.audit_events(events,'A','gpt-6-astra')
        self.assertIsNone(meta['verified_served_snapshot']);self.assertEqual(meta['returned_model_identifiers'],[])
        events[0]['model']='different-model'
        with self.assertRaises(ValueError):h.audit_events(events,'A','gpt-6-astra')
    def claude_events(self):
        return [{'type':'system','subtype':'init','session_id':'s','model':'claude-fable-5-1','tools':['StructuredOutput'],'plugins':[],'mcp_servers':[]},{'type':'assistant','message':{'model':'claude-fable-5-1','content':[{'type':'tool_use','name':'StructuredOutput','input':{}}]}},{'type':'result','subtype':'success','session_id':'s','structured_output':{'x':1},'num_turns':1,'modelUsage':{'claude-fable-5-1':{}}}]
    def test_claude_internal_formatting_retries_and_model_fallback(self):
        e=self.claude_events();e.insert(2,copy.deepcopy(e[1]))
        meta,payload=h.audit_events(e,'B','claude-fable-5-1[1m]','s')
        self.assertEqual(meta['formatting_retries']['observed_formatting_retries'],1)
        self.assertEqual(payload,{'x':1})
        e[1]['message']['model']='different-model'
        with self.assertRaises(ValueError):h.audit_events(e,'B','claude-fable-5-1[1m]','s')
    def test_tools_and_invalid_output(self):
        for field in ('tool','missing','session','error'):
            e=self.claude_events()
            if field=='tool':e[1]['message']['content'][0]['name']='Read'
            if field=='missing':del e[-1]['structured_output']
            if field=='session':e[0]['session_id']='reused'
            if field=='error':e[-1]['is_error']=True
            with self.assertRaises(ValueError):h.audit_events(e,'B','claude-fable-5-1[1m]','s')
    def test_analysis_keeps_primary_controls_and_off_band_separate(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);(base/'judgments').mkdir();runs=[]
            for run in h.order():
                payload=self.sample(h.response_id(run));c=payload['classification']
                c['final_class']='Alien' if run['condition']=='control' else 'Native'
                if run['condition']=='control':
                    del c['axes'];del c['boundary_evidence']
                p=base/'judgments'/f'{run["id"]}.json';h.write_new(p,payload)
                runs.append({**run,'files':{'response.json':h.sha(p.read_bytes())}})
            # Keep real validation and schemas; only redirect published result reads.
            original_read=h.read
            def local_read(path):
                if path.parent==h.HERE/'judgments':return original_read(base/'judgments'/path.name)
                return original_read(path)
            original_sha=h.sha
            with patch.object(h,'frozen_results',return_value={'runs':runs}),patch.object(h,'read',side_effect=local_read),patch.object(Path,'read_bytes',autospec=True) as read_bytes:
                real_read_bytes=Path.open
                def bytes_for(path):
                    p=base/'judgments'/path.name if path.parent==h.HERE/'judgments' else path
                    with real_read_bytes(p,'rb') as stream:return stream.read()
                read_bytes.side_effect=bytes_for
                result=h.analyze()
            self.assertEqual(result['primary']['final_class']['n'],16)
            self.assertEqual(result['supplementary']['final_class']['n'],3)
            self.assertEqual(result['primary']['class_distributions']['A'],{'Native':16})
            self.assertEqual(result['supplementary']['class_distributions']['A'],{'Alien':3})
            for b in result['boundaries'].values():
                self.assertEqual(b['side_agreement']['exact_count'],8)
                self.assertFalse(b['both_sides_exercised'])
                self.assertEqual(len(b['out_of_band']),8)
    def test_exclusive_write(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.json';h.write_new(p,{'x':1})
            with self.assertRaises(FileExistsError):h.write_new(p,{'x':2})
    def test_timeout_is_preserved(self):
        class Process:
            pid=999999
            def communicate(self,*args,**kwargs):raise subprocess.TimeoutExpired('fake',900)
            def wait(self):return -9
        with tempfile.TemporaryDirectory() as td,patch.object(h.subprocess,'Popen',return_value=Process()),patch.object(h.subprocess,'check_output',return_value='fake'),patch.object(h,'git',return_value=b'fake'),patch.object(h.os,'killpg') as kill:
            result=h.execute('A',Path(td)/'attempt','probe',h.HERE/'probe.schema.json')
            self.assertEqual(result['status'],'failed');self.assertIn('TimeoutExpired',result['error']);kill.assert_called_once()
            self.assertTrue((Path(td)/'attempt/validation.json').exists())
    def test_stop_scheduling_on_failure(self):
        with tempfile.TemporaryDirectory() as td,patch.object(h,'RUNTIME',Path(td)),patch.object(h,'verify'),patch.object(h,'git',return_value=b'fake'),patch.object(h,'execute',return_value={'status':'failed','error':'test'}) as execute,patch.object(h,'read',return_value={'families':{'A':{'cli_version':'fake'},'B':{'cli_version':'fake'}}}),patch.object(h,'config',return_value={'families':{'A':{'cli':'codex'},'B':{'cli':'claude'}}}),patch.object(h.subprocess,'check_output',return_value='fake'),patch.object(h,'order',return_value=[self.run_spec()]),patch.object(h,'packet',return_value='test'):
            with self.assertRaises(ValueError):h.run_all()
            self.assertEqual(execute.call_count,1);self.assertTrue((Path(td)/'STOP.json').exists())
    def test_hash_and_commit_gate(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);b=root/'boundary';b.mkdir();p=b/'input';p.write_text('original')
            h.write_new(b/'prepared.json',{'files':{'boundary/input':h.sha(p.read_bytes())},'packets':{}})
            with patch.object(h,'ROOT',root),patch.object(h,'HERE',b),patch.object(h,'validate_inputs'),patch.object(h,'order',return_value=[]),patch.object(h,'git',return_value=b'not committed'):
                h.verify()
                with self.assertRaises(ValueError):h.verify(committed=True)
                p.write_text('changed')
                with self.assertRaises(ValueError):h.verify()

if __name__=='__main__':unittest.main()
