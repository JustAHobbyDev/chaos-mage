# H7 — Natural-transfer admission pilot v0.2

Status: **PREPARED_AWAITING_BUDGET_AND_USAGE_APPROVAL**. Zero scientific provider
sessions. The six-mapping stop rule and UNMEASURED recovery boundary are frozen in
[PROTOCOL.md](PROTOCOL.md). H6.R4 remains return-gate INCOMPLETE.

Targets, deterministic selection and all six generation packets are frozen. Six
different instrument families were selected. No expected artifact labels exist.

The initial-stage runner supports only generation and atomization. It reserves
each individual session through the shared budget ledger and uses serial batches
of at most two isolated contexts. It has no retry, resume, substitution, automatic
approval or recovery command. Later classification/discovery/evaluation adapters
must be frozen and verified before those stages; the scientific protocol already
defines their behavior. Their costs remain in the cumulative forecast.

Offline verification:

```sh
python -B distance/natural-admission-v0.2/runner.py verify
python -B -m unittest discover -s distance/natural-admission-v0.2/tests -v
python -B scripts/experiment_budget.py check --plan distance/natural-admission-v0.2/budgets/plan-001.json
```

The last command is expected to exit 2 until actual user approval is recorded.
It reports unknown dollars, not a zero-cost experiment. Its known session subtotal
is 36; evaluation fan-out is unknown. Initial consent requested: at most six
generation and six atomization sessions. No future count approval authorizes
unknown evaluation dispatch.

After actual consent, record the exact plan approval through the repository gate.
Before each stage/batch, capture fresh allowance and construct the usage-only batch
plan from the corresponding cumulative stage with its session count set to one or
two. Run the usage forecast with reserve 10. Obtain required usage review, then
save an operator review under `.runtime/natural-admission-v0.2/` containing:
`consent_reference`, `financial_and_usage_approved`, `stage`, `packet_ids`,
`plan_sha256`, `snapshot_path`, `snapshot_sha256`, `calibration_path`,
`calibration_sha256`, `usage_plan_path`. References must identify actual consent,
never an agent-created authorization. Use the forecast's canonical snapshot and
calibration hashes. The runner checks freshness, stage order, plan and scope.

Only then use `runner.py run-batch --review <review-path>`. It preserves raw attempts,
before/after snapshots and available usage, excluding unattested concurrent-account
observations from clean calibration. No account information is committed.

After six successful generation observations, `runner.py freeze generation` and
commit the resulting freeze. `runner.py prepare-claims` imports unchanged H.5
segmentation and creates all atomization packets; commit those before atomization.
After atomization, `runner.py freeze claims` freezes all claims before any role
classification. The initial adapter deliberately refuses incomplete stage freezes;
a real local quarantine needs committed non-contamination evidence under PROTOCOL.md
before any independent continuation, never a fabricated successful freeze.

The implementation fingerprint includes frozen inputs, runner, schemas and prompts.
Changes require a new cumulative budget plan and any required renewed consent;
they do not erase previous reservations or reopen scientific terminal states.

See [pre-execution report](../review/natural-admission-v0.2.md). This document does
not claim experiment completion or any scientific admission outcome.
