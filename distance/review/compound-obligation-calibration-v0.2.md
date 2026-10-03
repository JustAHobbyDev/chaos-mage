# H6.R3 corrected compound-obligation calibration v0.2 — Stage C approval checkpoint

**Incomplete calibration: Stage A and Stage B are complete; all Stage C packets and mandatory preflights are frozen and pass. No Stage C provider session has run.**

Base: `5b6dd0e63b280118a6473fa25b3295af376f7a3c`. Branch: `experiment-h6r3-compound-obligations`. H.6, H6.R1 and H6.R2 remain unchanged. H6.R2 stays terminated; none of its provider observations or corrupted packets is reused.

## Main findings before evaluation

Exact obligation-provenance projection passes for all 28 scientific packets with zero mismatches. Each packet's source_id + role pairs and provenance hash equal its own frozen obligation; resolved source text and rendered requests also match frozen construction. Array order is explicitly irrelevant; roles never are. Parent-versus-obligation citation differences are preserved, never inherited away. All 18 projection/routing regression tests pass.

The actual P2 dependency result is TARGET_SUPPLIED + FACT + REFERENCED_PREMISE for its agreed threshold and resolves GROUNDING_REF. All four P2 dependencies are grounding references. Its only scientific obligation is GOVERNANCE_STRUCTURE, with zero FACT_WARRANT, DERIVED_WARRANT or OPERATION_LICENSE secondaries. The actual P2 preflight passes.

P3's C1 classified INFERENCE and has one planned DERIVED_WARRANT evaluation. C2 uses CLAIM_REF to C1, with no duplicate scientific call. U1 retains an unresolved operation (ORIGIN_UNCERTAIN + OPERATION + ASSERTED_COMPONENT, null resolution) and DEPENDENCY_UNCERTAIN. It receives no guessed operation contract and cannot aggregate to clean SATISFIED.

**A separate scientific routing gap is already visible.** The discovered operation components of N3, N4, N6, P1, N7 and N8 are supplied-origin asserted components and mechanically route to fidelity. The target explicitly supplies N3's proposed workload-changing comparison; N8's target defines its badge-color test. The frozen origin-sensitive rule therefore does not ask whether those supplied operations are licensed. N3/N8's operation-validity defects are not measured by OPERATION_LICENSE, and P1/N7's expected valid-operation license contrasts are absent. This is not a packet projection defect. Original classifications, hidden hypotheses and derived contracts remain unchanged. Stage C can still measure governance and other secondary judgments, but the exact requested decomposition cannot all be observed from this obligation set.

## Frozen architecture

CORRECTIONS.md, CONTRACTS.md and taxonomy.json preserve the exact new GOVERNANCE_STRUCTURE question and mandatory boundary wording. The historical GOVERNANCE_COHERENCE contract remains untouched. Any prohibited substantive governance reasoning must be preserved and flagged rather than reinterpreted.

Stage B classifies origin, function, assertion mode and resolution without selecting contracts. Only after all Stage B responses froze were contracts derived mechanically. Every base and inline obligation then froze its own provenance refs/hash. GROUNDING_REF creates no new judgment; CLAIM_REF reuses an existing claim; INLINE_OBLIGATION receives its origin-sensitive contract(s).

## Stage status and all twelve controls

13/13 Stage A and 13/13 Stage B judgments completed in fresh isolated Astra/high contexts. All primary claims are ATOMIC and MAPPING_GENERATED. Twelve primary functions are GOVERNANCE_RULE; P3 C1 is INFERENCE. Stage C is 0/28 and Stage D has not run. No scientific overall or governance/secondary validity verdict is yet available.

| Control | Frozen base contracts | Frozen scientific secondaries | Dependency state |
|---|---|---|---|
| N1 | GOVERNANCE_STRUCTURE | OPERATION_LICENSE | COMPLETE |
| N2 | GOVERNANCE_STRUCTURE | OPERATION_LICENSE | COMPLETE |
| N3 | GOVERNANCE_STRUCTURE | TARGET_FIDELITY | COMPLETE |
| N4 | GOVERNANCE_STRUCTURE | DERIVED_WARRANT, TARGET_FIDELITY, SOURCE_FIDELITY | COMPLETE |
| N5 | GOVERNANCE_STRUCTURE | FACT_WARRANT | COMPLETE |
| N6 | GOVERNANCE_STRUCTURE | SOURCE_FIDELITY, FACT_WARRANT | COMPLETE |
| P1 | GOVERNANCE_STRUCTURE | SOURCE_FIDELITY, CONDITIONAL_LICENSE, CONDITIONAL_LICENSE | COMPLETE |
| P2 | GOVERNANCE_STRUCTURE | None | COMPLETE |
| P3 C1 | DERIVED_WARRANT | None | COMPLETE |
| P3 C2 | GOVERNANCE_STRUCTURE | None | CLAIM_REF C1 |
| N7 | GOVERNANCE_STRUCTURE | SOURCE_FIDELITY | COMPLETE |
| N8 | GOVERNANCE_STRUCTURE | TARGET_FIDELITY, CONDITIONAL_LICENSE | COMPLETE |
| U1 | GOVERNANCE_STRUCTURE | None | DEPENDENCY_UNCERTAIN |

N1–N6 governance verdicts, secondary verdicts and overall verdicts are all unmeasured. N4 repair has both fidelity contracts. N6's empirical reversibility assertion still has FACT_WARRANT despite its deployment procedure receiving SOURCE_FIDELITY. P1 has two distinct CONDITIONAL_LICENSE obligations (R1 and R2) in addition to source fidelity. N8's two discovered secondary judgments are both planned without short-circuit, but one is TARGET_FIDELITY rather than the hypothesized OPERATION_LICENSE.

