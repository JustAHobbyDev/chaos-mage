# Gemini capability qualification — frozen v0.1

Starting commit: cb5ac745d4326bc6a097411b819c14563ae28c80. The capability contract
is copied byte-for-byte from the Muse qualification, originally frozen at
1f51578aff8f8409b9a3c297a86ed84f8e6d7ee1. No historical experiment is edited.

## Same experiment, substituted candidate

The exact twelve packets, source commits, classifiers, and canonical schemas are
bound by manifest.json. Six Experiment E validity cases: E003, E010, E014, E006,
E022, E030. Six Experiment D anti-collapse cases: N010, N006, N001, N002, N004,
N009. Packet bytes must match the prior qualification. Only that packet and the
wire schema reach Gemini: no coverage intent, operator commentary, capability
rubric, historical labels, other judgments, repository context, or prior messages.
The exact native baseline and source-neutral procedure remain inside each D packet.

The historical structural schema projection removes $schema, $id, and allOf only.
All fields, enums, requiredness, nullable types, and remaining constraints survive.
Full canonical Draft 2020-12 and historical cross-field validation follow decoding.
Unsupported wire compatibility causes a stop; no schema relaxation or semantic repair.

## Gemini API and identity

Python standard-library urllib.request calls the native v1beta generateContent
endpoint for gemini-3.1-pro-preview only. Explicit thinkingLevel HIGH, no legacy
thinking budget, temperature 1.0, maxOutputTokens 32768, other sampling defaults
unset and recorded. No SDK retries, HTTP redirects, fallback, tools, grounding,
URL context, code execution, function calls, retrieval, or explicit caching.
One response candidate is required; only STOP completion is accepted. Raw response
metadata and returned modelVersion are retained. This frozen adapter requires the
exact returned preview identifier; mismatch or absence stops, never substitutes.
A returned preview alias does not prove immutable weights. Internal provider retry
activity may be unobservable; no claim of zero hidden retries is made.

Credentials are loaded solely via the authorized bws-4-agents GEMINI_API_KEY helper
into the environment. Its private temporary file is consumed internally and deleted
before provider calls. No key in argv, URL, request JSON, logs, errors, or fixtures.
Credential-reflecting responses are withheld. Sanitized provenance: environment.

## Cost and request budget

At most two artificial format probes, one per schema, and twelve primary requests.
The same configuration applies to both. An artificial fixture contains no real case.
Authentication, exact model, high thinking, schema compatibility, canonical validation,
usage, and isolation must succeed on both probes. No separate catalog inference.

Standard paid pricing checked 2026-09-29: $2/M prompt and $12/M response plus
thinking tokens at <=200k prompt tokens; $4/M and $18/M above that threshold.
No cache discount assumed. Source: https://ai.google.dev/gemini-api/docs/pricing .
Usage fields promptTokenCount, candidatesTokenCount, thoughtsTokenCount must sum
to totalTokenCount. Missing, negative, inconsistent, unexpected-tier or tool usage
stops scheduling. Raw metadata is retained even when reconciliation fails.

Before sending, reserve input cost for serialized request UTF-8 byte length plus
4096 overhead tokens and output cost for all 32768 allowed tokens. This is a
conservative estimate, not a tokenizer count or invoice. The documented output cap
includes thinking: https://ai.google.dev/gemini-api/docs/generate-content/thinking .
Cumulative observed cost plus the next reservation must not exceed $2.00. Actual
usage replaces a reservation; sent requests with unknown charges retain it. Observed
bound violations stop immediately. Budget stops leave incomplete qualification;
never shrink the cap, change reasoning, or rerun a case to complete within credit.

## Freeze sequence and isolation

1. Commit preparation, copies, manifest, randomized alternating-strata order,
   provider adapter, configuration, schemas, fixtures, pricing, and tests.
2. Run two artificial probes, then commit successful preflight and its inventory.
3. Run the frozen order sequentially, one case in each fresh process/request and
   empty temporary working directory. Exclusive reservations prevent repeated samples.
4. Commit all twelve results and a complete freeze inventory before semantic review.
5. Assess Gemini independently against packet and contract for every case; save a
   write-once preliminary review and preliminary decision before historical decoding.
6. Load historical context only after both gates; explain any classification changes.
   Complete final review and ordinary push. Do not run Experiment F.

The handoff's explicit freeze-before-review rule governs its conflicting read-first
list. Before complete freeze, historical outputs may be hashed but never decoded.
The context already disclosed in the operator handoff is not claimed to be blinded.

Stop on first authentication/provider/timeout/schema/malformed-output/canonical/model/
configuration/usage/budget failure. Preserve request-sent evidence, sanitized failure,
and partial inventory. No automatic recovery, content repair, or retry; partial
freeze does not unlock historical comparison. Report qualification_inconclusive.

## Review

Use unchanged capability dimensions and the four classes: none,
ontology_specification_ambiguity, legitimate_reasoning_variation, model_failure.
Record preliminary and final classes, changed-classification explanation, and
none/minor/material downstream consequence. Inspect every rationale, including
same-status cases. Repeated systematic failure can disqualify; historical agreement
cannot qualify. Final outcomes: qualified, not_qualified, qualification_inconclusive.

Report counts, tokens, estimated costs, status/gate distributions, descriptive
historical status matches, all failure/ambiguity cases and representative legitimate
variation. Discuss warrant, baseline, mechanism, formalization, modest departure,
uncertainty and coordinated departure. Muse's three disclosed failures are secondary
context, never an answer key. No numeric eligibility cutoff or majority vote.

Update current Family B policy only if qualified. No fresh comparison calls, tuning,
Experiment F, resumed E, new mappings, changed anti-collapse, retrieval or grounding.
