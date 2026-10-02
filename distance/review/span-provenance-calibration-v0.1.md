# H.5 — Neutral span provenance calibration v0.1

The bounded offline calibration passes its engineering expectations. All 20 frozen mappings resolve through opaque span IDs; historical scientific results remain unchanged. Semantic support was reviewed explicitly by Codex, not established by an automated semantic evaluator or independent rater.

Base: `bdeeb973b794823a35257f472a020e12d816a8a9`. Branch: `experiment-h5-span-provenance`. Provider calls: **0**. No main merge.

## Checkpoints

| Checkpoint | SHA |
|---|---|
| architecture_and_contract | `0df9bf229ff228ef2eb6ba2bc201a6784bc2a759` |
| segmentation_and_schemas | `d29f661dead683b41c847fc255b001eb5b7c7452` |
| twenty_span_tables | `7282f028edae675cf21c1b4fcdf87d7db25bce05` |
| engineering_fixtures | `003ebea285b31c6b14d66c0c3f1ce9fd936fc137` |
| reviews_validator_and_tests | `29b8dfb3064f5ea1ed397e9052a54458ae8e015b` |

The final SHA is the commit containing publication-manifest.json; resolve it with `git log -1 --format=%H -- distance/span-provenance-calibration-v0.1/publication-manifest.json`.

## Segmentation and provenance contract

One conservative Python splitter applies equally to state, operation, signal, inference and limit. It preserves explicit blocks first, splits prose only at safe sentence boundaries, and retains ambiguity. No clause-, role-, or length-based segmentation occurs. Lists retain item/parent structure; pipe tables retain rows and header context. Those structures are tested synthetically because none occur in the frozen corpus.

Packet-local P001, P002, … IDs identify harness-owned text. Field, block, sentence and harness-only character ranges are separate metadata. The annotation envelope binds a packet; refs contain only source_id and SUPPORT/CONTEXT. A wrong envelope is rejected, but an accidentally copied local ID that also exists locally cannot reveal its foreign origin by itself.

SUPPORT contributes substantive content; CONTEXT resolves identities, antecedents, conditions and scope. The cited bundle must recover the entire claimed component through ordinary comprehension. Multiple SUPPORT spans, extra propositions, reused spans and nonminimal context are allowed. Context cannot invent an outcome relation, and a claim cannot broaden qualifiers. Review returns only SUFFICIENT, INSUFFICIENT or UNCERTAIN.

The mechanical validator checks schema, packet binding, ID existence, SUPPORT presence, duplicates and role conflicts. Separate frozen review records assess meaning. Replay validates the review binding and expected diagnostics; it is not independent confirmation of semantic judgments. Missing review remains unassessed.

## Corpus and fixture results

Mappings: **20**. Total spans: **86**.

| Field | Spans | Min per mapping | Max per mapping |
|---|---:|---:|---:|
| state | 19 | 0 | 4 |
| operation | 10 | 0 | 1 |
| signal | 21 | 0 | 4 |
| inference | 28 | 0 | 4 |
| limit | 8 | 0 | 4 |

Full per-mapping distributions and retained-boundary diagnostics are in metrics.json.

| Fixture group | Fixtures | Expectations met |
|---|---:|---:|
| positive | 20 | 20 |
| h4-regressions | 2 | 2 |
| h3-regressions | 2 | 2 |
| negative | 9 | 9 |

Component review statuses: {"INSUFFICIENT": 4, "SUFFICIENT": 60, "UNCERTAIN": 1}.

Positive coverage includes single propositions, coarse multi-proposition spans, reuse, joint support, distributed state/operation/signal bundles, pronouns and scoped relations. Negative fixtures deliberately isolate unknown IDs, absent SUPPORT, duplicate/conflicting refs, wrong packet, missing context, absent differential relations, an uncited substantive premise and scope overreach. These are engineering fixtures, not replacement provider observations.

| Regression | Result | Complete inquiry units |
|---|---|---:|
| H4-f070ba17a9b7 | pass | 0 |
| H4-86f4954813b3 | pass | 1 |
| H3-4d30014ef73c | pass | 1 |
| H3-d6134c9f4c74 | pass | 1 |

The punctuation control retains the generic request and its incomplete-inquiry interpretation despite the annotation omitting terminal punctuation. The duplicate-offset control cites both textual formulations by ID, preserving one IQ1. Both H.3 affirmative tests remain recoverable with case and scope context. None of the original H.4/H.3 judgments or historical failures was repaired.

## Diagnostics and ambiguity

Counts below are expected fixture diagnostics, not provider failure rates. Synthetic unit-test injections are excluded.

| Code | Occurrences |
|---|---:|
| PROV_UNKNOWN_SOURCE_ID | 1 |
| PROV_WRONG_PACKET | 1 |
| PROV_NO_SUPPORT | 1 |
| PROV_DUPLICATE_REF | 2 |
| PROV_ROLE_CONFLICT | 1 |
| PROV_SCHEMA | 0 |
| PROV_MISSING_CONTEXT | 1 |
| PROV_UNSUPPORTED_COMPONENT | 2 |
| PROV_SCOPE_OVERREACH | 1 |
| PROV_UNCERTAIN_SUPPORT | 1 |
| PROV_CONFLICT_REVIEW | 0 |

PROV_SCHEMA and PROV_CONFLICT_REVIEW have dedicated synthetic tests. A conflict signal requires an explicit reviewed incompatibility, matching component type and packet/target scope, and materially overlapping SUPPORT. It never automatically invalidates an annotation. REVIEW_* failures concern missing/stale/malformed review machinery; INTEGRITY_* failures concern changed artifacts, not semantic support.

Retained uncertain boundaries: 7. These arise from lowercase following sentences or single-digit numeric endings treated conservatively as possible initials. Some crossdating, delta and diagnosis spans consequently contain multiple sentences. No reviewed component became ambiguous because of this coarseness.

The meaning of ordinary lock waits is plausible but undefined; the ambiguity is lexical, not caused by coarse spans. Its UNCERTAIN review is retained rather than forced to pass or fail.

## Verification, limitations and next step

Tests: 30 passing in distance/span-provenance-calibration-v0.1/tests, 32 passing in distance/inquiry-unitization-calibration-v0.1/tests.

Historical preservation: {"historical_integrity_manifests_verified": true, "runtime_files": 10615, "tracked_files": 4178, "unchanged": true}.

Model-authored exact-text and offset requirements are removed from the new citation schema and validator. Terminal punctuation, quote shape, whitespace, line endings and JSON escaping do not determine semantic citation validity. Exact comparison remains appropriate for frozen source, span-table, fixture, review, historical-result and raw-response integrity; a changed source is a changed input.

H.5 establishes a usable bounded provenance mechanism for future separately authorized semantic experiments. It does not establish general semantic reliability, independent agreement, model compliance, robust parsing of arbitrary markup, or production readiness. The splitter deliberately under-segments and supports only explicit lightweight authored structures. Real lists/tables and former/latter language are absent from this corpus; their tests exercise plumbing only. Recorded semantic reviews remain fallible operator judgments. A valid ID alone cannot establish support.

**Recommended next step:** Design a separately authorized broader-language provenance challenge with independent semantic review; make no new provider calls or production integration as part of H.5.

Recommendation not executed. Work stops after H.5: no new natural outputs, Experiment E, provider calls, historical rewrites, production integration or merge to main.
