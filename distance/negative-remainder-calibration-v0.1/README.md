# Experiment H.3 — Productive Negative Remainder Calibration v0.1

**Measurement complete; productivity separates the authored boundary, while full
negative-role calibration remains incomplete.** All five insufficiency-only artifacts
are CORE_INVALID. All ten intended productive artifacts retain viable contributions.
Two diagnostic inquiry directives are productive but were classified as nonnegative,
so the schema allowed their negative-role assessments to be omitted.

- [Full report and checkpoint SHAs](../review/negative-remainder-calibration-v0.1.md)
- [Frozen productivity rule](PRODUCTIVITY.md) and [protocol](PROTOCOL.md)
- [Post-freeze operator audit](review/operator.json)
- [All five discriminating inquiries](review/inquiry-contributions.json)
- [Derived metrics](metrics.json)
- [Additive engineering recovery evidence](recovery/evidence.json)

Counts: 12 primary cases, 3 controls, 40 claim judgments and 15 artifact judgments,
all in distinct fresh GPT-6 Astra/high contexts. Claims: 21 SUPPORTED, 19 UNSUPPORTED.
Artifacts: 1 KEEP_WITH_WARRANT_FLAGS, 9 KEEP_WITH_REDUCED_SCOPE, 5 CORE_INVALID,
0 UNCERTAIN_LOAD_BEARING.

Across all 21 candidates, productivity is YES=10, NO=11, UNCERTAIN=0. The 19 candidates
classified as negative have TARGET_CONSTRAINT=5, INQUIRY_CONSTRAINT=3,
INSUFFICIENCY_ONLY=11, UNCERTAIN=0; their productivity is YES=8, NO=11, UNCERTAIN=0.
Two productive affirmative directives have no negative role. These missing roles are
design/instrument coverage problems, not recoded UNCERTAIN responses. The operator
identified no judge-productivity errors and one plausible stopping/scope alternative.

One inherited validator rejected an inactive diagnostic flag permitted by the schema.
The original stop, failed validation and response remain unchanged. An additive
adapter removed only that inapplicable check, with hash-bound proof and a complete
recovery preflight. No scientific output was rewritten or request repeated. The
supplementary verifier is necessary for the preserved original representation:

```sh
python -B distance/negative-remainder-calibration-v0.1/runner.py verify
python -B distance/negative-remainder-calibration-v0.1/recovery.py verify
python -B -m unittest discover -s distance/negative-remainder-calibration-v0.1/tests -p 'test_*.py'
python -B -m unittest discover -s distance/negative-remainder-calibration-v0.1/recovery/tests -p 'test_*.py'
```

Historical experiments remain byte-preserved at the exact H.2 base
e35948a601fefabb648218cde728aa7fdc1651d2. Publication is restricted to
experiment-h3-negative-remainders. No main merge, production integration, Experiment E
continuation or natural-output admission experiment occurred. The recommended narrow
inquiry-role follow-up was not executed. Provider execution is sealed by the final
runtime freeze.
