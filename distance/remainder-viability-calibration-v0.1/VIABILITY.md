# H.2 frozen remainder-viability construct

CORE_INVALID means absence of a viable source-derived remainder after all measured
UNSUPPORTED claims are deleted simultaneously. It is not a judgment about deleted
claim centrality, count, text volume, or how many operations remain executable.

For every supplied candidate, and any additional candidate discoverable in the
surviving mapping, assess four independent properties as YES, NO, or UNCERTAIN:

* warranted: surviving content licenses the inference; plausibility, weaker wording,
  executability and potential future evidence do not supply warrant;
* source_derived: an operational consequence of the imported reasoning instrument,
  rather than generic/native target-domain procedure;
* material: changes understanding, constraints, investigation, intervention or inquiry
  in a useful way, even if its scope or textual size is small;
* target_relevant: bears on the exact retained question or a legitimate bounded
  subpart. A valid inference about something else does not qualify.

A candidate is viable exactly when all four assessments are YES. A candidate is
decisively unresolved exactly when none is NO and at least one is UNCERTAIN.
An UNCERTAIN field cannot rescue a candidate already disqualified by NO.

Derivation, in order:

1. An explicitly unresolved structural contradiction yields UNCERTAIN_LOAD_BEARING.
2. At least one viable candidate and substantially_intact scope yields
   KEEP_WITH_WARRANT_FLAGS; with reduced scope, KEEP_WITH_REDUCED_SCOPE.
3. With no viable candidate but at least one decisively unresolved candidate, use
   UNCERTAIN_LOAD_BEARING.
4. Otherwise use CORE_INVALID, with mechanism_death, generic_remainder,
   target_payoff_loss, or epistemically_empty as the best explanatory reason.

A viable candidate combined with none/uncertain scope is a structural contradiction;
explain it and either reconcile the fields or mark it unresolved. Unresolved conflicts
are the sole exception allowing UNCERTAIN_LOAD_BEARING alongside a definite viable
candidate. Generator-facing uncertainty policy remains keep + flag.

Reason none accompanies definite keep decisions; uncertain accompanies unresolved
decisions. CORE_INVALID normally has scope none. A declared conflict may explain
diagnostic differences; do not silently overwrite any model field.

Retain mechanism_survival, target_contribution_survival, dependency_cascade,
remainder_check, strongest_surviving_target_inference and central_bridge as diagnostic
evidence. They do not independently derive status. Mechanism death generally aligns
with DOES_NOT_SURVIVE; generic remainder generally aligns with GENERIC_REMAINDER.
Require a structural_conflict explanation for departures. Unreconciled departures
yield uncertainty. A central claim can be bypassed by another viable contribution.

Assess every frozen candidate without changing its identity, text, or provenance.
Additional judge-discovered candidates must be marked judge_added and cite surviving
mapping text. Direct entailment is allowed; inventing a repaired, replacement or
future-supported inference is not. Strongest inference references an assessed
candidate and its four properties; merely source-derived or merely warranted is
insufficient. When no candidate inference exists, its reference/text may be null.

The output remainder_viability contains candidate assessments, viable IDs, scope,
diagnostics, reason, status, structural_conflict {present,resolved,explanation}, and
uncertainty. viable_remainder_assessment is a deterministic publication projection of
that same output, never a second independent controlling judgment.
