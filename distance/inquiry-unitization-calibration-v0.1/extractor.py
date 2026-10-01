"""Bounded, polarity-independent semantic grammar. No case/expectation input.

Lexical rules recognize explicit relations, never isolated keyword co-occurrence.
All field strings are searched, then compatible components are joined by mechanism.
The four supported inquiry operations each have one outcome vocabulary. Unrecognized
operations/logic are outside this v0.1 grammar; see LANGUAGE.md.
"""
import hashlib
import json
import re

# Canonical alternatives, operation aliases, and outcome/consequence aliases.
LANGUAGE = {
 'ach': {
  'alternatives': ['H1', 'H3'],
  'operations': [r'inspect individual evaluator scores saved before consensus', r'inspect record R, the individual scores saved before consensus'],
  'outcomes': [
   ('post-opening score changes', ['post-opening score changes', 'unexplained post-opening score changes'], 'favor H1 over H3', ['favor H1 over H3']),
   ('stable contemporaneous scores', ['stable contemporaneous scores'], 'favor H3 over H1', ['favor H3 over H1', 'bear against H1 relative to H3'])]},
 'delta': {
  'alternatives': ['b required', 'b not required'],
  'operations': [r'replay \{a,c\} after removing b under the frozen F oracle'],
  'outcomes': [
   ('F persists', ['F persists'], 'favor b not required over b required', ['favor b not required over b required']),
   ('F disappears', ['F disappears'], 'favor b required over b not required', ['favor b required over b not required'])]},
 'crossdating': {
  'alternatives': ['offset +6', 'offset +7'],
  'operations': [r'compare the next preserved increment against R2'],
  'outcomes': [
   ('narrow-to-wide correspondence', ['narrow-to-wide correspondence'], 'favor offset +6 over offset +7', ['favors offset +6 over offset +7', 'favor offset +6 over offset +7']),
   ('wide-to-narrow correspondence', ['wide-to-narrow correspondence'], 'favor offset +7 over offset +6', ['favors offset +7 over offset +6', 'favor offset +7 over offset +6'])]},
 'diagnosis': {
  'alternatives': ['lock contention', 'isolated pool exhaustion'],
  'operations': [r'measure lock-wait duration (?:together )?with pool occupancy', r'check waiting next, together with how full the pool is'],
  'outcomes': [
   ('elevated lock waits with normal occupancy', ['elevated lock waits with normal occupancy', 'long waits with spare capacity'], 'favor lock contention over isolated pool exhaustion', ['favor lock contention over isolated pool exhaustion', 'favor lock contention']),
   ('ordinary lock waits with saturated occupancy', ['ordinary lock waits with saturated occupancy', 'short waits with a full pool'], 'favor isolated pool exhaustion over lock contention', ['favor isolated pool exhaustion over lock contention', 'favor pool exhaustion'])]}
}
GENERIC = r'(?:investigate further|(?:collect|get|gather|seek) more (?:evidence|records)|run another test|check this)'

def hits(mapping, pattern):
    """Byte-exact provenance; no field whitelist and no metadata traversal."""
    result=[]
    for field,text in mapping.items():
        if not isinstance(text,str):
            raise TypeError('Surviving mapping fields must be strings')
        for m in re.finditer(pattern,text,re.I):
            result.append({'source_field':'mapping.'+field,'exact_text':m.group(),
                           'start':len(text[:m.start()].encode()),'end':len(text[:m.end()].encode())})
    return result

def union(spans):
    return sorted({(x['source_field'],x['start'],x['end']):x for x in spans}.values(),
                  key=lambda x:(x['source_field'],x['start'],x['end']))

def valid_span(mapping,span):
    field=span['source_field'].removeprefix('mapping.')
    if not span['source_field'].startswith('mapping.') or field not in mapping:return False
    data=mapping[field].encode();a,b=span['start'],span['end']
    return 0<=a<b<=len(data) and data[a:b]==span['exact_text'].encode()

def outcomes_are_discriminating(unit):
    outcomes=unit['differential_outcome_relation']['outcomes']
    alts=set(unit['unresolved_contrast']['alternatives'])
    return (len({x['outcome'].lower() for x in outcomes})>=2
            and len({x['consequence'].lower() for x in outcomes})>=2
            and all(set(x['bears_on'])==alts for x in outcomes)
            and all(not re.fullmatch(GENERIC,x['consequence'],re.I) for x in outcomes))

def complete(unit):
    return (unit['unresolved_contrast']['present'] is True
        and len(unit['unresolved_contrast']['alternatives'])>=2
        and unit['next_operation']['present'] is True
        and unit['differential_outcome_relation']['present'] is True
        and len(unit['differential_outcome_relation']['outcomes'])>=2
        and unit['provenance_complete'] is True
        and outcomes_are_discriminating(unit))

