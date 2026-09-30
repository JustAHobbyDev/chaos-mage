# Gemini model-agnostic capability qualification v0.1

Candidate: Google Gemini 3.1 Pro Preview (`gemini-3.1-pro-preview`), explicit HIGH
thinking, 32768 maximum output tokens. Frozen twelve-case capability experiment;
[protocol](PROTOCOL.md), [unchanged contract](CAPABILITY-CONTRACT.md).

Lifecycle (run from repository root):

```sh
python -B -m unittest discover -s distance/model-qualification-gemini-v0.1/tests
python -B distance/model-qualification-gemini-v0.1/runner.py verify
python -B distance/model-qualification-gemini-v0.1/provider/gemini/credential-launch.py preflight
# Commit successful preflight before run.
python -B distance/model-qualification-gemini-v0.1/provider/gemini/credential-launch.py run
python -B distance/model-qualification-gemini-v0.1/runner.py freeze
# Commit full results before any independent semantic assessment / historical review.
```

Reservations and freezes are exclusive/write-once. These commands are not a rerun
recipe for a completed experiment. On failure, use `freeze-failure`, publish partial
evidence as inconclusive, and stop; do not retry or change configuration.
Historical verification reports must be written here, never into frozen experiments.
