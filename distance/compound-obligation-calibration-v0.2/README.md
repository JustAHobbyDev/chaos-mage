# H6.R3 — corrected compound obligations v0.2

Fresh calibration based exactly on H6.R2 terminal commit `5b6dd0e63b280118a6473fa25b3295af376f7a3c`. Historical experiments remain unchanged. See CORRECTIONS.md and PROTOCOL.md.

Current checkpoint: offline preparation; Stage A authorization pending. No provider observations exist yet. The complete Stage C projection barrier must be constructed from fresh frozen Stage B results, so it cannot be claimed passed from fixtures alone.

Commands (from repository root, with distance requirements installed):

```sh
python -B -m unittest discover -s distance/compound-obligation-calibration-v0.2/tests
python -B distance/compound-obligation-calibration-v0.2/runner.py verify
```

The runner offers prepare/freeze for classification, dependency, evaluation; resolve-dependencies after the committed dependency freeze; write-plan/forecast; explicitly gated run batches; record-batch; aggregate; metrics; seal-audit. Commit each freeze before the next stage. Actual user approval is separate from preparation and cannot be fabricated by the harness. Account readings/calibration remain under ignored .runtime/compound-obligation-calibration-v0.2.
