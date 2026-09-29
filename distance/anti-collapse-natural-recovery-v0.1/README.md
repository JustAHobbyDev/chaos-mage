# Experiment E recovery — prepared, execution paused

See [AMENDMENT.md](AMENDMENT.md) for authority, preserved evidence and remaining work.
No new provider probes or measurements have been run. The original incomplete
[report](../review/anti-collapse-natural-v0.1.md) remains unchanged.

`runner.py` imports the frozen Experiment E implementation and adds an explicitly
separate recovery context. It reuses the original classifier, schemas, prompts,
packet construction, isolation flags, event audit and metric formulas. Imports keep
response bytes and execution provenance. `preservation.json` covers previously
tracked files and raw runtime artifacts; `prepared.json` binds recovery inputs/code.

Offline commands, from the repository root:

```bash
mise exec -- codex --version
python -B distance/anti-collapse-natural-recovery-v0.1/runner.py binaries
python -B distance/anti-collapse-natural-recovery-v0.1/runner.py verify --private
python -B -m unittest discover -s distance/anti-collapse-natural-recovery-v0.1/tests
python -B distance/anti-collapse-natural-v0.1/review/verify_incomplete.py --private
```

The `binaries` command runs only `--version`, not a model request. The recovery
execution configuration also uses absolute version-specific paths so project mise
discovery is unnecessary inside isolated model working directories.

When the user explicitly resumes, record their instruction in
`execution-authorization.json` with `resume_provider_calls: true`, the current
`prepared_sha256`, and an ISO 8601 `recorded_at` timestamp after preparation; commit
it before probes. Never create this file merely because it is described here.
Then run `preflight --stage neutralization`, commit the two probe results, and
`run --stage neutralization`. Freeze and commit before preparing the next stage.
The same sequence applies to audit, validity and, if admission is viable,
anti-collapse. See the amendment for attrition and stopping rules.

There is deliberately no recovery generation command. `preflight`, `run`, and the
underlying execution function all refuse provider calls while authorization is absent.
Future failures require a new recorded recovery decision; the original STOP remains
untouched throughout.
