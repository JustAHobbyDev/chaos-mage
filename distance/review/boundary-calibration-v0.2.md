# Boundary calibration v0.2 — completed research report

2026-09-27. **Recommendation: revise the draft; retain the four classes as research
hypotheses, with no production promotion.** The experiment completed all 32 primary
and six supplementary judgments. No final labels were adjudicated or changed.

The Adjacent/Remote group meets the numerical side-agreement criterion (8/8), but
all sixteen judgments occupy the Native/Adjacent side. It therefore supplies
**insufficient evidence of boundary discrimination**. The Remote/Alien group meets
the numerical criterion (7/8) and exercises both sides, but its only side disagreement
is explained by displacement, not grounding. The intended grounding attribution
gets **0/1**, failing the strict-majority test. Some essential-counterpart explanations
are persuasive, but this is not a successful validation of both boundaries.

Exact final-class agreement is **11/16 (68.75%)**. The new controls resolve only the
original luminol literary disagreement, and it resolves under both v0.1 and v0.2.
There is no observed exact-class resolution attributable specifically to v0.2.

## What was tested

The exact full text is [CLASSIFIER-tested.md](../boundary-v0.2/CLASSIFIER-tested.md),
identical to the [experimental draft](../CLASSIFIER-v0.2-draft.md) at preparation.
It remains unchanged after measurement. Snapshotting establishes reproducible tested
text, not scientific validity. No post-run revised classifier text was installed.

- **Native:** The representation is substantially naturalized in the target.
  Removing source labels leaves ordinary target practice with little
  representational change.
- **Adjacent:** The transfer extends or reinterprets target concepts or procedures
  while leaving ordinary inquiry substantially intact. Unfamiliar entity roles
  alone do not establish epistemic reorganization.
- **Remote:** The transfer reorganizes inquiry through a substantively non-native
  operation, observable, or inferential rule, while its essential source roles have
  independently defensible target counterparts.
- **Alien:** The transfer produces strong epistemic reorganization and requires at
  least one essential counterpart constructed mainly to preserve the source
  structure, without independent target grounding.

Alien requires **both** strong reorganization and an essential independently
ungrounded counterpart. Low/moderate displacement with weak grounding remains an
explicit taxonomy tension, not automatically Alien.

The independent axes were:

- **Displacement:** change in ordinary expectations about representation,
  investigation, evidence and inference. Low = surface extension or familiar
  procedural variation; moderate = representational reinterpretation without
  reorganizing inquiry; high = epistemic reorganization.
- **Grounding:** independent target justification for transferred roles. Grounded =
  essential roles have defensible counterparts; partially-grounded = mixed or
  conditional support; weakly-grounded = an identified essential analogy-dependent
  construction; uncertain = available information cannot establish the judgment.

An essential role is one whose removal breaks the instrument's operational chain.
New measurements can be grounded; absent measurements, implementation difficulty,
unfamiliarity and low usefulness do not establish weak grounding. Source mechanism
and target question must be preserved. Naturalization primarily informs
Native/Adjacent and cannot independently decide Remote/Alien.

The original seven dimensions (entities, relations, processes, operations,
observables, inferences, failure_modes), their 0/native, 1/extension,
2/reinterpretation and 3/replacement definitions, and naturalization statuses
(native, partially-naturalized, non-native, uncertain) were unchanged. Axes and the
four boundary-evidence strings were analytical annotations, not added dimensions.
Strict structural validation accepted semantic inconsistencies for later review.

## Design, cases and independence

[Protocol](../boundary-v0.2/PROTOCOL.md),
[operator manifest](../boundary-v0.2/operator-manifest.json),
[execution order](../boundary-v0.2/execution-order.json) and
[configuration](../boundary-v0.2/execution-config.json) were fixed before calibration.
Case IDs were neutral. Boundary groups, contrast relationships, synthetic provenance
and control origins were excluded from classifier packets. Each packet supplied
only source identity, verbatim instrument fields, target and neutral case ID.
No expected classes, other judgments or review entered a measurement context.

