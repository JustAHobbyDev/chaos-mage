# Cross-Domain Retrieval and Mapping Test v0.1

Status: preregistered before target construction and retrieval execution.

Purpose: test whether the frozen five-field instrument schema carries enough
source-neutral operational structure to support **cross-domain retrieval and
mapping without adding new schema fields**.

This experiment follows the completed extraction stress test in
`review/stress-batch-v0.1-classification.md`, where schema v0.1 survived
extraction.

## 1. Research question

Can a retriever, given only:

```yaml
state:
operation:
signal:
inference:
limit:
```

recover structurally appropriate instruments for problems in unrelated domains,
and can a mapper instantiate those same five fields coherently in the target
domain?

The experiment deliberately separates:

1. **retrieval** — finding a structurally relevant instrument;
2. **mapping capacity** — mapping the correct instrument when it is supplied;
3. **end-to-end transfer** — mapping the instrument actually retrieved.

No new instrument-schema field may be introduced during the experiment.

## 2. Frozen corpus snapshot

Use the repository state at commit:

```text
9a5bc7e626d1e5f27d6ecec224f70dbc08a6a3a2
```

The candidate pool consists only of instruments whose final status at that
snapshot is `accepted`.

Provisional instruments are excluded from the retrieval pool.

At preregistration, this yields 14 accepted instruments.

During the experiment:

- do not revise their five fields;
- do not add newly extracted instruments to the pool;
- do not remove an accepted instrument because it creates ambiguity;
- do not expose `name`, `practice`, `source`, `notes`, `ambiguities`,
  or `extraction_failures` in the schema retrieval arm.

Each candidate receives a randomly or arbitrarily assigned opaque identifier
whose mapping to the repository instrument remains hidden from retrievers and
mappers.

## 3. Fixed anchor set

Ten accepted instruments are selected in advance as hidden benchmark anchors:

1. luminol latent-trace detection
2. chain-of-custody verification
3. dechallenge/rechallenge
4. seismic tomography
5. chromatography
6. source corroboration
7. regression bisection
8. delta debugging
9. dendrochronological crossdating
10. step-response probing

The remaining accepted instruments remain in the candidate pool as distractors.

The anchor identity for each target is benchmark metadata and is never shown to
the retriever or mapper.

## 4. Target construction

Create exactly one target case from each hidden anchor.

### 4.1 Target author packet

For each target, the target author receives only:

- the anchor's five frozen fields;
- an assigned target-domain label;
- these target-construction rules.

The target author does **not** receive:

- instrument name;
- source practice;
- source or provenance;
- notes or ambiguity metadata;
- repository filename;
- other instruments.

### 4.2 Target-domain diversity

Targets must come from domains substantially different from the anchor's source
practice. Across the ten cases, use ten distinct target-domain families.

Suitable families include:

- organizational operations;
- literary or textual analysis;
- product/customer behavior;
- education or learning;
- supply-chain operations;
- legal/compliance work;
- online community operations;
- project management;
- financial/accounting process;
- creative/editorial production.

The exact anchor-to-domain assignment is frozen before the first retrieval run.

### 4.3 Target narrative requirements

Each target is a 120–250 word natural-language problem.

It must:

- describe the target situation, available observations/data, objective, and
  material constraints;
- make the anchor operation possible in the target domain;
- contain enough structure for an appropriate instrument to be useful;
- avoid prescribing the solution itself;
- avoid source-practice terminology and source-domain imagery;
- avoid the instrument name or obvious paraphrases of that name.

The target must not be written in the five-field schema.

### 4.4 Lexical leakage audit

Before retrieval begins, a separate auditor receives:

- the completed target;
- the anchor name and practice;
- source-domain terminology needed to identify obvious leakage.

The auditor may flag only lexical or source-domain leakage, not structural
similarity.

A flagged target is rewritten before any retrieval run.

Once the first retrieval run begins, target text is frozen and cannot be
rewritten.

## 5. Retrieval arms

Every target is tested in two arms using the same candidate pool.

The same model family/configuration must be used for both arms, in fresh
contexts. Record provider, model, date, serving metadata when available, and any
sampling controls exposed by the provider.

### 5.1 Schema-only arm — primary

