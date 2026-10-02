# H6.R1 claim-role taxonomy calibration v0.1

Completed: 24 prospective role assignments and 19 routed evaluations. The taxonomy corrected four clear contract mismatches and retained two role-specific failures. It did **not** demonstrate preserved rejection of unsupported derived inferences, source-fact routing, or operational scrutiny of the mandatory fallback cases. The result is partial calibration with material boundary and coverage gaps, not a warrant-stage recovery success.

Base: `3af1d99cdd0c23ebf456f2223f60b0512a71757e`. Branch: `experiment-h6r1-claim-taxonomy`. H.6 remains unchanged at scientific terminal `84ad66c6a7150e02f31201c16a4d90f54d1a56ba`. No H.6 judgment was repaired or reinterpreted as a new H.6 result.

## Frozen checkpoints

| Checkpoint | SHA |
|---|---|
| schema_contracts | `2351032242a701f3e3fb8c6dff390b6762ba324e` |
| selection_hypotheses | `d80b05fe0891a95da5f11c9232d426301ab7c6c2` |
| stage_a_packets_runner | `9a35e66ab8a476dd7f8909425e74caaa375c7758` |
| cumulative_forecast | `6389a38776737693d4b5a62ee0a756ac32274494` |
| stage_a_judgments | `fc3240d5b8c6fea9cf8c013362b7555c728a3a1f` |
| stage_b_packets | `56a9fa2ac46ce656b1b281e8573297198bb83fdc` |
| Corrected cumulative Stage B forecast | `3423aa5eb1393cbf54e0efe34ac066a70e60e524` |
| Stage B judgments | `8fb24e8899f3668ef781dc6830645f547f16060d` |
| Historical comparison | `bdcd3309e8c0390135631c2b1ab442ffca908573` |

The subsequent audit-freeze and publication SHAs are recorded in [checkpoints.json](../claim-role-taxonomy-v0.1/checkpoints.json), avoiding a self-referential report hash.

## Corpus and assignment

All eleven mandatory anchors were included. The bounded corpus uses 24 original H.6 claims, with no synthetic replacements or postmeasurement reselection. Content-only selection added plausible inference and operation controls and a mixed-function claim; historical labels were unavailable to selection except the mandated anchor identities. Two source-restatement candidates were retained without forcing a third. This does not establish that all H.6 lacks clean source facts.

| Intended role | Count |
|---|---|
| SUPPLIED_FACT | 3 |
| SOURCE_FACT | 2 |
| DERIVED_INFERENCE | 5 |
| CONDITIONAL_RELATION | 2 |
| OPERATION | 7 |
| GOVERNANCE_RULE | 2 |
| LIMIT | 2 |
| SPLIT_REQUIRED | 1 |

Stage A: 19 ASSIGNED (79.2%), 4 ROLE_UNCERTAIN (16.7%), 1 ATOMIZATION_DEFECT (4.2%). Atomicity concordance was 24/24. Role concordance with hidden operator hypotheses was 15/19 among assigned cases with paired hypotheses; 15/24 across all selected claims. Operator hypotheses are not independently established ground truth. Single judgments provide no stability or repeatability estimate.

Uncertain: T01-2/C055 and T02-2/C075 (SOURCE_FACT/LIMIT), T01-3/C033 (DERIVED_INFERENCE/GOVERNANCE_RULE), T02-1/C040 (CONDITIONAL_RELATION/OPERATION/GOVERNANCE_RULE). T02-2/C008 combines a coexistence limitation with a comparison instruction and was recorded as an atomization defect without splitting. None of these five entered Stage B.

## Routed results

| Role | Contract | Assigned | SATISFIED | CONDITIONAL | VIOLATED | UNCERTAIN |
|---|---|---:|---:|---:|---:|---:|
| SUPPLIED_FACT | TARGET_FIDELITY | 3 | 3 | 0 | 0 | 0 |
| SOURCE_FACT | SOURCE_FIDELITY | 0 | 0 | 0 | 0 | 0 |
| DERIVED_INFERENCE | DERIVED_WARRANT | 4 | 3 | 1 | 0 | 0 |
| CONDITIONAL_RELATION | CONDITIONAL_LICENSE | 2 | 2 | 0 | 0 | 0 |
| OPERATION | OPERATION_LICENSE | 2 | 2 | 0 | 0 | 0 |
| GOVERNANCE_RULE | GOVERNANCE_COHERENCE | 6 | 5 | 0 | 1 | 0 |
| LIMIT | LIMIT_WARRANT | 2 | 1 | 0 | 1 | 0 |

**Totals: 16 SATISFIED, 1 CONDITIONAL, 2 VIOLATED, 0 UNCERTAIN.** Assignment uncertainty and evaluation uncertainty have separate denominators and meanings.

