# Transfer-validity calibration v0.3 — completed Experiment A

2026-09-27, America/Chicago (collection 2026-09-28 UTC).
**All 48 judgments completed. Final-status agreement is 24/24, exercising all three
statuses. Recommendation: retain the gate as a promising research model, but refine
and extend validity calibration before declaring it adequate for Experiment B.**

Perfect final-label agreement on these purposive authored packets does not establish
independent reliability of the three criteria, consistent reframe metadata or
correctness of the judges' empirical advice. No original judgment was changed.
No displacement, grounding, creativity or retrieval experiment was executed.

## What was run

The [frozen protocol](../v0.3/PROTOCOL-transfer-validity-v0.3.md) asks whether fresh
independent contexts can distinguish Valid, Conditional and Invalid **fixed candidate
mappings**, using mechanism fidelity, target fidelity and operational coherence.
There are 24 synthetic cases in eight contrast triplets, each deliberately including
obvious and borderline examples. Judges received source identity, its unchanged
five-field instrument, target question/evidence and an explicit five-field mapping.
They could not construct or repair a different mapping.

The [execution supplement](../validity-v0.3/EXECUTION.md) records the user's subsequent
“run” authorization and explicitly supersedes the preparation-only stop. The old
`distance/v0.3/` snapshot remains byte-identical; execution artifacts live separately
in `distance/validity-v0.3/`. Its instructions, cases, order, operator manifest and
canonical schemas were not changed. The operator's design intentions and contrast
membership never entered judge contexts and are not treated as ground truth.

A requested OpenAI `gpt-6-astra`, high reasoning, through Codex CLI 0.157.0.
B requested Anthropic `claude-fable-5-1[1m]`, high effort, through Claude Code 2.1.282.
These are materially different requested families; equal effort labels are not equal
compute. Codex exposed no returned model identifier. Claude consistently returned
`claude-fable-5-1` with metadata provenance. Neither runner exposes a verified
immutable served snapshot; those fields remain null.

Every request used a fresh process/session and empty working directory. Tools,
retrieval, project/user customizations, plugins, memory, hooks and delegation were
disabled. Claude's native StructuredOutput formatter was the only allowed tool.
Substantive instructions and candidate bytes were identical between families.
Runner system instructions and internal formatting machinery necessarily differ.
The [preflight notes](../validity-v0.3/PREFLIGHT-NOTES.md) record successful artificial
formatting probes; they contained no calibration cases and are not observations.

Both providers received the same structural projection of the canonical validity
schema: only `$schema`, `$id` and cross-field `allOf` entries were removed. The
response fields, enums, required keys, null alternatives and strict object boundaries
were retained. Every captured response then passed the unchanged canonical contract,
including criterion-to-final-status consistency and original-question identity.
No repair prompts, normalization or replacement judgments were used.

## Collection and freeze audit

Execution preparation was committed as
**`8968b25f36eebad8841cb44ffa0e9bc49d221dae`** before any calibration launch. Every
launch checked prepared bytes and prompt hashes against the commit. The original
48-entry schedule ran sequentially with exclusive reservations and a 900-second
per-process timeout.

- First judgment started: **2026-09-28 00:35:34 UTC**.
- Last judgment finished: **2026-09-28 01:01:39 UTC**.
- All results frozen: **2026-09-28 01:01:51 UTC**, before content review.
- **48 distinct measurement sessions**, none reused from preflight.
- **Zero failed runs, timeouts, harness retries or execution amendments.**
- **Zero visible internal formatting or transport retries.** Codex lacks the same
  formatter-call visibility as Claude; hidden retries cannot be ruled out.

[Preparation hashes](../validity-v0.3/prepared.json),
[result hashes and reservations](../validity-v0.3/results-freeze.json), and the
[execution audit](../validity-v0.3/review/execution-audit.json) retain the evidence.
Published judgment files are unchanged copies of the retained validated payloads.
For Claude that payload is a lossless JSON serialization of its structured-output
object; the original stream is also retained privately. Prompts, raw events, stderr,
responses and validation records remain under ignored `.runtime/validity-v0.3/`.

## Preregistered outcomes

| Measure | Exact agreement | Rate |
| --- | --- | --- |
| Final validity | 24/24 | 100% |
| Mechanism fidelity | 22/24 | 91.67% |
| Target fidelity | 20/24 | 83.33% |
| Operational coherence | 24/24 | 100% |
| Reframe occurrence | 23/24 | 95.83% |

Each family returned **8 Valid, 8 Conditional and 8 Invalid** judgments. This is not
class collapse. The final-status confusion table (A rows, B columns) is:

| A \ B | Valid | Conditional | Invalid |
| --- | --- | --- | --- |
| Valid | 8 | 0 | 0 |
| Conditional | 0 | 8 | 0 |
| Invalid | 0 | 0 | 8 |

