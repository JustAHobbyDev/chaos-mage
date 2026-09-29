# Experiment E — Natural-output anti-collapse v0.1: incomplete

2026-09-29. **Experiment E stopped during neutralization auditing, before any
transfer-validity or anti-collapse judgment. It provides no answer about whether the
frozen gate preserves naturally generated strange-but-valid reasoning.** The next
OpenAI audit was blocked before launch because the installed `codex` command changed
from the frozen CLI version 0.157.1 to 0.158.0. No model substitution or retry occurred.

A separate implementation defect also matters: the frozen generation self-label
checker incorrectly excluded three structurally valid outputs for innocuous uses of
“novel” and “novelty.” These are harness false positives, not evidence of generator
self-assessment and not anti-collapse rejections. The original outputs remain intact.
Neither the checker nor the cohort was changed after collection.

## Checkpoints, models and execution

| Checkpoint | Commit |
|---|---|
| Verified starting local/remote main | `16dd7eb3a35f41a278f3798feef64d3318e9c457` |
| Baselines, assignments, prompts, schemas and harness | `c56d4bf313a82f88c07e9183a8adccbd2d104c45` |
| Generation probes | `170f96c75d385c45f8779be14845e2621593ccd8` |
| All generation outputs and exclusions | `235882247258bec735b80e7b515f3613512a6841` |
| Blind neutralizer inputs | `503a69b3cd4e3747b0f3cff8376eac5768ff8e47` |
| Neutralizer probes | `01d90b42eaa54658ea58465089c41c62218c4992` |
| Neutralizations | `9a08e44ab6123c25e2efbd5fdc4c2fbefd9974ae` |
| Independent audit inputs | `a24cd80a1f35dd4c96daab24283746b0d9ff6d13` |
| Audit probes | `cd16b3261b1f2722c4bd124815771b6811232fe9` |
| Failure and partial audit evidence | `68fda61e031cbba53efd55a7ed15f2c87c320f11` |
| Incomplete-run publication | Containing commit titled `Publish incomplete natural-output anti-collapse experiment`; its resolved SHA is reported after commit/push |

The publication commit cannot contain its own hash. The
[review binding](../anti-collapse-natural-v0.1/review/result-binding.json) binds this
review to the committed failure freeze. All earlier experiment artifacts and accepted
instruments remain unchanged.

| Family | Requested model | Effort | CLI used for completed calls | Exposed returned identifier |
|---|---|---|---|---|
| A / G1 | `gpt-6-astra` | high reasoning | codex-cli 0.157.1 | Not exposed |
| B / G2 | `claude-fable-5-1[1m]` | high | Claude Code 2.1.283 | `claude-fable-5-1` |

Six artificial probes passed: two each for generation, neutralization and audit.
No validity or anti-collapse probes were run. There were **84 distinct provider
sessions**: six probes, 30 generations, 27 neutralizations and 21 audit judgments.
The failed prelaunch version check is not a provider session or judge observation.
Immutable serving snapshots remain unknown, and equal effort labels do not establish
equal compute. Temperature, provider seed and service tier were unset.

Calls were sequential, with fresh processes/sessions, empty working directories and
900-second timeouts. Repository/user rules, memory, tools, browsing, retrieval, hooks,
plugins and connectors were disabled; native structured-output formatting alone was
allowed. Existing subscription authentication was consumed without retrieving or
copying credentials. No SSH was used. Native formatter retry metadata remains in the
frozen records; no harness retry or replacement measurement occurred.

## Frozen targets, sources and generation

All six Experiment D baseline files were copied byte-for-byte: software regression,
investigative reporting, literary textual formation, organizational handoff delays,
product-proposal decomposition and archival chronology. Practitioner scope was not
narrowed. D's synthetic target evidence fixtures were omitted. Planned downstream
`target.evidence` is empty, so generated assumptions cannot become supplied evidence.
These baselines remain authored hypotheses about practice, not verified consensus.

The fixed 30 assignments use all fourteen accepted instruments, each two or three
times and in both generator families. No instruments were extracted. Each target has
five assignments; each generator has fifteen. The following table names requested
sources, not intended or observed novelty categories.

