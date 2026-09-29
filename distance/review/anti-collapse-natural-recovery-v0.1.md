# Experiment E — natural-output recovery: insufficient coverage

2026-09-29. **Experiment E reached its prespecified coverage stop: only 8 mappings
were admitted, below the required 18. All six targets are represented. No anti-collapse
probe or judgment was run.** The recovery completed generation revalidation,
neutralization, two-family fidelity auditing and two-family transfer validity.

The experiment therefore does **not answer** whether the frozen anti-collapse gate
preserves naturally generated strange-but-valid reasoning while removing native
collapse. Eight admitted mappings out of thirty is an upstream admission count,
not an anti-collapse survival rate. No claim about suppression, retention,
permissiveness, action bias or gate agreement follows from it.

The principal bottleneck was transfer validity: 9/30 mappings were Valid/Valid.
Neutralization auditing excluded one of those nine, leaving eight. Even removing
the audit requirement would leave coverage below the frozen minimum. No replacement
generation, threshold change, classifier tuning, grounding, distance analysis,
diversity filtering or production integration was performed.

This is the terminal report for the authorized recovery. The
[original incomplete report](anti-collapse-natural-v0.1.md), its metrics, all earlier
experiments and the prelaunch CLI-version failure remain unchanged. The recovery's
README, amendment and paused-readiness record describe its earlier preparation
checkpoint; [RESULT.md](../anti-collapse-natural-recovery-v0.1/RESULT.md) records the
terminal state. The [review binding](../anti-collapse-natural-recovery-v0.1/review/result-binding.json)
ties this review to the committed admission freeze.

## Checkpoints and recovery boundary

| Checkpoint | SHA |
|---|---|
| Experiment D / expected original starting main | `16dd7eb3a35f41a278f3798feef64d3318e9c457` |
| Original E baselines, assignments, prompts and harness | `c56d4bf313a82f88c07e9183a8adccbd2d104c45` |
| All thirty original generation responses frozen | `235882247258bec735b80e7b515f3613512a6841` |
| Original twenty-seven neutralizations frozen | `9a08e44ab6123c25e2efbd5fdc4c2fbefd9974ae` |
| Original partial audits and failure frozen | `68fda61e031cbba53efd55a7ed15f2c87c320f11` |
| Published incomplete E verification / recovery base | `6f5b43b3ba7455f9fd5d95640f6be5ba9e1ff61a` |
| Local CLI pin, recovery amendment and imported evidence | `ea49dc19c7bd5482fb830a30877ee15233b2dce4` |
| Restored neutralization packets; execution paused | `4bfddbfa583eaecabdb7930d423703bfce672b5f` |
| User instruction to resume recorded | `f1134cece60b43e54ce1d63bacae72b7f7604c7a` |
| Recovery neutralization probes | `80950386bd18e3ce218eab547bb079e5743f8271` |
| All thirty neutralizations frozen | `40cb8d5c6cc8f89e0bd2b917dcbbdfe839abc4a6` |
| Remaining audit inputs | `df92d850b80ceffacb8ef6a0efb96839ee9c1145` |
| Recovery audit probes | `1cf24c10d41f0ae14ecf76036f324fdc98ceb8ea` |
| All sixty fidelity judgments frozen | `5cad1211cc3c43b059fd00561573008af0e934fc` |
| Transfer-validity inputs | `8527450bb53d27f6e458b19fb59052359ed652b8` |
| Transfer-validity probes | `c4060fbd72cc554ae79bd51b817f8bf098e715c8` |
| All sixty transfer-validity judgments frozen | `91e223eecbb12c8e2595de5331fdf6c3b9184c5f` |
| Terminal admission / insufficient-coverage freeze | `a7856403200fb8e826993798750c13ef3545bc82` |

The original report contains the remaining pre-recovery probe/input checkpoints.
The containing publication commit is titled `Complete Experiment E recovery with insufficient coverage`;
its resolved SHA is reported after commit. A commit cannot contain its own hash.

