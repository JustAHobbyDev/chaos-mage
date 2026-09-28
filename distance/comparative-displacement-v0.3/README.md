# Comparative displacement v0.3 — Experiment B.1

See PROTOCOL.md for the frozen design and CLASSIFIER.md for judge instructions.
The pair is the measurement unit: one fixed task and baseline, two admitted mappings.
There are 28 planned conceptual pairs and six secondary orientation controls.
Mappings retain their original evidence contexts; this is not a controlled shared
evidence-state experiment. No grounding or retrieval integration is authorized here.

Commands (from repository root, with python -B):

    runner.py prepare
    runner.py verify
    runner.py preflight
    runner.py run --stage validity
    runner.py freeze --stage validity
    runner.py publish --stage validity
    runner.py admit
    runner.py run --stage comparison
    runner.py freeze --stage comparison
    runner.py publish --stage comparison
    runner.py analyze
    runner.py verify-results --private
    verify_completion.py --private

Prefix runner.py with distance/comparative-displacement-v0.3/. Commit between stages
exactly as PROTOCOL.md requires. Commands that collect or freeze write exclusively.
Verification is read-only. Failed runs stop scheduling; freeze-failure preserves
failure evidence without retry. Public judgments are unchanged returned payloads.
