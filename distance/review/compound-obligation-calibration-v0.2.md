# H6.R3 corrected compound-obligation calibration v0.2 — paused partial results

**H6.R3 is incomplete and paused after its third Stage C response failed frozen citation-role validation.** One of twelve controls is fully evaluated. No retry, substitution, response edit, validator relaxation or further provider dispatch occurred.

Base: `5b6dd0e63b280118a6473fa25b3295af376f7a3c`. Branch: `experiment-h6r3-compound-obligations`. H.6, H6.R1 and H6.R2 remain unchanged; H6.R2 remains terminated. Its observations and corrupted packets were not reused. This report closes the current execution attempt without declaring the calibration complete or introducing a new scientific terminal state.

## Observed separation and the stopping event

N1 produced the intended decomposition: GOVERNANCE_STRUCTURE **SATISFIED**, OPERATION_LICENSE **VIOLATED**, mechanical overall **VIOLATED**. The governance rationale evaluated trigger, response and coherence while explicitly excluding badge inspection's diagnostic usefulness. The operation judgment found badge colors independent of the delivery process. The failed secondary propagated correctly.

N2's governance response returned raw **SATISFIED**, but cited `R3K02-S` as CONTEXT where its frozen packet assigns SUPPORT. The frozen semantic validator rejected it with `Response cites unfrozen evidence/roles`. Transport, JSON schemas and fresh-session event checks passed; the executed request is byte-identical to its frozen request. The raw rationale also excludes diagnostic usefulness, but its verdict is not an accepted scientific observation.

This is one **response-side citation-role validation failure**, classified as `provider_measurement_failure`, not an input provenance-projection failure or a scientific-input lineage violation. [The incident impact analysis](../compound-obligation-calibration-v0.2/review/incidents/response-citation-role/impact.json) preserves hashes, role differences, original pause, request/response evidence and ledger checks. [The frozen protocol](../compound-obligation-calibration-v0.2/PROTOCOL.md) requires pause, preservation and reporting on schema/validation events, without retry or substitution; [the recovery policy](../../docs/EXPERIMENT-RECOVERY-POLICY.md) applies the stage's frozen rule. Remaining spending approval does not clear this stop.

## Frozen corrections and projection barrier

Every obligation froze its own subject, contract, source_id + role bundle and provenance hash. All 28 Stage C packets passed canonical reference equality, equal provenance hashes, resolved-source-text checks and rendered-request checks before the first evaluation. Fourteen obligation bundles differ from parent-claim bundles and retain those differences. Array order is explicitly semantically irrelevant; roles are material. All three executed requests preserve their frozen inputs. **No Stage C input citation role differed from its obligation; PROVENANCE_PROJECTION_FAILURE = 0.** The response-side change described above is recorded separately.

The new GOVERNANCE_STRUCTURE contract asks only whether a prospective rule has a determinate trigger, determinate response and internally coherent decision structure at its scope. Frozen packet instructions exclude scientific, causal, diagnostic, informational, mechanistic, empirical and target relevance of embedded content. The historical GOVERNANCE_COHERENCE contract is unchanged. Prohibited substantive reasoning would be flagged without changing a verdict.

Stage B froze origin, function, assertion mode, resolution and obligation-specific provenance before mechanical contract derivation. GROUNDING_REF merely invokes a supplied premise at unchanged scope/strength and creates no scientific call; CLAIM_REF reuses an existing evaluated claim; INLINE_OBLIGATION receives origin-sensitive contract(s). SOURCE_SUPPLIED + LIMIT remains independently representable, including P1's supplied limiting premise and the asserted-limit routing regression.

All 18 projection/routing tests passed, including opposite parent/child roles, fewer/additional child refs, changed role on the same ID, reordered IDs, multiple SUPPORT refs and mixed SUPPORT/CONTEXT. The actual P2 regression also passed, with no empirical secondary.

## All twelve control results

