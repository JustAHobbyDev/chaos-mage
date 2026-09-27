# Experiment A — transfer-validity calibration v0.3

2026-09-27. **PREPARED / UNEXECUTED.** This protocol and its 24 authored cases are
preparation artifacts, not observations. No provider calls, preflight probes,
classifier judgments, reliability results or live runner are part of this handoff.

## Objective and unit of measurement

Can independent judges reliably distinguish faithful, conditional and invalid
source→target transfers using mechanism fidelity, target fidelity and operational
coherence? The unit is a **fixed explicit mapping**, not permission to invent a
mapping. This removes the transfer-construction variability observed in v0.1/v0.2.
No displacement, grounding, native-baseline reliability or retrieval outcome is
measured in this primary experiment.

## Cases and blinding

There are 24 synthetic packets, eight triplets, with obvious and borderline cases.
Accepted source instruments are copied verbatim at the field-value level. Target
facts and proposed operations are synthetic scenario stipulations, not observed
facts about real organizations. Every packet contains only case_id, source,
target (domain, question, evidence), and the five-field proposed mapping.

| Contrast group | What the triplet varies |
| --- | --- |
| Perspectives versus propagation | Measured route inversion, unresolved stability, generic viewpoints |
| Elimination mechanism | Tested bisection, unresolved transition conditions, arbitrary halving |
| Chronology and present meaning | Independent meaning bridge, unresolved bridge, chronology substituted for meaning |
| Detection versus event attribution | Bounded detection, unvalidated diagnostic, unsupported event proof |
| Missing measurement | Established timestamps, possible instrumentation, circular predicted “observations” |
| Partition and counterparts | Established workflow, speculative but investigable roles, manufactured categories |
| Reframe and persistence | Temporal corroboration, explicit conditional subquestion, contemporary consistency treated as history |
| Functional transfer and literalism | Software hypothesis discrimination, uncertain specificity, clinical labels without functional counterparts |

The operator manifest records design intentions, difficulty, exact changed fields,
source provenance, group membership and adversaries. Each triplet intentionally
includes a Valid, Conditional and Invalid candidate, but **intent is not ground
truth**. Judges need not reproduce that balance; never repair or replace cases to
obtain it. The contrast design is purposive, not a prevalence sample or a clean
factorial causal design: some contrasts alter more than one necessary premise.

Numeric IDs are assigned with the recorded fixed seed and carry no label or group
prefix. The fixed 48-entry execution order interleaves cases and families. Source
names remain visible; this is not a source-name masking study. Judges receive
neither this protocol, its table, the operator manifest, other cases, examples,
historical records nor expected labels. Packet generation uses an allowlist of
fields, not a blacklist of leakage words. Identical instruction/case bytes and
substantively identical response contracts go to both families.

## Planned measurement and separate launch requirements

- Family A: an OpenAI model; family B: an Anthropic model. Use materially different
  model families, not two contexts of one model. Exactly one fresh judgment per
  family per case gives **48 planned judgments / 24 planned pairs**.
- Before any future launch, obtain separate execution authorization and prepare a
  new execution configuration recording exact requested identifiers, reasoning
  settings, CLI versions and command lines. Run non-calibration schema/isolation
  probes only at that later authorized stage. Verify available capabilities then;
  historical aliases or flags are not evidence of current support.
- Keep the canonical contracts unchanged. If a provider requires a structural wire
  projection, document and freeze it, retaining exactly the same response fields
  and enumerations. Validate every returned payload with the canonical schema and
  local identity checks. If this cannot be done without changing substantive
  instructions/contracts, amend and recommit preparation before measurement.
- Successfully commit all case bytes, prompts, schemas, configuration, runner and
  manifests before launching. Check their hashes against that commit, including
  the frozen model. Record the exact prepared commit per run.
- Every judgment gets a fresh process, fresh session and empty working directory.
  Disable tools, browsing, retrieval, memory, project/user instructions, plugins,
  hooks, connectors and delegation. The runner must not expose this repository.
  Native structured-output formatting machinery may operate; audit its visible
  retries separately from operator retries. Never send a repair prompt.
