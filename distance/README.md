# Ontological distance research prototype

This independent experiment asks how much a target's ordinary representation
changes when an existing operational instrument is imported. It does not change
the five-field schema or participate in retrieval.

- [Classifier definitions and response contract](CLASSIFIER-v0.1.md)
- [Frozen calibration protocol](PROTOCOL-v0.1.md)
- [Cases](cases/) and [instrument provenance](provenance.yaml)
- [Execution configuration](execution-config.json) and [output schema](output.schema.json)
- [Calibration report](review/calibration-v0.1.md)

Requirements: Python 3.11+, dependencies in `requirements.txt`, and authenticated
Codex CLI for live measurements. Existing authentication is used; no credential is
read or copied by this harness. No SSH is involved.

```sh
python -m pip install -r distance/requirements.txt
python distance/harness.py validate
python -m unittest discover -s distance -p 'test_*.py'
python distance/harness.py verify
python distance/harness.py run                     # offline, no calls
python distance/harness.py analyze                 # reproduce published metrics
```

The initial experiment used this sequence:

```sh
python distance/harness.py freeze                  # exclusive; only before first run
# Commit the frozen inputs before execution.
python distance/harness.py run --execute           # 40 independent processes, max 3 at once
python distance/harness.py freeze-results          # requires all 40 valid results
python distance/harness.py publish                 # byte-identical frozen response copies
python distance/harness.py analyze
```

`--case CASE-001 --replicate A` restricts execution. Successfully completed
reservations are skipped on continuation; incomplete/failed reservations stop
continuation and require a documented protocol amendment, never deletion. Do not
rerun this named experiment into its frozen snapshot; use a new version/runtime
root for future replications. Raw local runs remain under `.runtime/distance-v0.1/`.
Published responses and both freeze manifests permit offline checking of the
report without provider access. Raw event hashes bind the retained audit logs.

Reference labels are created only after the automated freeze and are qualitative
expectations, not training labels or an accuracy oracle. See their provenance in
the review directory. No numerical class thresholds are defined.