The 28 evaluations comprise 12 GOVERNANCE_STRUCTURE, 2 OPERATION_LICENSE, 3 TARGET_FIDELITY, 4 SOURCE_FIDELITY, 2 DERIVED_WARRANT, 2 FACT_WARRANT and 3 CONDITIONAL_LICENSE judgments. Discovery retained 14 inline dependencies (one both-supplied component creates two fidelity obligations), 23 grounding references, one claim reference and one unresolved dependency. SOURCE_SUPPLIED + LIMIT is structurally represented, including a P1 grounding dependency; the schema/routing regression also covers source fidelity for an asserted supplied limit.

## Diagnostics and limitations

PROVENANCE_PROJECTION_FAILURE: 0 in the complete Stage C preflight. No Stage C citation role differs from its frozen obligation. Intentional failing test fixtures are not experiment incidents.

SUPPLIED_PREMISE_OVERTRIGGER: P2 has zero unnecessary empirical obligations. Every discovered REFERENCED_PREMISE resolves grounding/reference or remains unresolved, rather than an inline generated warrant. Full semantic operator audit is still pending.

GOVERNANCE_BOUNDARY_LEAK: not yet measurable because Stage C has not run. GROUNDING_REF_MISCLASSIFICATION: semantic audit pending; no false zero is inferred from schema validation. DEPENDENCY_UNCERTAIN: one preserved validation diagnostic, U1. No provider/schema execution failure occurred.

All original diagnostics remain in scope: OBLIGATION_OMISSION, GOVERNANCE_LAUNDERING, OVERTRIGGER, WRONG_SECONDARY_CONTRACT, DEPENDENCY_DUPLICATION, FAILURE_NONPROPAGATION, SHORT_CIRCUIT, RECURSIVE_EXPLOSION, DEPENDENCY_CYCLE, DEPENDENCY_UNCERTAIN and CLASSIFICATION_CONTRACT_FAILURE. The operator audit must assess the supplied-operation coverage gaps against the original control intents, even though formal origin routing is mechanically correct. Failure propagation tests pass; actual scientific propagation is unmeasured. No completed-calibration diagnostic rates or aggregate accuracy are claimed.

## Provider, budget and recovery

26 provider sessions total (13 classification + 13 dependency); no retries, substitutions, capacity/transport incidents or scientific recovery events. Requested model/reasoning are frozen Astra/high. Returned model identifiers and isolation/event evidence are retained; unexposed provider internals or served snapshots are not invented assurances.

Ten bounded batches have before/after allowance, actual session counts, usage profiles and available token records preserved under ignored .runtime. They are excluded from clean quota calibration because account isolation and telemetry settling were not established. Stage B provider-reported totals: 158,457 input, 15,872 cached input, 20,351 output and 7,756 separately reported reasoning-output tokens. These are not dollar or quota estimates. No reset credits were used.

Cumulative plan-003 retains all 26 prior reservations and adds 28 evaluations, for 54 total sessions. All stage costs remain unknown. Exact plan hash: `fa90ccf4c800984e06712f820ba109cf9393b0abdc96b169d7418276ad3bc80c`. Financial and fresh included-usage preflights require explicit approval. Predicted points/share of remaining allowance are UNKNOWN without comparable evaluation calibration; reserve stays 10 points. Account values remain private under .runtime.

## Checkpoint SHAs

- base: `5b6dd0e63b280118a6473fa25b3295af376f7a3c`
- corrections_contracts_schema_harness: `6efed356e2c4d3d4496f7ef997875f48de7c1c5a`
- controls: `59e99dd59840131ddc96687f46bba7bc6a8b3f17`
- stage_a_packets: `e6a220e7c9814345511ef59d230c76d4efe3d5cf`
- cumulative_budget_plan: `af2423300591ba48bb069581bd52c88969f6688c`
- first_three_stage_a_observations: `aa9d5a6c31c3bbf54409fe5c6622f0fbd7f16ce5`
- stage_a_judgments: `7b532b4010e4433600e31960c4b5413e7ef3e732`
- stage_b_packets: `c0032a8ff9e968325574d4a12a8f250c55f821f4`
- stage_b_cumulative_budget: `c8da6d985da14ed8a3d212ad815ba1eb1bc0a2f6`
- stage_b_judgments: `b096c8430f02fc4ff7bd2ad030b6cf6826659880`
- obligation_sets: `85d12dac9a43d4d4523858b8e4b20018e8d7ed2e`
- stage_c_packets_projection_p2: `5af373474af268b96f976395a80e5bf3f91ad9a4`
- stage_c_exact_budget: `d99d0c029b1b2153a26eb8c6f389b17c4271ac65`

## Research status and next step

The deterministic provenance correction, P2's lightweight routing, P3 reference reuse and explicit U1 closure have passed their relevant premeasurement checks. Questions about governance-boundary behavior, observed strict-negative decompositions and failure propagation still need Stage C. The source/target-supplied operation gap already prevents all specified exact contrasts. The architecture is not ready for a natural-claim negative-control test on current evidence.

Recommended next step: review this gap together with the exact 28-session Stage C forecast and decide whether to authorize measurement of the unchanged frozen obligation set. Such measurement can assess the governance boundary and remaining secondaries; it cannot repair the missing operation-license contrasts. No recommendation has been executed. Do not add obligations post hoc, resume earlier experiments, perform natural admission, settle provider no-observation semantics, or merge to main.
