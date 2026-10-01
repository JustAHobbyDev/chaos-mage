# Experiment H.1 — fault-localized calibration v0.2

**Stopped before measurement; the experiment is incomplete.** All four revised
CORE candidates retain source-derived material answers after central-claim deletion.
No provider observations, final cases, controls, or provider packets were produced.

The revised drafts satisfy focal-ownership and length-balance checks, but fail the
mandatory semantic construction gate. This is not an Astra result or a rubric failure.

- [Full report](../review/fault-localized-calibration-v0.2.md)
- [Protocol](PROTOCOL.md) and [targets frozen before variants](targets.json)
- [Exact deletion audits](review/authoring-audit.json)
- [Metrics with explicit unmeasured outcomes](metrics.json)

Verify the preserved stopped state from the repository root:

```sh
python -B distance/fault-localized-calibration-v0.2/publication.py verify
python -B -m unittest discover -s distance/fault-localized-calibration-v0.2/tests -p 'test_*.py'
```

`runner.py measurement-gate` intentionally rejects this corpus. Files under
`authoring-attempts/` are rejected drafts, not frozen final measurement cases. No
provider execution path was activated. H scoring/contracts/schemas are byte-identical.
Historical H/G/F and other inherited evidence remain unchanged.
