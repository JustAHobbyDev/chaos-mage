# Ontological transfer model v0.3

2026-09-27. **Conceptual refactor informed by v0.2; reliability untested.**
This is the active research model. Historical v0.1/v0.2 definitions, judgments,
reports and hashes remain records of those experiments, not outputs of this model.

```text
candidate source→target mapping
  → TRANSFER VALIDITY (gate)
  → ONTOLOGICAL DISPLACEMENT (relative to a fixed native baseline)
  → GROUNDING (independent target justification)
```

The unit of assessment is an explicit candidate mapping, not a source discipline
or instrument in isolation. Different mappings of one source/target pair can receive
different judgments. Validity is a prerequisite, not a distance dimension. The
sequence is an assessment workflow, not a causal dependency of grounding on
displacement. Never combine these judgments into a scalar, ordinal distance score,
weighted profile, creativity score, usefulness measure or production ranking.

## Why replace the four classes?

The [completed v0.2 report](review/boundary-calibration-v0.2.md) found that the
Adjacent/Remote group never exercised its upper side. The Remote/Alien group's
side disagreement concerned displacement despite agreement on weak grounding.
Moderate displacement with weak grounding had no clean label; some Alien cases
also lost the source mechanism or retained target question. Practitioner scope
and supplied evidence changed the assumed baseline.

Alien was experimentally useful in exposing a separate grounding variable. It is
no longer an active distance class. Remote→Alien is replaced by Remote combined
with Grounded, Partially-grounded, Weakly-grounded or Unknown. Adjacent and Native
can also combine with any grounding status where their separate definitions hold.
Historical Alien judgments remain untouched. This refactor supersedes the old
model for new work; it does not retroactively revise either experiment's findings.

## 1. Transfer validity

Ask: **Is this a faithful application of the source operational structure to the
retained target problem?** Use all five unchanged instrument fields:
`state`, `operation`, `signal`, `inference`, `limit`. Source materials and nouns can
change; the functional chain and its inferential limits cannot silently disappear.

### Mechanism fidelity

Does the mapping preserve the essential source operational chain?

- `preserved`: the distinctive state→operation→signal→inference chain survives,
  including relevant limits. Functional counterparts need not use source materials.
- `conditionally-preserved`: a specific unresolved target condition determines
  whether that chain is instantiated; no established contradiction replaces it.
- `not-preserved`: a material step or warrant is removed or substituted. Calling
  “look from many perspectives” tomography loses travel measurement and inversion.

Require a rationale naming the preserved chain or the precise gap. Do not add
source preconditions absent from the supplied instrument merely to reject a transfer.

### Target fidelity

Does the mapped inference address the question actually posed?

- `addressed`: it provides a justified answer or bounded contribution to that
  question, without pretending to answer more than the signal warrants.
- `conditional`: its contribution depends on an explicit unresolved bridge that
  could be established without changing the question.
- `not-addressed`: it answers another question or lacks a defensible relationship
  to the retained question. Merely sharing a topic is not enough.

Record any suggested or enacted reframe in `target_reframe`: `occurred`,
`original_question`, `reframed_question`, `relationship`. If none occurred, all
three text fields are null. If one occurred, all are nonempty and the original
question equals the retained target question. A reframe is not automatically
invalid, but its contribution to the original must be justified. A creative
alternative can be retained alongside an Invalid assessment. Assessing a new
question requires a separate candidate; never overwrite the original question.
Chronology of brand motifs does not by itself answer present brand meaning.

### Operational coherence

Does performing X produce observable Y that provides warrant concerning Z?

- `coherent`: operation, signal and inference form an intelligible target chain;
  the claim stays within what the signal could support.
- `conditional`: a named unresolved measurement or empirical relation must be
  established for the signal to support the inference.
- `incoherent`: the inference does not follow even under the mapping's stated
  assumptions, or depends solely on source imagery/circular definitions.

A possible missing measurement is not automatically incoherent. Conversely,
“if the analogy works” is not a substantive unresolved condition.

### Final gate

Derive the final status, rather than choosing an independent overall impression:

| Final status | Rule |
| --- | --- |
| Valid | All three criteria pass; no unresolved validity conditions. |
| Conditional | No criterion fails; at least one is conditional; list specific unresolved conditions and how they could be established. |
| Invalid | At least one criterion fails. Failure takes precedence over conditional criteria. |

Invalid ≠ uncreative and Invalid ≠ useless. Preserve inspiration if desired, but
stop formal displacement and grounding classification: both fields are **null**.
Do not give an invalid transfer Remote because it is unusual.

For Conditional transfers, downstream judgments may be withheld as null. Every
populated downstream judgment has `provisional: true` and is explicitly assessed
under the stated conditions. Valid full records populate both judgments with
`provisional: false`. This flag describes dependence on unresolved validity
conditions; it does **not** claim experimentally validated reliability.

## 2. Fix the target-native baseline

Before classifying displacement, specify:

```yaml
native_baseline:
  target_domain: nonempty target domain
  target_task: retained target question, verbatim
  reference_practitioner: concretely scoped role and specialty
  ordinary_methods: [methods expected without exposure to the source ontology]
  ordinary_evidence: [signals ordinarily sought or available in this practice]
  uncertainty: [limits on the claimed baseline]
```

Use, for example, “professional literary scholar interpreting textual organization
and formation, without a computational-stylometry specialty,” not “expert.” The
same task and practitioner baseline must remain fixed across evidence contrasts.
A particular packet's absent archive or instrument does not make that evidence
non-native. Baselines are authored hypotheses about practice, not verified
practitioner consensus. Record uncertainty rather than inventing support.
`target_domain` and `target_task` match the retained target, not the source or reframe.

