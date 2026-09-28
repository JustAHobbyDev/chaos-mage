# Ontological displacement calibration v0.3 — Experiment B

2026-09-28. **Completed; useful research distinctions, insufficient evidence for a reliable standalone control.**

The fixed-baseline primary cohort distinguishes Native, Adjacent and Remote with
19/20 cross-family class agreement and concrete epistemic changes in the Remote
cases. That result is dominated by Native judgments and does not establish robust
three-region control: only three primary cases are Remote, two reuse tomography,
boundary annotations agree on only 12/20 cases, and many intended contrasts collapse
to ties. Provisional cases agree on only 1/4 classes and 0/2 same-target orderings.
Evidence variants change labels despite unchanged mapping and baseline bytes.
Retain the distinctions for inspected research judgments; do not promote them to
an automatic reliability claim or advance to grounding/retrieval on this evidence.
No agreement target, consensus procedure, relabeling or adjudicator was used.

## Authorization and checkpoints

The user instructed implementation of the initially untracked
[plan](../../docs/PLAN-displacement-v0.3.md), including measurement, publication and
normal push. This supersedes A's earlier stop for this new experiment only. Historical
experiments and frozen Problem Frames remain byte-identical; the new analysis is a
[dated continuation](../../docs/PROBLEM_FRAMES-displacement-v0.3.md).

| Checkpoint | Commit |
| --- | --- |
| Fetched starting local/remote main | `2be6b72eee170152c3025b30e500dcf3f830f624` |
| Freeze Experiment B target-native baselines | `2c6eec7e7f5aceed0c0188aa9070afb56b2f68b0` |
| Prepare ontological displacement Experiment B | `e39e505` |
| Freeze Experiment B provider probes | `f453aff` |
| Freeze Experiment B displacement admission | `7a572cd` |
| Completion | Commit titled `Complete ontological displacement calibration v0.3` containing this report |

The eight baseline files and target tasks were authored and committed before source
selection and mapping authorship. Preparation was committed before all four artificial
probes. Probe evidence was committed before validity collection. All 52 validity
outputs were frozen before admission review, and admission was committed before
all 48 displacement calls. Displacement outputs were frozen before result review.

## Design and admission

24 core mappings cover eight tasks, with one intended Native, Adjacent and Remote
mapping per task. Two evidence-only variants produce 26 candidate packets. IDs were
shuffled with seed 20260927; validity and displacement orders use 20260928 and
20260929. Source names/practices and all five accepted instrument fields are copied
unchanged. No provisional extraction is used. Operator bands and variant relations
remain outside judge packets and are coverage intentions, not reference answers.

Baselines specify domain, verbatim task, practitioner role/specialty, ordinary methods,
ordinary evidence and uncertainty. They are authored synthetic hypotheses, not verified
practitioner consensus. The exact serialized baseline file bytes are embedded in every
corresponding displacement prompt, regardless of evidence availability or cohort.

The primary gate requires two unconditional Valid judgments with passing criteria.
Every Conditional requirement is preserved verbatim and reviewed for designation and
compatibility in [admission-review.json](../displacement-v0.3/admission-review.json).
All 28 returned conditions were designated instantiation-dependent in operator review; none was classified ontology,
mixed or uncertain. Two demand additional operations incompatible with the frozen
mapping. This sample therefore does not empirically exercise ontology-dependent
holdouts, although the contract tests reject them.

A returned 22 Valid, 3 Conditional and 1 Invalid; B returned 20 Valid and 6 Conditional.
Status agreement was 23/26. The admission result is 20 primary core cases, four
provisional cases (two core, two variants), and two core holdouts. The primary core
minimum passes: 20 cases, eight baselines, all three intended bands.

| Target | Task domain | Intended Native | Intended Adjacent | Intended Remote | Variants → base |
| --- | --- | --- | --- | --- | --- |
| T01 | production-regression diagnosis | 008 (primary) | 015 (primary) | 022 (holdout) | none |
| T02 | investigative reporting | 023 (primary) | 010 (primary) | 003 (primary) | none |
| T03 | literary textual formation | 004 (primary) | 026 (primary) | 005 (provisional) | 020 → 005 |
| T04 | organizational handoff delays | 016 (primary) | 024 (primary) | 018 (primary) | none |
| T05 | product-proposal decomposition | 019 (primary) | 006 (primary) | 007 (primary) | none |
| T06 | archival chronology | 025 (primary) | 001 (primary) | 002 (provisional) | 011 → 001 |
| T07 | software-release workflow failures | 013 (holdout) | 009 (primary) | 014 (primary) | none |
| T08 | product-rollout monitoring | 021 (primary) | 017 (primary) | 012 (primary) | none |

