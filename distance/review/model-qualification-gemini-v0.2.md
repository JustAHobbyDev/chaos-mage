# Gemini capability qualification v0.2

**Qualification: `not_qualified`.**

Gemini 3.1 Pro Preview / high does not meet the frozen capability threshold in this sample. It repeatedly accepts target conclusions that the supplied operations and signals do not establish in E006, E022 and E030. This independent decision was committed before historical comparison. N004 adds a separate baseline/uncertainty failure, but the decision does not depend on that contestable individual case. Reliable provider/schema behavior and competent mechanism and anti-collapse reasoning elsewhere do not remove the repeated warrant problem.

## Starting point, recovery and freezes

- Starting SHA: `cee19ee0c4c110df65de7c4380f0c271b298f30a`; local and origin/main matched.
- Preparation: `12aeab0fe7c62bcf35c9d1d1dd6f28dc11f63739`.
- Successful two-schema preflight: `e28e62f92e61f451d4f2cfd776741693556725d2`.
- Twelve-judgment result freeze: `e70024a8d1347521f8697416e79980a1d447076d`.
- Independent assessment before historical decoding: `041d0fd4a47b53aca526cd1a2011993aacf419c3`.
- Completion: commit introducing this report, reported separately to avoid self-reference.

Gemini v0.1 is unchanged and remains qualification_inconclusive. Its successful
artificial response returned lowercase serviceTier standard; the harness incorrectly
expected uppercase STANDARD. V0.2 corrects that exact representation, requests
Standard explicitly at the top level, and serializes thinkingLevel high. V0.1's
accepted HIGH was not a provider/model failure. V0.2 uses fresh probes and judgments,
separate cost accounting and the same $2 ceiling. No v0.1 answer informed prompt tuning.

The contract was originally frozen at 1f51578aff8f8409b9a3c297a86ed84f8e6d7ee1;
SHA-256 `21b2ce7aeda5eef39175eb838f31f148afa7339e8fe02719c6ea1a2bf7acf31a`.
It, all historical classifiers, canonical schemas, native baselines and packets
are unchanged. The [manifest](../model-qualification-gemini-v0.2/manifest.json) records full source paths, commits, hashes, source-freeze
bindings, and historical-output hashes. Input/packet hashes are:

| Case | Stage | Source commit | Input / packet SHA-256 |
|---|---|---|---|
| E003 | validity | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` | `befdfadfd0e984257e8df1b035169dc1a5a542c34f1571bf5087ab1c95afbfc5` |
| E010 | validity | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` | `78e654a7692ab68caba0df853fc11fa4908aad951c19d775805a99dce1d5be43` |
| E014 | validity | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` | `b29ef4643df718bf701493904d2bfd898a3813bb31bfc7cae711722262109e15` |
| E006 | validity | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` | `19c70caa2701e2268a091746a56d2ea200b7a059becd92ef9a0d9540503e9a89` |
| E022 | validity | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` | `148c8fe60a7b711d8333dd333baccea67c4bc3ea34ed420ec06e7de2cef26082` |
| E030 | validity | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` | `74a4466ed5bfe3b8266fcb913265f3fab153c4082fae3a4780cd2fec5ee9bab2` |
| N010 | anti-collapse | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` | `cc341a68c5f2aa8ea7faec8e3090926af2d3b7ab6a7c90da7adbc544acffafcb` |
| N006 | anti-collapse | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` | `f459b6e000d843f88d0f80dfc7f5df3ed2d56ce48091e05577e51d261741624c` |
| N001 | anti-collapse | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` | `180e00d2fe19d86ce3d0025f55752a0c54047a82e4747780a7270a6a3ab97d5a` |
| N002 | anti-collapse | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` | `9205f239ac8dec34ec0bcba8bdb4f5f73f2238b2cb7cf6f941b0257437283d46` |
| N004 | anti-collapse | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` | `0e6ac2f7d472ea31499bddac880b40874931a7a6c7cd351b410e10aab0006313` |
| N009 | anti-collapse | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` | `63c5af8a9b8335a0d03154e67a56f4d186952f9b86fd78b2e0239eaaa7fddfa8` |

