# H6.R2 — Claim origin/function + compound-obligation calibration v0.1

**TERMINATED_LINEAGE — calibration incomplete.** Stage A and Stage B completed. Stage C stopped after **21 of 27 evaluations**, with **47 total provider sessions**. The packet builder introduced a material citation-provenance projection defect: it dropped each inline obligation’s frozen provenance and reused whole-claim roles. P2’s evaluator explicitly rejected a target-supplied agreement because its supporting source had become CONTEXT. These scientific observations cannot be repaired or rerun under the existing authorization.

All original inputs, responses, failures and stop records are preserved. Six evaluations—N7 ×2, N8 ×3, U1 ×1—were never reserved or launched. There is no complete Stage C freeze or formal Stage D completion. The terminal budget block prevents automatic continuation.

Base: `c48f06aa32c03674a6c509ec5e631ce7a700b633`. Branch: `experiment-h6r2-compound-obligations`. H.6 and H6.R1 remain byte-identical to the required base; neither was resumed, relabeled or merged to main.

## Checkpoints

| Checkpoint | SHA |
|---|---|
| schema_contracts_compound_protocol | `d6b51fe3c8ec76128006ef56a4e348c6d1d073bb` |
| cases_hidden_hypotheses | `8afb2bee51ad84c8d9a62f14d490265ed8a3df61` |
| stage_a_packets_harness | `4ed69fcc2470a483d616d2592f54b8b40331aa44` |
| initial_cumulative_forecast | `fad51a865c1f5ba2fcc3f2040f9029a25e84528d` |
| stage_a_judgments | `84db08973af52a495f90361b71123ac4fe20f279` |
| stage_b_packets | `57349a3278df443b29237a31e65227ea2b97f574` |
| stage_b_forecast | `2be228f82c7de06829645fdb8a499c5e69747cac` |
| u1_recovery_evidence | `33f208193453d1e58e6828b92614388947252dcd` |
| u1_supplementary_validation | `18eec65cd92196a701b4e92162c06558d72e8ad9` |
| stage_b_judgments | `d7e0a7e7c4e508ed624817fa6c56fc340a5dacd5` |
| stage_c_packets | `acc2edbf7858cee01bb8f518744a85e80da6621e` |
| stage_c_forecast | `82a71128686de5a53a33c3c3c406b6886983294a` |
| stage_c_terminal_partial_freeze | `a9d508c6c38f3d7ad7c0c89c07383da5137d483e` |

Terminal partial-audit SHA: `0c33c89ba6cafbbd0e420984ba8c9f904f05dd13`.

The terminal-audit checkpoint is recorded in [checkpoints.json](../compound-obligation-calibration-v0.1/checkpoints.json). The final publication SHA is given in the completion message, avoiding a self-referential hash.

## Two-axis classification and corpus

Exactly twelve frozen synthetic cases contain thirteen claim records because P3 has a premise and a governance claim. The user confirmed primary-plus-subordinate atomicity, Stage B embedded-function assignment, and explicit contextual P3 reliance. All thirteen Stage A responses were ATOMIC and assigned on both independent axes.

| Dimension | Observed count |
|---|---|
| MAPPING_GENERATED | 13 |
| TARGET_SUPPLIED / SOURCE_SUPPLIED / BOTH_SUPPLIED | 0 / 0 / 0 |
| GOVERNANCE_RULE | 12 |
| INFERENCE | 1 |
| FACT / CONDITIONAL_RELATION / OPERATION / LIMIT | 0 / 0 / 0 / 0 |
| Origin/function uncertainty | 0 / 0 |

Observed combinations: **MAPPING_GENERATED + GOVERNANCE_RULE: 12**; **MAPPING_GENERATED + INFERENCE: 1** (P3 C1). The latter differs from the hidden operator FACT hypothesis and was preserved without rerouting. Primary function counts do not count embedded subjects as extra roles.

The schema and offline fixtures permit all 24 origin/function combinations, including SOURCE_SUPPLIED + LIMIT, TARGET_SUPPLIED + FACT, MAPPING_GENERATED + FACT, MAPPING_GENERATED + GOVERNANCE_RULE and MAPPING_GENERATED + OPERATION. SOURCE_SUPPLIED + LIMIT is representable without SOURCE_FACT/LIMIT role competition. That is structural evidence, not a measured source/limit reliability result. Citation SUPPORT/CONTEXT provenance remains a separate concept; the terminal defect demonstrates the importance of preserving it.

## Obligation discovery and evaluation coverage

