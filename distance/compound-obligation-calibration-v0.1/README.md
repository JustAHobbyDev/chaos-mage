# H6.R2 — Claim origin/function + compound-obligation calibration v0.1

Base: c48f06aa32c03674a6c509ec5e631ce7a700b633.
Branch: experiment-h6r2-compound-obligations.
Read PROTOCOL.md, CLASSIFICATION.md, OBLIGATIONS.md and CONTRACTS.md.
Preparation is not measurement completion. See STATUS.md and checkpoints.json.

Offline: `python -B runner.py verify` and
`python -B -m unittest discover -s tests -p 'test_*.py'` (from this directory).
Runner prepare/freeze stages: classification, obligation, evaluation.
Run is explicit and requires committed packets plus financial and fresh usage gates.
No automatic approval or recovery command exists. Hidden hypotheses never enter
provider packets; operator audit is available only after all measurement freezes.
