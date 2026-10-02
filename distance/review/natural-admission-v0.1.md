# H.6 — Fresh natural-output admission pilot v0.1: incomplete terminal report

**Status: TERMINATED_MEASUREMENT; H.6 admission measurement is incomplete.** All 18 natural mappings and all 1,042 atomic claims were generated and frozen. Warrant measurement stopped after 736 valid judgments when Astra reported capacity exhaustion for one request. No ablation, remainder/inquiry inventory, artifact judgment, or full instrumentation assessment was performed. This is not an admission success/failure result.

Base: `experiment-h5-span-provenance` at `fae0c0b742cd3bcbc7b54599fa9f6234b0ffdc4b`. Work/publication branch: `experiment-h6-natural-admission`. No merge to main, production integration, ranking, sample expansion, replacement generation, model substitution, or duplicate judgment.

## Stop and preservation

At 2026-10-02 06:00:22 UTC, `H6-T05-1--C027` returned the provider message “Selected model is at capacity. Please try a different model.” The frozen [protocol](../natural-admission-v0.1/PROTOCOL.md) makes provider failures terminal and non-retriable, under the repository [recovery policy](../../docs/EXPERIMENT-RECOVERY-POLICY.md). The suggested substitution was not followed.

All in-flight results were retained. The final claim-stage disposition is 736 successful observations, one failed provider observation, one reserved but demonstrably unlaunched request (`H6-T05-1--C028`), and 304 never-reserved claims. Thus 306 of 1,042 claims have no warrant judgment. There were 773 started provider sessions across generation, atomization and warrants: 772 successful observations and one failure. No additional probe or retry calls occurred.

A concurrent cancellation exposed a bookkeeping defect: the failed provider call appended `TERMINATED_MEASUREMENT`, then the unlaunched reservation appended `PAUSED_AMBIGUOUS`. Both states block the frozen runner from restarting. The original records are preserved; an additive adjudication restores the already-established terminal state. No scientific input or output was changed and no request launched after the observed failure. The frozen runner was not repaired or resumed. See the [terminal incident](../natural-admission-v0.1/review/terminal-incident.json) and [partial freeze](../natural-admission-v0.1/claim-judgments-partial-freeze.json).

## Checkpoints

| SHA | Checkpoint |
| --- | --- |
| `7e0a5aa34d4711e483d22f82a2803b90b353ac7f` | Freeze H.6 six natural target frames before instrument pairing |
| `5f558b418a37de757aff42cc4fc02cfb98e8004a` | Freeze H.6 deterministic family-diverse instrument selection rule |
| `5778d1a1ba8b53b1eac3ea53c68ace7f6ba82251` | Freeze H.6 protocol pairings rubrics schemas and passing collision preflight |
| `0019d97aca02b183102cc03ef71f3305f7a7ff92` | Freeze H.6 eighteen isolated natural generation packets |
| `03680bda42022f54c0c3d25d028f0cd50c2824c6` | Freeze all 18 H.6 natural mappings raw generations and unchanged H.5 spans |
| `f59a7e74f3afe7665cff969333b1499be342b1b4` | Freeze H.6 atomic claim extraction packets before warrant judgments |
| `95e416da3bafa496eb69a9643118987bcf75262a` | Freeze H.6 all eighteen atomic claim inventories before warrant measurement |
| `31c560d5f41ccda9cd857db07f670e1b9f70b323` | Freeze H.6 1042 isolated one-claim warrant judgment packets |
| `5bcdca315a1485ebbdbcc67c3b469a61c8249c05` | Preserve terminal H.6 Astra capacity failure and 736 unchanged warrant judgments |

The report/publication seal is additive to these checkpoints; its resolved final SHA is reported with the pushed branch and publication manifest.

## Targets and selection

Targets were committed before the selection rule and before any pairing. They contain no expected transfer or artifact status. Full frames are in [targets](../natural-admission-v0.1/targets/).