Stage A: 13/13 fresh judgments. Stage B: 13/13 fresh judgments. Stage C: 3/28 sessions attempted, 2 accepted, 1 rejected, 25 unlaunched. Twelve primary claims are GOVERNANCE_RULE; P3 C1 is INFERENCE. Stage D has only a partial mechanical aggregate: one measured claim and twelve incomplete claims across twelve cases. Missing observations have null overall, not a fabricated scientific verdict.

“Unmeasured” below means no accepted verdict. Contract names shown are the actual frozen obligation sets.

| Control | GOVERNANCE_STRUCTURE | Secondary judgments | Overall |
|---|---|---|---|
| N1 | SATISFIED | OPERATION_LICENSE: VIOLATED | VIOLATED |
| N2 | Unmeasured; raw SATISFIED rejected | OPERATION_LICENSE: unlaunched | INCOMPLETE |
| N3 | Unmeasured | TARGET_FIDELITY: unmeasured | INCOMPLETE |
| N4 | Unmeasured | DERIVED_WARRANT, TARGET_FIDELITY, SOURCE_FIDELITY: all unmeasured | INCOMPLETE |
| N5 | Unmeasured | FACT_WARRANT: unmeasured | INCOMPLETE |
| N6 | Unmeasured | SOURCE_FIDELITY, FACT_WARRANT: both unmeasured | INCOMPLETE |
| P1 | Unmeasured | SOURCE_FIDELITY, two distinct CONDITIONAL_LICENSE obligations: all unmeasured | INCOMPLETE |
| P2 | Unmeasured | None; four GROUNDING_REF records | INCOMPLETE |
| P3 | C2 unmeasured | C1 DERIVED_WARRANT: unmeasured; C2 CLAIM_REF C1 | INCOMPLETE |
| N7 | Unmeasured | SOURCE_FIDELITY: unmeasured | INCOMPLETE |
| N8 | Unmeasured | TARGET_FIDELITY, CONDITIONAL_LICENSE: both unmeasured | INCOMPLETE |
| U1 | Unmeasured | Unresolved operation; DEPENDENCY_UNCERTAIN | INCOMPLETE |

P2 remains lightweight in the frozen architecture: its agreed threshold is TARGET_SUPPLIED + FACT + REFERENCED_PREMISE, resolving GROUNDING_REF. Its only obligation is GOVERNANCE_STRUCTURE; no FACT_WARRANT, DERIVED_WARRANT or OPERATION_LICENSE was added. Its governance verdict is still unmeasured.

P3 plans exactly one DERIVED_WARRANT evaluation of C1, reused by C2 through CLAIM_REF. No duplicate scientific judgment occurred, but neither P3 evaluation ran, so successful completed reuse is not demonstrated. U1 preserves ORIGIN_UNCERTAIN + OPERATION + ASSERTED_COMPONENT with null resolution; no operation contract was invented and no clean satisfaction assigned. Its overall remains INCOMPLETE because even its base is unmeasured.

A scientific coverage gap was disclosed before Stage C approval: operation dependencies in N3, N4, N6, P1, N7 and N8 classified as supplied and therefore route to fidelity under the frozen rule. Only N1/N2 have OPERATION_LICENSE. N3's target supplies the workload-changing comparison; N8's target defines the badge-color test. Their operation defects cannot receive the expected license judgments. P1/N7 likewise lack the expected positive license contrasts. Discovery found those dependencies and formal routing complied; this gap is relative to preregistered scientific control intent. No classifications, contracts or hidden expectations were repaired post hoc.

## Diagnostics and operator audit

Counts are affected claims in available evidence, not complete-calibration rates. Zero observed failures does not establish absence in the unmeasured judgments.

