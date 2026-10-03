# Experiment approval and accounting — updated 2026-10-03

The user directed that the recent allowance rule apply to **everything** in the
experiment approval workflow. Within an already-authorized scientific task, approval
is required only when **any fresh quota window has less than 30% remaining**.
Exactly 30% passes. This supersedes the former independent $10, 100-session,
unknown-cost/fan-out, overrun and changed-plan-hash approval triggers.

Costs and workload remain visible forecasts. Unknown values remain `null`, not zero.
The former dollar/session thresholds in `experiment-budget-policy.json` are now
advisory thresholds. The 10-percentage-point reserve remains a planning reference,
not another approval trigger. Do not translate dollars or tokens into quota points.

This policy does not authorize new scientific scope, expand fixed samples, reopen
H.6 or other terminal experiments, permit retries/substitution, bypass recovery,
redeem reset credits, or clear evaluator-work stops. Those constraints remain
independent of spending consent.

## Forecast and preflight

Retain one cumulative plan and experiment identity across all stages/revisions.
Include completed, failed and uncertain reservations; never reset the ledger or
rename stages to erase consumption. Record the execution fingerprint and update it
when scientific inputs, prompts, schemas, model configuration or runner change.
Refresh the forecast after atomization/discovery and before evaluation fan-out.
A revised plan within the existing task needs no new approval at 30% or above.

A plan contains version, experiment_id, description, execution_fingerprint,
execution_allowed and stages with id, sessions, estimated_cost_usd, estimate_basis
(for known costs) and usage_profile. Session counts may be null for future stages;
resolve the dispatched stage's count before launching it. Keep execution_allowed
false for retrospective/forecast-only examples. Approval cannot make those executable.

```sh
python -B scripts/experiment_budget.py check --plan path/to/budget-plan.json
```

`check` reads live account allowance without launching a model. Exit 0 means the
accounting/allowance checks pass. Exit 2 means fresh allowance is below 30% and
applicable consent is absent. Exit 1 means a data, freshness, bookkeeping or scientific
block needs resolution; it is not a request to approve away an integrity problem.
A fresh normalized snapshot may be supplied with the global `--usage-snapshot`
option for offline/read-only checks. Never manufacture account readings.

The [usage forecast](USAGE-FORECAST.md) still reports LOW/BORDERLINE/HIGH/UNKNOWN
scenarios, predicted percentage points, share of remaining allowance and reset timing.
Missing calibration and predicted reserve/exhaustion risk are advisory when current
remaining usage is at least 30%. Missing/stale/reset-crossed readings need refresh;
approval cannot substitute for current account data.

Account data, quota-bearing gate reports and calibration stay under ignored
`.runtime/`. The shared reservation ledger remains `.runtime/experiment-budget.sqlite3`.
The gate's fresh account reads are read-only; they start no model turn and redeem
no credits. Concurrent account activity can change allowance between observations.

## Each provider session

Every worker must reserve immediately before provider launch, using `Gate.reserve`
or the one-session CLI wrapper. The gate reads fresh allowance for each reservation;
there is no separate financial-approval flag in the H7 runner.

```sh
python -B scripts/experiment_budget.py launch \
  --plan path/to/budget-plan.json --stage generation --session target-01 \
  -- codex exec --sandbox read-only - < request.txt
```

Never wrap a multi-session runner as one reservation. The gate still rejects unknown
or exhausted stage counts, omitted/shrunk consumed stages, duplicate session identities,
forecast-only plans and scientific terminal blocks. Reconcile plans within existing
scope when needed; no permission request is implied merely by bookkeeping work.
A failed, crashed, cancelled or uncertain launch retains its reservation. Preserve
raw observations; use the repository recovery policy for any continuation.

After launch, call `finish(experiment_id, session_id, returncode)`. Reliable observed
costs should be recorded with `observe-cost`. An observed overrun is a warning to
reforecast; it does not independently stop for approval above the usage threshold.
Lower observed costs do not refund sessions or erase history. Never guess that a
whole credit top-up or token count is the cost of one session.

## Consent below 30%

Only when this threshold is crossed, present the current plan hash, cumulative
workload, known/unknown cost and current allowance, and request explicit consent.
Actual consent can be recorded using the interactive `approve` command or
`Gate.approve(plan, policy, reference)` with the real conversation reference.
No piped approval, invented consent or autonomous approval is allowed.
Below-threshold approvals remain bound to the exact plan/policy hashes. Above the
threshold, no approval record is needed and changed hashes do not block continuation.

Scientific authorization is still established by the user's assignment and scope.
The H7 handoff plus subsequent approval and this policy direction authorize continuation
of the fixed H7 task under this rule. They do not authorize a different experiment.

## Cost evidence and limitations

The existing [calibration record](experiment-budget-calibration.json) documents the
historical H.6 cash-reload proxy and $0.20 planning allowance for comparable claim
sessions. It is not itemized billing or a quota conversion. Generation, atomization
and materially different contexts remain unknown without matching evidence. Keep
those unknowns explicit; do not invent a cheap estimate to make a forecast look better.

The gate cannot observe every provider-internal request, automatic reload or concurrent
account activity. Session counts are not invoice counts. This is not a guaranteed
monetary spending cap. The user's chosen approval boundary is current usage remaining.

## Offline verification

```sh
python -B -m unittest discover -s scripts -p test_experiment_budget.py
python -B -m unittest discover -s scripts -p test_codex_usage.py
```

Tests inject synthetic account snapshots and launch only offline fixture commands;
no provider observations or calibration probes are involved. Frozen historical
scientific records and their old forecasts are not retroactively relabeled.
