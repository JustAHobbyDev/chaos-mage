# H7 — Natural-transfer admission pilot v0.2

Status: **PAUSED_PROVIDER_TIMEOUT**. The unified spending gate requires approval
only below 30% current remaining allowance; cost, unknown workload and revised
plan hashes do not independently block for consent. The gate change is `0cdf855`.

All six generations, 326 claims and all classifications are frozen. Discovery
completed for H7-T01-1, with 50 required contract judgments and one cleanly routed
supplied-operation watch. H7-T01-2 discovery hit the frozen 900-second timeout.
Its artifact is instrumentation FAILURE / scientific admission UNMEASURED.
The other five admissions remain pending. End-to-end completion is 0/6.

20 sessions launched; 19 responses succeeded. No role-specific evaluation,
ablation, remainder inventory or admission judgment has run. No retry,
substitution, replacement generation or sample expansion. H6.R4 remains INCOMPLETE.

The handoff's transport rule requires pause, preserve, no retry and report.
No provider-no-observation continuation policy is invented. The preserved runtime
state blocks further launches. Do not use the normal batch commands to bypass it.

- [Full pause report](../review/natural-admission-v0.2.md)
- [Frozen protocol, six-slot stop and UNMEASURED boundary](PROTOCOL.md)
- [Timeout evidence](review/discovery-timeout.json)
- [Partial discovery freeze](discovery-partial-freeze.json)
- [Checkpoint SHAs](review/checkpoints.json)
- [Current cumulative plan](budgets/plan-004.json)
- [Unified policy amendment](unified-gate-amendment.json)

Offline preservation check:

```sh
python -B distance/natural-admission-v0.2/runner.py verify
```

The report recommends resolving continuation policy before more scientific work.
That recommendation has not been executed. No merge to main or production work.
