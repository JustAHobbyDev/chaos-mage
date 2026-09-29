# Experiment E — Natural-output anti-collapse v0.1

Thirty fixed natural generations, cross-family blind neutralization, paired fidelity
audits, unchanged Valid/Valid admission and the frozen permissive anti-collapse gate.
See PROTOCOL.md for the preregistered boundaries and failure policy.

Use `python -B distance/anti-collapse-natural-v0.1/runner.py` with:

- `prepare`, `verify`
- `prepare-stage --stage STAGE`, `preflight --stage STAGE`
- `run --stage STAGE`, `freeze --stage STAGE`, `admit`
- `analyze`, `verify-results --private`, `freeze-failure`

Stages: generation, neutralization, audit, validity, anti-collapse. Commit each input,
probe and output freeze before the dependent operation. Writers are exclusive; never
rerun over existing artifacts. Verify commands are read-only and make no provider calls.

Tests: `python -B -m unittest discover -s distance/anti-collapse-natural-v0.1/tests`.
No follow-on experiment is authorized by these artifacts.
