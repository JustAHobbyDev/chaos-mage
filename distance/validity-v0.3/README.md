# Transfer-validity calibration v0.3 — execution

This is the execution successor to the unchanged [preparation snapshot](../v0.3/README.md).
[EXECUTION.md](EXECUTION.md) records authorization, the explicit transition from
preparation-only status, isolation settings, schema projection and failure policy.
The frozen [protocol](../v0.3/PROTOCOL-transfer-validity-v0.3.md) supplies the design.

Commands below are version-specific and exclusive: live execution/publication are
not rerunnable over an existing reservation or result. Never delete a failed run.

```sh
python -B -m unittest discover -s distance/validity-v0.3 -p 'test_*.py'
python -B distance/validity-v0.3/runner.py validate
python -B distance/validity-v0.3/runner.py preflight --attempt initial
python -B distance/validity-v0.3/runner.py prepare
# Successfully commit every prepared input before the following live command.
python -B distance/validity-v0.3/runner.py run
python -B distance/validity-v0.3/runner.py freeze-results
python -B distance/validity-v0.3/runner.py publish
python -B distance/validity-v0.3/runner.py analyze
python -B distance/validity-v0.3/runner.py verify-results --private
```

If measurement stops, use `freeze-failure` and report the incomplete fixed-denominator
study; no continuation is implemented. A documented amendment must precede any
future continuation. An Invalid transfer is a legitimate judgment, distinct from
a failed response or execution. Analysis uses original published responses only.

Preserve this prepared README and runner after the execution freeze. Put outcomes
and any post-freeze review tools in separate result/review artifacts. No automatic
launch of later experiments is included.
