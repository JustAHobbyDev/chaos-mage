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

## Entry #3 — 2026-09-27 — Boundary experiment with a second provider and matched controls

### Domains

Existing lexical inputs are the immutable v0.1 artifacts and accepted instrument
corpus. Experiment-owned lexical inputs are sixteen synthetic/control fixtures,
a tested draft, schemas, fixed order and preservation/preparation manifests.
External model services now comprise OpenAI through Codex and Anthropic through
Claude Code, with independently changing serving behavior and distinct runner
instructions. Each receives one isolated packet and schema; neither receives
operator labels, contrasts, other judgments or review. Existing subscription auth
is consumed by the CLIs; the machine never republishes credentials. Owned outputs
are private raw events, frozen judgments, metadata, metrics and research review.
The biddable researcher interprets evidence and explicitly retains uncertainty.

### Frame split

Preparation transforms accepted sources and authored targets into frozen packets.
Independent commanded measurement collects judgments through two isolated runners.
Research review transforms fixed evidence into agreement statistics and an argued
boundary recommendation. These remain the three frames of Entry #2.

### Requirements (per frame, with explicit out-of-scope)

Preparation preserves every v0.1 byte and source field, isolates changed evidence
in matched targets and freezes tested text before execution. Measurement must
collect 32 primary plus six original-prompt control judgments, with traceable
configuration, session and retry metadata. All prepared inputs must be committed
successfully before any calibration call. Review must distinguish exact class
resolution from side agreement, and reproducibility from scientific validity.
Production classification, distance scores and retrieval integration are excluded.

### Invariance test

Content hashes and Git objects stabilize local inputs. Neither provider's serving
snapshot, compute allocation nor practitioner consensus can be fixed by this
machine. Return unavailable served IDs as unavailable and preserve exposed model
fields with provenance. Equal high labels do not imply equal compute. Matched
controls reduce one ambiguity but a single observation per family/condition cannot
identify a causal prompt effect. The experiment is bounded evidence, not validation
of a universal taxonomy. Freeze all results before review.

### Stakeholder test

The stakeholder remains a researcher needing independent disagreements, not a
coding agent needing a repaired answer. Fresh processes and strict shape validation
serve that need; internal formatting retries are separately reported because they
can alter the measurement path. Existing stateful assistant sessions would violate
the boundary. No product analogy supplies a hidden stakeholder assumption.

### Open questions — decided here, with reasoning

- Alien requires both high reorganization and essential weak grounding; preserve
  low/moderate weak-grounding tensions for review instead of forcing labels.
- Preflight both adapters on non-calibration structured probes; safe mode preserves
  Claude subscription auth while disabling external context.
- One process at a time in frozen order, at most two permitted; 900-second timeout.
- Failures are preserved, scheduling stops, and amendments must precede any further
  scheduling. Missing results block completion rather than shrink denominators.
- Commit gate, unique sessions, exclusive reservations and no overwrites are enforced.
- Experimental snapshotting asserts what was tested, not scientific validity.

### Carried forward

Independent practitioner evidence and repeated observations remain limitations.
The user authorizes the specified live measurements and focused commits. No new
permission gate is needed. End with a recommendation in the completed report.

## Entry #4 — 2026-09-30 — Astra-only prospective transfer validity

### Domains

Existing lexical domains are the immutable Experiment E mappings, sixty historical
judgments, instruments, questions, fidelity exclusions, and historical experiments
including candidate qualifications. Read-only Git blobs and SHA-256 hashes identify
these. Experiment-owned lexical domains are extracted parent/atomic records,
opaque packets, schemas, randomized orders, exclusive reservations, raw execution
records, freezes and reviews. The external provider is independently changing and
nondeterministic; it receives one packet/schema and returns events and a response.
Subscription credentials remain provider-managed and never enter experiment artifacts.
The biddable human authorizes scope; the implementation agent records operator review,
which is not independent human evidence or another model measurement.

### Frame split

Historical-text transformation extracts explicit conditions and preserves spans and
provenance. Isolated commanded measurement obtains one Astra response per condition
and later one per mapping. Post-freeze review interprets immutable responses, first
against the prospective mapping/classifier, then against historical context. These
are distinct responsibilities with separately committed boundaries.

### Requirements (per frame, with explicit out-of-scope)

Extraction must preserve all explicit conditions without invented requirements or
labels, retaining duplicates as independently sourced statements. Measurement must
exclude historical status/identity/operator expectations from packets, forbid tools
and fallback, and preserve unsuccessful attempts without replacement. Review must
retain disagreements as annotations and distinguish conceptual usefulness from
unmeasured stability and cross-model robustness. Anti-collapse execution, generation,
E resumption, qualification, production integration and threshold changes are excluded.

### Invariance test

Hashes and Git commits fix lexical inputs and execution instructions. Provider behavior
and backend identity cannot be fixed; unavailable served identifiers remain null and
observed substitution stops scheduling. The research conclusion concerns these samples,
not a stable model capability or scientifically verified warrants.

### Stakeholder test

The research operator needs preserved disagreements, not repaired answers. The existing
CLI route serves that same experimental stakeholder. Fresh stateless calls fit it;
parent agent context and interactive tool access would violate the measurement boundary.
No product analogy or claim of candidate qualification is imported.

### Open questions — decided here, with reasoning

The supplied plan already authorizes these frames and calls. Atomic decomposition is
an operator textual decision, recorded with exact spans and full shared context; no
category is assigned during extraction. Overlapping historical sources remain separate.
Taxonomy may inform general classifier clarification after freeze, never case keys.
Semantic exclusion preserves domain wording such as “novelty effects.” Historical
outcomes are read for extraction: this is not operator blinding. Old/new comparison
is prohibited during prospective measurement. One artificial probe precedes each stage;
900-second sequential calls have exclusive reservations and no harness retries. Any
failure yields frozen partial evidence and an incomplete publication, not a reduced
successful denominator. Raw state belongs to this experiment and is retained privately.

### Carried forward

Astra is the historically accepted research judge, not a newly qualified candidate.
Within-model stability and cross-model robustness remain unmeasured. A single-model
eligible count cannot satisfy E's dual-family admission rule. Experiment E remains stopped.
