# Frozen claim-role schema v0.1

Stage A JSON is `schemas/role.schema.json`; Stage B JSON is
`schemas/evaluation.schema.json`. Each object is one record, not a wrapper.
These encode the fields supplied in the handoff, with cross-field invariants
checked by the runner. `claim_id` is the original packet/local ID joined by `/`.

## Stage A — claim_role_assignment

Required fields: claim_id, atomicity, assignment_status, primary_role,
competing_roles, role_provenance, rationale.

- ATOMIC + ASSIGNED: exactly one primary_role; competing_roles is empty.
- SPLIT_REQUIRED: ATOMIZATION_DEFECT; primary_role is null; competing_roles is empty.
- ROLE_UNCERTAIN: ATOMIC; primary_role is null; at least two distinct competing roles.
- No eighth evidential role. No role priorities are added to resolve overlap.
- One proposition gets one role. A mixed historical claim is recorded as a defect,
  never silently split, rewritten, or repaired during measurement.
- Every Stage A output freezes before any Stage B call. Neither the evaluator nor
  operator can reclassify a claim after Stage B begins.

Each provenance entry contains source_type (TARGET, SOURCE_INSTRUMENT, MAPPING)
and source_id. Mapping span IDs remain local to the original packet envelope;
target IDs and source instrument IDs remain distinct namespaces.

## Seven definitions

### SUPPLIED_FACT

A proposition directly supplied by the target/problem material or a faithful non-expansive restatement thereof. It is not required to be independently established by the transferred mechanism.

### SOURCE_FACT

A proposition directly supplied by the frozen source instrument or a faithful non-expansive restatement of its mechanism, conditions, or limits. It is not required to be established from target observations.

### DERIVED_INFERENCE

A proposition asserting that evidence, observations, or transferred structure supports, weakens, excludes, bounds, ranks, explains, or establishes something about the target.

### CONDITIONAL_RELATION

A proposition asserting what a hypothetical or future outcome would imply. It does not assert that the outcome has occurred.

### OPERATION

A proposed observation, test, comparison, intervention, perturbation, or transformation to perform on the target.

### GOVERNANCE_RULE

A prospective decision rule, threshold, stopping condition, rollback rule, safety rule, or policy rule that governs what to do rather than purporting to report an empirical discovery.

### LIMIT

A proposition stating scope, ambiguity, confound, failure condition, non-identifiability, or restriction on reasoning or application.

## Stage B — claim_evaluation

Required fields: claim_id, frozen_role, contract_id, verdict,
evaluation_provenance, unresolved_conditions, rationale.
Only ATOMIC + ASSIGNED proceeds. The role and contract must match the frozen
assignment and routing exactly. CONDITIONAL requires at least one explicit
unresolved condition. Other verdicts retain whatever conditions the provider
actually reports; they are not repaired.

> A proposition may be marked VIOLATED only for failure of the contract associated
> with its prospectively frozen role. Failure to satisfy another role's contract
> is irrelevant.

Machine validation checks record structure and routing. Semantic adherence to this
invariant is audited without rewriting any provider judgment.
