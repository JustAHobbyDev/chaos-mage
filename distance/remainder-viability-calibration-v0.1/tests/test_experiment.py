import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import runner as r
import contracts as c
from audit_authoring import verify as author_verify

class ExperimentTests(unittest.TestCase):
    def test_corpus_and_authoring_gate(self):
        result=r.verify();self.assertEqual(len(result['cases']),16);self.assertEqual(result['claims'],57)
        self.assertTrue(author_verify()['passed'])
        audit=c.read(r.H/'authoring-audit/primary.json')
        self.assertEqual(len(audit['case_audits']),12)
        for a in audit['case_audits']:
            self.assertEqual(bool(a['viable_remainders']),a['pair_role']=='reduced')
            self.assertFalse(a['decisively_unresolved_candidates'])
        self.assertTrue(all(b['max_min_ratio']<=1.15 for b in audit['surface_balance']))

    def test_accepted_sources_and_same_target_focal(self):
        import yaml
        instruments=[yaml.safe_load(p.read_text()) for p in (r.R/'instruments').glob('*.yaml')]
        for t in c.read(r.H/'targets.json'):
            original=c.read(r.R/t['source_input_path']);self.assertEqual(t['source'],original['source'])
            self.assertEqual(c.sha(r.R/t['source_input_path']),t['source_input_sha256'])
            matches=[i for i in instruments if i['extraction']['name']==t['source']['name']]
            self.assertEqual(matches[0]['extraction']['status'],'accepted');self.assertEqual(matches[0]['instrument'],t['source']['instrument'])
        for pair in c.read(r.H/'hidden-design/pairs.json'):
            a,b=[r.candidate(cid) for cid in pair['case_ids']]
            self.assertEqual(a['target'],b['target']);self.assertEqual(a['source'],b['source'])
            designs=[c.read(r.H/'hidden-design'/f'{cid}.json') for cid in pair['case_ids']]
            self.assertEqual(designs[0]['focal_object'],designs[1]['focal_object'])

    def test_allowlisted_packets(self):
        for a in r.claims():
            packet=r.reconstructed_claim_packet(a);body=json.loads(packet.split('CASE PACKET\n')[1])
            self.assertEqual(set(body),{'source','target','mapping','atomic_claim'})
            for forbidden in ['pair_role','control_purpose','authoring_gate_passed','hypothesis','viable_remainders']:
                self.assertNotIn('"'+forbidden+'"',packet)

    def test_exact_simultaneous_deletion_empty_and_overlap(self):
        mapping={'inference':'first. middle. last.'}
        atoms=[{'claim_id':'C1','source_field':'mapping.inference','span_start':0,'span_end':6,'exact_claim_span':'first.'},
               {'claim_id':'C2','source_field':'mapping.inference','span_start':15,'span_end':20,'exact_claim_span':'last.'}]
        self.assertEqual(r.delete_claims(mapping,[]) ,mapping)
        self.assertEqual(r.delete_claims(mapping,atoms)['inference'],'[DELETED C1] middle. [DELETED C2]')
        with self.assertRaises(ValueError):r.delete_claims(mapping,atoms+atoms[:1])

    def test_isolation_and_event_audit(self):
        r.binary_check();cmd=r.command('/tmp/empty',Path('/tmp/evidence'),'claim-warrant')
        for option in ['--ignore-user-config','--ignore-rules','--ephemeral','gpt-6-astra','model_reasoning_effort="high"','project_doc_max_bytes=0','web_search="disabled"']:
            self.assertIn(option,cmd)
        with patch.dict(r.os.environ,{'OPENAI_MODEL':'other','CODEX_THREAD_ID':'old'}):
            self.assertNotIn('OPENAI_MODEL',r.clean_env());self.assertNotIn('CODEX_THREAD_ID',r.clean_env())
        events=[{'type':'thread.started','thread_id':'fresh'},{'type':'turn.completed','usage':{}}]
        self.assertEqual(r.audit_events(events)['session_id'],'fresh')
        for extra in [{'type':'x','model':'other'},{'type':'item.completed','item':{'type':'command_execution'}},{'type':'error'}]:
            with self.assertRaises(ValueError):r.audit_events(events+[extra])

    def test_terminal_state_and_reservation_prevent_launch(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(r,'RT',Path(tmp)),patch.object(r,'execute') as execute:
            r.transition('TERMINATED_MEASUREMENT','fixture')
            with self.assertRaises(ValueError):r.run('claim-warrant')
            execute.assert_not_called()
        with tempfile.TemporaryDirectory() as tmp,patch.object(r,'RT',Path(tmp)),patch.object(r,'execute') as execute:
            (Path(tmp)/'runs/claim-warrant/C-existing').mkdir(parents=True)
            with self.assertRaises(ValueError):r.run('claim-warrant')
            execute.assert_not_called()

if __name__=='__main__':unittest.main()
