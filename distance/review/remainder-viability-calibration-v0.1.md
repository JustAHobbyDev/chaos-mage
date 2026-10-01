# Experiment H.2 — remainder-viability calibration v0.1

H.2 completed 57 claim and 16 artifact observations, but did not establish a robust reduced-scope/CORE_INVALID calibration boundary. Most intended core constructions remained viable through source-specific negative evidentiary constraints that the authoring gate missed.

## Publication and lineage

Base: `5d22364465c8183581452cc720b21f9bd0cc38b4`. Branch: `experiment-h2-remainder`. No merge to main.
The final publication SHA is the commit containing `publication-manifest.json`; resolve it with the command in metrics.json. Checkpoints preceding publication:

| Checkpoint | SHA |
|---|---|
| construct | `0874cb6554065e19d2cee00611d157ea525f6548` |
| target | `928984a86f1afcef5b4e79293563e51024fbac5f` |
| primary | `fb0626000adc885262b0e44c0eb022cd9159d196` |
| controls | `a77b3cf465a4a490918f0a5c8ee57cf4deb8fa01` |
| claim_inventory | `74264e1d62964ae20ef8b63f1974be531bb39c86` |
| claim_preflight | `18ff89fab68bc5fc01256c040cf6bb997623e764` |
| host_launch_recovery | `5d94b830b465ba8662c618c0f824040aea589a53` |
| claim_freeze | `5bd802b6b03d403096f50d589efc9d55c3be01cf` |
| candidate_freeze | `b706b53c5a0296af2c607036ef6d5d4256f05eca` |
| artifact_preflight | `7a94f09d0a96a2397cdd5e0b41f084220c92c605` |
| artifact_freeze | `8a46800bbd956bccc28d10f5497fc94e21fa36c6` |
| operator_review | `5f9620ae02a3fc4affb30db842b87f82fe8310bc` |

H.1 remains `STOPPED_PREMEASUREMENT_DESIGN_GATE`, with zero provider calls. Historical files and runtime evidence were preserved. Each provider stage passed 46 historical checks plus the H.2 test suite before launch.

A sandboxed detached launcher ended before any reservation or provider call. Its empty files, positive non-contamination proof and passing 47-check recovery were committed before a host-only launcher continued. No observation was retried or replaced. See [recovery evidence](../remainder-viability-calibration-v0.1/recovery/premeasurement-launch.json).

## Construct and paired authoring

**CORE_INVALID means no viable source-derived remainder after all measured unsupported claims are deleted.** A remainder must be warranted, distinctively source-derived, material and relevant to the exact target. Graph position and prose volume do not control status. Unresolved viability or structural contradiction yields UNCERTAIN_LOAD_BEARING; generator policy remains keep + flag.

Six source instruments were reused verbatim from accepted inputs. The source, bounded target and focal object are identical within each pair. Targets were committed before variants. The following questions and narrowing rationales are frozen:

| Mechanism | Bounded target | Narrowing rationale |
|---|---|---|
| Analysis of Competing Hypotheses | What can the current evidence establish or constrain about whether award P-17 was steered? | One award, with weakening and discriminating inquiry counted as material; does not require positive steering attribution. |
| Step-response probing | Which bounded changes measurably reduce delay in process P-17 under the tested operating point? | One process and operating point; bounded effects, constraints and useful inquiry count without internal-cause identification. |
| Chain-of-custody verification | Which assembly-order constraints for draft D-17 are supported by the surviving evidence? | One draft; witnessed order and uncertainty between textual histories count; full authorial reconstruction is unnecessary. |
| Delta debugging | Which deployed-change subset is sufficient and minimal for reproducing failure F under the frozen replay? | One deployment and defined checkout failure; single-removal minimality is a useful bounded answer without unique causal attribution. |
| Dendrochronological crossdating | What chronological placement or offset of sequence S is supported by overlap with independently dated references? | One correspondence sequence; a bounded local offset is meaningful without a unique chronology of the whole bundle. |
| Differential diagnosis | Which of the two specified mechanisms is better supported for failure pattern F-17, and what inquiry does that justify? | Two plausible regression mechanisms and one focal pattern; a relative inquiry priority is meaningful without diagnostic certainty. |

