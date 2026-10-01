# Experiment H completed

See the [final report](../review/fault-localized-calibration-v0.1.md) and
[metrics](metrics.json). Final verification:

```bash
python -B distance/fault-localized-calibration-v0.1/publication.py verify
```

91 claim judgments: 64 SUPPORTED, 27 UNSUPPORTED, no conditional or uncertain
claims. All 24 cases received simultaneous-deletion ablations in fresh sessions:
8 KEEP_WITH_WARRANT_FLAGS, 7 KEEP_WITH_REDUCED_SCOPE, 9 CORE_INVALID, no
UNCERTAIN_LOAD_BEARING. Total: 115 observations, 115 unique sessions, no resampling.

All six primary triples show structural separation. The operator audit records
23 structurally concordant cases and one metadata-only hidden-graph omission.
There is no independent-rater evidence. Four step-response cases retain an explicit
numerical-precision reservation. Shared template-transfer defects, focal ownership
cues and primary deletion-length differences limit broader calibration claims.

The original failed historical-test preflight is preserved, along with its
non-contaminating adapter. A daemon restart interrupted the scheduler during the
fourth ablation; the original child completed and its response survived unchanged.
The missing exit code remains unavailable. Recovery resumed only unreserved cases
after a committed 44-check preflight. The final runtime inventory is frozen.

All G/F and earlier tracked/runtime artifacts remain unchanged. No new instrument,
natural-output experiment, E resumption, production integration or recommended
follow-on study was executed. Stop after H.