Discovery froze **14 inline secondary obligations**, **one CLAIM_REF**, and **one unresolved material operation** (U1). Twelve claim sets have COMPLETE closure and U1 has DEPENDENCY_UNCERTAIN. All required secondary content in the frozen controls was represented; none was silently omitted. The semantic audit identifies one overtrigger: P2’s supplied agreement received an unnecessary FACT_WARRANT.

| Contract | Planned judgments | Preserved judgments |
|---|---:|---:|
| GOVERNANCE_COHERENCE | 12 | 9 |
| OPERATION_LICENSE | 8 | 6 |
| DERIVED_WARRANT | 2 | 2 |
| FACT_WARRANT | 3 | 3 |
| CONDITIONAL_LICENSE | 2 | 1 |
| TARGET_FIDELITY / SOURCE_FIDELITY / LIMIT_WARRANT | 0 | 0 |
| Total | 27 | 21 |

Each preserved contract response came from a fresh isolated Astra/high session. As-run verdicts are 14 VIOLATED and 7 SATISFIED. They are not a completed benchmark score. The partial mechanical replay contains 7 VIOLATED, 3 SATISFIED and 3 INCOMPLETE claim records (P3 contributes two records); missing observations are never fabricated. Nine of twelve cases have all their planned responses, but the Stage C lineage defect prevents claiming complete calibration validity.

## Exact control results

All entries below preserve **as-run** responses. V = VIOLATED; S = SATISFIED; — = never measured. The P2 aggregate is specifically invalid as a scientific conclusion, and the whole Stage C calibration is incomplete.

| Case | Primary governance | Secondary / premise results | As-run aggregate |
|---|---|---|---|
| N1 | V | OPERATION_LICENSE V | V |
| N2 | V | OPERATION_LICENSE V | V |
| N3 | V | OPERATION_LICENSE V | V |
| N4 | V | DERIVED_WARRANT V; OPERATION_LICENSE V | V |
| N5 | V | FACT_WARRANT V | V |
| N6 | V | OPERATION_LICENSE S; FACT_WARRANT V | V; lost mapping CONTEXT refs |
| P1 | S | OPERATION_LICENSE S; CONDITIONAL_LICENSE S | S |
| P2 | S | Unnecessary FACT_WARRANT V | V; demonstrated provenance contamination |
| P3 | C2 S | C1 DERIVED_WARRANT S; C2 CLAIM_REF C1 | C1 S; C2 S |
| N7 | — | OPERATION_LICENSE discovered; unmeasured | Incomplete |
| N8 | — | OPERATION_LICENSE and CONDITIONAL_LICENSE discovered; unmeasured | Incomplete |
| U1 | — | DEPENDENCY_UNCERTAIN; ambiguous operation retained | Incomplete |

**N1–N6:** every targeted secondary was discovered and returned VIOLATED, but all six governance judgments also returned VIOLATED. N1–N3 judges treated operational irrelevance or mechanism incompatibility as trigger/action incoherence. N4–N6 judges rejected the empirical premise within governance coherence as well. Therefore **zero of six** demonstrated the intended primary-SATISFIED/secondary-VIOLATED contrast. This is a control-design/contract-boundary limitation, not evidence that secondary contracts uniquely prevented laundering.

**P1:** all three contracts passed, preserving a valid compound claim. **P2:** governance passed, but discovery overtriggered on the supplied agreement. Its Stage B inline provenance named the target as SUPPORT; Stage C instead exposed the whole claim’s target CONTEXT role. The evaluator explicitly relied on that difference to reject the factual subject. The resulting false burden cannot be attributed purely to model strictness. **P3:** C1 was judged once; C2 reused its result through CLAIM_REF without a duplicate scientific call.

**N7/N8/U1:** required structures are present in discovery, but their evaluations were stopped before dispatch. No bad-governance/valid-operation result, designated dual-secondary-failure result, or final U1 claim verdict is claimed. Offline tests cover these mechanics; they are not substitutes for measured controls.

## Failure diagnostics

Counts are affected claims in the available discovery/as-run evaluation prefix. Zero does not imply a completed-suite success. Detailed events and semantic rationales are in [metrics.json](../compound-obligation-calibration-v0.1/metrics.json) and the dependency audit.

| Diagnostic | Observed count |
|---|---:|
| OBLIGATION_OMISSION | 0 |
| GOVERNANCE_LAUNDERING | 0 |
| OVERTRIGGER | 1 |
| WRONG_SECONDARY_CONTRACT | 0 |
| DEPENDENCY_DUPLICATION | 0 |
| FAILURE_NONPROPAGATION | 0 |
| SHORT_CIRCUIT | 0 |
| RECURSIVE_EXPLOSION | 0 |
| DEPENDENCY_CYCLE | 0 |
| DEPENDENCY_UNCERTAIN | 1 |
| CLASSIFICATION_CONTRACT_FAILURE | 0 |