All provider-visible Stage A packets omitted historical labels, selection reasons and operator hypotheses. Every role output was frozen before constructing Stage B. Stage B used the frozen role and exact associated contract with allowlisted role-appropriate evidence; supplied facts received only claim and target. Historical labels were opened only after the complete Stage B freeze. The evaluator did not reclassify any role.

## Every selected claim and historical comparison

An asterisk marks a mandatory anchor. H.6 labels in this table are post-freeze comparison evidence only. “—” means ineligible for Stage B.

| H.6 claim | Old H.6 status | Frozen role or assignment result | New verdict |
|---|---|---|---|
| H6-T01-1/C002 | SUPPORTED | DERIVED_INFERENCE | SATISFIED |
| H6-T01-1/C026* | UNSUPPORTED | GOVERNANCE_RULE | SATISFIED |
| H6-T01-1/C059* | UNSUPPORTED | GOVERNANCE_RULE | SATISFIED |
| H6-T01-2/C055 | SUPPORTED | ROLE_UNCERTAIN | — |
| H6-T01-2/C061* | UNSUPPORTED | GOVERNANCE_RULE | SATISFIED |
| H6-T01-3/C033 | SUPPORTED | ROLE_UNCERTAIN | — |
| H6-T01-3/C037* | UNSUPPORTED | GOVERNANCE_RULE | SATISFIED |
| H6-T02-1/C036 | SUPPORTED | DERIVED_INFERENCE | CONDITIONAL |
| H6-T02-1/C040* | CONDITIONAL_WARRANT | ROLE_UNCERTAIN | — |
| H6-T02-2/C001* | UNSUPPORTED | SUPPLIED_FACT | SATISFIED |
| H6-T02-2/C002* | UNSUPPORTED | SUPPLIED_FACT | SATISFIED |
| H6-T02-2/C008 | SUPPORTED | ATOMIZATION_DEFECT | — |
| H6-T02-2/C009 | SUPPORTED | SUPPLIED_FACT | SATISFIED |
| H6-T02-2/C017 | SUPPORTED | OPERATION | SATISFIED |
| H6-T02-2/C020 | SUPPORTED | CONDITIONAL_RELATION | SATISFIED |
| H6-T02-2/C058 | SUPPORTED | LIMIT | SATISFIED |
| H6-T02-2/C075 | SUPPORTED | ROLE_UNCERTAIN | — |
| H6-T03-1/C026 | SUPPORTED | DERIVED_INFERENCE | SATISFIED |
| H6-T04-1/C020* | UNSUPPORTED | GOVERNANCE_RULE | SATISFIED |
| H6-T04-1/C044* | CONDITIONAL_WARRANT | LIMIT | VIOLATED |
| H6-T04-2/C007 | SUPPORTED | OPERATION | SATISFIED |
| H6-T04-2/C016* | UNSUPPORTED | GOVERNANCE_RULE | VIOLATED |
| H6-T04-2/C031 | SUPPORTED | DERIVED_INFERENCE | SATISFIED |
| H6-T04-3/C034* | CONDITIONAL_WARRANT | CONDITIONAL_RELATION | SATISFIED |

Exact claim text, original scope and mapping references are preserved in [selection/claims.json](../claim-role-taxonomy-v0.1/selection/claims.json). Full historical rationales and source hashes are in [comparison/historical.json](../claim-role-taxonomy-v0.1/comparison/historical.json); provider outputs remain unchanged.

## Anchor interpretation and strictness

**Supplied facts:** T02-2/C001 (stable median) and C002 (reported approximate long-delay frequency) both became SUPPLIED_FACT / TARGET_FIDELITY / SATISFIED. The target explicitly supplies both. H.6 had acknowledged their supplied status but required diagnostic signals to establish them. C009, another directly supplied fact, also passed; its historical status was already SUPPORTED. Correct routing does not authorize labeling arbitrary generated assertions as supplied facts; no such negative control was measured.

**Explicit governance:** T01-1/C059 and T01-2/C061 both became GOVERNANCE_RULE / GOVERNANCE_COHERENCE / SATISFIED. Their prospective threshold-setting and workload-triggered stopping rules were coherent without deriving normative authority from a diagnostic signal. No threshold value or harm-onset claim was empirically validated.

**Fallbacks:** T01-3/C037 and T04-1/C020 both became GOVERNANCE_RULE / SATISFIED, contrary to the operator OPERATION hypotheses. Coherence of a readiness-trial fallback or allocation of a release slot to measurement does not demonstrate informative operational design. Neither received OPERATION_LICENSE. H.6 objections about relevance and discrimination therefore remain untested. T01-1/C026 similarly passed as a sparse-booking fallback policy, while the choice of combined recording/handoff trial remains unvalidated. These are concrete permissiveness risks at the role boundary, not evidence that all fallback operations deserve acceptance.

