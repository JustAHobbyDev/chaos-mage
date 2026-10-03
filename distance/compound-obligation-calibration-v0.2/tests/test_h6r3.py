import ast
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
H = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(H))
import contracts as c
import runner
T = json.loads((H/'taxonomy.json').read_text())


def assignment(cid='X', origin='MAPPING_GENERATED', function='GOVERNANCE_RULE'):
    return {'claim_id': cid, 'atomicity': 'ATOMIC',
            'content_origin': {'assignment_status': 'ASSIGNED', 'kind': origin},
            'epistemic_function': {'assignment_status': 'ASSIGNED', 'kind': function}}


def refs(*pairs):
    return [{'source_id': sid, 'role': role} for sid, role in pairs]


def dependency(origin='MAPPING_GENERATED', function='OPERATION', mode='ASSERTED_COMPONENT', resolution='INLINE_OBLIGATION'):
    return {'dependency_id': 'D1', 'subject': 'do X', 'dependency_classification': {
        'content_origin': origin, 'epistemic_function': function, 'assertion_mode': mode,
        'origin_refs': [], 'rationale': 'fixture'}, 'resolution': resolution, 'claim_ref': None,
        'provenance_refs': refs(('S1', 'SUPPORT')), 'materiality_rationale': 'fixture', 'resolution_rationale': 'fixture'}


def discovery(dep=None):
    return {'claim_id': 'X', 'base_provenance_refs': refs(('T1','CONTEXT'), ('S1','SUPPORT')),
            'dependencies': [] if dep is None else [dep], 'closure_status': 'COMPLETE', 'unresolved_dependencies': []}


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.case = {'target': {'source_id':'T1','text':'target'}, 'source_instrument': {'source_id':'S1','text':'source'},
                     'mapping': {'source_id':'M1','text':'mapping'}}
        self.claim = {'claim_id':'X','value':'If unresolved, do X','scope':'case',
                      'provenance': {'refs': refs(('T1','CONTEXT'), ('S1','SUPPORT'))}}

    def packet(self, rs):
        job = {'claim_id':'X','obligation_id':'D1','contract':'OPERATION_LICENSE','subject':'do X',
               'provenance_refs':rs,'provenance_hash':c.digest(c.canonical(rs))}
        return job, c.evaluation_packet(self.claim,self.case,job,T)

    def test_adversarial_projections(self):
        for rs in [refs(('T1','SUPPORT'),('S1','CONTEXT')),  # parent roles inverted
                   refs(('S1','SUPPORT')),                  # fewer child refs
                   refs(('T1','SUPPORT'),('S1','CONTEXT'),('M1','CONTEXT')), # additional
                   refs(('T1','SUPPORT'),('S1','SUPPORT')), # multiple support
                   refs(('S1','CONTEXT'),('T1','SUPPORT'))]: # reordered IDs
            with self.subTest(refs=rs):
                job, packet = self.packet(rs)
                self.assertEqual(packet['provenance_refs'],rs)
                self.assertNotIn('claim',packet)
                self.assertNotIn('target',packet)
                self.assertEqual({r['source_id'] for r in packet['evidence_bundle']},{r['source_id'] for r in rs})
                self.assertTrue(c.projection_check(job,packet)['exact_match'])

    def test_array_order_is_irrelevant_but_roles_never_are(self):
        job, packet = self.packet(refs(('T1','SUPPORT'),('S1','CONTEXT')))
        packet['provenance_refs'].reverse()
        self.assertTrue(c.projection_check(job,packet)['exact_match'])
        packet['provenance_refs'][0]['role']='SUPPORT'
        with self.assertRaisesRegex(ValueError,'PROVENANCE_PROJECTION_FAILURE'): c.projection_check(job,packet)

    def test_resolved_evidence_role_mutation_rejected(self):
        job, packet = self.packet(refs(('T1','SUPPORT')))
        packet['evidence_bundle'][0]['role']='CONTEXT'
        with self.assertRaisesRegex(ValueError,'PROVENANCE_PROJECTION_FAILURE'):c.projection_check(job,packet)

    def test_missing_bundle_no_parent_fallback(self):
        job,_=self.packet([]);del job['provenance_refs']
        with self.assertRaises(KeyError):c.evaluation_packet(self.claim,self.case,job,T)

    def test_missing_extra_duplicate_conflicting_or_unknown_ref(self):
        job,packet=self.packet(refs(('S1','SUPPORT')))
        for bad in [[], refs(('S1','SUPPORT'),('T1','CONTEXT'))]:
            badpacket=deepcopy(packet);badpacket['provenance_refs']=bad
            with self.assertRaisesRegex(ValueError,'PROVENANCE_PROJECTION_FAILURE'):c.projection_check(job,badpacket)
        for rs in [refs(('T1','SUPPORT'),('T1','SUPPORT')),refs(('T1','SUPPORT'),('T1','CONTEXT')),refs(('UNKNOWN','SUPPORT'))]:
            with self.assertRaisesRegex(ValueError,'PROVENANCE_PROJECTION_FAILURE'): self.packet(rs)

    def test_complete_set_blocks_on_last_bad_packet(self):
        job,packet=self.packet(refs(('T1','SUPPORT')))
        jobs={'a':job,'z':deepcopy(job)};packets={'a':packet,'z':deepcopy(packet)}
        packets['z']['provenance_refs'][0]['role']='CONTEXT'
        with self.assertRaisesRegex(ValueError,'PROVENANCE_PROJECTION_FAILURE'):c.projection_barrier(jobs,packets)
        with self.assertRaisesRegex(ValueError,'PROVENANCE_PROJECTION_FAILURE'):c.projection_barrier(jobs,{'a':packet})


