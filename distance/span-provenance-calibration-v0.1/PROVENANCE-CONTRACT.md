# Provenance contract — frozen H.5 architecture

**Scientific provenance requires an unambiguous reference from each semantic
component to frozen surviving source content. The model is not required to
reproduce source bytes, punctuation, quotes, or character offsets. Exact byte
preservation belongs to harness-owned experiment-integrity machinery, not
semantic annotation.**

Artifact identity is exact: source files, historical results, raw responses,
tables and review records remain hash-bound. Semantic citation is an opaque
packet-local span ID plus a separately assessed support relationship. Hashes
never establish semantic support.

An annotation envelope identifies `packet_id`. Its components have `component_id`,
`component_type`, `value`, `scope`, and `provenance.refs`. Each ref contains only
`source_id` and `role` (`SUPPORT` or `CONTEXT`). At least one SUPPORT is required.
Engineering fixtures additionally record `expected_support_status` (nullable for
mechanically invalid bundles) and expected diagnostics. A future annotation can
include `provenance.support_status` and `rationale`; this is an annotator claim,
not a trusted assessment. Independent review records live outside fixtures.

SUPPORT contributes substantive content. CONTEXT supplies antecedents, identities,
definitions, scope, conditions, or list/table meaning needed to interpret it.
Context cannot manufacture an absent relation. Multiple spans may jointly support
one component; one span may support several components; extra propositions and
unnecessary context do not invalidate a bundle. Minimality is not tested.

**A provenance bundle must contain all substantive source material necessary to
recover the annotated component.** Given only the cited bundle and ordinary
linguistic interpretation, can a reviewer recover the claim at its stated scope?
Return SUFFICIENT, INSUFFICIENT, or UNCERTAIN. Resolve normal coreference when
cited context supplies its referent. Do not import uncited substantive premises
or drop material qualifiers. No numeric support score exists.

## Mechanical taxonomy

- `PROV_UNKNOWN_SOURCE_ID`: ID absent from the bound packet.
- `PROV_WRONG_PACKET`: annotation envelope names a different packet from the
  supplied table. Resolution never falls back to another packet.
- `PROV_NO_SUPPORT`: no SUPPORT reference.
- `PROV_DUPLICATE_REF`: a source ID occurs more than once in a bundle.
- `PROV_ROLE_CONFLICT`: the same ID is SUPPORT and CONTEXT; also emit duplicate.
- `PROV_SCHEMA`: malformed interface or invalid role.

IDs are local, not globally unique. A bare P003 copied from another packet cannot
be identified as foreign if local P003 exists. Packet binding prevents explicit
cross-packet resolution; semantic review is still necessary to catch wrong content.
No model-authored start/end, byte/character offset, exact quote, or source text is
part of citation validity. Serialization formatting is not a semantic judgment.

## Recorded semantic taxonomy

- `PROV_MISSING_CONTEXT`: unresolved necessary referent, condition, or scope.
- `PROV_UNSUPPORTED_COMPONENT`: bundle lacks the substantive claimed relation.
- `PROV_SCOPE_OVERREACH`: claim broadens/drops a material qualifier.
- `PROV_UNCERTAIN_SUPPORT`: plausibly supported but genuinely indeterminate;
  preserve UNCERTAIN, not automatic failure.

`PROV_CONFLICT_REVIEW` is non-failing and requires an explicit engineering review
that two assertions are mutually incompatible, plus matching component type and
target/scope and overlapping SUPPORT. Mere differing values or span reuse are
insufficient. H.5 implements no logical contradiction detector.

Missing, stale or structurally inconsistent engineering review records are harness
gate failures (`REVIEW_*`), not semantic provenance findings. Changed frozen bytes
are integrity failures (`INTEGRITY_*`), never evidence of unsupported meaning.
