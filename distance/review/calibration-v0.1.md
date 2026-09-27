# Ontological-distance calibration v0.1

Date: 2026-09-27. Status: complete; frozen research results, no downstream use.

The distinction is useful for describing these transfers, but this experiment does
**not yet establish enough boundary stability for automated operational use**.
Independent contexts agree on 17 of 20 final classes (85%); all disagreements are
one step. The Adjacent–Remote distinction has an interpretable inferential basis,
while Remote–Alien depends on an unsettled standard for grounded counterparts.
Neither observation supplies a numerical decision rule.

## Evidence and execution

- 20 purposive source→target cases, 11 accepted instruments, 15 target domains,
  and 40 valid initial judgments. No classifier failures, output repairs, selective
  reruns, or exclusions. Source instrument fields are unchanged from the corpus.
- 15/20 cases belong to six repeated-instrument groups: differential diagnosis,
  bisection, luminol, crossdating, chromatography, and seismic tomography.
  Software regression debugging has four instruments with byte-identical target
  content; literary/textual analysis has three. Early progress commentary's
  estimate of 17 source-contrast cases was incorrect; the verified count is 15.
- Requested model: `gpt-6-astra`; reasoning effort: `high`; CLI: `0.157.0`.
  A/B are same-model replicates, not separate model families. Temperature, seed,
  and service tier were not set by the runner. A served backend snapshot is not
  exposed; do not claim a pinned model revision or cross-time reproducibility.
- Forty fresh ephemeral processes and forty distinct thread IDs. No resume/fork,
  shared conversation, reference label, other case, or other output in prompts.
  Every A/B prompt hash matches. Fresh empty working directories, user-config
  exclusion, project-instruction exclusion, disabled capabilities, and event audits
  supplied isolation. All event streams contain no tool items. Host system
  instructions and shared model priors remain, so this is context independence,
  not independent sources of scientific evidence.
- Inputs hash-frozen before execution in [freeze-v0.1.json](../freeze-v0.1.json).
  Preparation commit: `4a0be79`. The first process started 11 seconds before that
  Git commit because staging initially hit read-only metadata. No response had
  arrived before commit, and all input hashes were already fixed. See the
  [execution note](execution-notes-v0.1.md); this is a recorded sequencing deviation.
- All 40 initial responses were frozen at **2026-09-27 12:08:05 UTC** in
  [results-freeze-v0.1.json](../results-freeze-v0.1.json), before creating reference
  labels. [Published judgments](../judgments/) are byte-identical response copies.
  Raw prompts, events, stderr, reservations, and validation records remain under
  ignored `.runtime/distance-v0.1/`; their hashes are retained in the result freeze.

The [protocol](../PROTOCOL-v0.1.md), [classifier](../CLASSIFIER-v0.1.md), and
[configuration](../execution-config.json) were not altered after the input freeze.

## Coverage and unadjudicated classes

The reference column is a separate, post-freeze expectation, **not ground truth**.
Cases 001–016 retain the handoff's tentative groups. Cases 017–020 and all confidence
statements/rationales were synthesized by the implementation agent after outputs
were available. No new independent human ratings were collected; do not interpret
reference agreement as measured accuracy. See [reference labels](reference-labels-v0.1.yaml).

| Case | Instrument → target | A | B | Reference |
| --- | --- | --- | --- | --- |
| CASE-001 | Differential diagnosis → Software regression debugging | Native | Native | Native |
| CASE-002 | Source corroboration → Investigative journalism | Native | Native | Native |
| CASE-003 | Regression bisection → Software regression debugging | Native | Native | Native |
| CASE-004 | Serial monitoring → Operations monitoring | Native | Native | Native |
| CASE-005 | Regression bisection → Project-history failure localization | Adjacent | Adjacent | Adjacent |
| CASE-006 | Dechallenge and rechallenge → Organizational process troubleshooting | Native | Native | Adjacent |
| CASE-007 | Chain-of-custody verification → Data lineage and document workflow | Native | Native | Adjacent |
| CASE-008 | Step-response probing → Product rollout monitoring | Adjacent | Native | Adjacent |
| CASE-009 | Luminol latent-trace detection → Literary and textual analysis | Remote | Adjacent | Remote |
| CASE-010 | Dendrochronological crossdating → Fragmented organizational histories | Adjacent | Adjacent | Remote |
| CASE-011 | Chromatography → Idea decomposition | Remote | Remote | Remote |
| CASE-012 | Seismic tomography → Organizational hidden-structure inference | Remote | Remote | Remote |
| CASE-013 | Seismic tomography → Literary and textual analysis | Remote | Alien | Alien |
| CASE-014 | Chromatography → Interpersonal conflict | Remote | Remote | Alien |
| CASE-015 | Dendrochronological crossdating → Brand identity | Alien | Alien | Alien |
| CASE-016 | Luminol latent-trace detection → Abstract strategic planning | Remote | Remote | Alien |
| CASE-017 | Differential diagnosis → Clinical diagnostic reasoning | Native | Native | Native |
| CASE-018 | Differential diagnosis → Literary and textual analysis | Native | Native | Adjacent |
| CASE-019 | Luminol latent-trace detection → Software regression debugging | Native | Native | Adjacent |
| CASE-020 | Dendrochronological crossdating → Software regression debugging | Adjacent | Adjacent | Adjacent |

