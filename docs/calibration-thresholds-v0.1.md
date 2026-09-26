# Calibration Thresholds v0.1

Status: preregistered before the 10-instrument stress-test batch.

Purpose: define in advance when repeated provisional or rejected extractions count as evidence that the frozen five-field schema is missing an operational relationship.

These thresholds apply only to the planned stress-test batch:

- seismic tomography
- system identification
- chromatography
- source corroboration
- provenance reconstruction
- analysis of competing hypotheses
- regression bisection
- delta debugging
- dendrochronological crossdating
- step-response probing

The extraction decision rule remains [extraction-decision-rule-v0.1.md](extraction-decision-rule-v0.1.md).

## 1. What counts toward a schema-gap threshold

Not every provisional or rejected extraction is evidence against the schema.

A case is **schema-relevant** only when all of the following hold:

1. The source procedure and its inferential warrant are established well enough to extract.
2. The difficulty cannot be adequately explained by choosing the wrong candidate unit, such as selecting a whole pipeline or discipline instead of one instrument.
3. The difficulty cannot be resolved by ordinary rewording, removing unnecessary source-domain nouns, or choosing a better abstraction level while keeping the five fields unchanged.
4. The missing or distorted information is part of the operational mechanism and would matter to later comparison, retrieval, or mapping.
5. Preserving that information would require either:
   - leaving an essential relationship implicit or ambiguous inside the five fields; or
   - carrying essential mechanism information in notes, ambiguity metadata, provenance, or another non-schema location.

Cases caused only by `composite`, `underabstracted`, `overabstracted`, `source_unclear`, or poor candidate selection do **not** count toward a schema-gap threshold unless the same problem remains after a defensible instrument boundary and abstraction are identified.

An unusual signal type is not itself a schema problem.

## 2. Schema-relevant provisional and rejection

### Schema-relevant provisional

Count a provisional case when all five fields can be populated, but an essential operational relationship must be represented ambiguously, collapsed into another relation, or left implicit in a way that could materially affect comparison, retrieval, or mapping.

### Schema-relevant rejection

Count a rejection when a coherent source instrument cannot be represented faithfully in the five fields because an essential operational relationship has no adequate place in the schema.

A rejection is therefore stronger evidence than a provisional case.

## 3. Gap signatures

Every schema-relevant provisional or rejection must be assigned a short **gap signature**.

A gap signature describes the allegedly missing relationship without source-domain vocabulary.

Examples of the required form:

- "must represent an explicit set of competing alternatives"
- "must distinguish the observation from the pattern formed across observations"
- "must preserve an ordered sequence of dependent operations"
- "must represent a stopping condition separately from the inference"

Do not use instrument names in the signature.

Two cases may share a signature only when the **same hypothetical schema clarification or addition** would resolve both. Superficially similar difficulties must remain separate if they would require different remedies.

This rule prevents unrelated failures from being grouped after the fact.

## 4. Evidence thresholds for a specific schema gap

A recurring gap signature becomes **strong evidence of a schema gap** if any one of these conditions is met:

### A. Repeated rejection

- at least **2 schema-relevant rejections**;
- sharing the same gap signature;
- from at least **2 different practices**.

### B. Rejection plus repeated provisional evidence

- at least **1 schema-relevant rejection**;
- plus at least **2 schema-relevant provisional cases**;
- all sharing the same gap signature;
- spanning at least **2 different practices**.

### C. Repeated provisional evidence without rejection

- at least **4 schema-relevant provisional cases**;
- sharing the same gap signature;
- spanning at least **3 different practices**.

Meeting any of A, B, or C is sufficient to justify a v0.2 schema-change proposal for that gap. It does **not** automatically determine what the change should be.

## 5. Suggestive but insufficient evidence

The following count as **suggestive evidence** and trigger targeted follow-up, but do not justify changing the frozen schema:

- 1 schema-relevant rejection by itself;
- 2 schema-relevant provisional cases with the same signature across at least 2 practices;
- 3 schema-relevant provisional cases with the same signature that do not span 3 practices;
- repeated schema-relevant difficulty confined to one practice.

A suggestive result should produce another targeted extraction set designed specifically to test the suspected gap.

## 6. Evidence that does not count as a schema gap

The following do not count toward the thresholds above:

- one instrument is too broad and needs to be split;
- one source is unclear about its own method;
- the extractor chose the wrong abstraction level;
- a signal is documentary, relational, temporal, negative, comparative, or otherwise nonphysical;
- two source-domain terms collapse into one abstract mechanism;
- an extraction is awkward stylistically but preserves the full mechanism;
- several failures come from variants of the same underlying instrument within one practice;
- a problem disappears after rewording without adding an operational relationship.