All final judgments align with the corresponding author design intentions, but those
intentions are not an independent reference standard. This is not an accuracy result.
Canonical full-precision summaries are in [metrics.json](../validity-v0.3/metrics.json).
No combined validity/distance score or ordinal error measure was calculated.

The table below lists all cases by substantive contrast. Both families returned the
same final status shown for each case; the column names describe observed outcomes.

| Contrast | Valid | Conditional | Invalid |
| --- | --- | --- | --- |
| Measured propagation versus perspectives | 019: path inversion | 005: workload comparability | 003: interview themes |
| Evidence-driven elimination | 012: tested bisection | 015: repeatability/transition unknown | 011: untested halving |
| Chronology and present meaning | 021: independent bridge supplied | 007: bridge untested | 023: chronology substitutes for meaning |
| Detection versus event attribution | 010: bounded matches | 018: detector unvalidated | 022: copying/author/event proof |
| Missing measurements | 001: checked timings/model | 016: possible instrumentation | 009: model compared with itself |
| Partition and counterparts | 014: established workflow | 017: speculative but investigable roles | 006: assigned categories as proof |
| Reframing and persistence | 024: bounded dated recurrence | 002: explicit subquestion/bridge | 004: present consistency as past persistence |
| Function versus source literalism | 020: software diagnosis | 013: signature specificity unknown | 008: clinical-label matching |

All unchanged responses are in [judgments/](../validity-v0.3/judgments/). The
[mechanical inventory](../validity-v0.3/review/inventory.json) links every case,
contrast, original response, author intention and categorical disagreement.

## Criterion disagreements and metadata tensions

There are no final-status disagreements, but six pairs disagree on a criterion or
reframe occurrence. No disagreement was adjudicated or fed back to a judge.

| Case | Difference | Interpretation |
| --- | --- | --- |
| 005 | Target A conditional / B addressed | Both accept the proposed localization question; A propagates uncertain workload comparability into target fidelity, B treats the intended bounded answer as addressed. |
| 015 | Target A conditional / B addressed | Same divergence for bisection: presently warranted first-boundary localization versus the relevance of the proposed procedure. |
| 007 | Mechanism A preserved / B conditionally-preserved | Both condition the meaning bridge; B also requires fuller definition and anchoring of the crossdated series. |
| 018 | Mechanism A conditionally-preserved / B preserved; target A conditional / B addressed | A propagates unvalidated detector performance across criteria; B places it in operational coherence alone. |
| 013 | Target A addressed / B conditional | A accepts the bounded present conclusion that alternatives remain plausible; B conditions a fuller narrowing answer. This reverses the family direction in 005/015/018. |
| 004 | Reframe A false / B true | Both reject present consistency as historical persistence; B encodes the implicit change of answered question, A does not. |

A criterion can refer either to the structure of a proposed answer or to its current
empirical warrant. The instructions do not settle that allocation consistently.
Final Conditional agreement conceals this difference, and the reversal on 013 means
it is not simply one family being uniformly stricter.

Reframe occurrence agreement also overstates semantic consistency. In 003-B and
011-B the explanation explicitly says the operation answers a different question
(departmental beliefs or newest revision), while both occurrence flags are false.
006-B likewise describes a different, stronger question but records no reframe.
In contrast, both families encode the implicit label-selection reframe in 008, and
only B encodes the implicit persistence substitution in 004. These are observed
narrative/flag tensions, not corrected classifications. Future guidance should
clarify enacted question substitution versus an unsupported answer to the same
question. The explicit subquestion in 002 and chronology substitution in 023 are
encoded by both families without silently changing the retained assessment target.

## Review of concordant cases and conditions

[Case reviews](../validity-v0.3/review/case-reviews.json) cover every pair and all
eight contrasts, with explicit audits for generic metaphor, mechanism loss, target
drift, unsupported inference, missing measurements, invented counterparts, reframing
and literalism. This is implementation-agent author-informed review, not independent
human evidence or an accuracy oracle.

The principal positive findings are bounded:

- Missing clocks/logging in 016 and an unvalidated detector in 018 remain Conditional,
  while model-to-itself residuals in 009 and arbitrary release categories in 006 are
  Invalid. The judges distinguish missing evidence from an operation that manufactures
  its own support.
- Proposed fragment persistence and phase affinity in 017 do not automatically become
  Invalid. Both name investigable conditions and retain the source's bounded behavioral
  inference, while noting possible circular individuation.
- Bounded feature detection in 010 is separated from historical proof in 022. Dated
  evidence in 024 supports recurrence, with limits on uninterrupted persistence or cause.
- Functional diagnosis in software is accepted in 020; merely importing clinical
  vocabulary in 008 is rejected for mechanism loss, not foreign materials.
- Chronology contributes to meaning in 021 only through a separately stipulated
  independent bridge. Its mere availability does not rescue the unused bridge in 023.

Important limitations remain visible even where labels agree:

