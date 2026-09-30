# Family-B instrumentation bridge v0.1 — inconclusive

**Recommendation: `inconclusive`.** Collection stopped during artificial preflight:
Claude Fable returned HTTP 401, reporting an expired OAuth access token. Both Muse
schema probes succeeded. There are **zero fresh primary Fable judgments and zero
fresh primary Muse judgments**. This evidence cannot answer whether changing Family B
would materially change the research instrument. It establishes no compatibility,
strictness, collapse-threshold, or model-equivalence finding.

The failure occurred at 2026-09-30 00:13:56 UTC (2026-09-29 in America/Chicago).
Scheduling stopped immediately. No retry, credential refresh, subscription upgrade,
additional credit purchase, model fallback, historical-response substitution, or
semantic repair was attempted. The second Fable preflight was not scheduled.

## Checkpoints and evidence

| Checkpoint | Commit |
|---|---|
| Verified starting main | `f2fb4ba80a6f35061f10d6a24149fe304d8bde7f` |
| Frozen twelve-case manifest and exact packets | `15dec1ae58b0b35fe29e5267e31ca18ee8a1daab` |
| Prepared adapters, parameters, randomized order and tests | `94b41c94883cb1bd80acdf4ae4e4c072129fbe2c` |
| Frozen partial preflight and failure | `792bf6ccb32ae18ac73d50d7f8fa78f290c38b2b` |
| Successful two-provider preflight | Not reached |
| Complete 24-response freeze | Not reached |

This report belongs to the final publication commit, obtainable with
`git log -1 --format=%H -- distance/review/family-b-bridge-v0.1.md`; a commit cannot
include its own hash. The completion message records that final hash and remote check.

The [manifest](../family-b-bridge-v0.1/manifest.json) records source/input/classifier/
canonical-schema/historical-response paths and SHA-256 values. The
[partial freeze](../family-b-bridge-v0.1/partial-freeze.json) binds every retained raw
runtime artifact, including failed events. [Public preflight evidence](../family-b-bridge-v0.1/preflight/partial.json)
contains the two artificial payloads, configurations, session identities, returned Muse
metadata, and the sanitized Fable error. Raw HTTP bodies and Claude event streams remain
in ignored local runtime storage; their hashes are published. They are not prerequisites
for reading the report, but the private verifier uses them for stronger auditing.

## Exact case manifest

All twelve inputs resolved cleanly. Each copied packet is byte-identical to its frozen
historical packet, including classifier content. Input and schema hashes also match
the historical measurement reservation. Historical Fable response hashes match the
corresponding result freeze; source Git blobs were checked. No case was substituted.

