# H.5 — Neutral span provenance calibration

Offline instrumentation over 18 frozen H.4 mappings and two H.3 regressions.
Zero provider calls; historical observations stay unchanged.

See [protocol](PROTOCOL.md), [contract](PROVENANCE-CONTRACT.md), and
[segmentation policy](SEGMENTATION.md). Engineering semantic reviews are recorded
Codex judgments, not independent ratings or an automatic entailment evaluator.

Commands (from repository root):

```sh
python -B -m unittest discover -s distance/span-provenance-calibration-v0.1/tests -p 'test_*.py'
python -B distance/span-provenance-calibration-v0.1/calibrate.py verify
```

The final report is [here](../review/span-provenance-calibration-v0.1.md).
