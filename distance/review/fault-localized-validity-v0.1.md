# Experiment G — Fault-localized transfer viability v0.1

Completed 2026-09-30. The frozen deletion-only rule retained E006 with warrant flags and retained E022/E030 with reduced scope. All three source-derived mechanisms survived; no case was CORE_INVALID. This establishes an inspectable distinction between local and scope-reducing defects in these diagnostic cases. It does **not** establish sensitivity to structurally fatal defects.

## Starting point and checkpoints

Starting clean `main` and fetched `origin/main`: `ac79a379938ae07d5a0a5a65e14c6145b60ed08b`. Publication is the commit containing this report; its exact SHA is reported in the handoff rather than self-embedded in its own contents.

| Checkpoint SHA | Frozen work |
|---|---|
| `2dc0ae017cdc88081a6c4ee17e041a11d96e4cbe` | Freeze load-bearing warrant and core-invalidity threshold |
| `58f1ff0692056560fc4d3cdd53d5589e9b4d0335` | Freeze E006/E022/E030 claim inventory and measurement packets |
| `98367f9aee84bff79da08b4eb6492c9a097cc589` | Recover premeasurement audit and freeze complete atomic inventory |
| `77405dd7957f3d7464d4606d225c53499076a514` | Freeze claim-warrant preflight |
| `a681de3ba95fb5fc4b69307701507e9c0c6b4bb0` | Preserve exact-paragraph quotation failure and non-contaminating recovery proof |
| `dd3f97b1a83e4e8c23027e73a99b26b69702e3ef` | Freeze verified quotation-recovery preflight |
| `826329bd9ce55456ead9652d1ad1e11a7187997a` | Preserve and verify ordered exact-excerpt representation recovery |
| `ec74a2b1b92483ca3b8d65a5fe46befa2f0c2e3d` | Freeze verified exact-excerpt recovery preflight |
| `23633bc6d16874eb0309b6fbfc96e424274faac0` | Freeze claim-level warrant judgments |
| `05b09952c42e3203b2905441a88008fe8733f5fe` | Freeze simultaneous-deletion ablation packets |
| `ddc7c555b4e78def7747db2c3d857bce1e1cd268` | Freeze artifact-ablation preflight |
| `472f3d25bb4addaec1b19730d668bd961717a3e1` | Freeze artifact-level viability judgments |

## Frozen policy and corpus

> An unsupported inference is core-invalidating only when removing that inference destroys the transferred procedure’s distinctive material epistemic contribution to the target.

The policy was committed before detailed case access for G. No operator blinding is claimed. Mechanism survival asks whether a source-derived state → operation → signal → supported-inference chain remains. Target-contribution survival asks whether that chain still materially helps the target, without requiring a complete answer. Dependency analysis traces what actually relies on the deleted claim. Number of defects alone never determines artifact status.

`KEEP_WITH_WARRANT_FLAGS` requires surviving mechanism and substantially surviving contribution. `KEEP_WITH_REDUCED_SCOPE` requires a surviving distinctive mechanism and reduced but material contribution. `CORE_INVALID` requires absent mechanism or no material contribution; total cascade must be reflected in one of those dimensions. `UNCERTAIN_LOAD_BEARING` requires structural uncertainty and means keep plus flag. All four apply only after a defect is established; none is a novelty score. See [frozen threshold](../fault-localized-validity-v0.1/CORE-INVALIDITY.md).

Exactly E006 (Analysis of Competing Hypotheses → procurement steering), E022 (step-response probing → approval handoff delay), and E030 (chain-of-custody verification → literary textual formation) were taken from frozen Experiment E natural mappings. Source paths and SHA-256 digests are in [manifest.json](../fault-localized-validity-v0.1/manifest.json). No mapping was generated and no historical experiment was executed.

## Extraction and measurement

Operator-authored segmentation covered every inference-field sentence or heading, with an explicit non-inferential disposition where appropriate. Operation/signal clauses were included when they themselves asserted evidential consequences. Every child retains an exact contiguous source span, full exact parent, offsets, local context and textual downstream references. Those extraction references are candidate textual links, not pre-judged dependencies. The five-field original mapping accompanied every claim. Opaque IDs carry no verdict labels.

