# Separate boundary experiment v0.2

Run from the repository root with Python and the pinned dependencies in
`../requirements.txt`. This harness never imports or modifies the v0.1 harness.

Preparation: `python distance/boundary-v0.2/harness.py validate`, `preflight`, then
`prepare`; run tests; commit all inputs. Execution: `run`, `freeze-results`,
`publish`, `analyze`. These commands reserve/write exclusively, so they are not
idempotent. `verify` and tests are read-only. No live calls occur in tests.

`CLASSIFIER-tested.md` is the immutable experimental text. The operator manifest,
protocol, order, provenance, controls and review never enter classifier packets.
`preservation.json` covers every previously tracked v0.1 artifact. `prepared.json`
fixes inputs, `results-freeze.json` fixes outputs and includes audit metadata.
Raw events remain under ignored `.runtime/boundary-v0.2/`.

Completed interpretation: `../review/boundary-calibration-v0.2.md`.
