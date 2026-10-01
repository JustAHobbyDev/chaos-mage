"""Independent coverage enforcement; never rewrites a model judgment."""
import copy
import json
import re
from pathlib import Path
import jsonschema
import extractor as e

CODES=['IQ_MISSING_ROLE','IQ_WRONG_ROLE','IQ_MISSING_CONTRAST','IQ_TOO_FEW_ALTERNATIVES',
       'IQ_MISSING_OPERATION','IQ_GENERIC_OPERATION','IQ_MISSING_OUTCOME_RELATION',
       'IQ_TOO_FEW_OUTCOMES','IQ_NONDISCRIMINATING_OUTCOMES','IQ_INVENTED_COMPONENT',
       'IQ_POLARITY_GATING','IQ_DUPLICATE_UNIT','IQ_UNCITED_SPAN',
       'IQ_COMPONENT_MISMATCH','IQ_COVERAGE_SUMMARY','IQ_PRODUCTIVITY','IQ_SCHEMA','IQ_UNKNOWN_UNIT']

def normalize(u):
    """Normalize only the frozen lexical aliases; never fill a missing component."""
    v=copy.deepcopy(u)
    for lex in e.LANGUAGE.values():
        op=v['next_operation']['operation']
        if any(re.search(p,op,re.I) for p in lex['operations']):
            v['next_operation']['operation']=lex['operations'][0].replace('\\','').replace('(?:together )?','together ')
        for o in v['differential_outcome_relation']['outcomes']:
            for name,aliases,consequence,consequences in lex['outcomes']:
                if o['outcome'].lower().rstrip('.:') in [a.lower() for a in aliases]:
                    o['outcome']=name
                    if o['consequence'].lower().rstrip('.') in [x.lower() for x in consequences]+[consequence.lower()]:o['consequence']=consequence
    return v

def coverage(expected,units):
    found=[u for u in expected if e.complete(u)]
    uncovered=[];duplicates=[];emitted=sum(u['role']=='INQUIRY_CONSTRAINT' for u in units)
    for u in found:
        matches=[v for v in units if v['unit_id']==u['unit_id']]
        if len(matches)>1:duplicates.append(u['unit_id'])
        valid=[v for v in matches if v['role']=='INQUIRY_CONSTRAINT']
        if not valid:uncovered.append(u['unit_id'])
    return {'complete_units_found':len(found),'inquiry_constraints_emitted':emitted,
            'uncovered_complete_units':uncovered,'duplicate_units':duplicates,
            'validation_passed':not uncovered and not duplicates and len(found)==emitted}

def component_equal(comp,a,b):
    if comp=='unresolved_contrast':return set(a)==set(b)
    if comp=='differential_outcome_relation':
        def key(rows):return sorted((x['outcome'],x['consequence'],tuple(sorted(x['bears_on']))) for x in rows)
        return key(a)==key(b)
    return a==b