Provisional 002 assumes the existing impression/office/timing links and conditional
damage-date requirements; 005 assumes revision-state linkage and uniquely supported
alignment; 011 and 020 assume availability, shared-pattern behavior, independent
anchors and documentary links of their already mapped sequences. Assumptions contain
the exact reviewed condition strings and a fixed instruction to retain source,
mapping, target question and baseline. They make no claim those conditions are true.

Holdout 022 is A Invalid/B Conditional: delay localization did not supply A's required
deployed-change attribution. B additionally requested an attribution bridge including
revert/bisection. Holdout 013 is A Valid/B Conditional: B requested a real-workflow
remedy intervention and outcome evaluation beyond the frozen reduction operation.
That latter holdout is a conservative operator compatibility decision, not a new
validity judgment. The original disagreements and suggested reframe remain intact.

## Execution and provenance

A requested OpenAI `gpt-6-astra` with high reasoning; B requested Anthropic
`claude-fable-5-1[1m]` with high effort. Codex CLI was 0.157.1 and Claude Code 2.1.283,
one patch newer than A's recorded versions. All other A configuration settings were
retained: sequential processes, 900-second timeouts, isolated empty working directories,
fresh contexts, disabled tools/connectors/plugins/memory, and existing subscription
authentication. No credentials were retrieved or copied. Equal effort labels do not
establish equal compute. Temperature, seed and service tier used provider defaults.

All four post-preparation formatting/isolation probes passed. All 52 validity and
48 displacement calls completed with no scheduler failure, timeout, model substitution,
semantic repair, replacement measurement or rerun. There are 104 unique exposed
sessions including probes. Every stage's timestamps are sequential, and both families
received byte-identical prompts for each case. A exposes no returned model identifier;
B exposes `claude-fable-5-1`. Verified immutable serving snapshots are null for both.
Two exposed B formatting retries occurred during validity; zero were exposed during
displacement. A exposed none; hidden retries remain unknown rather than asserted absent.

| Stage | First start (UTC) | Last finish (UTC) | Judgments |
| --- | --- | --- | --- |
| validity | 2026-09-28T03:47:39.884176+00:00 | 2026-09-28T04:20:00.790366+00:00 | 52 |
| displacement | 2026-09-28T04:31:52.502590+00:00 | 2026-09-28T05:08:54.481695+00:00 | 48 |

The [execution audit](../displacement-v0.3/review/execution-audit.json) and stage
freezes retain commands, requested/returned model metadata and provenance, session IDs,
timestamps and private raw hashes. Raw attempts remain in ignored `.runtime/displacement-v0.3/`.
[Published judgments](../displacement-v0.3/judgments/displacement/) are unchanged returned
responses. The [packet index](../displacement-v0.3/packet-index.json) links every admitted
prompt in its primary/provisional directory; those files are exact measured prompt bytes.
No packet contains validity judgments, historical labels, intended bands or another judgment.

## Class and boundary results

All denominators below include every admitted packet in its cohort. No primary/provisional
reliability result is pooled. Primary all and primary core-only are identical because
both variants are provisional. Counts are single judgments, not estimates from repeats.

| Cohort | A N/A/R | B N/A/R | Class exact | Same / one-step / N↔R | Boundary exact | Disagreements with borderline |
| --- | --- | --- | --- | --- | --- | --- |
| Primary all/core | 13/4/3 | 14/3/3 | 19/20 (95.0%) | 19 / 1 / 0 | 12/20 (60.0%) | 1/1 |
| Provisional all | 1/2/1 | 0/3/1 | 1/4 (25.0%) | 1 / 3 / 0 | 3/4 (75.0%) | 3/3 |
| Provisional core only | 1/1/0 | 0/1/1 | 0/2 (0.0%) | 0 / 2 / 0 | 2/2 (100.0%) | 2/2 |

**Primary (20): confusion rows A, columns B.**

| A \ B | Native | Adjacent | Remote |
| --- | --- | --- | --- |
| Native | 13 | 0 | 0 |
| Adjacent | 1 | 3 | 0 |
| Remote | 0 | 0 | 3 |

**Provisional all (4): confusion rows A, columns B.**

| A \ B | Native | Adjacent | Remote |
| --- | --- | --- | --- |
| Native | 0 | 1 | 0 |
| Adjacent | 0 | 1 | 1 |
| Remote | 0 | 1 | 0 |

**Provisional core only (2): confusion rows A, columns B.**

| A \ B | Native | Adjacent | Remote |
| --- | --- | --- | --- |
| Native | 0 | 1 | 0 |
| Adjacent | 0 | 0 | 1 |
| Remote | 0 | 0 | 0 |