Reduced members preserve a cited bounded comparative, intervention, ordering, reproduction, offset or diagnostic result. Core members retain erased comparison ratings, an input-recorder trace, later custody, a pooled wrong-outcome flag, ordinary documentary dating, or mere test completion. The contrast changes informative evidence, not focal/comparison ownership; it is not a pure graph intervention.

The recorded operator gate marked all twelve primary audits as passing before measurement: each reduced member had a four-YES remainder and every enumerated core candidate had a definite NO. Post-freeze review found five primary false passes because negative evidentiary candidates were omitted or misclassified. All five mapping fields were searched, including negative constraints and meaningful next inquiries. The audits are author hypotheses, not independent-rater truth. [Primary audits](../remainder-viability-calibration-v0.1/authoring-audit/primary.json) and [control audits](../remainder-viability-calibration-v0.1/authoring-audit/controls.json).

The delta draft explicitly made the pooled flag neither necessary nor sufficient for F before freeze, avoiding a negative-flag singleton exclusion. No provider result informed this authoring change.

| Mechanism | Intended deletion max/min | Measured deleted characters (reduced/core) | Measured max/min |
|---|---:|---|---:|
| ach | 1.057 | [141, 149] | 1.057 |
| step | 1.007 | [145, 146] | 1.007 |
| custody | 1.000 | [160, 160] | 1.000 |
| delta | 1.027 | [150, 192] | 1.280 |
| crossdate | 1.006 | [169, 168] | 1.006 |
| diagnosis | 1.032 | [162, 157] | 1.032 |

All intended ratios were below 1.06. Delta debugging exceeded the 1.15 target after an additional measured unsupported span was deleted. This is retained as a measured imbalance, not repaired. Full lengths, fractions, modal/position checks and case provenance are in the authoring audit and metrics.

## Claim judgments, ablation and candidates

57 claim judgments: SUPPORTED=32, CONDITIONAL_WARRANT=0, UNSUPPORTED=25, UNCERTAIN=0.
Every measured UNSUPPORTED span was deleted simultaneously; all other text remained. No subset search, semantic repair or replacement inference was used. All 16 cases were eligible, including empty deletion sets by policy; none actually had an empty set.
88 candidates were frozen before artifact calls. The judge added 12 cited candidates, for 100 assessments. These are correlated, operator-selected text units and direct entailments, not independent observations.

| Viability field | YES | NO | UNCERTAIN |
|---|---:|---:|---:|
| warranted | 100 | 0 | 0 |
| source_derived | 51 | 49 | 0 |
| material | 87 | 13 | 0 |
| target_relevant | 76 | 19 | 5 |

Four-YES candidates: 38. Decisively unresolved candidates (UNCERTAIN with no NO): 3. Exact model outputs remain in judgments; viable_remainder_assessment files are deterministic projections, not rewritten judgments.

## Artifact outcomes

| Status | Count |
|---|---:|
| KEEP_WITH_WARRANT_FLAGS | 3 |
| KEEP_WITH_REDUCED_SCOPE | 11 |
| CORE_INVALID | 1 |
| UNCERTAIN_LOAD_BEARING | 1 |

