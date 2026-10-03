# Problem Frames — Unified experiment approval

## Entry #1 — 2026-10-03 — One allowance-based approval predicate

### Domains

Existing lexical domains: experiment plans, append-only reservations, historical
approvals and freezes. External observable domain: account allowance snapshots.
Biddable operator: authorizes the scientific task and any below-threshold spend.
The budget gate now reads current allowance before each individual reservation.

### Frame split

Forecasting displays cumulative costs/workload as information. Commanded execution
uses current remaining allowance to determine whether additional consent is needed.
Scientific scope, measurement integrity and session identity remain separate checks.

### Requirements (per frame, with explicit out-of-scope)

Within an authorized task, only current allowance below 30% triggers approval.
Unknown cost, high totals, stage transitions and changed plan hashes must not create
extra permission requests. Keep cumulative bookkeeping, unique reservations and
scientific terminal states. This does not authorize a new experiment or scope change.

### Invariance test

Quota moves independently. Read before reservation; refresh stale/missing/reset-crossed
data. A prediction is not a live reading. Do not redeem reset credits automatically.

### Stakeholder test

The research operator explicitly selected this simpler consent boundary. Preserve
cost information for inspection without treating its uncertainty as another approval.

### Open questions — decided here, with reasoning

Exactly 30% passes. Any returned window below 30% requires consent. Missing account
data needs a fresh read, not an approval override. Unknown future fan-out is advisory;
the dispatched stage still needs a finite count to prevent unbounded reservations.
Existing historical approvals remain records; no consent is fabricated above 30%.

### Carried forward

Fixed scientific sample, no retries/substitution, recovery evidence, H6 terminal
states and the evaluator-work stop policy remain in force.
