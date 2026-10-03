# User-directed usage approval amendment — 2026-10-03

Authority: user message, “Adjust usage prediction gate to only block for approval
when remaining usage is <30%”. No scientific provider sessions or reservations
have occurred. This instruction changes the approval predicate, not the sample,
scientific inputs, judgments, model configuration or 10-point planning reserve.

Approval now depends only on current observed remaining allowance: any fresh
window below 30% requires usage consent; exactly 30% does not. Forecast LOW,
BORDERLINE, HIGH and UNKNOWN remain informational. Missing/stale/reset-crossed
account readings require refresh (exit 1), not consent. Financial approval remains
separate and unknown H7 costs still require it.

The original PROTOCOL, initial freeze, preservation inventory, budget plan 001,
preflight results and preparation report are retained unchanged. This amendment
supersedes their usage-approval trigger. `usage-gate-amendment.json` binds original
and updated hashes for the shared usage tool, its tests/docs/instructions and the
H7 runner/tests. Every other historical/scientific file remains protected by its
original hash. No H.3–H.6, H6.R1–R4 or evaluator-stop-rule file changes.

Plan 002 preserves the same cumulative session counts and unknown costs, with an
updated execution fingerprint. No approval is carried over or fabricated. The
runner reads plan 002, requires financial consent, and only asks for separate
usage consent when the new predicate is true. Historical UNKNOWN/exit-2 results
are not retroactively relabeled. Future preflights use the new policy.

Verification: 22 usage tests, 7 H7 runner boundary tests and 18 budget tests pass.
The live preflight under the revised policy exits 0 despite UNKNOWN forecast risk;
private readings remain in `.runtime/natural-admission-v0.2/preflight-002/`. The
financial preflight still exits 2 for unknown costs and evaluation fan-out. No
provider execution is authorized by this policy change.