No GOVERNANCE_LAUNDERING pattern was observed in the measured prefix; no required discovery obligation was omitted. Failure propagation works in the mechanical replay, including propagation of the unchanged contaminated P2 verdict. The six missing judgments followed an integrity stop, not a first-failure shortcut. N4 preserved both secondary failures. P3 has zero duplicate scientific judgments. All dependencies remain direct and acyclic. U1 uncertainty is explicitly retained. No supplied-origin fidelity contract was measured, so CLASSIFICATION_CONTRACT_FAILURE=0 has no positive calibration significance. WRONG_SECONDARY_CONTRACT=0 reports no mismatch against the frozen embedded function routing; the unnecessary P2 contract and corrupted evidence are separately identified.

An additional material harness diagnostic is **PROVENANCE_PROJECTION_FAILURE**: all inline jobs lacked a dedicated obligation-provenance field; three executed packets had explicit citation-role/list differences (two N6 packets and P2). P2 demonstrates substantive effect. N6 lost mapping CONTEXT citations while retaining the text. No counterfactual corrected verdict is inferred.

## Integrity incidents, budget and verification

**Recoverable U1 metadata incident:** the provider returned a schema-valid DEPENDENCY_UNCERTAIN record with companion D1 metadata linked to an explicitly named unresolved dependency. A local assertion recognized only resolved dependencies and rejected it. The original response, failure and pause were preserved; ten tests established a hash-bound supplementary validation without changing any scientific field, provider input, process/session identity or other response. Zero repeat calls occurred. [Recovery evidence](../compound-obligation-calibration-v0.1/review/recovery/unresolved-metadata/README.md).

**Terminal Stage C input incident:** the packet builder dropped inline-obligation provenance and reused the parent claim’s roles. This was introduced before Stage C freezing: executed requests exactly match their frozen packets, so it is not post-freeze byte tampering. The projection between scientific stages is wrong. P2’s response demonstrates that this affects measurement; positive non-contamination cannot be established. The experiment is TERMINATED_LINEAGE, with the shared ledger blocked. Inputs and observations were neither corrected nor repeated. [Impact audit](../compound-obligation-calibration-v0.1/review/incidents/provenance-projection/impact.json).

The user’s explicit completion approval followed the displayed initial UNKNOWN-cost/UNKNOWN-allowance plan. Cumulative plans were displayed, committed and recorded against that authority as frozen stages advanced: 13+13+unknown, then 13+13+27=53. Actual consumption is **47 reserved/completed provider sessions**: 13 classification, 13 discovery, 21 evaluation. All reservations preceded their launches; six planned evaluations remain unreserved. No provider transport/capacity event, observed substitution, duplicate sampling, harness retry, reset redemption or automatic top-up action occurred. Billed dollar cost remains UNKNOWN.

Every one of 17 bounded batches has fresh preflight, before/after allowance snapshots, actual session counts and available token records. Samples remain excluded from clean calibration because interactive account usage and telemetry settling were not independently isolated; the initially failed U1 bookkeeping also retains its original incomplete-attribution exclusion. No percentage-per-session rate or exhaustion probability was invented. Account data and the ledger remain under ignored .runtime/. The 10-percentage-point reserve was unchanged.

Offline engineering checks: 55 H6.R2 tests, 18 shared financial tests, 18 shared usage tests, and 10 recovery tests. Passing engineering tests did not prevent the scientific packet-projection defect. The terminal evidence verifier checks historical preservation, all 47 original sessions/reservations, packet reconstruction, stage barriers, immutable responses, the six unlaunched requests and the permanent block. Its preservation PASS is not a scientific calibration PASS. Requested model was gpt-6-astra/high throughout; a verified served snapshot and provider-internal retry behavior remain unobservable.

## Research questions

1. **Does separating origin from function eliminate SOURCE_FACT/LIMIT competition?** Structurally yes: SOURCE_SUPPLIED + LIMIT is valid and routes to SOURCE_FIDELITY in the offline fixtures. No measured primary claim had that combination, so empirical assignability for source-supplied limits remains untested.

