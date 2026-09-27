# Calibration protocol v0.1

Frozen before any classification. Date: 2026-09-27.

## Design

Twenty deliberately selected cases span proposed low through high displacement;
there is no forced output balance. Every source is an accepted existing instrument
copied verbatim, with provenance outside its five fields. CASE-001/003/019/020
share an identical software target; CASE-009/013/018 share a literary target.
Repeated sources provide the opposite contrast direction. Cases are purposive,
not a sample supporting population prevalence estimates.

The only classifier prompt is CLASSIFIER-v0.1.md followed by one YAML packet.
The output schema is supplied separately and identically. No calibration examples,
expected classes, other cases, reference labels, user handoff, or prior judgments
enter either prompt. A/B identifiers are bookkeeping only and absent from prompts.

## Execution and independence

One fresh ephemeral `codex exec` process per case per replicate. No resume or fork.
Use the same frozen model/configuration for A/B. Each process starts in a new empty
temporary directory, ignores user configuration, disables project instructions,
memories, plugins, apps, browsing, shell and agent delegation. Built-in host system
instructions and model priors remain; this is not a claim of a bare model API.
No tools are allowed in the classifier instruction. Audit JSONL item events and
reject any tool activity. Unique thread IDs and matching prompt hashes are required.
Independent contexts do not imply independent model biases or different weights.

The operator's existing gpt-6-astra/high configuration is retained. Record requested
alias, CLI version, settings, event stream, and hashes; a served snapshot is not
available from this interface. This limits replication across time. CLI behavior
reference: https://learn.chatgpt.com/docs/non-interactive-mode (consulted 2026-09-27).

Create reservations exclusively. Never overwrite, retry, or conversationally
repair malformed/refused/incomplete results. Preserve failures and stop for an
execution-protocol amendment if necessary. Internal CLI transport retries are
possible and remain visible in raw logs. Missing/invalid pairs block completion;
do not silently reduce denominators. Concurrency is at most three processes.

## Freeze and retention

Commit protocol/configuration/cases with SHA-256 hashes before first execution.
Raw runs initially stay in ignored `.runtime/distance-v0.1/`. After all 40 valid
responses exist, write a result hash manifest before making any reference labels.
Then copy unchanged validated responses into `judgments/` as a frozen calibration
snapshot so the report is reproducible from a clean checkout. Retain raw local logs.

Only after that freeze, write separate expected-class/confidence/rationale records.
If these are synthesized from the handoff by the implementation agent, label them
as author-informed reference expectations, not independently collected human truth.
No reference labels affect prompts, class assignment, denominators, or agreement.

## Analysis fixed before observation

Class order is Native, Adjacent, Remote, Alien, solely for describing disagreements.
Report exact final-class agreement, exactly-one-step disagreement, and agreement
within one step (exact plus one-step). Give counts and rates with denominator 20.
This ordering is not a classifier threshold or summed dimension score.

For each dimension report exact 0–3 agreement and mean absolute disagreement.
Report exact naturalization agreement, an A-row/B-column class confusion matrix,
and unordered boundary counts. For each observed class boundary, show which
dimensions differ, their counts and absolute ordinal differences; these describe
association, not causal attribution or learned weights. Read both rationales,
including cases with identical dimension vectors but different final classes.

Examine the hypothesis that operations/observables/inferences distinguish Adjacent
from Remote alongside counterexamples and other dimensions. If no disagreements
occur at a boundary, say that the disagreement analysis has no evidence there;
do not claim stability from absent cases. Inspect same-source and same-target
contrasts and look for foreign-domain or vocabulary shortcuts even when A/B agree.

Preserve every class, dimension, or naturalization disagreement in a review log
with evidence and one or more categories: target-native-profile-unclear,
source-profile-unclear, naturalization-uncertain, disciplinary-distance-substitution,
semantic-distance-substitution, operation-distance-overweighted,
entity-vocabulary-overweighted, mapping-difficulty-confused-with-distance,
usefulness-confused-with-distance, class-boundary-unclear, other.
Distinguish observed errors from possible confounds. Do not automatically adjudicate.

No numeric class thresholds, weights, fit/usefulness scores, retrieval integration,
or production decisions. Stop after the calibration report. Proposed v0.2 changes
must be separate from frozen v0.1 evidence.
