# Ontological transfer model refactor v0.3

2026-09-27. **Conceptual refactor informed by v0.2, not evidence that the new
classifier is reliable. No new calibration was executed.**

## Why the four-class model was retired

The [completed v0.2 report](boundary-calibration-v0.2.md) documents collapse of the
intended Adjacent/Remote observations onto the lower side. Its Remote/Alien side
disagreement concerns displacement despite agreement on weak grounding. Low or
moderate displacement with weak grounding remains awkward in that ordinal model.
Mechanism loss and target-question drift can also masquerade as unusual transfers.

Alien usefully exposed grounding as an independent variable. It is retired from new
displacement output, not deleted from history. Its former position above Remote is
replaced by combinations of Native/Adjacent/Remote with independent grounding.
Historical results retain their original definitions, labels, denominators and
interpretations. No old judgment is converted into a v0.3 observation.

## New sequence and exact gate

[MODEL-v0.3.md](../MODEL-v0.3.md) is the authoritative definition. Assess an explicit
candidate mapping, then transfer validity, then baseline-relative displacement,
then independent grounding. The sequence does not combine the judgments or make
weak grounding a reason for high displacement.

| Criterion | Passing | Conditional | Failing |
| --- | --- | --- | --- |
| Mechanism fidelity | preserved | conditionally-preserved | not-preserved |
| Target fidelity | addressed | conditional | not-addressed |
| Operational coherence | coherent | conditional | incoherent |

Mechanism fidelity preserves the essential five-field source chain and relevant
limits without requiring literal source materials. Target fidelity retains the
posed question or justifies a bounded contribution. Operational coherence requires
an operation-produced signal that warrants the stated inference in the target.

**Valid** requires all three to pass and no unresolved validity conditions.
**Conditional** requires no failure, at least one conditional criterion, and explicit
conditions identifying what must be established and how. **Invalid** follows any
criterion failure, even when another criterion is conditional. An unsupported
inference or materially replaced mechanism cannot be rescued by declaring that a
better future mapping would work.

A reframe records occurrence, original question, reframed question and relationship.
Its original question must equal the retained target verbatim. No-reframe detail
fields are null. A reframe can be useful yet fail to answer the original question;
a candidate against a new question would be assessed separately.

Invalid full records retain the source, question, mapping, criterion reasons and
optional scoped baseline, but displacement and grounding are required nulls.
Conditional records can withhold either downstream judgment as null; populated
judgments require `provisional: true`, and displacement requires a baseline. Valid
full records populate both judgments with `provisional: false`. This flag concerns
conditional applicability, not demonstrated scientific reliability. Experiment A
has a validity-only response contract and never requests the downstream records.

## Stabilized native baseline and displacement

The baseline contains target_domain, target_task (the retained question), a scoped
reference_practitioner, nonempty ordinary_methods and ordinary_evidence lists, and
an uncertainty list. It describes practice without source prompting, independently
of evidence supplied in a particular packet. A missing archive does not redefine
archival evidence as non-native. Practitioner claims remain explicitly unverified.

- **Native:** removing source terms leaves substantially ordinary target practice;
  historical disciplinary origin is irrelevant.
- **Adjacent:** meaningful extension or reinterpretation with ordinary inquiry
  substantially intact.
- **Remote:** substantive change to what the specified practitioner does, notices,
  treats as evidence, infers or investigates next. The new warrant or investigative
  action must matter; unusual vocabulary alone is insufficient.

The original seven dimensions remain entities, relations, processes, operations,
observables, inferences and failure_modes. Each has a rationale and an actual
integer: 0 native, 1 extension, 2 reinterpretation, 3 replacement. There is no total,
average, weighting, scalar distance or numerical class rule.

## Grounding and interpretation modes

Grounding asks whether all essential roles have independent target justification.
Each counterpart records its source role, target counterpart, essential reason,
independent target basis (including explicit absence/uncertainty) and status.

- **Grounded:** all essential roles have independently defensible counterparts.
- **Partially-grounded:** established roles coexist with assumptions, incomplete
  evidence or unvalidated measurements that can in principle be established.
- **Weakly-grounded:** an identified essential role exists mainly to retain the
  source structure; removing the metaphor removes its target justification.
