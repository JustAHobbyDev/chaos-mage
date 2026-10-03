# Evidence-record schema

[evidence-record.schema.json](evidence-record.schema.json) describes one offline
candidate/selected case with source lineage and separately recorded measurements.
It is specific to the three H6.R4 observations, not a new evaluator taxonomy.

- `status`: SCREENED_CANDIDATE is a shortlist entry, not a selected scientific
  observation. SELECTED is allowed only with all three slots frozen together.
- `selection`: stable case/claim identity, original claim-file hash and JSON
  pointer, exact frozen text and scope, independent origin/function/mode, source
  references, selection reason, expected contracts, hidden operator hypotheses.
- Each `source_refs` entry binds a case-local source ID and input role to an exact
  text value, its SHA-256, the repository file's SHA-256 and its JSON pointer.
  Hash text as UTF-8 without trimming or newline normalization. Original mapping
  P IDs retain their existing roles. Named target/source IDs have explicit lineage.
- `routing`: intended resolution and contract list. This is an offline record,
  not proof that a provider has applied or satisfied an obligation.
- `measurements`: empty until an actual judgment exists. Each later record binds
  contract, verdict, reasoning and response source IDs to request/response/raw
  evidence hashes, execution commit, model/effort and reservation identity (or
  explicit historical reuse lineage). Never copy a hidden hypothesis here.
- `overall`: null until all required obligations have actual interpretable
  observations; always null for grounding-only. Null is not UNCERTAIN.

The schema checks record shape. Scientific supply, unchanged scope, eligibility,
allowed citation membership, exact input projection and complete three-slot freeze
remain explicit evidence checks, not assertions inferred from schema validity.
Provider packets are separately constructed from an allowlist; they never contain
the full evidence record or any hidden operator hypothesis.

If selection fails, `selection/scan.json` records the missing slot and rejected
alternatives separately. Do not invent an original claim ID, text, verdict or
evidence record to fill a missing scientific case.

The provider-facing response schema has only obligation identity, verdict,
reasoning and `evidence_used: [{source_id: ...}]`. Input roles remain harness-owned.
A syntactically valid response still must cite only its frozen obligation's IDs;
the full input ID/role/text projection is independently checked before dispatch.
