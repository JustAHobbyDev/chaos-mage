import copy
import inspect
import json
from pathlib import Path
import sys
import unittest
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H))
import extractor as e
import validation as v
M=json.loads((H/'manifest.json').read_text())
def case(row):return json.loads((H/'cases'/f"{row['case_id']}.json").read_text())
def primary():return case(next(r for r in M['cases'] if r['mechanism']=='ach' and r['formulation']=='negative'))
class InquiryTests(unittest.TestCase):
 def errors(self,c,value):return {x['code'] for x in v.validate(c,value)['errors']}
 def mutate(self,fn):
  c=primary();a=v.assess_deterministically(c);fn(a['semantic_units'][0]['inquiry_unit']);return self.errors(c,a)
 def test_exact_corpus(self):
  self.assertEqual(len(M['cases']),18);self.assertEqual(len(list((H/'cases').glob('*.json'))),18)
  self.assertEqual(sum(r['kind']=='primary' for r in M['cases']),12)
  self.assertEqual(sum(r['kind']=='control' for r in M['cases']),6)
  self.assertEqual(len(set(M['case_order'])),18)
 def test_all_authored_structures_and_intended_missing_components(self):
  for r in M['cases']:
   with self.subTest(r=r):
    c=case(r);units=e.extract_inquiry_units(c['mapping']);self.assertEqual(len(units),1)
    self.assertEqual(sum(e.complete(u) for u in units),r['expected_complete'])
    self.assertEqual(set(e.missing(units[0])),set(r['expected_missing']))
    self.assertTrue(v.validate(c,v.assess_deterministically(c))['validation_passed'])
 def test_triplets(self):
  for family in e.LANGUAGE:
   rows=[r for r in M['cases'] if r['kind']=='primary' and r['mechanism']==family]
   self.assertEqual({r['formulation'] for r in rows},{'negative','affirmative','distributed'})
   units=[e.extract_inquiry_units(case(r)['mapping'])[0] for r in rows]
   self.assertEqual(len({e.canonical(u) for u in units}),1)
 def test_polarity_metadata_irrelevant(self):
  for r in M['cases']:
   self.assertEqual(v.polarity_audit(case(r)),[])
   self.assertEqual(v.audit_discovery_adapter(case(r),lambda c:e.extract_inquiry_units(c['mapping'])),[])
 def test_legacy_gate_detected(self):
  self.assertEqual(v.audit_discovery_adapter(primary(),lambda c:e.extract_inquiry_units(c['mapping']) if c.get('negative_inference') else []),['IQ_POLARITY_GATING'])
 def test_no_negative_metadata_reference_in_discovery(self):
  self.assertNotIn('negative_inference',inspect.getsource(e))
 def test_all_fields_and_new_field_names(self):
  text=primary()['mapping']['inference'];expected=e.canonical(e.extract_inquiry_units({'state':text})[0])
  for f in ['state','operation','signal','inference','limit','new_surviving_field']:
   self.assertEqual(e.canonical(e.extract_inquiry_units({f:text})[0]),expected)
 def test_three_field_composition(self):
  r=next(r for r in M['cases'] if r['formulation']=='distributed');u=e.extract_inquiry_units(case(r)['mapping'])[0]
  self.assertEqual({s['source_field'] for s in u['source_spans']},{'mapping.state','mapping.operation','mapping.signal'})
 def test_no_cartesian_cross_family_invention(self):
  c=primary();mapping={'state':'H1 and H3 remain unresolved.','operation':'Measure lock-wait duration together with pool occupancy next.','signal':'Post-opening score changes favor H1 over H3. Stable contemporaneous scores favor H3 over H1.'}
  self.assertFalse(any(e.complete(u) for u in e.extract_inquiry_units(mapping)))
 def test_unselected_hypothetical_operation(self):
  c=primary();c['mapping']['inference']=c['mapping']['inference'].replace('Inspect','One could inspect')
  self.assertFalse(e.complete(e.extract_inquiry_units(c['mapping'])[0]))
 def test_fewer_alternatives(self):
  self.assertIn('IQ_TOO_FEW_ALTERNATIVES',self.mutate(lambda u:u['unresolved_contrast'].update(alternatives=['H1'])))
 def test_missing_contrast(self):
  self.assertIn('IQ_MISSING_CONTRAST',self.mutate(lambda u:u['unresolved_contrast'].update(present=False)))
 def test_missing_operation(self):
  self.assertIn('IQ_MISSING_OPERATION',self.mutate(lambda u:u['next_operation'].update(present=False)))
 def test_generic_operation(self):
  self.assertIn('IQ_GENERIC_OPERATION',self.mutate(lambda u:u['next_operation'].update(operation='investigate further')))
 def test_missing_outcome_relation(self):
  self.assertIn('IQ_MISSING_OUTCOME_RELATION',self.mutate(lambda u:u['differential_outcome_relation'].update(present=False)))
 def test_fewer_outcomes(self):
  self.assertIn('IQ_TOO_FEW_OUTCOMES',self.mutate(lambda u:u['differential_outcome_relation']['outcomes'].pop()))
 def test_repeated_outcome_not_two(self):
  def change(u):u['differential_outcome_relation']['outcomes']=[u['differential_outcome_relation']['outcomes'][0]]*2
  self.assertIn('IQ_TOO_FEW_OUTCOMES',self.mutate(change))
 def test_nondiscriminating_rejected(self):
  r=next(r for r in M['cases'] if r['formulation']=='nondiscriminating');c=case(r);a=v.assess_deterministically(c);a['semantic_units'][0]['inquiry_unit']['role']='INQUIRY_CONSTRAINT'
  self.assertIn('IQ_NONDISCRIMINATING_OUTCOMES',self.errors(c,a))
 def test_resolved_contrast(self):
  r=next(r for r in M['cases'] if r['formulation']=='resolved');u=e.extract_inquiry_units(case(r)['mapping'])[0]
  self.assertFalse(u['unresolved_contrast']['present']);self.assertFalse(e.complete(u))
 def test_provenance_required(self):
  self.assertIn('IQ_INVENTED_COMPONENT',self.mutate(lambda u:u.update(source_spans=[])))
  self.assertIn('IQ_INVENTED_COMPONENT',self.mutate(lambda u:u.update(provenance_complete=False)))
 def test_exact_source_bytes(self):
  self.assertIn('IQ_UNCITED_SPAN',self.mutate(lambda u:u['source_spans'][0].update(exact_text='invented')))
  self.assertIn('IQ_UNCITED_SPAN',self.mutate(lambda u:u['source_spans'][0].update(start=-1)))
 def test_utf8_byte_offsets(self):
  mapping={'extra':'Évidence. '+primary()['mapping']['inference']};u=e.extract_inquiry_units(mapping)[0]
  self.assertTrue(e.complete(u));self.assertTrue(all(e.valid_span(mapping,s) for s in u['source_spans']))
 def test_missing_role_blocks_downstream(self):
  c=primary();a=v.assess_deterministically(c);a['semantic_units']=[];r=v.validate(c,a)
  self.assertIn('IQ_MISSING_ROLE',{x['code'] for x in r['errors']});self.assertFalse(r['downstream_allowed'])
  self.assertEqual(r['inquiry_role_coverage']['uncovered_complete_units'],['IQ1'])
 def test_wrong_role(self):
  self.assertIn('IQ_WRONG_ROLE',self.mutate(lambda u:u.update(role='NOT_INQUIRY_CONSTRAINT')))
 def test_duplicate_assessment(self):
  c=primary();a=v.assess_deterministically(c);a['semantic_units']*=2
  self.assertIn('IQ_DUPLICATE_UNIT',self.errors(c,a))
 def test_duplicate_with_changed_id(self):
  c=primary();a=v.assess_deterministically(c);x=copy.deepcopy(a['semantic_units'][0]);x['inquiry_unit']['unit_id']='IQ2';a['semantic_units'].append(x)
  self.assertIn('IQ_DUPLICATE_UNIT',self.errors(c,a))
 def test_duplicate_text_is_one_unit(self):
  r=next(r for r in M['cases'] if r['formulation']=='redundant_complete');u=e.extract_inquiry_units(case(r)['mapping']);self.assertEqual(len(u),1)
  self.assertEqual({s['source_field'] for s in u[0]['source_spans']},{'mapping.state','mapping.limit'})
 def test_insufficiency_role_stays_separate(self):
  result=e.scan(primary()['mapping']);self.assertEqual(result['ordinary_remainders'][0]['role'],'INSUFFICIENCY_ONLY')
  self.assertEqual(result['semantic_units'][0]['inquiry_unit']['role'],'INQUIRY_CONSTRAINT')
 def test_role_and_productivity_independent(self):
  self.assertEqual(self.mutate(lambda u:u.update(counterfactual_effect={'next_inquiry':'unchanged'},productivity='NO')),set())
  self.assertIn('IQ_PRODUCTIVITY',self.mutate(lambda u:u.update(productivity='YES')))
 def test_coverage_summary_not_trusted(self):
  c=primary();a=v.assess_deterministically(c);a['inquiry_role_coverage']['complete_units_found']=0
  self.assertIn('IQ_COVERAGE_SUMMARY',self.errors(c,a))
 def test_h3_regressions_exact(self):
  for p in (H/'regression-fixtures').glob('*.json'):
   c=json.loads(p.read_text());old=json.loads((H.parents[1]/c['historical_packet']).read_text().split('CASE PACKET\n')[1])
   self.assertEqual(c['mapping'],old['ablated_mapping']);self.assertFalse(c['negative_inference'])
   a=v.assess_deterministically(c);self.assertEqual(a['inquiry_role_coverage']['complete_units_found'],1)
   self.assertTrue(v.validate(c,a)['validation_passed'])
 def test_no_viability_schema(self):
  self.assertNotIn('artifact_viability',(H/'schemas/assessment.schema.json').read_text())
if __name__=='__main__':unittest.main()
