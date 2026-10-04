# H7 — Natural-transfer admission pilot v0.2

Status: **COMPLETE**. End-to-end scientific admission **3/6**; final local
quarantine **3 UNMEASURED**. No pending scientific work. The fixed six slots,
all original observations and earlier pauses are preserved.

| Mapping | Admission | Instrumentation |
| --- | --- | --- |
| H7-T01-1 | KEEP_WITH_REDUCED_SCOPE | CLEAN |
| H7-T01-2 | UNMEASURED — discovery no-observation | FAILURE |
| H7-T02-1 | UNMEASURED — unresolved discovery routing | FAILURE |
| H7-T02-2 | UNMEASURED — discovery no-observation | FAILURE |
| H7-T03-1 | KEEP_WITH_WARRANT_FLAGS | WARNING |
| H7-T03-2 | KEEP_WITH_REDUCED_SCOPE | CLEAN |

211 unique provider attempts, 209 validated responses, 181 contract judgments.
Thirty-seven claims were ablated from the three evaluated mappings; 32 definite
viable candidates and five complete inquiry units survived. Neither timeout was
retried or replaced. H7-T01-2 received no downstream provider call.

- [Final report, with original pause report preserved](../review/natural-admission-v0.2.md)
- [Authorized no-observation continuation and independence proof](CONTINUATION.md)
- [Final metrics](metrics-final.json)
- [Operator audit](review/operator-audit-final.json)
- [Continuation checkpoint SHAs](review/continuation-checkpoints.json)
- [Final run closure](review/run-complete.json)
- [Frozen scientific protocol](PROTOCOL.md)
- [Prospective recovery policy](../../docs/EXPERIMENT-RECOVERY-POLICY.md)
- [Final cumulative plan](budgets/plan-007.json)

The original protocol's provider pause clause is superseded only by the authorized
continuation record. Usage approval remains required only below 30% fresh remaining
allowance. H6.R4's return gate remains INCOMPLETE. No historical experiment reopened.

Offline preservation check:

```sh
python -B distance/natural-admission-v0.2/runner.py verify
```

H7 is closed. The report recommends a separately authorized target-facing assessment;
it has not been executed. No evaluator calibration, main merge or production work.
