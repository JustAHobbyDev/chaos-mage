# H.6 natural admission

18 fixed natural mappings, Astra/high only, H.5 spans and H.4 inquiry units.
See [protocol](PROTOCOL.md), [review rubric](REVIEW-RUBRIC.md), and
[collision preflight rules](COLLISIONS.md). Historical artifacts remain read-only.

Offline: `python -B distance/natural-admission-v0.1/runner.py verify`
Tests: `python -B -m unittest discover -s distance/natural-admission-v0.1/tests`
Execution: prepare each stage, commit, run, freeze, commit before the next stage.
No provider call is made by verification or tests.
