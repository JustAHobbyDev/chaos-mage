# Model-agnostic capability qualification v0.1

**Qualification: `not_qualified`.** Muse Spark 1.3 Contributor reliably produced
structured judgments and demonstrated several relevant reasoning capabilities, but
repeatedly accepted a stronger target inference than the supplied signal warrants.
E006, E022 and E030 exhibit this pattern across different source mechanisms. This
checkpoint does not authorize Muse as Family B for Experiment F.

The decision answers whether Muse can instantiate the frozen protocols without a
systematic disqualifying failure. It is not derived from agreement with historical
models. No historical model is ground truth, no consensus answer was synthesized,
and historical experiment interpretations remain unchanged.

## Frozen checkpoints and provenance

| Checkpoint | Commit |
|---|---|
| Starting current origin/main | `b436f2e75f5fe4088b650b3901d4a5bca730351b` |
| Model-agnosticism principle and capability contract | `1f51578aff8f8409b9a3c297a86ed84f8e6d7ee1` |
| Manifest, packets, order, schemas and Muse adapter | `c1b18e0b36c2cc8b42ca725a06efd3478e100ddd` |
| Explicitly authorized credential environment loader | `a7631c8953b8a4acb6387823fe9d4502f1da50ac` |
| Successful provider preflight | `a9b73f020f51bb8fa73ba73a707a5ecc54dc2b65` |
| All twelve primary judgments | `746c550e61af163a0be5391c4e8629ccb23e6a5a` |

The completion commit contains this report, the case reviews, metrics, tests,
verification records and current model-policy status. Its SHA is reported in the
publication handoff; a commit cannot embed its own content-derived SHA.

Measurement ran sequentially from 2026-09-30 03:10:38 to 03:26:50 UTC
(2026-09-29 in America/Chicago). The complete results inventory was written at
03:26:59 UTC and committed before historical outcomes were loaded for comparison.
[Review binding](../model-qualification-v0.1/review/start.json) records the subsequent
qualitative-review start and results commit.

## Architectural principle and capability contract

The frozen [model-agnosticism principle](../../docs/MODEL-AGNOSTICISM.md) states that
Chaos Mage is model-agnostic above a minimum reasoning and protocol-competence
threshold. The harness owns the five-field instrument representation, transfer
validity, anti-collapse, schemas, baselines and experimental controls; models
instantiate reasoning within them. Agreement is diagnostic evidence of robustness,
not a prerequisite for eligibility. Agnosticism does not imply interchangeability.

The [capability contract](../model-qualification-v0.1/CAPABILITY-CONTRACT.md) requires:
protocol compliance; instrument-structure reasoning; mechanism preservation;
evidential-warrant reasoning; execution/epistemic-validity separation; native-baseline
respect; anti-collapse competence; bounded uncertainty; and inspectable rationale.
Eligibility is decided from coherent performance and repeated failure patterns, not
a percentage threshold. A single controversial judgment cannot disqualify a model.

Permanent disagreement classes are ontology/specification ambiguity, legitimate
reasoning variation, and model failure; `none` records cases without a material
review disagreement. Only model failure directly argues against eligibility.
Every experiment must retain requested/returned identifiers and provider configuration.
The current [model-policy status](../../docs/MODEL-POLICY.md) preserves historical
Astra/Fable provenance and records this candidate's outcome without declaring a
Family-B transition.

## Exact twelve-case manifest

The complete [manifest](../model-qualification-v0.1/manifest.json) contains each
source case, source commit, input/classifier/canonical-schema path and SHA-256,
historical freeze path/hash, both historical response paths/hashes, copied packet
path, and masking declaration. All twelve cases resolved without substitution.

| Qualification ID | Judgment | Source experiment | Source commit |
|---|---|---|---|
| E003 | transfer_validity | Experiment E recovery | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| E010 | transfer_validity | Experiment E recovery | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| E014 | transfer_validity | Experiment E recovery | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| E006 | transfer_validity | Experiment E recovery | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| E022 | transfer_validity | Experiment E recovery | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| E030 | transfer_validity | Experiment E recovery | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| N010 | anti_collapse | Experiment D | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` |
| N006 | anti_collapse | Experiment D | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` |
| N001 | anti_collapse | Experiment D | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` |
| N002 | anti_collapse | Experiment D | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` |
| N004 | anti_collapse | Experiment D | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` |
| N009 | anti_collapse | Experiment D | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` |

E comes from `distance/anti-collapse-natural-recovery-v0.1`; D comes from
`distance/anti-collapse-v0.1`. Original classifier, schema and complete packet bytes
match their historical commits and both families' frozen measurement reservations.
D's embedded baseline and neutralized procedures were copied without rewriting.
The validity classifier is historical v0.3, not prospective Experiment F taxonomy.

