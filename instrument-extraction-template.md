# Instrument Extraction Template v0.1

## Frozen instrument schema

Do not add, remove, rename, or subdivide these fields during the initial extraction batch.

```yaml
instrument:
  state:
  operation:
  signal:
  inference:
  limit:
```

### `state`

**Definition:** The kind of situation that must exist for the instrument to be applicable.

Describe the structural precondition, not the source-domain setting.

**Good:**
`A past event may have left a persistent residue that ordinary inspection does not reveal.`

**Too domain-specific:**
`Investigators suspect blood was cleaned from a crime scene.`

**Too vague:**
`Something is hidden.`

---

### `operation`

**Definition:** The intervention, observation, comparison, perturbation, or transformation actually performed.

This is the instrument's active mechanism.

**Good:**
`Apply a probe that selectively interacts with the suspected residue.`

**Too descriptive:**
`Examine the scene carefully.`

**Not an operation:**
`Hidden evidence exists.`

---

### `signal`

**Definition:** The observable result produced or exposed by the operation.

It should be distinguishable from both the operation and the interpretation of the result.

**Good:**
`Locations containing responsive material produce a visible reaction.`

**Inference disguised as signal:**
`The operation reveals where the event occurred.`

The visible reaction is the signal. What it means belongs in `inference`.

---

### `inference`

**Definition:** What the signal legitimately supports, constrains, distinguishes, or makes more/less plausible.

State the narrowest warranted inference.

**Good:**
`A positive response supports the presence of material capable of producing the reaction at that location.`

**Too strong:**
`A positive response proves that blood was present and identifies what happened.`

---

### `limit`

**Definition:** Conditions under which the signal or inference may mislead, fail, become ambiguous, or cease to discriminate.

This describes limitations of the **instrument itself**, not uncertainty in our extraction.

**Good:**
`Other substances may produce the same reaction; degradation can suppress a true signal; a positive signal does not establish the event that produced the residue.`

A useful extraction should normally contain at least one meaningful limit.

---

# Extraction record

This section is metadata. It is **not part of the instrument schema** and must not be used as an extra field during structural comparison unless an experiment explicitly calls for it.

```yaml
extraction:
  id:
  name:
  practice:
  source:
  status:
  ambiguities: []
  extraction_failures: []
  notes:
```

### `id`

Stable catalogue identifier.

Example:

```yaml
id: FORENSICS-LUMINOL-001
```

### `name`

Human-readable name of the source instrument.

Example:

```yaml
name: Luminol latent-trace detection
```

### `practice`

Practice from which it was extracted.

Example:

```yaml
practice: Forensic investigation
```

### `source`

Where the procedure was learned or verified. Provenance only; source terminology should not leak into the abstract schema unnecessarily.

### `status`

Use one of:

```text
accepted
provisional
rejected
```

* **accepted** — mechanism can be expressed coherently in all five fields.
* **provisional** — probably an instrument, but one or more structural questions remain.
* **rejected** — candidate could not be reduced to a coherent operational instrument.

---

## Recording ambiguity

Use `ambiguities` for uncertainty about the **extraction**, not limitations inherent to the instrument.

Format:

```yaml
ambiguities:
  - field: signal
    issue: >
      It is unclear whether the relevant signal should be the immediate
      chemical response or the spatial pattern formed by multiple responses.
    alternatives:
      - "Individual visible reaction"
      - "Distribution of visible reactions across the examined surface"
```

Common ambiguity types:

* unclear boundary between `state` and `operation`;
* multiple plausible abstraction levels;
* one named technique may actually contain several instruments;
* unclear whether an observation is a `signal` or already an `inference`;
* source practice disagrees about what a signal licenses;
* abstraction removes so much structure that the instrument becomes generic.

Do **not** resolve ambiguity by creating another schema field.

---

## Recording extraction failures

Use `extraction_failures` when the candidate cannot cleanly satisfy the frozen schema.

Format:

```yaml
extraction_failures:
  - type: composite
    description: >
      The named practice contains several distinct operations with different
      signals and inference rules and should probably be split.
```

Suggested failure types:

```text
not_operational
composite
no_distinct_signal
no_warranted_inference
no_meaningful_limit
overabstracted
underabstracted
domain_nouns_required
duplicate_mechanism
source_unclear
other
```

### Interpretation

**`not_operational`**
The candidate is a perspective, concept, metaphor, discipline, or principle rather than an instrument.

**`composite`**
Several separable instruments have been bundled together.

**`no_distinct_signal`**
The operation produces no identifiable observation distinct from the interpretation.

**`no_warranted_inference`**
Something is observed, but there is no clear epistemic relationship between observation and conclusion.

**`no_meaningful_limit`**
No known condition can be stated under which the inference would fail or mislead. This may indicate an empty heuristic rather than an instrument.

**`overabstracted`**
The extraction has become so generic that many unrelated instruments collapse into the same representation.

**`underabstracted`**
The extraction still depends on source-domain entities that are not structurally necessary.

**`domain_nouns_required`**
Removing source-specific vocabulary destroys the explanation of how the instrument works.

**`duplicate_mechanism`**
The candidate appears operationally indistinguishable from an existing catalogue entry despite having a different source-domain name.

**`source_unclear`**
The actual procedure or its inferential warrant cannot be established confidently enough to extract.

---

# Admission checks

Before marking an instrument `accepted`, apply these tests.

### 1. Operation test

Can you answer:

> What is actually done?

If not, reject as `not_operational`.

### 2. Signal test

Can you distinguish:

> what is observed

from:

> what that observation means?

If not, record `no_distinct_signal` or revise the extraction.

### 3. Noun-removal test

Remove the source-domain terminology.

Does the mechanism still make sense?

If not, record `domain_nouns_required` or `underabstracted`.

### 4. Misleading-signal test

Can you describe at least one circumstance in which the signal would fail to support the intended inference?

If not, inspect for `no_meaningful_limit`.

### 5. Granularity test

Does the candidate contain one coherent operation/signal relationship?

If several independent ones exist, mark `composite` and split them.

---

# Example

```yaml
extraction:
  id: FORENSICS-LUMINOL-001
  name: Luminol latent-trace detection
  practice: Forensic investigation
  source: "Verified forensic reference"
  status: accepted
  ambiguities:
    - field: signal
      issue: >
        The primitive signal may be treated as an individual visible reaction,
        while spatial distribution becomes a higher-order observation.
      alternatives:
        - "Visible reaction at a location"
        - "Spatial pattern of reactions"
  extraction_failures: []
  notes: >
    Keep event reconstruction outside the instrument. Luminol detection and
    bloodstain-pattern reconstruction are separate instruments.

instrument:
  state: >
    A past event may have left a persistent residue that is not visible
    through ordinary inspection.

  operation: >
    Apply a probe that selectively interacts with material associated with
    the suspected residue.

  signal: >
    Responsive material produces an otherwise absent observable reaction.

  inference: >
    The reaction supports the presence and location of material capable of
    producing that response.

  limit: >
    Unrelated material may produce the same response, relevant material may
    fail to respond because of degradation or removal, and detection of a
    residue does not by itself establish the event that produced it.
```

## Extraction rule

The final catalogue entry should always preserve this separation:

```text
SOURCE / PROVENANCE / UNCERTAINTY
             │
             ▼
      extraction record

STATE → OPERATION → SIGNAL → INFERENCE
                         ▲
                         │
                       LIMIT

       frozen comparable instrument
```

Ambiguity about our representation stays outside the five fields.

Failure modes inherent to the instrument belong in `limit`.

Failure to successfully extract an instrument belongs in `extraction_failures`.