The original generation checker rejected E027 and E030 for the literary noun
“novel,” and E029 for behavioral “novelty effects,” fading and decay. All thirty
outputs were schema-valid. The prior post-failure diagnostic established these
three lexical false positives before recovery was authorized. Recovery uses
[exact hash-bound exceptions](../anti-collapse-natural-recovery-v0.1/lexical-corrections.json)
for these unchanged payloads. It neither rewrites the original exclusions nor
generalizes the exception to future outputs. Thus the original recorded cohort
was 27; the explicitly amended cohort is 30. This is a disclosed correction after
an interrupted run, not an uninterrupted execution of the original checker.

The [import manifest](../anti-collapse-natural-recovery-v0.1/imports.json) retains
all original sessions, timestamps, validations, response hashes and execution
commits. It reuses 30 generations, 27 neutralizations and 21 completed audits.
Recovery collected only three missing neutralizations, 39 missing audits and 60
validity judgments, plus six artificial probes. The originally blocked E021-A audit
had no launched provider request; its successful recovery call used a new directory
and session. Neither completed judgments nor generations were replaced.

## Models, CLI configuration and isolation

| Role family | Requested model | Effort | CLI for completed calls | Exposed returned identifier |
|---|---|---|---|---|
| A / generator G1 | `gpt-6-astra` | high reasoning | Codex CLI 0.157.1 | Not exposed |
| B / generator G2 | `claude-fable-5-1[1m]` | high | Claude Code 2.1.283 | `claude-fable-5-1` |

Generator and neutralizer families are crossed. Both families independently judge
every fidelity audit and validity mapping. The frozen anti-collapse configuration
would have used the same pair, but that stage was not executed. No model was silently
substituted. Immutable serving snapshots remain unknown; equal effort labels do not
establish equal compute. Temperature, provider seed and service tier were unset.

Repository `mise.toml` pins Codex 0.157.1. The
[execution configuration](../anti-collapse-natural-recovery-v0.1/execution-config.json)
records version-specific absolute executable paths and hashes for both CLIs;
hash/version checks precede recovery calls. This avoids the mutable `latest` alias
that caused the original prelaunch stop. CLI 0.158.0 was detected at that failed
attempt, not used for a completed measurement.

Every call used a fresh process and session, an initially empty working directory,
sequential scheduling and a 900-second timeout. Tools, browsing, retrieval, repository
and user rules, memory, hooks, plugins and connectors were disabled. Only native
structured-output machinery was enabled. Existing subscription authentication was
consumed without copying credentials. No SSH was used. Stage inputs and two artificial
probes were committed before each measured stage.

There were **192 unique provider sessions**: 30 generations, 30 neutralizations,
60 fidelity audits, 60 validity judgments and 12 artificial probes. Of these, 84
preceded recovery and 108 occurred during it. Each family accounts for 96 sessions.
No recovery provider/formatting failure occurred. Both families exposed zero
formatter retries; hidden provider retries cannot be ruled out merely from that
observation. No harness retry, model substitution or completed-measurement replacement
occurred. No anti-collapse preflight or measurement was scheduled.

## Generation procedure and coverage

All six Experiment D baselines were copied byte-for-byte with the same practitioner
scope. No target was replaced or narrowed. The original 30-assignment manifest uses
14 accepted instruments, each two or three times and in both generator families.
No instruments were extracted. Every target has five mappings; each generator has
fifteen. Seeds 20260929051–20260929056 fix identities and schedules. Recovery filters
those schedules to missing calls without reshuffling their relative order.

Each generator received the target question, exact baseline, source instrument and
instructions for a concrete operational transfer. It saw no anti-collapse criteria,
verdicts, synthetic ladder examples, distance ranking, diversity objective or prior
mapping. All generation outputs froze before neutralization or qualitative review.
There was no selection by perceived novelty, maximally-weird instruction, duplicate
control or replacement generation. The five mapping fields are the assessment unit;
the separate explanation cannot add operative content to downstream packets.

The target evidence array is empty. D's synthetic evidence fixtures were not reused,
and a generated assumption did not become a supplied target fact. That choice is
material to the validity attrition discussed below.

| Target | Generated | Both fidelity audits pass | Valid/Valid | Primary admitted |
|---|---:|---:|---:|---:|
| T01 software regression debugging | 5 | 5 | 2 | 2 |
| T02 investigative reporting | 5 | 5 | 2 | 2 |
| T03 literary textual formation | 5 | 2 | 1 | 1 |
| T04 organizational handoff delays | 5 | 3 | 1 | 1 |
| T05 product/proposal analysis | 5 | 5 | 1 | 1 |
| T06 archival chronology | 5 | 3 | 2 | 1 |
| **Total** | **30** | **23** | **9** | **8** |

