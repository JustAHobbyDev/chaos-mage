"""Post-freeze authored interpretations; never reads operator intent as an answer key.

Run once to publish the review JSON. Mechanical relations always come from the
original frozen judgments; the prose below is an operator audit, not adjudication.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import runner as r
import metrics

# Order: decisive reasoning, evidence context, depth/propagation/reach,
# opponent consistency, outcome authorship, stage transition, interpretation.
CASES = {
 'C001': [
  'Family A sees custody and alignment as ordinary archival chronology; Family B treats the ordered sequence, gaps and pattern warrant of alignment as a material departure.',
  'Both see the same letters, calendar and receipts. Their results agree on weeks 11, 12, 13 and 15. Repeated fair events exist in the calendar but no letter refers to fair; Family B invokes a distinction that is not exercised by this realized sequence.',
  'Family B gives alignment depth and propagation; the families disagree about whether its altered warrant governs more of the full task or merely reconstructs the same chronology.',
  'Neither mapping has another primary opponent. Overall relations survive the reversal in both stages; this cannot establish opponent independence.',
  'All referenced events are unique, making alignment relatively easy. Custody receives independent receipts and a dated event, so neither branch is starved of evidence.',
  'Both families retain their relation; Family B becomes close in consequence.',
  'A persistent baseline and meaningfulness disagreement, not literal unequal evidence. Exotic source identity alone is insufficient to resolve it.'
 ],
 'C003': [
  'Both favor reduction: the object of inquiry becomes a failure-preserving rule configuration and tested deletions rather than a list of separately suspected rules.',
  'Reduction exhausts its 20-trial cap with a remaining BDE failure and incomplete minimality checks. Family A preserves the lack of a BD-alone sufficiency test; Family B overstates necessity within BDE from other passing subsets.',
  'Reduction changes decomposition and the reason to conduct subsequent deletion tests. Breadth across the complete proposal task is less settled than its local configuration warrant.',
  'Bisection failed admission, so no repeated-opponent triangle remains.',
  'The frozen world contains a B-and-D interaction, which favors configuration reasoning. Diagnosis still produces discriminating results. Reduction also receives more explicit analytical narration.',
  'Reduction dominates for both families at both stages.',
  'A useful stable direction with bounded evidence; the judgment must not be read as proof that the executed procedure found a minimal sufficient failure set.'
 ],
 'C004': [
  'Both favor inverse reconstruction over the competing-hypothesis matrix because route measurements become equations constraining latent component delays and identifiability.',
  'The same additive route world supports both. Nominal reconstruction uses the held-out route to separate A and D; the common 1 ms measurement bound limits exact numerical claims.',
  'Local warrant and decomposition favor inverse reconstruction. Task reach is not inferred from these criterion counts.',
  'Inverse reconstruction also dominates diagnosis in C013 for both families and stages. This is consistent across its two opponents.',
  'An additive noiseless realization with informative route membership is favorable to inversion. Those properties predate mappings, and the matrix obtains nontrivial contradiction evidence.',
  'Unchanged inverse dominance in both families.',
  'One of the clearest common-world contrasts, conditional on an unusually well-specified inverse problem.'
 ],
 'C006': [
  'Both prospectively favor assembly-hypothesis comparison over custody. In consequence, Family A sees the matrix as largely familiar collation; Family B retains assembly dominance.',
  'The reliable B-before-C join already excludes H3 in the initial state. The matrix mainly makes shared implications explicit and leaves H1/H2 unresolved.',
  'The disagreement concerns whether broad hypothesis bookkeeping is itself displaced reasoning. Task-wide coverage does not establish a novel warrant.',
  'Family B gives this matrix broad material novelty against custody but discounts it as ordinary against the probe in C012. The difference is not automatically inconsistent, but its changing baseline description is an opponent-framing concern.',
  'The matrix obtains little new discriminatory information; this was fixed by the initial world, not a post-measurement change.',
  'Family A weakens dominance to equality; Family B is stable. Reversed consequence C009 changes Family A back to assembly dominance.',
  'The stage change is plausible but cannot be confidently attributed to consequences alone given the presentation-control change.'
 ],
 'C007': [
  'Both favor the controlled latent-trace probe over custody because it makes an otherwise inaccessible overwritten reading into evidence with assay and control warrants.',
  'Q lies below R on A. A separate day-4 witness to Q does not date Q on A or supply a day-4 lower bound on its revision. Family B nevertheless infers a day-4-to-day-12 revision window in consequence.',
  'The probe changes local observability and inferential warrant strongly; its physical result does not itself settle the whole assembly history.',
  'The probe is also central in C012, but broad assembly comparison provides a countervailing respect there. This is a coherent partial-order possibility.',
  'A positive recoverable trace and successful controls were authored before the probe mapping. They are still favorable choices, not empirical evidence of typical assay informativeness.',
  'Probe dominance is stable in both families.',
  'Stable direction coexists with an unsupported chronological inference. Direction agreement does not validate the rationale.'
 ],
 'C008': [
  'Family A treats whole-document and clause provenance as comparable ordinary reporting work; Family B treats clause-level lineage as a material change in the unit of evidence.',
  'The receipt authenticates the complete BD document, whose known contents include exact K. Family B discounts its clause-level implication. The clause outcome also labels a memo about K as a K occurrence although its displayed text does not quote K.',
  'The families disagree on whether a finer provenance unit supplies greater local depth, propagation and reach, rather than a routine change of granularity.',
  'This is the sole surviving same-source pair. Both overall relations survive reversal; Family B changes some trajectory/propagation diagnostics in consequence.',
  'Reads, analysis passes, time and followup are identical. The clause representation can appear stronger because its labels overstate one record; full-document authentication is simultaneously underused in a judge rationale.',
  'Relations are stable; Family A confidence rises from close to clear.',
  'Common bytes expose rather than eliminate interpretation drift. The result cannot establish that finer units are generally more displacing.'
 ],
 'C010': [
  'Both favor the exposure step over serial monitoring: response shape and timing become a designed dynamic inquiry rather than a persistence check.',
  'The packet specifies a pre-rollout baseline, an adverse current snapshot, reset replicas, a 0-to-1 step and holding current settings without fully specifying the initial input state. Family B interprets step and hold as different starting exposures.',
  'Both see a local and downstream operational change. Six hours do not establish equilibrium, a unique mechanism or a completed response-to-action rule.',
  'Narrow routing-step exclusion removes the intended repeated-source scope comparison.',
  'Finite potential-response arrays give the step a prominent transient and monitoring a mostly flat plateau. This is coherent as a lookup world but its physical initial-state semantics are underspecified.',
  'Step dominance is stable for both families.',
  'Treat this as a limited synthetic contrast. The physical same-start requirement is not fully established by byte identity; this weakens its evidential value.'
 ],
 'C012': [
  'Both prospectively identify a tradeoff: probe depth and harder-to-reduce assay warrant versus assembly comparison across the larger formation problem. In consequence Family A retains it; Family B favors the probe.',
  'The probe recovers Q below R; the matrix mostly retains H1/H2 and rejects already-disfavored H3. Family B also introduces an unsupported day-4 revision lower bound, while Family A explicitly withholds it.',
  'This is the clearest local-depth versus task-reach tradeoff. Family B discounts the matrix advantage after seeing weak discrimination; propagation and full-task reach are not interchangeable.',
  'Compare C006: Family B gives the matrix substantial task-wide novelty against custody but treats it as near-native against the probe. Comparative relations can change by opponent; changing the native characterization itself remains concerning.',
  'A positive latent trace is paired with largely redundant matrix evidence. Freeze order rules out later editing but does not rule out author-selected informativeness favoring the probe.',
  'Family A stays tradeoff; Family B resolves tradeoff to probe dominance. There is no orientation reversal control for this pair.',
  'Tradeoff has concrete content and is not a catch-all. Its survival after consequences depends on centrality judgments, baseline interpretation and authored informativeness.'
 ],
 'C013': [
  'Both favor inverse reconstruction over differential diagnosis: latent additive contributions and the rank of route constraints reorganize evidence and subsequent measurements.',
  'Both can run the same routes and builds. The diagnosis branch chooses serial contrasts; inversion chooses measurements that separate component contributions. No initial evidence is withheld.',
  'The dominant advantage is an altered warrant and decomposition, with subsequent route selection following identifiability rather than a symptom checklist.',
  'Inverse dominance over matrix in C004 agrees with this direction. No cross-opponent absolute scores were requested.',
  'Inversion uses 8 route trials versus diagnosis 6 under a common cap of 10. Unused opportunity is allowed. Exact additive truth and zero realized noise favor the inverse ontology.',
  'Stable inverse dominance in both families.',
  'A robust observed direction within this authored world, not evidence that inversion is generally useful for unconstrained production incidents.'
 ],
 'C014': [
  'Family A sees diagnosis and competing hypotheses as similarly ordinary troubleshooting; Family B favors explicit inconsistency-based matrix reasoning.',
  'Diagnosis records observations with no comparable explicit analytic table despite allocating two analysis passes. Family B uses the missing recorded synthesis as evidence of limited displacement.',
  'The disputed advantage is chiefly warrant and inquiry organization. The broad incident task does not itself favor either source ontology.',
  'Both lose to inversion. Family B supports a complete inverse > matrix > diagnosis chain; Family A leaves matrix/diagnosis unordered by dominance.',
  'Matrix uses 4 trials versus diagnosis 6 under the same cap. Unequal completeness of recorded analysis may inflate the matrix advantage even though resources and initial evidence are equal.',
  'Relations remain stable. Family B becomes close in consequence; reversal preserves both overall relations.',
  'This is a baseline and recording-completeness disagreement. Equal opportunity alone does not guarantee comparably complete consequence descriptions.'
 ]
}

# All eight authored worlds, including every pair removed by admission.
AUDITS = {
 'T01': [
  'Zero realized noise, additive components and identifiable routes favor inversion; matrix has explicit analytic output while diagnosis mainly records observations.',
  'Nominal component values must retain the shared measurement bound. Absence of written diagnostic synthesis is not proof that the practitioner cannot synthesize.',
  'Assumes stable additive routes, reliable build changes and comparable load; these are explicit stipulations, not real-world validation.',
  'World facts were frozen first and are accessible to all operations; author choice of an invertible geometry remains favorable to one source ontology.',
  'Shared cap 10 trials and 2 analysis passes. Diagnosis uses 6 trials, matrix 4, inverse 8; unequal consumption is permitted, unequal opportunity is not observed.',
  'All branches regenerate from W-T01; numerical outcomes coexist. Analytic record completeness is not equal.'
 ],
 'T02': [
  'The clause record labels p6 as an occurrence of K although its text is a memo about K; this could strengthen the clause branch artificially.',
  'The authenticated complete BD hash supports the presence of its known exact K by day 3, but neither branch establishes authorship or wrongdoing.',
  'Distinguish literal clause occurrence, discussion of a clause and full-document content authentication. The packet/derivation labels do not consistently emphasize these distinctions.',
  'The common six records predate mapping authorship. No new record is introduced for either branch, but outcome labeling is an author contribution.',
  'Both use 9 record reads, 2 analysis passes and 75 minutes, with the same followup.',
  'W-T02 record selection regenerates exactly. Literal-occurrence wording is semantically overbroad, which a reference validator cannot detect.'
 ],
 'T03': [
  'Probe receives a positive controlled recovery; matrix largely repeats the initial B-before-C exclusion. This is a material informativeness asymmetry.',
  'Q beneath R licenses local relative order, not the day-4 lower bound inferred by Family B. Neither Q recovery nor custody settles H1 versus H2.',
  'Independent day-4 Q witness is not located on A. Matrix coverage and novelty depend on the native collation baseline.',
  'The positive hidden trace is frozen before mappings but especially useful to the future probe; ordering alone cannot exclude design favoritism.',
  'All branches share caps on record reads, assay trials and analysis. Probe performs 3 assays including controls and one collation; others use records/analysis. No branch exceeds its ledger.',
  'All outcomes regenerate from W-T03 and can coexist. Day-4-to-day-12 revision precision is a judge over-inference, not a derived world result.'
 ],
 'T04': [
  'Route persistence supports monitoring; additive route constraints support inversion. Both produce informative but bounded observations.',
  'Route localization alone does not prove an effective organizational remedy. The monitor mapping failed the unchanged gate rather than receiving an outcome repair.',
  'Synthetic stable additive service times and route membership are supplied; organizational generalization is untested.',
  'World frozen before either mapping. Invertibility still reflects author choices.',
  'Shared cap 8 trials: monitor uses 6 and inverse 8; unused opportunity is allowed.',
  'W-T04 outcomes regenerate. No comparison measured because M001 was Conditional in Family B.'
 ],
 'T05': [
  'A hidden B-and-D interaction favors configuration-based reduction. Its trace has more explicit analysis than diagnosis; bisection localizes a revision but not the interaction.',
  'Capped reduction has not proved minimality or BD-alone sufficiency. Passing BC and DE do not prove standalone harmlessness without an additional arbitrary-subset assumption.',
  'Revision-chain monotonicity does not establish monotonicity over all subsets. The operator knows the interaction but judges must not use hidden truth.',
  'The failure function was committed before the mappings; its interaction structure still favors one method and needs variation in a future replication.',
  'Shared 20-trial cap: diagnosis 5, reduction 20, bisection 5. The cap binds reduction, limiting its conclusion.',
  'All W-T05 trials regenerate. Incomplete minimization is recorded; stronger necessity claims belong to judge reasoning, not the engine.'
 ],
 'T06': [
  'Every event mentioned by a letter has a unique calendar occurrence, making alignment easy. Custody gets independent receipts and a dated event, yielding the same chronology.',
  'The repeated fair event does not occur in the letters. Its presence does not demonstrate that alignment resolved actual ambiguity in this run.',
  'Assumes stable sequence gaps and reliable calendar/receipt content. Ordinary archival pattern comparison is already in the baseline.',
  'All calendar entries and receipts were frozen together; neither branch has a privileged initial chronology.',
  'Both remain within the shared record and analysis ledger. Neither gets an extra external source.',
  'W-T06 yields weeks 11, 12, 13 and 15 for both operations; no outcome contradiction found.'
 ],
 'T07': [
  'Corroboration identifies documentary dependencies; reversal yields baseline 2/4 failures, bypass 1/4, restoration 2/4. Neither gets a perfectly decisive signal.',
  'Documentary localization is not causal proof of a repair, and small reversal counts do not establish a unique failure mechanism.',
  'Stable synthetic replay and source dependencies are stipulated; causality and documentary independence remain different warrants.',
  'All receipts and replay potential outcomes were frozen before mappings. No later facts were added.',
  'Record inspection and replay draw on the same available ledger; no overrun in either branch.',
  'W-T07 outcomes regenerate. M003 failed admission; no displacement comparison measured.'
 ],
 'T08': [
  'Exposure step has a prominent transient; hold is largely a plateau; routing changes only queue. Authored arrays make these distinctions informative by construction.',
  'Six hours cannot establish equilibrium or a unique mechanism. No completed action/window rule should be credited beyond what is actually recorded.',
  'Baseline 2/4, current 3/8, reset replicas, 0-to-1 steps and holding current settings leave initial input semantics underspecified. Same serialized state does not fully establish physical equivalence.',
  'All three potential-response arrays predate mappings. Lookup provenance proves no mutation but cannot establish an independently warranted causal world.',
  'Common 6 samples, 2 analysis passes, 6 hours and at most 1 input step. Monitoring leaves its step unused; narrow and broad use one. No resource overrun.',
  'W-T08 arrays regenerate exactly. Physical same-start coherence is not fully established; retain this as a material limitation, not a repaired or removed post-measurement pair.'
 ]
}

def build():
    r.verify_results(True)
    fields=('decisive_reasoning','evidence_context','local_depth_propagation_reach','opponent_consistency','outcome_rigging','stage_transition','interpretation')
    audit_fields=('authored_signal_asymmetry','unjustified_decisiveness','hidden_assumptions','world_fact_favoritism','resource_use','world_consistency')
    values={s:r.published(s) for s in ('prospective','consequence')}
    reviews=[];audits=[]
    for p in r.pair_records():
        if p['cohort']!='primary':continue
        cid=p['case_id']
        reviews.append(dict(case_id=cid,relations={s:{f:metrics.normalized(values[s][(cid,f)],p)['overall'] for f in 'AB'} for s in values},**dict(zip(fields,CASES[cid],strict=True))))
        audits.append(dict(case_id=cid,target_id=p['target_id'],**dict(zip(audit_fields,AUDITS[p['target_id']],strict=True))))
    r.write_new(r.HERE/'review/case-reviews.json',reviews)
    r.write_new(r.HERE/'review/outcome-audit.json',audits)
    measured={frozenset((p['mapping_1'],p['mapping_2'])) for p in r.pair_records() if p['cohort']=='primary'}
    planned=[]
    for p in r.read(r.HERE/'operator-manifest.json')['pair_designs']:
        planned.append({k:p[k] for k in ('target_id','mapping_1','mapping_2')} | {'measured':frozenset((p['mapping_1'],p['mapping_2'])) in measured} | dict(zip(audit_fields,AUDITS[p['target_id']],strict=True)))
    r.write_new(r.HERE/'review/planned-outcome-audit.json',planned)
    r.write_new(r.HERE/'review/historical-comparison.json',{
      'prior_report':'distance/review/comparative-displacement-v0.3.md',
      'comparison_policy':'Post-freeze qualitative comparison; no accuracy labels, retrospective revisions or pooled scores.',
      'B1':{'primary_pairs':28,'overall_agreement':22,'jointly_directional':23,'same_direction':22,'opposite_direction':1,'orientation_preserved_per_family':'6/6'},
      'findings':[
        'B.2 removes unequal serialized initial evidence and adds explicit common-world derivation provenance. This is a design improvement, not evidence that interpretation drift declined.',
        'Separating meaningful difference exposes the equality threshold: Family A uses equality in 3 prospective and 4 consequence pairs, Family B in none. The family split persists.',
        'The manuscript probe versus assembly-matrix contrast makes local depth versus broader reach expressible as tradeoff. Both families use it prospectively; one resolves it after consequences. This is conceptually relevant to B.1 but not a matched replication.',
        'No opposite dominance direction occurs in B.2, on only 6 prospective and 5 consequential jointly dominant pairs. Different admission, targets, pair construction and outcome access prohibit a reliability-improvement claim.',
        'B.2 has a consequence presentation-control change whereas B.1 preserved all sampled overall controls. Neither small control set estimates a general rate.',
        'Comparative diagnostics avoid intrinsic per-mapping scale claims, but manuscript baseline descriptions still vary across opponents. Task reach remains especially unstable.',
        'Use a partial-order representation for inspected research; do not infer a total order or deploy it as an autonomous creative-search controller.'
      ]})

if __name__=='__main__':build()