| Mechanism | Intended reduced member | Intended core member | Viable/nonviable boundary separated |
|---|---|---|---|
| ach | `H2-6f44184ce89e`: KEEP_WITH_REDUCED_SCOPE | `H2-af1fe1a18f36`: KEEP_WITH_REDUCED_SCOPE | False |
| step | `H2-a814c5035bee`: KEEP_WITH_WARRANT_FLAGS | `H2-622904b211e7`: CORE_INVALID | True |
| custody | `H2-16df75b43727`: KEEP_WITH_REDUCED_SCOPE | `H2-eb081c18a2e8`: KEEP_WITH_REDUCED_SCOPE | False |
| delta | `H2-de38329a6cac`: KEEP_WITH_WARRANT_FLAGS | `H2-25d1bd70c84a`: KEEP_WITH_REDUCED_SCOPE | False |
| crossdate | `H2-545059f94c7b`: KEEP_WITH_REDUCED_SCOPE | `H2-c5ce20f5d61c`: KEEP_WITH_REDUCED_SCOPE | False |
| diagnosis | `H2-04edf722fb7e`: KEEP_WITH_WARRANT_FLAGS | `H2-72fb2477d1bc`: KEEP_WITH_REDUCED_SCOPE | False |

| Control | Case | Outcome | Reason |
|---|---|---|---|
| A: tiny viable remainder | `H2-89ae4468006c` | KEEP_WITH_REDUCED_SCOPE | none |
| B: large generic remainder | `H2-53fc9c8368c3` | KEEP_WITH_REDUCED_SCOPE | none |
| C: target-irrelevant source remainder | `H2-945fda3cecc8` | KEEP_WITH_REDUCED_SCOPE | none |
| D: unresolved viability | `H2-5c20feb8415d` | UNCERTAIN_LOAD_BEARING | uncertain |

### All cases and surviving contributions

