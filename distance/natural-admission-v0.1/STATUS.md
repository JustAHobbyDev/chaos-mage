# H.6 status — terminal and incomplete

Astra capacity failure stopped warrant measurement. There were 18 parsed generations,
18 frozen atom inventories (1,042 claims), 736 valid claim judgments and one failed
provider observation. One reservation was canceled before launch; 304 claims were
never reserved. No retry, substitution, ablation or downstream judgment occurred.

The authoritative outcome is TERMINATED_MEASUREMENT. The original terminal and later
cancellation state records are both preserved, followed by an additive terminal
adjudication. The frozen runner cannot automatically resume this run.

See [the incomplete report](../review/natural-admission-v0.1.md),
[partial freeze](claim-judgments-partial-freeze.json), and
[terminal incident](review/terminal-incident.json).

Read-only verification:

```sh
python -B distance/natural-admission-v0.1/partial_publication.py verify
```

Any future recovery study requires separate explicit authorization and a prospective
protocol. This publication does not authorize retrying or changing frozen observations.
