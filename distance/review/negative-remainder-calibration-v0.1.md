# Experiment H.3 — Productive Negative Remainder Calibration v0.1

H.3 closes automatic insufficiency rescue on this synthetic corpus and preserves productive constraints: 5 CORE_INVALID, 9 KEEP_WITH_REDUCED_SCOPE, and 1 KEEP_WITH_WARRANT_FLAGS. Full three-way negative-role calibration remains incomplete: two productive diagnostic directives were classified as nonnegative and omitted from role assessment.

## Lineage and preservation

Base: `e35948a601fefabb648218cde728aa7fdc1651d2`. Branch: `experiment-h3-negative-remainders`. Push only this branch; no merge to main.
The completion SHA is the commit containing publication-manifest.json, resolved by the command in metrics.json.

| Checkpoint | SHA |
|---|---|
| construct_checkpoint | `ebc9ea0b211a810c2585120ef6e9ed17b46824c1` |
| target_checkpoint | `24d5aee39feaab4de81bf6721b57361626917d79` |
| primary_checkpoint | `f4cf37ee1c930ba76ba3680f397dbba751bd442e` |
| controls_checkpoint | `dbabb95b9a28f7ef7a1923ff80f7762eb424f240` |
| claim_inventory_checkpoint | `0024840fde8265c1ed0330049d96b737c1e68b34` |
| claim_preflight_checkpoint | `86f92b00e415b6cd1468dcdef4b97ba5cb613f54` |
| claim_judgments_checkpoint | `b54093979cab1412543f854a5eff66f36bc7d74c` |
| ablations_and_candidates_checkpoint | `56df7ca00d4f841eb14fd1f197c48d765f94bf20` |
| artifact_preflight_checkpoint | `2c97108daae8bc27c78507a381bf937fae14cf53` |
| artifact_judgments_checkpoint | `862dbf1d0c164be130e54ea5224000b48f8fd28d` |
| operator_audit_checkpoint | `b24491b218b4ac50242b0c1668d970930a06eca7` |

Historical preservation: {'tracked': 3822, 'runtime': 9928}. Both measurement stages passed 49 historical checks and the H.3 test suite. Historical observations and files remain unchanged.

## Productive-negative rule and construction

**A negative remainder is productive only when it changes justified target states, bounds, alternative priorities, a stopping decision, or a specific discriminating next inquiry already present in surviving mapping content.** Merely acknowledging failure to establish an answer does not by itself supply viable remainder value.
Cannot conclude X does not mean X is excluded. Viability requires warranted, source-derived, target-relevant, productive, and material, assessed in that order. Graph centrality and ownership do not control status.
Four matched triplets cover ACH, dendrochronological crossdating, differential diagnosis and delta debugging. Source instruments, target, focal identity, baseline procedure and conditions are fixed within triplets. Observation content varies to license the intended consequence. The three controls manipulate wording or jargon while preserving a concrete semantic contrast.
Each focal consequence appears once. Authoring audits inspect all five mapping fields, removal effects, inquiry components, redundancy and other possible contributions. These are operator hypotheses, not independent truth. The inventory stage split coordinated delta root-cause assertions and the wording control into separate atomic claims; the earlier authoring audit counts refer to pre-extraction prose units.
Inquiry members contain an extra assertion. Text size and claim-count differences are disclosed below; no padding or numeric parity threshold was used.

