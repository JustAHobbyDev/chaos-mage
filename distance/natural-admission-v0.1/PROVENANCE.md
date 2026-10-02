# H.5 integration — unchanged semantic citation contract

Mapping fields are segmented by the frozen H.5 segment.py, unchanged: field, explicit
authored block, conservative sentence boundary, stop. No clause splitting. Pxxx IDs
are opaque and local to the packet_id envelope. Cite only this packet's mapping spans.
Source instrument and target are distinct named input data, not other mapping packets.

Each semantic component has value, scope and provenance.refs, each ref comprising
source_id and role SUPPORT or CONTEXT. SUPPORT contributes substance; CONTEXT only
resolves reference, identity, scope or authored structure. CONTEXT cannot supply missing
substantive inference. Include material qualifiers in the cited bundle. Assess whether
only the cited bundle plus ordinary linguistic interpretation reconstructs the component:
SUFFICIENT, INSUFFICIENT, UNCERTAIN. These statuses describe attribution to the mapping,
not whether the attributed claim has warrant. An unsupported claim can be perfectly
traceable. At least one SUPPORT per substantive component. An explicitly inapplicable
component uses value NOT_APPLICABLE, empty refs, scope NOT_APPLICABLE and SUFFICIENT
with a reason; it is excluded from provenance support counts.

Never supply offsets, exact source-text reproduction or byte-identical quotes as
semantic citation requirements. Model component values are semantic descriptions.
Harness-only ranges and hashes preserve immutable artifact identity.

Report anomalies without repairing content. Codes include PROV_UNKNOWN_SOURCE_ID,
PROV_NO_SUPPORT, PROV_DUPLICATE_REF, PROV_ROLE_CONFLICT, PROV_WRONG_PACKET,
PROV_MISSING_CONTEXT, PROV_UNSUPPORTED_COMPONENT, PROV_SCOPE_OVERREACH,
PROV_UNCERTAIN_SUPPORT. A wrong citation initially is PROVENANCE_MODEL_ERROR. Report
H5_UNREPRESENTABLE_SUPPORTED_COMPONENT, H5_UNCITED_SUBSTANTIVE_DEPENDENCE,
H5_COARSE_CONTRADICTION_OR_QUALIFIER, H5_DISPERSED_SIMPLE_SUPPORT,
H5_OUTSIDE_QUALIFIER, H5_CONTEXT_INFERENCE, H5_NONDETERMINISTIC_SEGMENTATION,
H5_MARKUP_SCOPE_DAMAGE only when describing the corresponding observed weakness.
For each anomaly identify component, evidence and whether correct support can be
represented with the existing spans. No automatic segmentation repair.