Post-result labels follow the frozen precedence: contested for a class disagreement,
otherwise boundary if either judge says borderline, otherwise consensus. Primary:
1 contested, 14 boundary, 5 consensus. Provisional: 3 contested, 1 boundary, 0 consensus.
These are review statuses, not replacements for original labels. Case 012 is a useful
warning: both judges choose Adjacent, but A's nearest alternative is Remote and B's
is Native. Exact class agreement can conceal different boundary interpretations.

## Dimension results

Each cell gives exact level agreement and mean absolute ordinal disagreement (MAOD).
Levels are independent true integers 0–3. No summed, averaged or weighted distance
profile is computed; MAOD compares raters on one dimension only.

| Dimension | Primary all/core exact; MAOD | Provisional all exact; MAOD | Provisional core exact; MAOD |
| --- | --- | --- | --- |
| entities | 15/20; 0.25 | 4/4; 0.00 | 2/2; 0.00 |
| relations | 15/20; 0.25 | 2/4; 0.50 | 1/2; 0.50 |
| processes | 13/20; 0.35 | 3/4; 0.25 | 1/2; 0.50 |
| operations | 16/20; 0.20 | 1/4; 0.75 | 0/2; 1.00 |
| observables | 15/20; 0.25 | 1/4; 0.75 | 0/2; 1.00 |
| inferences | 14/20; 0.30 | 1/4; 1.00 | 1/2; 1.00 |
| failure_modes | 11/20; 0.45 | 3/4; 0.25 | 1/2; 0.50 |

Failure modes are the least exact primary dimension (11/20); B sometimes gives level 1
for explicitly naming a hazard that its own rationale calls familiar. Provisional
operations, observables and inferences agree on only 1/4 levels each. Case 002 has a
two-level inference disagreement (0 versus 2). Conversely, 026 has identical full
profiles but different classes. The class boundary cannot be recovered mechanically
from the dimension vector, and the outputs do not support inventing such a rule.

## Relative ordering, including ties

Every unordered same-target pair among admitted cases is listed below, ordered by neutral
case ID. A and B entries express case 1 relative to case 2, not author intentions.
Primary: 15/16 relation agreement (93.75%); provisional all: 0/2 (0%). Provisional
core-only has no same-target pairs, so its rate is unavailable, not zero. The eight
cross-cohort comparisons are separately descriptive (5/8 agreement), never added to
primary or provisional reliability. This table includes all 26 unordered pairs.

| Target | Case 1 | Case 2 | Cohort comparison | A relation | B relation | Both core |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | 008 | 015 | primary | < | < | yes |
| T02 | 003 | 010 | primary | = | = | yes |
| T02 | 003 | 023 | primary | = | = | yes |
| T02 | 010 | 023 | primary | = | = | yes |
| T03 | 004 | 005 | cross-cohort | < | < | yes |
| T03 | 004 | 020 | cross-cohort | < | < | no |
| T03 | 004 | 026 | primary | < | = | yes |
| T03 | 005 | 020 | provisional | < | > | no |
| T03 | 005 | 026 | cross-cohort | = | > | yes |
| T03 | 020 | 026 | cross-cohort | > | > | no |
| T04 | 016 | 018 | primary | < | < | yes |
| T04 | 016 | 024 | primary | = | = | yes |
| T04 | 018 | 024 | primary | > | > | yes |
| T05 | 006 | 007 | primary | < | < | yes |
| T05 | 006 | 019 | primary | = | = | yes |
| T05 | 007 | 019 | primary | > | > | yes |
| T06 | 001 | 002 | cross-cohort | = | < | yes |
| T06 | 001 | 011 | cross-cohort | < | < | no |
| T06 | 001 | 025 | primary | = | = | yes |
| T06 | 002 | 011 | provisional | < | = | no |
| T06 | 002 | 025 | cross-cohort | = | > | yes |
| T06 | 011 | 025 | cross-cohort | > | > | no |
| T07 | 009 | 014 | primary | < | < | yes |
| T08 | 012 | 017 | primary | = | = | yes |
| T08 | 012 | 021 | primary | > | > | yes |
| T08 | 017 | 021 | primary | > | > | yes |

Primary ordering is coherent where concrete procedures differ: ticket tomography
018 exceeds monitoring 016 and signoff removal 024; replay reduction 007 exceeds
prototype removal 006 and differential discovery 019; release tomography 014 exceeds
log corroboration 009. T02's three intended bands all become Native, and T08's intended
Adjacent/Remote mappings tie as Adjacent. Thus ordering supports distinguishable
regions in some tasks, not uniform three-step control across all eight targets.