- Retain existing provider authentication through the provider tooling without
  reading/copying credentials into artifacts. Host policies and formatter behavior
  may differ; identical substantive inputs do not imply identical system prompts
  or equal compute. Requested IDs are not verified served snapshots; record exposed
  returned identifiers with provenance and leave unavailable metadata null.
- Schedule sequentially in the frozen order, with a 900-second timeout per process
  and exclusive experiment/run reservations. Verify unique sessions and reject
  visible unexpected model fallback, prohibited tool activity or context leakage.
- Preserve raw request, event stream, response, stderr, configuration, timing,
  validation outcome and exposed retry metadata privately in a new runtime root.
  Publish only appropriate validated responses and audit metadata after freezing.
  Never overwrite previous runs or touch the historical runtime roots.
- On timeout, transport failure, schema failure, criterion/final-status contradiction,
  identity mismatch or isolation failure, preserve the attempt and stop scheduling.
  An amended protocol is required before continuation; never retry silently or
  substitute a cleaner answer. An Invalid **transfer judgment** is a legitimate
  outcome and is not a failed run. Incomplete data block a complete-study claim;
  planned denominators do not shrink.
- Freeze all original responses and audit metadata before reviewing their content.
  Structural or cross-field inconsistencies remain raw failures, not repaired data.
  Semantically questionable but contract-valid responses remain judgments for review.

This handoff implements only offline contracts, packet assembly and verification.
The future runner and its validated provider configuration belong to the separate
execution-preparation task; no live execution command is supplied here.

## Prespecified analysis and advancement decision

Only after an authorized future run and result freeze:

1. Report exact agreement on final validity and each of the three criteria, the
   three-by-three final-status confusion table and per-family status distributions.
   Report reframe-occurrence agreement separately; review question/relationship
   text qualitatively. There is no ordinal distance between validity statuses.
2. Report all 24 intended pairs and all failures/missing outputs. For an incomplete
   study, label any available-pair description explicitly as incomplete alongside
   the fixed planned denominator; do not claim the full reliability result.
3. Examine every contrast and every disagreement, including Conditional versus
   Invalid, with the original explanations. Also audit concordant judgments for
   shared mechanism loss, target drift, circular warrant, literalism, and unexplained
   collapse to one status. Do not assume a triplet should cross all three statuses.
4. Explain whether the judgments exercised all intended distinctions, whether
   unresolved conditions are concrete and investigable, and whether agreeing labels
   conceal different mappings or premises. Retain alternative interpretations.
5. Compare author intentions only as qualitative design diagnostics, never accuracy
   against ground truth. No adjudicated labels replace measured responses and no
   new agreement statistics are constructed from retrospective examples.

**Advancement uses documented evidence review**, as selected by the user, not an
arbitrary numerical threshold. The researcher must explain observed agreement,
status coverage, Conditional/Invalid discrimination, contrast performance, shared
errors, failures and limitations, and recommend revise/repeat or consider B.
Complete class collapse or failure to exercise Conditional/Invalid discrimination
prevents a claim that reliability is adequate. An inconclusive or incomplete study
requires revision/further evidence. No result automatically authorizes the next run.
Small purposive paired data do not establish population reliability or practitioner
truth, even with strong agreement; correlated priors and single draws remain limits.

## Research stop sequence

```text
A: transfer-validity reliability
  if adequate after documented review:
B: scoped native baseline + Native/Adjacent/Remote displacement
  if adequate after its own review:
C: grounding reliability
  then consider research on creative retrieval control
```

Do not preregister numerical success thresholds for B or C here. Each needs its own
cases, protocol, authorization and freeze. No retrieval integration, creativity or
usefulness scoring, dimension weights or combined distance score is authorized.

## Preparation verification

`python -B distance/v0.3/verify_preparation.py` verifies frozen definitions,
historical preservation, sources, strict packets, operator separation, all 48
planned entries, retrospective provenance and the preparation-only file inventory.
Unit tests exercise contract failures with synthetic fixtures; those fixtures are
not judge outputs. There must be no experimental results, metrics, run reservations
or provider logs under v0.3. A future experiment must explicitly supersede this
preparation-only state rather than bypass this handoff's absence checks.