| Case | Mechanism | Intended role/control | Claims | Mapping chars | Deleted chars |
|---|---|---|---:|---:|---:|
| `H3-0185f7ef5bd4` | delta | INSUFFICIENCY_ONLY / jargon | 3 | 1097 | 123 |
| `H3-29005a76cc33` | delta | INSUFFICIENCY_ONLY / primary | 3 | 1053 | 123 |
| `H3-4d30014ef73c` | diagnosis | INQUIRY_CONSTRAINT / primary | 3 | 1072 | 110 |
| `H3-5f1006224642` | ach | INQUIRY_CONSTRAINT / primary | 3 | 1150 | 131 |
| `H3-65c8b64e5dc2` | delta | INQUIRY_CONSTRAINT / primary | 4 | 1123 | 123 |
| `H3-692e955b9c15` | diagnosis | INSUFFICIENCY_ONLY / primary | 2 | 956 | 110 |
| `H3-8e37a4f3d05a` | diagnosis | TARGET_CONSTRAINT / primary | 2 | 968 | 110 |
| `H3-b57bdc93765e` | delta | TARGET_CONSTRAINT / primary | 3 | 944 | 123 |
| `H3-c7caa99e20ef` | crossdate | INSUFFICIENCY_ONLY / primary | 2 | 973 | 103 |
| `H3-d1569e3d7fbb` | crossdate | TARGET_CONSTRAINT / wording | 3 | 946 | 103 |
| `H3-d6134c9f4c74` | diagnosis | INQUIRY_CONSTRAINT / terse | 3 | 1048 | 110 |
| `H3-dbca10a933d7` | crossdate | INQUIRY_CONSTRAINT / primary | 3 | 1055 | 103 |
| `H3-e09eb242555a` | ach | INSUFFICIENCY_ONLY / primary | 2 | 1072 | 131 |
| `H3-ebcf45e8fdd8` | ach | TARGET_CONSTRAINT / primary | 2 | 1071 | 131 |
| `H3-ff52f4c34dbc` | crossdate | TARGET_CONSTRAINT / primary | 2 | 920 | 103 |

## Claim judgments and ablation

40 claim judgments: {"CONDITIONAL_WARRANT": 0, "SUPPORTED": 21, "UNCERTAIN": 0, "UNSUPPORTED": 19}.
All measured UNSUPPORTED spans were deleted simultaneously; conditional and uncertain claims remained. No subset search, semantic repair or replacement inference occurred. All 15 artifacts were measured under the user-selected empty-deletion policy.
Empty deletion cases: []. Unrealized intended deletions: []. These cases are excluded from ablation-effect conclusions.
Candidate inventories were frozen after claim results and before artifact calls. They cover surviving claims and an explicit all-field search for additional consequences. Judge-added candidates require exact surviving citations.

## Negative remainder and artifact results

All negative-candidate assessments (19): {"INQUIRY_CONSTRAINT": 3, "INSUFFICIENCY_ONLY": 11, "TARGET_CONSTRAINT": 5, "UNCERTAIN": 0}.
Productivity among those candidates: {"NO": 11, "UNCERTAIN": 0, "YES": 8}.
Focal assessments (13, separate denominator): {"INQUIRY_CONSTRAINT": 3, "INSUFFICIENCY_ONLY": 5, "TARGET_CONSTRAINT": 5, "UNCERTAIN": 0}; productivity {"NO": 5, "UNCERTAIN": 0, "YES": 8}.
Artifact statuses: {"CORE_INVALID": 5, "KEEP_WITH_REDUCED_SCOPE": 9, "KEEP_WITH_WARRANT_FLAGS": 1, "UNCERTAIN_LOAD_BEARING": 0}.

| Mechanism | Intended target member | Intended inquiry member | Intended insufficiency member |
|---|---|---|---|
| ach | H3-ebcf45e8fdd8: TARGET_CONSTRAINT/YES; KEEP_WITH_REDUCED_SCOPE | H3-5f1006224642: INQUIRY_CONSTRAINT/YES; KEEP_WITH_REDUCED_SCOPE | H3-e09eb242555a: INSUFFICIENCY_ONLY/NO; CORE_INVALID |
| crossdate | H3-ff52f4c34dbc: TARGET_CONSTRAINT/YES; KEEP_WITH_REDUCED_SCOPE | H3-dbca10a933d7: INQUIRY_CONSTRAINT/YES; KEEP_WITH_REDUCED_SCOPE | H3-c7caa99e20ef: INSUFFICIENCY_ONLY/NO; CORE_INVALID |
| diagnosis | H3-8e37a4f3d05a: TARGET_CONSTRAINT/YES; KEEP_WITH_WARRANT_FLAGS | H3-4d30014ef73c: No surviving focal assessment; KEEP_WITH_REDUCED_SCOPE | H3-692e955b9c15: INSUFFICIENCY_ONLY/NO; CORE_INVALID |
| delta | H3-b57bdc93765e: TARGET_CONSTRAINT/YES; KEEP_WITH_REDUCED_SCOPE | H3-65c8b64e5dc2: INQUIRY_CONSTRAINT/YES; KEEP_WITH_REDUCED_SCOPE | H3-29005a76cc33: INSUFFICIENCY_ONLY/NO; CORE_INVALID |

### Adversarial controls