## Evidence variants and baseline stability

- **001 → 011, archival event sequences:** base is primary Native/Native; the missing-evidence
  variant is provisional Adjacent/Adjacent. A moves clear to borderline; B remains
  borderline but changes its alternative from Adjacent to Remote. Both now emphasize
  candidate offsets and match measures appearing in the applicability conditions.
- **005 → 020, literary copying counts:** both are provisional. A moves Adjacent/borderline
  to Remote/clear; B moves Remote/borderline to Adjacent/borderline. This reverses the
  families' relative ordering of otherwise identical mappings and baseline bytes.

The candidates differ only in evidence and neutral IDs. The displacement packets also
differ in admission-derived assumptions and, for the first pair, provisional status.
Consequently these observations cannot isolate an evidence-availability causal effect
from condition wording, reasoning variability or single-draw noise. They do show that
byte-stable baselines are insufficient for stable interpretation. Both judges explicitly
deny that missing evidence alone determines class, but assumptions sometimes make the
same mapping read as more formal or more central. No baseline was edited or repaired
following these results. Conditions are not practitioner-consensus evidence.

## Review of every admitted pair

The complete authored reviews, including every dimension disagreement, are in
[case-reviews.json](../displacement-v0.3/review/case-reviews.json). All 24 admitted pairs
are reviewed, including five primary consensus cases. The table retains original classes
and lists the post-result status; variants are explicit.

| Case | Cohort/type | A / B | A boundary / B boundary | Review status |
| --- | --- | --- | --- | --- |
| 001 | primary/core | Native / Native | clear / borderline | boundary |
| 002 | provisional/core | Native / Adjacent | borderline / borderline | contested |
| 003 | primary/core | Native / Native | borderline / borderline | boundary |
| 004 | primary/core | Native / Native | clear / borderline | boundary |
| 005 | provisional/core | Adjacent / Remote | borderline / borderline | contested |
| 006 | primary/core | Native / Native | clear / borderline | boundary |
| 007 | primary/core | Remote / Remote | borderline / borderline | boundary |
| 008 | primary/core | Native / Native | clear / clear | consensus |
| 009 | primary/core | Native / Native | clear / borderline | boundary |
| 010 | primary/core | Native / Native | borderline / borderline | boundary |
| 011 | provisional/variant of 001 | Adjacent / Adjacent | borderline / borderline | boundary |
| 012 | primary/core | Adjacent / Adjacent | borderline / borderline | boundary |
| 014 | primary/core | Remote / Remote | clear / borderline | boundary |
| 015 | primary/core | Adjacent / Adjacent | borderline / borderline | boundary |
| 016 | primary/core | Native / Native | clear / clear | consensus |
| 017 | primary/core | Adjacent / Adjacent | borderline / borderline | boundary |
| 018 | primary/core | Remote / Remote | clear / borderline | boundary |
| 019 | primary/core | Native / Native | clear / borderline | boundary |
| 020 | provisional/variant of 005 | Remote / Adjacent | clear / borderline | contested |
| 021 | primary/core | Native / Native | clear / clear | consensus |
| 023 | primary/core | Native / Native | clear / clear | consensus |
| 024 | primary/core | Native / Native | clear / borderline | boundary |
| 025 | primary/core | Native / Native | clear / clear | consensus |
| 026 | primary/core | Adjacent / Native | borderline / borderline | contested |

The four contested pairs identify three distinct issues. In 026, systematic tabulation
is either an extension or already naturalized manuscript argument, despite identical
profiles. In 002, following a marking tool rather than a letter changes the inferred
object and chained warrant but not the provenance toolkit. In 005 and 020, new numerical
dating evidence is either substantive local reorganization or a bounded input into
otherwise ordinary textual formation research. These conflicts remain unresolved.

Concordant examples also matter. 008/019 show diagnosis naturalized across software and
product discovery; 016/021 show serial monitoring naturalized across operations and
rollouts; 023/025 anchor explicit corroboration/provenance baselines. Concordant 007
changes experiment selection and its minimality warrant. Concordant 014/018 replace
direct stage observation with inverse constraints and coverage/non-uniqueness questions.
Concordant 012 shows that transient-shape measurement can remain Adjacent when the
underlying monitoring and decision procedure remain familiar.

## Shortcut and coverage audit

- **Different disciplines → Remote:** contradicted by Native diagnosis, monitoring,
  corroboration and event-list crossdating. Ratios were not derived from discipline names.
