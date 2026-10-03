# Post-freeze operator audit

Run `runner.py metrics` only after the evaluation and aggregation freezes are
committed. It first creates review/dependency-audit-template.json. Complete a separate
review/dependency-audit.json from preserved outputs, never by modifying judgments.
Match each expected embedded subject to discovered dependency IDs semantically, with
an explicit rationale; string equality is insufficient for paraphrases. An omitted
obligation stays omitted. No expected verdict is inserted into aggregation.

Each claim requires explicit PRESENT/ABSENT/UNMEASURED findings with evidence for:
OBLIGATION_OMISSION (including content beyond minimum hypotheses), OVERTRIGGER,
WRONG_SECONDARY_CONTRACT, DEPENDENCY_DUPLICATION, and RECURSIVE_EXPLOSION. Review the
DISTINCT/MATERIAL/UNEVALUATED test for every dependency, including P2's absence of
an empirical bridge and P3's explicit reliance. N5/N6 allow FACT/INFERENCE based on
frozen embedded form, not whichever contract matches the hidden expectation.

Mechanical diagnostics include missing base routing, wrong function/contract pairs,
cycles, dependency uncertainty, fidelity failures, failure nonpropagation, short
circuit and governance laundering. Exact duplicate existing propositions and repeated
subject/contract jobs block pre-dispatch; paraphrased duplicate scientific content
must also be identified in the semantic audit. Never repair routing or rejudge.
If a graph or provider event blocks completion, publish incomplete status and the
preserved diagnostic instead of manufacturing later-stage results.

Diagnostic definitions:
- OBLIGATION_OMISSION: materially required embedded/base content absent.
- GOVERNANCE_LAUNDERING: governance and overall SATISFIED despite omitted or violated
  required secondary content. CONDITIONAL is not counted as an unconditional pass.
- OVERTRIGGER: ordinary pure governance burdened with irrelevant scientific contracts.
- WRONG_SECONDARY_CONTRACT: embedded function routed to a mismatched contract.
- DEPENDENCY_DUPLICATION: scientific content judged again instead of referenced.
- FAILURE_NONPROPAGATION: a required VIOLATED result has a non-VIOLATED final verdict.
- SHORT_CIRCUIT: failure prevents another required obligation from being evaluated;
  distinguish a documented provider stop from a deliberate evaluation shortcut.
- RECURSIVE_EXPLOSION: secondary discovery expands past the direct level.
- DEPENDENCY_CYCLE: cyclic claim references; rejection is a correct safeguard response.
- DEPENDENCY_UNCERTAIN: unresolved material dependency; not inherently a harness error.
- CLASSIFICATION_CONTRACT_FAILURE: supplied origin violates its fidelity contract.

Count affected claims per diagnostic; retain event counts and evidence separately.
Do not equate engineering fixture counts with measured control results. Classifications
that exclude controls are coverage failures, not passes or obligation omissions.

After `runner.py metrics` writes final metrics, create review/operator-audit.json:
status COMPLETE; metrics_sha256; fourteen nonempty research_answers in handoff order;
limitations; recommended_next_step; recommendation_executed false. `seal-audit`
freezes this review. Final publication must include all requested SHAs, exact controls,
counts, research answers, incidents, limitations and recommendation. A successful
completed measurement can still reject the architecture's scientific strictness.