| Target | G1 sources | G2 sources |
|---|---|---|
| T01 software regression | Differential diagnosis; dechallenge/rechallenge; ACH | Delta debugging; seismic tomography |
| T02 reporting | Source corroboration; chain of custody | ACH; crossdating; chromatography |
| T03 textual formation | Provenance reconstruction; luminol; chromatography | Chain of custody; crossdating |
| T04 organizational delays | Serial monitoring; seismic tomography | Differential diagnosis; regression bisection; step-response probing |
| T05 product proposal | Delta debugging; step-response probing; chromatography | Dechallenge/rechallenge; serial monitoring |
| T06 archival chronology | Crossdating; regression bisection | Provenance reconstruction; source corroboration; luminol |

The generator received target question, exact baseline, unchanged accepted source
instrument and instructions for a concrete operational transfer. It received no gate
criteria, verdicts, benchmark examples, ladder positions, novelty goals, distance
rankings or diversity objectives. The schema requires the five mapping fields plus
operational explanation and uncertainty; it requests no self-assessment. The mapping
fields define the downstream assessment unit. Every generation used an independent
context, and all outputs froze before neutralization. There was no output selection by
the operator, replacement generation or duplicate control.

Seeds 20260929051 through 20260929056 fix opaque identities and the five schedules.
Downstream schedules filter the original assignments without reshuffling. Preparation
and provider-probe commits preceded their corresponding model calls.

All **30 provider responses passed the generation JSON schema**. The additional frozen
wording check excluded three, leaving 27 generation-stage successes, split 14 G1 / 13
G2. Calling the three cases generation failures describes the runner's recorded
status, not malformed JSON or failed provider execution.

## Content-exclusion defect and blind neutralization

The checker matched vocabulary anywhere in mapping or explanation strings instead
of identifying a self-assessment. Post-failure inspection establishes three false
positives:

| Case | Target / generator | Matched language | What the wording means |
|---|---|---|---|
| E030 | T03 / G2 | “the novel as a whole” | The literary work being studied. |
| E027 | T03 / G1 | “the whole novel's formation” | A limitation on interpreting the literary work. |
| E029 | T05 / G2 | “novelty effects” and “novelty fading” | Temporal behavioral effects in product evaluation. |

The [lexical review](../anti-collapse-natural-v0.1/review/content-exclusion-review.json)
quotes bound evidence from the original payloads. None of these phrases is a claim
that the mapping is novel or creative. The implementation therefore failed to enforce
the intended semantic requirement accurately. Its tests covered vocabulary rejection
but missed domain-appropriate uses of those words. This is a substantive sampling
limitation: two literary cases and one product case lost access to neutralization.
They have not been readmitted, rewritten or regenerated.

The 27 remaining mappings were neutralized by the opposite family: 13 by A and 14 by
B. Neutralizers received only opaque ID, target question and the five-field mapping;
they saw no baseline, source metadata, generator identity, gate criteria or judgments.
All 27 returned the seven required fields and passed the explicit verdict-wording ban.
Their outputs froze before the first audit. No neutralization was repaired or retried.

Passing the lexical ban does not prove absence of semantic evaluative bias. It also
does not prove that operations, signals or limits were preserved. Those questions
belong to the independent audits, which did not finish.

## Partial audit and the execution halt

Of 54 planned fidelity judgments, **21 completed**: ten from A and eleven from B.
There are four complete paired audits (E006, E014, E023, E026). The partial verdict
counts are A: nine pass, one exclude; B: nine pass, two exclude. These describe a
truncated execution sequence, not a completed neutralization-admission cohort.

The three observed exclusion judgments identify the following concerns:

- **E001-A:** a recording requirement for usable references was broadened to every
  inspected item, adding operational scope.
- **E007-B:** the paraphrase may add a count-based comparison criterion and treat the
  existence of further witnesses as assumed. The auditor records uncertainty because
  faithful formulations also remain elsewhere in the paraphrase.
- **E013-B:** dropping “only” may weaken necessary conditions and negative inference
  limits for chronology claims. The auditor records uncertainty because other language
  still implies some restrictions.

These are unchanged auditor observations, not adjudicated findings about fidelity.
They demonstrate why lexical compliance alone is inadequate. Full audit exclusion
counts and agreement remain unavailable; no case was admitted to anti-collapse.
The [partial freeze](../anti-collapse-natural-v0.1/audit-partial-freeze.json) distinguishes
completed judgments, the failed setup attempt and calls never scheduled.

At `audit-E021-A`, the per-call guard read `codex-cli 0.158.0` instead of the frozen
`codex-cli 0.157.1`. The `codex` command resolves through mise's mutable `latest`
installation alias. The alias now points to 0.158.0; the installed version-specific
0.157.1 executable still reports 0.157.1. The actor or mechanism that advanced the
alias is unknown, so an automatic-update cause is not claimed as established.

