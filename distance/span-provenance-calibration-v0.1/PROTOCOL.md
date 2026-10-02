# H.5 — Neutral span provenance calibration v0.1

Base: `bdeeb973b794823a35257f472a020e12d816a8a9` (H.4).
Branch: `experiment-h5-span-provenance`. Push only this branch; never merge main.

This is engineering/instrumentation calibration, not a model-quality experiment.
Provider calls must be zero. Read the 18 H.4 cases and the two H.3 regression
mappings carried into H.4. Never rewrite their sources, judgments, raw responses,
validators, metrics, or published interpretations. Synthetic examples are allowed
only in isolated harness tests and never enter the 20-mapping corpus.

Freeze in order: architecture/contract; segmentation and schemas; all 20 span
tables; engineering fixtures; recorded semantic reviews and validator/tests;
calibration results and publication. Each freeze is a Git checkpoint. Later
checkpoints identify earlier SHAs. The final publication SHA is resolved with
`git log -1 --format=%H -- distance/span-provenance-calibration-v0.1/publication-manifest.json`.

The authoring gate checks source identity, segmentation reproducibility, fixture
structure, recorded review consistency, regressions, and historical preservation.
No acceptance percentage exists. Expected negative diagnostics are successful
test outcomes, not historical scientific failures. Unexpected errors block completion.
UNCERTAIN is retained and is not automatically fatal.

Semantic reviews are explicit Codex-authored engineering judgments with rationale.
They are neither fresh provider observations nor independent rater evidence. The
validator checks review binding/structure and replays these frozen records; it
does not establish semantic entailment. An absent review is unassessed, never
SUFFICIENT. Expectations cannot supply missing reviews.

Use ../../docs/EXPERIMENT-RECOVERY-POLICY.md (relative to distance's parent;
canonical repository path: docs/EXPERIMENT-RECOVERY-POLICY.md). Pre-freeze
engineering corrections are permitted. Post-freeze recovery preserves previous
bytes and checkpoints, documents dependencies, and establishes non-contamination
before proceeding. Historical experiments remain frozen regardless.

Stop after publication. No natural-output admission, Experiment E, viability
reruns, production integration, provider invocation, or execution of recommendations.
