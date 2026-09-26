# Retrieval benchmark v0.1

Ten frozen target problems for the preregistered cross-domain retrieval and
mapping experiment. This release constructs the benchmark only; retrieval,
baseline runs, mapping, mapping adjudication, scoring, and final classification
have not been performed.

## Frozen references

- Protocol: [retrieval-mapping-test-v0.1.md](../../docs/retrieval-mapping-test-v0.1.md)
- Preregistration commit: `c0daa4ef06f7c077d87e7e3232a72fefabac7308`
- Instrument corpus snapshot: `9a5bc7e626d1e5f27d6ecec224f70dbc08a6a3a2`

The source records were read directly with `git show` at the corpus snapshot.
The five schema values were copied verbatim as parsed YAML strings, including
any terminology already present in those frozen values. No schema fields,
source records, candidate eligibility decisions, or protocol documents changed.

## Construction and isolation

The coordinator assigned the ten preregistered anchors to ten distinct remote
target-domain families. The assignment list was privately shuffled before
numbering the opaque target IDs, so numbering does not preserve the protocol's
anchor order. The private assignments were frozen and hashed before the first
author session began. This was an arbitrary construction assignment, not an
experimental randomization claim.

Each author received one YAML packet containing exactly `target_id`,
`target_domain`, `instrument` with the five frozen fields, and the eight
target-writing instructions from the construction brief. Packets excluded
extraction metadata, filenames, source references, other instruments, and the
answer key. The coordinator did not write the narratives.

Authors ran in separate, fresh `codex exec` subprocesses, each in a newly created
temporary directory outside the repository. No session was resumed or forked.
Construction used Codex CLI 0.157.0 with its default model selection; no model
or sampling override was supplied. The runner did not capture a resolved model
identifier or provider serving version, so those are not asserted here.
The launcher used `--no-daemon`, `--ephemeral`, `--ignore-user-config`,
`--ignore-rules`, `--skip-git-repo-check`, and a read-only sandbox. Project
instruction loading was disabled with `project_doc_max_bytes=0`; automatic
skill instructions and host skill discovery were disabled. Memories, plugins,
apps, agent delegation, shell execution, browsing, image tools, hooks, and code
execution were disabled. A neutral model instruction requested a response using
only the supplied text and prohibited tool calls. The author packet was the
entire task input through standard input. Parent-thread environment identifiers
were removed; no parent conversation was supplied.

Local event records were checked for distinct fresh thread IDs, successful
completion, and absence of tool calls. Generic CLI role/environment messages
were not experimental data. This separation withholds source identities and
other cases from the author context; it does not claim that a model cannot
recognize a mechanism from its permitted frozen fields or pretrained knowledge.

## Lexical audit and freezing

A separate fresh subprocess audited each completed narrative. Its packet
contained only that narrative, the hidden anchor name and source practice,
relevant source-domain terminology, and lexical-audit instructions. It did not
receive other targets, the candidate pool, author reasoning, or retrieval
results.

Auditors checked only lexical or source-domain imagery leakage. They were
explicitly prohibited from judging structural quality, solution fit, likely
retrieval performance, or alternate-instrument applicability. Structural
similarity and ordinary vocabulary required by the target domain were not
leakage by themselves. Detailed audit records remain private because their
reasoning can disclose source identities.

Each published narrative is the author's output, with surrounding whitespace
normalized, and is byte-matched to the narrative in its passing audit packet.
It was frozen after that audit. Public front matter contains only its opaque
ID, target domain, and frozen status. The manifest records public audit status
and narrative word counts. Words are counted by splitting the narrative on
whitespace; YAML front matter is excluded. Each narrative must contain
120–250 words.

All ten targets passed their first lexical audit. No narrative rewrites were
needed. The final narrative range is 202–236 words.

## Private construction records

The hidden answer key is stored locally at
`.runtime/retrieval-v0.1/answer-key.yaml`. The repository ignores `.runtime/`.
The key, author packets, session inputs and outputs, detailed audits, assignment
freeze record, and validation evidence are not tracked or committed. Preserve
these local materials for later scoring and construction review. The public
repository alone intentionally cannot reconstruct the assignments.

The answer key will remain withheld until retrieval and mapping judging are
complete. Later experiment execution requires new appropriately isolated
contexts; the construction coordinator and lexical auditors have seen hidden
information.

## Deviations and limits

No preregistered rules were changed. The construction record reports lexical
audit outcomes only; they do not certify structural quality or retrieval
performance. No candidate anonymization or subsequent experiment phase is part
of this release.
