# Frozen atomic claim-warrant scoring

Judge only the identified atomic claim in its exact parent context and original
mapping. Assume all stated execution prerequisites are satisfied and the stated
signal occurs. Does that signal license this claim within the supplied limits?

SUPPORTED: the stated operation/signal licenses the claim within its explicit bounds.
CONDITIONAL_WARRANT: the mapping supplies a specific unresolved empirical relation
whose establishment would license it. Cite that relation; do not invent one or
confuse execution readiness with warrant.
UNSUPPORTED: even with execution prerequisites satisfied and the signal observed,
the claim does not follow as mapped.
UNCERTAIN: packet information is insufficient to decide; explain without forcing
an unsupported label.

Do not assess whole-artifact viability, infer intended defects, or repair claims.
No external context, tools, browsing, other cases or historical judgments.
Return claim_id, status, rationale, signal_basis, stated_empirical_relation, uncertainty.
signal_basis and stated_empirical_relation are lists of separate exact contiguous
excerpts, each {source_field, exact_text}. source_field is mapping.FIELD or
source.instrument.FIELD, where FIELD is state/operation/signal/inference/limit.
Never concatenate separated excerpts in one exact_text. The empirical relation
must cite mapping content and be nonempty only for CONDITIONAL_WARRANT.
For UNCERTAIN supply a nonempty uncertainty list. Keep explanation outside quotes.
