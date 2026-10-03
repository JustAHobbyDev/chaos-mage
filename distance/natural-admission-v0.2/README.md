# H7 — Natural-transfer admission pilot v0.2

Status: **CLASSIFICATION_COMPLETE_DISCOVERY_READY**.
All six generations, atomizations and classifications are frozen: 326 atomic claims. No retries,
replacements or quarantines. Scientific admission remains pending for all six.
H6.R4 remains return-gate INCOMPLETE.

The six-mapping stop and UNMEASURED recovery boundaries remain in PROTOCOL.md.
The usage-policy amendment requires usage approval only below 30% current remaining
allowance; stale/missing readings need refresh. The 10-point planning reserve remains.
Original scientific inputs, observations and freezes are preserved.

Current cumulative budget plan: `budgets/plan-004.json`. All 18 prior reservations
and all future stages remain included: 36 known sessions plus unknown evaluation
fan-out. Costs remain unknown. The user's unified approval direction supersedes
independent financial, stage and revised-plan approval requirements. Continue the
authorized H7 stages at 30% or above; below 30% requires actual consent.
`unified-gate-amendment.json` preserves the previous freezes and binds the policy
and adapter changes. No scientific provider observation changed.

The runner now supports generation, claims, classification and discovery. The role
stage extension was prepared offline and installed only after all initial sessions
and their outputs froze. `role-stage-amendment.json` binds changed harness/config
bytes; `role-stage-static-freeze.json` binds new prompts, schemas, definitions,
preparation/routing code and tests. Requested model, reasoning and isolation remain
Astra/high, fresh one-packet contexts, serial batches of at most two, no retry.

```sh
python -B distance/natural-admission-v0.2/runner.py verify
python -B -m unittest discover -s distance/natural-admission-v0.2/tests -v
python -B scripts/experiment_budget.py check --plan distance/natural-admission-v0.2/budgets/plan-004.json
```

Capture fresh account readings before every stage/batch and every reservation.
Preserve account snapshots and usage under `.runtime/`; exclude confounded
observations from clean calibration. Unknown cost is not zero cost.

Each reviewed batch contains `authorization_reference`, `stage`, `packet_ids`,
`plan_sha256`, `snapshot_path`, `snapshot_sha256`, `calibration_path`,
`calibration_sha256`, `usage_plan_path`. Only below 30%, add `usage_approved: true`
and actual `usage_consent_reference`, and record actual consent in the shared gate.
The runner checks fresh readings, plan binding, frozen order and integrity.
Then use `runner.py run-batch --review <review-path>`.

Classification packets contain all frozen claims, unchanged target/source material,
H.5 mapping/source spans and the existing origin/function definitions. Source IDs
are disjoint within each packet: T for target, S for source and P for mapping.
Input roles are harness-owned; responses contain source IDs only.

After classification completes, `runner.py freeze classification` and commit.
Then `runner.py prepare-role discovery` and commit its packets before any discovery
session. After discovery completes, `runner.py freeze discovery` and commit.
`runner.py freeze-obligations` freezes mechanical routes, supplied-operation watch
records and evaluation fan-out. It never creates provider verdicts. Routing issues
leave the evaluation count unresolved and require the existing quarantine/recovery
policy; they cannot become scientific CORE_INVALID.

Reforecast all cumulative stages after discovery, including all previous reservations,
and obtain required approval before any claim evaluation. The current adapter has
no evaluation launch command. Later admission stages remain to be implemented and
frozen before use. No recommendation, integration or further experiment is authorized.

See [progress report](../review/natural-admission-v0.2.md).
