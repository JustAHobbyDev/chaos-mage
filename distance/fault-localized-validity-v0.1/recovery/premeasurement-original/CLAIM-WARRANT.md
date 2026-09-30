# Claim-level warrant rubric

Judge only the single identified atomic claim, in its exact parent context.
Assume all stated execution prerequisites are satisfied and the stated signal
occurs exactly as described. Does that signal license this specific claim within
the mapping's stated limits?

- SUPPORTED: the stated operation/signal licenses the claim within its explicit bounds.
- CONDITIONAL_WARRANT: the mapping itself supplies a specific unresolved empirical
  relation whose establishment would license the claim. Quote that relation.
  Do not invent a missing relation or count execution readiness as warrant.
- UNSUPPORTED: even with execution prerequisites satisfied and the stated signal
  observed, the claim does not follow as mapped.
- UNCERTAIN: the packet establishes insufficient information to decide. Explain
  the uncertainty; do not automatically classify it as unsupported.

Do not assess other claims or whole-artifact viability. Do not repair the mapping.
No external context, browsing, tools, historical judgments, or prior sessions.
Return the specified JSON object with claim_id, status, rationale, signal_basis
(exact mapping quotation), stated_empirical_relation (exact quotation for
CONDITIONAL_WARRANT, null otherwise), and uncertainty (nonempty for UNCERTAIN).
