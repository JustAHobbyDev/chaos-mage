# H7 — Natural-transfer admission pilot v0.2

Status: **GENERATION_AND_ATOMIZATION_COMPLETE_AWAITING_ROLE_STAGE_APPROVAL**.
All six generations and all six atomizations are frozen: 326 claims. No retries,
replacements or quarantines. Scientific admission remains pending for all six.
H6.R4 remains return-gate INCOMPLETE.

The six-mapping stop and UNMEASURED recovery boundaries remain in PROTOCOL.md.
The usage-policy amendment requires usage approval only below 30% current remaining
allowance; stale/missing readings need refresh. The 10-point planning reserve remains.
Original scientific inputs, observations and freezes are preserved.

Current budget plan: `budgets/plan-003.json`. It retains all 12 prior reservations
and all future stages. Next requested scope: six classification and six direct
obligation-discovery sessions, with unknown dollars. Evaluation fan-out is still
unknown and cannot be dispatched. Plan 002's consent covered generation/atomization.
No approval for plan 003 has been recorded.

The runner now supports generation, claims, classification and discovery. The role
stage extension was prepared offline and installed only after all initial sessions
and their outputs froze. `role-stage-amendment.json` binds changed harness/config
bytes; `role-stage-static-freeze.json` binds new prompts, schemas, definitions,
preparation/routing code and tests. Requested model, reasoning and isolation remain
Astra/high, fresh one-packet contexts, serial batches of at most two, no retry.

```sh
python -B distance/natural-admission-v0.2/runner.py verify
python -B -m unittest discover -s distance/natural-admission-v0.2/tests -v
python -B scripts/experiment_budget.py check --plan distance/natural-admission-v0.2/budgets/plan-003.json
```

The budget check must deny until actual consent is recorded. Never reuse an old
plan's approval reference as consent to a new plan. Unknown cost is not zero cost.
After actual approval, capture fresh account readings before each stage/batch;
construct the usage-only batch plan from the current cumulative stage with its
session count set to one or two. Preserve before/after account snapshots and usage
under `.runtime/`; exclude confounded observations from clean calibration.

Each reviewed batch file contains `consent_reference`, `financial_approved`,
`stage`, `packet_ids`, `plan_sha256`, `snapshot_path`, `snapshot_sha256`,
`calibration_path`, `calibration_sha256`, `usage_plan_path`. Only below 30%, add
`usage_approved: true` and an actual `usage_consent_reference`. The runner independently
checks fresh readings, plan binding, stage order, frozen hashes and the shared gate.
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
