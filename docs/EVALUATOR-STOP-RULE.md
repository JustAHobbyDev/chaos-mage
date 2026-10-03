# Evaluator-work stop rule

## Purpose and frozen governing principle

Chaos Mage exists to:

> **Generate genuinely unusual cross-domain transfers, preserve foreign operational or ontological structure when it creates a material new way of reasoning or acting on the target, and avoid discarding useful generations merely because they contain local defects.**

Evaluator work serves that purpose. Fault-localized warrant handling, productive
remainder viability, inquiry constraints, natural-language provenance,
claim-contract routing, and compound obligations are supporting machinery, not
independent project goals.

> **Evaluator work is justified only when it has a concrete, plausible path to reducing false rejection of materially valuable transfers, false retention of transfers whose distinctive source-derived contribution has failed, or measurement ambiguity that prevents distinguishing those outcomes. Evaluator work that primarily improves annotation cleanliness, schema elegance, citation precision, bookkeeping, or evaluator compliance without changing that decision boundary must stop or be deferred.**

This is a human-readable decision rule. Do not build scripts, validators, schemas,
CI jobs, or an experimental harness to enforce or evaluate this policy.

## Admission outcomes

These definitions preserve the existing [natural admission rule](../distance/natural-admission-v0.1/ARTIFACT.md)
and [remainder criteria](../distance/natural-admission-v0.1/REMAINDER.md); they do not
relabel historical results or introduce a new scoring layer.

A **definite viable remainder** is a surviving contribution that is warranted,
source-derived, target-relevant, productive, and material. All five must be
established. Preserve the contribution's scope and conditions; do not repair it
with deleted premises or invented inferences. A potentially decisive unresolved
candidate has no failed viability dimension and at least one genuinely uncertain
dimension.

| Outcome | Admission meaning |
| --- | --- |
| `KEEP_WITH_WARRANT_FLAGS` | Retain: essentially the same material, distinctive, source-derived transfer survives. Disclose any local, conditional, or uncertain warrant flags. This also covers an artifact with no local defect; the existing vocabulary has no separate unqualified `KEEP`. |
| `KEEP_WITH_REDUCED_SCOPE` | Retain at a narrower stated scope: a meaningful branch or scope was lost, but a definite viable contribution survives. |
| `CORE_INVALID` | Do not admit as a surviving transfer: no definite viable remainder remains and no potentially decisive viability issue is unresolved. Explain the loss of the distinctive source-derived contribution. |
| `UNCERTAIN_LOAD_BEARING` | Leave admission unresolved: no definite viable remainder is established, but a potentially decisive survivor remains genuinely unresolved. Do not silently treat it as either a definite retention or core invalidity. |

`KEEP / REDUCED / CORE / UNCERTAIN` are shorthand for these outcomes, not new
labels. Scope loss is a scientific judgment about the contribution, not a count of
deleted claims or text. With a definite survivor and uncertainty about scope loss,
retain permissively with flags and disclose that uncertainty. An evaluator or
instrumentation failure means the outcome could not be measured; it is not
scientific `CORE_INVALID`, nor automatically `UNCERTAIN_LOAD_BEARING`.

False rejection discards a materially valuable surviving transfer. False retention
admits an artifact whose distinctive source-derived contribution has failed.
Retaining a viable transfer with explicit local defects or reduced scope is not,
by itself, false retention.

## The evaluator-work gate

Before authorizing any new evaluator, warrant, provenance, citation,
classification, or admission calibration, answer all five questions concretely.

### 1. What decision failure are we trying to prevent?

Name a concrete failure, such as:

- A useful source-derived transfer would be rejected.
- A dead transfer would be retained.
- A local defect would poison the whole artifact.
- An unsupported inference would survive because it was hidden inside another
  claim type.
- A materially valid survivor could not be measured because the instrument cannot
  represent its support.

Evidence may come from natural output, a prior calibration exposing a
decision-boundary defect, or a narrowly constructed control for a demonstrated
defect. A cleaner schema, imperfect citation metadata, failure to echo labels
exactly, or a more precise harness is not sufficient justification.

### 2. How could this defect change an admission decision?

State a plausible causal path:

```text
defect
→ wrong claim/remainder judgment
→ wrong deletion/retention
→ wrong artifact admission outcome
```

or:

```text
defect
→ measurement becomes genuinely uninterpretable
→ admission outcome cannot be established
```

If no plausible path can be stated: **STOP EVALUATOR WORK.**

### 3. What is the smallest intervention that tests or fixes it?

