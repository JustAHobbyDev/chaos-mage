# Deterministic selection — frozen before computation

Eligible corpus: every `instruments/*.yaml` at exact base
`281cf1606de59b9b0c9753dcbe0d170f26b601c9` with extraction.status = accepted.
Instrument identity = extraction.id; family = extraction.practice, unchanged.
Use unchanged five fields; do not author or revise instruments.

Visit T01, T02, T03 in that order; slots 1 then 2. Exclude families already used
for that target. Minimize this lexicographic tuple over eligible instruments:

1. Global prior use count of the family.
2. Global prior use count of the instrument.
3. SHA256 of UTF-8 `H7-natural-v0.2|<target_id>|<slot>|<instrument_id>`.
4. Instrument ID.

Increment both counts immediately after selection. This favors family diversity
across six slots without evaluating compatibility. No target text, semantic
similarity, predicted success or output enters the computation. No reseeding,
reranking, replacement or hand selection. Freeze the entire six-pairing result
before packet creation or provider execution.
