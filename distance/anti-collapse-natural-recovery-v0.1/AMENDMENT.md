# Experiment E recovery amendment

This additive continuation starts from published checkpoint
`6f5b43b3ba7455f9fd5d95640f6be5ba9e1ff61a`. The original Experiment E directory,
report, metrics, raw responses, failed attempt and STOP marker remain unchanged.
The original report accurately describes the interrupted run; it is not a completed
natural-output test. A future recovery report must distinguish both execution segments.

## Authorization and current boundary

The user requested: “add a local mise file pinning the codex version then perform
recommended next step”, subsequently paused execution, then instructed:
“Do local mise pin and recovery work. Pause at the experiement run step.”

This authorizes the local pin, recovery implementation, mechanical revalidation,
input preparation, offline verification and local checkpoint commits. **All provider
calls remain paused**, including artificial preflight probes. No execution authorization
file is present. A later explicit user instruction to resume must be recorded in a
committed `execution-authorization.json` bound to this preparation before any call.
Preparing that file is outside the current scope. Publication/push awaits completion.

## Frozen procedure retained

The original source assignments, generation outputs, baselines, schedules, prompts,
schemas and both gate classifiers are reused exactly. No regeneration, source
replacement, novelty selection, distance ranking, grounding, diversity filtering or
production integration is introduced. No qualitative novelty labels are assigned.
Validity and anti-collapse results have not been collected or inspected.

The initial generation checker mistakenly rejected three schema-valid payloads:
E027 and E030 use the literary noun “novel”; E029 describes novelty effects, fading
and decay as a behavioral mechanism. The post-failure diagnostic documented these
before this amendment. Recovery admits those unchanged payloads by exact hash-bound
exceptions. All other outputs still pass the original checker. There is no general
relaxation of novelty self-assessment detection, and no exception for a modified or
new response. The original exclusion records remain reproducible. This is a cohort
correction after a failed run, explicitly reported as such, not the original cohort.

Reuse all 30 generation payloads, 27 completed neutralizations and 21 completed audit
judgments byte for byte, retaining their original sessions, versions, execution
commits, returned model metadata, timestamps and validation records. The import
manifest separately records corrected validation status and original provenance.
It does not claim that reused calls occurred during recovery.

## Remaining execution, after resumption

1. Commit preparation and the three restored cases' neutralization packets. Run and
   commit two artificial neutralization probes, then collect only those three missing
   cross-family neutralizations. Combine with 27 imports, freeze, commit.
2. Prepare audit packets from the completed neutralization freeze. Run and commit
   two audit probes. Filter the original 60-entry audit order to compliant neutralizations,
   removing the 21 completed imports without changing relative order. Up to 39 new
   audit calls remain. E021-A's previous attempt never launched a provider call;
   its newly authorized attempt uses a separate runtime directory. Preserve the
   failed attempt and do not repeat any completed judgment. Freeze and commit.
3. Run the unchanged two-family validity gate on all 30 original mappings, including
   neutralization/audit exclusions. Commit inputs and artificial probes first, then
   results. Derive admission only after the completed audit and validity freezes.
4. Require unconditional Valid/Valid and two passing fidelity audits. If fewer than
   18 cases across 5 targets qualify, report insufficient coverage and stop. Generate
   no replacements. Otherwise prepare blind anti-collapse packets, probe, commit,
   measure with the unchanged classifier, freeze and commit.
5. Only after the terminal freeze, perform the required suppression/retention,
   formalization, one-rule and mechanism reviews and recompute all metrics. Publish
   a companion recovery report covering all original handoff items and linking the
   preserved incomplete report. Run all historical and recovery verifiers. Push
   normally to main, verify the remote SHA, and stop after Experiment E.

The original stop-on-failure policy applies to all recovery calls. No automatic
retry, output repair, replacement, model substitution or restart is authorized.
Malformed/evaluative neutralization content is preserved attrition as originally
specified; provider/isolation/formatting failures halt scheduling. Both independent
audits must pass; neither partial fidelity judgments nor validity exclusions count
as collapse. The only rejecting anti-collapse status remains CLEAR_COLLAPSE.

## CLI and isolation correction

Repository `mise.toml` pins `npm:@openai/codex` to 0.157.1. Recovery resolves both
installed CLIs to version-specific absolute paths, records executable hashes, and
checks hashes and exact version strings before each new call. This avoids reliance
on project discovery or the mutable `latest` alias in fresh empty working directories.
Claude remains 2.1.283; requested models remain gpt-6-astra/high and
claude-fable-5-1[1m]/high. No model alias is treated as a verified serving snapshot.

Original fresh-process/session, empty-directory, no-tools/retrieval/repository/history,
no-memory/plugins/connectors/hooks settings and the event auditor are reused. Session
uniqueness includes both runtime trees. Probe and measurement reservations remain
exclusive; a failed call cannot be overwritten. Execution verification distinguishes
original and recovery commits rather than asserting a single uninterrupted stage.

This amendment is limited to the documented lexical corrections and execution recovery.
It does not answer the research question; doing so requires the still-paused calls.
