# Frozen inquiry-unit rule v0.1

Inquiry-role annotation is semantic rather than polarity-based. A surviving inquiry constraint exists whenever the mapping explicitly preserves (a) an unresolved set of live alternatives, (b) a specific next operation, and (c) an outcome relation under which possible results bear differently on those alternatives. These elements may occur in affirmative or negative language and may span multiple clauses. Every such complete unit must receive INQUIRY_CONSTRAINT role assessment regardless of any negative_inference flag. Mere non-discrimination language remains INSUFFICIENCY_ONLY when no complete discriminating inquiry unit is supplied.

```python
complete_inquiry_unit = (
    unresolved_contrast.present is True
    and len(unresolved_contrast.alternatives) >= 2
    and next_operation.present is True
    and differential_outcome_relation.present is True
    and len(differential_outcome_relation.outcomes) >= 2
    and provenance_complete is True
    and outcomes_are_discriminating(unit)
)
if complete_inquiry_unit:
    assert exactly_one_role_assessment(unit_id)
    assert role == "INQUIRY_CONSTRAINT"
```

All fields are scanned after ordinary remainder extraction. Discovery, completeness,
role eligibility, assignment and coverage must not depend on negative_inference,
polarity, field placement or imperative/declarative form. The implementation pattern
`if negative_inference: classify_inquiry(...)` is prohibited.

An unresolved contrast requires two explicit, currently live alternatives. An already
resolved contrast is not live. A next operation must be selected and concrete, not
merely a hypothetical test or an ungrounded request for evidence. At least two distinct
outcome/consequence mappings must differ in their bearing on the live alternatives.
Every component needs exact surviving-source provenance; combine clauses, never invent
components. Offsets are zero-based UTF-8 byte offsets, end exclusive.

Unit identity is the canonical contrast + selected operation + differential outcome
logic. Multiple clauses and repeated equivalent formulations belong to one unit with
all supporting spans. Independent inquiries with different operations or outcome logic
are separate units. Insufficiency statements remain INSUFFICIENCY_ONLY in the ordinary
inventory; the composite decision structure owns INQUIRY_CONSTRAINT.

Role and productivity are separate. Remove the entire semantic unit, including all its
formulations. If the specifically selected inquiry ceases to be justified/selected,
next_inquiry=changed and productivity=YES; unchanged gives NO; uncertain gives UNCERTAIN.
An independent surviving unit can make a complete inquiry nonproductive. Exact duplicates
are one unit, so deleting only one duplicate sentence is not this counterfactual.

Required failure codes: IQ_MISSING_ROLE, IQ_WRONG_ROLE, IQ_MISSING_CONTRAST,
IQ_TOO_FEW_ALTERNATIVES, IQ_MISSING_OPERATION, IQ_GENERIC_OPERATION,
IQ_MISSING_OUTCOME_RELATION, IQ_TOO_FEW_OUTCOMES, IQ_NONDISCRIMINATING_OUTCOMES,
IQ_INVENTED_COMPONENT, IQ_POLARITY_GATING, IQ_DUPLICATE_UNIT, IQ_UNCITED_SPAN.
Additional checks may fail as IQ_COMPONENT_MISMATCH, IQ_COVERAGE_SUMMARY,
IQ_PRODUCTIVITY, IQ_SCHEMA or IQ_UNKNOWN_UNIT. No failed coverage can count as success.
