# H8 — Target-facing impact of frozen survivors

Frozen before measurement, 2026-10-03. Authority: the user's H8 handoff, approved
implementation plan and instruction to implement. Base exactly
`c62b622b69ed900b9debcc9e41e133536287be59`; only push
`origin/experiment-h8-target-impact`. Historical tracked files remain unchanged.

## Question and materiality

**A Chaos-Mage transfer has target-facing impact when its frozen admitted survivor
causes a material change in the target's inquiry, prioritization, action, decision
rule, constraint structure, or decision-relevant problem representation compared
with the same target considered without that survivor.**

**A difference is material only if it could change what evidence is gathered, what
uncertainty is resolved first, what action is taken or withheld, what future
condition triggers action, what conclusion/action is ruled out, or the
decision-relevant representation used to choose among these.**

Terminology, source names, formatting, length and detail alone are not impact.
This measures Level 1 effects on model reasoning, not economic benefit, field
effectiveness, causal outcome improvement, human preference, cross-family
repeatability or production economics. No pass percentage or population estimate.

## Fixed corpus and preparation

| Survivor | H7 status | Definite candidates | Target |
|---|---|---:|---|
| H7-T01-1 | KEEP_WITH_REDUCED_SCOPE | 15 | T01 delivery temperature exceptions |
| H7-T03-1 | KEEP_WITH_WARRANT_FLAGS | 9 | T03 refill repeat-purchase decline |
| H7-T03-2 | KEEP_WITH_REDUCED_SCOPE | 8 | T03 refill repeat-purchase decline |

Only artifact-judgment definite allowlists supply positive content. Copy component
value/scope verbatim, assign sequential V IDs in allowlist order, and add only
necessary restrictive artifact cautions. Keep the provenance crosswalk outside
provider inputs. No deleted, nonviable, insufficiency-only or unresolved candidate
becomes positive guidance. No source identities, original mappings, source-domain
rationales, scores or admission rationales reach generation. Audit against frozen
judgments, inventories and deletion evidence; failure blocks measurement.

T01 does not restore cross-delivery logger rotation/field sampling. T03 chronology
does not promote K14 or establish intervention priority. T03 continuity does not
restore intervention selection, causal comparison, retain/revert or purchasing
commitment. Candidate reliability and implementation conditions remain intact.

## Calls, schemas and isolation

Exactly 2 native + 3 augmented + 3 impact slots, serial and at most two per batch.
No extra scientific calls for construction, audit, unblinding or reporting. No
retry, replacement, sample expansion, H7 regeneration or H7 admission rerun.
All calls request gpt-6-astra/high; fresh ephemeral empty contexts, tools/history/
config inheritance disabled. Timeout 900 seconds. Provider-internal retries and
served snapshot may be unobservable and must be disclosed.

Native order T01,T03; augmented order H7-T01-1,H7-T03-1,H7-T03-2; judgment order
PAIR-01,PAIR-02,PAIR-03. The exact same frozen T03 native response supports both
T03 comparisons: these are correlated cases, not three independent samples.

Common target instructions and schema apply to all five responses. Only the
additional-considerations packet differs by condition. Maximum list lengths are
3 except 4 important distinctions; empty lists permitted. Hidden survivor_basis
uses zero-based locations and V IDs, is empty for native responses, and never
reaches judges. Not every consideration must be used. Raw observations are never
rewritten to enforce neutrality or improve traceability.

The judgment schema adds the user-agreed blinded introduced_in field:
A_ONLY/B_ONLY/BOTH_DIFFERENT. Exact locations and downstream consequences make
interpretation inspectable. Categories are PROBLEM_REPRESENTATION_CHANGE,
INQUIRY_CHANGE, PRIORITY_CHANGE, ACTION_CHANGE, DECISION_RULE_CHANGE,
CONSTRAINT_CHANGE and NO_MATERIAL_CHANGE. The last is an overall no-difference
result with differences []; the other six are per-difference categories. Pure
representation changes require an inquiry/decision consequence. Judges do not
choose a winner. No material differences means differences [] and overall NO.

## Freeze sequence and blinding

Freeze protocol/definition, allowlists, neutral packets, audits, two native inputs
and three augmented inputs, schemas, runner/config and cumulative budget before
measurement. Commit and test before launching. Freeze both native responses before
augmented generation; freeze all augmented responses before comparison packets.

Order algorithm: SHA256 of UTF-8 `H8|<base SHA>|<pair_id>`; even first byte places
native at A, odd at B. Freeze all order maps and comparison packets before judging.
A judge receives only target frame, visible A/B reasoning, common instructions,
schema and pair identifier. No condition identity, survivor packet, metadata,
admission status, source identity, operator hypothesis or other pair is visible.

