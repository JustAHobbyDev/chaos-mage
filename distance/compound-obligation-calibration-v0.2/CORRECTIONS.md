# Frozen prospective corrections — H6.R3 v0.2

H6.R2 remains unchanged and terminated at `5b6dd0e63b280118a6473fa25b3295af376f7a3c`. This is a new calibration, not a repair, continuation, or re-use of measurements. All historical packets, judgments, incident evidence, metrics, reports and terminal state remain immutable.

## 1. Immutable obligation provenance

Every obligation, including each inline secondary, freezes obligation_id, contract, subject and provenance_refs before Stage C.

**The Stage C packet builder may resolve frozen obligation references to their associated source text, but may not add, remove, substitute, reorder semantically, promote, demote, or reconstruct citation roles. The `source_id + role` pairs in the Stage C scientific packet must canonically equal those frozen for that obligation.**

`canonical(stage_c.provenance_refs) == canonical(frozen_obligation.provenance_refs)` and obligation provenance hash == Stage C packet provenance hash are mandatory. Reference order is explicitly semantically irrelevant in the schema; roles are never ignored. No whole-claim citation inheritance, parent fallback, or inferred SUPPORT/CONTEXT assignment. Exact equality also applies to the resolved evidence bundle. Every packet is constructed and checked before any Stage C launch. A mismatch is PROVENANCE_PROJECTION_FAILURE and blocks premeasurement execution.

## 2. Governance structure is orthogonal to substantive validity

GOVERNANCE_COHERENCE stays historical and unchanged. GOVERNANCE_STRUCTURE is the new contract, with the exact question and boundary wording frozen in CONTRACTS.md and taxonomy.json. It judges determinate prospective trigger/response and internal decision coherence only. It excludes operation information value, mechanism licensing, effectiveness, causal appropriateness, target relevance, and factual/inferential/conditional/limiting premise truth or warrant.

No identifiable trigger, indeterminate response, incompatible responses without precedence, an explicit nonterminating resolution loop, or internally contradictory policy can violate this contract. An irrelevant diagnostic, mechanism violation, false empirical reason, unsupported threshold, or overreaching outcome relation alone cannot.

For “If unresolved, inspect badge colors”: GOVERNANCE_STRUCTURE is expected SATISFIED; OPERATION_LICENSE is expected VIOLATED. These are hidden hypotheses, never answers supplied to evaluation contexts. Any prohibited substantive reasoning is preserved and flagged GOVERNANCE_BOUNDARY_LEAK; no post-hoc verdict repair.

## 3. Origin and function for embedded dependencies

Every material dependency independently receives content_origin, epistemic_function, assertion_mode (REFERENCED_PREMISE or ASSERTED_COMPONENT), origin_refs and rationale before contract selection. Uncertain axes stay explicit. After the full Stage B response freezes, deterministic routing selects contracts.

Asserted target/source/both supplied content receives target/source/both fidelity contracts regardless of function. Generated FACT, INFERENCE, CONDITIONAL_RELATION, OPERATION, GOVERNANCE_RULE and LIMIT receive respectively FACT_WARRANT, DERIVED_WARRANT, CONDITIONAL_LICENSE, OPERATION_LICENSE, GOVERNANCE_STRUCTURE and LIMIT_WARRANT.

A supplied REFERENCED_PREMISE merely invoked at unchanged scope/strength, without reassertion, transformation or extension, resolves GROUNDING_REF with no new judgment. An existing separately evaluated proposition resolves CLAIM_REF with no duplicate judgment. A distinct asserted material proposition resolves INLINE_OBLIGATION.

P2's target-supplied threshold agreement is TARGET_SUPPLIED + FACT + REFERENCED_PREMISE -> GROUNDING_REF. Its only scientific obligation is GOVERNANCE_STRUCTURE. “T is where user harm begins” is a new generated FACT or INFERENCE with a warrant obligation. Supplied origin never licenses expanding a premise through GROUNDING_REF.
