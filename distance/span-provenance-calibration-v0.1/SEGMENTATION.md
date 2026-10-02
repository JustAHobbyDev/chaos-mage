# Neutral segmentation — H.5

**Preserve field boundaries. Within each field, segment according to explicit
authored structure first and ordinary sentence boundaries second. Never perform
clause-, proposition-, argument-, or semantic-role-sensitive segmentation. When a
boundary is uncertain, retain the larger span.**

Process state, operation, signal, inference, limit in that order with one shared
function. Empty fields contribute no spans. Explicit blocks are paragraphs, list
items (including nested items), and table rows. Blank lines separate paragraphs;
ordinary single line breaks do not. List continuation lines stay with their item.
Nested items retain a parent ID. Markdown pipe-table headers are separately
addressable; delimiter rows remain harness metadata; data rows are never split
into cells. List items and table rows remain whole, even with multiple sentences.

Within prose paragraphs, split only at unambiguous . ! ? followed by whitespace
and a new uppercase sentence. Retain ambiguous abbreviation/initial/decimal,
ellipsis, quote, parenthesis or bracket boundaries; lowercase starts remain
coarse. This deliberately incomplete English splitter uses no NLP dependency.
Do not chase perfect sentence splitting with semantic rules.

Never split at commas, semicolons, colons, conjunctions, because/therefore,
if/then, contrasts, or model-inferred propositions. No word/token/character cap.
No field-specific action/observation/conclusion rules. Segmentation has no access
to component expectations, inquiry roles, provider judgments, or semantic reviews.

Assign P001 onward in field/block/sentence encounter order. These are identities
only; field and structure live in separate metadata. IDs need not persist when
the source changes. Harness-only character ranges identify exact source slices
and support integrity checks; they never appear in the annotation schema.
Span text is copied without normalization. Inter-span layout remains in the
frozen mapping; no claim is made that concatenating citation text recreates layout.

Round-trip JSON must preserve ID-to-text association. Repeated segmentation of
identical content must reproduce the complete table. Report retained uncertain
boundaries as diagnostics, not semantic failures. Test synthetic lists/tables and
former/latter independently; none occur in the frozen 20-mapping corpus.
