# Experiment spending and usage approval

Before any future paid or subscription-backed model experiment, follow
[the budget gate workflow](docs/EXPERIMENT-BUDGET-GATE.md). This also applies to
headless Codex and automatic credit top-ups. A request to conduct an experiment
does not waive the separate budget gate.

- Present a cumulative forecast of all stages, sessions and estimated cost before
  the first launch. Unknown cost or fan-out requires approval, not a zero estimate.
- Also run the [included-usage preflight](docs/USAGE-FORECAST.md) using fresh account
  percentages/reset times and matched before/after calibration. Present predicted
  percentage points, share of remaining allowance, reserve and LOW/BORDERLINE/HIGH/
  UNKNOWN scenarios. A nonzero usage-forecast exit requires explicit user review
  and approval before work proceeds; financial approval alone does not waive it.
  Refresh before each stage and at bounded batch checkpoints. Never turn dollars
  into quota percentages without evidence, invent exhaustion probabilities, launch
  calibration probes without authorization, or consume reset credits automatically.
  The user confirmed a 10-percentage-point reserve; do not lower it without their
  direction.
- Use `scripts/experiment_budget.py` before **every model session**, either its
  `launch` command or the `Gate.reserve` API inside each runner worker immediately
  before provider launch. Never wrap a whole multi-session runner as one session.
- Stop and request user approval when `check`/`reserve` denies. Never approve your
  own plan, raise thresholds, delete/reset the ledger, invent a cheaper estimate,
  rename an experiment/stage to reset consumption, or pipe an approval response.
- Approval must reference the exact displayed plan hash, known/unknown cost and
  session limits. Record consent only after the user actually grants it. A chat
  approval can be recorded through `Gate.approve` with the conversation reference;
  autonomous calls to that method without such consent are forbidden.
- Reforecast after generation/atomization and before evaluation fan-out. Include
  all earlier stages and reservations, even failures and uncertain launches.
- Update forecasts when token usage or observed costs indicate underestimation.
  Record reliable per-session costs with `observe-cost`; do not guess that token
  counts equal billed dollars or that subscription allowance means free usage.
- Budget approval never clears scientific terminal states or authorizes retries.
  H.6 and other frozen experiments remain unchanged; do not run legacy launchers
  directly. Any authorized future continuation needs a prospectively verified
  adapter that includes this gate and retains the original scientific checks.

Offline preparation, forecasts, tests and reviews do not require spending approval.
