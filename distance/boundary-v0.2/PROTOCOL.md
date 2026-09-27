# Boundary calibration v0.2 — preregistered protocol

2026-09-27. Sixteen purposive cases; 32 primary cross-family judgments and six
supplementary matched v0.1-prompt judgments. No expected labels or forced balance.
The tested snapshot freezes experimental text, not validity or production status.
All existing v0.1 files remain byte-for-byte unchanged (preservation.json).

## Preparation and packets

CLASSIFIER-tested.md snapshots ../CLASSIFIER-v0.2-draft.md before measurement.
Seven dimensions, ordinal 0–3 meanings, and naturalization statuses are unchanged.
Axes and boundary evidence are analytical annotations. Alien requires high
reorganization AND an essential independently unjustified counterpart. Weak
grounding at low/moderate displacement is a taxonomy tension. Structural validation
must preserve semantic inconsistencies rather than reject, repair, or coerce them.

Neutral IDs 001–016 carry only source identity, five verbatim instrument fields,
and target domain/problem. Newly authored cases are synthetic fixtures, identified
in operator-manifest.json. This operator-only file also holds boundary groups,
source provenance, contrast relationships and control origins; it never enters
classifier context. Groups express questions under test, not expected labels.
001, 003, 009 reproduce source/target content of CASE-008, CASE-009, CASE-013.
Their supplementary controls reproduce the entire original v0.1 prompt/packet
bytes (including original IDs) and schema. Primary cases use neutral IDs.
004/005 and 006/007 have identical targets. Close evidence pairs retain identical
questions and surrounding text; changed evidence sentences are documented there.

## Execution and provenance

Family A requests gpt-6-astra, high reasoning via Codex. Family B requests
claude-fable-5-1[1m], high effort via Claude Code. Equal effort labels do not imply
equal compute. Preflight uses a non-calibration JSON task with each adapter before
configuration commitment. CLI versions, explicit settings, actual command lines,
returned model fields and their provenance are recorded. Unavailable verified
served snapshots remain null; requested aliases never substitute for served IDs.
A returned identifier outside the requested model (allowing removal of the [1m]
context request suffix) or an explicit fallback event invalidates the run. CLI
metadata cannot detect an undisclosed server-side substitution.

Each judgment uses a new empty temporary directory and fresh process/session.
Codex ignores user config/rules, disables project instructions, tools, plugins,
apps, memories, browsing, hooks and delegation, and runs ephemeral/read-only.
Claude safe mode retains subscription authentication and disables customizations;
empty setting sources, explicit hook/memory disabling, empty MCP configuration,
no tools, disabled skills and no session persistence provide additional isolation.
Explicitly disable agents-md and telemetry built-in plugins, connector discovery
and account skill/plugin synchronization; the init event must show no plugins.
Provider environment overrides and parent-agent markers are removed. Auth stays
on disk with the existing CLIs; no credentials are copied into experiment records.
Runner-host system prompts, policies and structured-output instructions necessarily
differ and are not fully exposed. Claude's StructuredOutput formatting tool is
allowed solely as runner machinery; no external tool activity is permitted.
Equivalent classifier text/case bytes/schema are supplied to both families.

Raw JSONL events, stderr, request, response, reservation and validation stay private
under .runtime/boundary-v0.2. CLI internal formatting/transport retries remain in
raw streams. Record visible StructuredOutput calls, failed calls, inferred visible
formatting retry count and runner turn count; unexposed retries are unavailable,
not asserted absent. Never author repair prompts. Claude structured-output behavior:
https://code.claude.com/docs/en/agent-sdk/structured-outputs (consulted 2026-09-27).
Codex structured output/event auditing:
https://developers.openai.com/blog/eval-skills (consulted 2026-09-27).
Local CLI --help and preflight are the evidence for available isolation flags.

execution-order.json fixes all 38 invocations, including interleaved supplementary
controls. Schedule sequentially (one process, below maximum two); 900 seconds per
process, killing the process group on timeout. Exclusive experiment/run reservations
prevent concurrent schedulers, overwrites and retries. Preserve any failure and stop
all further scheduling for a documented amendment. Never reduce denominators.
Prepare hashes and successfully commit every prepared input, schema, harness and
manifest BEFORE calibration: runner verifies each against HEAD. Freeze all 38
valid results, verify unique sessions, then publish unchanged payloads and audit
metadata. Review begins only after the result freeze. No family receives other
judgments, expectations or review. No adaptation of tested definitions mid-run.

## Fixed analysis and decision rules

Compute exact final-class, displacement-axis, grounding-axis and naturalization
agreement. For each original dimension report exact agreement and mean absolute
ordinal disagreement. No composite distance scores or class thresholds.
Report per-family class distributions, confusion matrices and all exact classes.
Primary n=16 and supplementary n=3 pairs remain separate.

For Adjacent/Remote cases 001–008 map {Native, Adjacent} versus {Remote, Alien}.
For Remote/Alien cases 009–016 map {Native, Adjacent, Remote} versus {Alien}.
Each fixed n=8 boundary requires at least 6/8 (75%) side agreements. Report all
out-of-band labels and whether both sides were exercised; agreement entirely on
one side is insufficient evidence of discrimination. Native control agreement
alone cannot establish the Adjacent/Remote distinction.

Review every class, axis, dimension or naturalization disagreement with evidence,
uncertainty and unresolved alternatives. Audit these six shortcuts for every
such case (also inspect concordant cases): disciplinary distance, semantic distance,
operation-distance overweighting, entity-vocabulary overweighting, mapping
 difficulty confused with distance, usefulness confused with distance.
Inspect EVERY Remote for a substantive non-native operation, observable or inference;
inspect EVERY Alien for an essential independently unjustified counterpart. Also
record class/axis/evidence tensions, naturalization shortcuts and target drift.
Do not adjudicate or relabel any response. Researcher interpretations are judgments,
not independently collected human ground truth.

“Usually/mostly” requires a strict majority of observed side disagreements explained
by the intended axis (displacement for Adjacent/Remote, grounding for Remote/Alien).
With no side disagreements this attribution test is not applicable. If attribution
is uncertain it does not count as explained. A boundary needs both its agreement
criterion and supporting semantic evidence; side coverage is necessary, not enough.

For each original disagreement compare original frozen v0.1 same-family A/B, new
v0.1 cross-family A/B, and new v0.2 cross-family A/B. Resolution requires exact final
class equality; side equality alone is insufficient. One observation per family
and condition supports limited experimental evidence, not causal identification.

Finish with retain/revise/abandon-a-class recommendations and exact tested text,
cases, configurations, metrics, shortcut audits, controls and limitations. Any
post-run proposed wording is separately identified as untested. Stop at research
review: no production promotion, retrieval integration or numeric distance score.