All thirty generation payloads pass schema validation. The amended cohort has zero
generation failures, while the three original lexical exclusions remain visible in
the preserved failed-run record. They are harness false positives, not malformed
generations or collapse decisions.

## Blind neutralization and audit findings

Neutralizers received only the opaque case ID, target question and original five-field
mapping. They received no native baseline, source metadata, model identity, generation
explanation, gate instructions, prior judgment or operator expectation. All thirty
seven-field paraphrases passed the schema and explicit evaluative-wording ban. There
were zero neutralization generation failures and no repaired or regenerated paraphrases.

Both auditors received only the original mapping, target question and neutral procedure.
They assessed preservation rather than novelty or target validity. Family A returned
27 pass / 3 exclude; B returned 24 pass / 6 exclude. Both passed 23 cases, both excluded
two, and five had an audit-status disagreement. Any non-pass check, including uncertainty,
excluded the paraphrase from primary admission. This rule is separate from the
anti-collapse gate's uncertainty-means-keep policy.

| Case | A / B fidelity result | Recorded concern |
|---|---|---|
| E001 | exclude / exclude | Recording requirements expand from usable references to every inspected item, including undated documents. |
| E007 | exclude / exclude | Possible remnants and available witnesses become assumed existing features/witnesses; a summary may add counting of supported relationships. A also flags ambiguity in the chemical prohibition. |
| E009 | pass / exclude | B is uncertain whether negated annual/environmental contrasts retain source imagery after explicit source names are removed. |
| E013 | pass / exclude | B is uncertain whether removing restrictive “only” language weakens necessary conditions on dating inferences. This is the sole Valid/Valid case lost to audit. |
| E021 | pass / exclude | B finds categorical summary language where the original conditionally groups co-traversed handoffs, potentially dropping the role of intermediate observations. |
| E022 | exclude / pass | A finds the capacity inference narrowed from an intake change to an intake increase. |
| E030 | pass / exclude | B finds the loss of “only” broadens which claims a broken transition can weaken; removal of the source comparison may also obscure the stated weakening of inference. |

The [case-level attrition record](../anti-collapse-natural-recovery-v0.1/review/attrition.json)
preserves both auditors' exact non-passing checks, evidence and rationales. Some
exclusions are explicit failures; others are unresolved fidelity concerns. This
report does not silently adjudicate them into passes.

Across the sixty judgments, signal, stopping-condition, next-inquiry and
no-verdict-language checks all passed. Operation preservation had one uncertain
judgment; inference had two failures and two uncertainties; limits had one failure
and one uncertainty; no-added-content had two failures and three uncertainties;
no-source-imagery had one uncertainty. No evaluative verdict leakage was detected
by either the lexical screen or the auditors. This does not prove perfect semantic
neutrality. The concrete concerns show that paraphrasing can add assumptions,
broaden or narrow scope, or weaken constraints without using forbidden verdict words.
No consistent bias toward apparent collapse or departure was measured, because the
gate was never run.

## Transfer-validity admission and attrition

The unchanged v0.3 classifier evaluated each original mapping, source instrument
and target question, including mappings excluded by fidelity audit. It received no
neutralization, audit verdict, generator identity or operator review.

| Validity status | Family A | Family B |
|---|---:|---:|
| Valid | 12 | 13 |
| Conditional | 14 | 17 |
| Invalid | 4 | 0 |

The pairs were 9 Valid/Valid, 11 Conditional/Conditional, 3 Valid/Conditional,
3 Conditional/Valid, 1 Invalid/Valid and 3 Invalid/Conditional. Exact validity-status
agreement is 20/30; this is **not anti-collapse agreement**. Twenty cases have at
least one Conditional judgment; four have an Invalid judgment, with three overlapping
those twenty. Thus 21 distinct mappings fail Valid/Valid admission. Seven fail audit,
six overlap the validity exclusions, and 22 distinct mappings fail primary admission.