- validity: classifier `7bc98c9c46583125f57112dbd9f7cac4027d1d671894a39779ef512bdaf91804`; canonical schema `7bd5161d5f9ad48d3c650c74e083846aa6ba312a92372fb3c25a3f4e44cf4405`.
- anti-collapse: classifier `a20cfeb7803e93bd4fb44c41b3f9e8d58c9e49da9289912250a5b22833c4651b`; canonical schema `47bb3a2f3b435bf44a1e5493ce5a2f0c646ad2144aeef46b1575f2770965fdf6`.

## Provider, schemas and isolation

Requested model: gemini-3.1-pro-preview. Returned identifiers: gemini-3.1-pro-preview.
Requested serviceTier: standard; returned tiers: standard.
Explicit thinkingConfig.thinkingLevel high; no thinkingBudget. Maximum output
32768, temperature 1.0; top-p/top-k/seed unset, recorded as provider defaults.
Native v1beta endpoint: https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent .
Client: Python 3.14.7 standard-library urllib.request; jsonschema 4.23.0. Full versions
are recorded in execution-config.json and every reservation. No SDK or harness
retries; no model fallback. Returned preview aliases do not establish immutable
served weights. Response IDs and raw metadata are preserved; hidden internal
provider retries remain unobservable. Credential source: environment via authorized
helper; temporary secret file removed before calls, never passed in argv or artifacts.

Native responseMimeType application/json and responseJsonSchema enforce the frozen
wire projection. It removes only $schema, $id and conditional allOf from the
canonical schema. Fields, enums, requiredness and null semantics are preserved;
unchanged full canonical and cross-field validation follow decoding. No repair.
Both artificial schemas passed before measurement and their freeze was committed.

Each primary request contained one user packet, fresh process/request identifier and
empty temporary working directory; no history, system/developer additions, external
context, tools, browsing, grounding, URL context, code execution or retrieval.
Exact packet bytes match the prior Muse qualification. No historical labels, reviews,
operator case intent or known failure descriptions reached Gemini. Randomized order
uses the existing within-stratum shuffle and alternating-strata methodology.
All twelve results were committed before independent assessment and historical
comparison. Preliminary assessment was saved before decoding historical outputs;
any later classification changes are recorded per case. The operator handoff had
already disclosed selected historical findings; this is not a claim of human blinding.

## Mechanical results and cost

Primary planned/attempted/successful: **12/12/12**. Artificial planned/successful:
**2/2**. Provider/schema/harness failures: **0/0/0**. Fresh Astra/Fable/Muse and
Experiment F calls: **0**. No repeated samples or retries.

- Validity: {"Valid": 5, "Conditional": 1, "Invalid": 0}.
- Anti-collapse: {"CLEAR_COLLAPSE": 4, "BORDERLINE_KEEP": 0, "SUFFICIENT_DEPARTURE": 2}.
- Gate: keep 2; reject 4.
- Input tokens: 24723.
- Candidate output tokens: 6238.
- Thinking tokens: 22158.
- Billable output including thinking: 28396.
- Estimated preflight cost: $0.022470.
- Estimated primary cost: $0.367728.
- Estimated experiment cost: **$0.390198**, below $2 ceiling.

