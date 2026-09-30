# Model-agnostic capability qualification — frozen v0.1

The [capability contract](CAPABILITY-CONTRACT.md) and
[model policy](../../docs/MODEL-AGNOSTICISM.md) define eligibility. This is a small
diagnostic qualification, not equivalence, accuracy, majority vote, or optimization.

## Inputs and masking

Use precisely E003, E010, E014, E006, E022, E030 from frozen Experiment E
transfer-validity, and N010, N006, N001, N002, N004, N009 from frozen Experiment D
anti-collapse. The abandoned bridge selection is retained. No new cases or rewritten
packets. The manifest binds source commits, input/classifier/canonical-schema hashes,
historical measurement reservations, and copied judge packets. D packets include
the exact baseline and neutralized procedure bytes as historically submitted.

Only the original packet and native structured-output schema reach Muse. Coverage
intent, historical labels/rationales, provider identity annotations, capability
contract, and the operator's interpretation do not enter packets. Pre-measurement
verification may hash historical artifacts and inspect reservation metadata but
must not interpret historical judgments. Historical comparison is gated on twelve
committed Muse results and their committed freeze inventory.

## Provider and compatibility

Only `muse-spark-1.3-contributor` at `https://api.meta.ai/v1` is allowed. No model
fallback. Use direct Python standard-library HTTP, high reasoning, provider-default
temperature/seed/output-token limit, one request and no retry. Record requested and
returned identity, response ID, fingerprint when exposed, usage, endpoint, API v1,
Python/jsonschema versions, settings, and Contributor provenance. An exposed alias
does not establish immutable served weights.

Contributor prompts/completions are training-eligible. Only the public/synthetic
project corpus is included. Credentials come from the environment and are never
printed or written. Any additional credential-loading method needs explicit operator
authorization. Response artifacts are checked for credential reflection.

Native `response_format.json_schema` uses `strict: true`. Reuse the historical
structural projection: remove `$schema`, `$id`, and conditional `allOf` constraints
from the wire schema; preserve every field, enum, required field, nullable type,
and other constraint. Decode without repair; validate the full unchanged canonical
schema and historical cross-field contracts locally. No weakened acceptance rule.
Freeze this projection and artificial fixtures before calls.

Current documentation checked 2026-09-29:
[models](https://dev.meta.ai/docs/models),
[structured output](https://dev.meta.ai/docs/structured-output),
[stateless chat completions](https://dev.meta.ai/docs/protocols/chat-completions).
Authenticated catalog discovery must confirm exact availability. Two artificial
formatting probes, one per schema, must then succeed with matching model identity,
canonical validation, metadata capture, separate processes/requests, and no tools.
Commit successful preflight before any real measurement.

## Collection and failure

Freeze the randomized alternating-stratum order in execution-order.json. Run exactly
twelve planned primary judgments, at most one per case, sequentially. Each uses a
new process, empty temporary working directory, a new request/session identifier,
one user message, no history, repository access, memory, browsing, tools, retrieval,
plugins, connectors, or other cases. The provider receives no local filesystem.

Create exclusive reservations before each call. No repeated sample, semantic retry,
repair, alternate model, fresh Astra/Fable, or adjudicator. Preserve failure category,
HTTP evidence where available, timeout, malformed output, identity mismatch, and
schema failures. Stop scheduling on first failure. Recovery requires explicit
authorization. Missing credentials stop before network use. Publish partial evidence
as inconclusive; do not invent unmeasured findings.

Commit all twelve responses and their inventory before interpreting or loading
historical outcomes. A partial freeze does not unlock historical comparison.

## Review and decision

For each complete case record Muse status/reasoning; historical Astra/Fable status;
disagreement class (`none`, `ontology_specification_ambiguity`,
`legitimate_reasoning_variation`, `model_failure`); capability dimensions
(protocol_compliance, instrument_structure, mechanism_reasoning, warrant_reasoning,
native_baseline_use, uncertainty_handling, rationale_coherence: pass/concern/fail);
downstream consequence (none/minor/material); and rationale. A pass is bounded by
the supplied task; note dimensions not directly exposed by neutralized D packets.
Inspect even same-label cases for failure. Do not synthesize a consensus answer.

Describe requested/successful judgments, schema/provider failures, validity statuses,
anti-collapse statuses and keep/reject counts. After complete freeze, describe raw
status matching both historical models, one, or neither, without accuracy claims.

Review all failure/ambiguity cases, formalization cases, N002 modest departure,
N004 uncertainty, warrant-sensitive validity cases, and any repeated direction of
error. Recommend exactly qualified, not_qualified, or qualification_inconclusive
under the contract. No simple score threshold. Preserve meaningful uncertainty.

No post-result tuning or rerun. Record ambiguity for later specification work or
pathology for a separately authorized candidate. F requires a separate handoff;
no F execution or prospective-design change, resumed E, new mappings, new natural
anti-collapse, grounding, retrieval, or diversity filtering is authorized here.
