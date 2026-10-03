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
| `provider_no_observation` / `PROVIDER_NO_OBSERVATION` | Positive launched-request identity, frozen input/config/context intact, no scientific response or completed observation, unique harness attempt, no retry/substitution | Consume attempt permanently; quarantine affected mapping FAILURE / UNMEASURED; permit positively verified independent lineages under applicable authority |
| `provider_observation_failure` / `PROVIDER_OBSERVATION_FAILURE` | An observation exists but fails the frozen scientific contract (including malformed/schema-invalid response, provenance/identity failure or model substitution) | Preserve observation/failure; apply frozen stage scientific failure rule; no automatic no-observation continuation |
| `provider_observation_ambiguous` / `PROVIDER_OBSERVATION_AMBIGUOUS` | Launch, response existence, partial bytes, identity, duplication or contamination unresolved | PAUSED_AMBIGUOUS; investigate; unresolved ambiguity becomes measurement_lineage_violation |

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

## Prospective provider no-observation rule — 2026-10-03

A provider request definitely launched against its frozen scientific input, but no
scientific response observation was returned or preserved, launch status is known,
and positive evidence establishes intact request/configuration/context lineage.
All eight conditions are required: positive launch; exact executed identity; match
with frozen packet/configuration; no usable scientific response; no completed
observation interpretable as the requested judgment; process/session identity
excluding duplicate harness launch; no retry/substitution; distinguishable absence
from unknown launch. Error strings alone never qualify. Partial or unknown response
bytes/events require investigation, not a negative inference. A known invalid
scientific response is an observation failure, not an absent observation.

A qualifying event permanently consumes that specific attempt. Never retry,
replace, substitute, or convert it into a scientific judgment. Instrumentation is
FAILURE, admission UNMEASURED, end_to_end_complete false. Do not assign CORE_INVALID,
UNCERTAIN_LOAD_BEARING or a KEEP status. Preserve prior valid stages unchanged.

Pause scheduling briefly to preserve and classify each event. Before independent
continuation, commit positive proof for each eligible mapping: frozen hashes,
explicit packet allowlists/dependency closure, distinct fresh sessions and no shared
history, unchanged scientific configuration, no leaked response/event/failure or
mutable scientific artifact, and scheduler/reservation integrity. Reverify committed
evidence, historical preservation, experiment-local checks, clean branch/working
tree, and fresh budget/usage checks before launch. A different mapping ID is not
proof. One uncertain local mapping need not block a positively independent mapping;
a shared unresolved lineage issue blocks all affected mappings.

Recovery is additive: preserve PAUSED_AMBIGUOUS and the original event; record
resolution of the policy ambiguity under new authority, without calling the old
pause incorrect. Append the authorized resume checkpoint to the state chain.
Future events require the same evidence; classification does not auto-resume.

Historical stopped experiments are not reopened by this policy unless separately
authorized. The user's H7 continuation handoff separately authorizes H7 only.
A fixed-sample run may be COMPLETE once each original slot has a completed admission
or final local quarantine and no scientific actions remain; separately report the
number of end-to-end scientific admissions. Quarantine never counts as admission.