Freeze every judgment slot (successful or terminal) before unblinding. Direction
is a mechanical mapping from introduced_in and the frozen order. Do not alter a
judgment after unblinding. Store responses and raw streams unchanged with hashes.

## Attribution and outcomes

Offline operator audit for each augmented material contribution checks cited V IDs,
definite allowlist membership, scope, and independence from deleted/unresolved
claims. Classify ATTRIBUTABLE_TO_SURVIVOR, TARGET_ONLY_OR_GENERIC,
UNSUPPORTED_BY_FROZEN_SURVIVOR or UNCERTAIN_ATTRIBUTION. Never invent absent model
citations. Record any grounding regression or unsupported action prominently.

By the user's planning decisions, final MATERIAL_TARGET_CHANGE requires at least
one material augmented contribution with documented consequence and
ATTRIBUTABLE_TO_SURVIVOR. BOTH_DIFFERENT can qualify through its augmented side;
this does not imply improvement. Preserve the blinded comparison_result separately.
A material augmented change without established survivor attribution receives
UNCERTAIN_TARGET_CHANGE. Plausible uncertain consequences also receive UNCERTAIN.
MINOR_OR_NONMATERIAL_CHANGE means additional distinctions/detail without an
established material consequence; NO_MATERIAL_CHANGE means substantive equivalence.
UNMEASURED means instrumentation/provider failure prevented comparison.

Count each category once per difference, allowing multi-category membership.
Report all-direction material counts separately from survivor-attributable counts;
do not treat their sum as a number of unique differences. Operator inspection may
record nonmaterial augmented additions even when the judge's differences list is
empty; that distinction does not create a material judgment.

## Usage, preservation and failures

Use unchanged repository budget/usage policy: one cumulative eight-session plan,
fresh stage/batch forecasts and per-call Gate.reserve immediately before launch.
Known/unknown dollars and session totals remain advisory. Request actual consent
only below 30% fresh allowance in any quota window; exactly 30% passes. Refresh
stale/missing readings. Preserve a ten-percentage-point planning reserve. No reset
credits redeemed. Before/after usage and calibration remain in ignored .runtime;
concurrent account work, resets and saturation exclude clean calibration.

Every failure pauses scheduling and preserves raw evidence. Apply the frozen
EXPERIMENT-RECOVERY-POLICY; do not create a new continuation policy. Definite
provider no-observation consumes the attempt, no retry/replacement, affected pair
UNMEASURED. T01 native loss affects PAIR-01; T03 native loss affects PAIR-02 and
PAIR-03. Augmented/judgment loss affects only its pair. Skip unused dependent calls.
Unrelated fixed comparisons may continue only after committed positive hash,
allowlist, configuration, isolation and reservation proof. A partial/invalid
observation is not no-observation. Ambiguous lineage is investigated; unresolved
lineage terminates affected work. No automatic recovery of terminal states.

## Evaluator-work gate

**Observed decision failure:** H7 establishes defensible source-derived survivors,
but does not observe whether those survivors change target-facing reasoning. A
claim of demonstrated target impact from H7 admission alone is unsupported. No H7
admission defect or new calibration defect is asserted.

**Admission consequence:** none for frozen H7; all H7 statuses remain unchanged.
The concrete consequence is overclaiming target impact, or overlooking a real
reasoning change, by treating admission as a proxy for impact.

**Minimum intervention:** this user-authorized fixed target-facing comparison,
three blinded natural-output judgments and offline attribution, with no evaluator
calibration, taxonomy changes or H7 machinery edits.

**Scientific success evidence:** inspectable frozen differences (or equivalence),
material consequences and scoped survivor attribution, including negative results.
Success does not require positive impacts.

**Stop condition:** complete or terminalize the original eight slots, audit and
report, then stop. Incidental evaluator/provenance issues are recorded and assessed
under the existing stop rule; they do not authorize further calibration. If this
were proposed as admission calibration, the absence of a new concrete admission
defect would fail that gate. It is not such a proposal.

## Reporting and stop

Report base, branch, checkpoint SHAs, all five responses, A/B order, judgments,
directions, material differences, attribution and survivor outcomes. Surface native
reproduction of machinery, non-effects, unsupported changes, and effects requiring
deleted/unresolved content. A neutral-packet effect shows independence from explicit
source identity, not removal of source-derived semantics. Limitations include
single samples, same model family, shared baseline, model simulation, variable
provider behavior and no real-world outcome test. Recommend but do not execute one
next step. Stop after H8; do not merge main or push any other branch.
