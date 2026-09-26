# Borderline-Case Adjudication Rule v0.1

Status: preregistered before the 10-instrument stress-test batch.

Purpose: resolve disagreements about candidate granularity, abstraction level, extraction status, schema relevance, and gap-signature assignment without allowing the batch outcome to influence those decisions.

This document supplements:

- [instrument-extraction-v0.1.md](instrument-extraction-v0.1.md)
- [extraction-decision-rule-v0.1.md](extraction-decision-rule-v0.1.md)
- [calibration-thresholds-v0.1.md](calibration-thresholds-v0.1.md)

The frozen five-field schema remains unchanged.

## 1. Roles

Each stress-test candidate has two distinct roles.

### Extractor

The extractor:

1. researches the source practice;
2. chooses the proposed instrument boundary;
3. produces the five-field extraction;
4. records ambiguities and extraction failures;
5. proposes `accepted`, `provisional`, or `rejected`;
6. proposes whether any difficulty is schema-relevant;
7. proposes a gap signature when required.

The extractor does not decide the final adjudicated classification when a borderline issue is raised.

### Adjudicator

The adjudicator reviews the candidate in a **fresh context** after the extraction is complete.

The adjudicator receives:

- the source evidence used for the extraction;
- the candidate extraction;
- the frozen schema;
- the extraction decision rule;
- this adjudication rule.

The adjudicator must **not** receive:

- current accepted/provisional/rejected totals for the stress batch;
- recurrence counts for existing gap signatures;
- whether any A/B/C/D/E threshold is close to firing;
- the provisional overall batch classification.

This separation prevents an adjudication from being influenced by its effect on the final result.

Where practical, extractor and adjudicator should be different model instances or sessions. Different providers are desirable but not required. Independence here means fresh context and withheld batch-outcome information, not a claim of independent human judgment.

## 2. When adjudication is required

Adjudication is mandatory when any of the following occurs:

- the extractor marks the candidate `provisional` or `rejected`;
- the extractor records a `composite`, `overabstracted`, `underabstracted`, `domain_nouns_required`, or `no_distinct_signal` failure;
- the extractor claims a difficulty is schema-relevant;
- a gap signature is proposed;
- two extractions appear to share a gap signature;
- a later extraction would cause A, B, C, D, or E to fire;
- a reviewer explicitly disputes granularity, abstraction, schema relevance, or signature assignment.

Accepted cases without any of these triggers do not require a separate adjudication pass.

## 3. General adjudication principle

The adjudicator answers only:

> What is the narrowest defensible classification supported by the source mechanism and the preregistered rules?

The adjudicator does not optimize for a clean corpus, an even status distribution, preservation of schema v0.1, or discovery of a schema gap.

When uncertainty remains after applying the rules below, resolve it **conservatively against counting evidence as a schema gap**.

This means uncertainty may produce a provisional extraction or an unusable candidate, but it must not be converted into schema-gap evidence merely because a missing field is imaginable.

## 4. Granularity adjudication

A granularity dispute asks whether the named candidate is:

- one coherent instrument;
- a composite pipeline containing separable instruments; or
- too underspecified to determine.

Apply this test:

### 4.1 Coherent-chain test

Write the candidate as:

```text
state -> operation -> signal -> inference
```

A candidate is a sufficiently coherent instrument when one principal operation produces or exposes one principal signal relationship that licenses one principal inferential move, even if implementation contains subordinate steps.

Subordinate steps do not make an instrument composite merely because the real procedure has multiple actions.

### 4.2 Split test

Classify the candidate as composite when:

1. two or more subprocedures could be applied independently;
2. they produce materially different signal types or inferential warrants; and
3. later comparison or mapping could plausibly retrieve one without the other.

If all three are true, the candidate boundary is the problem.

### 4.3 Granularity outcome

The adjudicator records one of:

- `coherent`
- `split-required`
- `granularity-unresolved`

If `split-required`, the original candidate does **not** count as schema-relevant evidence. It is a candidate-selection failure unless a child instrument, once separately extracted, still exhibits a schema-relevant failure.

If `granularity-unresolved`, the candidate is provisional or unevaluable as appropriate and does not count toward a schema-gap threshold.

## 5. Abstraction adjudication

An abstraction dispute asks whether the extraction is too source-specific or too generic.

The target is the **least abstract formulation that removes unnecessary source-domain dependence while preserving the complete operational mechanism**.

Apply two transformations.

### 5.1 Noun-removal test

Replace source-specific nouns that are not necessary to the mechanism.

If the mechanism remains intelligible and source-faithful, the original wording was underabstracted.

If removing a noun destroys an essential causal or inferential relation, that concept may remain, expressed at the narrowest transferable level possible.

### 5.2 Specificity-restoration test

Starting from the abstract extraction, ask whether two materially different source mechanisms would collapse into the same five fields even though their later mapping behavior should differ.

If yes, restore the minimum relational specificity needed to distinguish them.

### 5.3 Abstraction outcome

The adjudicator records one of:

- `adequate`
- `underabstracted`
- `overabstracted`
- `abstraction-unresolved`

An abstraction problem does not count as a schema gap unless the adjudicator can state an essential source-faithful relationship that cannot be retained at any defensible abstraction level within the five fields.

If both a more concrete and a more abstract extraction are defensible and preserve the same operational relationships, choose the less abstract one for the corpus. Do not create a schema gap from stylistic preference.

## 6. Signal/inference boundary adjudication

When it is unclear whether something belongs in `signal` or `inference`, apply this counterfactual:

> Could an observer record this distinction without yet deciding what it means?

If yes, it belongs in `signal`.

If no, and it states what the observation supports, rules out, reprioritizes, or makes plausible, it belongs in `inference`.