These may justify candidate or extraction-guide changes, not schema changes.

## 7. Batch-level broad insufficiency

The schema is considered **broadly insufficient for this stress batch** if either condition is met, even when the individual cases have different gap signatures:

### D. Rejection rate

At least **3 of the 10 instruments** are schema-relevant rejections.

### E. Total schema-relevant difficulty

At least **5 of the 10 instruments** are schema-relevant provisional or rejected cases.

A broad-insufficiency result triggers a general schema redesign review rather than an immediate field addition. Different failures may require different remedies.

## 8. Batch testability threshold

The overall stress batch is **inconclusive** if fewer than **7 of the 10 instruments** provide a valid test of the schema because candidate-selection, source-quality, or granularity problems prevent a defensible extraction attempt.

In that case:

- do not treat those failures as evidence against the schema;
- replace enough unusable candidates to restore at least 7 evaluable cases;
- keep the thresholds unchanged.

A specific gap may still meet a strong-evidence threshold even if the overall batch is inconclusive.

## 9. Schema v0.1 survival rule

Schema v0.1 **survives the stress batch** when all of the following are true:

1. The batch meets the testability threshold.
2. No gap signature meets strong-evidence condition A, B, or C.
3. Neither broad-insufficiency condition D nor E is met.

"Survives" means only that this batch did not demonstrate a representational gap large or recurrent enough to justify revision.

It does not establish that the schema is optimal or sufficient for later cross-domain mapping.

## 10. Preregistered full-batch classification rule

After all 10 planned extractions have been attempted, classify the batch into exactly one of three outcomes:

- **schema survives**
- **schema needs revision**
- **batch inconclusive**

Apply the following decision rule in order. Stop at the first matching rule.

### Rule 1 — Specific demonstrated gap overrides batch incompleteness

Classify **schema needs revision** if any single gap signature meets strong-evidence condition A, B, or C.

This rule applies even if fewer than 7 instruments are otherwise evaluable. A repeated cross-practice failure of the same operational relationship is sufficient evidence for a revision proposal even when the remainder of the batch is poorly testable.

The result must identify each qualifying gap signature and which condition it met.

### Rule 2 — Insufficient testability

If Rule 1 does not apply and fewer than **7 of the 10** planned instruments provide valid schema tests, classify **batch inconclusive**.

Candidate-selection, source-quality, or granularity failures that prevent a valid schema test do not count against the schema.

An inconclusive batch must replace enough unusable candidates to restore at least 7 evaluable cases while retaining the same schema, decision rule, and calibration thresholds.

### Rule 3 — Broad insufficiency

If the batch has at least 7 evaluable cases, classify **schema needs revision** if either broad-insufficiency condition D or E is met:

- **D:** at least 3 of the 10 planned instruments are schema-relevant rejections; or
- **E:** at least 5 of the 10 planned instruments are schema-relevant provisional or rejected cases.

This outcome means the representation is under enough pressure to justify a general revision review even if no single missing relationship recurs often enough to meet A, B, or C.

### Rule 4 — Survival

If none of Rules 1–3 applies, classify **schema survives**.

A survival result may still contain isolated or suggestive difficulties. Those are recorded for targeted follow-up under section 5 but do not change the full-batch classification.

"Schema survives" means only:

> Under this preregistered 10-instrument stress test, schema v0.1 did not show a repeated or broad representational failure at the thresholds defined here.

It does not mean the schema is optimal, complete, or proven sufficient for cross-domain retrieval and mapping.

## 11. Decision table

| Specific A/B/C gap? | Evaluable instruments | D or E met? | Outcome |
| --- | ---: | --- | --- |
| Yes | Any number | Either | **schema needs revision** |
| No | 0–6 | Either | **batch inconclusive** |
| No | 7–10 | Yes | **schema needs revision** |
| No | 7–10 | No | **schema survives** |

This table is authoritative if prose elsewhere appears ambiguous.

## 12. Reporting requirement

The final batch report must include:

1. number of evaluable instruments;
2. accepted / provisional / rejected counts;
3. which provisional or rejected cases are schema-relevant;
4. every gap signature and its cross-practice recurrence count;
5. whether A, B, C, D, or E fired;
6. the first decision rule above that matched;
7. exactly one final classification.

Do not substitute an informal overall judgment for this calculation.

## 13. Freeze discipline

Do not change:

- the five-field schema;
- the extraction decision rule;
- these thresholds;
- the 10 named stress-test candidates;

during the stress-test extraction batch.

Record unexpected cases as evidence. Any later change must be made after the batch outcome is calculated under these preregistered rules.