| Bridge/source ID | Judgment | Source experiment | Source result-freeze commit |
|---|---|---|---|
| E003 | Transfer validity | E recovery: anti-collapse-natural-recovery-v0.1 | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| E010 | Transfer validity | E recovery: anti-collapse-natural-recovery-v0.1 | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| E014 | Transfer validity | E recovery: anti-collapse-natural-recovery-v0.1 | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| E006 | Transfer validity | E recovery: anti-collapse-natural-recovery-v0.1 | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| E022 | Transfer validity | E recovery: anti-collapse-natural-recovery-v0.1 | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| E030 | Transfer validity | E recovery: anti-collapse-natural-recovery-v0.1 | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| N010 | Anti-collapse | D: anti-collapse-v0.1 | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` |
| N006 | Anti-collapse | D: anti-collapse-v0.1 | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` |
| N001 | Anti-collapse | D: anti-collapse-v0.1 | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` |
| N002 | Anti-collapse | D: anti-collapse-v0.1 | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` |
| N004 | Anti-collapse | D: anti-collapse-v0.1 | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` |
| N009 | Anti-collapse | D: anti-collapse-v0.1 | `5f79f8bad1e7c46438dc8b026db7c001633ee7cd` |

The manifest additionally records each historical measurement's actual input commit.
The anti-collapse packets retain the exact D baselines and source-neutral procedures.
The validity packets use E's frozen natural mappings and the historical v0.3 rubric.
Historical labels and bridge-design rationales do not enter fresh packets.

## Providers and structured output

| Arm | Requested model | Returned evidence | Client |
|---|---|---|---|
| Fresh Fable | `claude-fable-5-1[1m]` | Runner init says `claude-fable-5-1`; error message model is `<synthetic>`, with empty modelUsage | Claude Code 2.1.283, executable hash pinned |
| Fresh Muse | `muse-spark-1.3-contributor` | Both artificial responses return `muse-spark-1.3-contributor` | Python 3.14.7 standard-library urllib.request; no SDK retry layer |

Fable's init alias is client initialization evidence, **not evidence of a completed
inference or served snapshot**. The synthetic authentication-error message records
zero input/output tokens; its model field is not a served model. Neither arm supplies a verified immutable serving
snapshot. The local validator uses jsonschema 4.23.0. Both planned arms request high
reasoning effort; equal labels do not imply equal compute. Temperature and sampling
seed remain provider defaults. The frozen configuration was not tuned after responses.

Muse uses `https://api.meta.ai/v1/chat/completions`. Its Contributor variant is explicit
provider provenance, absent from classifier content. Official [model documentation](https://dev.meta.ai/docs/models)
lists the exact identifier, and an authenticated `GET https://api.meta.ai/v1/models`
confirmed it for this environment before inference. There was no alternate model or
third-party routing. [Endpoint/model provenance](../family-b-bridge-v0.1/provider/provenance.json)
and [catalog evidence](../family-b-bridge-v0.1/provider/catalog.json) preserve the configuration.

The API credential source is environment. The local credential launcher uses
`bws-4-agents` without printing its value or placing it on argv. No credential is part
of the prompts, public artifacts, raw result metadata, or request-body files. Only the
requested credential was retrieved. The helper initially needed sandbox escalation to
create its protected temporary file; this was resolved before provider calls.

The wire method is the existing D/E structural projection: remove schema identifiers
and conditional `allOf` rules, retain every substantive field, enum, required key, null
alternative, and closed-object boundary. Muse submits it through
`response_format.json_schema` with `strict: true`; Fable uses native StructuredOutput.
All conditional rules remain in the unchanged canonical schemas and are checked locally,
along with historical contract checks. Meta's [structured-output documentation](https://dev.meta.ai/docs/structured-output)
describes the strict subset. Both Muse artificial fixtures passed exact fixture equality
and canonical validation. Fresh Fable schema compatibility remains **unestablished**
because authentication failed; historical support does not replace fresh preflight.

Contributor prompts/completions may be used for provider training. The selected corpus
is the existing public/synthetic project corpus. Only artificial fixtures reached Muse
in this attempt; no confidential material or actual bridge case was submitted.

## Execution and isolation

| Operation | Fable | Muse |
|---|---:|---:|
| Planned primary judgments | 12 | 12 |
| Actual primary judgments/attempts | 0 | 0 |
| Artificial preflight attempts | 1 | 2 |
| Successful artificial responses | 0 | 2 |
| Harness retries | 0 | 0 |

One additional Muse catalog request performed no inference. Each preflight used a
fresh child process and unique session UUID, with an empty temporary working directory.
Muse sent one user message through a stateless HTTP request, with no tools or history.
Fable's frozen D/E flags disable settings context, tools other than StructuredOutput,
hooks, MCP servers, plugins, skills, connectors, memory and session persistence; init
evidence confirmed no external capabilities. The model had no repository access.
Primary measurement isolation remains unexercised because the gate never opened.

The frozen 24-entry order uses seed 2026092901: six shuffled four-entry blocks, each
containing one provider/type combination, with independently shuffled case lists.
No entry was consumed. Exclusive reservations, STOP handling and schema checks were
tested offline. No partial or successful primary response exists. Provider-internal
formatter/transport retries are separate from harness retries; Muse exposes none in
these responses, and unexposed internals remain unknown. Fable failed before usage.

## Comparisons and review classifications

| Quantity | Validity | Anti-collapse |
|---|---|---|
| Fresh Fable distribution | Unmeasured | Unmeasured |
| Fresh Muse distribution | Unmeasured | Unmeasured |
| Fresh exact status agreement | Undefined: zero pairs | Undefined: zero pairs |
| Policy-equivalent agreement | Undefined: zero pairs | Undefined: zero pairs |
| Keep/reject agreement | Not applicable | Undefined: zero pairs |
| Historical/fresh Fable exact status agreement | Undefined: zero pairs | Undefined: zero pairs |

No combined agreement rate or accuracy-against-Fable metric was calculated. Historical
Fable is not ground truth and was not substituted for the missing fresh arm. No
within-instrument stability estimate can be made.

All twelve cases are explicitly **not measured / not reviewed** in the
[case review record](../family-b-bridge-v0.1/review/unmeasured-cases.json). No comparison category
is assigned: stable, instrumentation_drift, substantive_close and substantive_divergence
counts are all **not assessed**, for both fresh Fable/Muse and historical/fresh Fable.
There are zero evaluated pairs, which must not be interpreted as zero divergences.
There are no measured status-changing drift, substantive-close or substantive-divergence
cases to discuss, and no synthetic consensus labels. The complete-results freeze gate
remained closed throughout. The report describes operational failure, not semantics.

## Directional questions

1. Systematic validity permissiveness relative to fresh Fable: not assessed.
2. Systematic validity strictness: not assessed.
3. Warrants reinterpreted as implementation conditions: not assessed.
4. Implementation conditions reinterpreted as validity defects: not assessed.
5. Preservation of clear anti-collapse rejections: not assessed.
6. Preservation of N002's modest material departure: not assessed.
7. Permissive uncertainty treatment in N004: not assessed.
8. Formalization promoted to sufficient departure: not assessed.
9. Mundane-looking operational novelty suppressed: not assessed.
10. Differences larger or qualitatively different from historical/fresh Fable variation:
    not assessed; neither comparison exists.

Artificial formatting fixtures cannot answer any of these questions. No rationale-based
review was performed because the required collection and freeze were not reached.

## Recommendation, limitations and next boundary

The single recommendation is **`inconclusive`**. Muse's successful artificial probes
establish current access and output-contract handling, not instrument comparability.
An expired Fable authentication token is neither evidence for compatibility nor evidence
of a material transition. There is no basis to decide whether replacing Fable would
change the meaning of Family B or produce ordinary independent-model disagreement.

Do not begin Experiment F with Muse as the presumed replacement. Resolving the bridge
requires restored Fable authentication and explicit recorded recovery authorization
under an additive recovery plan that retains this failure. No automatic resumption is
authorized by this report. No compatible-transition protocol marker was added.

Limitations: no primary sample, no fresh Fable inference, incomplete two-provider
preflight, unavailable served snapshots, and unobservable provider internals. Even a
later completed bridge would be twelve deliberately selected frozen cases, not a
population reliability estimate or proof of model equivalence. This attempt does not
modify historical experiments, prospective validity, or the experimental classifiers.
Experiment F, resumed E, natural-output anti-collapse, grounding, diversity filtering,
and retrieval integration were not executed.

## Verification

Bridge tests cover source/packet/schema integrity, schedule uniqueness, projection
preservation, canonical rejection, fallback rejection, disabled tools/history, exclusive
reservations, failure preservation, comparison gating and review categories. Additional
incomplete-state tests verify the actual STOP, null metrics, absent primary calls,
sanitized failure evidence and preserved raw transport hashes.

Historical suites passed: v0.3 contracts (33), validity runner (15), Experiment D (44),
original E (47), and E recovery (22). D completion and E recovery completion verifiers
passed with private evidence, as did v0.3 preparation verification. E's historical
insufficient-coverage result remains unchanged. All 18 bridge tests and the terminal
incomplete verifier passed with private evidence. Together the six suites comprise
179 passing tests. `git diff --check` passed before publication.

Run the read-only terminal verifier with:

```bash
python -B distance/family-b-bridge-v0.1/verify_incomplete.py --private
```