A final premeasurement audit split four alternative-antecedent lists before any provider call: fragility cues in E006, loop cues and delay-localization criteria in E022, and removed-leaf cues in E030. The original 45-claim freeze is archived intact; the corrected complete inventory has 50 claims. No support labels were added during extraction. All model packets were reconstructed by allowlist, without history, old verdicts, case expectations or review questions.

Each claim received one fresh isolated `gpt-6-astra`/high judgment under the execution-prerequisites-satisfied warrant rubric. Each case then received one fresh artifact judgment after the **committed complete claim freeze**. All UNSUPPORTED claims in a case were deleted simultaneously. CONDITIONAL_WARRANT claims were retained with their original status; no UNCERTAIN claims occurred. There were no subset searches, duplicate samples, second models or provider probes.

| Case | Claims | SUPPORTED | CONDITIONAL_WARRANT | UNSUPPORTED | UNCERTAIN |
|---|---:|---:|---:|---:|---:|
| E006 | 20 | 16 | 2 | 2 | 0 |
| E022 | 18 | 8 | 0 | 10 | 0 |
| E030 | 12 | 8 | 0 | 4 | 0 |
| **Total** | **50** | **32** | **2** | **16** | **0** |

## Every unsupported claim

The spans below are verbatim. Sentence fragments inherit the exact parent’s antecedent, modal strength and consequence; they are not standalone paraphrases. Full parent text and unchanged model rationales are linked through the [inventory](../fault-localized-validity-v0.1/claims/inventory.json) and [claim judgments](../fault-localized-validity-v0.1/judgments/claim-warrant).

| Case / ID | Exact span deleted | Judge’s reason |
|---|---|---|
| E006 / [`C-c662394207dc`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-c662394207dc.json) | What remains is a smaller surviving set, which may hold more than one hypothesis. | Comparative inconsistency need not eliminate any hypothesis; a smaller set is not guaranteed. |
| E006 / [`C-aec3f6fb7c89`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-aec3f6fb7c89.json) | the process was irregular | Joint survival of H1/H3 does not establish their shared irregularity premise. |
| E022 / [`C-65fb2166199f`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-65fb2166199f.json) | the handoff holds items in fixed waiting (scheduled review, batch release, transfer latency) | Response delay does not identify fixed waiting at the handoff. |
| E022 / [`C-a6302cc6c88e`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-a6302cc6c88e.json) | not a shortage of processing capacity | The signal does not exclude capacity shortage. |
| E022 / [`C-c3ea44c01d41`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-c3ea44c01d41.json) | a stage that absorbs change through a large backlog | Slow dynamics do not establish a large backlog. |
| E022 / [`C-ee7ba687b92d`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-ee7ba687b92d.json) | improvements there take long to appear end to end | Local stabilization time does not determine when end-to-end improvement first appears. |
| E022 / [`C-fc9f6119cb11`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-fc9f6119cb11.json) | Oscillation without such a match | Unmatched oscillation alone does not identify rework or escalation. |
| E022 / [`C-27bdca332183`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-27bdca332183.json) | - Downstream overshoot after an upstream change suggests the change relocates delay rather than removing it. | A transient peak can coexist with eventual delay reduction. |
| E022 / [`C-3f457e7027ec`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-3f457e7027ec.json) | - No end-to-end change despite a local improvement suggests the binding delay lies at another handoff. | No aggregate change does not locate the binding delay elsewhere. |
| E022 / [`C-1aeee26e0610`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-1aeee26e0610.json) | Delay accumulates at the stages showing the longest dead time | Late downstream response can reflect upstream propagation rather than local waiting. |
| E022 / [`C-b4c28e8bfd92`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-b4c28e8bfd92.json) | the slowest settling | Slowest settling need not locate accumulated delay. |
| E022 / [`C-446e025f2e0e`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-446e025f2e0e.json) | keep the record as evidence of saturation or non-settling at that operating point. | An abort can occur during a transient that would later settle. |
| E030 / [`C-3d03b6585877`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-3d03b6585877.json) | the arrangement examined is the arrangement the author left | A continuous ledger can document later rearrangement. |
| E030 / [`C-ed9468fc8969`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-ed9468fc8969.json) | its order can be used as evidence of authorial assembly | The authorial-arrangement premise is unlicensed. |
| E030 / [`C-e81bb1689f0d`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-e81bb1689f0d.json) | The sequence offered as best explaining the draft is the one that leaves the fewest breaks and contradictions | Fewest gaps is not an established best-explanation ranking rule. |
| E030 / [`C-8774b2c56a72`](../fault-localized-validity-v0.1/judgments/claim-warrant/C-8774b2c56a72.json) | gaps in numbering indicating removed leaves | Numbering discontinuity does not establish physical leaf removal. |

