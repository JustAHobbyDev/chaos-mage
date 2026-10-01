import copy
import itertools
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import contracts as c

def assessment(values):
    return {d:{'status':v,'rationale':'fixture evidence'} for d,v in zip(c.DIMENSIONS,values)}

class DerivationTests(unittest.TestCase):
    def test_all_81_candidate_combinations(self):
        for values in itertools.product(c.YESNO,repeat=4):
            row=assessment(values)
            expected='CORE_INVALID' if 'NO' in values else 'UNCERTAIN_LOAD_BEARING' if 'UNCERTAIN' in values else 'KEEP_WITH_REDUCED_SCOPE'
            self.assertEqual(c.derive([row],'reduced' if expected.startswith('KEEP') else 'none'),expected,values)

    def test_mixed_candidates_and_scope(self):
        yes=assessment(['YES']*4);unknown=assessment(['YES','YES','UNCERTAIN','YES']);no=assessment(['NO','YES','UNCERTAIN','YES'])
        self.assertEqual(c.derive([no,unknown,yes],'substantially_intact'),'KEEP_WITH_WARRANT_FLAGS')
        self.assertEqual(c.derive([no,unknown,yes],'reduced'),'KEEP_WITH_REDUCED_SCOPE')
        self.assertEqual(c.derive([no,unknown],'uncertain'),'UNCERTAIN_LOAD_BEARING')
        self.assertEqual(c.derive([no],'none'),'CORE_INVALID')
        self.assertEqual(c.derive([],'none'),'CORE_INVALID')

    def test_conflict_exception_and_invalid_scope(self):
        row=assessment(['YES']*4)
        with self.assertRaises(ValueError):c.derive([row],'none')
        for rows in [[],[row],[assessment(['NO']*4)]]:
            self.assertEqual(c.derive(rows,'none',{'present':True,'resolved':False}),'UNCERTAIN_LOAD_BEARING')

    def test_schema_and_duplicate_key_rejection(self):
        for stage in ['claim-warrant','artifact']:c.jsonschema.Draft202012Validator.check_schema(c.schema(stage))
        with self.assertRaises(ValueError):c.unique([('status','YES'),('status','NO')])

class ValidationTests(unittest.TestCase):
    def fixture(self):
        case={'mapping':{'inference':'Defect. Useful survivor.'}}
        deleted=[{'claim_id':'C-x','source_field':'mapping.inference','span_start':0,'span_end':7}]
        spans=[{'source_field':'mapping.inference','exact_text':'Useful survivor.'}]
        frozen=[{'remainder_id':'R1','inference':'Useful survivor.','source_spans':spans}]
        row={**frozen[0],'origin':'frozen',**assessment(['YES']*4)}
        def comp(status):return {'status':status,'rationale':'fixture rationale'}
        a={'case_id':'H2-x','unsupported_claim_ids':['C-x'],'candidate_remainders':[row],
           'viable_remainders':['R1'],'strongest_surviving_target_inference':{'remainder_id':'R1','text':'Useful survivor.','source_spans':spans,'why_warranted':'fixture warrant'},
           'scope_survival':comp('reduced'),'mechanism_survival':comp('PARTIALLY_SURVIVES'),
           'remainder_check':comp('DISTINCTIVE_REMAINDER'),'target_contribution_survival':comp('REDUCED_BUT_MATERIAL'),
           'dependency_cascade':comp('GLOBAL'),'central_bridge':{'deleted_claim_is_required_for_all_material_contributions':'no','rationale':'survivor bypasses it'},
           'no_viable_remainder_reason':'none','artifact_status':'KEEP_WITH_REDUCED_SCOPE',
           'structural_conflict':{'present':False,'resolved':True,'explanation':'no conflict'},'uncertainty':[]}
        return {'remainder_viability':a},case,deleted,frozen

    def valid(self,value,case,deleted,frozen):c.validate(value,'artifact','H2-x',case,deleted,frozen)

    def test_viable_reduced_and_diagnostic_centrality(self):
        args=self.fixture();self.valid(*args)
        args[0]['remainder_viability']['central_bridge']['deleted_claim_is_required_for_all_material_contributions']='uncertain'
        self.valid(*args)

    def test_core_cannot_contain_viable_or_unresolved_candidate(self):
        value,case,deleted,frozen=self.fixture();a=value['remainder_viability']
        a['artifact_status']='CORE_INVALID';a['scope_survival']['status']='none';a['no_viable_remainder_reason']='mechanism_death'
        with self.assertRaises(ValueError):self.valid(value,case,deleted,frozen)
        a['candidate_remainders'][0]['material']['status']='UNCERTAIN';a['viable_remainders']=[]
        with self.assertRaises(ValueError):self.valid(value,case,deleted,frozen)

    def test_keep_requires_definite_candidate(self):
        args=self.fixture();a=args[0]['remainder_viability'];a['candidate_remainders'][0]['source_derived']['status']='NO';a['viable_remainders']=[]
        with self.assertRaises(ValueError):self.valid(*args)

    def test_added_candidate_allowed_and_missing_frozen_rejected(self):
        args=self.fixture();a=args[0]['remainder_viability']
        row=copy.deepcopy(a['candidate_remainders'][0]);row.update(remainder_id='NEW1',origin='judge_added');row['material']['status']='NO'
        a['candidate_remainders'].append(row);self.valid(*args)
        a['candidate_remainders']=a['candidate_remainders'][1:]
        with self.assertRaises(ValueError):self.valid(*args)

    def test_deleted_citations_and_changed_inventory_rejected(self):
        args=self.fixture();args[0]['remainder_viability']['candidate_remainders'][0]['inference']='Invented replacement'
        with self.assertRaises(ValueError):self.valid(*args)
        with self.assertRaises(ValueError):c.cited_spans([{'source_field':'mapping.inference','exact_text':'Defect.'}],args[1],args[2],surviving=True,mapping_only=True)

    def test_unresolved_structural_conflict(self):
        args=self.fixture();a=args[0]['remainder_viability']
        a.update(artifact_status='UNCERTAIN_LOAD_BEARING',no_viable_remainder_reason='uncertain',uncertainty=['unreconciled structural contradiction'],structural_conflict={'present':True,'resolved':False,'explanation':'unreconciled scope'})
        self.valid(*args)

    def test_empty_deletion_set_is_valid(self):
        value,case,_,frozen=self.fixture();value['remainder_viability']['unsupported_claim_ids']=[]
        self.valid(value,case,[],frozen)

if __name__=='__main__':unittest.main()
