"""Post-freeze operator interpretation, not an independent-rater observation."""
import contracts as c
import runner as r

H=r.H

NOTES={
 'H2-04edf722fb7e':('PLAUSIBLE_ALTERNATIVE',False,False,
    'Relative support between the two mechanisms and the justified lock inquiry answer the exact frozen question. Deleting exclusive certainty removes an overclaim without materially narrowing that answer. KEEP_WITH_WARRANT_FLAGS is better supported than the intended reduced label.'),
 'H2-16df75b43727':('STRUCTURALLY_CONCORDANT',False,False,
    'The reliable chain connects witnessed attachment on 4 June to binding on 7 June for the same packet. This is a material partial assembly order after the complete-order and original-arrangement claims are deleted.'),
 'H2-25d1bd70c84a':('CASE_DESIGN_PROBLEM',True,False,
    'The authoring audit tested whether flag minimality itself answered F, and whether positive/negative flag outcomes proved F. It missed the distinct warranted test-relative constraint that neither F sufficiency nor F minimality follows from this reduction. R06 states that constraint without reconstructing an F oracle. Its materiality is permitted by the frozen definition; the intended core audit was a false pass.'),
 'H2-53fc9c8368c3':('CASE_DESIGN_PROBLEM',True,False,
    'The long catalog procedure and docket are correctly treated as generic. However the surviving explicit inability to reconstruct ordered overlap (R03) and its source-specific implication for offset support (R08) are material constraints. This was not a generic-only control; increasing prose did not cause its keep result.'),
 'H2-545059f94c7b':('STRUCTURALLY_CONCORDANT',False,False,
    'Distinctive ordered overlap with independent references and anchors supports positions 4-11 at 1901-1908. The rest remains undated by that alignment. The retained local placement is narrower than the deleted global chronology.'),
 'H2-5c20feb8415d':('STRUCTURALLY_CONCORDANT',False,False,
    'The Q-specific differential is warranted, distinctive and useful, while Q membership in the F-17 request path remains unresolved. The judge correctly treats the routing inquiry as generic and retains uncertainty rather than assuming either membership or exclusion.'),
 'H2-622904b211e7':('AMBIGUOUS',False,False,
    'The recorder response itself is valid but off target, and the command plot is generic. The judge assesses the added exact-target negative limitation R05 as warranted/material/relevant but generic. This CORE_INVALID reading is plausible. However other cases count application of missing source prerequisites as distinctive negative remainders; applying the step-response requirement for a process-output trajectory could support the opposite source_derived assessment. The text does not decisively calibrate that distinction. No definite judge error is established.'),
 'H2-6f44184ce89e':('STRUCTURALLY_CONCORDANT',False,False,
    'Independent records and stability checks support weakening two specified steering routes while leaving other routes open. The contact-log inquiry is already present and is not newly invented. The broad steering verdict is lost.'),
 'H2-72fb2477d1bc':('CASE_DESIGN_PROBLEM',True,False,
    'No ranking follows from a completion code, but the surviving restriction on updating only from discriminating observations and the explicit missing predictions support an inquiry into the exact missing diagnostic relation. R04/R05 are a negative differential constraint and necessary inquiry, not an invented response or calibrated equality. The audit wrongly treated all missing-interpretation inquiry as generic without assessing this source-specific application.'),
 'H2-89ae4468006c':('STRUCTURALLY_CONCORDANT',False,False,
    'One examined score still supports a bounded comparative weakening. Losing four broad exoneration claims leaves a small but material source-derived contribution. The model did not confuse its small size with nonviability.'),
 'H2-945fda3cecc8':('CASE_DESIGN_PROBLEM',True,False,
    'Positive packet continuity is correctly disqualified as immaterial and off target. But the text explicitly supplies that histories differ only in earlier internal order and all documented features are later/shared. The custody audit therefore supports a material non-discrimination constraint. R04/R06 are independent of the affirmative identity result. The supposedly target-irrelevant-only control was impure.'),
 'H2-a814c5035bee':('PLAUSIBLE_ALTERNATIVE',False,False,
    'The exact target asks which bounded change measurably reduces delay at the tested point. The two-hour reversible intervention result answers that question intact. Internal causal uniqueness was unnecessary; flags is a reasonable scope result rather than a remainder error.'),
 'H2-af1fe1a18f36':('CASE_DESIGN_PROBLEM',True,False,
    'The audit rejected positive ranking and specific follow-up but missed that destruction of all consistency/inconsistency distinctions itself licenses an ACH-specific prohibition on ranking or eliminating the ordinary-award hypothesis from this table. R07 is warranted, material and directly relevant to what current evidence establishes; no missing rating was reconstructed.'),
 'H2-c5ce20f5d61c':('CASE_DESIGN_PROBLEM',True,False,
    'The source-specific limitation was explicit before measurement: counts cannot reconstruct ordered patterns or positional overlap. R03 and added R08 materially constrain what chronological support exists. The authoring audit inspected positive offsets and generic chronology but failed to recognize this negative contribution.'),
 'H2-de38329a6cac':('PLAUSIBLE_ALTERNATIVE',False,False,
    'The surviving oracle, {a,b} reproduction and negative singleton tests establish the exact requested sufficient 1-minimal reproducer. Unique causation is beyond the bounded target, so removing it leaves that target contribution substantially intact.'),
 'H2-eb081c18a2e8':('CASE_DESIGN_PROBLEM',True,False,
    'The custody audit expressly separates recorded events from unobserved decisions and gives the record no coverage of the feature distinguishing the histories. R04/R05 license a bounded non-discrimination constraint. The primary core design, like control C, overlooked that source-derived negative evidentiary contribution.')
}