The failure happened **before subprocess launch for a model request**: the retained
attempt contains prompt and validation evidence but no request reservation, stream or
response. The remaining 33 audit calls, including that blocked call, were not launched.
There is no observation to repair or replace for the failed call. Scheduling stopped
as required by the frozen policy; the original failed attempt remains preserved.

## What is—and is not—established

| Requested outcome | Result |
|---|---|
| Target / accepted-source coverage | Six targets, fourteen sources; all 30 assigned generations returned. |
| Generation / neutralization attrition | Three false lexical generation exclusions; zero of 27 neutralizations failed schema/wording checks. |
| Neutralization-audit exclusions | Incomplete; three exclusion judgments among 21 responses, not a complete case-level denominator. |
| Validity admission / exclusion | Not measured: zero validity calls. Counts are null, not zero admitted/excluded findings. |
| Anti-collapse distributions / survival fraction | Not measured: zero anti-collapse calls. |
| Status, keep/reject, locus, materiality, native-reduction and formalization agreement | Not measured. |
| Every CLEAR_COLLAPSE / BORDERLINE_KEEP / status disagreement | No measured cases; absence of measurement is not zero incidence. |
| Same-status mechanism disagreements | Not measured. |
| Natural formalization / one-rule findings | Not reviewed or classified. |
| Generator-family collapse/keep comparison | Unavailable; only the fixed 15/15 generation assignment and 14/13 wording-check survivors are reportable. |
| Source-instrument collapse/keep comparison | Unavailable; source coverage does not establish a status pattern. |
| Neutralization bias | Wording compliance observed in 27 outputs; fidelity/bias unresolved, with three partial audit concerns. |
| Action-centric gate behavior | Unknown. |
| Suppression of unusual valid mappings | Unknown. |
| Removal of native collapse | Unknown. |
| Permissiveness for Chaos Mage generation | Unknown. |

The [metrics file](../anti-collapse-natural-v0.1/metrics.json) uses explicit nulls for
unmeasured results and retains the execution counts. No primary denominator was shrunk
to the completed audit prefix. The 18-case/five-target admission condition was never
assessed: this is an **incomplete execution**, not a finding of insufficient natural
coverage or a negative gate result. No operator novelty labels were assigned to the
mappings. No qualitative result was inferred from source names or generator identity.

## Verification, limitations and recommendation

Preparation passed all 216 historical tests and 47 new tests, plus historical public
and private verifiers. The final [test record](../anti-collapse-natural-v0.1/review/verification.json)
repeats those checks; the [completion record](../anti-collapse-natural-v0.1/review/completion-verification.json)
adds read-only incomplete-run verification: historical preservation, exact packet and
payload hashes, all complete stage freezes, the partial audit prefix, failure retention,
84 unique sessions, unchanged classifier bytes, independent metric recomputation and
absence of validity/anti-collapse calls. Passing tests did not prevent the semantic
false-positive checker defect; that limitation is retained explicitly.

This run's main limitations are its interruption, false lexical exclusions, incomplete
fidelity audit, absent validity and anti-collapse measurements, small purposive sample,
unverified practitioner baselines, coupled generator/neutralizer families and unknown
serving snapshots. It supports no conclusion about the frozen gate's effectiveness.

**Recommended next step: an explicitly authorized Experiment E recovery amendment,
not a follow-on experiment.** Pin the installed version-specific CLI executable and
re-probe it without altering either judge classifier. Preserve all existing outputs,
failures and hashes. Specify how to retain the 21 completed audits and resume unlaunched
work with separately recorded execution commits. Correct the self-label checker to
recognize evaluative self-description, add regression cases for literary “novel” and
behavioral “novelty effects,” and obtain explicit authorization for any readmission of
the three unchanged outputs. Do not generate replacements or silently rewrite the
original frozen procedure. No recovery is executed here.

The version-drift incident is recorded in the shared development papercut log with a
linked deferred environment task. Project-specific checker correction remains in this
report's recovery recommendation. No global prevention, grounding, diversity filter,
distance ranking, retrieval integration or production gate was implemented.

Publish this incomplete record with a normal push to main. If the push fails, stop and
report it. Local/remote SHA equality and the final publication SHA are reported after
publication; the containing commit cannot record its own hash.