## Agreement metrics

Computed by `python distance/harness.py analyze`; canonical values are in
[metrics-v0.1.json](metrics-v0.1.json). Denominator: all 20 pairs.

| Final-class measure | Count | Rate |
| --- | --- | --- |
| Exact agreement | 17/20 | 85% |
| Exactly one-step disagreement | 3/20 | 15% |
| Agreement within one step, including exact | 20/20 | 100% |
| Disagreement larger than one step | 0/20 | 0% |
| Exact naturalization agreement | 18/20 | 90% |

| Dimension | Exact agreement | Mean absolute 0–3 disagreement |
| --- | --- | --- |
| entities | 18/20 (90%) | 0.10 |
| relations | 17/20 (85%) | 0.15 |
| processes | 16/20 (80%) | 0.20 |
| operations | 18/20 (90%) | 0.10 |
| observables | 19/20 (95%) | 0.05 |
| inferences | 18/20 (90%) | 0.15 |
| failure_modes | 19/20 (95%) | 0.05 |

Across 140 dimension comparisons, 125 agree exactly (89.3%). This is an agreement
summary, not a distance score. Processes disagree most often; inferences include
the only two-level difference. These descriptive statistics assign no weights.

Confusion matrix: rows are A, columns are B.

| A \ B | Native | Adjacent | Remote | Alien |
| --- | --- | --- | --- | --- |
| Native | 9 | 0 | 0 | 0 |
| Adjacent | 1 | 3 | 0 | 0 |
| Remote | 0 | 1 | 4 | 1 |
| Alien | 0 | 0 | 0 | 1 |

There is no most frequent class boundary: Native↔Adjacent, Adjacent↔Remote, and
Remote↔Alien each occur once. Eight cases have at least one class, dimension, or
naturalization mismatch: 006, 008, 009, 010, 013, 015, 016, and 020. Every such case
is preserved and categorized in [failure-log-v0.1.yaml](failure-log-v0.1.yaml).
Categories identify issues to inspect; they are not verified error counts.

## Adjacent versus Remote

**Qualitatively distinguishable, not yet shown stable enough to operationalize.**
CASE-009, luminol→literary analysis, is the only direct boundary disagreement:
A=Remote, B=Adjacent. A treats passages as event residues and reorganizes the
inference from probe response to historical attribution. B regards detecting a
feature without proving its cause as ordinary competent textual reasoning.

| Differing dimension | A | B | Absolute difference |
| --- | --- | --- | --- |
| entities | 2 | 1 | 1 |
| relations | 2 | 1 | 1 |
| processes | 2 | 1 | 1 |
| inferences | 2 | 0 | 2 |

Operations and observables are both 1 in both runs; failure_modes is also 1.
Naturalization is partially-naturalized in both. Thus **inferences has the largest
observed disagreement**, with entities, relations, and processes also involved.
It would be incorrect to attribute this split to operational novelty alone or to
a changing naturalization status. This is association in one pair, not causal
attribution or evidence for numerical weighting.

The agreed Remote cases 011 (chromatography→ideas) and 012 (tomography→organization)
preserve specific partition/inversion mechanisms and reinterpret their evidence
and conclusions. In contrast, agreed Adjacent cases 005, 010, and 020 change how
investigators search or align evidence while retaining recognizable chronology
and localization reasoning. CASE-010's 0-versus-1 inference disagreement also
shows that an added evidential route need not change the kind of conclusion.

The hypothesis receives **qualified support**: changed evidential roles and
inferential warrants are informative; merely doing an additional operation or
noticing an additional signal is insufficient. CASE-016 remains Remote in both
runs despite operation levels of 1 and 2. The data do not establish that the
operations/observables/inferences group dominates other dimensions. The prompt
explicitly asks models to discuss this hypothesis, so their verbal endorsements
are not independent validation of it.

## Remote versus Alien

**A plausible distinction, with weaker operational evidence than Adjacent–Remote.**
CASE-013, tomography→literary analysis, is A=Remote, B=Alien. The level differences
are relations, processes, and operations, each 2 versus 3. Entities, observables,
and inferences are 2 in both runs; failure_modes is 1; naturalization is non-native
in both. No differing entity labels or naturalization status explains this split.

A accepts recurring motifs and measurable feature transformations as provisional
path counterparts. B says they do not establish propagation through intervening
regions and requires constructing a medium, crossing paths, and a propagation law.
**Relations, processes, and operations are equally implicated in the observed
boundary difference.** The unresolved criterion is when recognizable anchors
suffice to make a constructed mechanism coherent rather than substantially
replacement-based.

Both classify chromatography→conflict as Remote, even while explicitly constructing
two phases and retention procedures. Both classify crossdating→brand identity as
Alien. That is the only agreed Alien case, and it introduces chronology into a
present-meaning question. Task substitution and missing source preconditions may
therefore contribute to its distance judgment. Both outputs acknowledge this gap;
no claim of an established error or automatic reclassification follows.