**Conditional anchors:** T02-1/C040 was ROLE_UNCERTAIN and unmeasured in Stage B. T04-1/C044 became LIMIT / VIOLATED: the mapping merely asserts team-size dependence of retention without a warranted connection. The failure did not demand that a hypothetical outcome already occurred. T04-3/C034 became CONDITIONAL_RELATION / SATISFIED: an improvement in *useful* first publication under random assignment can support bounded deployment. P005 still treats publication-as-useful-activation as provisional; passing this hypothetical relation neither validates that proxy nor authorizes actual deployment. The ordinary T02-2/C020 conditional control also passed while preserving hypothetical status.

**Named problematic inference anchors:** T01-1/C026 became GOVERNANCE_RULE / SATISFIED; T04-2/C016 became GOVERNANCE_RULE / VIOLATED. C016 fails because reliable histories without an actionable recurring problem need not have a deficient recording step, so its disjunctive trigger does not coherently license the prescribed recording repair. This is a surviving defect under the assigned governance contract.

**Derived controls:** T01-1/C002, T03-1/C026 and T04-2/C031 passed bounded aggregate, discrepancy-constraint and documentary-attribution conclusions. T02-1/C036 was CONDITIONAL on valid endpoints, comparable/reliable adequately sampled trials and a persistent single transition. All four were historically SUPPORTED. No historically UNSUPPORTED case retained DERIVED_INFERENCE, and no DERIVED_WARRANT evaluation was VIOLATED. The ability to reject genuine overclaims remains unestablished by this experiment, even though the contract permits rejection.

**Other operational and limit controls:** T02-2/C017 and T04-2/C007 passed mechanism-specific evidence comparison and documentary linkage checks. Their rationales discuss applicability and relevance, but no invalid assigned operation was tested. T02-2/C058 passed the restriction that missing traces do not prove a phase was fast. C044 provides a negative LIMIT_WARRANT observation.

## Contract-mismatch attribution

Eight selected claims were historically UNSUPPORTED: seven now pass and one remains violated. The operator audit conservatively attributes **four clear mismatches** to inappropriate historical contracts: T02-2/C001, T02-2/C002, T01-1/C059 and T01-2/C061. **Three qualified routing-dependent changes** are T01-1/C026, T01-3/C037 and T04-1/C020; governance coherence does not settle their historical action-choice/relevance objections. **One genuine defect survives**: T04-2/C016. The raw seven transitions must not be reported as seven vindicated claims or extrapolated to H.6-wide failure prevalence. See [attribution.json](../claim-role-taxonomy-v0.1/comparison/attribution.json).

## Research questions

1. **Can the seven roles be assigned prospectively to natural H.6 claims?** Partly: 19/24 received one role, 4 were role-uncertain and 1 required splitting. Six roles were observed; SOURCE_FACT was not assigned. One judgment per claim provides no repeatability estimate.

2. **Which claims are genuinely role-ambiguous?** The provider could not resolve T01-2/C055 and T02-2/C075 between SOURCE_FACT and LIMIT; T01-3/C033 between DERIVED_INFERENCE and GOVERNANCE_RULE; or T02-1/C040 among CONDITIONAL_RELATION, OPERATION and GOVERNANCE_RULE. These are observed ambiguities under the frozen definitions, not proof no future rule could resolve them.

3. **Which frozen claims reveal atomization defects?** T02-2/C008 combines the limitation that explanations can coexist with an instruction for the comparison. It was recorded SPLIT_REQUIRED / ATOMIZATION_DEFECT, excluded from Stage B and never split or repaired.

4. **Do supplied target facts route cleanly to target fidelity?** Yes in this sample: T02-2/C001, C002 and C009 were SUPPLIED_FACT / TARGET_FIDELITY / SATISFIED. Their packets contained the frozen target without diagnostic mapping requirements. This does not test a generated assertion falsely claiming supplied provenance.

5. **Do source facts route cleanly to source fidelity?** Not demonstrated: both intended SOURCE_FACT cases became ROLE_UNCERTAIN against LIMIT. No SOURCE_FIDELITY judgment occurred. The content scan did not establish a third clean candidate; it does not prove absence across H.6.

6. **Do governance rules stop being evaluated as empirical conclusions?** Yes for T01-1/C059 and T01-2/C061: prospective threshold-setting and workload rollback rules passed coherence without requiring a diagnostic signal to establish an authored norm. This grants no empirical truth to threshold values.

7. **Can governance rules still fail for incoherence or false empirical presentation?** A failure was observed: T04-2/C016 is VIOLATED because reliable histories with no actionable recurring problem need not contain the recording deficiency its rule presupposes. This tests trigger/action coherence and embedded empirical presupposition. No separate pure masquerading-as-discovery control was measured.

