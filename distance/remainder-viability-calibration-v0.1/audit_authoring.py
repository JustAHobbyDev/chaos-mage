"""Operator semantic audit, distinct from any independent/model observation."""
import math
from common import H, read, write, span, verify_span, viable, unresolved, guard, require, git

# Evidence-backed interpretations. These are author hypotheses, never judge inputs.
CORE = {
 'ach': [
  ('The index enables retrieval and the hypothesis list remains organized.', ['inference'], 'YES','NO','YES','YES', 'Useful dossier administration is ordinary target practice; no comparative weighting, elimination or diagnostic priority is supplied.'),
  ('The X table weakens one steering explanation relative to another.', ['signal','limit'], 'NO','YES','YES','YES', 'X replaces every original rating; neither a hypothesis-specific inconsistency nor a relative pattern is available.'),
  ('Repeating the documented comparison or retrieving source records supplies a discriminating next inquiry.', ['operation','limit'], 'NO','UNCERTAIN','UNCERTAIN','YES', 'The operation is a procedure, not a surviving evidential comparison. No record is identified as discriminating between hypotheses; proposing such a relation would be repair.')
 ],
 'step': [
  ('The submitted command trajectory and recorder-filter transient can be plotted and characterized.', ['signal','inference','limit'], 'YES','YES','NO','NO', 'A bounded step response of the recorder is real, but input execution is already granted and the recorder is not the delay-producing process. No added delay answer or inquiry priority follows.'),
  ('The two-unit decrease measures a two-hour delay improvement or a candidate delay remedy.', ['signal','limit'], 'NO','YES','YES','YES', 'Command units have no supplied delay conversion and the trace is generated before the scheduler acts.'),
  ('The trace discriminates internal delay models or licenses a specific further delay test.', ['operation','signal','limit'], 'NO','YES','YES','YES', 'No process-output observation or model-dependent delay prediction is supplied. Adding one would change the mapping.')
 ],
 'custody': [
  ('The sealed packet has continuous documented identity and handling after assembly.', ['signal','inference','limit'], 'YES','YES','NO','NO', 'This is genuine custody evidence, but packet identity is already fixed and all competing pre-accession assembly histories admit the same later handling.'),
  ('Shelf transfer order constrains leaf revision or assembly order.', ['signal','limit'], 'NO','YES','YES','YES', 'Events postdate assembly and record no internal leaf or attachment relation; temporal order of administration is not order of formation.'),
  ('The ledger distinguishes uncertainty between the competing textual histories.', ['state','signal','limit'], 'NO','YES','YES','YES', 'The histories differ only before accession; no recorded event bears differently on them. New witnesses or documents would be replacement evidence.')
 ],
 'delta': [
  ('The pooled nonzero-exit flag has a test-relative 1-minimal producing subset {a,b}.', ['signal','inference'], 'YES','YES','YES','NO', 'This is a real reduction result for a different outcome of the same focal replay. Neither sufficiency nor single-removal necessity for target F follows.'),
  ('The absent flag on singleton subsets excludes target F there.', ['signal','limit'], 'NO','YES','YES','YES', 'Handled target deadline failures can have zero exit. The flag is not necessary for F, so negative pooled tests do not eliminate target reproductions.'),
  ('A present flag on {a,b} establishes target reproduction or prioritizes it over other subsets for F.', ['signal','limit'], 'NO','YES','YES','YES', 'Nonzero exits can precede checkout; the flag is not sufficient for F. No supplied relation ranks the F likelihoods of the subsets.'),
  ('The missing oracle supports a specific F-discriminating next inquiry.', ['operation','limit'], 'NO','UNCERTAIN','YES','YES', 'A new failure-identity oracle could make reduction useful, but is not supplied by the surviving mapping. Generic advice to define an outcome is not an already warranted target inference.')
 ],
 'crossdate': [
  ('The physical transcription of S is dated 1912 by the docket.', ['state','inference','limit'], 'YES','NO','YES','YES', 'A material native documentary dating result survives. It is independent of any imported ordered overlap/offset operation.'),
  ('Separate counts license a discriminating alignment or exclude an offset for S.', ['signal','limit'], 'NO','YES','YES','YES', 'Counts discard order and position and supply no overlap/shared influence. Recovering an ordered sequence would add evidence, not reveal a surviving offset.'),
  ('Listing dated references and high/low similarities yields another source-derived contribution.', ['operation','signal'], 'YES','NO','NO','UNCERTAIN', 'The facts can be listed, but their tabulation supplies no source-specific temporal placement, discriminating constraint or inquiry priority.')
 ],
 'diagnosis': [
  ('The ledger confirms three completed tests and identifies the two mechanisms.', ['signal','inference'], 'YES','NO','NO','YES', 'Execution bookkeeping is ordinary procedure; neither relative support nor inquiry priority follows.'),
  ('R favors lock contention over connection-pool exhaustion.', ['signal','limit'], 'NO','YES','YES','YES', 'R denotes completion only and has no supplied response semantics or mechanism-dependent prediction.'),
  ('R supports retaining both mechanisms because their diagnostic predictions coincide.', ['signal','limit'], 'NO','YES','YES','YES', 'Missing diagnostic predictions do not establish equal predictions or evidential non-discrimination. Inferring calibrated equality would invent a weaker comparison.'),
  ('A specific follow-up test can be prioritized from R.', ['operation','signal','limit'], 'NO','YES','YES','YES', 'No candidate-specific result or differentiating follow-up is supplied. Asking for missing documentation does not itself perform the imported comparison.')
 ]
}