## Conditional and uncertain claims

**Every UNCERTAIN claim: none.** This observed zero does not establish that uncertainty handling is calibrated.

The two CONDITIONAL_WARRANT judgments both belong to E006:

- `C-3441c1d0bd7c`: narrowed specifications after bidder contact would be more expected under H1/H5 than H2.
- `C-6e35cd133b10`: unexplained post-opening score changes would be less expected under H2.

In each response, the stated empirical relation is the same proposed comparative expectation as the claim. The mapping labels these as conditional illustrations, and for specification narrowing it explicitly acknowledges unknown diagnosticity. Nevertheless, using the claim itself as its licensing relation is a potential circularity at the CONDITIONAL_WARRANT boundary. The operator does not replace these judgments or ablate them as unsupported. The surviving general ACH mechanism does not require either illustrative expectation to be established. A later protocol should clarify when a stated empirical relation is independently checkable rather than merely a restatement of the conclusion.

## Artifact ablation results

| Case | Unsupported spans deleted | Mechanism | Target contribution | Artifact status |
|---|---:|---|---|---|
| E006 | 2 | `survives` | `substantially_survives` | `KEEP_WITH_WARRANT_FLAGS` |
| E022 | 10 | `survives` | `reduced_but_material` | `KEEP_WITH_REDUCED_SCOPE` |
| E030 | 4 | `survives` | `reduced_but_material` | `KEEP_WITH_REDUCED_SCOPE` |

The distinction is visible without equating mechanism with target contribution: all mechanisms survive, while the target contribution substantially survives in one case and is materially reduced in two. Zero cases are CORE_INVALID; zero are UNCERTAIN_LOAD_BEARING. These unobserved categories remain untested here.

## E006 qualitative audit

The ACH chain remains operational: live competing explanations and itemized records → cross-hypothesis ratings weighted by authentication/independence, second rating and sensitivity tests → comparative inconsistency and fragility → conditional weakening of explanations. The intact first inference sentence already licenses that bounded weakening. No replacement inference is needed.

Deleting guaranteed set shrinkage removes an overpromised outcome, not the ability to compare or pursue evidence. Deleting the irregularity assertion removes a reporting license; H1/H3 survival can no longer be reported as an established irregular process. The dangling “that” in the remaining intent clause cannot quietly reinstate the deleted fact. Follow-up on discriminating records, reporting alternatives together, and stopping/reopening rules retain their independent operational basis. The useful target contribution remains essentially the same, supporting KEEP_WITH_WARRANT_FLAGS.

The set-shrinkage judgment is a new measured defect beyond the historically emphasized irregularity claim. There is an interpretive boundary: the surrounding weakening sentence could be read as conditioning the next sentence on an actual elimination. The judge instead read “What remains is a smaller surviving set” as a guarantee. Both that ambiguity and the returned UNSUPPORTED label are retained. Useful ACH machinery does not make the irregularity claim licensed.

## E022 qualitative audit

The intact chain remains: authorize and apply one bounded input step → record stage and end-to-end trajectories with disturbance monitoring → observe non-settling/cycle-linked/steady-state features → make bounded inferences and assess candidate remedies through reversal and repetition. The procedure still measures a source-specific response to intervention.

Major diagnostic branches are lost. Long dead time no longer identifies fixed waiting or excludes capacity shortage; slow rise/settling no longer identifies backlog or predicts end-to-end improvement lag. Unmatched oscillation loses its loop diagnosis. Overshoot loses the delay-relocation conclusion, and unchanged aggregate turnaround loses the elsewhere-bottleneck conclusion. The target localization alternatives using longest dead time or slowest settling are removed. An abort still requires reversion but no longer automatically establishes saturation/non-settling.

