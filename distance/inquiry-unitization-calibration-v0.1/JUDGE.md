# Assessment instructions

Assess the supplied surviving mapping. Scan ALL fields, regardless of the descriptive
negative_inference flag. Populate the semantic components from this text alone. Do not
make an artifact viability judgment. Return only the JSON schema response.

Group spans by the same contrast, selected operation, and outcome logic; repeated
formulations of that entire structure receive one unit and one role assessment. Include
incomplete candidate structures too, with NOT_INQUIRY_CONSTRAINT or UNCERTAIN as warranted.
Number structures IQ1, IQ2, ... in alphabetical mechanism order if more than one. All
components of one structure share one ID. Do not create one object per sentence.

Use these field conventions consistently:
- source_field is mapping.<field>; cite whole supporting clauses or sentences. exact_text
  must be copied verbatim. start/end are zero-based UTF-8 byte offsets, end exclusive.
  Include the full contrast relation, selected action clause, and each outcome/consequence
  relation, preserving their wording. One long exact span covering several clauses is fine.
- alternatives lists the explicit named alternatives, even if the contrast is resolved;
  present is true only if at least two remain live. Copy their names exactly, preserving
  case (H1/H3, b required/b not required, offset +6/offset +7, lock contention/isolated pool
  exhaustion). If none are explicitly identifiable, use [].
- operation copies the concrete action phrase, retaining its qualifiers; including "next"
  or the declarative selection prefix is fine. If only a generic evidence request occurs,
  retain that exact request here but present=false. If no action is selected, use "".
- outcomes retains each explicit outcome/consequence mapping, including nondiscriminating
  ones; present=true requires at least two that bear differently on the live alternatives.
  Copy each outcome phrase and its consequence phrase separately; omit separator punctuation.
  For each bears_on list both alternatives involved in the comparison, with the same names
  as alternatives. A favored alternative and the alternative disfavored relative to it are
  both affected. Use [] if no outcomes are supplied. Keep abstract discriminating outcome
  relations even when the contrast is resolved; unresolved_contrast.present separately
  records whether both alternatives are live. Thus differential_outcome_relation.present
  can be true for a resolved contrast when the stated test is abstractly discriminating.
- provenance_complete=true only when an explicit unresolved contrast, selected concrete
  operation and discriminating relation all have exact surviving-source citations.
  Partial structures have provenance_complete=false. Do not infer missing content.
- Every complete unit MUST have role=INQUIRY_CONSTRAINT. Incomplete structures do not qualify.
- Assess the counterfactual removal of the entire unit, including ALL duplicate formulations.
  Changed/unchanged/uncertain mechanically maps to YES/NO/UNCERTAIN productivity. An
  insufficiency statement alone cannot supply the inquiry. Independent surviving units
  can make a complete unit nonproductive; duplicate formulations of one unit are removed
  together. Membership and marginal productivity are distinct.
- The coverage summary counts complete semantic units and all INQUIRY_CONSTRAINT assessments.
  A successful response has equal counts, no uncovered IDs, no duplicate units and
  validation_passed=true. For an incomplete case both counts can be zero with successful
  validation. Do not count source clauses or duplicate textual formulations as extra units.

Rationales should explain the supplied text and counterfactual. No missing component may
be invented. Polarity, imperative/declarative wording, field placement and initial remainder
classification never control discovery, completeness, role assignment or coverage.