def build():
    pairs = read(H/'hidden-design/pairs.json')
    audits, balance = [], []
    for pair in pairs:
        lengths = []
        for cid in pair['case_ids']:
            case = read(H/'authoring-attempts'/f'{cid}.json')
            design = read(H/'hidden-design'/f'{cid}.json')
            deleted = design['intended_deletion']; verify_span(case, deleted)
            mapping = dict(case['mapping'])
            mapping['inference'] = mapping['inference'][:deleted['start']]+'[DELETED INTENDED CLAIM]'+mapping['inference'][deleted['end']:]
            candidates = []
            if design['pair_role'] == 'reduced':
                text = case['mapping']['inference'][deleted['end']:].strip()
                candidates.append({'remainder_id':'R1','inference':text,
                    'source_spans':[span(case,'inference',text),span(case,'signal',case['mapping']['signal'])],
                    'warranted':'YES','source_derived':'YES','material':'YES','target_relevant':'YES',
                    'rationale':'The surviving explicit bounded inference is licensed by the stated mechanism-specific observation; it narrows the exact target without the deleted comprehensive conclusion.'})
            else:
                for i,(text,fields,w,s,m,t,why) in enumerate(CORE[design['mechanism_key']],1):
                    citations=[]
                    for field in fields:
                        excerpt = case['mapping'][field]
                        if field == 'inference': excerpt=excerpt[deleted['end']:].strip()
                        citations.append(span(case,field,excerpt))
                    candidates.append(dict(remainder_id=f'R{i}',inference=text,source_spans=citations,warranted=w,source_derived=s,material=m,target_relevant=t,rationale=why))
            for candidate in candidates:
                for citation in candidate['source_spans']:
                    verify_span(case,citation)
                    require(citation['source_field']!=deleted['source_field'] or citation['end']<=deleted['start'] or citation['start']>=deleted['end'],'Deleted evidence in remainder')
            good=[r['remainder_id'] for r in candidates if viable(r)]
            unknown=[r['remainder_id'] for r in candidates if unresolved(r)]
            passed=bool(good) if design['pair_role']=='reduced' else not good and not unknown
            chars=len(deleted['exact_text']);lengths.append(chars)
            audits.append({'case_id':cid,'mechanism_key':design['mechanism_key'],'pair_role':design['pair_role'],
                'deleted_span':deleted,'ablated_mapping':mapping,'candidate_remainders':candidates,
                'viable_remainders':good,'decisively_unresolved_candidates':unknown,'authoring_gate_passed':passed,
                'all_fields_searched':list(case['mapping']),
                'search_record':'Inspected state, operation, signal, inference and limit for direct entailments, negative constraints, dependencies and meaningful next inquiries; no replacement evidence allowed.',
                'unsupported_chars':chars,'token_estimate':math.ceil(chars/4),'mapping_chars':len('\n'.join(case['mapping'].values())),
                'deleted_fraction':chars/len('\n'.join(case['mapping'].values()))})
        ratio=max(lengths)/min(lengths)
        balance.append({'mechanism_key':pair['mechanism_key'],'unsupported_chars':lengths,'max_min_ratio':ratio,'within_1_15':ratio<=1.15,
            'explicit_inference_sentences':[2,2],'position':'first inference sentence in both members',
            'semantic_difference':'Evidence licenses a distinctive target remainder in one member; the other lacks the required relation or retains only generic/irrelevant content.',
            'no_comparison_object_shortcut':True,'no_target_tautology':True,'same_focal_object':True})
    return {'type':'operator_premeasurement_audit_not_independent_rater_evidence','provider_calls':0,
        'case_audits':audits,'surface_balance':balance,'passed':all(a['authoring_gate_passed'] for a in audits),
        'design_limitation':'The pairs deliberately differ in observation informativeness. Unknown or wrong-outcome semantics may be strong cues; source-specific next-inquiry boundaries remain open to measured disagreement.',
        'delta_authoring_correction':'Before freeze made explicit that pooled flag is neither necessary nor sufficient for F, preventing a surviving singleton exclusion inferred from a negative broad oracle. No provider observation informed this correction.'}

def verify():
    counts=guard();audit=read(H/'authoring-audit/primary.json')
    require(audit==build(),'Authoring audit drift')
    require(len(audit['case_audits'])==12 and len(audit['surface_balance'])==6,'Wrong primary corpus')
    targets={t['mechanism_key']:t for t in read(H/'targets.json')}
    for pair in read(H/'hidden-design/pairs.json'):
        t=targets[pair['mechanism_key']]
        for cid in pair['case_ids']:
            case=read(H/'authoring-attempts'/f'{cid}.json');d=read(H/'hidden-design'/f'{cid}.json')
            require(case['source']==t['source'] and case['target']==t['target'],'Instrument/target drift')
            require(d['focal_object']==t['focal_object'],'Focal drift')
            require(git('show',d['target_checkpoint']+':distance/remainder-viability-calibration-v0.1/targets.json')==(H/'targets.json').read_bytes(),'Target checkpoint drift')
            require(subprocess_absent_case(d['target_checkpoint'],cid),'Variant existed at target freeze')
    return {'passed':audit['passed'],'primary_cases':12,'primary_pairs':6,'preservation':counts}

def subprocess_absent_case(commit,cid):
    import subprocess
    return subprocess.run(['git','cat-file','-e',commit+':distance/remainder-viability-calibration-v0.1/authoring-attempts/'+cid+'.json'],stderr=subprocess.DEVNULL).returncode != 0

if __name__=='__main__':
    import sys,json
    if sys.argv[1]=='write': write(H/'authoring-audit/primary.json',build())
    elif sys.argv[1]=='verify': print(json.dumps(verify(),indent=2))
    else: raise ValueError('Unknown action')
