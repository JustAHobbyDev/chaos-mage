# Experiment budget approval — 2026-10-02

The gate warns and refuses new sessions when the **whole experiment** forecast
exceeds $10 or 100 sessions, or any stage has unknown cost or session count.
These are provisional defaults in `experiment-budget-policy.json`; thresholds
must not be raised by an agent to get a run through. Equality is allowed.

The separate [included-usage forecast](USAGE-FORECAST.md) compares expected
percentage-point consumption with current remaining quota and reset timing. Run
both preflights; neither dollars nor automatic reloads establish usage percentage.

This controls prospective experiments. Historical H.6 inputs, runner, outputs,
freezes and terminal status are unchanged. Installing the gate launches no model.

## What the warning means

Reports display each stage, known total sessions, known estimated dollars,
whether either total is incomplete, the plan/policy hashes, reserved sessions,
approval reference, and blocking reasons. Unknown amounts are never priced at
zero. Forecasts must include generation, claim extraction, **every claim judge**,
downstream stages, and any protocol-authorized probes or retries. A Codex session
may itself make multiple provider requests; session counts are not invoice counts.

This is **not a guaranteed dollar cap or a top-up monitor**. The gate has no
provider billing/credit-card feed and cannot see concurrent usage outside this
ledger, provider-internal retries, or actual final token consumption. Cost estimates
must state their basis: current applicable prices or observed charges for comparable
work, input/output size assumptions, cache treatment and a conservative margin.
If those are not established, use `null` and get explicit approval of bounded
sessions with unknown cost. Do not infer a credit price from API token prices.
Provider account spending/top-up settings remain a separate control.

## Initial empirical calibration

The user reported nine deduplicated automatic reloads totaling **$45.88** between
11:57:24 PM CDT October 1 and 12:24:15 AM CDT October 2, 2026 (1,611 seconds).
The later failed reload is excluded. Local H.6 records show 276 claim sessions
starting and 276 exiting in that window. All nine reloads imply $1.71/minute;
excluding the first boundary reload gives $1.52/minute. Dividing by 276 yields a
rough **$0.15–$0.17 per claim session** cash-reload proxy, not itemized billing.

Use **$0.20 per comparable claim session** as an initial conservative planning
allowance. Thus 50 such sessions forecast $10 and 100 forecast $20, before other
stages. Explicitly cite [the calibration record](experiment-budget-calibration.json)
in `estimate_basis`. Generation, atomization, different models/prompts and much
larger/smaller contexts still need their own estimate or explicit unknown-cost
approval. This allowance is not a guaranteed maximum. Update it when new
observations demonstrate underestimation; do not silently lower it to evade review.

The H.6 retrospective forecast now illustrates 1,042 × $0.20 = **$208.40 for the
claim stage alone**, with other stages unknown. This is a prospective scenario
at the expensive window's allowance, **not an estimate of the actual H.6 bill**.
The reported $45.88 purchased credits, and account balance/usage outside the
window has not been reconciled. A forecast can still trigger useful approval
without pretending those uncertainties are resolved.

## Prepare and check

Create an experiment-owned JSON plan. Example shape:

```json
{
  "version": 1,
  "experiment_id": "example-new-study",
  "description": "Describe the complete study and stages",
  "execution_fingerprint": "Hash of runner, prompts, schemas, model/reasoning config and frozen inputs",
  "execution_allowed": false,
  "stages": [
    {"id": "generation", "sessions": 6, "estimated_cost_usd": null},
    {"id": "claim-judgments", "sessions": null, "estimated_cost_usd": null}
  ]
}
```

Set `execution_allowed` to true only for an otherwise authorized experiment.
That flag is not budget approval. The execution fingerprint must be updated for
changed scientific inputs/configuration; the runner retains responsibility for
verifying those files. For known costs, add a nonempty `estimate_basis` to each
stage. Use decimal dollar strings. Session counts must be nonnegative integers
or null. Approving an unknown future count does not allow dispatch of that stage:
resolve the count, revise the plan and pass the gate again first.

