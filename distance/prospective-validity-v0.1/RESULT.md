# Terminal state — incomplete

The historical-preservation failure stopped collection after one successful artificial
probe and four taxonomy judgments. No prospective stage ran. See the
[publication](../review/prospective-validity-v0.1.md), failure-freeze.json and
taxonomy-partial-freeze.json. Do not rerun any collection command.

The original frozen preparation includes an erroneous appended shared design log.
Historical bytes were restored; the executed version is archived under review/.
The original manifests remain unchanged. Consequently `runner.py verify` detects the
known path difference. The authoritative read-only terminal check is:

```sh
python -B distance/prospective-validity-v0.1/review/verify_incomplete.py
```

It verifies both the archived executed input and restored historical document, all
raw attempts, sequential launch/stop ordering, unique sessions, packet/schema hashes,
response bytes and reconstructed incomplete metrics. No repair-and-continue occurred.