- **Unknown:** available information is insufficient to establish grounding.

Weak grounding does not imply Invalid: a speculative ontology can yield a coherent,
bounded operational inference. An unresolved empirical warrant makes that chain
Conditional; circularity or an unsupported leap makes it Invalid. Grounding does
not automatically lower displacement. The model documents ordinary expertise,
nearby reframing, cross-domain candidates, speculative/ontology-generating modes,
and candidates requiring investigation, without scoring creativity or usefulness.
No retrieval ranking or policy is implemented.

## Freeze and retrospective exercise

The model, canonical schemas and core validator were committed as
`89b5728` before retrospective authoring. Their hashes are retained in
[model-freeze.json](../v0.3/model-freeze.json); no post-freeze contract amendment was
needed. Each example binds the full preparation commit and the model-freeze hash,
plus its original case and judgment hashes.

**RETROSPECTIVE / NON-EXPERIMENTAL.** Twelve examples preserve A and B as separate
historical mappings for six v0.2 packets. Historical seven-field profiles are
rendered into a five-field mapping by joining entities/relations/processes for state
and copying operations/observables/inferences/failure_modes into the corresponding
remaining fields. The original task sentence is retained verbatim as the question; surrounding
historical context/evidence sentences are preserved separately in target.evidence.
This keeps target_task identical across evidence contrasts without adding target facts. New baselines and assessments are explicitly author-informed.
These records test expressiveness, not reliability, and generate no agreement
statistics.

| Historical mappings | Retrospective interpretation |
| --- | --- |
| Crossdating 016-A | Invalid: chronology does not answer present meaning. A proposed chronology question is an explicit reframe; its existence does not repair the original. |
| Crossdating 016-B | Invalid: positional identity membership substitutes for temporal placement, with an unsupported inference to meaning. Reframe and mechanism loss are both visible. |
| Literary tomography 009-A | Conditional / Remote / Weakly-grounded: preserves the proposed path-inversion chain, but the signal, propagation relation and target explanatory bridge need establishment. |
| Literary tomography 009-B | Invalid: coded motif changes or stylometric distances do not themselves instantiate measured propagation through intervening regions. Another mapping could supply that mechanism; this one is not silently repaired. |
| Chromatography 012-A | Valid / Remote / Grounded: established circulation/retention/release supports bounded behavioral distinguishability, not complete conceptual identity. |
| Chromatography 012-B | Conditional / Remote / Partially-grounded: the stronger resolved-profile/reference interpretation depends on record resolution and reference support. |
| Chromatography 013-A and 013-B | Separately retained Conditional / Remote / Weakly-grounded proposals: persistent components and stable partition relations need investigation; missing equipment alone is not the issue. |
| Luminol 003-A | Valid / Adjacent / Grounded: bounded feature detection from final text is possible without proving a revision event. |
| Luminol 003-B | Conditional / Adjacent / Partially-grounded: treating features as vestiges of a prior layer adds a discriminatory bridge that remains unestablished. |
| Luminol 004-A | Conditional / Adjacent / Partially-grounded: archives ground material counterparts but do not guarantee the proposed diagnostic's specificity/sensitivity. |
| Luminol 004-B | Valid / Adjacent / Grounded for its explicitly supplied collation branch: matching features are detectable; formation attribution still needs corroboration. Other offered diagnostic branches remain uncertain. |

See the [example index](../v0.3/examples/retrospective/README.md) for individual
rationales, counterpart inventories, dimensions and preserved historical uncertainty.
The product-proposal-review baseline is identical across 012/013. Retention-based
warrant remains Remote while grounding changes; merely supplying records does not
move the baseline. The same literary-scholar baseline applies to 003/004/009.

The exercise does not force a Valid/Weakly-grounded historical outcome. That tuple
is contractually permitted, including at low displacement, and tested with clearly
synthetic contract fixtures rather than asserted as an experimental finding.

## Next calibration, prepared only

[Experiment A](../v0.3/PROTOCOL-transfer-validity-v0.3.md) contains 24 explicit,
synthetic candidate packets in eight triplets: propagation versus viewpoints,
bisection loss, target drift, detection/inference overreach, missing measurements,
invented counterparts, reframing/persistence and source-material literalism.
Operator intentions include Valid, Conditional and Invalid but remain hidden and
are not ground truth. All copied instruments match accepted source records.

