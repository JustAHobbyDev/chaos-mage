# Gemini 3.1 Pro capability qualification v0.1

**Qualification: `qualification_inconclusive`.** No primary judgments were collected.
The first artificial probe returned successfully; a defect in the frozen harness's
billing-tier check stopped scheduling. This is no evidence for or against Gemini's
reasoning competence. No replacement Family B is declared.

## Provenance and checkpoints

- Starting SHA: `cb5ac745d4326bc6a097411b819c14563ae28c80` (local and remote matched).
- Preparation: `1d14a978af71f46410da290480d6fb04ebee702b`.
- Partial preflight/result evidence freeze: `58267d7374cece69f992c832a644599dff9d680a`.
- Successful preflight checkpoint: absent.
- Twelve-judgment result checkpoint: absent.
- Completion commit: the commit introducing this report, reported separately to avoid a self-reference.
- Contract original freeze: `1f51578aff8f8409b9a3c297a86ed84f8e6d7ee1`.
- Contract SHA-256: `21b2ce7aeda5eef39175eb838f31f148afa7339e8fe02719c6ea1a2bf7acf31a`.

The contract, historical qualification, D/E experiments, model-agnosticism principle,
and model policy remain unchanged. The unrelated untracked handoff is untouched.
The complete provenance manifest carries each source input, source freeze, classifier,
canonical schema, prior packet, and historical-output hash. Historical outputs were
hash-verified only; their judgments and reviews were not decoded for comparison.
The handoff's explicit complete-freeze embargo takes precedence over its read-first list.

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

Every copied packet matches the prior qualification byte-for-byte. Coverage is six
validity and six anti-collapse cases. None was submitted to Gemini. Randomized
interleaved order was frozen before the artificial probe and remains unexecuted.

## Provider and artificial preflight

Requested and returned model: `gemini-3.1-pro-preview`.
Native endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent`.
Client: Python standard-library `urllib.request`; exact Python and jsonschema versions
are frozen in execution-config.json and the request reservation. No Google SDK.
Explicit `thinkingConfig.thinkingLevel: HIGH`, `maxOutputTokens: 32768`, temperature
1.0; top-p, top-k and seed unset/provider default. No legacy thinking budget.
The returned preview identifier establishes the requested model alias, not immutable
served weights. Response ID and raw metadata are retained with the artificial response.

The sole request was a synthetic validity formatting fixture in one fresh process,
one user message, an empty working directory, and no history, tools, grounding,
URL context, retrieval, code execution, or other cases. The serialized request and
schema are frozen. Native JSON output used responseMimeType/responseJsonSchema;
wire projection retained the historical structural projection. Offline inspection
confirmed exact fixture equality and full unchanged canonical/cross-field validation.
No response was rewritten. The anti-collapse artificial schema was never tested.

The API returned HTTP 200, finishReason STOP, the exact model ID, and coherent token
counts. It returned usageMetadata.serviceTier as lowercase `standard`. The harness
allowed only uppercase `STANDARD` (or an omitted tier), raising “Unexpected billing
service tier” before extracting the successful structured response. The original
validation artifact retains its generic provider_or_protocol_failure classification;
the audit correctly attributes it to the harness accountant, not the provider or schema.
The defect is in our adapter validation, not the model's response.

The original response is preserved in http-body.json, including opaque thought
signature metadata. No thought signature or history was replayed. High thinking was
explicitly serialized and accepted; internal execution cannot be independently inspected.
The response reports thinking tokens, not access to private reasoning.

A credential-helper sandbox failure preceded all reservations. The identical
launcher succeeded with approved escalation; this was credential setup, not an API
retry. Credential source: environment. Temporary helper file removed before the call;
no secret in argv, request artifacts or errors. A live-key artifact scan passed.

## Mechanical counts and cost

| Measurement | Count |
|---|---:|
| Planned primary judgments | 12 |
| Attempted primary judgments | 0 |
| Successful primary judgments | 0 |
| Planned artificial probes | 2 |
| Attempted artificial probes | 1 |
| Successful preflight sequences | 0 |
| HTTP-successful artificial responses | 1 |
| Offline canonical-valid artificial responses | 1 |
| Provider failures | 0 |
| Schema failures | 0 |
| Harness accounting failures | 1 |
| Retries / fresh historical-model calls / Experiment F calls | 0 |

All usage below belongs to the artificial probe; primary usage is zero:

- Input: 154 tokens.
- Candidate output: 112 tokens.
- Thinking: 652 tokens.
- Billable output including thinking: 764 tokens.
- Total: 918 tokens.
- Estimated experiment cost: **$0.009476**; ceiling **$2.00**.

Standard pricing checked 2026-09-29: $2/M input and $12/M output including thinking
at this context length ([Google pricing](https://ai.google.dev/gemini-api/docs/pricing)). Estimate:
`154 × 2 / 1,000,000 + (112 + 652) × 12 / 1,000,000 = 0.009476 USD`.
This is an offline estimate, not an invoice or a successful execution-ledger update.
The frozen scheduler conservatively retains its unresolved $0.407658
reservation; its stop has not been cleared. No double counting of thoughts.

Validity, anti-collapse and keep/reject distributions are **unmeasured**, represented
as null rather than fabricated results. Historical raw-status matching is unmeasured.
Model-failure/ambiguity/variation counts and case IDs are unassessed, not zero findings.

## Capability findings and Muse comparison

There are no Gemini primary judgments and no case-level capability findings.
E006, E022 and E030 warrant reasoning are unmeasured. N001/N006 formalization,
N002 modest departure, N004 uncertainty and N009 coordinated departure are likewise
unmeasured. E003/E010/E014 and N010 are also unmeasured. No historical comparison,
majority vote, consensus score, or accuracy-against-model calculation was performed.

The operator handoff disclosed Muse's warrant failure pattern in E006/E022/E030.
That context was excluded from the artificial request and all frozen Gemini packets.
No Muse judgments or case reviews were opened. Whether Gemini reproduces any of
those failures is unknown. This stopped run cannot establish whether the capability
contract discriminates between these candidates; it supplies provider/harness
compatibility evidence only. No systematic Gemini pathology can be assessed.

## Verification, limitations and next step

Offline qualification tests, partial-evidence tests, the Gemini preparation verifier,
and the historical Muse hash/provenance verifier are recorded in review/verification.json.
All original tracked bytes are preserved. Completion/semantic historical suites remain
gated because they decode judgments, and the required twelve-result freeze does not
exist. They are explicitly deferred, not claimed as passing. No historical verifier
was allowed to overwrite its frozen report.

Publish this partial result as **qualification_inconclusive**. Leave MODEL-POLICY.md
unchanged. Before Experiment F, a separately authorized attempt must correct and test
the service-tier representation handling and establish both artificial schemas.
The present v0.1 adapter, request and stop remain frozen. Do not repair-and-continue,
retry the probe, run a primary judgment, choose another candidate, or execute F here.

Limitations: no capability evidence; incomplete preflight; untested anti-collapse wire
compatibility; alias-only served identity; estimated rather than invoiced billing;
provider-internal retries are not observable. The 32768-token cap and $2 guard have
only offline test coverage plus one low-consumption artificial response.