1. **Condition advice is not experimentally verified.** In 015-B, sparse intermediate
   sampling or checking neighbors after bisection cannot alone rule out an earlier
   disappear/reappear transition elsewhere. In 018-B, control texts lacking draft
   ancestry may still contain the target features; a feature detector needs independent
   feature truth, not ancestry alone, to validate specificity without changing the task.
2. **Extra assumptions can enter explanations.** B invokes additivity and stationarity
   in tomography cases. Additivity is explicitly supplied in 001, but only contribution
   to total delay is supplied in 019; neither linearity nor a single static model is a
   universal requirement of the abstract source. In 016-B, entry/exit logging is read as
   per-handoff logging, a granularity the packet does not establish. These are explanatory
   overstatements or candidate modeling choices, not grounds for rewriting verdicts.
3. **One authored packet has carryover ambiguity.** In 007 the operation still refers
   to an existing audience-study bridge while the evidence/inference say it is untested
   and proposed. B notices this and follows the latter fields; A does not explicitly
   address it. The packet remains frozen unchanged. Agreement does not remove the
   ambiguity or establish a general information-precedence rule.
4. **Bounded contribution needs a stable definition.** Recurrence is narrower than
   continuous persistence; current audience associations are narrower than all present
   meaning; retaining nondiscriminated hypotheses can already answer part of a diagnostic
   question. The target-fidelity splits show that this distinction is not settled.
5. **All final labels also follow operational coherence in this sample.** Every coherent
   response is Valid, every conditional coherence response Conditional and every incoherent
   response Invalid. Thus this study does not isolate a coherent operation that fails only
   source fidelity, or a coherent faithful operation that answers only the wrong target.
   Final agreement cannot demonstrate the independent contribution of each gate criterion.

## Evidence-review decision and next research step

The pilot supplies strong evidence of final-status reproducibility **on these fixed,
purposive packets**: both families use all three statuses, distinguish Conditional
from Invalid, and explain major mechanism and inference defects. There were no
missing observations or execution failures. This is a substantially clearer result
than a boundary test that collapses onto one side.

Nevertheless, the full prerequisite is not yet established strongly enough to
advance automatically to Experiment B. Mechanism/target attribution and reframe
metadata remain inconsistent; coherent-but-unfaithful and coherent-but-wrong-question
controls are absent; condition-resolution advice sometimes overreaches; and one
packet contains an authored contradiction. The synthetic facts are unusually explicit,
with conditionality and failure often stated clearly in the candidate. No wording
ablation tests whether surface conditional phrases help drive labels. A single draw
per family/case cannot establish within-family repeatability or population reliability.

**Recommendation: refine and extend Experiment A before declaring adequacy for B.**
A later protocol should clarify criterion attribution and reframe occurrence, remove
carryover ambiguity in newly versioned packets, add the fidelity-only controls, and
include less overtly signaled borderline cases. Existing packets, tested instructions
and judgments must remain frozen; any revision is new, untested guidance until measured.
Do not derive a post hoc numerical success threshold from this run.

No new follow-up protocol or classifier revision was installed during this review.
No additional judges, experiment B/C, grounding/displacement reliability measurement,
retrieval integration or production ranking were run. Work stops at this report.

## Verification and reproduction

All **78 tests** pass: 6 original distance tests, 16 boundary-v0.2 tests, 8 retrieval
tests, 33 v0.3 contract/preparation tests and 15 execution-runner tests. They include
wire/canonical separation, packet identity, isolation commands, environment filtering,
exclusive writes, known nominal confusion arithmetic, session coverage, stop/no-retry,
timeout preservation, fallback/tool rejection, formatter retry auditing, retention of
failed payloads and the actual preparation commit check.

The completion verifier recomputes all summaries from unchanged responses, checks
all 24 case reviews/eight contrasts and categorical disagreements, binds the review
to the result freeze, and verifies sequential execution after the preparation commit.
Its private option checks all raw execution hashes. Existing v0.1/v0.2 public and
private archives and the entire v0.3 preparation snapshot remain unchanged.

Offline verification, without provider calls:

```sh
python -B -m unittest discover -s distance -p 'test_harness.py'
python -B -m unittest discover -s distance/boundary-v0.2 -p 'test_*.py'
python -B -m unittest discover -s scripts -p 'test_*.py'
python -B -m unittest discover -s distance/v0.3/tests -p 'test_*.py'
python -B -m unittest discover -s distance/validity-v0.3 -p 'test_*.py'
python -B distance/v0.3/verify_preparation.py
python -B distance/validity-v0.3/runner.py verify-results
python -B distance/validity-v0.3/review/review_tools.py verify
# When private raw artifacts are available:
python -B distance/validity-v0.3/review/review_tools.py verify --private
python -B distance/boundary-v0.2/review/verify_review.py --private
```

The run, freeze, publish and analyze commands write exclusively and are not rerunnable
over this completed snapshot. Verification reads the existing artifacts; it does not
collect new observations or overwrite the analysis.
