# Transfer-validity calibration v0.3 — execution supplement

2026-09-27. The user's subsequent **“run”** authorizes Experiment A, including
runner preparation, non-calibration preflight, 48 judgments, freezing and review.
It does not authorize experiments B/C, retrieval integration or new case construction.

This explicitly supersedes the **operational** preparation-only stop at commit
`7b1aad2f12080031d46a5619cdc49ea14380e365`. The `distance/v0.3/` directory remains
an immutable historical preparation snapshot. All live experiment artifacts are
in this sibling `distance/validity-v0.3/`; private attempts use
`.runtime/validity-v0.3/`. Historical preparation tests continue to describe that
snapshot, not the effective execution status of this successor. No old absence
check or historical artifact is edited or disabled.

The [frozen protocol](../v0.3/PROTOCOL-transfer-validity-v0.3.md), its 24 packets,
classifier instructions, order, canonical contracts and definitions remain unchanged.
This supplement adds execution settings and provenance, not new substantive
classifier instructions. Model and provider configuration are in execution-config.json.
A = OpenAI gpt-6-astra/high; B = Anthropic claude-fable-5-1[1m]/high. These are
requested aliases, not verified immutable backend snapshots. Availability and
isolation must be demonstrated by fresh probes. Equal effort labels do not imply
equal compute.

## Structured output

The canonical validity schema includes cross-field allOf/if/then constraints.
The shared wire projection removes only $schema, $id and allOf entries recursively;
it preserves all response fields, required fields, enums, types, null alternatives,
nonblank checks and strict object boundaries. Both families receive that same
projection. All judgments must then pass the unchanged canonical schema and
candidate identity checks. No normalization, repair, coercion or relabeling occurs.
The frozen classifier already states the cross-field rules explicitly.

Preflight uses the wire schema with an explicitly specified artificial response
(case_id = PREFLIGHT, no source/target calibration case), verifying formatting,
canonical Valid/false-reframe structure, live authentication, requested model
acceptance and event isolation. Preflight responses are not observations. Every
attempt is retained; a failed preflight requires diagnosis before a new named
preflight attempt. Successful probes do not demonstrate classifier reliability.

## Isolation and execution

Installed CLI help and live preflight verify command support. Codex uses ephemeral
read-only sessions, ignores user config/rules and project docs, and disables tools,
apps, plugins, memory, browser/computer/image features, hooks and delegation. Claude
uses safe mode, empty setting sources/MCP/tool configuration, explicit built-in
plugin exclusions, disabled hooks/memory/connectors/skills and no session persistence.
Only native StructuredOutput formatting machinery is allowed for Claude.

Each process receives an empty temporary working directory, one allowlisted packet,
and the output schema. Provider/model environment overrides and parent-session
markers are stripped. Authentication remains with each CLI's existing subscription
configuration; no credentials are retrieved or copied into experiment records.
Native runner system instructions and unexposed backend behavior remain limits.

Execution is sequential in the original 48-entry order, 900 seconds per process.
Exclusive experiment/run reservations reject concurrent schedulers and repeats.
Prepared files, prompt hashes and CLI versions are checked against the committed
preparation before measurement and on each subsequent launch. Exact outputs and
all exposed retries are preserved privately. Raw returned responses are saved even
when canonical validation fails. Failed run status is distinct from an Invalid
transfer judgment. Any run failure stops scheduling and is preserved; continuation
requires a separately recorded amendment, never a silent retry or replacement.

Freeze all responses and audit metadata before content review. Incomplete runs
produce a failure freeze and fixed-denominator status report, not a successful
reliability result. Full successful runs publish byte-identical responses, calculate
only preregistered validity/criterion/reframe summaries, and review every contrast,
disagreement and concordant pair. Author intent is not ground truth. No subsequent
experiment is automatically launched.

## References and local evidence

- [Official Codex non-interactive documentation](https://learn.chatgpt.com/docs/non-interactive-mode)
  documents structured final responses and machine-readable events.
- [Official Codex CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
  describes execution options; installed `codex exec --help` is the version-specific
  authority for the flags actually used.
- Installed `claude --help` and fresh audited init events establish Claude's flags
  and enabled capabilities. Historical safe-mode/authentication incident
  PC-20260927-05 motivates explicit exclusions and live probes, not an assumption
  that configured authentication proves availability.

No existing credential, SSH, extraction, retrieval or historical experiment state
is changed. The prior boundary harness's pure event-audit routine is reused by
reference; its bytes are included in this execution freeze.