| Case | Status | Reason | Strongest assessed candidate | Operator category |
|---|---|---|---|
| [H2-04edf722fb7e](../remainder-viability-calibration-v0.1/judgments/artifact/H2-04edf722fb7e.json) | KEEP_WITH_WARRANT_FLAGS | none | Within the specified differential the response favors lock contention over isolated pool exhaustion | PLAUSIBLE_ALTERNATIVE |
| [H2-16df75b43727](../remainder-viability-calibration-v0.1/judgments/artifact/H2-16df75b43727.json) | KEEP_WITH_REDUCED_SCOPE | none | The witnessed opening-section attachment precedes the witnessed binding of the same D-17 packet | STRUCTURALLY_CONCORDANT |
| [H2-25d1bd70c84a](../remainder-viability-calibration-v0.1/judgments/artifact/H2-25d1bd70c84a.json) | KEEP_WITH_REDUCED_SCOPE | none | The recorded reduction establishes single-removal minimality only for the nonzero-exit flag. It does not establish that {a,b} reproduces F or that removing either change eliminates F, so it cannot establish {a,b} as sufficient and minimal for F under the frozen replay. | CASE_DESIGN_PROBLEM |
| [H2-53fc9c8368c3](../remainder-viability-calibration-v0.1/judgments/artifact/H2-53fc9c8368c3.json) | KEEP_WITH_REDUCED_SCOPE | none | The supplied comparison does not support a specific chronological placement or offset of S: the retained counts cannot establish ordered-pattern alignment or positional overlap, and the docket does not anchor an identified S increment. | CASE_DESIGN_PROBLEM |
| [H2-545059f94c7b](../remainder-viability-calibration-v0.1/judgments/artifact/H2-545059f94c7b.json) | KEEP_WITH_REDUCED_SCOPE | none | The independent overlapping pattern supports placing S positions 4 through 11 at 1901 through 1908 | STRUCTURALLY_CONCORDANT |
| [H2-5c20feb8415d](../remainder-viability-calibration-v0.1/judgments/artifact/H2-5c20feb8415d.json) | UNCERTAIN_LOAD_BEARING | uncertain | None | STRUCTURALLY_CONCORDANT |
| [H2-622904b211e7](../remainder-viability-calibration-v0.1/judgments/artifact/H2-622904b211e7.json) | CORE_INVALID | mechanism_death | None | AMBIGUOUS |
| [H2-6f44184ce89e](../remainder-viability-calibration-v0.1/judgments/artifact/H2-6f44184ce89e.json) | KEEP_WITH_REDUCED_SCOPE | none | Recorded-score alteration and bidder-specific authorship of the examined specification are weakened | STRUCTURALLY_CONCORDANT |
| [H2-72fb2477d1bc](../remainder-viability-calibration-v0.1/judgments/artifact/H2-72fb2477d1bc.json) | KEEP_WITH_REDUCED_SCOPE | none | The supplied response R does not warrant ranking lock contention against connection-pool exhaustion, and it does not establish equal support. Before this test can justify revising their relative plausibility, inquiry must establish what it measures and how its observations discriminate between the two mechanisms. | CASE_DESIGN_PROBLEM |
| [H2-89ae4468006c](../remainder-viability-calibration-v0.1/judgments/artifact/H2-89ae4468006c.json) | KEEP_WITH_REDUCED_SCOPE | none | Alteration of the one examined score is weakened. | STRUCTURALLY_CONCORDANT |
| [H2-945fda3cecc8](../remainder-viability-calibration-v0.1/judgments/artifact/H2-945fda3cecc8.json) | KEEP_WITH_REDUCED_SCOPE | none | The recorded post-assembly transfers do not distinguish the competing pre-accession internal assembly orders; documented packet continuity therefore supplies no assembly-order constraint selecting among those histories. | CASE_DESIGN_PROBLEM |
| [H2-a814c5035bee](../remainder-viability-calibration-v0.1/judgments/artifact/H2-a814c5035bee.json) | KEEP_WITH_WARRANT_FLAGS | none | The tested priority step reduces settled end-to-end delay by two hours at this operating point | PLAUSIBLE_ALTERNATIVE |
| [H2-af1fe1a18f36](../remainder-viability-calibration-v0.1/judgments/artifact/H2-af1fe1a18f36.json) | KEEP_WITH_REDUCED_SCOPE | none | The surviving exported comparison cannot rank the three P-17 hypotheses or rule out an ordinary unsteered award: X erases the distinctions between consistency, inconsistency and unrated entries, and no hypothesis-specific conflict or sensitivity result is supplied. | CASE_DESIGN_PROBLEM |
| [H2-c5ce20f5d61c](../remainder-viability-calibration-v0.1/judgments/artifact/H2-c5ce20f5d61c.json) | KEEP_WITH_REDUCED_SCOPE | none | The supplied pattern table and reference dates do not warrant an overlap-based chronological placement or offset of S. | CASE_DESIGN_PROBLEM |
| [H2-de38329a6cac](../remainder-viability-calibration-v0.1/judgments/artifact/H2-de38329a6cac.json) | KEEP_WITH_WARRANT_FLAGS | none | Subset {a,b} is sufficient and 1-minimal for reproducing F under the frozen replay: removal of either retained change eliminates that defined failure. | PLAUSIBLE_ALTERNATIVE |
| [H2-eb081c18a2e8](../remainder-viability-calibration-v0.1/judgments/artifact/H2-eb081c18a2e8.json) | KEEP_WITH_REDUCED_SCOPE | none | The surviving post-assembly custody record supports no constraint that distinguishes the competing pre-accession internal assembly orders of D-17. | CASE_DESIGN_PROBLEM |

A strongest candidate is not automatically viable: its four fields still control. This table includes every KEEP_WITH_WARRANT_FLAGS, KEEP_WITH_REDUCED_SCOPE, CORE_INVALID and UNCERTAIN_LOAD_BEARING case.

## Failure modes and operator audit

| No-viable-remainder reason | Count |
|---|---:|
| mechanism_death | 1 |
| generic_remainder | 0 |
| target_payoff_loss | 0 |
| epistemically_empty | 0 |
| none | 14 |
| uncertain | 1 |