- **jargon** (`H3-0185f7ef5bd4`): INSUFFICIENCY_ONLY/NO; CORE_INVALID.
- **wording** (`H3-d1569e3d7fbb`): TARGET_CONSTRAINT/YES; KEEP_WITH_REDUCED_SCOPE.
- **terse** (`H3-d6134c9f4c74`): ; KEEP_WITH_REDUCED_SCOPE.

### All CORE_INVALID

- `H3-0185f7ef5bd4` (delta, INSUFFICIENCY_ONLY): The ddmin complement ledger and single-removal exit-bit vector cannot establish target-F sufficiency: the binary channel pools handled deadlines, preflight configuration rejection and harness termination, with either bit value possible both with and without F.
- `H3-29005a76cc33` (delta, INSUFFICIENCY_ONLY): The observed nonzero-exit flag does not establish reproduction of F: either flag value can occur with or without F because handled deadlines, configuration rejection and harness termination share that result channel.
- `H3-692e955b9c15` (diagnosis, INSUFFICIENCY_ONLY): The current test does not determine which mechanism caused F-17: R denotes probe completion and carries no mechanism-dependent response value in the retained ledger.
- `H3-c7caa99e20ef` (crossdate, INSUFFICIENCY_ONLY): The available overlap does not establish a unique offset: the retained comparison gives no offset-specific mismatch or discriminating ordering among the six candidate alignments.
- `H3-e09eb242555a` (ach, INSUFFICIENCY_ONLY): The current matrix does not establish whether P-17 was steered: its retained X cells pool consistency, inconsistency and unrated entries, with the original values unavailable.

### All UNCERTAIN_LOAD_BEARING

None.

### Every assessed negative remainder