The eight primary cases are **E003, E004, E005, E016, E020, E024, E026 and E027**.
E013 is the ninth Valid/Valid mapping but fails the fidelity requirement. The exact
case-by-case decisions and review categories are in the attrition record; categories
are only `validity-excluded` and/or `neutralization-excluded`. Admitted cases have no
anti-collapse review label. No case was labeled native, novel, collapse or departure
by the operator.

Most Conditional rationales name absent target capabilities or evidence: reliable
timestamps and comparison records, reproducible and separable interventions,
independent chronology anchors, distinctive overlapping sequences, an adequate
forward model, or a demonstrated connection from test results to the actual target.
These are judge-stated conditions, not newly collected evidence.

The treatment of prospective procedures is a significant calibration question.
E010, E012 and E023 are Conditional for A but Valid for B; E007, E014 and E019 go in
the other direction. In E010, B explicitly describes its choice to treat verified-at-
execution data assumptions as execution preconditions rather than validity conditions.
In E003, E004, E005, E016, E020, E024, E026 and E027, both judges accept a bounded
procedure despite absent observed outcomes. Conversely, both mark E002, E008, E009,
E011, E017, E018, E021, E025, E028 and E029 Conditional for specific unestablished
conditions, alongside E001. This is not evidence that all such decisions are wrong
or interchangeable. It shows that unconditional admission of prospective natural
transfers depends on a boundary the two families sometimes interpret differently.

The four Invalid judgments identify additional, concrete inference concerns:

| Case | A's stated failure | B's result |
|---|---|---|
| E006 | Surviving competing hypotheses are turned into a categorical claim that the procurement process was irregular. | Valid |
| E015 | Differential treatment profiles are used to rank checkpoints by contribution to the award outcome without a supplied attribution method. | Conditional |
| E022 | Response dead/settling times are treated as locations of accumulated waiting, and transient downstream overshoot as delay relocation. | Conditional |
| E030 | Continuous handling documentation is taken to support unchanged authorial arrangement, although continuity can document rearrangement. | Conditional |

These are validity disagreements, not anti-collapse mechanism disagreements or
dangerous gate suppression. The mappings and judgments were preserved unchanged.

## Generator-family and source descriptions

| Generator | Generated | Both audits pass | Valid/Valid | Validity admission rate | Primary admitted |
|---|---:|---:|---:|---:|---:|
| G1 / A | 15 | 12 | 7 | 7/15 (46.7%) | 7 |
| G2 / B | 15 | 11 | 2 | 2/15 (13.3%) | 1 |

These are descriptive admission counts, not generator rankings or creativity
measurements. Each family covers all targets and all sources, but specific
source-target combinations differ. Generator and neutralizer families are coupled
by cross-family assignment. Small populations, wording differences and the validity
boundary prevent causal attribution of the split. Collapse/keep distributions,
borderline counts and departure-locus patterns by generator are unmeasured.

| Source instrument | Generated | Both audits pass | Valid/Valid | Primary admitted |
|---|---:|---:|---:|---:|
| Chromatography | 3 | 3 | 0 | 0 |
| Provenance reconstruction | 2 | 1 | 2 | 1 |
| Dechallenge and rechallenge | 2 | 2 | 1 | 1 |
| Differential diagnosis | 2 | 2 | 0 | 0 |
| Serial monitoring | 2 | 2 | 1 | 1 |
| Step-response probing | 2 | 1 | 0 | 0 |
| Dendrochronological crossdating | 3 | 2 | 0 | 0 |
| Chain-of-custody verification | 2 | 1 | 1 | 1 |
| Luminol latent-trace detection | 2 | 1 | 0 | 0 |
| Analysis of Competing Hypotheses | 2 | 2 | 1 | 1 |
| Source corroboration | 2 | 2 | 2 | 2 |
| Seismic tomography | 2 | 1 | 0 | 0 |
| Delta debugging | 2 | 2 | 1 | 1 |
| Regression bisection | 2 | 1 | 0 | 0 |

The eight primary mappings cover seven source instruments. These counts identify
where upstream attrition occurred; they cannot identify instruments that produce
valid collapsed versus retained mappings. No source-selection policy was modified.

## Anti-collapse outcomes and research questions

The frozen gate, schemas, five departure loci and three statuses remain unchanged:
CLEAR_COLLAPSE rejects; SUFFICIENT_DEPARTURE and BORDERLINE_KEEP keep. No novelty
score or ranking was added. Coverage failed before anti-collapse packet preparation,
provider preflight or measurement. Consequently all following outcomes are
**unmeasured**, represented explicitly as null in the
[nonmeasurement record](../anti-collapse-natural-recovery-v0.1/review/nonmeasurement.json).

