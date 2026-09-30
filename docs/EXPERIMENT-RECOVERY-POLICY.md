# Experiment recovery policy — 2026-09-30

**Pause on invariant violation. Terminate only when measurement integrity is
compromised or cannot be established.** Frozen stage protocols may additionally
make unsuccessful provider observations terminal and non-retriable.

Never repair a model judgment. Never silently alter a measured input. Never
replace a failed scientific observation. Recover engineering errors aggressively;
preserve scientific measurements conservatively.

## Classification and action

| Class | Evidence required | Action |
|---|---|---|
| `recoverable_integrity_violation` | Executed scientific inputs, configuration, context and returned response demonstrably unaffected | Pause, preserve incident, remediate, verify exact restoration/non-contamination, commit recovery evidence, resume |
| `measurement_lineage_violation` | Material change to executed packet, classifier, schema, mapping, model configuration, order, context, or response | Freeze evidence, invalidate affected stage, terminate; explicit new recovery/restart authorization required |
| `ambiguous_impact` | Effect on measurement cannot yet be established | Pause and investigate; unresolved uncertainty is treated as a lineage violation |
| `provider_measurement_failure` | Request sent followed by timeout, malformed/schema-invalid response, substitution, or other frozen-protocol execution failure | Preserve the observation and apply the stage's non-retry/terminal rule |

Harness, bookkeeping, verifier, metadata-representation and restorable documentation
errors can be recoverable only with positive non-contamination evidence. Error
message text alone never establishes this classification. Model substitution also
compromises lineage; it cannot be converted into a recoverable metadata mismatch.

## Evidence and authority

Preserve original stops, reservations, commands, raw events, responses, validation,
freezes, reports and commits. Record incident time and affected paths, expected and
actual hashes, archived erroneous bytes, remediation, dependency analysis, every
verification result, applicable user authority and the exact resume checkpoint.
Separate integrity-manifest dependencies from information reaching a measurement.
Hash equality, explicit input allowlists and isolation provenance must support
recovery together; assertions that a file was unrelated are insufficient.

Recovery is additive. A later recovery cannot rewrite an earlier incomplete result.
A recovered observation retains its original identity, bytes, process, session and
execution commit. Harness revisions require distinct provenance from unchanged
scientific inputs. Unknown provider internals and unavailable served identifiers
remain disclosed limitations, never invented assurances.

## Scheduling and state

Before every provider stage or resumed segment: complete all historical preservation
verification, experiment-local verification and clean continuation checks. Before
each launch, recheck state and frozen hashes. Verification precedes provider work;
an integrity violation found before a request is not itself a scientific observation.

Use append-only evidence for `RUNNING`, `PAUSED_RECOVERABLE`, `PAUSED_AMBIGUOUS`,
`TERMINATED_LINEAGE`, `TERMINATED_MEASUREMENT`, and `COMPLETE`. A recoverable pause
clears only against committed, reverified evidence and applicable continuation
authority. No terminal state auto-clears. Preserve an already running response if a
pause is detected, but launch no further request.

Reservations are globally unique within a scientific stage, including prior segments.
Never reschedule a completed or sent attempt. A demonstrably unlaunched reservation
may launch once under committed remediation evidence, retaining that reservation.
Uncertain launch status blocks continuation. Successful responses survive bookkeeping
repairs unchanged; supplementary validation must not overwrite the original record.

This policy governs future work and explicitly authorized continuations. It does not
reopen stopped experiments or override scientific protocols without authorization.