Only two cases receive Alien from either classifier. A single agreement plus one
boundary split is insufficient evidence of a stable high-distance category. Do
not force the handoff's other candidate Alien examples into Alien to improve balance.

## Naturalization and reference tensions

The two status mismatches are CASE-006 (native versus partially-naturalized) and
CASE-008 (partially-naturalized versus native). Both concern how much of a complete
procedure is ordinary, rather than its historical origin. CASE-006 has identical
vectors and identical Native classes despite different naturalization statuses;
there is no deterministic status-to-class override. CASE-008 changes both status
and final class. This supports preserving the explicit judgment and rationale,
while leaving its application qualitative.

No run used status `uncertain`; uncertainty instead appears in rationale and
uncertainty lists, especially around specialty practices. This may conceal more
naturalization uncertainty than the 90% categorical agreement suggests. The
experiment supplies no independent observations of current practitioner behavior.
A target packet's ability to perform an operation (notably 006 and 008) does not
prove that practitioners ordinarily reach for it.

Both models differ from the handoff's tentative expectations on 006, 007, 010,
014, and 016. Inspecting them gives different reasons: familiar reversible trials,
native provenance auditing, alignment as an archival extension, and conditionally
coherent constructed transfers for conflict and strategic assumptions. Agreement
here is evidence to inspect the reference expectation and the shared model
assumptions, not proof that either is correct. Post-freeze agent expectations for
018 and 019 also differ from both models and have even weaker evidential standing.

## Confounds and classifier failure review

No explicit disciplinary-distance shortcut or vocabulary-only high class was found.
Foreign-source diagnosis→software and corroboration→journalism are Native in both
runs. With the same target, software judgments range from Native (diagnosis,
bisection, luminol) to Adjacent (crossdating); literary judgments range from Native
(diagnosis), through Adjacent/Remote (luminol), to Remote/Alien (tomography). With
the same source, crossdating ranges from Adjacent (history and software) to Alien
(brand), and luminol ranges from Native (software) to higher classes elsewhere.
These contrasts argue against a fixed disciplinary remoteness per instrument.

There is nevertheless **no blinded naming/vocabulary ablation**, and all runs
share a model family. No observed shortcut does not prove absence of semantic or
disciplinary influence. No usefulness-based classification or summed numeric
class threshold appears in the audited judgments.

The stronger observed concern is freedom to construct the transfer:

- In 009 and 013, different assumptions about ordinary practice or grounded
  counterparts change the class. This experiment mixes transfer construction
  variability with classification variability.
- In 011 and 014, both models describe retention/release procedures whose signals
  may reflect imposed rules. Same-model agreement does not validate those
  correspondences or establish that components persist through the operation.
- In 015, preserving chronology changes the stated target question. This may
  confound displacement with a missing prerequisite or task mismatch.
- In 016, both posit residues of prior belief formation despite no specified past
  event. They explicitly mark that premise uncertain, but their agreement may
  depend on relaxing the source state or inventing target history.
- In 020, A aligns incident logs; B aligns records to revision-indexed bundles.
  Both are Adjacent despite different constructed transfers and target ambiguities.
  Agreement in final class therefore does not guarantee agreement in representation.

The review log distinguishes observed disagreements from possible shared confounds.
No disagreement was resolved, merged, or fed back to a classifier.

## Verification

Six harness tests pass, covering known agreement arithmetic, same-vector/different-
class preservation, invalid output rejection, duplicate keys, fixture provenance
and contrast coverage, and empty denominators. A separate complete-data audit
verified all 40 raw artifact hash sets, distinct thread IDs, matching configuration
and prompt content, and forty agent-message items with no tool items. Recomputed
metrics exactly match the checked-in JSON; the review covers every disagreement,
and reference-label creation postdates the automated freeze. Git whitespace checks
pass. No existing extraction or retrieval artifact was modified.

## Proposed v0.2 changes — not part of frozen v0.1

1. Obtain target-native profiles and practitioner examples independently of the
   source. Specify the practitioner population and specialty; distinguish packet
   capabilities from demonstrated ordinary practice.
2. Compare free transfer construction with a condition in which both classifiers
   receive the same explicitly described transfer. Audit whether source-state,
   operation, signal, inference, and limits survive, and whether the target
   question changes. Treat missing counterparts as uncertainty, not automatic Alien.
3. Add focused contrasts around inference 0↔2 and reinterpretation↔replacement,
   especially grounded propagation, persistent components, and temporal increments.
   Add plausible Alien cases that preserve the target question.
4. Collect independent human judgments after a fresh automated freeze, and replicate
   across model families. Add a source-name masking/paraphrase condition to test
   disciplinary and semantic contamination; retain the present visible-name run.
5. Clarify when to use naturalization `uncertain` and require explicit evidence
   for conventionality without turning naturalization into a deterministic gate.

Do not infer weights or class thresholds from these 20 cases. No threshold is
proposed here. The next research decision should use targeted boundary evidence;
this prototype has stopped at the calibration report and performs no catalogue
filtering, retrieval, mapping optimization, or downstream scoring.