No coverage-intent descriptions, historical labels, capability-contract text or
operator rationales were added to judge packets. Source-response hashes were checked
before measurement without decoding their judgments. Historical outcomes were loaded
only through the complete-results gate after commit `746c550`.

Frozen execution order:
`E030 → N004 → E006 → N001 → E003 → N009 → E022 → N010 → E014 → N006 → E010 → N002`.
The order was randomized within strata with a recorded seed, then alternated between
validity and anti-collapse; the reproducibility test checks that algorithm and seed.

## Muse identity, configuration and Contributor data use

- Requested: **`muse-spark-1.3-contributor`**.
- Returned on both artificial probes and all twelve judgments:
  **`muse-spark-1.3-contributor`**. Exact matches were enforced; no fallback.
- Provider: Meta Model API, API path version **v1**;
  `https://api.meta.ai/v1/chat/completions`, with catalog discovery at `/v1/models`.
- Client: Python standard-library `urllib.request`, **Python 3.14.7**;
  canonical validator: **jsonschema 4.23.0**. Full build string is in
  [execution-config.json](../model-qualification-v0.1/execution-config.json).
- Reasoning effort: **high**. Temperature, seed, top-p and output-token limit were
  unset/provider defaults. No post-result setting or prompt change.
- Response ID, creation time, usage and whitelisted HTTP metadata were captured.
  System fingerprint was null; no immutable served snapshot was exposed. The returned
  alias does not prove immutable model weights.