def canonical(unit):
    return (tuple(sorted(unit['unresolved_contrast']['alternatives'])),
            unit['next_operation']['operation'].lower(),
            tuple(sorted((o['outcome'].lower(),o['consequence'].lower(),tuple(sorted(o['bears_on'])))
                         for o in unit['differential_outcome_relation']['outcomes'])))

def extract_remainders(mapping):
    return [{'role':'INSUFFICIENCY_ONLY','source_span':s} for s in hits(mapping,r'[^.\n]*does not (?:distinguish|discriminate)[^.\n]*\.')]

def extract_inquiry_units(mapping):
    candidates=[]
    for family,lex in sorted(LANGUAGE.items()):
        a,b=map(re.escape,lex['alternatives'])
        pair=rf'(?:{a} and {b}|{b} and {a})'
        live=hits(mapping,rf'(?:{pair} remain (?:live under the current evidence|unresolved)|does not (?:distinguish|discriminate) (?:{a} from {b}|{b} from {a}))')
        resolved=hits(mapping,rf'(?:{a} is already established over {b}|{b} is already established over {a})')
        operations=[]
        for op in lex['operations']:
            # Explicit imperative with next, or affirmative declarative selection.
            operations+=hits(mapping,rf'(?:{op}(?: next)?(?=[:.]|$)|the selected next operation is to {op}(?=[.]|$))')
        # Prevent an unselected hypothetical operation from passing: require clause start.
        operations=[s for s in operations if clause_start(mapping,s)]
        outcome_rows=[];outcome_spans=[]
        for name,aliases,consequence,consequences in lex['outcomes']:
            pat='(?:'+'|'.join(map(re.escape,sorted(aliases,key=len,reverse=True)))+')'
            cp='(?:'+'|'.join(map(re.escape,sorted(consequences,key=len,reverse=True)))+')'
            matches=hits(mapping,pat+r'\s*(?::\s*)?'+cp+r'(?=[.,;]|$)')
            generic=hits(mapping,pat+r':\s*gather more evidence(?=[.]|$)')
            for found,meaning in [(matches,consequence),(generic,'gather more evidence')]:
                if found:
                    outcome_spans+=found
                    outcome_rows.append({'outcome':name,'consequence':meaning,'bears_on':list(lex['alternatives'])})
        generic=hits(mapping,GENERIC+r'(?=[.]|$)') if live or resolved else []
        if not (live or resolved or operations or outcome_rows):continue
        spans=union(live+resolved+operations+outcome_spans+generic)
        has_contrast=bool(live) and not resolved
        u={'unit_id':'','source_spans':spans,
           'unresolved_contrast':{'present':has_contrast,'alternatives':list(lex['alternatives']) if live or resolved else [],'rationale':'Explicit live relation; resolved declarations veto live status.' if live or resolved else 'No explicit live contrast.'},
           'next_operation':{'present':bool(operations),'operation':lex['operations'][0].replace('\\','').replace('(?:together )?','together ') if operations else (generic[0]['exact_text'] if generic else ''),'rationale':'Selected concrete operation cited.' if operations else 'No selected concrete operation.'},
           'differential_outcome_relation':{'present':len(outcome_rows)>=2,'outcomes':outcome_rows,'rationale':'Explicit outcome implications cited.' if outcome_rows else 'No explicit outcome relation.'},
           'provenance_complete':bool(live and operations and len(outcome_rows)>=2) and not resolved,
           'role':'NOT_INQUIRY_CONSTRAINT','counterfactual_effect':{'next_inquiry':'uncertain'},'productivity':'UNCERTAIN','rationale':'Deterministic semantic structure; productivity is assessed separately.'}
        u['differential_outcome_relation']['present']=len(outcome_rows)>=2 and outcomes_are_discriminating(u)
        u['provenance_complete']=bool(has_contrast and operations and u['differential_outcome_relation']['present'])
        if complete(u):u['role']='INQUIRY_CONSTRAINT'
        candidates.append(u)
    # Components of repeated equivalent bundles were already unioned, not emitted anew.
    for i,u in enumerate(candidates,1):u['unit_id']=f'IQ{i}'
    return candidates

def clause_start(mapping,span):
    text=mapping[span['source_field'][8:]].encode()[:span['start']].decode()
    return not text.strip() or text.rstrip().endswith(('.', '\n', ':'))

def missing(unit):
    result=[]
    if unit['unresolved_contrast']['present'] is not True:result.append('unresolved_contrast')
    if unit['next_operation']['present'] is not True:result.append('operation')
    if len(unit['differential_outcome_relation']['outcomes'])>=2 and not outcomes_are_discriminating(unit):result.append('discrimination')
    elif unit['differential_outcome_relation']['present'] is not True:result.append('outcome_relation')
    return result

def scan(mapping):
    ordinary=extract_remainders(mapping)
    units=extract_inquiry_units(mapping)
    return {'ordinary_remainders':ordinary,'semantic_units':[{'inquiry_unit':u} for u in units]}