Prefer one rule clarification, one routing correction, one small control, or one
natural-output check over another general taxonomy, broad synthetic benchmark,
provenance subsystem, or scoring layer. The burden of proof is on adding evaluator
complexity.

### 4. What evidence would tell us the issue matters scientifically?

Define success through an admission-relevant observation, such as:

- A previously false-rejected claim now survives for the correct reason.
- An invalid secondary obligation is still rejected.
- A local failure no longer destroys surviving material machinery.
- An unsupported remainder no longer rescues a dead artifact.
- Natural output can now be measured where it previously could not.
- Artifact `KEEP / REDUCED / CORE / UNCERTAIN` status would differ for a
  scientifically defensible reason.

All tests green, schema-valid output, zero citation warnings, 100% annotation
agreement, or cleaner metadata may be engineering checks. They are not sufficient
justification for evaluator research.

### 5. What is the stop condition?

Every evaluator effort must state in advance:

> **When this specific decision-boundary defect is adequately resolved, stop evaluator work and return to fresh natural transfers.**

Do not broaden scope because calibration reveals unrelated representational
imperfections. Record unrelated findings for later only if they independently
pass this evaluator-work gate.

## Mandatory protocol section

Every future evaluator-related experimental protocol must contain this short
section:

```markdown
## Evaluator-work gate

**Observed decision failure:**
<concrete failure>

**Admission consequence:**
<how it could create false reject / false retain / unmeasurable result>

**Minimum intervention:**
<smallest proposed change>

**Scientific success evidence:**
<what admission-relevant observation would justify the work>

**Stop condition:**
<when evaluator work ends and natural-output testing resumes>
```

If these cannot be filled concretely, **do not start the evaluator experiment**.
Passing this gate does not replace experiment authorization, the
[budget gate](EXPERIMENT-BUDGET-GATE.md), the [included-usage preflight](USAGE-FORECAST.md),
or existing scientific stop conditions.

## Hard stop conditions

### A — Representation-only defect

Stop or defer issues confined to punctuation, whitespace, character offsets, byte
offsets, serialization, citation formatting, response echo conventions, label
ordering, or metadata neatness unless concrete evidence shows false acceptance,
false rejection, or genuinely unresolvable measurement.

### B — Provenance is already sufficient

Stop citation/provenance research when a competent reviewer can locate the source
material, identify what supports the component, identify missing or inappropriate
evidence, and detect scope overreach, even if the citation representation is not
perfectly elegant. **H.5-level provenance is sufficient unless natural output
demonstrates otherwise.**

### C — Model compliance without scientific consequence

If a response-format violation leaves the scientific source identifiable, the
intended claim interpretable, and its scientific classification unchanged, treat
it as an interface/engineering issue. Do not automatically create another
evaluator experiment.

For example, H6.R3 citing the correct source ID but labeling it `CONTEXT` rather
than `SUPPORT` is not by itself a Chaos Mage research question. It becomes one
only if the role difference materially changes the scientific interpretation.

### D — Evaluator precision exceeds generator need

Stop when proposed work distinguishes cases more finely than needed to decide:
retain, retain with warrant flags, retain with reduced scope, core invalid, or
uncertain load-bearing. Do not introduce precision simply because it can be
measured.

### E — No demonstrated natural-output problem

Once a synthetic calibration resolves its demonstrated defect, return to natural
outputs. Do not chain synthetic calibrations merely because conceivable evaluator
edge cases remain. A hypothetical failure must have a plausible decision-boundary
consequence and independently pass the full gate to justify further work.

## Provenance-specific stop rule

> **Provenance work continues only when a genuinely supported natural-output component cannot be cleanly represented using the available span IDs and SUPPORT/CONTEXT structure, when citation ambiguity causes a false scientific acceptance or rejection, or when packet/source ambiguity makes support genuinely indeterminate. Otherwise provenance is considered good enough.**

Do not pursue further provenance work merely because `SUPPORT/CONTEXT` labels could
be more precise, the model changes a citation role while citing the right source,
spans contain multiple propositions, or citations are not minimal, unless one of
those causes a scientific decision error. Here, clean representation means
scientifically inspectable support, not perfect citation formatting.

## Warrant/classification-specific stop rule

Continue warrant-routing work only when getting the contract wrong can cause:

- A supplied premise to be deleted as unsupported.
- A governance label to hide a bad operation or empirical premise.
- An invalid generated assertion to evade warrant.
- A local defect to poison an otherwise viable transfer.

