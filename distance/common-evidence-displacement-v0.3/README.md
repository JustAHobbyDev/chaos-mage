# Experiment B.2 — common-evidence comparative displacement

Research only. Shared-world authorship, independent validity admission, prospective
comparison, then consequence comparison. See PROTOCOL.md and CLASSIFIER.md.
Historical experiments are frozen. No grounding C or retrieval work is authorized.

Prefix these commands with `python -B distance/common-evidence-displacement-v0.3/`:

    runner.py validate
    runner.py prepare
    runner.py verify
    runner.py preflight
    runner.py run --stage validity
    runner.py freeze --stage validity
    runner.py publish --stage validity
    runner.py admit
    runner.py run --stage prospective
    runner.py freeze --stage prospective
    runner.py publish --stage prospective
    runner.py run --stage consequence
    runner.py freeze --stage consequence
    runner.py publish --stage consequence
    runner.py analyze
    runner.py verify-results --private
    verify_completion.py --private

Commit at every checkpoint specified in PROTOCOL.md. Preparation/collection/freeze
commands write exclusively and must not be rerun over existing artifacts.
Verification commands are read-only. On failure use `runner.py freeze-failure` to
retain evidence; do not resume without explicit recorded authorization.

Worlds and common states were authored and committed before mappings. `derive.py`
replays the frozen operations; it does not read any provider judgment. Judge packets
contain only allowlisted observable content. The `review/` files interpret results
after both stages freeze; they never overwrite judgments.
