# Experiment B — fixed-baseline displacement v0.3

Authorized by [the supplied plan](../../docs/PLAN-displacement-v0.3.md).
Eight baseline hypotheses were committed before selecting 24 core mappings and two
evidence-only variants. Operator intentions are design coverage, never ground truth.
The immutable historical experiments and full-transfer schema remain unchanged.

Execution configuration copies A exactly. The scheduler order uses seed 20260928
for validity and 20260929 for admitted displacement, after neutral ID shuffle with
20260927. The unchanged validity classifier sees only case ID, source, target and
mapping. Displacement receives the fixed baseline bytes and provisional marker;
only provisional packets additionally receive exact instantiation conditions.
The admission review must classify every condition and cannot rewrite a candidate.
All provider sessions are fresh, sequential, empty-directory, tool-disabled processes
with a 900-second timeout. Raw output, commands, timestamps, exposed model metadata
and formatter retries are retained. Unavailable served model identifiers remain null.
Every launch checks committed inputs and prerequisite freezes. Any failure stops the
schedule, preserving planned denominators. Recovery and substitutions need explicit
authorization. Do not delete a reservation or create replacement cases.

Checkpoints:
1. `Freeze Experiment B target-native baselines` before mapping authorship.
2. `Prepare ontological displacement Experiment B` before any provider call.
3. Artificial probes for both families and stages; commit their evidence before runs.
4. Freeze/publish all 52 validity responses before admission review.
5. `Freeze Experiment B displacement admission` before displacement calls.
6. Freeze/publish all admitted responses before qualitative review; completion and push.

```sh
python -B -m unittest discover -s distance/displacement-v0.3 -p 'test_*.py'
python -B distance/displacement-v0.3/runner.py prepare
# Commit preparation.
python -B distance/displacement-v0.3/runner.py preflight
# Commit preflight.json.
python -B distance/displacement-v0.3/runner.py run --stage validity
python -B distance/displacement-v0.3/runner.py freeze --stage validity
python -B distance/displacement-v0.3/runner.py publish --stage validity
# Review all cases in admission-review.json only after validity-freeze.json exists.
python -B distance/displacement-v0.3/runner.py admit
# Commit admission. If viability fails, publish inconclusive admission; no calls.
python -B distance/displacement-v0.3/runner.py run --stage displacement
python -B distance/displacement-v0.3/runner.py freeze --stage displacement
python -B distance/displacement-v0.3/runner.py publish --stage displacement
python -B distance/displacement-v0.3/runner.py analyze
python -B distance/displacement-v0.3/runner.py verify-results --private
```

The separate output contract rejects extra fields, Alien, grounding, aggregates,
non-integer dimension values and invalid boundary alternatives. Both wire schemas
remove only schema metadata and allOf; full local semantic validation still applies.
Native/Adjacent/Remote class is qualitative, with no vector-to-class rule. Metrics
separate primary/provisional and report both all-admitted and core-only denominators.
Every same-target unordered pair retains ties. No agreement target or adjudication.

Post-result review precedence is contested (class disagreement), then boundary
(any borderline), then consensus. Review every admitted pair and all design
contrasts, including disciplinary-distance shortcuts in both directions, vocabulary,
evidence availability redefining practice, mechanical counting and grounding
contamination. Assess usefulness through distinguishable regions, explicit epistemic
changes, baseline stability and coherent ordering, not agreement alone.