Once the evaluator can distinguish those cases sufficiently to run a natural
admission test: **STOP CALIBRATING THE TAXONOMY. RETURN TO NATURAL OUTPUTS.**
Do not require an exhaustive ontology of claim types.

## Sufficient evaluator state: “good enough”

The evaluator is sufficient for another natural-output experiment when it can,
with inspectable reasoning:

1. Distinguish supplied content from newly generated assertions.
2. Apply substantive warrant to generated inferences.
3. Scrutinize operations separately from governance structure where the
   distinction matters.
4. Localize unsupported content rather than globally poisoning the artifact.
5. Identify a surviving warranted, source-derived, material, target-relevant
   contribution.
6. Distinguish productive negative constraints from mere insufficiency.
7. Represent evidence well enough for a reviewer to inspect the judgment.
8. Separate evaluator/instrumentation failure from scientific `CORE_INVALID`.

Perfection, exhaustive classification, and citation exactness are not required.

## Natural-output return gate

At the stated stop condition, make a short human-readable decision using the
existing evidence:

1. Has the named decision-boundary defect been adequately resolved according to
   the effort's stated scientific success evidence?
2. Is the evaluator sufficient under the eight “good enough” criteria above to
   inspect the admission outcomes of fresh natural transfers?
3. Does any remaining issue have a concrete admission consequence that prevents
   this natural-output test, rather than merely an imperfect representation or
   interface?

If the defect is adequately resolved, the evaluator is sufficient, and no such
blocker remains, **end evaluator refinement and make fresh natural-transfer
testing the next scientific work**. Do not demand another synthetic calibration
to certify this return gate, a target KEEP rate, or perfect output conventions.

If a concrete blocker remains, describe its causal admission consequence and the
minimum intervention through the evaluator-work gate. Only independently justified
work may continue; do not turn the return check into a general evaluator audit.
New issues found in subsequent natural outputs must independently pass the same
gate before they justify evaluator work.

This gate determines scientific readiness and direction, not launch permission.
Fresh natural-transfer testing still requires separate authorization and the
existing budget, usage, and scientific checks. It does not resume H.6, H6.R3, or
any other frozen experiment. This policy branch performs no correction,
calibration, or natural-output test.

## Anti-goals

Chaos Mage is not trying to optimize for:

- Perfect evaluator-model agreement.
- Perfect annotation agreement.
- Complete logical formalization.
- Complete taxonomy coverage.
- Zero warning counts.
- Zero ambiguity.
- Minimal citation spans.
- Perfect reproducibility across capable models.
- Globally ranked generations.
- Maximum evaluator precision.

An exception requires direct necessity to protect the generator's admission
boundary and must pass this gate.

## Evaluator complexity principle

> **Every new evaluator distinction spends complexity budget. It must buy a demonstrable reduction in false rejection, false retention, or measurement ambiguity. If the expected gain is merely cleaner representation, do not spend the complexity.**

> **When false rejection and false retention have asymmetric costs, preserve the existing Chaos Mage preference: false rejection of a genuinely distinctive generation is generally more costly than retaining an imperfect generation with explicit flags.**

Explicit flags do not rescue an artifact whose distinctive contribution has failed.

## Relationship to current H6.R3 findings

These are policy examples drawn from the [preserved H6.R3 pause](../distance/compound-obligation-calibration-v0.2/CONTINUATION.md),
not new experiment results or revised verdicts.

**Worth pursuing:** A `TARGET/SOURCE` supplied operation that the mapping actively
prescribes may need functional scrutiny: failing to apply `OPERATION_LICENSE`
could allow a bad action to survive. This has a direct admission consequence and
can justify a minimum claim-contract correction through the gate.

**Not worth a standalone research program:** A response that cites the correct
source ID but changes `SUPPORT` to `CONTEXT` does not justify another citation
calibration unless review establishes that the role change alters the scientific
judgment or makes provenance uninterpretable. Treat response-side citation-role
echo as an interface issue by default. This policy does not convert the frozen
rejected H6.R3 response into an accepted judgment or relax its historical validator.

## Current stop decision

> **The evaluator/provenance subsystem is not to receive additional broad synthetic refinement merely to clean up citation or schema behavior. After the minimum claim-contract correction needed to prevent known false rejection/retention paths, the project should return to fresh natural-transfer testing. New evaluator work discovered thereafter must independently pass this gate.**

This branch freezes policy only. Do not implement the future correction here,
start H6.R4, resume H6.R3, modify provenance machinery or historical experiment
results, or run any provider evaluation.