| Diagnostic | Count / scope |
|---|---|
| PROVENANCE_PROJECTION_FAILURE | 0 across 28 packets and 3 executed requests |
| GOVERNANCE_BOUNDARY_LEAK | 0 in 1 accepted governance judgment; 11 lack accepted judgments |
| SUPPLIED_PREMISE_OVERTRIGGER | 0; P2 has no empirical obligation |
| GROUNDING_REF_MISCLASSIFICATION | 0 in 23 operator-reviewed grounding references |
| OBLIGATION_OMISSION | 6 operation-license coverage gaps relative to control intent |
| WRONG_SECONDARY_CONTRACT | 6, the same supplied-operation fidelity substitutions |
| GOVERNANCE_LAUNDERING | 0 observed; scientific measurement incomplete |
| OVERTRIGGER | 0 |
| DEPENDENCY_DUPLICATION | 0 |
| FAILURE_NONPROPAGATION | 0; N1 is the only complete empirical test |
| SHORT_CIRCUIT | 0; global validation pause, not verdict-based skipping |
| RECURSIVE_EXPLOSION | 0 |
| DEPENDENCY_CYCLE | 0 |
| DEPENDENCY_UNCERTAIN | 1, U1 |
| CLASSIFICATION_CONTRACT_FAILURE | 0 |

The rejected N2 raw governance rationale also shows no substantive boundary leak, but is excluded from accepted-verdict counts. N8's two planned secondaries were not run; neither dual-failure preservation nor the intended OPERATION_LICENSE contrast is demonstrated. All 23 grounding references were checked against supplied text at unchanged scope and strength. This finding does not erase the independent supplied-operation licensing gap.

[Partial metrics](../compound-obligation-calibration-v0.2/review/partial-metrics.json), [dependency audit](../compound-obligation-calibration-v0.2/review/partial-dependency-audit.json), [mechanical aggregation](../compound-obligation-calibration-v0.2/review/partial-aggregation.json) and [operator audit with all 14 research answers](../compound-obligation-calibration-v0.2/review/partial-operator-audit.json) are explicitly partial. No completed evaluation/aggregation freeze or full-calibration metrics is claimed.

## Provider, budget and recovery

29 fresh provider sessions ran: 13 Stage A + 13 Stage B + 3 Stage C. Requested model/reasoning were OpenAI GPT-6 Astra/high. Raw isolation/event records and available returned identifiers are preserved; unexposed served snapshots or internal retries are not asserted. There were no harness retries, model substitutions, capacity/transport failures or malformed input packets. One response failed the frozen semantic validator.

The user approved Stage C against cumulative plan-003, hash `fa90ccf4c800984e06712f820ba109cf9393b0abdc96b169d7418276ad3bc80c`, with 54 total planned sessions (13 + 13 + 28), unknown costs and UNKNOWN quota risk. The exact Stage C count came from fresh Stage B discovery. All 29 per-session reservations, including the rejected response, remain recorded. The gate reserved immediately before each launch. Fresh included-usage preflights accompanied bounded batches of at most three; the reserve remains 10 percentage points and no reset credits were consumed. The postpause financial check still allows the existing budget, while scientific scheduling remains blocked.

Eleven before/after usage observations, actual counts, profiles and available token totals remain private under ignored .runtime. They are excluded from clean calibration because account isolation and telemetry settling were not established; the last batch also includes the rejected response. No token-to-dollar or dollar-to-quota conversion was invented. No separate budget failure caused the scientific pause.

The original PAUSED_EVENT is preserved. The incident analysis confirms intact executed scientific inputs and reproduces the response-validator rejection. Accepting the response would change a frozen acceptance rule; no such recovery was performed. No new no-observation semantics or terminal precedence was established.

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
- stage_c_partial_observations_and_incident: `4eddd372fdf974555ec983f4539e7ea97d891cf1`

## Limitations and recommended next step

Exact provenance projection and lightweight P2 routing passed their planned checks. N1 demonstrates governance passing while an invalid operation fails, with correct failure propagation. N2–N6 do not establish the full intended separation; empirical-premise governance behavior, all positive outcomes, N7's structural contrast and N8's dual failure remain unmeasured. The supplied-operation routing gap independently prevents several requested exact contrasts even if all remaining packets were evaluated.

**The corrected architecture is not ready for a natural-claim negative-control test on this evidence.** Recommended next step: review the response-side citation-role acceptance rule and the supplied-operation licensing gap before any separately authorized recovery or future calibration. That recommendation has not been executed. H6.R3 remains paused; earlier experiments remain unchanged, and no natural admission, main-branch merge or broader policy formalization occurred.
