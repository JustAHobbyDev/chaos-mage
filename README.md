# chaos-mage

A research corpus for extracting **operational instruments** from diverse practices and testing whether their abstract mechanisms can later be compared, retrieved, and mapped across domains.

This repository is intentionally separate from `chaos-magick-engine`. The current phase is narrower: establish whether useful cross-domain instruments can be represented consistently before building retrieval, mapping, composition, or agent orchestration around them.

## Current phase

1. Freeze the minimal instrument schema.
2. Sample diverse practices.
3. Identify candidate instrument sets within each practice.
4. Extract instruments independently using the frozen schema.
5. Record ambiguity and extraction failures without modifying the schema.
6. Review the first batch before designing what follows.

No retrieval system, embeddings, database, or application code is in scope yet.

## Frozen schema v0.1

Every extracted instrument has exactly five comparable fields:

```yaml
instrument:
  state:
  operation:
  signal:
  inference:
  limit:
```

Definitions, admission checks, ambiguity handling, and extraction-failure recording are in [docs/instrument-extraction-v0.1.md](docs/instrument-extraction-v0.1.md). The frozen acceptance decision is in [docs/extraction-decision-rule-v0.1.md](docs/extraction-decision-rule-v0.1.md). The preregistered stress-batch thresholds are in [docs/calibration-thresholds-v0.1.md](docs/calibration-thresholds-v0.1.md). Borderline cases are resolved under [docs/adjudication-rule-v0.1.md](docs/adjudication-rule-v0.1.md).

## Repository layout

```text
docs/
  instrument-extraction-v0.1.md   # frozen extraction specification

practices/
  catalogue-v0.1.yaml             # seed practices and candidate instruments

instruments/                       # accepted/provisional/rejected extractions, added as work proceeds
```

The `instruments/` directory will appear when the first actual extraction is committed.

## Naming

- Files and directories: lowercase kebab-case.
- Versioned research specifications/catalogues: suffix with `-vMAJOR.MINOR`.
- Instrument files: `<practice-slug>--<instrument-slug>.yaml`.
- Stable extraction IDs inside instrument files: uppercase practice family + instrument + ordinal when needed, e.g. `FORENSICS-LUMINOL-001`.
- Source/provenance metadata stays outside the five-field comparable schema.

## Research discipline

A candidate is not admitted merely because it supplies an evocative metaphor. It must expose an operational chain:

```text
STATE --apply OPERATION--> SIGNAL --licenses--> INFERENCE
                                  ^
                                  |
                                LIMIT
```

The initial batch is meant to stress the schema. Recurring awkward fits are evidence about the representation and should be recorded rather than silently repaired by adding fields.

The next preregistered phase is [docs/retrieval-mapping-test-v0.1.md](docs/retrieval-mapping-test-v0.1.md), which tests schema-only cross-domain retrieval and mapping against a name/practice baseline.