class RoutingTests(unittest.TestCase):
    def test_all_independent_combinations_and_source_limit(self):
        for o in T['origins']:
            for f in T['functions']:
                contracts=c.route(o,f,T)
                self.assertEqual(contracts,T['supplied_routing'][o] if o in T['supplied_routing'] else [T['generated_routing'][f]])
        self.assertEqual(c.route('SOURCE_SUPPLIED','LIMIT',T),['SOURCE_FIDELITY'])
        self.assertEqual(c.route('BOTH_SUPPLIED','FACT',T),['TARGET_FIDELITY','SOURCE_FIDELITY'])
        self.assertEqual(c.route('MAPPING_GENERATED','GOVERNANCE_RULE',T),['GOVERNANCE_STRUCTURE'])

    def test_p2_real_control_fixture(self):
        fixture=json.loads((H/'tests/p2-preflight-fixture.json').read_text())
        case=json.loads((H/'cases/R3K08.json').read_text());claim=case['claims'][0]
        a=assignment(claim['claim_id'])
        packet=c.obligation_packet(claim,case,a,{claim['claim_id']:a})
        c.validate('dependency',fixture,packet,json.loads((H/'schemas/dependency.schema.json').read_text()),T)
        resolved=c.resolve(claim,a,fixture,T)
        self.assertEqual(c.p2_preflight(resolved)['empirical_secondary_count'],0)
        self.assertEqual(len(c.obligation_jobs(claim,a,resolved)),1)
        bad=deepcopy(resolved);bad['claim_obligation_set']['base_obligations'].append({'contract':'FACT_WARRANT'})
        with self.assertRaisesRegex(ValueError,'SUPPLIED_PREMISE_OVERTRIGGER'):c.p2_preflight(bad)

    def test_expanded_grounding_rejected_when_classified_generated(self):
        fixture=json.loads((H/'tests/p2-preflight-fixture.json').read_text())
        fixture['dependencies'][0]['dependency_classification']['content_origin']='MAPPING_GENERATED'
        case=json.loads((H/'cases/R3K08.json').read_text());claim=case['claims'][0];a=assignment(claim['claim_id'])
        with self.assertRaisesRegex(ValueError,'GROUNDING_REF_MISCLASSIFICATION'):
            c.validate('dependency',fixture,c.obligation_packet(claim,case,a,{claim['claim_id']:a}),
                       json.loads((H/'schemas/dependency.schema.json').read_text()),T)

    def test_asserted_supplied_routes_fidelity_and_generated_harm_routes_warrant(self):
        claim={'claim_id':'X','value':'claim'}
        for origin,expected in [('TARGET_SUPPLIED',['TARGET_FIDELITY']),('BOTH_SUPPLIED',['TARGET_FIDELITY','SOURCE_FIDELITY']),('MAPPING_GENERATED',['FACT_WARRANT'])]:
            result=c.resolve(claim,assignment(),discovery(dependency(origin,'FACT')),T)
            self.assertEqual([o['contract'] for o in result['claim_obligation_set']['dependencies'][0]['obligations']],expected)

    def test_no_contract_selection_in_stage_b_schema(self):
        schema=(H/'schemas/dependency.schema.json').read_text()
        self.assertNotIn('"contract"',schema)

    def test_uncertain_axes_never_routed(self):
        for origin,function in [('ORIGIN_UNCERTAIN','FACT'),('MAPPING_GENERATED','FUNCTION_UNCERTAIN')]:
            with self.assertRaises(ValueError):c.route(origin,function,T)


