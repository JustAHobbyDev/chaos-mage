# Frozen fault-localized viability scoring

After the identified unsupported claims are deleted without replacement, what
distinctive source-derived epistemic capability still survives?

Treat the deletion markers as unavailable premises. Original text is supplied for
dependency tracing only; deleted content cannot support a surviving inference.
Delete all listed claims simultaneously. Do not add new measurements, controls,
hypotheses, evidence, inference rules or target framing. Grammatical debris alone
does not establish failure. Preserve surviving antecedents and explicit limits.

## Dimensions

mechanism_survival: SURVIVES | PARTIALLY_SURVIVES | DOES_NOT_SURVIVE | UNCERTAIN.
Does at least one distinctive source-derived state → operation → signal →
warranted-inference chain remain? Executable operations alone do not establish
survival. Generic target reasoning alone does not establish survival.

target_contribution_survival: SUBSTANTIALLY_SURVIVES | REDUCED_BUT_MATERIAL |
NO_MATERIAL_CONTRIBUTION | UNCERTAIN. What material warranted contribution to the
original target question remains? Discriminating evidence, hypothesis elimination,
bounded causal or historical constraint, problem decomposition, intervention,
stopping rule or next-inquiry selection can be material. Full solution is unnecessary.

dependency_cascade: LOCAL | BRANCH | GLOBAL | UNCERTAIN.
LOCAL: defect terminates locally or affects only minor descendants.
BRANCH: a meaningful advertised branch fails while another material source-derived
branch survives. GLOBAL: essentially every distinctive material target contribution
depends directly or indirectly on the deleted inference. UNCERTAIN: dependency
extent cannot be established from the packet. Inventory failed claims, failed
actions/inquiries, surviving claims and surviving actions/inquiries with citations.
Cascade is diagnostic; it does not independently determine artifact status.

remainder_check: DISTINCTIVE_REMAINDER | GENERIC_REMAINDER | NO_REMAINDER | UNCERTAIN.
Is surviving reasoning recognizably an operational consequence of the imported
source mechanism? Lots of remaining text does not establish viability.

strongest_surviving_target_inference requires text, source_spans, why_warranted.
The inference must already exist in or be directly entailed by surviving mapping
content. Never invent a repaired inference. If none can be identified, text is
null, source_spans is empty, and why_warranted explains the absence/uncertainty.
Failure to identify a material warranted target inference is strong core-invalidity
evidence, not an extra automatic status rule.

central_bridge requires deleted_claim_is_required_for_all_material_contributions
(yes | no | uncertain) and rationale. Distinguish importance from load-bearing necessity.

## Deterministic base status

Precedence: 1. hard failure; 2. decisive-field uncertainty; 3. surviving target
contribution; 4. dependency cascade as consistency evidence only.

```python
if mechanism_survival == "DOES_NOT_SURVIVE":
    artifact_status = "CORE_INVALID"
elif target_contribution_survival == "NO_MATERIAL_CONTRIBUTION":
    artifact_status = "CORE_INVALID"
elif mechanism_survival == "UNCERTAIN":
    artifact_status = "UNCERTAIN_LOAD_BEARING"
elif target_contribution_survival == "UNCERTAIN":
    artifact_status = "UNCERTAIN_LOAD_BEARING"
elif target_contribution_survival == "SUBSTANTIALLY_SURVIVES":
    if mechanism_survival == "SURVIVES":
        artifact_status = "KEEP_WITH_WARRANT_FLAGS"
    elif mechanism_survival == "PARTIALLY_SURVIVES":
        artifact_status = "KEEP_WITH_REDUCED_SCOPE"
elif target_contribution_survival == "REDUCED_BUT_MATERIAL":
    artifact_status = "KEEP_WITH_REDUCED_SCOPE"
```

SURVIVES + REDUCED_BUT_MATERIAL + cascade UNCERTAIN → KEEP_WITH_REDUCED_SCOPE.
SURVIVES + SUBSTANTIALLY_SURVIVES + cascade UNCERTAIN → KEEP_WITH_WARRANT_FLAGS.

## Structural contradiction exception

If cascade positively contradicts decisive dimensions, mark structural_conflict
present=true and explain. Examples: SUBSTANTIALLY_SURVIVES with GLOBAL, or
NO_MATERIAL_CONTRIBUTION with LOCAL. Do not silently override either dimension.
Set resolved=true only if the rationale reconciles the apparent contradiction;
otherwise resolved=false and artifact_status=UNCERTAIN_LOAD_BEARING, reason
"unresolved structural contradiction". This exception overrides the base status,
including a hard failure. Genuine uncertainty is a valid structured answer.
When no conflict exists, present=false and resolved=true, explaining why.

## Anti-shortcut and output requirements

Do not infer status from number of unsupported claims, percentage deleted, amount
of remaining prose, technical sophistication, foreign terminology, number of
executable operations, surviving bullets, or original apparent usefulness.
Ten leaf defects may still be non-core. One central defect may be CORE_INVALID.

Return the specified JSON schema. Citations are separate exact contiguous excerpts:
source_spans entries use source_field (mapping.state/operation/signal/inference/limit
or source.instrument.state/operation/signal/inference/limit) and exact_text.
Never join separated excerpts into one quotation. Cite surviving mapping content
for the strongest inference and surviving inventories; deleted spans may be cited
only when identifying failed claims/dependencies. Explain entailment in prose
outside the quotations. Include per-claim dependencies for every unsupported ID.