| Case / remainder | Role | Productive | Exact candidate | Counterfactual effects |
|---|---|---|---|---|
| H3-0185f7ef5bd4 / R01 | INSUFFICIENCY_ONLY | NO | The ddmin complement ledger and single-removal exit-bit vector cannot establish target-F sufficiency: the binary channel pools handled deadlines, preflight configuration rejection and harness termination, with either bit value possible both with and without F. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-29005a76cc33 / R01 | INSUFFICIENCY_ONLY | NO | The observed nonzero-exit flag does not establish reproduction of F: either flag value can occur with or without F because handled deadlines, configuration rejection and harness termination share that result channel. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-4d30014ef73c / R01 | INSUFFICIENCY_ONLY | NO | The current result does not discriminate lock contention from isolated pool exhaustion. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-5f1006224642 / R01 | INSUFFICIENCY_ONLY | NO | The retained comparison does not distinguish H1 from H3. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-5f1006224642 / R02 | INQUIRY_CONSTRAINT | YES | Inspect record R, the individual scores saved before consensus, next: unexplained post-opening score changes favor H1 over H3, whereas stable contemporaneous scores bear against H1 relative to H3. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "changed", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-65c8b64e5dc2 / R01 | INSUFFICIENCY_ONLY | NO | The current tests leave {a,b,c} and {a,c} unresolved as the required reproducing subset. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-65c8b64e5dc2 / R02 | INQUIRY_CONSTRAINT | YES | Replay {a,c} by removing b from {a,b,c} next under the frozen F oracle: persistence of F eliminates b from the required subset, while disappearance of F retains b as required in that configuration. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "changed", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-692e955b9c15 / R01 | INSUFFICIENCY_ONLY | NO | The current test does not determine which mechanism caused F-17: R denotes probe completion and carries no mechanism-dependent response value in the retained ledger. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-8e37a4f3d05a / R01 | TARGET_CONSTRAINT | YES | The recorded R is incompatible with isolated pool exhaustion under its stipulated diagnostic expectation, while R is compatible with lock contention at the same operating point. | {"alternative_priorities": "changed", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "changed", "target_state_set": "changed"} |
| H3-b57bdc93765e / R01 | TARGET_CONSTRAINT | YES | Under the frozen oracle that directly measures F, subset {a,b} does not reproduce F on the recorded replay. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "changed"} |
| H3-c7caa99e20ef / R01 | INSUFFICIENCY_ONLY | NO | The available overlap does not establish a unique offset: the retained comparison gives no offset-specific mismatch or discriminating ordering among the six candidate alignments. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-d1569e3d7fbb / R01 | INSUFFICIENCY_ONLY | NO | The anchored overlap is insufficient for a unique chronology | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-d1569e3d7fbb / R02 | TARGET_CONSTRAINT | YES | , but offsets +2 through +5 conflict with its ordered pattern; +6 and +7 remain compatible. | {"alternative_priorities": "unchanged", "bounds": "changed", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "changed"} |
| H3-d6134c9f4c74 / R01 | INSUFFICIENCY_ONLY | NO | The current result does not discriminate lock contention from isolated pool exhaustion. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-dbca10a933d7 / R01 | INSUFFICIENCY_ONLY | NO | The available overlap does not distinguish offsets +6 and +7. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-dbca10a933d7 / R02 | INQUIRY_CONSTRAINT | YES | Compare the next preserved increment with R2 next: +6 predicts a narrow-to-wide correspondence there and +7 predicts wide-to-narrow, so either observed correspondence bears against the other offset. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "changed", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-e09eb242555a / R01 | INSUFFICIENCY_ONLY | NO | The current matrix does not establish whether P-17 was steered: its retained X cells pool consistency, inconsistency and unrated entries, with the original values unavailable. | {"alternative_priorities": "unchanged", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-ebcf45e8fdd8 / R01 | TARGET_CONSTRAINT | YES | The authenticated comparison records an important inconsistency between E and H1, with E compatible with H2 and H3; this asymmetry persists when disputed entries are omitted. | {"alternative_priorities": "changed", "bounds": "unchanged", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "unchanged"} |
| H3-ff52f4c34dbc / R01 | TARGET_CONSTRAINT | YES | In the anchored overlap, offsets +2 through +5 conflict with the retained ordered pattern, while +6 and +7 remain compatible. | {"alternative_priorities": "unchanged", "bounds": "changed", "next_inquiry": "unchanged", "stopping_decision": "unchanged", "target_state_set": "changed"} |

### All inquiry constraints and discriminating next inquiries

- `H3-5f1006224642/R02`: **Inspect record R, the individual scores saved before consensus.**. Contrast: Whether H1 or H3 better explains P-17, which the retained comparison does not distinguish.. Outcomes: Unexplained post-opening score changes favor H1 over H3; stable contemporaneous scores bear against H1 relative to H3.. Surviving provenance present: True.
- `H3-65c8b64e5dc2/R02`: **Replay {a,c} by removing b from {a,b,c} next under the frozen F oracle.**. Contrast: {a,b,c} versus {a,c}, specifically whether b is required in that configuration.. Outcomes: Persistence of F eliminates b from the required subset, while disappearance of F retains b as required in that configuration.. Surviving provenance present: True.
- `H3-dbca10a933d7/R02`: **Compare the next preserved increment with independently dated reference R2.**. Contrast: The available overlap leaves +6 and +7 undistinguished.. Outcomes: A narrow-to-wide correspondence bears against +7; a wide-to-narrow correspondence bears against +6.. Surviving provenance present: True.

### All insufficiency-only remainders

- `H3-0185f7ef5bd4/R01`: The ddmin complement ledger and single-removal exit-bit vector cannot establish target-F sufficiency: the binary channel pools handled deadlines, preflight configuration rejection and harness termination, with either bit value possible both with and without F.
- `H3-29005a76cc33/R01`: The observed nonzero-exit flag does not establish reproduction of F: either flag value can occur with or without F because handled deadlines, configuration rejection and harness termination share that result channel.
- `H3-4d30014ef73c/R01`: The current result does not discriminate lock contention from isolated pool exhaustion.
- `H3-5f1006224642/R01`: The retained comparison does not distinguish H1 from H3.
- `H3-65c8b64e5dc2/R01`: The current tests leave {a,b,c} and {a,c} unresolved as the required reproducing subset.
- `H3-692e955b9c15/R01`: The current test does not determine which mechanism caused F-17: R denotes probe completion and carries no mechanism-dependent response value in the retained ledger.
- `H3-c7caa99e20ef/R01`: The available overlap does not establish a unique offset: the retained comparison gives no offset-specific mismatch or discriminating ordering among the six candidate alignments.
- `H3-d1569e3d7fbb/R01`: The anchored overlap is insufficient for a unique chronology
- `H3-d6134c9f4c74/R01`: The current result does not discriminate lock contention from isolated pool exhaustion.
- `H3-dbca10a933d7/R01`: The available overlap does not distinguish offsets +6 and +7.
- `H3-e09eb242555a/R01`: The current matrix does not establish whether P-17 was steered: its retained X cells pool consistency, inconsistency and unrated entries, with the original values unavailable.

## Post-freeze operator audit

Categories: {"CASE_DESIGN_PROBLEM": 2, "PLAUSIBLE_ALTERNATIVE": 1, "STRUCTURALLY_CONCORDANT": 12}. Case-design problems: 2; judge-productivity errors: 0.
The operator reviewed every case after all artifact judgments froze. This is not independent-rater evidence. Raw outputs and hidden hypotheses remain unchanged.

| Case | Category | Finding |
|---|---|---|
| `H3-0185f7ef5bd4` | STRUCTURALLY_CONCORDANT | Both flag values remain possible with and without F. This identifies no sufficient subset and supplies no selected replacement measurement or source-specific stopping decision. Detailed ddmin vocabulary does not alter the nonproductive judgment. |
| `H3-29005a76cc33` | STRUCTURALLY_CONCORDANT | Both flag values remain possible with and without F. This identifies no sufficient subset and supplies no selected replacement measurement or source-specific stopping decision. |
| `H3-4d30014ef73c` | CASE_DESIGN_PROBLEM | The paired waiting/occupancy observation and contrasting outcomes are supplied and productive. However, the affirmative directive was separated from its negative context and the added negative_inference flag allowed the judge to omit its role assessment. This is a case/instrument coverage problem, not a productivity error. |
| `H3-5f1006224642` | STRUCTURALLY_CONCORDANT | R01 is redundant insufficiency. R02 selects the pre-consensus score record and already supplies change-versus-stability outcomes for H1/H3; no outcome is asserted observed. |
| `H3-65c8b64e5dc2` | STRUCTURALLY_CONCORDANT | The next removal-of-b replay has an explicit persistence/disappearance interpretation. The judge correctly treats conditional elimination as inquiry selection, not as an already observed subset exclusion. |
| `H3-692e955b9c15` | STRUCTURALLY_CONCORDANT | Probe-completion R has no mechanism-dependent response value. Removing the insufficiency statement leaves both hypotheses live with the same priorities and no selected test. |
| `H3-8e37a4f3d05a` | PLAUSIBLE_ALTERNATIVE | Actual incompatibility with isolated pool exhaustion supports the target constraint. The judge additionally infers bounded branch termination and substantially intact target scope; this is a plausible consequence of stipulated incompatibility, rather than an invented next test. |
| `H3-b57bdc93765e` | STRUCTURALLY_CONCORDANT | A direct frozen-oracle observation excludes {a,b} as sufficient for F. Removing it restores that possibility; neither minimality nor a unique root cause follows. |
| `H3-c7caa99e20ef` | STRUCTURALLY_CONCORDANT | Lack of offset-specific mismatch or ordering leaves all six offsets live. Merely listing R2 and its next increment does not supply a discriminating outcome relation. |
| `H3-d1569e3d7fbb` | STRUCTURALLY_CONCORDANT | The sole anchored mismatch excludes +2 through +5 and leaves +6/+7 compatible. Removing that finding restores the six entry offsets and widens the bounds. The explicit insufficiency prefix is separately nonproductive; the exclusion clause remains productive, defeating an insufficiency-keyword shortcut. |
| `H3-d6134c9f4c74` | CASE_DESIGN_PROBLEM | The paired waiting/occupancy observation and contrasting outcomes are supplied and productive. However, the affirmative directive was separated from its negative context and the added negative_inference flag allowed the judge to omit its role assessment. This is a case/instrument coverage problem, not a productivity error. Terse wording still preserves the substantive inquiry, but the intended negative-role result was not elicited. |
| `H3-dbca10a933d7` | STRUCTURALLY_CONCORDANT | The named R2 comparison and opposing correspondences select a specific next inquiry. R01 alone adds no effect; no surviving result excludes the other four entry offsets. |
| `H3-e09eb242555a` | STRUCTURALLY_CONCORDANT | Erased X-cell ratings do not establish steering or exclude any hypothesis. The generic matrix procedure supplies no selected discriminating inquiry or stopping decision. |
| `H3-ebcf45e8fdd8` | STRUCTURALLY_CONCORDANT | E supplies the only authenticated asymmetry. Its removal restores H1's former standing; it neither eliminates H1 nor distinguishes H2 from H3. |
| `H3-ff52f4c34dbc` | STRUCTURALLY_CONCORDANT | The sole anchored mismatch excludes +2 through +5 and leaves +6/+7 compatible. Removing that finding restores the six entry offsets and widens the bounds. |

## Research questions

**1. Target constraints versus failure to conclude:** Yes in this corpus: five target constraints are productive YES; all eleven assessed insufficiency statements are productive NO. The four primary insufficiency artifacts and jargon control are CORE_INVALID.

**2. Specific inquiry versus generic more evidence:** All five supplied discriminating inquiries survive; generic baseline procedures and available records alone do not rescue the insufficiency cases. No dedicated collect-more-evidence sentence control was included, so that exact wording contrast remains unmeasured.

**3. Productive negative wording without a positive conclusion:** Yes. Offset exclusions, subset non-reproduction and comparative inconsistency remain productive without unique identification. The insufficiency-wording control preserves its exclusion while its insufficiency prefix is nonproductive.

**4. Source-specific language can be nonproductive:** Yes. The detailed ddmin exit-bit/complement jargon control is warranted, source-derived and relevant, but nonproductive and CORE_INVALID.

**5. Removing insufficiency leaves inquiry unchanged:** Yes for all eleven assessed insufficiency statements. This includes redundant non-discrimination statements in inquiry members, whose selected next operations survive independently.

**6. Target constraints narrow live states:** Crossdating and delta constraints exclude concrete candidates; ACH changes priorities without eliminating H1. Diagnostic incompatibility excludes the isolated-pool-exhaustion state within stipulated scope. The judge preserves these distinctions.

**7. Inquiry constraints change the next action:** Yes at the productivity level for all five inquiry members. ACH, delta and crossdating receive INQUIRY_CONSTRAINT. The diagnostic primary and terse control are productive affirmative directives but have no negative-role assessment; full four-mechanism role concordance was not achieved.

**8. Does productivity prevent automatic insufficiency rescue?:** Yes on this authored corpus: all five insufficiency-only artifacts are CORE_INVALID. There is no matched H.2-rule evaluation on the same H.3 stimuli, so this is boundary evidence rather than an isolated causal estimate of adding one field.

**9. CORE_INVALID without centrality or ownership shortcuts:** Yes in these five cases: the surviving warnings are explicitly warranted, source-derived and target-relevant, but fail productivity/materiality. No graph position, text amount or focal-ownership rule drives the decision.

**10. Case-design versus judge-productivity errors:** Two case/instrument role-coverage problems, one plausible diagnostic stopping/scope alternative, and no identified judge-productivity errors. The extra negative-inference eligibility flag and atomized affirmative directives explain the missing inquiry roles; outputs were not recoded.

## Interpretation, limitations and next step

**productivity_counts:** Across all 21 candidate remainders: YES=10, NO=11, UNCERTAIN=0. Across the 19 candidates classified as negative by the judge: YES=8, NO=11, UNCERTAIN=0. Their roles are TARGET_CONSTRAINT=5, INQUIRY_CONSTRAINT=3, INSUFFICIENCY_ONLY=11, UNCERTAIN=0. Two additional productive candidates have negative_inference=false and no role; they are not silently counted as UNCERTAIN.

**all_inquiry_contributions:** All five supplied inquiries were productive. Three received INQUIRY_CONSTRAINT; the diagnostic primary and terse control received no negative role. Complete cited records: [inquiry contributions](../negative-remainder-calibration-v0.1/review/inquiry-contributions.json).

| Case | Model role | Concrete next inquiry | Discriminating relation |
|---|---|---|---|
| `H3-4d30014ef73c/R02` | NONNEGATIVE — role absent | Measure lock-wait duration with pool occupancy next | elevated lock waits with normal occupancy favor lock contention, whereas ordinary lock waits with saturated occupancy favor pool exhaustion. |
| `H3-5f1006224642/R02` | INQUIRY_CONSTRAINT | Inspect record R, the individual scores saved before consensus, next | unexplained post-opening score changes favor H1 over H3, whereas stable contemporaneous scores bear against H1 relative to H3. |
| `H3-65c8b64e5dc2/R02` | INQUIRY_CONSTRAINT | Replay {a,c} by removing b from {a,b,c} next under the frozen F oracle | persistence of F eliminates b from the required subset, while disappearance of F retains b as required in that configuration. |
| `H3-d6134c9f4c74/R02` | NONNEGATIVE — role absent | Check waiting next, together with how full the pool is | long waits with spare capacity favor lock contention, whereas short waits with a full pool favor pool exhaustion. |
| `H3-dbca10a933d7/R02` | INQUIRY_CONSTRAINT | Compare the next preserved increment with R2 next | +6 predicts a narrow-to-wide correspondence there and +7 predicts wide-to-narrow, so either observed correspondence bears against the other offset. |


**loophole_closed:** The H.2 insufficiency-rescue loophole is closed for every authored insufficiency-only case here. This is a positive bounded result, not evidence that negative limitations are generally useless or that natural-output performance is established.

**productive_negative_constraints_preserved:** All five target constraints and all three model-labeled negative inquiry constraints survive. The other two supplied inquiries also survive productively, but the negative-role claim cannot be credited to them.

**absence_vs_centrality:** The five-property absence-of-viable-remainder definition yields CORE_INVALID across all four mechanisms without graph-centrality or ownership shortcuts.

**scope_alternative:** The diagnostic target member receives KEEP_WITH_WARRANT_FLAGS: the judge infers source-specific branch termination from stipulated incompatibility and treats comparative support plus that stopping decision as substantially intact target scope. This is a plausible interpretation, not a measured special-purpose stopping-condition calibration.

**protocol_coverage_gap:** The H.3 implementation added a negative_inference boolean to retain coverage of other possible viable contributions. Its frozen schema allowed even supplied negative candidates to be marked false and skip role assessment. This created a gap against the intended per-negative-candidate role coverage in the diagnostic primary and terse control. Their affirmation-style wording also exposed a candidate-unitization issue. This is retained as a design/instrument problem; it was not repaired after measurement.

**engineering_recovery:** Artifact 3 returned a schema-valid absent conflict with resolved=false. The inherited H.2 assertion rejected that inapplicable metadata bit even though H.3 status derivation ignores it. An additive adapter preserved every scientific byte, original failed validation, session, execution commit and terminal state; it removed only that assertion, passed 49 historical checks plus both local suites, and resumed the 12 never-reserved requests. The same harmless encoding also occurs in the delta target response. Evidence checkpoint 01443a5a9d65afc13b81e7bea6eed40d07507a65; recovery preflight a6489b19668f484cc4488934d43d2eb96fcb4949. No model output was normalized, resent or replaced. Use recovery.py verify for complete publication verification.

**natural_output_readiness:** Not ready for a fresh natural-output admission experiment. Productivity separation is promising, but mandatory role coverage and inquiry-unit boundaries should be resolved in a small follow-up first.

- Fifteen deliberately authored cases, one sample per claim/artifact, a single provider and correlated triplets; no prevalence or repeatability estimate.
- Warranted observations and diagnostic relations are explicitly stipulated; this tests the productivity boundary, not realistic acquisition or scientific truth of external evidence.
- Observation content necessarily differs between triplet members. Inquiry cases have an extra assertion, and atomic splitting changes some claim counts; this is not a wording-only randomized intervention.
- Two productive inquiry directives lack negative-role assessments because the schema permitted a nonnegative designation. Reported role counts cover 19 candidates, not all 21.
- Author and post-freeze reviewer are the same operator; there is no independent-rater validation.
- No dedicated uncertainty, stopping-condition, or literal generic-more-evidence control. Zero UNCERTAIN results do not validate uncertainty handling empirically.
- No same-corpus H.2-rule ablation was run, so causal attribution to the productivity field alone is not established.
- The metadata-validator recovery is disclosed and hash-bound; original failure and supplementary validation coexist. Served model snapshot identifiers were unavailable.

Exactly 55 observations in 55 distinct fresh sessions requested GPT-6 Astra/high. No harness retries or duplicate samples. Verified served snapshots: [None]; unavailable identifiers were not invented. Exposed internal retry events: 0.

**Recommended next step:** Run only a small follow-up on inquiry-remainder unitization and mandatory role coverage, using logically equivalent favor-versus-bear-against formulations and requiring a role for every supplied negative candidate. Resolve that gap before considering natural-output admission. This recommendation is not executed.

The recommendation was not executed. Work stopped after H.3; no Experiment E continuation, natural-output admission experiment, production integration, historical experiment changes or main merge occurred.