class AggregateTests(unittest.TestCase):
    def test_failure_propagation_both_secondary_calls_required(self):
        d=discovery(dependency());d2=dependency(function='CONDITIONAL_RELATION');d2['dependency_id']='D2';d['dependencies'].append(d2)
        a={'X':assignment()};b={'X':c.resolve({'claim_id':'X','value':'claim'},a['X'],d,T)}
        ev={('X','B1'):{'contract':'GOVERNANCE_STRUCTURE','verdict':'SATISFIED'},
            ('X','D1-O1'):{'contract':'OPERATION_LICENSE','verdict':'VIOLATED'}}
        self.assertEqual(c.aggregate(a,b,ev,T)['X']['status'],'INCOMPLETE')
        ev[('X','D2-O1')]={'contract':'CONDITIONAL_LICENSE','verdict':'VIOLATED'}
        out=c.aggregate(a,b,ev,T)['X'];self.assertEqual(out['overall'],'VIOLATED');self.assertEqual(len(out['results']),3)

    def test_uncertain_closure_and_violated_precedence(self):
        d=discovery();d.update(closure_status='DEPENDENCY_UNCERTAIN',unresolved_dependencies=['ambiguous operation'])
        a={'X':assignment()};b={'X':c.resolve({'claim_id':'X','value':'claim'},a['X'],d,T)}
        for base,expected in [('SATISFIED','UNCERTAIN'),('VIOLATED','VIOLATED')]:
            self.assertEqual(c.aggregate(a,b,{('X','B1'):{'contract':'GOVERNANCE_STRUCTURE','verdict':base}},T)['X']['overall'],expected)

    def test_claim_ref_reuses_one_judgment_and_propagates(self):
        a={'C1':assignment('C1',function='FACT'),'C2':assignment('C2')}
        dep=dependency(function='FACT',resolution='CLAIM_REF');dep['claim_ref']='C1'
        b={cid:c.resolve({'claim_id':cid,'value':cid},a[cid],discovery(dep if cid=='C2' else None),T) for cid in a}
        self.assertEqual(sum(len(c.obligation_jobs({'claim_id':cid},a[cid],b[cid])) for cid in a),2)
        ev={('C1','B1'):{'contract':'FACT_WARRANT','verdict':'VIOLATED'},('C2','B1'):{'contract':'GOVERNANCE_STRUCTURE','verdict':'SATISFIED'}}
        self.assertEqual(c.aggregate(a,b,ev,T)['C2']['overall'],'VIOLATED')
        b['C1']['claim_obligation_set']['dependencies']=[dict(dep,claim_ref='C2',obligations=[])]
        with self.assertRaisesRegex(ValueError,'DEPENDENCY_CYCLE'):c.aggregate(a,b,ev,T)


class DispatchTests(unittest.TestCase):
    def test_projection_failure_blocks_even_reservation(self):
        with patch.object(runner,'active_batch'),patch.object(runner,'verify'),patch.object(runner,'binary_check'),patch.object(runner,'verify_projection_barrier',side_effect=ValueError('PROVENANCE_PROJECTION_FAILURE')),patch.object(runner.subprocess,'Popen') as popen:
            gate=unittest.mock.Mock()
            with self.assertRaisesRegex(ValueError,'PROVENANCE_PROJECTION_FAILURE'):runner.run_one('evaluation','test',{},gate)
            gate.reserve.assert_not_called();popen.assert_not_called()

    def test_budget_denial_blocks_provider(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);packet={'hello':'world'};(p/'packet.json').write_text(json.dumps(packet));(p/'request.txt').write_bytes(b'request')
            with patch.object(runner,'RT',p),patch.object(runner,'active_batch'),patch.object(runner,'verify'),patch.object(runner,'binary_check'),patch.object(runner,'ids',return_value=['x']),patch.object(runner,'judgment',return_value=p/'missing'),patch.object(runner,'packet_path',side_effect=lambda stage,uid,suffix='json': p/('packet.json' if suffix=='json' else 'request.txt')),patch.object(runner,'build_packet',return_value=packet),patch.object(runner,'prompt',return_value=b'request'),patch.object(runner,'command',return_value=['codex']),patch.object(runner.subprocess,'Popen') as popen:
                gate=unittest.mock.Mock();gate.reserve.side_effect=runner.budget.BudgetError('denied')
                with self.assertRaises(runner.budget.BudgetError):runner.run_one('classification','x',{},gate)
                gate.reserve.assert_called_once();popen.assert_not_called()

    def test_governance_boundary_exact_and_historical_contract_absent(self):
        self.assertNotIn('GOVERNANCE_COHERENCE',T['contracts'])
        self.assertIn('Do not judge the scientific, causal, diagnostic, informational,',T['governance_boundary'])
        case=json.loads((H/'cases/R3K01.json').read_text());claim=case['claims'][0]
        d=discovery();d['base_provenance_refs']=claim['provenance']['refs']
        job=c.resolve(claim,assignment(),d,T)['claim_obligation_set']['base_obligations'][0]
        packet=c.evaluation_packet(claim,case,job,T)
        self.assertEqual(packet['governance_boundary'],T['governance_boundary'])


if __name__=='__main__': unittest.main()