def validate(case,value,check_summary=True):
    errors=[]
    def fail(code,unit='',detail=''):
        row={'code':code,'unit_id':unit,'detail':detail}
        if row not in errors:errors.append(row)
    schema=json.loads((Path(__file__).parent/'schemas/assessment.schema.json').read_text())
    try:jsonschema.validate(value,schema)
    except jsonschema.ValidationError as exc:
        return {'errors':[{'code':'IQ_SCHEMA','unit_id':'','detail':exc.message}], 'validation_passed':False,'inquiry_role_coverage':None,'downstream_allowed':False}
    if value['case_id']!=case['case_id']:fail('IQ_SCHEMA',detail='case identity')
    expected=e.extract_inquiry_units(case['mapping']);units=[x['inquiry_unit'] for x in value['semantic_units']]
    indexed={u['unit_id']:u for u in expected}
    for gold in expected:
        matches=[u for u in units if u['unit_id']==gold['unit_id']]
        if e.complete(gold):
            if not matches:fail('IQ_MISSING_ROLE',gold['unit_id'])
            elif any(u['role']!='INQUIRY_CONSTRAINT' for u in matches):fail('IQ_WRONG_ROLE',gold['unit_id'])
        if len(matches)>1:fail('IQ_DUPLICATE_UNIT',gold['unit_id'],'Multiple assessments of one unit')
    keys=[]
    for raw in units:
        u=normalize(raw);uid=u['unit_id'];role=u['role'];g=indexed.get(uid)
        key=e.canonical(u)
        if key in keys:fail('IQ_DUPLICATE_UNIT',uid,'Equivalent decision structure emitted again')
        keys.append(key)
        if g is None:fail('IQ_UNKNOWN_UNIT',uid)
        invalid=[s for s in u['source_spans'] if not e.valid_span(case['mapping'],s)]
        if invalid:fail('IQ_UNCITED_SPAN',uid)
        cited={f'span{i}':s['exact_text'] for i,s in enumerate(u['source_spans']) if e.valid_span(case['mapping'],s)}
        evidence=e.extract_inquiry_units(cited)
        if role=='INQUIRY_CONSTRAINT':
            if u['unresolved_contrast']['present'] is not True:fail('IQ_MISSING_CONTRAST',uid)
            if len(u['unresolved_contrast']['alternatives'])<2:fail('IQ_TOO_FEW_ALTERNATIVES',uid)
            if u['next_operation']['present'] is not True:fail('IQ_MISSING_OPERATION',uid)
            if re.fullmatch(e.GENERIC+r'[.]?',u['next_operation']['operation'],re.I):fail('IQ_GENERIC_OPERATION',uid)
            if u['differential_outcome_relation']['present'] is not True:fail('IQ_MISSING_OUTCOME_RELATION',uid)
            outcomes=u['differential_outcome_relation']['outcomes']
            if len({(x['outcome'].lower(),x['consequence'].lower()) for x in outcomes})<2:fail('IQ_TOO_FEW_OUTCOMES',uid)
            if len(outcomes)>=2 and not e.outcomes_are_discriminating(u):fail('IQ_NONDISCRIMINATING_OUTCOMES',uid)
            if not u['provenance_complete'] or not any(e.complete(x) and e.canonical(x)==key for x in evidence):fail('IQ_INVENTED_COMPONENT',uid)
        if g:
            for component in ['unresolved_contrast','next_operation','differential_outcome_relation']:
                if u[component]['present']!=g[component]['present']:fail('IQ_COMPONENT_MISMATCH',uid,component+'.present')
            if key!=e.canonical(g):fail('IQ_COMPONENT_MISMATCH',uid,'Canonical component values differ')
            if u['provenance_complete']!=g['provenance_complete']:fail('IQ_INVENTED_COMPONENT',uid,'Completeness of component provenance differs')
        # Any asserted positive component must itself be evidenced, even under a non-inquiry role.
        for comp,content in [('unresolved_contrast','alternatives'),('next_operation','operation'),('differential_outcome_relation','outcomes')]:
            if u[comp]['present'] is True and not any(x[comp]['present'] is True and component_equal(comp,x[comp][content],u[comp][content]) for x in evidence):
                fail('IQ_INVENTED_COMPONENT',uid,comp)
        derived={'changed':'YES','unchanged':'NO','uncertain':'UNCERTAIN'}[u['counterfactual_effect']['next_inquiry']]
        if u['productivity']!=derived:fail('IQ_PRODUCTIVITY',uid)
    cov=coverage(expected,units)
    if check_summary and value['inquiry_role_coverage']!=cov:fail('IQ_COVERAGE_SUMMARY')
    return {'errors':errors,'validation_passed':not errors and cov['validation_passed'],
            'inquiry_role_coverage':cov,'downstream_allowed':not errors and cov['validation_passed']}

def assess_deterministically(case):
    units=e.extract_inquiry_units(case['mapping'])
    value={'case_id':case['case_id'],'semantic_units':[{'inquiry_unit':u} for u in units],
           'inquiry_role_coverage':coverage(units,units)}
    return value

def polarity_audit(case,scanner=e.extract_inquiry_units):
    # Scanner API accepts only mapping. Adversarial legacy adapters are tested separately.
    a=scanner(copy.deepcopy(case['mapping']))
    altered={**case,'negative_inference':not case.get('negative_inference',False)}
    b=scanner(copy.deepcopy(altered['mapping']))
    return [] if a==b else ['IQ_POLARITY_GATING']

def audit_discovery_adapter(case,adapter):
    variants=[{**case,'negative_inference':x} for x in [False,True,None]]
    outputs=[adapter(c) for c in variants]
    baseline=e.extract_inquiry_units(case['mapping'])
    return [] if all(x==baseline for x in outputs) else ['IQ_POLARITY_GATING']
