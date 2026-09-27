# Execution preflight — v0.3 validity

2026-09-27. One named attempt (`initial`), both families successful. These are
artificial formatting probes with no calibration source, target or candidate.
No calibration judgment was requested before successful preparation commit.

- Installed Codex CLI: 0.157.0; requested gpt-6-astra, high reasoning.
- Installed Claude Code: 2.1.282; requested claude-fable-5-1[1m], high effort.
- Installed help confirmed all invoked isolation/output flags. The substantive
  provider command construction follows the previously audited boundary runner.
- Both probes returned the specified validity-format fixture and passed the
  unchanged canonical schema. The wire projection retained fields/enums and removed
  only schema metadata and cross-field allOf, as documented in EXECUTION.md.
- Codex events showed a fresh thread and no tool activity. No returned model
  identifier was exposed; the requested alias is not a verified served snapshot.
- Claude init showed only StructuredOutput, no plugins, MCP servers, skills or
  slash commands, with high effort active. Returned identifiers consistently named
  claude-fable-5-1. These are exposed identifiers, not immutable verified snapshots.
- No visible transport retries or formatter retries occurred in either probe.
  Codex does not expose a comparable formatter-call counter, so absence of visible
  retry evidence is not proof of absence of hidden retries.
- Both CLIs used existing subscription authentication. No credentials were fetched,
  displayed or copied. Filesystem escalation allowed normal CLI account-state
  access; it did not grant model tools or repository context.

`preflight.json` records the audit metadata and hashes of private prompts, responses,
events, stderr, reservations and validation files. Private data remains in the
ignored runtime directory. Tests use mocked subprocesses and synthetic responses;
their deliberately failed status output is not a failed provider judgment.
