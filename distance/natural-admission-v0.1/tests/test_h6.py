import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H))
import contracts as c
import runner as r

class CollisionTests(unittest.TestCase):
    def setUp(self):
        self.a=c.h5.segment('A',dict(state='Baseline.',operation='Procedure.',signal='Inspect evaluator scores next.',inference='No conclusion.',limit='Bound.'))
        self.b=c.h5.segment('B',dict(state='Baseline.',operation='Procedure.',signal='Offsets +2 through +5 are incompatible.',inference='No conclusion.',limit='Bound.'))
    def test_separate_contexts_vs_simultaneous_exposure(self):
        self.assertFalse(c.exposure([self.a]));self.assertFalse(c.exposure([self.b]));self.assertTrue(c.exposure([self.a,self.b]))
        self.assertFalse(c.collision_failure(simultaneous=True,reused=True,bare_citation=True,accepted_or_ambiguous=True))
    def test_envelope_resolution_no_global_fallback(self):
        self.assertEqual(c.resolve(self.a,'A','P003')['text'],'Inspect evaluator scores next.')
        with self.assertRaisesRegex(ValueError,'PROV_WRONG_PACKET'):c.resolve(self.a,'B','P003')
    def test_strongest_example_needs_semantic_evidence(self):
        # Recorded engineering review: B's assertion is NOT supported by A/P003.
        comp={'component_id':'C','value':'Offsets +2 through +5 are incompatible.','scope':'offsets',
              'provenance':{'refs':[{'source_id':'P003','role':'SUPPORT'}],'support_status':'INSUFFICIENT','rationale':'A/P003 selects inquiry; the claim comes from B/P003.'}}
        self.assertEqual(c.citation_checks(self.a,{'packet_id':'A','components':[comp]}),[])
        # Deliberately false semantic acceptance in two-packet context is a collision failure.
        facts=dict(simultaneous=True,reused=True,bare_citation=True,accepted_or_ambiguous=True,wrong_packet_material=True)
        self.assertTrue(c.collision_failure(**facts))
        for key in facts:
            omitted={**facts,key:False};self.assertFalse(c.collision_failure(**omitted),key)
        # Detected/rejected semantic mismatch does not become an accepted false provenance result.
        self.assertFalse(c.collision_failure(**{**facts,'accepted_or_ambiguous':False}))
    def test_single_packet_wrong_citation_is_not_collision(self):
        self.assertFalse(c.collision_failure(simultaneous=False,reused=False,bare_citation=True,accepted_or_ambiguous=True,wrong_packet_material=True))
    def test_legitimate_cross_packet_impossibility(self):
        self.assertTrue(c.collision_failure(simultaneous=True,reused=True,bare_citation=False,accepted_or_ambiguous=False,cross_packet_impossible=True))
    def test_genuinely_ambiguous_packet(self):
        self.assertTrue(c.collision_failure(simultaneous=True,reused=True,bare_citation=True,accepted_or_ambiguous=True,reviewer_ambiguity_material=True))

class HistoricalAndPipelineTests(unittest.TestCase):
    def test_h5_twenty_historical_tables_reproduce(self):
        old=H.with_name('span-provenance-calibration-v0.1');tables=list((old/'span-tables').glob('*.json'))
        self.assertEqual(len(tables),20)
        for source in json.loads((old/'manifest.json').read_text())['sources']:
            mapping=json.loads((H.parents[1]/source['path']).read_text())['mapping']
            table=json.loads((old/'span-tables'/(source['packet_id']+'.json')).read_text())
            self.assertEqual(table,c.h5.segment(source['packet_id'],mapping))
            c.h5.verify_table(table,mapping)
    def test_no_required_exact_citation_fields(self):
        forbidden={'exact_text','start','end','byte_offset','character_offset'}
        def walk(v):
            if isinstance(v,dict):
                self.assertFalse(forbidden & set(v.get('properties',{})))
                self.assertFalse(forbidden & set(v.get('required',[])))
                for x in v.values():walk(x)
            elif isinstance(v,list):
                for x in v:walk(x)
        for p in (H/'schemas').glob('*.json'):walk(json.loads(p.read_text()))
    def test_shared_span_deletion_does_not_poison_other_claim(self):
        def atom(cid,value):return {'claim_id':cid,'fields':['inference'],'component':{'component_id':cid,'value':value,'scope':'conditional','provenance':{'refs':[{'source_id':'P004','role':'SUPPORT'}],'support_status':'SUFFICIENT','rationale':'shared span'}}}
        atoms={'packet_id':'A','claims':[atom('C001','Unsupported leap'),atom('C002','Qualified surviving bound'),atom('C003','Uncertain distinction')]}
        js=[{'claim_id':'C001','status':'UNSUPPORTED'},{'claim_id':'C002','status':'SUPPORTED'},{'claim_id':'C003','status':'UNCERTAIN'}]
        out=c.ablate(atoms,js)
        self.assertEqual(out['deleted_claim_ids'],['C001']);self.assertEqual(out['surviving_claims'],atoms['claims'][1:])
        self.assertEqual(out['lineage'][1]['original_claim_sha256'],c.h5.canonical_hash(atoms['claims'][1]))
    def test_h4_complete_affirmative_unit_requires_role(self):
        comp={'value':'affirmative next operation'}
        u={'unit_id':'U1','alternatives':[comp,comp],'unresolved_contrast':comp,'next_operation':comp,'outcomes':[comp,comp],'outcomes_are_discriminating':True,'provenance_complete':True,'complete':True}
        value={'packet_id':'A','candidates':[],'inquiry_units':[u],'field_coverage':[{'field':f} for f in c.FIELDS],'deleted_claims_used':[]}
        result=c.semantic_checks('remainder-inventory',value,{'packet_id':'A','ablation':{'surviving_claims':[]}})
        self.assertIn('IQ_MISSING_OR_DUPLICATE_ROLE',[e['code'] for e in result])
    def test_insufficiency_does_not_establish_viability(self):
        candidate={'viability':{f:{'value':('NO' if f=='productive' else 'YES')} for f in ['warranted','source_derived','target_relevant','productive','material']}}
        self.assertFalse(c.viable(candidate));self.assertFalse(c.unresolved(candidate))
    def test_generation_context_allowlist(self):
        for cid in r.order():
            p=r.payload('generation',cid)
            self.assertEqual(set(p),{'packet_id','target','source_instrument'})
            self.assertEqual(set(p['source_instrument']),{'instrument'})
    def test_pairings_replay_frozen_rule(self):
        import hashlib
        m=r.read(H/'manifest.json');uses={x['instrument_id']:0 for x in m['eligible_instruments']}
        for target in range(1,7):
            tid=f'T{target:02}';families=set()
            for slot in range(1,4):
                eligible=[s for s in m['eligible_instruments'] if s['family'] not in families]
                s=min(eligible,key=lambda s:(uses[s['instrument_id']],hashlib.sha256(f"H6-natural-v0.1|{tid}|{slot}|{s['instrument_id']}".encode()).hexdigest(),s['instrument_id']))
                pair=m['pairings'][(target-1)*3+slot-1]
                self.assertEqual(pair['instrument_id'],s['instrument_id']);families.add(s['family']);uses[s['instrument_id']]+=1

if __name__=='__main__':unittest.main()