Relational, documentary, temporal, comparative, and negative observations are valid signals.

A difficult signal/inference boundary is schema-relevant only when the mechanism requires a third distinct epistemic relation that cannot be faithfully expressed as either an observation or what that observation licenses.

## 7. Extraction-status disagreement

The extractor and adjudicator each assign one status independently:

- accepted
- provisional
- rejected

If they agree, that status stands.

If they disagree, apply these deterministic rules:

### Accepted vs provisional
Final status: **provisional**.

### Provisional vs rejected
Final status: **provisional**, unless the adjudicator identifies a specific mandatory rejection condition from the extraction decision rule that cannot be remedied without changing the schema. In that case: **rejected**.

### Accepted vs rejected
A second adjudication pass is mandatory because the disagreement is too large for an automatic midpoint rule.

The second adjudicator receives the same allowed material and neither prior adjudicator's batch-outcome information.

- If the second adjudicator chooses accepted: final status **provisional**.
- If the second adjudicator chooses provisional: final status **provisional**.
- If the second adjudicator chooses rejected: final status **rejected**.

Thus an accepted/rejected dispute can never resolve directly to accepted.

## 8. Schema-relevance adjudication

A provisional or rejected extraction counts as schema-relevant only when the adjudicator can complete this sentence:

> Even after choosing a defensible candidate boundary and abstraction level, the instrument requires the relationship "________" to preserve its operational mechanism, and the frozen schema has no adequate place for that relationship.

The blank must:

- be expressed without source-domain nouns;
- describe an operational or inferential relationship, not a desired convenience;
- identify why collapsing it into an existing field would materially affect later comparison, retrieval, or mapping.

If this sentence cannot be completed precisely, the difficulty is **not schema-relevant**.

### Disagreement rule

If extractor and adjudicator disagree about schema relevance:

- one says schema-relevant and one says not schema-relevant -> **not schema-relevant**, unless a second adjudicator independently identifies the same missing relationship;
- if the second adjudicator identifies a materially different missing relationship -> **not schema-relevant** for threshold counting, but record both concerns for later review;
- only two independent adjudication judgments supporting the same missing relationship may override the conservative default.

## 9. Gap-signature assignment

Gap signatures exist only for adjudicated schema-relevant cases.

### 9.1 Independent formulation

Before seeing existing signature names or recurrence counts, the adjudicator writes a source-neutral description of the missing relationship.

Only after that description is fixed may it be compared with existing signatures.

### 9.2 Remedy-equivalence test

Two cases share a gap signature only if:

> The same schema clarification, field, or explicit relationship would resolve both cases without materially different additional machinery.

Similarity of wording, source domain, or symptom is insufficient.

### 9.3 Merge disagreement

If there is disagreement about whether two cases share a signature, **keep the signatures separate**.

They may be merged only when a second adjudicator independently concludes that the same remedy would resolve both.

This default deliberately biases against false recurrence.

### 9.4 Split disagreement

If an existing signature appears to contain two different missing relationships, split it before calculating thresholds whenever one schema remedy would not actually resolve all member cases.

Historical recurrence counts must be recalculated after the split.

## 10. Threshold-trigger review

Because one adjudication can trigger a preregistered threshold, every case that would newly cause A, B, C, D, or E to fire receives an automatic **threshold-trigger review** before the threshold is counted.

The threshold-trigger reviewer receives:

- the candidate and sources;
- the extraction;
- the adjudicated status;
- the proposed schema-relevance finding;
- the source-neutral gap signature, when applicable;
- the frozen rules.

The reviewer does not receive the batch outcome that would follow.

The reviewer checks only:

1. candidate boundary;
2. abstraction adequacy;
3. schema relevance;
4. signature remedy-equivalence.

If the reviewer disagrees:

- schema relevance defaults to **not schema-relevant** unless two independent reviews support it;
- signature merging defaults to **separate**;
- status defaults according to section 7.

A threshold fires only after this review is resolved.

## 11. Human operator role

The human operator does **not** adjudicate ordinary borderline cases during the stress batch.

This prevents knowledge of the project's desired direction from silently resolving evidence in favor of or against the schema.

The operator may intervene only when:

- source evidence is factually inaccessible or contradictory in a way the adjudicators cannot resolve;
- the preregistered rules themselves contain a true logical contradiction;
- a tool or data failure prevents the prescribed adjudication process.

Any such intervention must be recorded, and the affected candidate is **unevaluable for threshold counting** unless the intervention merely restores missing factual/source access without deciding the representational question.

## 12. Adjudication record

Every mandatory adjudication produces a record containing:

```yaml
adjudication:
  candidate:
  trigger:
  extractor_status:
  adjudicator_status:
  final_status:
  granularity:
  abstraction:
  schema_relevant:
  gap_signature:
  threshold_trigger_review:
  rationale:
```

`gap_signature` is null when the case is not schema-relevant.

The rationale must identify the rule applied. It must not mention the desired or resulting batch classification.

## 13. Conservative defaults

When the rules do not clearly resolve a borderline case:

- composite vs schema gap -> **candidate/granularity problem**
- abstraction problem vs schema gap -> **abstraction problem**
- schema-relevant vs not -> **not schema-relevant**
- same signature vs different -> **different signatures**
- accepted vs provisional -> **provisional**
- usable vs unevaluable when source evidence is inadequate -> **unevaluable**

These defaults reduce false evidence for schema revision. They do not erase the concern; unresolved issues remain recorded for later targeted experiments.

## 14. Freeze discipline

Do not change this adjudication rule during the 10-instrument stress-test batch.

Any defect discovered in the rule is recorded for a later protocol revision. If a true contradiction makes adjudication impossible for a candidate, mark that candidate unevaluable rather than editing the rule mid-batch.
