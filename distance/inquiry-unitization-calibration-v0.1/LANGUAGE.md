# Bounded semantic grammar and provenance

This v0.1 recognizer scans every string field, without an eligibility or polarity flag.
It recognizes explicit live or unresolved pair relations, concrete selected operations,
and linked outcome/consequence clauses. A resolved declaration vetoes unresolved status.
Each of four supported mechanisms has a vocabulary in extractor.LANGUAGE, including both
H.3 diagnostic phrasings. The grammar reads no case IDs, expectations or model output.
It joins only components with the same supported operation/alternative/outcome vocabulary.
An operation must begin a clause; a hypothetical mention does not select an inquiry.

The grammar deliberately covers these authored cases and two regressions. It does not
claim general synonym resolution, anaphora, nested logical scope, incompatible contextual
conditions, multiple distinct operations within one mechanism, or arbitrary natural output.
Those require separate future calibration. Matching words without the explicit relation
is insufficient. Contextual qualifiers outside this grammar can require abstention in a
future version; this version must not be integrated into production.

Canonical aliases normalize lexical variation, including the terse H.3 directive.
Evidence is always the original byte-exact span, never the normalized string. Model
responses must copy component text as instructed; normalizer accepts only frozen aliases.
The validator rescans cited spans and the full mapping independently. Components cannot
be licensed by an uncited field or an invented paraphrase. Full clauses preserve relation
provenance. Duplicate bundles union provenance into one decision structure; they do not
create independent marginal-value assessments.

Insufficiency sentences remain ordinary INSUFFICIENCY_ONLY inventory entries. Their
contrast spans may also supply one component of a composite inquiry, whose role belongs
to the full structure. This is not a role upgrade for the insufficiency sentence.