**mechanism_death:** One measured CORE_INVALID (step input recorder) with DOES_NOT_SURVIVE. Differential diagnosis instead yields PARTIALLY_SURVIVES and reduced scope through a negative diagnostic constraint. The lone core is ambiguous under the operator source-specificity audit.

**generic_remainder:** No artifact has generic_remainder as its controlling failure reason. Crossdating primary/control B retain explicit ordered-overlap insufficiency. Generic docket/listing candidates are correctly rejected individually, so this does not establish a tendency to treat generic residue itself as viable.

**target_payoff_loss:** No artifact has target_payoff_loss as its controlling reason. Custody and pooled-flag positive results are individually disqualified for target relevance, but source-specific negative evidentiary constraints keep the artifacts. Control C did not isolate purely off-target residue.

**epistemically_empty:** No artifact has epistemically_empty as its controlling reason. This failure mode lacks a demonstrated clean example in the measured corpus.

**negative_evidentiary_constraints:** Five primary core hypotheses and controls B/C were false passes of the semantic authoring gate. The broad materiality definition permits useful evidentiary limits and next inquiries, which the audit omitted or prematurely called generic.

Operator categories: {"AMBIGUOUS": 1, "CASE_DESIGN_PROBLEM": 7, "PLAUSIBLE_ALTERNATIVE": 3, "STRUCTURALLY_CONCORDANT": 5}.
Case-design problems: 7; judge remainder errors: 0.
Review occurred after both provider stages were frozen. It addresses warrant, source specificity, materiality, exact target relevance, invented repair, overlooked remainders, procedure-volume reasoning and hidden-design mistakes for every case and pair. This is operator interpretation, not independent-rater evidence. [Complete audit](../remainder-viability-calibration-v0.1/review/operator.json).

- Seven intended nonviable primary/control cases retained defensible source-specific negative constraints. The premeasurement audit files remain unchanged; their passing flags were not reliable evidence that the semantic gate was truly satisfied. Had these remainders been recognized then, measurement should have stopped under the gate.
- Three intended reduced members retained their exact bounded target answers substantially intact. Their flags outcomes are plausible alternatives, exposing sensitivity to target narrowing and the distinction between advertised overclaims and material target scope.
- The single CORE_INVALID distinguishes generic absence-of-outcome reasoning from source-specific negative constraints in other cases. That distinction remains ambiguous rather than independently validated; no confirmed judge remainder error is asserted.
- All 100 assessed candidate warrant fields are YES. The corpus does not provide artifact-stage evidence for NO or UNCERTAIN warrant decisions after deletion.
- Primary signals differ in informative content and explicitly state missing relations. This is authored boundary calibration, not an isolated manipulation of one viability dimension or an estimate of natural-output performance.
- Measured delta deletion ratio is 1.28 after the judge rejected an extra assertion that all flag/F combinations occur; intended balance was below 1.06.
- Operator authoring and review share an author/context, and the controls overlap their primary constructions. Neither the audit nor candidate-level counts are independent-rater evidence.

The only CORE_INVALID also depends on an explicit distinction between the recorder channel and the target process. This is not a second comparison process, but remains a salient measurement-ownership cue; H.2 does not demonstrate a core boundary free of such cues.

## Research questions and interpretation

**1_small_viable_vs_none:** The tiny ACH control survives with reduced scope. The only measured no-viable case is step-response, whose source-specificity boundary remains ambiguous in review.

**2_activity_without_target_payoff:** Executable activity and source-derived recorder response coexist with measured CORE_INVALID in step-response; the broader generalization is not established.

**3_generic_vs_distinctive:** The judge distinguishes generic candidate residue from operational consequences, but no clean generic-only artifact reached the intended outcome because negative source-specific constraints survived.

**4_target_irrelevant_source:** Off-target custody/flag/recorder results are correctly disqualified as candidates. Control C remains viable through a separate target-relevant negative constraint, so an artifact-level target_payoff_loss route was not demonstrated.

