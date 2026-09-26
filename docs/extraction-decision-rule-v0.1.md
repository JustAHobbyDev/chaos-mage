# Extraction Decision Rule v0.1

Status: frozen for the initial calibration and stress-test batches.

Purpose: decide whether a candidate practice has been successfully extracted into the frozen five-field instrument schema. This rule evaluates extraction fidelity only. It does **not** evaluate novelty, usefulness, transferability, retrieval quality, or downstream problem-solving value.

## Frozen comparable schema

```yaml
instrument:
  state:
  operation:
  signal:
  inference:
  limit:
```

No extraction may add, remove, rename, or subdivide these fields during v0.1 calibration.

## Outcomes

Every extraction receives exactly one status:

```text
accepted
provisional
rejected
```

### Accepted

Mark an extraction `accepted` only when all of the following hold:

1. **State is applicable.** The `state` names the structural situation in which the instrument can operate rather than merely restating the source domain.
2. **Operation is specific.** The `operation` says what is actually done: an intervention, observation, comparison, perturbation, transformation, or other definite procedure.
3. **Signal is distinguishable.** The `signal` identifies an observable distinction produced or exposed by the operation and is not merely the inference rewritten as an observation.
4. **Inference is warranted and narrow.** The `inference` states what the signal supports, constrains, eliminates, reprioritizes, or makes more or less plausible without claiming more than the source practice warrants.
5. **Limit is meaningful.** The `limit` names at least one substantive circumstance in which the signal or inference can fail, mislead, become ambiguous, or lose discriminating power.
6. **The mechanism survives abstraction.** Unnecessary source-domain nouns can be removed without destroying the explanation of how the instrument works.
7. **The candidate is one sufficiently coherent instrument.** A single operation-to-signal-to-inference relationship can be represented without hiding materially different sub-instruments inside one entry.
8. **No essential mechanism is hidden elsewhere.** The extraction record, notes, provenance, or ambiguity metadata do not carry information that is necessary to understand the operational mechanism itself.

### Provisional

Mark an extraction `provisional` when the candidate is clearly instrument-like and all five frozen fields can be populated without inventing information, but an unresolved issue could materially affect later comparison, retrieval, or mapping.

Typical reasons include:

- uncertain granularity or a possible composite instrument;
- multiple defensible abstraction levels;
- an unresolved boundary between `operation`, `signal`, and `inference`;
- source disagreement about what the signal licenses;
- concern that the abstraction is too broad or too source-specific;
- an unstable stopping rule or decision threshold;
- uncertainty about whether one named practice should be split into several instruments.

A provisional extraction is not a failed extraction. It preserves a usable hypothesis while explicitly recording why it is not yet safe to treat as canonical.

### Rejected

Mark a candidate `rejected` when it cannot be represented under the frozen schema without materially distorting the source mechanism.

Reject when one or more of these conditions holds and cannot be resolved by ordinary rewording or selecting a better abstraction level:

- the candidate is a perspective, discipline, metaphor, or principle rather than an operation;
- no identifiable signal is produced or exposed;
- no warranted inference connects the signal to the claimed conclusion;
- the mechanism requires source-domain analogy or metaphor to remain intelligible;
- several materially different instruments are bundled so tightly that one five-field representation is misleading;
- an essential operational relationship can only be preserved by adding information outside the five fields;
- the source is too unclear or disputed to establish what the procedure actually does.

Record the reason in `extraction_failures`.

## Signals may be nonphysical

An extraction does **not** fail because its signal is unusual.

A valid `signal` may be:

- physical;
- numerical;
- documentary;
- relational;
- comparative;
- temporal;
- spatial;
- negative or absence-based;
- a pattern of consistency or contradiction;
- a change in the relative standing of alternatives.

The requirement is not sensory observability. The requirement is an identifiable distinction produced or exposed by the operation that licenses a constrained inference.

## Essential-mechanism test

This is the strongest test for a schema failure.

After reading only:

```text
state
operation
signal
inference
limit
```

ask:

> Can the operational mechanism and its inferential warrant be understood without consulting notes, ambiguity metadata, source-domain metaphor, or an undeclared extra relation?

If **yes**, the schema may be sufficient for this candidate.

If **no**, do not repair the problem by adding prose elsewhere. Record the missing relationship as an extraction failure. Repeated failures of the same kind are evidence for a later schema revision.

## Decision sequence

Apply these questions in order:

1. **What is actually done?**
   - If no definite operation exists: reject as `not_operational`.

2. **What observable distinction results or becomes available?**
   - If no distinguishable signal exists: reject or record `no_distinct_signal`.

3. **What does that distinction legitimately license us to infer?**
   - If no warranted relationship exists: reject or record `no_warranted_inference`.

4. **When could that inference fail or mislead?**
   - If no meaningful limit can be established, inspect for `no_meaningful_limit`.

5. **Does the mechanism still make sense after unnecessary source-domain nouns are removed?**
   - If not, inspect for `underabstracted` or `domain_nouns_required`.

6. **Is this one coherent operation-signal-inference mechanism?**
   - If materially different mechanisms have been bundled, mark provisional or reject with `composite`.

7. **Is essential information being smuggled into metadata or notes?**
   - If yes, record the missing relationship rather than expanding the frozen schema.

## What this rule does not decide

This decision rule does not determine:

- whether an accepted instrument is useful outside its source domain;
- whether another instrument is structurally similar;
- whether retrieval can find it;
- whether a cross-domain mapping is valid;
- whether applying it improves reasoning;
- whether the five-field schema survives the calibration batch as a whole.

Those are later experiments.

## Freeze discipline

Do not alter this rule during the 10-instrument stress-test batch.

Unexpected cases should be recorded as evidence. After the batch is complete, the combined calibration set can be reviewed for recurring failure patterns and any proposed changes can be evaluated against predefined calibration thresholds.
