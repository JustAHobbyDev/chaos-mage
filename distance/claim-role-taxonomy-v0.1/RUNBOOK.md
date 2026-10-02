# H6.R1 operator runbook

All commands run from the repository root. Use `python -B` to avoid tracked cache
artifacts. Read the protocol first. Every provider invocation is behind `run`;
never invoke the old H.6 runner or launch the CLI directly.

## Offline preparation and audit

```
python -B -m unittest discover -s distance/claim-role-taxonomy-v0.1/tests -p 'test_*.py'
python -B -m unittest discover -s scripts -p test_experiment_budget.py
python -B -m unittest discover -s scripts -p test_codex_usage.py
python -B distance/claim-role-taxonomy-v0.1/runner.py verify
```

The frozen scientific JSON Schemas remain unchanged. The `*-wire.schema.json`
files are transport projections omitting `$schema`, `minLength` and `uniqueItems`
to avoid depending on decoder support for those keywords. All original constraints
and cross-field invariants are enforced on the returned original response. No
additional model turn repairs an invalid response.

Preparation was authorized in the implementation request. The budget and allowance
gates are separate; neither that request nor this runbook supplies their approval.
The initial complete forecast is 24 Stage A sessions and up to 24 Stage B sessions.
Cost is unknown for these new profiles. At $0.20 per comparable H.6 session the
illustrative 48-session proxy would be $9.60, but comparability/billing is not
established and that figure is not the approved forecast or a spending cap.

## Preflight and approval

After prepared packets and the financial plan are committed, use a new path on
EVERY account read. Reuse the existing account-scope label from the ignored usage
snapshots; never commit account data. Start with an empty calibration or the last
batch's `calibration.json` (retaining excluded samples).

```
python -B distance/claim-role-taxonomy-v0.1/runner.py forecast \
  --scope ACCOUNT_SCOPE --calibration CALIBRATION_JSON \
  --out .runtime/claim-role-taxonomy-v0.1/preflights/UNIQUE_ID
```

A nonzero result requires actual user review. Present the entire cumulative plan,
exact plan hash, cost uncertainty and stage/session bounds; present each quota
window's remaining allowance, reset, predicted points/share, reserve and risk.
Financial consent may be recorded through Gate.approve only after the user gives
it, with the actual message reference. The runner never calls Gate.approve.

For a warning-bearing usage report, record consent under ignored .runtime/ only
after the user's reply. It must contain:

```
{
  "plan_sha256": "exact cumulative financial-plan hash",
  "report_sha256": "exact reviewed usage-report hash",
  "stage": "role",
  "max_sessions": 3,
  "user_message_reference": "actual user message granting consent"
}
```

This review covers only that batch. Refresh snapshots that are older than five
minutes or whose resets have passed; an old review does not cover a new report.
A changed financial plan may require renewed financial consent. Never lower the
10-point reserve or redeem a reset credit automatically.

## Authorized batches

```
python -B distance/claim-role-taxonomy-v0.1/runner.py run role \
  --preflight .runtime/claim-role-taxonomy-v0.1/preflights/UNIQUE_ID \
  --count 3 --usage-review ACTUAL_CONSENT_JSON
```

Omit --usage-review only when the reviewed forecast is LOW without warnings.
No more than three serial calls dispatch. Each reserves separately in the shared
ledger. The runner rechecks frozen inputs, active batch, CLI and expected packet
before each launch. It records raw evidence and pauses on any provider event.
No retry/resubmission command exists. Retain runtime state, failures and reservations;
report a pause and archive its exact evidence before any proposed recovery.

After telemetry settles, record the batch with a later snapshot:

```
python -B distance/claim-role-taxonomy-v0.1/runner.py record-batch \
  --batch .runtime/claim-role-taxonomy-v0.1/batches/0000 \
  --reference 'actual bookkeeping evidence'
```

Use --isolated-account-work only with actual evidence of no other account work;
use --telemetry-settled only when established. Missing attestations conservatively
exclude the sample while retaining all bytes and available usage, including failures.
This current interactive agent may itself confound account usage; isolated child
contexts are not proof of account isolation. Complete bookkeeping even after a
paused batch. The next forecast uses the saved cumulative batch calibration.
Commit successful judgment outputs at bounded checkpoints. Reforecast before the
next batch; raw evidence is also archived by the complete stage freeze.

## Stage freezes and comparison

After all 24 Stage A judgments and batch bookkeeping:

```
python -B distance/claim-role-taxonomy-v0.1/runner.py freeze role
```

Commit the freeze, then prepare and commit Stage B packets:

```
python -B distance/claim-role-taxonomy-v0.1/runner.py prepare evaluation
```

Create a new cumulative budget plan revision with `write-plan --out
.../budgets/plan-002.json` and commit it. It retains all 24 Stage A sessions and
uses the actual Stage B eligibility count. Refresh both gates before any Stage B
batch. Use `run evaluation` with the same batch workflow. If no claims are eligible,
freeze an empty evaluation stage without provider calls and report the limitation.

After all eligible Stage B judgments:

```
python -B distance/claim-role-taxonomy-v0.1/runner.py freeze evaluation
```

Commit that freeze before invoking `compare` or `metrics`. No earlier historical
label read is allowed. Then commit the comparison and its `seal-review comparison`
freeze. Operator assessment belongs in `review/operator-audit.json`, separate from
provider judgments. Include twelve numbered `research_questions` entries with
`answer` and `evidence`, an `anchor_assessments` object keyed by all eleven original
IDs, detailed contract-mismatch attribution, strict inference/permissiveness checks,
limitations, recommended next step and `recommendation_executed: false`.

Write the final report at distance/review/claim-role-taxonomy-v0.1.md, then use
`seal-review audit` and commit. Verify all hashes and base preservation. Record
checkpoint SHAs in the subsequent report/checkpoint registry (never modify an
already sealed artifact to add its own SHA). Push only the H6.R1 branch. The final
completion message supplies the final SHA and all requested results.