**5_differential_mechanism_death:** Not demonstrated: the intended death case yields PARTIALLY_SURVIVES via the source-specific restriction on comparative updating and a necessary diagnostic inquiry.

**6_crossdating_generic_remainder:** Not demonstrated at artifact level: both primary core and control B retain an explicit ordered-overlap insufficiency result and yield DISTINCTIVE_REMAINDER.

**7_genuine_uncertainty:** Demonstrated in control D: the Q differential is warranted but its membership in the F-17 request path is unknown; no definite viable candidate is invented.

**8_four_properties_vs_volume:** The tiny control survives and long generic procedures are not counted as source-derived. Every status follows the four-field contract, but deterministic compliance alone is not independent evidence that source-specificity/materiality are calibrated.

**9_without_graph_labels:** Rationales address surviving evidence and target scope without intended graph-centrality labels. Exact intended reduced/core outcomes occur in zero of six pairs; viable/nonviable separation occurs mechanically in one, with operator ambiguity.

**10_dominant_limitation:** Case design remains the dominant limitation: seven nonviable hypotheses missed negative evidentiary contributions, compared with zero confirmed judge remainder errors and one ambiguous classification.

**boundary_operational:** Not yet demonstrated robustly. Outputs obey the four-part derivation, but zero of six pairs realize the intended reduced/core labels; only the step pair separates viable from nonviable, and its core source-specificity decision is ambiguous.

**absence_vs_centrality:** The measured CORE_INVALID is explicitly justified by absence of a four-YES remainder, not claim centrality. This is better aligned with the revised construct, but one ambiguous core observation cannot establish improved calibration or broad superiority over graph-based explanations.

**natural_output_readiness:** Not ready for a fresh natural-output admission experiment. First settle when a source-specific evidentiary-insufficiency result is itself a material remainder, and distinguish it operationally from generic lack-of-evidence commentary.

**Recommended next step:** Revise the authoring audit to require explicit negative-evidentiary candidates and useful stopping/inquiry rules for every proposed core. Clarify the source-specificity boundary for missing prerequisites using the step/diagnosis/crossdating contrasts, then author a small genuinely no-viable-remainder calibration before any new provider measurement. Do not impose a blanket ban on negative remainders. This recommendation is not executed.

The recommendation was not executed. No natural-output admission run, Experiment E continuation, production integration, historical experiment modification, or merge to main occurred.

## Unsupported claims

