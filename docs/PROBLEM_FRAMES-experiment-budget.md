# Experiment budget gate

## Entry #1 — 2026-10-02 — Forecast and per-session authorization

### Domains

The researcher is biddable and owns spending authorization. Existing experiment
plans, frozen scientific packets and model configurations are lexical inputs.
Runners are causal dispatchers, with concurrent workers. Provider serving, credit
balances and auto-reload billing are external domains the machine cannot fully
observe. User-reported receipt aggregates and exposed usage records are lexical
observations, not a direct billing feed. The gate owns a SQLite reservation,
approval and audit ledger and reads an explicit threshold policy. No credentials
cross this boundary. Gate reports go to the researcher; approval and plan identity
come back. Each worker reserves before dispatch; exit/cost observations return.

### Frame split

Transformation/information display produces a cumulative stage/session/cost
forecast. Commanded behaviour allows or refuses each new session according to
policy, user approval and already-reserved work. These are distinct: an estimate
can warn usefully even when it cannot establish actual charges.

### Requirements (per frame, with explicit out-of-scope)

The researcher must see substantial or unknown expected spending before it occurs.
No above-threshold or unknown-cost plan launches without explicit plan-specific
approval. Sessions beyond a declared stage quota cannot launch, including across
concurrent workers and restarts. Failed/uncertain attempts retain reservations.
Plan changes invalidate prior approval when approval remains required. A budget
approval cannot reopen a scientific terminal state. No live study is authorized
by this implementation. Frozen historical artifacts remain byte-identical.

Exact payment reconciliation, modifying top-up settings, controlling other account
workloads, and defending against an operator who rewrites local files are outside
the machine's boundary. Existing frozen runners are not retrofitted; future
runners must integrate reservations before every provider launch path.

### Invariance test

Canonical plan/policy hashes and transactional reservations are observable stable
controls. Future token consumption, credit conversion and internal provider
requests are not. Therefore reject the framing of a guaranteed dollar cap.
Instead use explicit forecasts, conservative session allowances and fail-closed
approval for missing cost/counts. Reforecast when observed usage/cost changes.

### Stakeholder test

The stakeholder is the person paying for credit reloads, not the scientific
pipeline trying to maximize completed judgments. A generic authorization to run
research is not permission for unbounded hidden fan-out. No borrowed product
pattern or advertised API price substitutes for this account's actual usage.

### Open questions — decided here, with reasoning

- Provisional defaults: approval above $10 or 100 sessions; unknown cost/count also
  requires approval. The user was asked for a preferred threshold but supplied
  receipt evidence instead; no above-threshold spending has been approved.
- Approval of unknown downstream fan-out does not authorize dispatch until that
  stage has a concrete count and a revised forecast has passed the gate.
- Cash-reload evidence yields a rough $0.15–$0.17/session proxy for comparable
  H.6 claim evaluation. Use $0.20 as a provisional planning allowance, not a price.
- Gate denials are pre-dispatch pauses, not provider failures or scientific labels.
- No automatic retries, reservation refunds, ledger reset or permanent unblock.
  Already-running calls may finish; do not launch additional work after denial.
- Interactive approval requires the displayed hash. Chat consent may be recorded
  by the agent only after explicit user approval, with a reference. This is an
  auditable operator workflow rather than an adversarial security boundary.
- Preserve H.6 as terminal. The new historical example is forecast-only and cannot
  launch even when budget approval is present.

### Carried forward

Future scientific runners must test per-session integration and archive the shared
ledger. Receipt-to-usage attribution remains approximate; no provider/billing
calls were needed to implement or test this gate.

## Entry #2 — 2026-10-02 — Remaining allowance and reset-aware preflight

### Domains

Add read-only Codex account quota telemetry, including window percentages,
scheduled resets and earned-reset availability. Local snapshots and matched
before/after batch calibration are new owned lexical artifacts. The researcher
owns any decision to redeem a reset. No reset redemption or billing write crosses
the machine boundary; this extension does not start a model thread or turn.

### Frame split

Information display reads current quota status. Transformation estimates required
percentage points from matched usage batches. Existing commanded financial/session
gating remains separate; the percentage forecast is a mandatory operator preflight
and batch review, not a runtime interception of provider requests.

### Requirements (per frame, with explicit out-of-scope)

Show the expected fraction of remaining allowance, reserve, limiting windows and
reset options before a run. Missing evidence yields UNKNOWN, not a fabricated
conversion from receipts to percentage. Preserve privacy by keeping snapshots
local and dropping account identity, credit balances and reset redemption IDs.
Every returned window is checked. Never redeem resets or change billing settings.

### Invariance test

Current percentage/reset telemetry is directly observable. Future consumption and
exhaustion probabilities are not fixed. Use matched historical ranges with
rounding allowance and headroom, explicitly not statistical probabilities. Reject
reset-crossing, saturated and unattributed batches; expire old calibration. No
assumption that prepaid dollars equal a fraction of included allowance is sound.

### Stakeholder test

The user wants to schedule research around included allowance and manually
available resets. Avoiding credit reloads is distinct from minimizing total tokens.
Do not automatically spend resets or run extra paid probes to improve estimates.

### Open questions — decided here, with reasoning

- Usage reserve: 10 percentage points, explicitly confirmed by the user.
- Fresh reads expire for forecasting after five minutes; refresh after a reset.
- Unknown risk requires explicit user review and approval, including the first
  normally planned batch used to calibrate; no additional probe is authorized.
- H.6 has no quota samples. A live read establishes current capacity only and
  cannot backfill historical percentage consumption.
- Matched observations yield LOW/BORDERLINE/HIGH scenarios, not an unsupported
  probability estimate. All personal account observations stay under `.runtime/`.

### Carried forward

Future authorized runs capture telemetry around bounded comparable batches,
reforecast remaining work at checkpoints, and keep the full cumulative financial
plan intact. Provider telemetry delay and unrelated account activity remain limits.