| Required question or finding | Result |
|---|---|
| Fraction of Valid/Valid natural mappings surviving anti-collapse | Unmeasured; 8/30 is not this fraction. |
| Status distributions by judge and keep/reject agreement | Unmeasured; there are zero anti-collapse observations, not a zero rejection rate. |
| Five-locus, materiality, native-reduction and formalization agreement | Unmeasured. |
| Every CLEAR_COLLAPSE case and dangerous-suppression review | No case received the status; no rejection exists to review. |
| Every BORDERLINE_KEEP case; natural occurrence of borderline status | No case received the status; natural frequency is unknown. |
| Every status disagreement and same-status mechanism disagreement | No anti-collapse pairs exist. Validity/audit disagreements are reported separately above. |
| Unusual-looking mappings rejected after neutralization | Unknown; validity/fidelity exclusions cannot stand in for gate rejection. |
| Obviously ordinary procedures retained; permissive-retention sample | Unknown; there are no retained gate decisions to sample. |
| Natural formalization cases and how the gate handled them | Not classified or measured. |
| Natural one-rule departures and whether modest departures were kept | Not classified or measured. |
| Action-centric behavior on natural outputs | Unknown; no departure-locus judgments exist. |
| Generator or source collapse/keep patterns | Unknown; only upstream admission patterns are available. |
| Faithful neutralization without verdict leakage | 23/30 pass both audits; seven excluded; no verdict wording detected. Directional bias in gate outcomes is unknown. |
| Removal of naturally generated native collapse | Not demonstrated. |
| Suppression of naturally unusual valid generations | Not measured. |
| Permissiveness enough for a downstream Chaos Mage filter | Not established. |

No claim from the synthetic pilot has been revalidated on natural outputs here.
There is neither a strong positive nor a strong negative result about the gate.
The observed result is insufficient coverage under the frozen admission protocol.

## Limitations, verification and next step

The principal limitation is the unmeasured gate. Further limitations include the
small purposive source-target set; authored baseline scope; lack of target evidence;
strict dual-family unconditional-validity admission; disagreement over execution
preconditions versus warrant conditions; fidelity exclusions on both failures and
uncertainties; possible undetected paraphrase loss; generator/neutralizer coupling;
unknown immutable serving snapshots; and interrupted collection with explicit
post-failure lexical corrections. The original checker defect and all exclusions
remain available for inspection rather than being hidden in a single success count.
The operator performed the post-freeze synthesis; this is not independent expert
adjudication of the validity or fidelity judgments.

[Metrics](../anti-collapse-natural-recovery-v0.1/metrics.json) recompute from frozen
outputs. The [read-only completion verifier](../anti-collapse-natural-recovery-v0.1/review/verify_completion.py)
independently checks admission and count denominators, the coverage stop, original
artifact hashes, fresh sessions, requested/returned model metadata, commands,
authorization ancestry, raw event/payload correspondence and absence of replacement
generation. All 263 historical/original-E tests and 22 recovery tests passed,
along with the historical public/private verifiers, recovery checks and diff checks.
The [historical verification](../anti-collapse-natural-recovery-v0.1/review/historical-verification.json),
[terminal verification](../anti-collapse-natural-recovery-v0.1/review/terminal-verification.json)
and [execution audit](../anti-collapse-natural-recovery-v0.1/review/execution-audit.json)
record commands, results and execution segments. Normal push and local/remote
SHA equality are verified after publication; no force-push is used.

**Recommended next step:** separately review the transfer-validity admission
boundary for prospective procedures before preregistering another natural-output
test. In particular, determine when a checked execution precondition is already
handled by a bounded procedure and when it leaves an unresolved transfer warrant,
using the preserved disagreements as diagnostic evidence. Address neutralization
scope loss as a separate issue. Do not interpret that recommendation as permission
to reclassify this cohort, relax its threshold, alter the frozen anti-collapse gate
or generate replacements. Optional generator-filter integration and diversity work
are not supported by an unmeasured gate. The recommended work was not executed;
Experiment E stops here.