| Target | Domain | Concrete problem |
| --- | --- | --- |
| T01 | Organizational / operational | Reduce late equipment-booking starts at a municipal depot with fragmented return, cleaning and collection logs, without more staff or equipment. |
| T02 | Technical | Investigate intermittent overnight workspace-export delays with uneven trace coverage and choose a safe deployment action. |
| T03 | Compliance / procedural | Explain missing supplier-approval attachments under a supplied internal rule, using potentially dispersed approval records before a board review. |
| T04 | Product / customer | Decide what to change about onboarding drop-off with one release slot, incomplete event data and competing interview explanations. |
| T05 | Project / process | Allocate museum digitization work and consider exhibition scope with metadata/rights backlogs, heterogeneous folders and volunteer schedules. |
| T06 | Analysis / decision | Design a reversible library weekend-hours trial under fixed staffing and conflicting demand evidence. |

The [frozen selection rule](../natural-admission-v0.1/SELECTION.md) uses the 14 accepted instruments at the base. For each target in order, select three distinct recorded source families, minimizing global prior use count, then SHA-256 of the fixed seed/target/slot/instrument identity. Target wording, similarity and predicted success are not inputs. All 14 accepted instruments occur across the 18 pairings. No new instrument was authored.

## All 18 pairings and completion

All rows have a parsed natural mapping and frozen H.5 spans. “Warrants” is completed/planned. No row has an end-to-end artifact status.

| Packet | Instrument | Atomic claims | Warrants | Unsupported judgments |
| --- | --- | ---: | ---: | ---: |
| H6-T01-1 | CLINICAL-DIAGNOSIS-SERIAL-MONITORING-001 | 65 | 65/65 | 2 |
| H6-T01-2 | SOFTWARE-DELTA-DEBUGGING-001 | 65 | 65/65 | 1 |
| H6-T01-3 | INTELLIGENCE-SOURCE-CORROBORATION-001 | 60 | 60/60 | 1 |
| H6-T02-1 | SOFTWARE-REGRESSION-BISECTION-001 | 57 | 57/57 | 0 |
| H6-T02-2 | INTELLIGENCE-ACH-001 | 77 | 77/77 | 2 |
| H6-T02-3 | CONTROL-SYSTEMS-STEP-RESPONSE-001 | 63 | 63/63 | 0 |
| H6-T03-1 | SEISMOLOGY-SEISMIC-TOMOGRAPHY-001 | 50 | 50/50 | 0 |
| H6-T03-2 | ARCHIVAL-PROVENANCE-RECONSTRUCTION-001 | 48 | 48/48 | 0 |
| H6-T03-3 | CLINICAL-DIAGNOSIS-DECHALLENGE-RECHALLENGE-001 | 47 | 47/47 | 0 |
| H6-T04-1 | ANALYTICAL-CHEMISTRY-CHROMATOGRAPHY-001 | 55 | 55/55 | 2 |
| H6-T04-2 | FORENSICS-CHAIN-OF-CUSTODY-001 | 58 | 58/58 | 1 |
| H6-T04-3 | CLINICAL-DIAGNOSIS-DIFFERENTIAL-001 | 65 | 65/65 | 0 |
| H6-T05-1 | DENDROCHRONOLOGY-CROSSDATING-001 | 68 | 26/68 | 0 |
| H6-T05-2 | FORENSICS-LUMINOL-001 | 59 | 0/59 | 0 |
| H6-T05-3 | SOFTWARE-REGRESSION-BISECTION-001 | 47 | 0/47 | 0 |
| H6-T06-1 | DENDROCHRONOLOGY-CROSSDATING-001 | 62 | 0/62 | 0 |
| H6-T06-2 | ANALYTICAL-CHEMISTRY-CHROMATOGRAPHY-001 | 49 | 0/49 | 0 |
| H6-T06-3 | CLINICAL-DIAGNOSIS-SERIAL-MONITORING-001 | 47 | 0/47 | 0 |

Twelve mappings have all their warrant judgments; T05-1 has 26 of 68, and the final five mappings have none. This ordering reflects the fixed schedule and provider stop, not selection by outcome.

## Measurements