A = OpenAI `gpt-6-astra`, high reasoning, Codex CLI `0.157.0`.
B = Anthropic `claude-fable-5-1[1m]`, high effort, Claude Code `2.1.282`.
Every judgment used a fresh empty temporary working directory and fresh session.
The schedule was sequential, within the cap of two concurrent processes, with a
900-second process timeout. Equal effort labels do not imply equal compute.

| ID | Group | Source → target / distinguishing evidence | Fixture origin |
| --- | --- | --- | --- |
| [001](../boundary-v0.2/cases/001.yaml) | A/R | Step-response → rollout monitoring | Exact CASE-008 source/target |
| [002](../boundary-v0.2/cases/002.yaml) | A/R | Step-response → museum interpretation; panel change, routes, pauses, interviews | Synthetic |
| [003](../boundary-v0.2/cases/003.yaml) | A/R | Luminol → literary analysis; final text and limited context | Exact CASE-009 source/target |
| [004](../boundary-v0.2/cases/004.yaml) | A/R | Luminol → same literary question plus dated drafts and correspondence | Synthetic enrichment |
| [005](../boundary-v0.2/cases/005.yaml) | A/R | Provenance reconstruction → identical enriched target from 004 | Synthetic source contrast |
| [006](../boundary-v0.2/cases/006.yaml) | A/R | Dechallenge/rechallenge → withholding interpretation; original/omitted/restored passages and blinded responses | Synthetic |
| [007](../boundary-v0.2/cases/007.yaml) | A/R | Delta debugging → identical reader-study target from 006 | Synthetic source contrast |
| [008](../boundary-v0.2/cases/008.yaml) | A/R | Crossdating → organizational histories; overlapping monthly reports and shared disruptions | Synthetic |
| [009](../boundary-v0.2/cases/009.yaml) | R/Al | Tomography → literary analysis; final text and limited context | Exact CASE-013 source/target |
| [010](../boundary-v0.2/cases/010.yaml) | R/Al | Tomography → coordination delays; identified requests, routes and successive timings | Synthetic |
| [011](../boundary-v0.2/cases/011.yaml) | R/Al | Tomography → same coordination question; unsequenced accounts and aggregates | Synthetic evidence contrast |
| [012](../boundary-v0.2/cases/012.yaml) | R/Al | Chromatography → idea decomposition; independently established circulation/retention/release workflow | Synthetic |
| [013](../boundary-v0.2/cases/013.yaml) | R/Al | Chromatography → same decomposition question; texts/discussion without that workflow | Synthetic evidence contrast |
| [014](../boundary-v0.2/cases/014.yaml) | R/Al | Luminol → strategic assumptions; prior decisions and repeatable scenario responses | Synthetic |
| [015](../boundary-v0.2/cases/015.yaml) | R/Al | Luminol → same persistence question; aspirations/scenarios without historical residues | Synthetic evidence contrast |
| [016](../boundary-v0.2/cases/016.yaml) | R/Al | Crossdating → present brand identity; current materials, explicitly not historical dating | Synthetic |

A/R denotes the Adjacent/Remote design group; R/Al denotes Remote/Alien. These are
operator design assignments, not expected labels. No contrast had to cross a boundary.
Close evidence pairs retain their question and surrounding text; 004/005 and 006/007
have identical targets. The six supplementary judgments use the entire original
v0.1 prompt/packet bytes (including CASE IDs) and unchanged v0.1 schema.

## Execution audit and preservation

Non-calibration structured-output probes preceded preparation. The initial Claude
probe failed because its subscription token had expired. The operator renewed the
login; fresh probes succeeded. Safe mode alone still listed built-in plugins, so
explicit exclusions were verified before freezing. See
[preflight notes](../boundary-v0.2/PREFLIGHT-NOTES.md) and
[preflight hashes and metadata](../boundary-v0.2/preflight.json).
The failed probe is retained and was never a calibration observation.

Preparation commit **214c0ce** succeeded before the first calibration launch. The
runner checked every prepared input against HEAD and enforced exclusive experiment
and run reservations. Calibration ran from **16:48:13 to 17:37:35 UTC**; all results
were frozen at **17:38:02 UTC**, before any result review. There were **38 unique
sessions, zero calibration failures, zero timeouts, zero harness retries and zero
protocol amendments**. All denominators remain fixed.

