# Forecast included Codex usage — 2026-10-02

Before a run, compare its expected **percentage points of allowance** with the
remaining allowance in **every returned quota window**. Keep dollar costs and
credit reloads as a separate forecast: no fixed conversion from dollars or tokens
to percentage is established by the receipt data.

The [official app-server account interface](https://learn.chatgpt.com/docs/app-server)
documents `account/rateLimits/read`, including `usedPercent`, `windowDurationMins`,
`resetsAt` and available earned-reset count/details. The installed CLI supports
this read. No thread or model turn is needed. The script never calls the reset
redemption endpoint and never adds available reset credits to current capacity.

## Read the account and forecast

Use one stable local `--scope` label per account. Change it if you switch accounts.
Keep actual account snapshots/calibration under ignored `.runtime/`; do not commit
personal allowance, credit balances, identities or reset redemption IDs.

```sh
python -B scripts/codex_usage.py snapshot --scope my-codex-account \
  --out .runtime/usage-forecast/before.json
python -B scripts/codex_usage.py forecast \
  --plan path/to/budget-plan.json \
  --snapshot .runtime/usage-forecast/before.json \
  --calibration .runtime/usage-forecast/calibration.json \
  --reserve-points 10 --out .runtime/usage-forecast/forecast.json
```

Output files are exclusive-create; choose a new filename for each observation.
`forecast` exits 2 if any window has unknown, borderline or high risk to the
reserve; exit 0 means the observed-rate scenarios fit. This is a required
**pre-run review**, alongside the financial gate, not a live quota interceptor.
The financial gate still enforces per-session reservations. Future runners must
obtain/read a fresh allowance forecast before each stage and at bounded batch
checkpoints, present warnings and obtain explicit user consent when needed.
The allowance tool itself does not launch experiments or record approval.

Add a `usage_profile` to every nonempty stage in the plan, identifying model,
reasoning effort, task/stage and comparable context/output size, for example
`astra-high-h6-like-claim-full-context`. A profile is a declared match, not an
automatic classification. Separate generation, atomization and evaluation.
The plan for an initial forecast includes every stage. For later forecasts of
remaining work, create a separate usage-only plan with remaining session counts;
retain the complete cumulative plan for the financial gate. Never omit work from
the financial plan to reset spending or session reservations.

## Calibration without extra model calls

Start with `{"version": 1, "samples": []}`. No calibration means unknown; it does
not mean the work consumes zero allowance. Capture before/after readings around
an **already-authorized**, representative batch and record the number of sessions.
Use normal planned work; do not launch paid probes simply to fill this file.
Append a sample with this structure (snapshots are embedded in full):

```json
{
  "usage_profile": "astra-high-h6-like-claim-full-context",
  "isolated_account_work": true,
  "sessions": 20,
  "before": {"...": "snapshot object from before this batch"},
  "after": {"...": "snapshot object from after this batch"}
}
```

`isolated_account_work` is an explicit operator attestation: no other ChatGPT/
Codex work consumed the same allowance during the measured batch. Do not mark it
true merely because the experiment used isolated model contexts. If concurrent
account activity, delayed telemetry or incomplete session attribution is known,
exclude that sample and collect evidence during another authorized batch. Allow
telemetry to settle; do not treat a coarse unchanged percentage as proof of free
work. Record total sessions, including failed ones that may have consumed usage.

The implementation matches account scope, plan type, bucket, window duration and
profile. It rejects samples that cross a reset, decrease usage, saturate at 100%,
are future-dated, are older than 30 days, or have unattributed concurrent work.
Matching a window type across two different historical reset periods is allowed;
the before/after pair itself must be within one period. Calibration is transferable
only while model/account/task behaviour remains comparable.

## Arithmetic and uncertainty

For each matched batch:

```text
observed points per session = (after.usedPercent − before.usedPercent) / sessions
remaining points = 100 − current.usedPercent
usable points = max(0, remaining points − reserve points)
run points = sessions × points per session, summed across stages
share of remaining allowance = 100 × run points / remaining points
```

Each batch rate allows ±1 percentage point on its measured difference for coarse
telemetry. Use the lowest observed lower rate and highest observed upper rate,
with 25% extra headroom on the upper estimate. This yields planning scenarios,
**not a confidence interval or a numerical probability of exhaustion**. One batch
can yield a provisional range but cannot support statements such as “90% likely
to finish.” Rates may change with prompt lengths, model/reasoning, cache behaviour,
account limits and other activity. Every stage and every returned window must be
covered; an uncalibrated model-specific bucket remains unknown rather than ignored.

The user-confirmed reserve is **10 percentage points** of a full allowance, not
10% of what remains. The CLI reads this default from
`experiment-budget-policy.json`. Changing it through `--reserve-points` requires
user direction; agents must not lower it to get a run through.

| Result | Meaning | Pre-run action |
|---|---|---|
| LOW | All upper scenarios fit after the reserve | May proceed if all other gates pass |
| BORDERLINE | Some scenarios consume the reserve | Ask approval; consider a smaller authorized batch |
| HIGH | All lower scenarios exceed usable allowance | Ask approval; expect to split work or consider a reset |
| UNKNOWN | Missing/stale/unusable evidence | Ask approval with the uncertainty explicit |

The report separately identifies scenarios that exhaust allowance itself, reports
remaining percentages and per-profile sessions fitting after reserve, and shows
automatic-reset timing and available manual resets. A rough runtime based on
observed batch throughput flags runs that may cross a scheduled reset. It assumes
neither a mid-run reset nor a specific effect of redeeming a credit. If waiting for
or manually redeeming a reset, fetch a new snapshot and reforecast. Never spend
an earned reset automatically. Other account activity can invalidate a forecast.

Current snapshots expire for forecasting after five minutes. A scheduled reset
already in the past also forces refresh. These freshness checks do not pretend to
monitor a run after its preflight. At each batch boundary, refresh and stop further
scheduling if the remaining forecast no longer fits the reviewed allowance.

## H.6 limitation

H.6 retained 773 session starts and exposed token usage, but no before/after quota
percentages. The nine reload receipts calibrate a rough cash-consumption proxy;
they cannot recover percentage points per claim judgment. The first implementation
therefore reports UNKNOWN for an H.6-like percentage forecast until valid
calibration exists. Account reads and offline tests introduce no new model work.

```sh
python -B -m unittest discover -s scripts -p test_codex_usage.py
```
