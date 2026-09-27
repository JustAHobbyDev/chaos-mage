# Problem Frames

## Entry #1 — 2026-09-26 — Frozen retrieval preparation and isolated execution

### Domains

- Existing lexical inputs: user-controlled corpus Git snapshot, committed targets,
  and preregistration. Preparation reads these without modifying them.
- Preparation-owned lexical outputs: candidate representations, packets, hashes,
  execution order, and configuration. Private identity key and seed stay local.
- Biddable operator: starts preparation now and, in a separately authorized phase,
  starts measurement. The target answer key never enters either machine.
- External provider: causal HTTP interface with independently changing serving
  infrastructure and nondeterministic model responses. Receives one packet plus
  fixed instructions; returns response and metadata. No filesystem interface.
- Runner-owned lexical outputs: private, exclusively created attempt/result records.

### Frame split

Preparation is a transformation from fixed corpus/targets to frozen packets.
Execution is commanded measurement: one fresh request and an immutable record.
Response validation is a separate shape check, with no ground truth input.

### Requirements (per frame, with explicit out-of-scope)

Preparation must preserve all accepted schema values, exclude provisional records,
and freeze all 60 independently shuffled packets without exposing private keys.
Execution must give each model context only its arm's packet and fixed instruction,
record serving metadata, and preserve failures. Validation must accept exactly
three distinct packet IDs in their returned order. Retrieval during preparation,
scoring, anchor lookup, mapping, and classification are out of scope.

### Invariance test

Git objects and SHA-256 checks fix local inputs. Provider availability and serving
behavior cannot be frozen locally: request a documented model snapshot, preserve
returned metadata, and stop on incompatible responses. No determinism claim is
made for model outputs. Packet reproducibility does not depend on the provider.

### Stakeholder test

The stakeholder is an experiment operator requiring comparable independent
measurements. A stateful coding-agent session would import history and tools;
a single stateless HTTP request satisfies this experiment's explicit boundary.
No borrowed product-origin analogy is needed.

### Open questions — decided here, with reasoning

- Existing artifacts are never overwritten or reshuffled; verification is read-only.
- Defaults are offline. Only an explicit execution flag can send a request later.
- Malformed/refused/incomplete responses remain recorded, without format-repair
  prompts or retries that might selectively improve measurements.
- Transient HTTP/transport failures allow at most three identical attempts, with
  fixed delays; all attempts persist. A reserved run cannot be silently restarted.
- The local operator owns result retention. No results are published during runs.
- Public baseline files necessarily associate names and IDs. Isolation is enforced
  by the API payload and absence of tools, not by public-file obscurity.

### Carried forward

API access and live compatibility remain untested until authorized execution.
Private seeds/keys are required for full regeneration; public hashes suffice for
execution. This entry authorizes no measurement calls.

## Entry #2 — 2026-09-27 — Ontological-distance calibration

### Domains

- Existing lexical inputs: accepted five-field instruments and authored target
  problems. Read-only source corpus; copied case packets owned by this experiment.
- Biddable researcher: interprets disagreements and supplies later reference labels.
- External model service: variable judgments about ordinary practice, exposed via
  fresh Codex processes. Receives one packet and fixed instructions per invocation.
- Machine-owned lexical outputs: frozen prompts, raw runs, validated judgments,
  metrics, and review. No writes to retrieval artifacts or source instruments.

### Frame split

Preparation transforms source records and target descriptions into frozen packets.
Commanded measurement collects separate judgments; transformation computes
agreement. Research review interprets this evidence without automatic adjudication.

### Requirements (per frame, with explicit out-of-scope)

Every case must have two fresh independent contexts with identical case instructions.
Representation differences, naturalization, and uncertainty must remain explicit.
Evidence must be auditable without treating reference expectations as ground truth.
Retrieval, usefulness, schema redesign, and production filtering are out of scope.

### Invariance test

Hashes fix packets and instructions. Target-native practice and model behavior can
change and are not directly observed here. Reframe results as model reproducibility
on these packets, not proof of actual practitioner consensus. Record uncertainty
and the unavailable backend snapshot; preserve raw events for local audit.

### Stakeholder test

The researcher needs disagreements, not an automatically improved answer. Fresh
per-case processes suit that stakeholder; shared conversational memory would not.
No borrowed product or stakeholder analogy drives this design.

### Open questions — decided here, with reasoning

- Use 20 purposive cases, with both contrast directions, and identical A/B prompts.
- Freeze initial results before writing any reference label file. Agent-synthesized
  expectations must be labeled as such, never presented as collected human ratings.
- Invalid output stays invalid, without repair; incomplete data blocks completion.
- Same-model contexts test repeatability, not independent model-family validity.
- User explicitly authorizes live classification; no additional permission gate.

### Carried forward

Practitioner evidence, independent human ratings, and model-family replication are
future research questions. Stop after the report; add no numeric decision thresholds.
