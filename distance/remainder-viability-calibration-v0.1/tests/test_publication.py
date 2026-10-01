"""Post-freeze lineage and operator-review checks; never run provider calls."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import contracts as c
import runner as r

class PublicationTests(unittest.TestCase):
    def test_every_response_retains_original_bytes_and_global_session_identity(self):
        sessions=[]
        for stage in r.STAGES:
            freeze=c.read(r.H/f'{stage}-freeze.json')
            self.assertEqual([x['identity'] for x in freeze['runs']],r.order(stage))
            for row in freeze['runs']:
                response=r.H/'judgments'/stage/f'{row["identity"]}.json'
                self.assertEqual(response.read_bytes(),(r.RT/'runs'/stage/row['identity']/'response.json').read_bytes())
                self.assertEqual(c.sha(response),row['response_sha256'])
                sessions.append(row['validation']['metadata']['session_id'])
        self.assertEqual(len(sessions),73);self.assertEqual(len(set(sessions)),73)

    def test_candidate_coverage_derivation_and_no_repair(self):
        frozen=added=0
        for cid in c.read(r.H/'manifest.json')['case_order']:
            inventory=c.read(r.H/'remainder-candidates'/f'{cid}.json')['candidates']
            value=c.read(r.H/'judgments/artifact'/f'{cid}.json')
            c.validate(value,'artifact',cid,r.candidate(cid),r.unsupported(cid),inventory)
            a=value['remainder_viability'];frozen+=len(inventory)
            added+=sum(x['origin']=='judge_added' for x in a['candidate_remainders'])
            self.assertEqual(r.ablation_body(cid)['ablated_mapping'],r.delete_claims(r.candidate(cid)['mapping'],r.unsupported(cid)))
        self.assertEqual(frozen,88);self.assertEqual(added,12)

    def test_freezes_precede_dependent_stages_and_review(self):
        claim_freeze=c.read(r.H/'claim-warrant-freeze.json')
        artifact_freeze=c.read(r.H/'artifact-freeze.json')
        review=c.read(r.H/'review/operator.json')
        self.assertLess(claim_freeze['at'],min(x['reservation']['at'] for x in artifact_freeze['runs']))
        self.assertLess(artifact_freeze['at'],review['at'])
        self.assertEqual(review['artifact_freeze_sha256'],c.sha(r.H/'artifact-freeze.json'))
        for row in artifact_freeze['runs']:
            import subprocess
            subprocess.check_call(['git','merge-base','--is-ancestor',c.read(r.H/'artifact-manifest.json')['claim_freeze_commit'],row['reservation']['input_commit']],cwd=r.R)
        for row in review['case_reviews']:
            self.assertEqual(row['judgment_sha256'],c.sha(r.H/'judgments/artifact'/f'{row["case_id"]}.json'))
            self.assertEqual(len(row['questions']),8)
            a=c.read(r.H/'judgments/artifact'/f'{row["case_id"]}.json')['remainder_viability']
            self.assertEqual(row['all_candidates_inspected'],[x['remainder_id'] for x in a['candidate_remainders']])
        self.assertEqual(len(review['pair_reviews']),6)
        self.assertFalse(review['model_outputs_rewritten'])

if __name__=='__main__':unittest.main()