## 3. Ontological displacement

Assuming validity sufficient to proceed, ask how the transferred structure changes
the target's ordinary representation and investigation.

- **Native:** substantially already naturalized in the specified baseline. Removing
  source terminology leaves ordinary target practice. Historical origins do not
  matter; differential diagnosis in software debugging can have this shape.
- **Adjacent:** meaningful extension or reinterpretation while ordinary inquiry
  remains substantially intact: new grouping, procedural variation or comparison,
  without substantive reorganization of evidence and inquiry.
- **Remote:** substantive epistemic displacement. At least one important change
  affects what the practitioner does, notices, treats as evidence, infers or
  investigates next. Examples include a non-native intervention, previously ignored
  features becoming evidence, unfamiliar relational decomposition or a new warrant.

Diagnostic: **Would this practitioner inspect, manipulate, compare or infer
something they probably would not reach for through ordinary practice?** If so,
Remote becomes plausible; explain the substantive change, not just an extra step.
Maximum strangeness is unnecessary. Different disciplines, exotic vocabulary,
difficulty, unfamiliarity and weak grounding do not establish Remote.

Describe exactly seven dimensions independently:

| Dimension | Meaning |
| --- | --- |
| entities | Meaningful kinds of objects. |
| relations | Meaningful relationships between them. |
| processes | Relevant changes or transformations. |
| operations | What the practitioner does. |
| observables | What counts as evidence. |
| inferences | Conclusions licensed by evidence. |
| failure_modes | Ways representation or inference misleads. |

Each has a rationale and integer level: **0 native**, already ordinary;
**1 extension**, accommodated without reorganizing the problem;
**2 reinterpretation**, treating target objects/relations as meaningfully different
kinds; **3 replacement**, substantial reorganization around a foreign representation.
No sum, average, weights, numerical thresholds or deterministic vector-to-class rule.
Explain the qualitative class relative to the fixed baseline.

## 4. Grounding

Ask whether essential mapped roles have independent target-domain justification.
A role is essential when removing it breaks the source operational chain. List all
such roles, including essential relations and warrants, not just convenient nouns.
For each record its source role, target counterpart, essential reason, independent
target basis (or explicitly absent/unknown basis), and grounding status.

- **Grounded:** all essential roles have independently defensible target counterparts.
  Removing source terminology leaves a target reason to distinguish and operationalize
  each role. Grounded does not mean an inference's conclusion is already proven.
- **Partially-grounded:** some roles are established while others rely on explicit
  assumptions, incomplete evidence or unvalidated measurements that can in principle
  be tested or established.
- **Weakly-grounded:** at least one essential counterpart exists mainly to retain
  the source structure: arbitrary constructions or analogy-dependent entities,
  relations or warrants. Identify that role explicitly.
- **Unknown:** information is insufficient to establish grounding. Prefer this over
  fabricated target facts; absence of a packet fact does not prove an arbitrary role.

Aggregate judgments remain reasoned assessments. Grounded requires every entry to
be Grounded; Weakly-grounded requires an identified Weakly-grounded entry. Explain
why incomplete support is Partially-grounded versus Unknown, rather than treating
these labels as a numeric scale.

Grounding and validity answer different questions. A stipulated speculative ontology
can support a coherent, bounded operational inference while lacking independent
justification: Valid + Remote + Weakly-grounded is permitted. If the operation's
ability to warrant that inference itself depends on an unresolved empirical bridge,
use Conditional. If no bridge could support the asserted inference as mapped, use
Invalid. Merely inventing a counterpart does not settle any of these alternatives.

## Interpretation modes, not rankings

| Tuple | Possible downstream interpretation |
| --- | --- |
| Valid + Native + Grounded | Ordinary expertise / baseline |
| Valid + Adjacent + Grounded | Nearby reframing |
| Valid + Remote + Grounded | Strong cross-domain transfer candidate |
| Valid + Remote + Partially-grounded | Speculative but target-supported candidate |
| Valid + Remote + Weakly-grounded | Ontology-generating / high-speculation candidate |
| Conditional + Remote + Unknown | Candidate requiring target investigation |
| Invalid | Optional inspiration, not faithful transfer |

These descriptions score neither usefulness nor creativity and implement no policy.

## Contracts, freeze and research boundary

[Full transfer schema](v0.3/transfer.schema.json),
[validity-only response schema](v0.3/validity.schema.json), and
[candidate packet schema](v0.3/candidate.schema.json) use strict JSON objects and
required fields. `target.evidence` separates supplied facts from ordinary practice.
Empty evidence/uncertainty lists are allowed; required explanations are nonblank.
Nullable fields remain present. Source provenance stays outside the five-field
instrument. The offline validator additionally checks identity relationships,
actual integer levels and duplicate keys; it never repairs inputs.

The schemas use Draft 2020-12 conditionals for gate invariants. They are local
canonical contracts, not a claim that every provider accepts every keyword. Future
runner preflight must verify any structural wire projection and retain identical
fields plus the full local validation; raw failed outputs must remain preserved.

Freeze this document, schemas and validator before retrospective authoring, recording
hashes and the preparation commit. Retrospective examples are analytical reconstructions
of frozen records, never new judge observations or agreement evidence. Contract changes
after that freeze require a dated amendment and new hashes before revised examples.

Next: transfer-validity reliability first; if adequate, baseline/displacement; if
adequate, grounding; only then consider research on creative retrieval. No new
calibration or provider preflight is authorized by this refactor.
