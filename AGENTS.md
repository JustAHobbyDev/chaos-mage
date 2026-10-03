# Experiment spending and usage approval

Before any future paid or subscription-backed model experiment, follow
[the budget gate workflow](docs/EXPERIMENT-BUDGET-GATE.md). This also applies to
headless Codex and automatic credit top-ups. The user-directed rule of 2026-10-03
applies to **all experiment approval gates**: request approval only below 30%
current remaining allowance in any fresh quota window. Exactly 30% passes.

- Present a cumulative forecast of all stages, sessions and estimated cost before
  the first launch. Unknown cost or fan-out remains unknown, never zero, but does
  not independently require approval. Dollars, session totals, observed overruns
  and new plan hashes are advisory when allowance is at least 30%.
- Also run the [included-usage preflight](docs/USAGE-FORECAST.md) using fresh account
  percentages/reset times and matched before/after calibration. Present predicted
  percentage points, share of remaining allowance, reserve and LOW/BORDERLINE/HIGH/
  UNKNOWN scenarios. Usage approval is required only when a fresh quota window
  has less than 30% remaining (exit 2); exactly 30% does not require approval.
  Forecast risk and missing calibration are advisory. Invalid, missing or stale
  account readings require refresh (exit 1), not an approval override.
  There is no separate financial/stage/plan-revision approval trigger.
  Refresh before each stage and at bounded batch checkpoints. Never turn dollars
  into quota percentages without evidence, invent exhaustion probabilities, launch
  calibration probes without authorization, or consume reset credits automatically.
  The user confirmed a 10-percentage-point reserve; do not lower it without their
  direction.
- Collect usage calibration as routine bookkeeping around each already-authorized
  experiment batch: save before/after allowance snapshots, actual session counts,
  usage profile and available token totals, then refresh the forecast from matched
  observations. This collection is authorized; do not ask again merely to record
  it. Preserve reset-crossing, saturated or confounded observations with their
  exclusion reasons; never present them as clean calibration. Keep account data
  under `.runtime/`. Collection does not authorize extra model calls or reopen H.6.
- Use `scripts/experiment_budget.py` before **every model session**, either its
  `launch` command or the `Gate.reserve` API inside each runner worker immediately
  before provider launch. Never wrap a whole multi-session runner as one session.
- Stop and request user approval when the fresh allowance is below 30% and no
  applicable consent exists. Repair missing/stale readings and incomplete plans
  within existing task authority; those are not permission requests. Scientific
  stops, fixed sample limits and duplicate-session guards still apply. Never approve
  your own below-threshold plan, delete/reset the ledger, invent a cheaper estimate,
  rename an experiment/stage to reset consumption, or pipe an approval response.
- When below-threshold approval is needed, it must reference the displayed plan hash, known/unknown cost and
  session limits. Record consent only after the user actually grants it. A chat
  approval can be recorded through `Gate.approve` with the conversation reference;
  autonomous calls to that method without such consent are forbidden.
- Reforecast after generation/atomization and before evaluation fan-out. Include
  all earlier stages and reservations, even failures and uncertain launches.
  Within the authorized scientific task, revise plans and continue without renewed
  spending consent when current allowance remains at least 30%.
- Update forecasts when token usage or observed costs indicate underestimation.
  Record reliable per-session costs with `observe-cost`; do not guess that token
  counts equal billed dollars or that subscription allowance means free usage.
- Budget approval never clears scientific terminal states or authorizes retries.
  H.6 and other frozen experiments remain unchanged; do not run legacy launchers
  directly. Any authorized future continuation needs a prospectively verified
  adapter that includes this gate and retains the original scientific checks.

Offline preparation, forecasts, tests and reviews do not require spending approval.

# Evaluator-work stop rule

Follow [the evaluator-work stop rule](docs/EVALUATOR-STOP-RULE.md) before any new
evaluator, warrant, provenance, citation, classification, or admission calibration.
Every future evaluator-related experimental protocol must include the policy's
`## Evaluator-work gate` section, with concrete **Observed decision failure**,
**Admission consequence**, **Minimum intervention**, **Scientific success evidence**,
and **Stop condition** answers. If these cannot be filled concretely, do not start
the evaluator experiment. Apply the policy's natural-output return gate once the
specific defect is adequately resolved; representation/interface cleanup alone
does not justify further calibration. This policy does not authorize model calls,
waive budget/usage gates, or reopen frozen experiments.