```sh
python -B scripts/experiment_budget.py check --plan path/to/budget-plan.json
```

Exit 2 means stop and ask the user. Exit 0 means the budget gate currently allows
the forecast; it does not override scientific authorization or stage quotas.
After claim extraction, reforecast all stages before any evaluation launch.
Approvals bind the entire plan and policy hashes. Changed approved forecasts
above threshold need fresh approval; changes falling within the automatic
thresholds follow normal under-threshold policy. Do not omit completed stages.

## Approve and launch

The researcher can approve from an interactive terminal after reviewing the
report. They must type `approve <full-plan-sha256>`; no piped approval or `--yes`
flag exists. Record a meaningful authorization reference:

```sh
python -B scripts/experiment_budget.py approve \
  --plan path/to/budget-plan.json --reference 'Researcher reviewed displayed plan'
```

An agent must first ask for explicit user consent to the concrete forecast.
Consent given in chat can be recorded by `Gate.approve(plan, policy, reference)`
with the actual conversation reference. This is an operator workflow, not a
security boundary against someone who controls the repository and ledger.

For **one session only**:

```sh
python -B scripts/experiment_budget.py launch \
  --plan path/to/budget-plan.json --stage generation --session target-01 \
  -- codex exec --sandbox read-only - < request.txt
```

Alternatively a runner imports `Gate`, calls `reserve(plan, policy, stage,
session_id, command_argv)` immediately before each provider launch, then calls
`finish(experiment_id, session_id, returncode)` afterwards. For direct API calls,
use a descriptive non-secret argv-style transport identifier in the reservation.
Never include credentials in argv or this ledger. Existing protocol, isolation,
commit, hash, and terminal-state checks still run. Do not treat budget denial as
a provider observation: it occurs before dispatch and is a scheduling pause.

The shared SQLite ledger at `.runtime/experiment-budget.sqlite3` serializes
concurrent reservations. Keep this same ledger and experiment ID across stages,
process restarts and plan revisions. Archive it with experimental evidence.
`--ledger` exists for offline tests/isolated projects, not for resetting a budget.
There is no reservation refund, automatic retry or unblock command. Failed,
crashed, canceled and uncertain launches conservatively retain their slots.

## During execution

The reservation quota is enforced at every launch. In-flight work can finish
when the gate stops new scheduling. Keep concurrency modest because those calls
cannot be retroactively prevented. Check observed token usage after each batch;
revise an underestimated forecast before scheduling more work. Runners with
reliable per-session dollar observations should report them immediately:

```sh
python -B scripts/experiment_budget.py observe-cost \
  --experiment example-new-study --session target-01 --usd 1.25
```

Known stage estimates are divided evenly across their declared sessions. For
heterogeneous costs, define separate stages/cost bands. An observed per-session
cost above its allowance causes the projected stage cost to exceed its forecast
and blocks the next launch, even with an existing approval. Missing observations
retain the allowance, and lower actual costs do not refund it. Reforecast with
adequate headroom and seek renewed approval when required. Do not assign a
whole top-up charge to a single session without supporting billing evidence.

A scientific terminal stop can additionally be mirrored as a permanent ledger
block, which budget approval cannot remove:

```sh
python -B scripts/experiment_budget.py block \
  --experiment example-new-study --reason 'Terminal scientific stop; see incident record'
```

This new gate is mandatory for future runners through root `AGENTS.md`; it is not
retroactively inserted into frozen legacy runners. Directly invoking a legacy
runner bypasses the code and is prohibited by the workflow. New runners must test
that every launch path, including retry paths if authorized, reserves first.

## Offline verification

```sh
python -B -m unittest discover -s scripts -p test_experiment_budget.py
python -B scripts/experiment_budget.py check \
  --plan docs/experiment-budget-h6-retrospective.json
```

The second command intentionally exits 2: 1,114 forecast sessions, $208.40 for the
claim-stage scenario and other stage costs unknown; approval required. This
illustrative plan is explicitly non-executable, including
after approval. It neither changes nor reopens H.6.
