# Stress Batch v0.1 — Final Classification

Status: complete.

This report applies the preregistered extraction, adjudication, calibration,
and full-batch decision rules to the 10-instrument stress batch.

## Final instrument statuses

| Candidate | Final status | Evaluable as schema test? | Schema-relevant difficulty? |
| --- | --- | --- | --- |
| Seismic tomography | accepted | yes | no |
| System identification | provisional | no | no |
| Chromatography | accepted | yes | no |
| Source corroboration | accepted | yes | no |
| Provenance reconstruction | accepted | yes | no |
| Analysis of Competing Hypotheses | accepted | yes | no |
| Regression bisection | accepted | yes | no |
| Delta debugging | accepted | yes | no |
| Dendrochronological crossdating | accepted | yes | no |
| Step-response probing | accepted | yes | no |

System identification is not counted as an evaluable schema test because its
adjudicated `split-required` result makes the original candidate a
granularity/candidate-selection failure under the preregistered adjudication
rule. Its final extraction status remains provisional, but it contributes no
schema-gap evidence.

## Required batch counts

1. **Evaluable instruments:** 9 of 10
2. **Final status counts:**
   - accepted: 9
   - provisional: 1
   - rejected: 0
3. **Schema-relevant provisional or rejected cases:** 0
4. **Gap signatures:** none
5. **Cross-practice gap recurrence:** none

## Threshold calculation

### A — repeated rejection
Not met.

There are zero schema-relevant rejections.

### B — rejection plus repeated provisional evidence
Not met.

There are zero schema-relevant rejections and zero schema-relevant provisional
cases.

### C — repeated provisional evidence without rejection
Not met.

There are zero schema-relevant provisional cases.

### D — rejection rate
Not met.

There are zero schema-relevant rejections, below the threshold of three.

### E — total schema-relevant difficulty
Not met.

There are zero schema-relevant provisional or rejected cases, below the
threshold of five.

## Preregistered full-batch decision

Apply the rules in order:

### Rule 1 — specific demonstrated gap
No A/B/C gap signature exists.

**Does not match.**

### Rule 2 — insufficient testability
Nine instruments provide valid schema tests. The minimum is seven.

**Does not match.**

### Rule 3 — broad insufficiency
Neither D nor E is met.

**Does not match.**

### Rule 4 — survival
No earlier rule matches.

**Matches.**

# Final classification: schema survives

Under this preregistered 10-instrument stress test, schema v0.1 did not show a
repeated or broad representational failure at the predefined thresholds.

This result means only that the five-field representation survived this
extraction stress test. It does **not** establish that the schema is optimal,
complete, or sufficient for cross-domain retrieval, mapping, instrument
composition, or downstream usefulness.

## What the batch did establish about extraction

Within the evaluable cases, the frozen schema represented:

- multi-stage but coherent inverse inference (seismic tomography);
- separation without conflating downstream identification (chromatography);
- nonphysical and relational evidence (source corroboration);
- documentary-temporal reconstruction (provenance reconstruction);
- eliminative comparison among explicit hypotheses (ACH);
- eliminative narrowing over ordered history (regression bisection);
- eliminative reduction over component sets (delta debugging);
- relational temporal alignment (crossdating);
- perturbation followed by temporal response (step-response probing).

The one candidate that failed the granularity test did so because the named
practice was broader than one instrument, not because an operational relation
could not be represented.

## Procedural consequence

Schema v0.1 remains frozen for the next research phase unless a later,
separately preregistered experiment supplies new evidence for revision.

The broad `system-identification` candidate may later be replaced by child
instruments such as model estimation and residual validation, but that
replacement is outside this completed stress batch.
