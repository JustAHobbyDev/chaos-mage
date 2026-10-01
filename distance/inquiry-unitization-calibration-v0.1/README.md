# Experiment H.4 — Inquiry-unitization and mandatory role coverage v0.1

18/18 fresh GPT-6 Astra/high judgments are preserved. See the [full report](../review/inquiry-unitization-calibration-v0.1.md) for validation findings and limits.

The deterministic scanner finds 13 complete units across the 18-case calibration corpus
and one in each of the two offline H.3 fixtures. H.3 artifacts remain unchanged.

- [Frozen rule](INQUIRY-UNIT.md), [protocol](PROTOCOL.md), [bounded grammar](LANGUAGE.md)
- [Case manifest](manifest.json), [authoring gate](review/authoring-gate.json)
- [Coverage results](coverage/summary.json), [metrics](metrics.json)
- [Post-freeze operator review](review/operator.json)

```sh
python -B -m unittest discover -s distance/inquiry-unitization-calibration-v0.1/tests -p 'test_*.py'
python -B distance/inquiry-unitization-calibration-v0.1/runner.py verify-results
python -B distance/inquiry-unitization-calibration-v0.1/publication.py verify
```

Publication is restricted to experiment-h4-inquiry-unitization. No recommendation was
executed; no historical measurement, natural-output experiment or production policy changed.