| Measure | Observed count / status |
| --- | --- |
| Generation calls / parsed mappings | 18 / 18 |
| Generation failures | 0 |
| Atomization calls / atomic claims | 18 / 1,042 |
| Successful warrant calls | 736 / 1,042 planned |
| SUPPORTED | 722 |
| CONDITIONAL_WARRANT | 3 |
| UNSUPPORTED | 9 |
| UNCERTAIN warrant | 2 |
| Claims actually deleted | Not measured; ablation did not run |
| Remainder candidates | Not measured |
| TARGET_CONSTRAINT / INQUIRY_CONSTRAINT / INSUFFICIENCY_ONLY / UNCERTAIN roles | Not measured; zero assigned for each |
| Productive YES / NO / UNCERTAIN | Not measured; zero assigned for each |
| KEEP_WITH_WARRANT_FLAGS / KEEP_WITH_REDUCED_SCOPE / CORE_INVALID / UNCERTAIN_LOAD_BEARING | Not measured; zero assigned for each |
| Full instrumentation CLEAN / WARNING / FAILURE | Not assessed; zero assigned for each, 18 unassessed |
| End-to-end mappings complete | 0 / 18 |

Zeros in the unmeasured stages are not evidence that a phenomenon was absent. In particular, there are no assigned CORE_INVALID or UNCERTAIN_LOAD_BEARING cases to explain. No provider/provenance error was converted to CORE_INVALID. The [metrics](../natural-admission-v0.1/metrics.json) retain explicit missingness and per-mapping counts.

## What the partial warrant observations show

The nine UNSUPPORTED judgments occur in six mappings. They identify local claims, not whole-artifact rejections. The limited terminal review inspected all 14 non-SUPPORTED completed judgments and all nine atomization anomaly records. It did not independently re-rate the 722 SUPPORTED judgments or complete the preregistered operator audit. Frozen labels remain unchanged. See [review](../natural-admission-v0.1/review/terminal-audit.json) and [cited evidence](../natural-admission-v0.1/review/terminal-claim-evidence.json).

| Packet / claim | Frozen status | Diagnostic observation |
| --- | --- | --- |
| T01-1 / C026 | UNSUPPORTED | Sparse bookings do not by themselves establish why a combined recording-and-handoff trial should be selected first. |
| T01-1 / C059 | UNSUPPORTED | A predeclared service-impact threshold is treated as a conclusion that must follow from a diagnostic signal; governance-rule versus inference eligibility needs clarification. |
| T01-2 / C061 | UNSUPPORTED | A rule to stop/reverse when agreed workload limits are exceeded has the same governance-versus-inference issue. |
| T01-3 / C037 | UNSUPPORTED | The readiness-confirmation fallback lacks an explicit discriminating relation; its general informational value is a plausible alternative reading, not an adjudicated repair. |
| T02-1 / C040 | CONDITIONAL_WARRANT | The bounded deployment experiment depends on reproducing the regression and its reversal. |
| T02-2 / C001, C002 | UNSUPPORTED | Stable median and roughly one-in-twenty slow exports are explicitly supplied target facts. The judge rejects them because the diagnostic signal does not establish them. This is a claim-type/rubric interface mismatch, not generator fabrication. |
| T02-3 / C032 | UNCERTAIN | “Expansion” of a lower concurrency limit could mean broader adoption or increasing the numerical limit; the mapping does not settle the reading. |
| T04-1 / C020 | UNSUPPORTED | The fallback selects unspecified missing measurement without a decision-relevant relation. |
| T04-1 / C023 | UNSUPPORTED | The harm-only early-stopping rule makes an exclusive claim beyond the rationale for harm stopping. |
| T04-1 / C044 | CONDITIONAL_WARRANT | The team-size/retention relation remains an unestablished empirical dependency in the frozen judgment. |
| T04-2 / C016 | UNSUPPORTED | Reliable histories can reveal no recurring actionable problem without a deficient recording step. The authored disjunction does not warrant its recording-repair prescription. |
| T04-3 / C014 | UNCERTAIN | Whether an obstacle-conditioned “change” includes a diagnostic release remains unresolved. |
| T04-3 / C034 | CONDITIONAL_WARRANT | Deployment support depends on the provisional relation between first publication and useful activation. |

**Prominent limitation:** the supplied-fact judgments and governance-rule cases show that broad all-field atomization plus a signal-centric warrant rubric can classify premises and design rules as unsupported generated inferences. The model can follow the literal frozen question while missing the intended admission distinction. This needs prospective clarification; silently changing eligibility or labels now would contaminate measurement. Whether these deletions would actually poison artifact admission is unknown because no ablation occurred.

## Requested example categories