Codex ignored user config/rules and project instructions and disabled tools,
memories, plugins, apps, hooks and delegation. Claude used safe mode, empty settings
sources/MCP configuration, disabled built-in plugins/skills/memory/hooks/connectors,
no session persistence and no tools except its internal StructuredOutput formatter.
Existing subscription authentication stayed with the CLIs. Raw files remain private
under `.runtime/boundary-v0.2/`.

Runner-host instructions and structured-output machinery necessarily differ.
Equivalent classifier, case and schema content is not a claim of identical system
prompts. Codex events exposed **no returned model identifier**. Claude returned
`claude-fable-5-1` in runner init, assistant message and modelUsage metadata. These
returned fields are preserved with provenance; neither runner exposes a verified
immutable served snapshot, so that field remains null. Requested aliases are never
reported as verified backend snapshots. CLI versions were checked before execution.
The harness used Python 3.14.7, PyYAML 6.0.3 and jsonschema 4.23.0, matching the
existing dependency pins. High effort is explicitly requested; unexposed backend compute/configuration remains
unverifiable. Undisclosed server-side substitution cannot be ruled out by CLI logs.

There was **one visible internal formatting retry**, on `primary-006-B`: the first
StructuredOutput call contained unparseable JSON; Claude's formatter returned an
InputValidationError and requested valid JSON, and the second call succeeded. That
run had three turns; the other 18 Claude runs each had two turns and one formatter
call. No harness repair prompt was sent. No visible transport retries occurred in
calibration. Codex exposes no comparable formatting-retry event; zero observed does
not prove zero hidden retries. Raw events and the
[execution audit](../boundary-v0.2/review/execution-audit.json) preserve this difference.
The formatter's documented repair behavior is described in the
[Claude structured-output documentation](https://code.claude.com/docs/en/agent-sdk/structured-outputs);
Codex event/schema facilities are described in the
[OpenAI evaluation guide](https://developers.openai.com/blog/eval-skills).

[Preparation hashes](../boundary-v0.2/prepared.json) fix the tested inputs;
[result hashes and per-run audit metadata](../boundary-v0.2/results-freeze.json)
fix all results. Published judgment payloads are unchanged copies of validated
private responses. For Claude, that response is the lossless JSON serialization
of the final `structured_output` object; the complete original stream also remains
private. All **77 previously tracked v0.1 files** are covered by
[preservation hashes](../boundary-v0.2/preservation.json). All **240 private v0.1 run
files** were also checked against their original result manifest and remain unchanged.
All copied instrument field values match the accepted source records exactly.

## Outcomes and fixed metrics

Primary final classes and analytical axes follow; A/B order is constant. G = grounded,
P = partially-grounded, W = weakly-grounded. No judgment selected uncertain grounding.

| Case | A class | B class | Displacement A / B | Grounding A / B |
| --- | --- | --- | --- | --- |
| 001 | Native | Adjacent | low / low | G / G |
| 002 | Adjacent | Adjacent | moderate / moderate | P / P |
| 003 | Adjacent | Adjacent | low / low | G / G |
| 004 | Adjacent | Adjacent | low / low | G / G |
| 005 | Native | Native | low / low | G / G |
| 006 | Native | Adjacent | low / low | G / G |
| 007 | Adjacent | Adjacent | moderate / moderate | G / P |
| 008 | Native | Adjacent | low / low | G / G |
| 009 | Alien | Adjacent | high / moderate | W / W |
| 010 | Adjacent | Adjacent | low / moderate | G / P |
| 011 | Remote | Remote | high / high | P / P |
| 012 | Adjacent | Remote | low / high | G / P |
| 013 | Alien | Alien | high / high | W / W |
| 014 | Adjacent | Adjacent | low / low | G / G |
| 015 | Adjacent | Adjacent | low / low | P / P |
| 016 | Alien | Alien | high / high | W / W |

| Agreement | Primary (n=16 pairs) | A/R group (n=8) | R/Al group (n=8) | Supplementary (n=3) |
| --- | --- | --- | --- | --- |
| Final class | 11/16 (68.75%) | 5/8 (62.50%) | 6/8 (75.00%) | 1/3 (33.33%) |
| Naturalization | 10/16 (62.50%) | 5/8 (62.50%) | 5/8 (62.50%) | 1/3 (33.33%) |
| Displacement axis | 13/16 (81.25%) | 8/8 (100.00%) | 5/8 (62.50%) | Not in v0.1 schema |
| Grounding axis | 13/16 (81.25%) | 7/8 (87.50%) | 6/8 (75.00%) | Not in v0.1 schema |

Each dimension cell below is **exact agreements / denominator; mean absolute ordinal
disagreement**. These are descriptive dimension statistics, not distance scores.

| Dimension | Primary n=16 | A/R n=8 | R/Al n=8 | Supplementary n=3 |
| --- | --- | --- | --- | --- |
| entities | 10/16; 0.3750 | 4/8; 0.5000 | 6/8; 0.2500 | 2/3; 0.3333 |
| relations | 9/16; 0.4375 | 5/8; 0.3750 | 4/8; 0.5000 | 1/3; 0.6667 |
| processes | 6/16; 0.6875 | 4/8; 0.6250 | 2/8; 0.7500 | 1/3; 0.6667 |
| operations | 11/16; 0.3125 | 5/8; 0.3750 | 6/8; 0.2500 | 1/3; 0.6667 |
| observables | 9/16; 0.5000 | 5/8; 0.3750 | 4/8; 0.6250 | 2/3; 0.3333 |
| inferences | 3/16; 0.8750 | 2/8; 0.7500 | 1/8; 1.0000 | 1/3; 0.6667 |
| failure_modes | 9/16; 0.4375 | 6/8; 0.2500 | 3/8; 0.6250 | 2/3; 0.3333 |

Primary class distributions are A: Native 4, Adjacent 8, Remote 1, Alien 3;
B: Native 1, Adjacent 11, Remote 2, Alien 2. Supplementary distributions are
A: Native 1, Adjacent 1, Remote 0, Alien 1; B: Native 0, Adjacent 2, Remote 1, Alien 0.
Full precision, per-group distributions and confusion matrices are retained in
[metrics.json](../boundary-v0.2/metrics.json).

| Boundary | Fixed side mapping | Agreement | Both sides exercised? | Interpretation |
| --- | --- | --- | --- | --- |
| Adjacent/Remote | Native+Adjacent vs Remote+Alien | 8/8 (100%); ≥6/8 | No | Insufficient evidence of discrimination |
| Remote/Alien | Native+Adjacent+Remote vs Alien | 7/8 (87.5%); ≥6/8 | Yes | Numerical criterion met; intended grounding attribution fails |

A/R out-of-band outcomes are 001-A, 005-A/B, 006-A and 008-A, all Native (5/16
judgments). Every remaining judgment there is Adjacent. This is complete collapse
onto the lower side, not evidence that the Adjacent/Remote boundary is reliable.
A has four Native/four Adjacent; B has one Native/seven Adjacent in this group.
No side disagreements exist, so the displacement attribution test is **not applicable**.

R/Al out-of-band outcomes are 009-B, 010-A/B, 012-A, 014-A/B and 015-A/B, all Adjacent
(8/16 judgments). A has four Adjacent/one Remote/three Alien; B has four Adjacent/two
Remote/two Alien. The only side disagreement is **009, Alien/Adjacent**. Both judge
weak grounding; they disagree high versus moderate displacement. Thus grounding
explains **0/1** side disagreements, not a strict majority. Exact Adjacent/Remote
disagreement on 012 is hidden by this group's side mapping and remains explicitly
reported. Strong side agreement cannot stand in for exact-class agreement.

## Semantic review and shortcut audit

The [mechanical evidence inventory](../boundary-v0.2/review/inventory.json) records
all disagreements with original explanations. The
[case review](../boundary-v0.2/review/case-reviews.json) audits every class, axis,
dimension and naturalization disagreement, all six specified shortcuts for every
pair, and every new Remote/Alien judgment. Coverage is **19 pairs, 18 with a
disagreement, and 10 Remote/Alien judgments**. Case 002 alone agrees on all measured
fields. This is author-informed implementation-agent review, not independent human
ratings or ground truth. All uncertainties and original labels remain intact.

The six shortcuts were disciplinary distance, semantic distance, overweighted
operation distance, overweighted entity vocabulary, mapping difficulty treated as
distance, and usefulness treated as distance. None was established as the decisive
cause of an observed label. Four secondary/conditional concerns remain: vocabulary
emphasis in 001-B, a possible data-absence-to-Alien move in 011-B's uncertainty,
low detectability linked to Native in control-003-B, and apparently coherent motif
names standing in for path grounding in control-009-B. “Not observed” elsewhere is
a finite-review finding, not proof of absence.

The more consequential findings concern baseline choice, inference and fidelity:

- **001, 006 and 008:** Native/Adjacent disagreements persist with identical
  low/grounded axes. Formalization versus ordinary practice, and specialist versus
  broad target baselines, explain these better than a high-distance boundary.
  001-B additionally treats a holdout as available although none is supplied.
- **002 and 007:** both families call meaningful procedural and inferential additions
  Adjacent. They distinguish reinterpretation from reorganizing inquiry, but neither
  case supplies a positive Remote observation within the assigned boundary group.
  Museum cohort timing and reader-study outcome criteria remain conditional.
- **003/004/005:** adding literary documents leaves luminol Adjacent in both families;
  changing the source to provenance with the identical enriched target produces
  Native in both. This supports attention to the source mechanism, without forcing
  either contrast to cross its assigned boundary.
- **009:** both families independently name an unsupported path-through-medium role.
  A treats model inversion and residual-based warrant as high displacement; B treats
  the same change as moderate because the conclusion remains a strata map. B records
  the resulting moderate/weak taxonomy gap. Keeping the final question or conclusion
  type does not resolve whether the evidential warrant reorganizes inquiry.
- **010/011:** identified route measurements yield Adjacent/Adjacent; their absence
  yields Remote/Remote with partial grounding. Both Remote explanations specify a
  change to route-level measurements, residual evidence and inverse inference, and
  preserve real request/handoff counterparts. Yet the ordinary-practice baseline
  moves with evidence availability. It is unresolved how much of this contrast is
  ontological displacement versus additional investigative work. B's stationary,
  additive-delay assumptions are stronger than the supplied source requires.
- **012/013:** the established workflow yields Adjacent/Remote; its absence yields
  Alien/Alien. In 012-B the substantive change is retention-based warrant replacing
  semantic analysis, not a foreign operation alone. A regards this as an added
  behavioral distinction that cannot establish conceptual identity. In 013 both
  identify essential stable phase affinity lacking independent justification, going
  beyond mere absence of apparatus. A newly validated measurement could alter that
  assessment; the synthetic packet does not prove such grounding impossible.
- **014/015:** both remain Adjacent. A withholds temporal-persistence claims when
  historical evidence is missing. **015-B instead infers persistence from cross-probe
  consistency**, while acknowledging the mismatch. This is an observed target-question
  drift that class agreement conceals, not an automatic reason to choose Alien.
- **016:** both identify essential ungrounded temporal ordering and offsets. A explicitly
  says chronology does not answer present meaning. **B reinterprets chronological
  position as identity-component membership**, losing part of the source inference.
  Alien agreement diagnoses an attempted transfer's requirements; it does not establish
  a mechanism that answers the retained present-meaning question.

All new Remote judgments have an explicit non-native operation, observable or
inferential change: 011-A/B route-residual inversion, 012-B retention-based evidential
warrant, and control-009-B crossing-probe residual localization. The last still lacks
established path grounding and belongs to the old rubric. All six new Alien judgments
identify an essential unsupported counterpart: literary propagation (009-A and its
v0.1 control), stable fragment-phase affinity (013-A/B), or temporal ordering and
offsets (016-A/B). Their conditions and fidelity caveats are preserved individually
in the high-class review, including the 016-B source-inference drift.

## Matched controls

Original A/B below are **two same-model Codex judgments**, not the new cross-family
A/B design. New A/B consistently mean Codex/Claude. Exact equality alone counts as
resolved.

| Case / original | Original v0.1 A / B | New v0.1 A / B | New v0.2 A / B | Exact resolution |
| --- | --- | --- | --- | --- |
| 001 / CASE-008 | Adjacent / Native | Native / Adjacent | Native / Adjacent | Neither new condition |
| 003 / CASE-009 | Remote / Adjacent | Adjacent / Adjacent | Adjacent / Adjacent | Both new conditions |
| 009 / CASE-013 | Remote / Alien | Alien / Remote | Alien / Adjacent | Neither new condition |

001 remains Native/Adjacent under both new prompts. 003 reaches Adjacent/Adjacent
under both. 009 remains unequal: new A stays Alien while new B changes from Remote
under v0.1 to Adjacent under v0.2 and explicitly records the weak-grounding tension.
This does not resolve the disagreement. A single observation per model/condition,
changed family composition relative to the original run, runner differences and
possible sampling variation prevent causal attribution to prompt wording.

## Recommendation and remaining limits

| Class | Recommendation | Evidence and next research question |
| --- | --- | --- |
| Native | Retain provisionally | Ordinary-practice interpretation is useful, but 001/006/008 need a consistently scoped target baseline; model claims about practice are unverified. |
| Adjacent | Revise boundary guidance | The entire intended A/R group falls at or below it; 009-B uses it provisionally for moderate/weak tension. Specify how added versus replaced evidential warrant is assessed without using familiarity alone. |
| Remote | Revise boundary guidance | Grounded non-native inquiry is intelligible in 011 and 012-B, but input evidence changes the baseline and 012 splits sharply. Distinguish a new observation plan from a reorganization of inquiry using a fixed target-practice baseline. |
| Alien | Retain the conjunctive research definition, conditionally | Essential ungrounded roles are explicitly identifiable in several cases. Do not relax the high-displacement requirement to absorb weak-grounding tensions; mechanism and question fidelity still need stronger review. |

Do not abandon a class on these observations. The research concepts remain useful,
but the v0.2 boundary calibration is incomplete. The recommendations above are
**untested follow-up guidance**, not revised tested definitions or authorization for
another experiment. A later design should exercise both A/R sides, fix specialist
scope independently of available evidence, and test essential grounding without
allowing new apparatus absence or target-question drift to decide the result.

The sample is small, purposive and mostly synthetic. Provider judgements are not
practitioner evidence; neither independent human ratings nor repeated model samples
were collected. Most R/Al observations are outside its named classes. Some target
questions are only partly answerable by the supplied mechanism. Grounded/partial
distinctions often depend on unspecified measurements. The independent axes improve
visibility of these problems but do not settle them. No result supports population
prevalence estimates, equal-compute claims, numerical distance scores, retrieval
integration or production promotion.

## Verification and reproduction

The original v0.1 suite passes **6 tests**; the separate v0.2 suite passes **16 tests**.
They cover preservation and copied instruments, exact control packet/schema identity,
paired-target differences, strict schema and duplicate keys, missing/reused results,
input hash and commit gates, known agreement calculations and off-band labels,
primary/control separation, unavailable model metadata, fallback rejection, invalid
output, timeout preservation, stop-on-failure and internal formatting retries.
The completion verifier checks all published hashes and metrics, all review fields,
all Remote/Alien entries, and retry coverage; its private option also verifies both
versions' raw artifacts. The frozen harness and tested text were not edited after
preparation.

From the repository root, offline checks are:

```sh
python -m unittest discover -s distance -p 'test_harness.py'
python -m unittest discover -s distance/boundary-v0.2 -p 'test_*.py'
python distance/boundary-v0.2/harness.py verify
python distance/boundary-v0.2/review/verify_review.py
# When the private raw archive is available:
python distance/boundary-v0.2/review/verify_review.py --private
```

Execution/preparation/publication commands write exclusively and are deliberately
not rerunnable over the frozen experiment. The tested inputs, all 38 unchanged
judgments, metrics, audit metadata and review are committed as a completed research
snapshot. Work stops at this report.