Rates frozen from [Google pricing](https://ai.google.dev/gemini-api/docs/pricing):
$2/M input and $12/M output including thinking at these context sizes. Prompt,
candidate and thought counts reconcile to totals. No double counting; no cache
discount assumed. Each request reserved conservative input plus the full output cap
before sending. These are estimates, not invoices; cost is descriptive, not eligibility.

Descriptive historical raw-status comparisons (not accuracy):
{"same_as_both": 6, "same_as_one": 4, "different_from_both": 2};
{"same_as_muse": 9, "different_from_muse": 3}.

## Capability assessment

- Model failure (4): E006, E022, E030, N004.
- Ontology/specification ambiguity (2): E010, E014.
- Legitimate reasoning variation (2): N002, N009.
- Warrant failures: ["E006", "E022", "E030"].
- Mechanism failures: [].
- Baseline-use failures: ["N004"].

The repeated pathology is evidential-warrant reasoning: correct descriptions of the source method coexist with acceptance of an unsupported target inference. E006 endorses irregularity from surviving alternatives; E022 conditions execution quality without establishing temporal-feature discrimination or delay localization; E030 treats ledger continuity and tagged reconstruction as sufficient for arrangement claims. No repeated source-mechanism loss, formalization-as-novelty pattern, or suppression of modest departures is established. N001/N006 correctly collapse formalization alone, N002 preserves the modest binding acquisition rule, and N009 preserves coordinated alignment. N004 is a separate failure to distinguish available tools from baseline practice and to retain uncertainty, not evidence of a repeated baseline pathology.

### E003 — Valid

Recognizes bounded rollback/reintroduction with matched load strata and a contemporaneous control as preserved dechallenge/rechallenge.

The packet specifies isolation, safety aborts, delays, workload matching and bundle-level attribution. Its proposed observation supports increased causal contribution, not a claimed culprit without evidence. Gemini follows that distinction. Its emphatic language is unnecessary but the Valid classification evaluates a coherent prospective protocol rather than asserting observations have occurred. No missing substantive warrant was identified. Historical rationales also retain bounded dechallenge/rechallenge; they supply no reason to revise the independent assessment.

Dimensions: protocol_compliance=pass, instrument_structure=pass, mechanism_reasoning=pass, warrant_reasoning=pass, native_baseline_use=pass, uncertainty_handling=pass, rationale_coherence=pass.

Preliminary class: `none`; final: `none`; consequence: none.

Historical context: astra_status=Valid, fable_status=Valid, muse_status=Valid. Classification changed: false. Historical context does not change the independent capability assessment.

### E010 — Valid

Accepts differential diagnosis as a bounded hypothesis-ranking procedure; retains uncertainty about log granularity and test independence.

The packet separates waits from work, generates competing mechanisms, records nondiscrimination, checks timestamp meaning and limits elimination to tests capable of detecting a candidate. Gemini preserves these constraints and does not turn association into unique causation. The unmeasured workflow telemetry can reasonably be treated as execution prerequisites within a proposed protocol; the uncertainty field makes those practical limits visible. Valid is defensible without demanding an actual completed investigation. Historical rationales expose the protocol boundary between a coherent prospective diagnostic procedure and established availability of discriminating telemetry. Fable explicitly permits the former reading; Astra and Muse require more established conditions. Gemini retains practical uncertainty and is defensible under the former reading. Context identifies specification ambiguity, not evidence of a capability failure.

Dimensions: protocol_compliance=pass, instrument_structure=pass, mechanism_reasoning=pass, warrant_reasoning=pass, native_baseline_use=pass, uncertainty_handling=pass, rationale_coherence=pass.

Preliminary class: `none`; final: `ontology_specification_ambiguity`; consequence: minor.

Historical context: astra_status=Conditional, fable_status=Valid, muse_status=Conditional. Classification changed: true. Historical rationales expose the protocol boundary between a coherent prospective diagnostic procedure and established availability of discriminating telemetry. Fable explicitly permits the former reading; Astra and Muse require more established conditions. Gemini retains practical uncertainty and is defensible under the former reading. Context identifies specification ambiguity, not evidence of a capability failure.

### E014 — Valid

Separates functional-demand retention patterns from necessity evidence supplied by coherent omission/restoration and pair comparisons.

The mapping does not infer necessity from retention alone: it requires activation failure on coherent omission and recovery on restoration, under comparable conditions. Gemini identifies those operations and bounded interactions, while preserving co-elution and nonspecific-signal limits. The functional rather than literal chemical counterpart is permitted by the classifier. The response is concise but supports the operative chain. The historical rationales distinguish a prospective functional omission/restoration protocol from prior establishment of clean attribution and empirical necessity relations. The frozen protocol leaves that Valid/Conditional boundary open. Gemini preserves bounded interactions; its result is not a failure merely because other implementations classify the execution prerequisites as conditions.

Dimensions: protocol_compliance=pass, instrument_structure=pass, mechanism_reasoning=pass, warrant_reasoning=pass, native_baseline_use=pass, uncertainty_handling=pass, rationale_coherence=pass.

Preliminary class: `none`; final: `ontology_specification_ambiguity`; consequence: minor.

Historical context: astra_status=Valid, fable_status=Conditional, muse_status=Conditional. Classification changed: true. The historical rationales distinguish a prospective functional omission/restoration protocol from prior establishment of clean attribution and empirical necessity relations. The frozen protocol leaves that Valid/Conditional boundary open. Gemini preserves bounded interactions; its result is not a failure merely because other implementations classify the execution prerequisites as conditions.

### E006 — Valid

Endorses the ACH mapping as strictly bounded and Valid without inspecting its surviving-hypotheses-to-irregularity assertion.

The exact inference says that if H1 and H3 both survive, the defensible statement is that the process was irregular. Retention in a comparative inconsistency matrix does not itself positively establish irregularity; the clause does not require authenticated evidence of an irregular act and does not even require that all regular-process alternatives have been eliminated. This remains a gap even if all proposed observations and ratings are obtained. Gemini correctly describes comparative elimination and repeats survival-is-not-proof, but then endorses every mapped conclusion as strictly bounded. It misses a substantive unsupported inference under the explicit v0.3 rule, not merely missing execution data or a disagreement about labels. Historical context does not change this assessment: Fable and Muse also accept Valid, while Astra identifies the unsupported irregularity inference. The explicit inference clause, not the number of agreeing models, determines the finding.

Dimensions: protocol_compliance=pass, instrument_structure=pass, mechanism_reasoning=concern, warrant_reasoning=fail, native_baseline_use=pass, uncertainty_handling=concern, rationale_coherence=concern.

Preliminary class: `model_failure`; final: `model_failure`; consequence: material.

Historical context: astra_status=Invalid, fable_status=Valid, muse_status=Valid. Classification changed: false. Historical context does not change the independent capability assessment.

### E022 — Conditional

Returns Conditional for clean interventions, accurate timestamps, known initial state and disturbance controls, while accepting the temporal-feature interpretations.

The packet claims long dead time followed by a prompt response suggests fixed waiting rather than capacity shortage, and uses temporal features to locate accumulating delay. Such response shapes can arise from interacting queues, capacity limits and aggregation; telemetry quality and a clean intervention do not uniquely distinguish these mechanisms. Gemini supplies concrete execution conditions, but none establishes the missing signal-to-mechanism discrimination, and it calls the resulting inferences directly warranted. The issue is not that a prospective intervention is unexecuted: the stated conditions can all hold while the mapped explanatory contrast remains unsupported. This is a missed warrant, despite the more cautious Conditional status. A concrete additional counterexample sharpens the same preliminary concern: a downstream boundary can inherit upstream delay, so the boundary with the longest dead time need not be the location where waiting accumulated. Clean timestamps and controlled steps do not resolve that localization warrant. Historical Fable explicitly conditions feature-to-waiting-share validation; Gemini does not. Sharing its Conditional status therefore does not establish equivalent reasoning.

Dimensions: protocol_compliance=pass, instrument_structure=pass, mechanism_reasoning=concern, warrant_reasoning=fail, native_baseline_use=pass, uncertainty_handling=concern, rationale_coherence=concern.

Preliminary class: `model_failure`; final: `model_failure`; consequence: material.

Historical context: astra_status=Invalid, fable_status=Conditional, muse_status=Conditional. Classification changed: false. Historical context does not change the independent capability assessment.

### E030 — Valid

Treats a continuous handling ledger and the distinction between contemporaneous and reconstructed entries as enough to support the proposed assembly account.

A continuous post-compositional ledger can document an actual reordering; continuity therefore does not establish that the present arrangement is the arrangement the author left. Moreover, compositional entries reconstructed from traces cannot independently corroborate the ordering they were used to construct. Tagging the entries or choosing the fewest breaks makes the reasoning inspectable but supplies no independent warrant. Gemini explicitly says the tags manage inherent circularity and accepts Valid with no uncertainty, missing both unsupported transitions. This is not a complaint about historical evidence being unavailable: the inference can fail even with the mapped ledger fully populated. The historical Invalid/Conditional split does not repair the ledger warrant. Gemini is more affirmative than Muse here, but the failure is still acceptance of continuity and tagged reconstruction as sufficient for the claimed assembly inference.

Dimensions: protocol_compliance=pass, instrument_structure=pass, mechanism_reasoning=concern, warrant_reasoning=fail, native_baseline_use=pass, uncertainty_handling=fail, rationale_coherence=concern.

Preliminary class: `model_failure`; final: `model_failure`; consequence: material.

Historical context: astra_status=Invalid, fable_status=Conditional, muse_status=Conditional. Classification changed: false. Historical context does not change the independent capability assessment.

### N010 — CLEAR_COLLAPSE

Finds ordinary candidate-cause testing, replay, traces and rollback wholly reducible to the supplied reliability-engineering baseline.

Every locus is absent with direct baseline comparisons. Availability of the route matrix elsewhere in the fixture is not misread as a change made by this procedure. Lossless reduction and CLEAR_COLLAPSE are coherent; no material rule is lost. Historical context confirms the same lossless native reduction; no capability assessment changes.

Dimensions: protocol_compliance=pass, instrument_structure=pass, mechanism_reasoning=pass, warrant_reasoning=pass, native_baseline_use=pass, uncertainty_handling=pass, rationale_coherence=pass.

Preliminary class: `none`; final: `none`; consequence: none.

Historical context: astra_status=CLEAR_COLLAPSE, fable_status=CLEAR_COLLAPSE, muse_status=CLEAR_COLLAPSE. Classification changed: false. Historical context does not change the independent capability assessment.

### N006 — CLEAR_COLLAPSE

Recognizes an explicit claims/source matrix as bookkeeping; it retains native R1 selection and ordinary corroboration.

The response distinguishes a table from a changed acquisition rule. It accurately observes unchanged evidence, warrants, decomposition and next inquiry, and does not assign departure because the representation is systematic. CLEAR_COLLAPSE is supported by the actual procedure. Historical context preserves the same bookkeeping-only distinction and unchanged R1 acquisition; no assessment changes.

Dimensions: protocol_compliance=pass, instrument_structure=pass, mechanism_reasoning=pass, warrant_reasoning=pass, native_baseline_use=pass, uncertainty_handling=pass, rationale_coherence=pass.

Preliminary class: `none`; final: `none`; consequence: none.

Historical context: astra_status=CLEAR_COLLAPSE, fable_status=CLEAR_COLLAPSE, muse_status=CLEAR_COLLAPSE. Classification changed: false. Historical context does not change the independent capability assessment.

### N001 — CLEAR_COLLAPSE

Recognizes the anomaly catalogue and matrix as ordinary manuscript comparison without a new evidence or stopping rule.

The actual procedure only catalogs visible variants and applies ordinary disconfirmation. Gemini does not confuse the micro-probe available in the general fixture with a probe used by this procedure. Its lossless-reduction argument is well grounded in the specified manuscript baseline. Historical context preserves the same distinction between cataloguing visible evidence and actively eliciting underlayer evidence; no assessment changes.

Dimensions: protocol_compliance=pass, instrument_structure=pass, mechanism_reasoning=pass, warrant_reasoning=pass, native_baseline_use=pass, uncertainty_handling=pass, rationale_coherence=pass.

Preliminary class: `none`; final: `none`; consequence: none.

Historical context: astra_status=CLEAR_COLLAPSE, fable_status=CLEAR_COLLAPSE, muse_status=CLEAR_COLLAPSE. Classification changed: false. Historical context does not change the independent capability assessment.

### N002 — SUFFICIENT_DEPARTURE

Preserves a modest minimax record-selection departure: the fixed rule forces R3 instead of the baseline discretionary R1.

The supplied finite dictionary makes the rule operational, not merely notation. Gemini locates the linked action/next-inquiry consequences without requiring changes to all five loci, and correctly leaves observables, warrant and decomposition native. Its optimality language is justified only within the stipulated account set and objective; the response context supplies that scope. Returning to ordinary authentication does not erase this material departure. The models retain the same binding R3 selection rule while allocating its consequences differently: Gemini treats observables as native; Fable marks that locus uncertain because a different record is acquired. This is coherent locus-level variation within the protocol, with the modest material departure preserved.

Dimensions: protocol_compliance=pass, instrument_structure=pass, mechanism_reasoning=pass, warrant_reasoning=pass, native_baseline_use=pass, uncertainty_handling=pass, rationale_coherence=pass.

Preliminary class: `none`; final: `legitimate_reasoning_variation`; consequence: none.

Historical context: astra_status=SUFFICIENT_DEPARTURE, fable_status=SUFFICIENT_DEPARTURE, muse_status=SUFFICIENT_DEPARTURE. Classification changed: true. The models retain the same binding R3 selection rule while allocating its consequences differently: Gemini treats observables as native; Fable marks that locus uncertain because a different record is acquired. This is coherent locus-level variation within the protocol, with the modest material departure preserved.

### N004 — CLEAR_COLLAPSE

Rejects the micro-probe as ordinary because the instrument and its controls are supplied in the shared target evidence.

The fixture supplies access and probe behavior to every procedure, not a stipulation that control-checked active micro-probing is ordinary for the baseline scholar. Ordinary reading explicitly cannot reveal the underlayer. Gemini treats a supplied instrument manual as the native baseline and calls its localized response already provided, overlooking the action that elicits otherwise invisible evidence. A defensible uncommon-native interpretation would need baseline reasoning and preserved uncertainty; the gate expressly says plausible uncertainty keeps. Instead it asserts lossless reduction, no uncertainty and CLEAR_COLLAPSE based on availability. That reasoning violates baseline control and the permissive uncertainty rule. The failure is the rationale, not disagreement with a historical status. The broad manuscript baseline does leave room to argue that an assay is an uncommon native method. Historical Astra/Fable explicitly preserve that uncertainty; the earlier Muse review conservatively treated its baseline-boundary interpretation as ambiguity, and that published assessment is unchanged. Gemini instead uses availability in the shared fixture as the decisive native-reduction argument and returns no uncertainty. The present failure assessment is rationale-specific, not a requirement to reproduce BORDERLINE_KEEP. N004 remains a contestable individual assessment: treating it as ambiguity instead would not remove the repeated independent warrant failures in E006, E022 and E030.

Dimensions: protocol_compliance=pass, instrument_structure=pass, mechanism_reasoning=pass, warrant_reasoning=pass, native_baseline_use=fail, uncertainty_handling=fail, rationale_coherence=concern.

Preliminary class: `model_failure`; final: `model_failure`; consequence: material.

Historical context: astra_status=BORDERLINE_KEEP, fable_status=BORDERLINE_KEEP, muse_status=CLEAR_COLLAPSE. Classification changed: false. Historical context does not change the independent capability assessment.

### N009 — SUFFICIENT_DEPARTURE

Identifies joint offset/gap assignment across overlaps and a discriminating anchor check as coordinated material departure.

The baseline permits ordinary pattern comparison but does not assume quantitative long-sequence alignment. Gemini identifies the actual global consistency, gap handling and targeted-check constraints and preserves residual uncertainty. It slightly overstates the anchor rule as information-maximizing: the packet requires a check where alternatives differ, not a proof of global optimization. That wording does not change the supplied operational distinction or the keep decision; it is a minor rationale precision concern, not a demonstrated systematic failure. The models agree that coupled offset/gap alignment is material but allocate its implications differently. Gemini marks all five loci present, while historical assessments sometimes treat anchor selection or warrant as native or uncertain. Its central operational distinction survives those reasonable allocations. Its information-maximizing phrasing remains a minor precision concern, not a separate failure.

Dimensions: protocol_compliance=pass, instrument_structure=pass, mechanism_reasoning=pass, warrant_reasoning=pass, native_baseline_use=pass, uncertainty_handling=pass, rationale_coherence=concern.

Preliminary class: `none`; final: `legitimate_reasoning_variation`; consequence: minor.

Historical context: astra_status=SUFFICIENT_DEPARTURE, fable_status=SUFFICIENT_DEPARTURE, muse_status=SUFFICIENT_DEPARTURE. Classification changed: true. The models agree that coupled offset/gap alignment is material but allocate its implications differently. Gemini marks all five loci present, while historical assessments sometimes treat anchor selection or warrant as native or uncertain. Its central operational distinction survives those reasonable allocations. Its information-maximizing phrasing remains a minor precision concern, not a separate failure.


## Muse qualification failure pattern versus Gemini findings

Gemini reproduces the substantive Muse warrant failure in E006: survival of irregular-process hypotheses is accepted as a warrant for irregularity. It reproduces E022: execution conditions leave the response-shape-to-mechanism/location inference unsupported. It reproduces E030: ledger continuity and reconstruction controls do not establish the claimed assembly history; Gemini returns Valid where Muse returned Conditional. These are descriptive comparisons made after the independent decision. Both candidates also distinguish formalization-only cases from the modest N002 and strong N009 departures. The contract meaningfully separates competent formatting/protocol execution from missed epistemic warrants, but these two failed candidates do not demonstrate discrimination between an eligible and an ineligible implementation. This result supports neither a general model ranking nor an inference that matching an historical answer is sufficient.

This secondary comparison follows the independently formed Gemini decision. Neither
matching historical models nor differing from Muse qualifies a candidate. No general
model ranking, global intelligence claim, numeric cutoff or consensus score is implied.

## Verification, implications and limitations

All 384 tests across 37 checks passed, including 32 v0.2 tests. The live-credential
scan found no secret in 2,290 artifacts; sanitized evidence is in review/secret-scan.json.
All relevant historical/new suites and verifiers are recorded in review/verification.json,
with reports written only into v0.2. Historical files, including both prior qualifications,
are hash-preserved. Historical policy-sensitive checks run before any authorized current
policy update. The unrelated untracked handoff remains untouched.

Qualification: not_qualified. Do not designate Gemini as the current qualified Family B; MODEL-POLICY.md remains unchanged. Inspect the repeated warrant failure pattern before selecting candidate #3. Experiment F remains deferred and was not run.

Twelve purposively selected cases and one sample per case do not estimate population accuracy or reliability. The preview identifier is not an immutable served snapshot. High thinking and Standard are explicit serialized settings accepted by the API; internal execution and undisclosed retries cannot be independently inspected. Human review is qualitative, and the handoff disclosed selected historical findings before measurement; packets and provider calls remained isolated. E010/E014 expose a prospective-protocol boundary, and N004 is a contestable rationale-level assessment. Reclassifying N004 as ambiguity would not alter the repeated warrant-based decision. Costs are metadata-based estimates, not an invoice. No conclusion about broader model intelligence or performance outside this frozen contract is warranted.

Stop after this qualification. No Experiment F, resumed E, new mapping, changed
anti-collapse, diversity filtering, grounding or retrieval integration was executed.
