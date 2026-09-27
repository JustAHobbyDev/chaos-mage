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

## Entry #4 — 2026-09-27 — Transfer validity, displacement and grounding v0.3

### Domains

Existing lexical domains are the frozen v0.1/v0.2 records and accepted instrument
corpus, read only. New owned lexical artifacts are model definitions, strict
contracts, retrospective analytical examples and future calibration packets.
The researcher authors mappings and baselines and interprets unresolved tensions.
Independent target practice exists outside these records; packet evidence does
not establish what practitioners ordinarily do. Future model providers remain
external, variable services; this handoff sends them no requests.

### Frame split

Offline transformation creates a new representation from preserved research evidence.
Simple workpieces support authored candidate mappings, explicit conditions and
baseline scopes. A separate future commanded-measurement frame will collect
validity judgments; its protocol is prepared here but not executed.

### Requirements (per frame, with explicit out-of-scope)

The representation must distinguish fidelity failures from displacement and grounding,
preserve original questions and stop downstream classification on Invalid transfers.
Historical evidence remains byte-identical. Retrospectives identify their analytical
origin. Future judges receive identical explicit mappings without author intent or
history. Retrieval policy, composite scores, usefulness/creativity optimization and
Chaos Magick Engine integration are excluded. No model calls, including preflight.

### Invariance test

Frozen bytes and explicit mappings are observable and stable. Ordinary practice,
provider behavior and empirical counterparts remain independently variable; express
them as scoped assumptions or uncertainty, not verified facts. Grounding is neither
implied by operational coherence nor a distance dimension. Reliability is untested.

### Stakeholder test

The researcher needs inspectable distinctions and preserved failures, not repaired
answers. A fixed mapping removes the prior transfer-construction confound. No
borrowed product analogy drives the design. Fresh future judge contexts serve
measurement, while historical examples remain explicitly author-informed analysis.

### Open questions — decided here, with reasoning

- User selected all 24 blinded packets now, with no execution runner or provider calls.
- User selected documented evidence review for advancement, not an arbitrary cutoff.
- Any failed validity criterion dominates conditional ones; unresolved conditions
  cannot rescue a known unsupported inference or silently substitute a target.
- Required nulls make stopped/withheld downstream judgments explicit. Provisional
  flags track conditional validity, not scientific validation of the model.
- Freeze contracts before retrospective authoring; disclose any later amendment.
- Preserve all 155 pre-existing distance files, including the protected README;
  add the active-model link to the root README instead.

### Carried forward

Weak speculative ontology versus unresolved operational warrant, partial answers
versus question drift, essential-role granularity, and evidence for practitioner
baselines remain research tensions. Later measurement needs its own authorization,
provider preflight, committed configuration and result freeze.
