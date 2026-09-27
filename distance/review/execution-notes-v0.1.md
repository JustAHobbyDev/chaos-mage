# Execution notes v0.1

## 2026-09-27 — First launch preceded Git commit by 11 seconds

All inputs had been written and SHA-256 frozen before any invocation. The initial
Git staging/commit command failed because sandboxed Git metadata was read-only.
The next tool call nevertheless launched CASE-001/A at 11:56:28 UTC. Retrying Git
with the available escalation mechanism committed those same frozen bytes in
`4a0be79` at 11:56:39 UTC. No response had arrived or been inspected at commit time.

This deviates from the protocol's commit-before-execution sequence, not its
freeze-before-execution or identical-prompt requirements. Keep the first run;
do not rerun it or change frozen inputs. Report this sequence transparently.