The future design requests one fresh judgment per case from each of two materially
different model families, OpenAI and Anthropic: 48 planned judgments. Exact future
model identifiers, runner commands and capabilities must be verified and committed
at a separately authorized execution-preparation stage. Judges receive identical
substantive instructions and the same fixed candidate, without history, retrieval,
other outputs or operator metadata. This handoff contains no live runner.

The prespecified review includes exact validity/criterion agreement, distributions,
confusion tables, reframe occurrence, all contrast outcomes, shared failures and
Conditional/Invalid discrimination. It does not measure displacement or grounding
reliability. Advancement is an argued evidence review, not an arbitrary threshold;
class collapse cannot demonstrate discrimination. Future sequence: validity, then
baseline/displacement, then grounding, then possible creative-retrieval research.
No later numerical thresholds are preregistered here.

No experiment was executed because the user authorized conceptual refactoring,
retrospectives and protocol preparation only. No calibration results, new reliability
metrics, model judges or provider preflight calls were created.

## Remaining conceptual tensions

1. A stipulated speculative ontology versus an unresolved empirical warrant is a
   real judgment boundary. State which premise is weakly justified and which, if
   any, prevents the operation's inference; a label alone cannot resolve it.
2. A bounded contribution can address a broad question without answering all of it.
   Mere topical association cannot. The chronology/meaning bridge tests this boundary.
3. Essential-role inventories can differ in granularity. Schemas ensure explicit
   entries, not completeness or philosophical truth; review must audit omitted warrants.
4. The fixed practitioner baseline removes evidence-driven movement but remains an
   authored hypothesis needing practitioner evidence and later reliability work.
5. Unknown versus Partially-grounded depends on what the packet actually establishes
   and whether unresolved roles are specified/testable. Do not infer impossibility
   from absence or invent facts to fill the gap.
6. Explicit candidate mappings reduce construction variance, but historical profiles
   contain alternative branches. The collation interpretation is disclosed rather
   than represented as the unique reconstruction of 004-B.
7. Strict contract failures and meaningful judgment disagreements are different.
   Preserve raw future failures, report their denominators and stop scheduling;
   never repair them to improve an agreement result.

## Verification and preservation

The preservation manifest covers all **155 pre-existing distance files and 18 source
instrument files**, plus the historical Problem Frames log, at base commit `b723b8d8f53537c8cd558935aa9492c81d4df07a`.
Existing historical manifests, schemas, harnesses, tests and reports are unchanged.
The original distance README is protected, so the active-model pointer is added to
the root README instead. The new Problem Frames entry lives in `docs/PROBLEM_FRAMES-v0.3.md`.
The first model-freeze commit appended it to the historical log; the full v0.2
verifier exposed that log as an additional frozen input. A subsequent preservation
fix restores its original bytes and moves the new entry to this separate document.
No history was rewritten. The canonical model/contracts did not change.

Offline validation covers enum restrictions, all 81 criterion/final-status
combinations, Invalid nulls, Conditional flags, complete baselines, question identity,
reframe structure, essential counterparts, duplicate keys, exact integer levels,
source/packet identity, independent grounding/displacement combinations, preservation,
freeze provenance, retrospective markers, all case contrasts, blinding, planned
schedule coverage and absence of experimental results.

Run all checks from the repository root:

```sh
python -B -m unittest discover -s distance -p 'test_harness.py'
python -B -m unittest discover -s distance/boundary-v0.2 -p 'test_*.py'
python -B -m unittest discover -s scripts -p 'test_*.py'
python -B -m unittest discover -s distance/v0.3/tests -p 'test_*.py'
python -B distance/boundary-v0.2/harness.py verify
python -B distance/boundary-v0.2/review/verify_review.py
python -B distance/v0.3/verify_preparation.py
git diff --check
```

The completed suites pass **63 tests**: 6 original distance, 16 v0.2 boundary,
8 retrieval and 33 new v0.3 contract/preparation tests. Preservation and both
historical completion verifiers pass. There are no measured v0.3 classifier
outcomes in this report.
