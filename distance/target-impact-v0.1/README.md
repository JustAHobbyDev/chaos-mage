# H8 target impact v0.1

Bounded target-facing experiment from exact H7 commit
`c62b622b69ed900b9debcc9e41e133536287be59`. See [PROTOCOL.md](PROTOCOL.md).

`prepare.py` builds offline immutable inputs. `runner.py` implements verify,
preflight, run, publish, comparisons, unblind and aggregate. Preflight is a live
account read, not a model call; run requires a committed checkpoint and a fresh
review file under `.runtime/target-impact-v0.1/`. No automatic retries or recovery.

Offline tests: `python -B -m unittest discover -s distance/target-impact-v0.1/tests`.
Account records stay ignored. Raw scientific observations and their hashes are
retained here. Final findings: [report](../review/target-impact-v0.1.md).