| Case | Claim | Deleted exact span |
|---|---|---|
| `H2-04edf722fb7e` | [C-60f57d1ce06e](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-60f57d1ce06e.json) | The recorded response proves that lock contention is certainly the sole cause of F-17, excluding every co-occurring or unlisted mechanism without further inquiry. |
| `H2-16df75b43727` | [C-21371384e61c](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-21371384e61c.json) | The continuous handling record proves that D-17 preserves its unchanged original authorial arrangement |
| `H2-16df75b43727` | [C-07cab0b63a85](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-07cab0b63a85.json) |  and settles the complete order of every textual revision. |
| `H2-25d1bd70c84a` | [C-0f5b1d8238f2](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-0f5b1d8238f2.json) | The reduction establishes that every nonzero exit is the defined failure F itself |
| `H2-25d1bd70c84a` | [C-c506f9362942](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-c506f9362942.json) |  and therefore that a and b are its unique underlying root cause. |
| `H2-25d1bd70c84a` | [C-b7a235da45b3](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-b7a235da45b3.json) | Thus both flag values occur with or without F. |
| `H2-53fc9c8368c3` | [C-694f1961c2e3](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-694f1961c2e3.json) | The observed correspondence fixes a unique global chronology for every position of S, aligning all its entries with the dated references without remaining alternatives. |
| `H2-545059f94c7b` | [C-176180efed9e](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-176180efed9e.json) | The observed correspondence fixes a unique global chronology for every position of S, including all entries outside the observed overlap, without remaining alternatives. |
| `H2-5c20feb8415d` | [C-a45c19ea3002](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-a45c19ea3002.json) | The recorded test establishes that lock contention is the sole cause of every occurrence of F-17 throughout the service, with no other contributing mechanism. |
| `H2-622904b211e7` | [C-64e99df1b2ff](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-64e99df1b2ff.json) | The repeated response establishes a two-hour reduction in end-to-end delay from the tested intake-priority change in P-17 at this operating point. |
| `H2-6f44184ce89e` | [C-462581c19962](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-462581c19962.json) | The comparative record establishes that steering is the best surviving explanation of award P-17, with an ordinary unsteered award ruled out. |
| `H2-72fb2477d1bc` | [C-2b576fdaf594](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-2b576fdaf594.json) | The recorded response proves that lock contention is certainly the sole cause of F-17, because the completed-test code exclusively identifies that mechanism. |
| `H2-89ae4468006c` | [C-45bb629dd3e3](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-45bb629dd3e3.json) | The comparison establishes that every score used for award P-17 was free of manipulation throughout the full evaluation. |
| `H2-89ae4468006c` | [C-0a792edc5b4f](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-0a792edc5b4f.json) | The comparison establishes that all specifications for award P-17 were drafted without bidder-specific influence. |
| `H2-89ae4468006c` | [C-64f103dd0465](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-64f103dd0465.json) | The comparison establishes that every private contact concerning award P-17 was lawful and unrelated to steering. |
| `H2-89ae4468006c` | [C-aee93cc575e5](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-aee93cc575e5.json) | The comparison establishes that all participants in award P-17 acted with impartial intent throughout the process. |
| `H2-945fda3cecc8` | [C-238ab7437d51](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-238ab7437d51.json) | The continuous handling record proves that D-17 preserves its unchanged original authorial arrangement |
| `H2-945fda3cecc8` | [C-4cec9201de5a](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-4cec9201de5a.json) |  and settles the complete order of every textual revision. |
| `H2-a814c5035bee` | [C-cdf63e360ab7](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-cdf63e360ab7.json) | The repeated response identifies intake scheduling as the unique internal cause of the measured end-to-end delay in P-17 at this operating point. |
| `H2-af1fe1a18f36` | [C-e1ff1ad780a6](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-e1ff1ad780a6.json) | The comparative record establishes that score alteration is the best surviving explanation of award P-17, with an ordinary unsteered award ruled out. |
| `H2-c5ce20f5d61c` | [C-142e6b89e8f3](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-142e6b89e8f3.json) | The observed correspondence fixes a unique global chronology for every position of S, aligning all its entries with the dated references without remaining alternatives. |
| `H2-de38329a6cac` | [C-47de9f37ca45](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-47de9f37ca45.json) | The reduction establishes that a and b are the unique underlying root cause of failure F in production |
| `H2-de38329a6cac` | [C-13f2f1545b56](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-13f2f1545b56.json) |  and excludes all alternative causal mechanisms. |
| `H2-eb081c18a2e8` | [C-07d2cd98255b](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-07d2cd98255b.json) | The continuous handling record proves that D-17 preserves its unchanged original authorial arrangement |
| `H2-eb081c18a2e8` | [C-47d8608fda71](../remainder-viability-calibration-v0.1/judgments/claim-warrant/C-47d8608fda71.json) |  and settles the complete order of every textual revision. |

## Measurement limitations

Exactly 73 observations in 73 fresh sessions used GPT-6 Astra/high, pinned Codex 0.157.1, disabled tools and isolated contexts. No harness retry, duplicate sample or review model was used. Served snapshots were unavailable (null), not inferred from aliases. Exposed internal retry events: 0; unexposed provider internals remain unknown.
Synthetic authoring, explicit observation semantics, one sample per case, operator-selected candidates and correlated paired/control examples limit generalization. Single-model concordance is not independent validation or an estimate of natural-output error prevalence.
