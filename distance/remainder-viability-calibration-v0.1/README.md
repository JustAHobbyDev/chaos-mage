# Experiment H.2 — remainder-viability calibration v0.1

**Measurement complete; the intended boundary is not robustly calibrated.**
The experiment collected 57 claim and 16 artifact judgments in fresh GPT-6 Astra/high
contexts. Most intended core cases retained source-specific negative evidentiary
constraints that the operator authoring gate missed. The only measured CORE_INVALID
remains ambiguous in post-freeze review.

- [Full report and checkpoints](../review/remainder-viability-calibration-v0.1.md)
- [Protocol](PROTOCOL.md) and [frozen viability construct](VIABILITY.md)
- [Primary authoring audit](authoring-audit/primary.json)
- [Post-freeze operator audit](review/operator.json)
- [Derived metrics](metrics.json)

Observed statuses: 3 KEEP_WITH_WARRANT_FLAGS, 11 KEEP_WITH_REDUCED_SCOPE,
1 CORE_INVALID, and 1 UNCERTAIN_LOAD_BEARING. Seven case-design problems, three scope
alternatives and one ambiguous classification are reported without changing the model
outputs or hidden hypotheses. The operator review is not independent-rater evidence.

The tiny viable remainder and unresolved-relevance controls worked as intended.
Generic-only and target-irrelevant-only artifact controls were not achieved: negative
source-derived constraints survived. A new natural-output admission experiment is
not yet recommended.

Read-only verification from the repository root:

```sh
python -B distance/remainder-viability-calibration-v0.1/runner.py verify
python -B distance/remainder-viability-calibration-v0.1/publication.py verify
python -B -m unittest discover -s distance/remainder-viability-calibration-v0.1/tests -p 'test_*.py'
```

Provider execution is sealed by the final runtime freeze. No observation may be
repeated. The sole engineering recovery occurred before any request reservation;
see [positive non-contamination evidence](recovery/premeasurement-launch.json).
H.1 remains stopped before measurement, with zero provider calls. H/G/F and all
other inherited artifacts remain unchanged. Work and publication are restricted to
experiment-h2-remainder; no merge or further experiment is part of this publication.