- **Same/adjacent disciplines → Native:** tested with Remote-intended clause provenance
  003 and block provenance 002. The former is Native/Native; the latter Native/Adjacent.
  Their rationales compare actual object/warrant changes, so they do not by themselves
  establish a disciplinary shortcut. No realized same-domain Remote example survives;
  that direction remains under-supported, rather than counted as demonstrated coverage.
- **Vocabulary versus operation:** clinical diagnostic vocabulary leaves 008 Native;
  ordinary rule-removal language makes 007 Remote through its minimality search. Source
  terminology alone does not explain the classes. Some level-1 failure-mode increments
  nevertheless reward explicit naming of familiar hazards (008, 019, 021), a dimension
  calibration concern.
- **Repeated instruments:** ACH is Native for reporting, Adjacent for engineering and
  rollout monitoring, and contested for literary formation. Tomography is Remote in
  admitted operations/release cases but the production attribution mapping is held out.
  Crossdating is Native for supplied event lists and unstable for count-series variants.
  The admitted delta-debugging example is Remote for product decomposition; its intended
  Native release counterpart was held out, limiting that paired comparison.
- **Grounding contamination:** no output contains grounding fields and no observed class
  rationale treats weak support as sufficient for Remote. The inverse cases distinguish
  changed warrants from withheld logs. Synthetic validated forward models make this a
  favorable test; no independent grounding assessment or broad claim of decontamination
  is justified.
- **Mechanical dimension counting:** no aggregate or explicit threshold is present.
  Identical profiles with different labels in 026 oppose a deterministic counting rule.
  Statements about a dimension changing the balance remain qualitative judgments, not
  evidence of an observed numerical classifier.
- **Evidence availability redefining practice:** literal baselines remain identical and
  judges often explicitly distinguish absence from nativeness. Variant label shifts and
  condition-driven formalization still demonstrate instability of interpretation.
- **Baseline scope drift:** B sometimes narrows the ordinary baseline to snapshot-based
  rollout monitoring (012), gives an unstated priority to material evidence over custody
  (004), or assumes sequential leading-suspect diagnosis (015). These are interpretive
  additions, not measured practitioner facts. The fixed baseline limits but does not
  eliminate them.

Operator intentions are used only for this coverage audit. They never enter agreement
numerators, replacement labels or a correctness score.

## Limitations, recommendation and unresolved concepts

This is an authored synthetic set with eight unverified practice baselines, one draw
per family/case, admission selection, highly related repeated instruments, opaque
backend snapshots and no within-family repeatability estimate. The 20 primary cases
are mostly Native; all-primary/core identity is a design consequence, not an additional
replication. Only three Remote cases survive primary admission and two share tomography.
Four provisional cases cannot support general population reliability estimates.

The study provides useful qualitative separation when it names a concrete new operation
and warrant, and its primary within-target ordering is mostly coherent. It does not
show uniformly distinguishable Native/Adjacent/Remote regions, stable provisional
classification or stable interpretation under evidence variants. Recommend retaining
the model as a research description with explicit baselines and original paired judgments;
do not treat it as a validated automatic control or promote grounding C/retrieval work.
The authorization ends with this experiment's verification, publication and push.

Unresolved concepts are: whether substantive change in one central subtask suffices
for Remote when downstream inquiry is unchanged; when formalizing ordinary comparison
crosses Native/Adjacent; how changing a tracked object's granularity changes inquiry;
which dimensions distinguish explicit wording from a real epistemic change; how to keep
instantiation assumptions from becoming new operational instructions; and when a bounded
contribution suffices for validity rather than requiring a fuller target answer. These
are findings for future deliberation, not tasks executed here.

## Verification

The five historical suites contain 78 passing tests. B's 21 preparation tests exercise
strict fields, true-integer dimensions (booleans/floats rejected), invalid boundary
alternatives, duplicate keys, packet blinding, identical family bytes, immutable baseline
embedding, incompatible/ontology/mixed/uncertain conditions, holdout blocking, assumptions
unable to replace baseline fields, viability exclusions, known ties and ordinal steps,
missing pairs, empty cohorts, precedence, isolation, timeout retention, malformed-output
retention, model fallback, tool/plugin leakage, duplicate sessions and repeat-run refusal.
The post-freeze checker recomputes every published metric and ordering relation, verifies
104 unique sessions, schedule and checkpoint chronology, exact published packet bytes,
all-case review coverage, original labels, status precedence and private artifact hashes.

Final verification also runs the historical preparation/completion verifiers, including
private v0.1/v0.2/A hashes, B's completion verifier, `git diff --check` and `git status`.
The [machine-readable verification record](../displacement-v0.3/review/verification.json) accompanies the completed publication. No
historical input, accepted instrument, old test or frozen Problem Frames file is changed.