A cleanly traceable local defect is available: T04-2/C016 is grounded in P008, which joins unreliable histories and no recurring actionable problem before prescribing repair of a deficient recording step. H.5 makes that local gap inspectable. **Surviving machinery after ablation is not established.** Reduced-scope survival, true core invalidity, productive target constraints, productive inquiry constraints and insufficiency-only rejection were not measured; no examples are manufactured.

## H.5 provenance and instrumentation

All 18 natural mappings were segmented into **574 spans** by the unchanged H.5 implementation: 27–40 per mapping, all prose-paragraph spans. Four uncertain sentence boundaries were retained conservatively. Repeated derivation matches all frozen tables. No clause-level segmentation, manual span editing, exact-text citation requirement, or offset-based semantic citation was used. No natural list/table markup occurred, so natural markup robustness remains untested.

| Stage | SUFFICIENT | INSUFFICIENT | UNCERTAIN |
| --- | ---: | ---: | ---: |
| Frozen atomic components | 1,042 | 0 | 0 |
| Completed warrant components | 1,475 | 0 | 0 |
| Total assessment occurrences | 2,517 | 0 | 0 |

These are annotator-reported support statuses, not independently proven entailments. Repeated assessments of a proposition count separately; empty NOT_APPLICABLE components are excluded. All completed observations replay with zero mechanical/relational citation diagnostics. All provenance insufficiency and uncertainty lists are empty in the available responses. A cleanly traceable unsupported claim still has SUFFICIENT provenance.

All nine model-reported atomization anomalies remain preserved:

| Packet / component | Anomaly | Interpretation retained |
| --- | --- | --- |
| T01-3 / coverage.signal | PROVENANCE_MODEL_ERROR | Coverage erroneously lists C008 under signal although its source is state/limit. The model flags the mistake; no output is repaired. |
| T02-3 / C031 | MAPPING_AMBIGUITY | “Better explanation” leaves the comparative alternative unspecified. |
| T02-3 / C032 | MAPPING_AMBIGUITY | The dimension of “expansion” is unspecified. |
| T04-3 / C014 | MAPPING_SCOPE_AMBIGUITY | Scope of “change” versus diagnostic improvement is unresolved. |
| T05-3 / K028 | MAPPING_AMBIGUOUS_REFERENT | Which queue triggers limiting scanning is not uniquely identified. |
| T06-1 / C026 | SEMANTIC_REFERENT_AMBIGUITY | The demonstrative does not fully delimit the referenced observation set. |
| T06-1 / C035 | SEMANTIC_DECISION_PRIORITY_UNSPECIFIED | Retain/change/restore triggers can overlap without a precedence rule. |
| T06-1 / C056 | SEMANTIC_RESPONSE_CHOICE_UNSPECIFIED | Pause versus reverse is left as a disjunction. |
| T06-3 / C021 | AMBIGUOUS_CONDITION_SCOPE | Qualification of the workload branch is ambiguous. |

Every record reports that correct support is representable with current spans. The meaning ambiguities are preserved source ambiguities, not evidence that clause splitting would resolve them. The terminal review found no case of correct support that demonstrably could not be represented cleanly. A full closed-bundle audit was not completed.

None of the eight H.5-specific failure signals was identified in the available observations/limited review: unrepresentable supported component; repeated uncited substantive dependence; coarse-span conflict/qualifier obstruction; dispersed simple support; outside-bundle qualifier; inferential CONTEXT; nondeterministic segmentation; or markup scope damage. This is bounded preliminary evidence, not a zero-failure estimate for the unmeasured downstream stages. CONTEXT use was not exhaustively independently audited.

Other preserved warnings/failures are separate from H.5: (1) T01-3 generation logged a system-skill installation directory-removal warning; (2) T05-1/C012 logged a model-cache TTL renewal parse warning; both returned valid observations without tool events; (3) T05-1/C027 had the terminal provider-capacity failure; (4) the cancellation/terminal-state precedence defect described above. Internal effects of CLI cache/startup maintenance were not independently verified. Neither warning caused response repair or retry.

## Packet collisions

`PROV_LOCAL_ID_COLLISION_EXPOSURE`: **0 provider contexts; 1 terminal operator-review context**. The latter legitimately displayed packet-bound evidence for the non-SUPPORTED judgments across nine packets to inspect possible recurring errors. Local IDs were reused; every evidence record remained packet-bound. Exposure is informational.

