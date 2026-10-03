from copy import deepcopy
from pathlib import Path
import sys,unittest
H=Path(__file__).resolve().parents[4];sys.path.insert(0,str(H))
import runner as r
import contracts as c
import recovery as x

class MetadataRecovery(unittest.TestCase):
    def args(self):
        return ['obligation',r.read(x.REC/'original/response.json'),r.read(H/'obligation-packets/K12-C1.json'),
                r.read(H/'schemas/obligation.schema.json'),r.taxonomy()]
    def test_original_rejection_and_unchanged_supplement(self):
        args=self.args();before=deepcopy(args[1])
        with self.assertRaisesRegex(ValueError,'Embedded classification identity mismatch'):x.ORIGINAL(*args)
        ds=x.validate(*args);self.assertEqual(args[1],before)
        self.assertEqual([d['code'] for d in ds],['DEPENDENCY_UNCERTAIN'])
    def test_both_frozen_schemas_accept_original(self):
        for name in ('obligation.schema.json','obligation-wire.schema.json'):
            c.Draft202012Validator(r.read(H/'schemas'/name)).validate(self.args()[1])
    def test_cannot_change_scientific_fields(self):
        for key,val in [('closure_status','COMPLETE'),('claim_id','K11-C1')]:
            args=self.args();args[1]['claim_obligation_set'][key]=val
            with self.assertRaises(Exception):x.validate(*args)
    def test_changed_function_rejected(self):
        args=self.args();args[1]['embedded_classifications'][0]['epistemic_function']='FACT'
        with self.assertRaises(ValueError):x.validate(*args)
    def test_changed_referent_or_rationale_rejected(self):
        for key in ('subject','rationale'):
            args=self.args();args[1]['embedded_classifications'][0][key]='changed'
            with self.assertRaises(ValueError):x.validate(*args)
    def test_omitted_or_unlinked_uncertainty_rejected(self):
        for value in ([],['Unlinked explanation']):
            args=self.args();args[1]['claim_obligation_set']['unresolved_dependencies']=value
            with self.assertRaises(ValueError):x.validate(*args)
    def test_bounded_linkage_predicate(self):
        v=self.args()[1];self.assertTrue(x.unresolved_linkage(v))
        for key in ('../D1','D2','D10'):
            v=self.args()[1];v['embedded_classifications'][0]['dependency_id']=key
            self.assertFalse(x.unresolved_linkage(v))
    def test_no_scientific_operation_is_invented(self):
        a=r.read(H/'classification-judgments/K12-C1.json');v=self.args()[1]
        jobs=c.obligation_jobs(r.claims()['K12-C1'][0],a,v)
        self.assertEqual([j['contract'] for j in jobs],['GOVERNANCE_COHERENCE'])
    def test_closure_cannot_pass_even_if_governance_passes(self):
        a=r.read(H/'classification-judgments/K12-C1.json');v=self.args()[1]
        for verdict in c.RANK:
            evals={('K12-C1','B1'):{'contract':'GOVERNANCE_COHERENCE','verdict':verdict}}
            result=c.aggregate({'K12-C1':a},{'K12-C1':v},evals,r.taxonomy())['K12-C1']['overall']
            self.assertEqual(result,'VIOLATED' if verdict=='VIOLATED' else 'UNCERTAIN')
    def test_other_twenty_five_observations_unchanged_validation(self):
        for stage in ('classification','obligation'):
            for p in (H/(stage+'-judgments')).glob('*.json'):
                if stage=='obligation' and p.stem=='K12-C1':continue
                args=[stage,r.read(p),r.read(H/(stage+'-packets')/p.name),r.read(H/'schemas'/(stage+'.schema.json')),r.taxonomy()]
                self.assertEqual(x.validate(*args),x.ORIGINAL(*args))

if __name__=='__main__':unittest.main()