The explicit intake-step/non-settling sentence remains an independent bounded localization contribution; it need not be reconstructed from the damaged summary sentence. The intact process-setting/steady-state estimate and the conjunctive candidate-remedy rule remain material answers to the bounded-change half of the question. The original no-sustained-overshoot criterion can survive without claiming that every overshoot proves relocation. The explicit backlog → improvement-lag dependency is lost, but the measurement, stopping and repeat/reverse operations do not depend on it. This is a material scope reduction, not a harmlessness judgment.

## E030 qualitative audit

The ledger chain remains: identify units → separately record compositional and later handling with evidence tags → inspect continuity and contradictions → support bounded unit-level sequences, grade claims, retain compatible alternatives, and target open-break inquiries. The retained compositional-ledger inference remains subject to the mapping’s explicit reliability and retrospective-reconstruction limits. It is not proof of a whole composition history. The surviving unit-level reconstruction claim was judged SUPPORTED, but this experiment does not independently establish whether evidence tagging adequately addresses circularity in trace-derived ledger entries.

The post-compositional continuity → unchanged authorial arrangement → authorial-assembly evidence cascade fails. A ledger can document rearrangement perfectly. The fewest-breaks → best-explanation selection branch also fails, removing a substantial advertised answer to “best explains.” Numbering gaps can no longer be converted into a removed-leaf event; no weakened substitute for that deleted span was inserted.

All six numbered operations remain textually present, but textual executability alone is not the reason to retain the transfer. Independent bounded sequence support, localized uncertainty, competing sequences, and specific already-listed inquiries supply its surviving material contribution. Inventorying present order and investigating earlier states continue without warranting that the present order is authorial. KEEP_WITH_REDUCED_SCOPE therefore reflects both a substantial loss and a non-generic remainder.

## Dependency and no-repair audit

The artifact responses give per-claim signal/dependency records for all 16 unsupported IDs. Strong explicit links are E022’s backlog → improvement-lag “so” clause and E030’s unchanged-arrangement → evidential-use “so that” clause. E006’s defects are outcome/reporting leaves, with no necessary downstream investigative branch. E022 loses several diagnostic interpretations but retains intervention testing. E030 loses authentication and ranking but retains local historical constraints.

The operator found no invented operation, measurement, hypothesis, evidence item or replacement ranking rule needed for the three retention decisions. Surviving operations cited in the responses are already in the original mappings. No semantic repair was performed on any packet or response. The ablation bytes are mechanically reproducible as original text plus exact deletion markers.

Two qualifications matter. First, per-claim arrays mix failed dependencies, candidate uses that survive independently, and statements that no further explicit consequence exists. The prose generally distinguishes them, but they are not a uniform typed dependency graph; repeated-judge consistency was not measured. Second, exact contiguous spans do not always form grammatically independent units. In E030, deleting “gaps in numbering indicating removed leaves” also removes the shared predicate after the retained “stubs” fragment. In E022, deleting the longest-dead-time span removes the head of a summary list, and deleting the unmatched-oscillation alternative removes shared wording. The artifact judge avoids relying on the damaged summary, keeps the re-entry branch within its original oscillation context, and never restores the removed numbering-gap claim. Retention relies on other intact chains. These are conservative, inspectable ablations, but atomization and shared-context handling need better calibration before adoption.

## Historical comparison and warrant poisoning

Historical judgments were opened for comparison only after both result freezes. They were absent from measurement packets.

| Case | E Astra | E Fable (descriptive only) | F prospective Astra | G artifact policy |
|---|---|---|---|---|
| E006 | Invalid | Valid | Valid | KEEP_WITH_WARRANT_FLAGS |
| E022 | Invalid | Conditional | Invalid | KEEP_WITH_REDUCED_SCOPE |
| E030 | Invalid | Conditional | Invalid | KEEP_WITH_REDUCED_SCOPE |

The clearest observed historical warrant-poisoning example is E006: E Astra explicitly recognized that most of the ACH transfer was preserved, then made the whole mapping Invalid because of the irregularity inference. G independently identified that defect, identified an additional set-shrinkage defect, and found that deleting both leaves the material ACH contribution substantially intact. This demonstrates the loss induced by the old artifact-level gate for this case; it is not a measured claim that a production generator actually discarded it. E022 and E030 likewise show that global failure can obscure substantial surviving branches, but their losses warrant downscoping rather than treating the defects as harmless.