Each candidate is shown as:

```yaml
id: <opaque-id>
instrument:
  state:
  operation:
  signal:
  inference:
  limit:
```

No candidate name, practice, source, or explanatory metadata is shown.

The retriever is instructed:

> Rank the three instruments whose operational structure is most applicable to
> this target. Prefer structural fit over vocabulary or source-domain
> resemblance. Return exactly three opaque IDs in ranked order, with an
> optional short structural rationale after the ranking.

### 5.2 Name/practice baseline — secondary

Each candidate is shown only as:

```yaml
id: <opaque-id>
name: <instrument name>
practice: <source practice>
```

The five fields are withheld.

The same ranking instruction and target are used.

This baseline tests how much retrieval could be accomplished from pretrained
knowledge or semantic associations with instrument names rather than the
explicit schema.

## 6. Retrieval repetitions

Run each target **three times per arm**, each in a fresh context.

Candidate order is independently shuffled on every run.

Do not feed earlier rankings or rationales into later runs.

Total planned retrieval calls:

```text
10 targets × 2 arms × 3 repetitions = 60 retrieval runs
```

## 7. Retrieval metrics

### 7.1 Target-level anchor recall@3 — primary retrieval metric

For one target, schema retrieval succeeds when its hidden anchor appears in the
top three in at least **2 of 3 schema-only runs**.

Report:

- number of successful targets out of 10;
- raw anchor recall@1 and recall@3 across all 30 schema runs;
- mean reciprocal rank of the anchor across schema runs, treating absence from
  top three as rank 4 for the preregistered summary.

### 7.2 Baseline comparison — secondary

Apply the same target-level success definition to the name/practice baseline.

A **schema retrieval advantage** is demonstrated when schema-only target-level
anchor recall@3 exceeds the name/practice baseline by at least **2 of the 10
targets**.

Failure to demonstrate this relative advantage does not by itself fail the
absolute schema-support test. It means only that explicit schema fields have not
been shown to outperform instrument-name/practice cues on this benchmark.

## 8. Selecting the retrieved candidate for mapping

For each target, select one candidate from the three schema-only retrieval runs.

Use this deterministic rule:

1. If the same candidate is ranked first in at least 2 of 3 runs, select it.
2. Otherwise assign each candidate its rank in each run, using rank 4 when it
   does not appear in the top three.
3. Sum ranks across the three runs.
4. Select the candidate with the lowest total.
5. If still tied, select the lexicographically lowest opaque ID.

This candidate is the **retrieved candidate** for end-to-end mapping.

Do not substitute the hidden anchor when retrieval selects another instrument.

## 9. Mapping tests

Mapping uses no new schema fields.

The mapper outputs exactly:

```yaml
instrument:
  state:
  operation:
  signal:
  inference:
  limit:
```

but every field must now be expressed in the target domain.

The source candidate remains visible only through its five source-neutral
fields and opaque ID.

Run two mapping conditions per target.

### 9.1 Anchor mapping capacity

A fresh mapper receives:

- the target narrative;
- the hidden anchor's five fields under an opaque ID.

It does not receive the instrument name or source practice.

Purpose: determine whether the five fields contain enough information to
construct a coherent cross-domain mapping **when retrieval is not a factor**.

### 9.2 End-to-end retrieved mapping

A different fresh mapper receives:

- the same target narrative;
- the selected retrieved candidate's five fields under its opaque ID.

It does not receive the candidate name, practice, or whether it is the hidden
anchor.

Purpose: test the actual retrieval-to-mapping pipeline.

## 10. Mapping adjudication

Each mapping is judged independently by two fresh-context adjudicators.

Adjudicators receive:

- the source candidate's five fields;
- target narrative;
- target-domain five-field mapping;
- these mapping criteria.

They do not receive:

- candidate name or practice;
- hidden-anchor identity;
- retrieval ranks;
- whether the candidate was the benchmark anchor;
- aggregate experiment results.

Judge each field pass/fail.

### State

Pass when the mapped state identifies a target-domain situation in which the
transferred operation is applicable without merely restating the problem.

### Operation

Pass when the mapped operation is a concrete target-domain procedure that
preserves the source operation's functional relationship rather than its
imagery or vocabulary.