8. **Do fallback operations receive meaningful operational scrutiny rather than automatic acceptance?** Not established for either mandatory fallback: T01-3/C037 and T04-1/C020 were GOVERNANCE_RULE and passed coherence, leaving the mechanism and information-value objections untested. T02-2/C017 and T04-2/C007 received substantive OPERATION_LICENSE rationales and passed, but there was no assigned invalid-operation control.

9. **Do conditional relations preserve hypothetical status?** Yes for T02-2/C020 and T04-3/C034: both are SATISFIED without asserting an outcome occurred. The latter conditions on useful publication; the packet retains P005 provisional proxy validity, which remains unestablished in real application. Of the other named cases, T02-1/C040 was ambiguous and T04-1/C044 was LIMIT / VIOLATED for an unjustified confound, not for lack of an observed effect.

10. **Do genuine unsupported derived inferences remain rejectable?** The contract still permits VIOLATED, but empirical preservation of strict rejection was not demonstrated. All four assigned DERIVED_INFERENCE cases were historically SUPPORTED; three passed and one was CONDITIONAL. The two named problematic inference anchors became GOVERNANCE_RULE. Do not infer successful negative-control discrimination from this run.

11. **How many historical UNSUPPORTED outcomes appear attributable to contract mismatch?** Of eight selected historical UNSUPPORTED outcomes, seven now pass and one remains violated. Four are clear mismatch cases (T02-2/C001, C002; T01-1/C059; T01-2/C061). Three changes (T01-1/C026; T01-3/C037; T04-1/C020) are qualified and routing-dependent because action-choice/relevance objections were not tested under OPERATION_LICENSE. Count neither all seven as vindicated nor the sample as H.6-wide prevalence.

12. **Does the taxonomy create any new systematic ambiguity?** Repeated SOURCE_FACT/LIMIT overlap and governance/operation routing of conditional action choices are systematic boundary risks within this sample; inference/governance and conditional/action overlap also occur. Frequency and novelty relative to other taxonomies are unmeasured. The schema is executable but not sufficiently validated to treat the next warrant/admission recovery step as calibrated.

## Integrity, budget and limitations

The [completed-run audit](../claim-role-taxonomy-v0.1/review/final-verification.json) verifies frozen hashes and additive scope, deterministic requests, raw-response/event equality, 43 unique isolated sessions, schema/provenance validity, complete Stage A before any Stage B execution, and one prior ledger reservation per session. Premeasurement tests passed 61/61. No provider incident, harness retry, substitution or tool activity was observed. Astra/high was requested throughout; the CLI did not expose a verified served snapshot or hidden provider retry behavior.

One engineering incident preceded Stage B: packet preparation returned a live subprocess while dependent bookkeeping began too early. An unapproved stale plan and incorrect checkpoint metadata were archived, the already-correct packets were committed, and a new plan superseded the stale plan additively. No Stage B request or reservation used the stale plan; positive hash, allowlist and lineage evidence established non-contamination before resumption. See [recovery evidence](../claim-role-taxonomy-v0.1/review/recovery/stage-b-preparation-order/evidence.json) and [resolution](../claim-role-taxonomy-v0.1/review/recovery/stage-b-preparation-order/resolution.json). No scientific observation or frozen role was rewritten.

The initial approved cumulative cap was 48 sessions at UNKNOWN cost (plan hash `0d55f965b5172be41e65603b41f7e81324e94c29bd1c3ba4094e8d159d4a729a`). After assignment, the valid forecast narrowed it to 24+19=43 (plan hash `127d2872e4ac030c637ba2f437330ad53c1755d55de2c26062e2c049a436e97e`). The user’s completion approval covered the remaining UNKNOWN allowance risk and within-cap refinement; financial and usage consents were recorded. Each of 15 bounded batches received a fresh preflight and before/after snapshots. The 10-point reserve was retained and no reset credits were redeemed. Dollar cost remains UNKNOWN. All calibration observations are retained with exclusions because concurrent interactive account work and unsettled telemetry prevent clean attribution; no percentage-per-session rate was inferred. Account data and the budget ledger remain under `.runtime/`.

The corpus is purposive and small, with one model judgment per claim and no independent adjudicator. Operator concordance is not accuracy against established truth. SOURCE_FACT has no measured evaluation, several roles lack negative controls, and the governance/operation boundary can avoid scrutiny of an action’s usefulness. The conditional publication result does not resolve outcome-proxy validity. These limitations prevent claiming the full seven-role taxonomy is validated, reliable across H.6, or sufficient for admission recovery.

**Recommended next step:** clarify SOURCE_FACT/LIMIT and governance/operation/inference boundaries offline, then separately preregister and authorize a bounded natural-claim calibration with genuine negative derived-inference and operation coverage. Preserve these observations. The recommendation was not executed. H6.R1 stops here: no terminal-state precedence fix, provider no-observation formalization, H.6 resumption, ablation, admission or new natural-output run.