`PROV_PACKET_ID_COLLISION_FAILURE`: **0 identified**. No observed annotation treated another packet’s text as support, left the intended packet genuinely unresolved, or required an unrepresentable legitimate cross-packet support relation. See [context record](../natural-admission-v0.1/review/collision-contexts.json). The offline [collision preflight](../natural-admission-v0.1/COLLISIONS.md) checks envelope rejection, ordinary local reuse, the adversarial A/P003-versus-B/P003 example, all five required conditions, and direct cross-packet representational impossibility. Its deliberately synthetic cases are excluded from natural counts. Mechanical ID existence is explicitly not semantic acceptance.

## Research-question answers and readiness

1. **Local defects versus all-or-nothing validity:** nine local unsupported judgments were observed, including inspectable inference gaps; some judgments instead expose premise/governance eligibility problems. Truncation prevents a corpus frequency conclusion.
2. **Ablation preserves source machinery:** unmeasured.
3. **Only insufficiency remains:** unmeasured.
4. **Genuine target constraints survive:** unmeasured.
5. **Natural inquiry constraints satisfy H.4:** unmeasured; only offline H.4 integration tests passed.
6. **H.5 represents natural prose without clause splitting:** preliminarily yes for generation/atomization/completed warrant annotations; no downstream conclusion.
7. **Actual coarse-span support ambiguity:** none demonstrated; several original semantic ambiguities remain explicitly traceable.
8. **CONTEXT remains interpretive:** not established by a completed independent audit.
9. **Citation/model mistakes are inspectable:** the self-reported T01-3 coverage mistake is inspectable and distinguished from H.5 architecture failure.
10. **Genuine packet-ID collision failure:** none identified; provider isolation avoided exposure, while operator exposure was recorded.
11. **CORE_INVALID reflects absence of viable remainder:** unmeasured; no artifact status assigned.
12. **Admission is permissive enough for a creative generator:** unmeasured. Supplied-fact/governance treatment is a concrete risk needing prospective clarification.

H.5 has preliminary natural-prose representability evidence. H.4’s behavior on natural inquiry wording and the complete fault-localized admission behavior remain untested. Local warrant failures were localized to claims, but successful isolation **without warrant poisoning has not been demonstrated**. The system is **not yet established as ready for a larger natural run**.

## Limitations and recommended next step

The pilot is incomplete and schedule-truncated; only 736 of 1,042 warrant observations exist. There is no ablation, viability, productivity, inquiry-role or artifact-status evidence. Target construction is authored, instrument assignment is deterministic rather than representative sampling, and all scientific roles request one model family. Operator review is diagnostic, limited and not an independent re-rating. Served model/snapshot identifiers were not exposed; requested `gpt-6-astra` and high reasoning, pinned CLI/binary hashes, session identities, commands and usage are recorded without inventing snapshot IDs. Hidden CLI/provider retries cannot be ruled out; harness retries were zero. Semantic-object ablation was preregistered but never exercised. The 1,042-claim inventory also exposes substantial annotation/execution overhead for an 18-mapping pilot.

Recommend a **separately authorized, preregistered recovery study** before any larger run: resolve claim eligibility/evidence roles for supplied premises and authored governance rules, specify handling of the failed/missing observations without rewriting the frozen evidence, and test terminal-state precedence under concurrent cancellation. Preserve the successful observations and original failure as historical data. Do not treat a capacity retry or a changed rubric as continuation under this unchanged protocol. **This recommendation was not executed.**

## Verification

The premeasurement gate passed 13 H.3 tests, 32 H.4 tests, 30 H.5 tests and 13 H.6 tests (88 total), including historical fixture replay, simultaneous-deletion lineage, polarity-independent inquiry coverage, absence of exact-text/offset semantic requirements and collision preflight. Two premeasurement historical-adapter failures were preserved and fixed before any provider call. All 4,313 base files retain their original bytes. Terminal verification replays raw requests/responses, metadata, schemas, diagnostics, unique sessions, no post-failure launches, the unlaunched reservation, and absence of downstream calls. Final checks are recorded in [publication verification](../natural-admission-v0.1/review/publication-verification.json).