- Tier: **Contributor**. This tier permits training use of prompts/completions.
  Only public/synthetic project material was submitted; no private user material
  was added. Provider documentation was checked before measurement:
  [model tiers](https://dev.meta.ai/docs/models),
  [structured output](https://dev.meta.ai/docs/structured-output), and
  [chat-completion isolation](https://dev.meta.ai/docs/protocols/chat-completions).
- Credential source to the runner: **environment**. The user explicitly authorized
  `bws-4-agents` to fetch only `META_API_KEY`; a local launcher loaded the protected
  file into the environment and removed the file before provider execution.
  No secret value was printed, passed on argv, or stored in evidence.

The first credential-helper attempt failed inside the filesystem sandbox before any
provider reservation or request. The identical command succeeded with approved
sandbox escalation. This was credential preparation, not a failed provider judgment
or measurement retry. The existing shared incident was updated with sanitized facts.

## Structured-output compatibility and isolation

Native JSON-schema output used `strict: true` and the pre-frozen historical structural
projection. It removes `$schema`, `$id` and conditional `allOf` from the wire schema,
while preserving semantic fields, enums, required structure, null semantics and
other constraints. Every decoded result was validated against the **unchanged full
canonical schema** and historical cross-field contracts. No semantic repair,
formatting retry or relaxed acceptance rule was used.

The authenticated catalog and two artificial formatting fixtures established exact
model availability and compatibility with both schemas. Both probes had separate
processes, requests, session IDs and empty temporary working directories. Their
successful evidence was committed before the first real case.

The [execution audit](../model-qualification-v0.1/review/execution-audit.json) and
independent completion tests establish twelve sequential primary requests, fourteen
unique process/session/working-directory records including the two probes, exact
packet and wire-schema delivery, raw-content-to-response equality, model identity,
and results/preflight commit ordering. Each model request contained one user message
and one schema, with no history or repository context. Tools, retrieval, browsing,
plugins, connectors and memory were not supplied. Provider-internal operations and
hidden retries remain unobservable; harness retries were zero.

Fresh provider calls: Muse **12 primary + 2 artificial probes**; Astra **0**;
Fable **0**. No Claude usage was purchased. No Experiment F execution, E resumption,
new generation, new natural-output anti-collapse, grounding or retrieval occurred.

## Mechanical results

| Measure | Count |
|---|---:|
| Requested/planned primary judgments | 12 |
| Attempted primary judgments | 12 |
| Successful primary judgments | 12 |
| Provider failures | 0 |
| Canonical-schema failures | 0 |
| Malformed primary outputs | 0 |
| Valid | 2 |
| Conditional | 4 |
| Invalid | 0 |
| CLEAR_COLLAPSE | 4 |
| SUFFICIENT_DEPARTURE | 2 |
| BORDERLINE_KEEP | 0 |
| Anti-collapse keep | 2 |
| Anti-collapse reject | 4 |

After the results freeze, raw status matched both historical models in **6** cases,
one in **5**, and neither in **1**. These are descriptive counts only. They are
neither accuracy estimates nor the qualification rule.

## Case-level review and historical context

CC = CLEAR_COLLAPSE; SD = SUFFICIENT_DEPARTURE; BK = BORDERLINE_KEEP.
Full rationale, seven capability dimensions, scope notes and downstream consequence
are in [case-reviews.json](../model-qualification-v0.1/review/case-reviews.json).

| Case | Muse | Historical Astra | Historical Fable | Review class | Consequence |
|---|---|---|---|---|---|
| E003 | Valid | Valid | Valid | none | none |
| E010 | Conditional | Conditional | Valid | ontology_specification_ambiguity | minor |
| E014 | Conditional | Valid | Conditional | ontology_specification_ambiguity | minor |
| E006 | Valid | Invalid | Valid | model_failure | material |
| E022 | Conditional | Invalid | Conditional | model_failure | material |
| E030 | Conditional | Invalid | Conditional | model_failure | material |
| N010 | CC | CC | CC | none | none |
| N006 | CC | CC | CC | none | none |
| N001 | CC | CC | CC | none | none |
| N002 | SD | SD | SD | legitimate_reasoning_variation | none |
| N004 | CC | BK | BK | ontology_specification_ambiguity | material |
| N009 | SD | SD | SD | legitimate_reasoning_variation | none |

Counts: **3 model_failure**, **3 ontology/specification ambiguity**, **2 legitimate
reasoning variation**, **4 none**. Same final status does not rule out variation in
reasoning; agreement with one historical model does not exonerate a concrete failure.
No replacement “correct” judgment is generated by this review.

### Every model-failure case

**E006 — surviving hypotheses become a factual irregularity conclusion.** The
mapping says that if H1 and H3 survive, the defensible statement is that the process
was irregular. Their survival alone does not eliminate regular-process, structural-
advantage or evidence-artifact alternatives, and survival is not itself corroboration
even if the reported set is restricted. Muse explicitly endorses the H1/H3 statement
while claiming the survival-not-proof limit is preserved. It supplies no independent
warrant for the categorical irregularity conclusion. This is a concrete failure to
inspect a particular inference amid an otherwise competent ACH summary.

**E022 — response dynamics become delay localization.** A downstream stage can
respond late to a step because delay occurred upstream while contributing little
local waiting. Clean timestamps, repeated controlled steps and known initial states
do not equate response dead time with local accumulated delay. The mapping's rule
that delay accumulates where dead time or settling is longest omits that bridge.
Its temporary overshoot interpretation can also coexist with eventual total-delay
reduction. Muse accepts these translations and lists execution conditions instead
of detecting the warrant issue. Direct waiting observations could help investigate
it, but the supplied rule does not require that discriminating check; the judge
cannot silently amend the mapping.

**E030 — continuous handling becomes unchanged arrangement.** A fully documented,
truthful ledger can include post-author sorting or rebinding. Continuity then accounts
for changed arrangement rather than supporting the claim that the examined arrangement
is the author's. Muse summarizes the claim as safer provenance/sequence support and
asks for execution and independent corroboration, missing this explicit stronger
inference. Reliability and non-circularity checks do not fix the logical distinction.

These diagnostics arise from the supplied mechanisms and claims, not a historical
vote. Fable shares Muse's final status in each case; that context does not establish
that Muse satisfies the frozen instruction to detect unsupported inferences. The
historical experiments and their published interpretations have not been revised.

### Every ontology/specification ambiguity

**E010:** the procedure checks timestamp meaning and retains alternatives. The
protocol also permits Conditional for identifiable missing measurements. Whether
those checks are execution prerequisites or unresolved validity conditions remains
ambiguous. Muse names concrete checks and does not declare the procedure Invalid.

**E014:** Muse understands partition, trace separation and omission/restoration
corroboration, but conditions validity on future specification and observations.
The boundary between a valid proposed method and an empirically instantiated method
is unsettled in v0.3. This is not grounds to impose the proposed F taxonomy retroactively.

**N004:** controlled assay may exceed ordinary material inspection, but the supplied
baseline does not precisely define that boundary. Muse reads it broadly and rejects;
it also acknowledges boundary uncertainty while asserting lossless replacement by
close inspection. The otherwise invisible, control-checked signal makes this a
material permissive-uncertainty concern. Conservatively, this review classifies the
case as specification ambiguity, not an additional model failure or evidence of a
systematic suppression tendency. A separately authorized specification revision
should clarify assay scope; no patch or rerun occurs in v0.1.

### Representative legitimate reasoning variation

**N002** retains the single worst-case-discrimination rule: the one allowed request
changes from R1 to R3, reducing the worst-case surviving set from two accounts to one.
Muse marks the observable type unchanged; Fable leaves that locus uncertain. A changed
record can be treated as a consequence of selection without positing a new evidence
kind. The decisive modest operational change is preserved.

**N009** retains joint offset/gap construction and global consistency filtering.
Muse allocates the departure to action, observables and decomposition while treating
the bounded inferential license and follow-up type as ordinary. Its formalization
field still states the global constraint and discriminating anchor choice. Historical
judges assign some of this departure to warrant or next inquiry. This is defensible
allocation of the same preserved operations, with the same keep decision.

## Capability findings and decision

**Protocol compliance:** 12/12 primary responses and both artificial probes obeyed
the mechanical contracts. Returned statuses are cross-field schema-consistent.
Substantive compliance concerns remain where unsupported inference should dominate
otherwise preserved procedure; schema success alone cannot qualify a model.

**Instrument structure:** E003 and the other validity rationales consistently identify
state, operation, signal, inference and limit. D packets are deliberately source-neutral,
so direct original-source fidelity is not tested there. Strong structure recognition
coexists with errors in the inferential link.

**Mechanism preservation:** Muse preserves dechallenge/rechallenge, differential
comparison, checkpoint partition and joint alignment at a useful descriptive level.
It does not equate exotic vocabulary with departure. E006/E022/E030 nevertheless
lose or soften a decisive source-to-target warrant while reporting preservation.

**Warrant reasoning:** this is the disqualifying pattern. Broad caution and recognizable
procedure receive credit while a particular stronger target conclusion escapes scrutiny.
E022/E030 turn the issue into future execution or corroboration; E006 declares no
unresolved warrant. The repetition across three distinct mechanisms is sufficient
qualitative evidence for this checkpoint, without a numerical failure threshold.

**Native baseline and anti-collapse:** N010 is correctly understood as ordinary
candidate-cause diagnosis; N006 and N001 are recognized as formalization-only in two
contexts. N002 demonstrates that Muse can preserve a modest single-rule departure
when most work remains native. N009 preserves a coordinated departure. N004 exposes
a baseline-boundary concern. There is no evidence here of systematic formalization
promotion, superficial terminology reward, or general modest-departure suppression.

**Uncertainty:** Muse uses specific Conditional conditions and preserves limits in
several rationales. E003 and E006 being Valid show that it does not collapse every
unexecuted procedure into invalidity. E010/E014 expose specification sensitivity;
N004 does not demonstrate the desired permissive uncertain keep behavior. No case
returned BORDERLINE_KEEP. This small set does not establish broad calibration.

**Inspectable rationale:** the outputs are concrete enough to diagnose both strengths
and failures. The concern is not opaque labels; it is that detailed summaries can
omit or normalize the operative inference defect. Mechanical consistency is not
substantive warrant adequacy.

**Decision: `not_qualified`.** The three repeated warrant failures make Muse unsuitable
as a qualified research implementation under this frozen configuration and v0.1
contract. This is not a universal claim about Muse or a judgment based on minority
labels. The positive anti-collapse and protocol findings remain part of the record.

## Verification, preservation and limits

The read-only suite passed **327 tests across 32 verification commands**, including
historical tests and private-archive completion verifiers, plus qualification tests.
[verification.json](../model-qualification-v0.1/review/verification.json) records exact
commands and outputs. New completion tests independently recompute distributions,
request delivery, response identity, isolation and commit ordering.

The initial historical test run caught a new policy link added to the root README,
which is frozen by an older preparation inventory. The original bytes were restored;
the new policy stays in separate documents. The initial failed attempt is retained
in [verification-attempt-1.json](../model-qualification-v0.1/review/verification-attempt-1.json).
This restoration changed no qualification packet, classifier, schema, provider setting
or judgment. Final historical preservation includes every pre-existing tracked file,
including the root README. The untracked prospective-validity handoff remains untouched.

Limitations: twelve deliberately selected cases, one response each, no estimate of
population-wide reliability; qualitative operator review without an adjudicator;
three unresolved specification boundaries; unknown immutable served snapshot and
provider-internal behavior; no demonstrated BORDERLINE_KEEP in this sample. The
frozen packet text, raw responses, structured rationales and review counterexamples
make the assessment inspectable. No prompts or settings were optimized after results.

## Implications for Experiment F and next work

Do not begin Experiment F with Muse as Family B. No Family-B transition is declared.
Historical Family A remains OpenAI GPT-6 Astra and historical Family B remains Claude
Fable 5.1 in their original records. No new Fable judgments or credits were used.

Recommend testing another sufficiently capable candidate under a separately authorized
qualification, and separately clarifying the documented protocol boundaries. Do not
automatically choose a model, tune Muse to these cases, rerun v0.1, revise F's
prospective design, or pool historical Fable and Muse agreement statistics. This
handoff stops at the qualification checkpoint.