F’s E006 Valid result remains a historical fact. It should not be rewritten as a fault-localized result: F made a whole-mapping prospective judgment and did not separately flag these claims. F remains **15 Valid, 5 Conditional, 10 Invalid**, with **13 eligible, 13 < 18**. G does not recalculate F’s cohort, waive the original dual-family admission rule, or integrate a new production gate.

## What counts against the approach; limits

| Failure concern | Observed evidence and remaining limitation |
|---|---|
| Every defect becomes CORE_INVALID | Not observed: none did. No positive fatal case was measured, so rejection sensitivity remains unknown. |
| Almost every defect becomes harmless | Not the artifact result: two of three cases lose material scope. All three are retained, so retention bias remains a concern requiring fatal controls. |
| Classification requires invented repairs | No replacement method was required in this audit. Shared syntax/antecedents create interpretation risk that should not be hidden. |
| Dependencies cannot be identified consistently | Explicit dependencies and independent surviving actions are inspectable, but output edge types are mixed and single-sample consistency is unmeasured. |
| Mechanism and target contribution collapse | They differ here: mechanism survives for all, target contribution differs. More diverse cases are needed to test the boundary. |

Three purposively selected diagnostic cases are not a representative sample. Atomic extraction is an operator judgment, not a model measurement or a uniquely correct partition. One Astra sample per claim and artifact measures neither within-model stability nor cross-model robustness. No actual procurement records, workflow trials, or draft-handling evidence were collected. The findings concern proposed procedures and conditional epistemic contribution. No historical eligibility or operational efficacy follows from retention.

## Integrity, recovery and verification

There were **53 provider requests and 53 unique sessions**: 50 claims plus 3 ablations. No harness retries, duplicate samples, substitutions observed in returned metadata, or replacement judgments occurred. Requested model/effort and pinned CLI hashes are recorded. Returned served-model identifiers were unavailable; requested Astra is not promoted into a verified serving snapshot. Hidden provider-internal behavior is not observable from these records.

Premeasurement recovery retained the earlier inventory and failed historical preflight, then corrected extraction and used a G-owned historical adapter. It verifies all live historical bytes before scoping only legacy Git addition queries to their historical boundary, using F’s existing recovery-aware verification rather than modifying F. Two later stops were representation-only quote-validator failures: one response joined exact paragraphs, another joined an exact heading and non-adjacent bullet. Both passed the unchanged frozen JSON schema. Additive source-offset/hash proofs validated their literal excerpts without changing any packet, classifier, model judgment or response byte. Original stops and failed validations remain preserved. Each resumption followed committed evidence and all 41 successful historical/local preflight checks.

The final local suite passes all **34 tests**. The final audit reconstructs distributions from frozen responses, checks all 53 sessions and execution commits, checks launch chronology against append-only RUNNING/paused/terminal events, and confirms no launch during a pause. Two recovered original failed-validation records are counted directly; an older helper’s summary field counted only its first recovery and is superseded by this additive count without changing measurements. All **2,934 pre-G tracked files** match their starting hashes. The final runtime inventory is sealed after measurement. Raw CLI events remain in the local ignored runtime archive, bound by published hashes; model judgments, request configurations, validation metadata and freeze records are committed.

Reproduce local validation with `python -B distance/fault-localized-validity-v0.1/publication.py verify` and `python -B -m unittest discover -s distance/fault-localized-validity-v0.1/tests`. The historical preflight records enumerate the 40 historical checks plus the local suite at each provider boundary.

## Recommendation — not executed

Fault-localized viability appears more appropriate for generator retention than failure-dominates global invalidity in these cases: it preserves useful source-derived structure while explicitly removing unlicensed conclusions and reducing advertised scope. This is evidence for continuing the research, not for production adoption.

Next, preregister a separate versioned validation that audits atomic extraction/shared context and the CONDITIONAL_WARRANT boundary, includes cases with independently established structurally fatal defects, and tests dependency judgments for stability. If that supports adoption, run a new versioned admission experiment. Do not revise F or reuse G to recalculate its eligible cohort. No recommendation has been executed; work stops after G.
