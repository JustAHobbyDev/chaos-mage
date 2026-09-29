# Family-B instrument bridge v0.1

Twelve prescribed frozen cases; twelve fresh judgments per provider. See PROTOCOL.md
for the scope, review taxonomy and stopping rules; manifest.json records exact provenance.
The user authorized this bridge through publication and ordinary push, ending before F.

Commands from the repository root:

```bash
python -B -m unittest discover -s distance/family-b-bridge-v0.1/tests
python -B distance/family-b-bridge-v0.1/runner.py verify
python -B distance/family-b-bridge-v0.1/runner.py catalog
python -B distance/family-b-bridge-v0.1/runner.py preflight
# Commit successful preflight/freeze.json and provider/catalog.json before run.
python -B distance/family-b-bridge-v0.1/runner.py run
python -B distance/family-b-bridge-v0.1/runner.py freeze
# Commit all fresh results before metrics or any qualitative comparison.
python -B distance/family-b-bridge-v0.1/runner.py metrics
```

Each command reserves exclusive artifacts. Do not rerun provider commands or delete
reservations. On failure, use `freeze-failure`, report inconclusive and stop; only new
explicit recorded authorization permits recovery. Never substitute historical responses.
Credentials enter from META_API_KEY or the bws-4-agents launcher and never enter artifacts.
Raw transport evidence remains in the ignored `.runtime/family-b-bridge-v0.1` directory;
freeze manifests hash it. Validated judgments and non-secret provenance are published.
