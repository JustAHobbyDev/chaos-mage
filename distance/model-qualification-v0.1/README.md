# Model-agnostic capability qualification v0.1

Frozen twelve-case diagnostic qualification of Muse Spark 1.3 Contributor.
See [protocol](PROTOCOL.md), [contract](CAPABILITY-CONTRACT.md),
[manifest](manifest.json), and [final review](../review/model-qualification-v0.1.md).

Lifecycle: freeze principle → freeze inputs/adapter → catalog and artificial
preflight → commit successful probes → twelve isolated judgments → commit results
→ post-freeze historical context and capability review → ordinary push.

Runner actions: `verify`, `catalog`, `preflight`, `run`, `freeze`, `freeze-failure`,
`metrics`, `audit`. Failures stop scheduling; there is no automatic recovery action.
Use `python -B runner.py ACTION` from any directory. Tests run with
`python -B -m unittest discover -s distance/model-qualification-v0.1/tests` at root.
