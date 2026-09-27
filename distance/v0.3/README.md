# Ontological transfer v0.3

**PREPARED / UNEXECUTED.** Conceptual refactor; classifier reliability untested.
Start with [the model](../MODEL-v0.3.md) and
[the refactor report](../review/model-refactor-v0.3.md).

- `candidate.schema.json`: fixed source, target/evidence and five-field mapping.
- `transfer.schema.json`: complete validity → displacement → grounding record.
- `validity.schema.json`: Experiment A response; no downstream classifications.
- `contracts.py`: strict offline validation and historical hash verification.
- `model-freeze.json`: concepts/contracts frozen before retrospective authoring.
- [Retrospective examples](examples/retrospective/README.md): twelve separately
  sourced A/B mapping interpretations, explicitly non-experimental.
- [Experiment A protocol](PROTOCOL-transfer-validity-v0.3.md): 24 packets, eight
  triplets, two future model families, 48 planned judgments, none collected.
- `CLASSIFIER-transfer-validity.md`: identical substantive instructions for judges.
- `operator-manifest.json`: synthetic provenance, design intent and contrast metadata;
  **never include this file in a judge context**. Intent is not ground truth.
- `execution-order.json`: fixed future order; not a record of executed runs.
- `preparation.json`: preparation-only inventory and SHA-256 hashes.

Use the existing pinned dependencies in `../requirements.txt`. From the repository
root, these commands make no model calls and do not change tracked artifacts:

```sh
python -B distance/v0.3/contracts.py preservation
python -B distance/v0.3/contracts.py candidate distance/v0.3/cases/001.json
python -B distance/v0.3/verify_preparation.py
python -B -m unittest discover -s distance/v0.3/tests -p 'test_*.py'
```

A retrospective file has an outer provenance/marker envelope; validate its `transfer`
object via `verify_preparation.py`, which also checks the envelope and historical
sources. A normal full response is simply `{"transfer": ...}`. `contracts.py validity`
accepts `--candidate PATH` to verify the case ID and original target question.

The in-memory `judge_packet` helper emits only fixed instructions plus an allowlisted
candidate. It has no provider or launch API. Future execution requires separate
authorization, an implemented isolated runner, verified provider configuration,
preflight and a committed execution freeze. No `run`, `execute` or calibration
command is provided in this version.
