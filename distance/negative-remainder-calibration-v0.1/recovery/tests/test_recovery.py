import copy
import itertools
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import contracts as c
import runner as r
import recovery as x

class RecoveryTests(unittest.TestCase):
    def args(self):
        cid=x.AFFECTED
        return [c.read(r.RT/'runs/artifact'/cid/'response.json'),'artifact',cid,r.candidate(cid),r.unsupported(cid),c.read(r.H/'negative-remainders'/f'{cid}.json')['candidates']]
    def test_original_failure_and_unchanged_supplement(self):
        args=self.args();before=copy.deepcopy(args[0])
        with self.assertRaisesRegex(ValueError,'Absent conflict'):x.ORIGINAL_VALIDATE(*args)
        x.validate(*args);self.assertEqual(args[0],before)
    def test_both_absent_encodings_same_science(self):
        args=self.args()
        for resolved in [False,True]:
            args[0]['remainder_viability']['structural_conflict']['resolved']=resolved;x.validate(*args)
    def test_invalid_identity_and_status_rejected(self):
        for key,value in [('case_id','wrong'),('artifact_status','CORE_INVALID')]:
            args=self.args();args[0]['remainder_viability'][key]=value
            with self.assertRaises(ValueError):x.validate(*args)
    def test_candidate_loss_and_invention_rejected(self):
        args=self.args();args[0]['remainder_viability']['candidate_remainders'].pop()
        with self.assertRaises(ValueError):x.validate(*args)
        args=self.args();args[0]['remainder_viability']['candidate_remainders'][0]['source_spans'][0]['exact_text']='invented'
        with self.assertRaises(ValueError):x.validate(*args)
    def test_productivity_and_inquiry_assertions_retained(self):
        args=self.args();args[0]['negative_remainder_assessment']['candidates'][0]['productive']='YES'
        with self.assertRaises(ValueError):x.validate(*args)
        args=self.args();a=args[0]['negative_remainder_assessment']['candidates'][0];a['counterfactual_effect']['next_inquiry']='changed'
        with self.assertRaises(ValueError):x.validate(*args)
    def test_metadata_cannot_change_any_viability_combination(self):
        for values in itertools.product(c.YESNO,repeat=5):
            row={k:{'status':v,'rationale':'fixture'} for k,v in zip(c.DIMENSIONS,values)}
            scope='reduced' if all(v=='YES' for v in values) else 'none'
            expected=c.derive([row],scope)
            for p,q in itertools.product([False,True],repeat=2):self.assertEqual(c.derive([row],scope,{'present':p,'resolved':q}),expected)
    def test_packet_schema_response_session_unchanged(self):
        evidence=x.proof_check();self.assertEqual(evidence['remaining_unreserved'],r.order('artifact')[3:])
        self.assertEqual(evidence['completed_or_sent'],r.order('artifact')[:3])
        for cid in evidence['completed_or_sent']:
            d=r.RT/'runs/artifact'/cid
            self.assertEqual((d/'prompt.txt').read_bytes(),r.packet('artifact',cid).read_bytes())
            self.assertEqual(c.read(d/'reservation.json')['schema_sha256'],c.sha(r.H/'schemas/artifact.schema.json'))
        self.assertEqual(c.read(r.RT/'runs/artifact'/x.AFFECTED/'validation.json')['status'],'failed')

if __name__=='__main__':unittest.main()