### Signal

Pass when the mapped signal is an identifiable target-domain distinction that
would be produced or exposed by the operation and remains distinct from its
interpretation.

### Inference

Pass when the mapped inference is warranted by the mapped signal, preserves the
source instrument's inferential role, and does not overclaim.

### Limit

Pass when at least one target-domain confound, failure condition, ambiguity, or
non-uniqueness preserves the epistemic discipline of the source limit.

### Overall mapping pass

A mapping passes only when:

- `operation` passes;
- `signal` passes;
- `inference` passes; and
- at least **4 of 5** total fields pass.

If the two adjudicators disagree on the overall pass/fail result, use a third
fresh-context adjudicator and take the majority result.

Field-level disagreements may be reported but do not require a third judge
unless they change the overall result.

## 11. Primary preregistered thresholds

The five-field schema is classified as **supporting cross-domain retrieval and
mapping on this benchmark** only if all three conditions hold:

### R — Retrieval

At least **8 of 10 targets** meet schema-only target-level anchor recall@3.

### M — Mapping capacity

At least **8 of 10 hidden-anchor mappings** pass adjudication.

### E — End-to-end transfer

At least **7 of 10 retrieved-candidate mappings** pass adjudication.

All three — R, M, and E — are required.

## 12. Failure localization

If the primary result does not pass, interpret the pattern before proposing any
schema change.

### R fails, M passes

The five fields appear sufficient for mapping when the correct instrument is
known, but the retrieval procedure does not reliably select it.

Interpret as a **retrieval problem**, not immediate evidence for new fields.

### R passes, M fails

The schema can identify structurally related candidates but does not reliably
carry enough information to instantiate them in a new domain.

Interpret as a **mapping-representation problem** and inspect field-level
mapping failures before proposing revision.

### R passes, M passes, E fails

Retrieval finds the benchmark anchor often enough and anchor mapping works, but
the selected top candidate does not produce reliable transfer.

Interpret as a **ranking/selection or alternate-candidate quality problem**.

### R and M both fail

The experiment does not isolate retrieval from representation well enough to
attribute the problem. Run targeted follow-up before changing the schema.

## 13. Field-level schema warning

Even if M reaches its 8/10 threshold, record a **mapping-field warning** if the
same field fails in at least **4 of the 10 anchor mappings**.

A field-level warning does not automatically change the overall classification.
It triggers a targeted follow-up experiment on that relation.

Do not add a field during this experiment.

## 14. Testability and inconclusive execution

The experiment is **execution-inconclusive** if fewer than 9 targets complete:

- all three schema retrieval runs;
- all three baseline retrieval runs;
- anchor mapping;
- retrieved-candidate mapping;
- required adjudication.

Provider or tool failures may be retried using the same frozen input.

Do not replace a target after seeing retrieval or mapping results.

If the experiment is execution-inconclusive, complete the missing runs before
classifying R, M, or E whenever technically possible.

## 15. Final reporting

The final report must include:

1. corpus snapshot and eligible candidate count;
2. opaque-ID key, revealed only after all judging is complete;
3. the ten target narratives and frozen anchor assignments;
4. all 60 retrieval rankings;
5. schema target-level anchor recall@3;
6. schema raw recall@1, recall@3, and MRR summary;
7. baseline target-level anchor recall@3;
8. whether the 2-target schema-advantage criterion was met;
9. selected retrieved candidate for each target;
10. all 20 mappings;
11. field-level adjudication results;
12. R, M, and E calculations;
13. mapping-field warnings;
14. exactly one primary result:
    - **schema supports cross-domain retrieval and mapping on this benchmark**;
    - **primary support threshold not met**; or
    - **execution-inconclusive**.

Do not reinterpret the thresholds after results are visible.

## 16. Freeze discipline

Once target construction begins, do not change:

- the five-field schema;
- corpus snapshot;
- accepted candidate pool;
- ten anchors;
- retrieval arms;
- number of repetitions;
- ranking rule;
- mapping output shape;
- mapping adjudication criteria;
- R, M, or E thresholds.

Target text becomes individually frozen after lexical audit and before its first
retrieval call.

Unexpected failure modes are recorded for later experiments rather than repaired
mid-run.
