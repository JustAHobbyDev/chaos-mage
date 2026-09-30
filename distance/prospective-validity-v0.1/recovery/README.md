# Experiment F additive continuation

The original F tree and runtime remain the incomplete historical checkpoint. This
directory owns new artifacts; `.runtime/prospective-validity-v0.1-recovery/` owns
new private evidence. The complete taxonomy freeze references the four original
responses and 192 new responses. No original probe or judgment is rerun.

`evidence.py audit` reconstructs the initial ten-gate proof. `evidence.py history`
runs all 36 historical checks and 37 original F tests. The legacy F verifier's Git
diff is explicitly scoped to its original publication commit; all original tracked
bytes and private evidence are independently checked against the live checkout.
This scope is essential because the original verifier forbids later publication.

`continuation.py resume` verifies committed initial recovery evidence. `run --stage
taxonomy` completes historical/local/state checks before starting Q0094. Each
`run` or `preflight` repeats those checks before provider work. `freeze --stage
taxonomy` writes the aggregate freeze; commit it before operator review.

After committed taxonomy review and prospective preparation, use `preflight --stage
prospective`, commit the probe, then `run --stage prospective` and `freeze --stage
prospective`. Commit the thirty outputs before any historical comparison.

`pause --reason TEXT` preserves an append-only investigation event. `recover --record
PATH` requires a committed recoverable incident record bound to the latest pause,
all attempted raw artifacts, remediation and the authorization. It rechecks frozen
inputs and responses and reruns history. A provably unlaunched attempt retains its
reservation; its actual launch metadata is supplemental. Ambiguous launch state or
invalid measured output cannot be recovered. A terminal state cannot auto-clear.

The original packet/schema/configuration contract is unchanged. Scientific input
hashes are separate from additive harness and checkpoint provenance. Later incident
records must demonstrate non-contamination; merely changing an error label is not
authorization. Raw events/authentication artifacts are never published together:
only hash-bound research evidence belongs in Git; credentials remain provider-owned.