def main():
    r.verify_results('claim-warrant',True);r.verify_results('artifact',True)
    freeze_checkpoint=r.git('log','-1','--format=%H','--',r.rel(H/'artifact-freeze.json')).decode().strip()
    rows=[]
    for cid in c.read(H/'manifest.json')['case_order']:
        a=c.read(H/'judgments/artifact'/f'{cid}.json')['remainder_viability'];d=c.read(H/'hidden-design'/f'{cid}.json')
        category,design_problem,judge_error,note=NOTES[cid]
        focus=a['strongest_surviving_target_inference']['remainder_id']
        if focus is None:focus='R05' if cid=='H2-622904b211e7' else 'R01'
        candidate=next(x for x in a['candidate_remainders'] if x['remainder_id']==focus)
        fields={key:candidate[key]['status'] for key in c.DIMENSIONS}
        if cid=='H2-622904b211e7':fields['source_derived']='UNCERTAIN'
        rows.append({'case_id':cid,'category':category,'case_design_problem':design_problem,'judge_remainder_error':judge_error,
            'judgment_sha256':c.sha(H/'judgments/artifact'/f'{cid}.json'),
            'hidden_hypothesis':d['hypothesis'],'observed_status':a['artifact_status'],
            'focus_candidate_id':focus,'focus_candidate_text':candidate['inference'],
            'focus_source_spans':candidate['source_spans'],'operator_viability_assessment':fields,
            'questions':{
                '1_warranted':{'answer':fields['warranted'],'evidence':'Checked the cited surviving spans against the original mapping and measured deletion set. '+note},
                '2_distinctively_source_derived':{'answer':fields['source_derived'],'evidence':candidate['source_derived']['rationale'] if category!='AMBIGUOUS' else note},
                '3_material':{'answer':fields['material'],'evidence':candidate['material']['rationale']},
                '4_exact_target_relevance':{'answer':fields['target_relevant'],'evidence':candidate['target_relevant']['rationale']},
                '5_invented_repair':{'answer':'NO_CONFIRMED_ERROR','evidence':'Added candidates use existing limitations or direct entailments; they do not supply new empirical results. Necessary inquiry is not represented as already successful. The step source-specificity issue remains ambiguous.'},
                '6_overlooked_explicit_viable_remainder':{'answer':'AMBIGUOUS' if category=='AMBIGUOUS' else 'NO','evidence':note},
                '7_kept_due_to_procedure_volume':{'answer':'NO','evidence':'The ruling is tied to named assessed candidates; generic descriptions and off-target positive results are explicitly disqualified. Long control B is retained for the same negative crossdating constraint as its short primary counterpart.'},
                '8_hidden_design_misclassification':{'answer':'YES' if design_problem else 'SCOPE_ALTERNATIVE' if category=='PLAUSIBLE_ALTERNATIVE' else 'UNRESOLVED' if category=='AMBIGUOUS' else 'NO','evidence':note}},
            'finding':note,
            'all_candidates_inspected':[x['remainder_id'] for x in a['candidate_remainders']],
            'judge_added_candidates_inspected':[x['remainder_id'] for x in a['candidate_remainders'] if x['origin']=='judge_added']})
    pairs=[]
    byid={x['case_id']:x for x in rows}
    for pair in c.read(H/'hidden-design/pairs.json'):
        pairs.append({'mechanism_key':pair['mechanism_key'],'case_ids':pair['case_ids'],
            'review_categories':[byid[cid]['category'] for cid in pair['case_ids']],
            'eight_question_audits':[{'case_id':cid,'reference':'case_reviews.questions'} for cid in pair['case_ids']],
            'interpretation':'The intended exact reduced/core pair was not realized. '+('Only this pair separated viable/nonviable mechanically, but the core source-specificity decision remains ambiguous.' if pair['mechanism_key']=='step' else 'The intended core retained a defensible negative evidentiary contribution.')})
    r.write(H/'review/operator.json',{
        'type':'post_freeze_operator_review_not_independent_rater_evidence','at':r.now(),
        'artifact_freeze_checkpoint':freeze_checkpoint,'artifact_freeze_sha256':c.sha(H/'artifact-freeze.json'),
        'claim_freeze_sha256':c.sha(H/'claim-warrant-freeze.json'),'model_outputs_rewritten':False,
        'case_reviews':rows,'pair_reviews':pairs,
        'failure_mode_findings':{
            'mechanism_death':'One measured CORE_INVALID (step input recorder) with DOES_NOT_SURVIVE. Differential diagnosis instead yields PARTIALLY_SURVIVES and reduced scope through a negative diagnostic constraint. The lone core is ambiguous under the operator source-specificity audit.',
            'generic_remainder':'No artifact has generic_remainder as its controlling failure reason. Crossdating primary/control B retain explicit ordered-overlap insufficiency. Generic docket/listing candidates are correctly rejected individually, so this does not establish a tendency to treat generic residue itself as viable.',
            'target_payoff_loss':'No artifact has target_payoff_loss as its controlling reason. Custody and pooled-flag positive results are individually disqualified for target relevance, but source-specific negative evidentiary constraints keep the artifacts. Control C did not isolate purely off-target residue.',
            'epistemically_empty':'No artifact has epistemically_empty as its controlling reason. This failure mode lacks a demonstrated clean example in the measured corpus.',
            'negative_evidentiary_constraints':'Five primary core hypotheses and controls B/C were false passes of the semantic authoring gate. The broad materiality definition permits useful evidentiary limits and next inquiries, which the audit omitted or prematurely called generic.'},
        'prominent_limitations':[
            'Seven intended nonviable primary/control cases retained defensible source-specific negative constraints. The premeasurement audit files remain unchanged; their passing flags were not reliable evidence that the semantic gate was truly satisfied. Had these remainders been recognized then, measurement should have stopped under the gate.',
            'Three intended reduced members retained their exact bounded target answers substantially intact. Their flags outcomes are plausible alternatives, exposing sensitivity to target narrowing and the distinction between advertised overclaims and material target scope.',
            'The single CORE_INVALID distinguishes generic absence-of-outcome reasoning from source-specific negative constraints in other cases. That distinction remains ambiguous rather than independently validated; no confirmed judge remainder error is asserted.',
            'All 100 assessed candidate warrant fields are YES. The corpus does not provide artifact-stage evidence for NO or UNCERTAIN warrant decisions after deletion.',
            'Primary signals differ in informative content and explicitly state missing relations. This is authored boundary calibration, not an isolated manipulation of one viability dimension or an estimate of natural-output performance.',
            'Measured delta deletion ratio is 1.28 after the judge rejected an extra assertion that all flag/F combinations occur; intended balance was below 1.06.',
            'Operator authoring and review share an author/context, and the controls overlap their primary constructions. Neither the audit nor candidate-level counts are independent-rater evidence.'
        ],
        'research_answers':{
            '1_small_viable_vs_none':'The tiny ACH control survives with reduced scope. The only measured no-viable case is step-response, whose source-specificity boundary remains ambiguous in review.',
            '2_activity_without_target_payoff':'Executable activity and source-derived recorder response coexist with measured CORE_INVALID in step-response; the broader generalization is not established.',
            '3_generic_vs_distinctive':'The judge distinguishes generic candidate residue from operational consequences, but no clean generic-only artifact reached the intended outcome because negative source-specific constraints survived.',
            '4_target_irrelevant_source':'Off-target custody/flag/recorder results are correctly disqualified as candidates. Control C remains viable through a separate target-relevant negative constraint, so an artifact-level target_payoff_loss route was not demonstrated.',
            '5_differential_mechanism_death':'Not demonstrated: the intended death case yields PARTIALLY_SURVIVES via the source-specific restriction on comparative updating and a necessary diagnostic inquiry.',
            '6_crossdating_generic_remainder':'Not demonstrated at artifact level: both primary core and control B retain an explicit ordered-overlap insufficiency result and yield DISTINCTIVE_REMAINDER.',
            '7_genuine_uncertainty':'Demonstrated in control D: the Q differential is warranted but its membership in the F-17 request path is unknown; no definite viable candidate is invented.',
            '8_four_properties_vs_volume':'The tiny control survives and long generic procedures are not counted as source-derived. Every status follows the four-field contract, but deterministic compliance alone is not independent evidence that source-specificity/materiality are calibrated.',
            '9_without_graph_labels':'Rationales address surviving evidence and target scope without intended graph-centrality labels. Exact intended reduced/core outcomes occur in zero of six pairs; viable/nonviable separation occurs mechanically in one, with operator ambiguity.',
            '10_dominant_limitation':'Case design remains the dominant limitation: seven nonviable hypotheses missed negative evidentiary contributions, compared with zero confirmed judge remainder errors and one ambiguous classification.'
        },
        'interpretation':{
            'summary':'H.2 completed 57 claim and 16 artifact observations, but did not establish a robust reduced-scope/CORE_INVALID calibration boundary. Most intended core constructions remained viable through source-specific negative evidentiary constraints that the authoring gate missed.',
            'boundary_operational':'Not yet demonstrated robustly. Outputs obey the four-part derivation, but zero of six pairs realize the intended reduced/core labels; only the step pair separates viable from nonviable, and its core source-specificity decision is ambiguous.',
            'absence_vs_centrality':'The measured CORE_INVALID is explicitly justified by absence of a four-YES remainder, not claim centrality. This is better aligned with the revised construct, but one ambiguous core observation cannot establish improved calibration or broad superiority over graph-based explanations.',
            'natural_output_readiness':'Not ready for a fresh natural-output admission experiment. First settle when a source-specific evidentiary-insufficiency result is itself a material remainder, and distinguish it operationally from generic lack-of-evidence commentary.'},
        'recommended_next_step':'Revise the authoring audit to require explicit negative-evidentiary candidates and useful stopping/inquiry rules for every proposed core. Clarify the source-specificity boundary for missing prerequisites using the step/diagnosis/crossdating contrasts, then author a small genuinely no-viable-remainder calibration before any new provider measurement. Do not impose a blanket ban on negative remainders. This recommendation is not executed.'
    })

if __name__=='__main__':main()
