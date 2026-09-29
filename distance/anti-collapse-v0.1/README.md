# Experiment D — Anti-collapse gate v0.1

Research-only, neutral-only benchmark. Six frozen native baselines, 24 matched designs,
unchanged validity admission, then permissive anti-collapse judgment. Only CLEAR_COLLAPSE
rejects. Operator design intentions are not reference truth. See PROTOCOL.md.

Run commands with `python -B distance/anti-collapse-v0.1/runner.py`:

- `validate`, `prepare`, `verify`
- `preflight` (after preparation commit)
- `run --stage validity`, `freeze --stage validity`, `publish --stage validity`, `admit`
- `run --stage anti-collapse`, `freeze --stage anti-collapse`, `publish --stage anti-collapse`
- `analyze`, `verify-results --private`

Commit each checkpoint specified in the protocol. Collection, freeze, preparation and
publication use exclusive writes; never rerun them over existing artifacts. `verify`
and `verify-results` are read-only. A failure requires `freeze-failure`, reporting and
an explicit subsequent authorization before recovery. Failed validity is attrition,
not a retry opportunity. Insufficient coverage stops anti-collapse measurement.

Tests: `python -B -m unittest discover -s distance/anti-collapse-v0.1/tests -p 'test_*.py'`.
Completion: `python -B distance/anti-collapse-v0.1/verify_completion.py --private`.
No diversity, grounding, retrieval, production changes or follow-on experiment.
