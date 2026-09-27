# Adapter preflight observations

2026-09-27, before configuration freeze or calibration.

Initial non-calibration Codex probe passed (codex-cli 0.157.0).
Initial Claude probe failed (Claude Code 2.1.282): the service reported HTTP 401,
OAuth access token expired. No calibration prompt was sent. `auth status` indicated
an account was configured but did not establish that its access token was usable.
The operator was asked to sign in again. Failed raw events remain private under
`.runtime/boundary-v0.2/preflight/B/`; they are never overwritten.

The failed probe's init event also listed agents-md and telemetry built-in plugins
despite safe mode. Before freezing configuration, add explicit disabled entries
for these built-ins and verify the next init event has no plugins. Safe mode alone
disables customizations but, per local --help, built-in plugins work normally.
Account connectors and skill/plugin synchronization are explicitly disabled too.

A fresh `preflight --attempt <unique-alphanumeric-name>` preserves previous
attempts. It must pass for both families before preparation and commitment. This
is adapter preparation, not a rerun of a calibration measurement. No protocol
amendment to a frozen calibration configuration has yet occurred.

The operator confirmed renewed authentication. Fresh `authrefresh` probes passed
for both adapters. Claude init reported no plugins, skills, slash commands or MCP
servers and only the StructuredOutput formatting tool. It returned model identifier
`claude-fable-5-1` in init, assistant message and result modelUsage metadata; the
requested context suffix remains recorded separately. Codex did not expose a served
model identifier in its event stream. Neither interface establishes a verified
immutable backend snapshot. CLI versions were codex-cli 0.157.0 and Claude Code
2.1.282. The second probe ran with approved filesystem escalation so the CLI could
use/refresh subscription state outside the workspace; operator reauthentication
also occurred, so recovery cannot be attributed solely to escalation.

Successful Claude probe: one StructuredOutput call, no observed formatting retry.
Both original and successful probe raw artifacts are retained and hashed in
preflight.json. The successful configuration explicitly disables the built-ins;
that configuration is the one to freeze and use for calibration.