2. **Can generated FACT claims receive warrant without becoming supplied facts?** The schema routes MAPPING_GENERATED + FACT to FACT_WARRANT, and embedded FACT assertions in N5/N6 were evaluated and rejected without reclassifying the primary claims. No primary generated FACT was measured: P3 C1 was classified INFERENCE. P2 shows why obligation-specific citation provenance must also be preserved; its extra FACT evaluation is contaminated.

3. **Can governance rules carry embedded operation obligations?** Yes at discovery: eight OPERATION_LICENSE obligations were frozen beneath governance claims. Six were evaluated before the stop; two were not.

4. **Can governance rules carry embedded empirical-premise obligations?** Yes: N4 carries DERIVED_WARRANT, N5/N6 carry FACT_WARRANT, and the three assertions were rejected as run. P2 also received an unnecessary factual obligation.

5. **Are invalid embedded operations rejected even when governance is coherent?** Not established in the intended contrast. N1–N3 operation verdicts were VIOLATED, but all three governance verdicts were also VIOLATED. The missing primary-SATISFIED/secondary-VIOLATED contrast cannot be repaired by reinterpreting those governance judgments.

6. **Are unsupported embedded premises rejected even when governance is coherent?** Not established in that contrast. N4–N6 empirical obligations were VIOLATED as run, but their governance judgments also failed. P2 has governance SATISFIED plus an extra FACT VIOLATED, but that is an overtrigger and a demonstrated provenance-projection defect, not a valid negative control.

7. **Do those failures propagate to the overall claim?** The as-run mechanical replay propagates all observed failures in fully evaluated claims. It intentionally propagates P2’s original corrupted judgment too, while labeling that aggregate invalid as a scientific conclusion. Six missing judgments remain missing. This verifies arithmetic, not a successful complete calibration.

8. **Does pure normative governance avoid unnecessary secondary obligations?** No. P2 received FACT_WARRANT for the already supplied agreement, contrary to the pure-normative control. OVERTRIGGER is 1. The later evidence-role mismatch falsely burdened that added obligation further.

9. **Does CLAIM_REF prevent duplicate evaluation?** Yes for the measured P3: C1 has one DERIVED_WARRANT judgment; C2 has one GOVERNANCE_COHERENCE judgment and a CLAIM_REF to C1. No second scientific judgment of C1 was launched.

10. **Can good operations coexist with bad governance without rescuing the claim?** N7 was discovered with separate governance and one-operation obligations, but neither evaluation launched. N6 incidentally has OPERATION_LICENSE SATISFIED and governance VIOLATED as run, with overall VIOLATED; its two inline packets also lost a mapping CONTEXT citation. The designated N7 control remains unmeasured.

11. **Are multiple simultaneous secondary failures all preserved?** N8 has both required secondary obligations, but its three evaluations were never launched. N4 retains two secondary VIOLATED judgments, demonstrating no short-circuit in the observed prefix. N8’s designated operation/conditional dual-failure check remains unmeasured.

12. **Does dependency uncertainty prevent silent acceptance?** U1 explicitly froze DEPENDENCY_UNCERTAIN. The unchanged response was preserved by metadata-only engineering recovery. No U1 contract judgment launched, so there is no final measured verdict. Offline propagation tests prove uncertain closure cannot produce SATISFIED, including when governance is supplied as SATISFIED in a fixture.

13. **Does obligation discovery remain one-level rather than recursively exploding?** Yes in all thirteen discovery records: resolved obligations are direct; P3 reuses a frozen claim; U1 remains unresolved. No nested obligation discovery or cycle was observed.

14. **Does this architecture preserve strictness better than H6.R1?** It exposes direct operation/empirical obligations that H6.R1 could omit, and the observed negative prefix rejects invalid content. A superiority claim is not warranted: P2 overtriggers, all N1–N6 governance judgments also fail, and Stage C was terminated for a material evidence-projection defect. The architecture is not calibrated for a natural-claim negative-control follow-on as-is.

## Recommendation and limits

Do not proceed directly to natural-claim calibration. In a separately authorized prospective effort, correct and test obligation-specific evidence-role projection, clarify pure-normative overtrigger and governance/secondary boundaries, then preregister a fresh bounded calibration without repairing these observations.

Purposive synthetic controls, one sample per item and no independent adjudicator limit any generalization. The terminal input defect, incomplete structural controls, primary governance failures across N1–N6, and P2 overtrigger preclude a claim that H6.R2 is strict enough to proceed directly to natural-claim calibration. No historical H.6 conclusion is revised.

The recommendation was not executed. Work stops at this preserved H6.R2 terminal checkpoint; no H.6 resumption, natural-output admission, ablation, terminal-state precedence fix, provider no-observation formalization, or main merge occurred.
