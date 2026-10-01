# Experiment H.1 — stopped at the premeasurement design gate

**H.1 is incomplete. No provider measurement was started.** Four revised CORE candidates retain material, source-derived answers after deletion of the intended central claim. They therefore fail the user-required authoring gate and were not promoted to final cases or provider packets. This is a construction finding, not an Astra result or evidence that the scoring rubric failed.

## Provenance and checkpoint status

- Base branch: `experiment-h-calibration`. Base SHA: `6d13e5203a40fbb4d3f0af10362eb57123beb524`.
- H.1 branch: `experiment-h1-calibration`; no main merge.
- Protocol, unchanged scoring/contracts and bounded-target freeze: `b92cf1350a4cd658bff6f5c729deb9dd55da38ef`.
- Failed-draft/audit preservation checkpoint: `7d86f0bbb8458fc8bc554ee21fdaf6ef5b6a92fa`.
- Primary final-case freeze, controls, claim packets/preflight/results, ablation packets/preflight/results, and post-result operator audit: **not reached**.
- Final publication commit is identified by `git log -1 -- distance/review/fault-localized-calibration-v0.2.md` and the push confirmation; a report cannot embed its own commit hash.

Frozen H reuse (also includes byte-identical schemas and deterministic contracts):

| Instrument | SHA-256 |
|---|---|
| SCORING.md | `ef80cdf7ec8e119f709caf083530bdfa81d700234e774422c9f8bf6ac2751e8e` |
| CLAIM-WARRANT.md | `8c851f1a64e9c8347ae8056b730ee95ef375bebcd279af2bcffbaff9f60d86fd` |

Both copies are checked against the actual files at the H base commit, not only a mutable manifest. H hard-failure precedence, decisive uncertainty and unresolved structural-conflict override are unchanged. See [reuse evidence](../fault-localized-calibration-v0.2/instrument-reuse.json) and [protocol](../fault-localized-calibration-v0.2/PROTOCOL.md).

## Planned design and realized work

The plan was 12 primary cases (ACH, step-response probing, chain-of-custody verification and delta debugging, each at three positions), plus differential-diagnosis mechanism death, crossdating generic remainder, ACH mechanism uncertainty and step-response target uncertainty controls.

Three authoring attempts produced 36 **drafts**, not a 36-case experiment: direct branches, conditional branches, and conditional branches with a reporting-only leaf and rebalanced lengths. There are zero final cases, zero claim judgments and zero artifact judgments. Controls were not authored because the mandatory primary CORE construction gate failed. No measurement harness was launched or provider preflight certified. The v0.2 runner verifies the stopped authoring state and rejects measurement.

### Targets frozen before variants

Each [target definition](../fault-localized-calibration-v0.2/targets.json) retains its benchmark domain and records the original question and narrowing rationale. Targets were committed before any variants. The bounded questions concern two allegations for one procurement award, two bounded setting changes in one approval process, assembly constraints for one draft, and bounded reproduction subsets for one checkout deployment. Local and scope candidates have material room to answer these questions; no target demands the defective conclusion by definition.

Target narrowing remains a potential calibration confound. Narrowing further to require complete absence of wrongdoing or unique internal causes would discard legitimate bounded contributions and could leave the supported variants without useful answers. That approach was rejected rather than used to manufacture CORE fatality.

### Same-focal-object audit

Within every draft triple, source, target, state, operation, signal, limit, four inference-slot order and graph topology are identical. Two material branch/action slots concern the same focal instance throughout. Only the selected inference slot changes between a supported candidate version and an intended defective version. Opaque random filenames contain no structural class. Provider-style case bodies contain only source, target and mapping; design metadata remains separate. No provider packets were created.

The operator checked ownership in the actual prose: award P-17 throughout ACH; process P-17 throughout step-response; draft D-17 throughout custody; deployment D-17 throughout delta debugging. There is no focal-versus-comparison transfer bridge. This removes H’s salient ownership cue **in the drafts**, without establishing successful experimental separation.

### Revised deletion-length balance

Characters count Unicode code points. Token estimate is ceil(characters/4), an explicitly approximate character-based estimate, not a provider tokenizer count. Fraction uses the newline-joined five-field mapping. Lengths concern intended defects; there are no measured unsupported spans.

| Mechanism | LOCAL chars | SCOPE chars | CORE chars | Max/min | Rank |
|---|---:|---:|---:|---:|---|
| Analysis of Competing Hypotheses | 178 | 182 | 177 | 1.0282 | CORE < LOCAL < SCOPE |
| Step-response probing | 173 | 181 | 175 | 1.0462 | LOCAL < CORE < SCOPE |
| Chain-of-custody verification | 175 | 164 | 175 | 1.0671 | SCOPE < LOCAL/CORE |
| Delta debugging | 172 | 172 | 174 | 1.0116 | LOCAL/SCOPE < CORE |

Every revised ratio is <=1.10. Each position is shortest in at least one triple (ties allowed), and there is no consistent LOCAL < SCOPE < CORE order. The initial conditional wording lengthened scope spans excessively; that failed attempt is preserved separately, not hidden. Natural shorter conditional statements resolved the length issue, without resolving semantic survival.

| Revised draft | Position | Characters | Estimated tokens | Mapping fraction |
|---|---|---:|---:|---:|
| [H1-e129959366fa](../fault-localized-calibration-v0.2/authoring-attempts/H1-e129959366fa.json) | local | 178 | 45 | 8.1839% |
| [H1-2b3d78a746b3](../fault-localized-calibration-v0.2/authoring-attempts/H1-2b3d78a746b3.json) | scope | 182 | 46 | 8.6543% |
| [H1-d1627a69d327](../fault-localized-calibration-v0.2/authoring-attempts/H1-d1627a69d327.json) | core | 177 | 45 | 8.4366% |
| [H1-5666ca4640a7](../fault-localized-calibration-v0.2/authoring-attempts/H1-5666ca4640a7.json) | local | 173 | 44 | 8.7551% |
| [H1-3dc9515b4ce1](../fault-localized-calibration-v0.2/authoring-attempts/H1-3dc9515b4ce1.json) | scope | 181 | 46 | 9.4764% |
| [H1-962b78aacf56](../fault-localized-calibration-v0.2/authoring-attempts/H1-962b78aacf56.json) | core | 175 | 44 | 9.2495% |
| [H1-00c3d9d65557](../fault-localized-calibration-v0.2/authoring-attempts/H1-00c3d9d65557.json) | local | 175 | 44 | 9.1384% |
| [H1-28643a2be1aa](../fault-localized-calibration-v0.2/authoring-attempts/H1-28643a2be1aa.json) | scope | 164 | 41 | 8.9666% |
| [H1-64d7a0a30eb5](../fault-localized-calibration-v0.2/authoring-attempts/H1-64d7a0a30eb5.json) | core | 175 | 44 | 9.5368% |
| [H1-b5bc369b28ab](../fault-localized-calibration-v0.2/authoring-attempts/H1-b5bc369b28ab.json) | local | 172 | 43 | 8.8341% |
| [H1-395502c8f80c](../fault-localized-calibration-v0.2/authoring-attempts/H1-395502c8f80c.json) | scope | 172 | 43 | 9.1733% |
| [H1-725f224527b8](../fault-localized-calibration-v0.2/authoring-attempts/H1-725f224527b8.json) | core | 174 | 44 | 9.3348% |

## Why the revised CORE candidates fail

The following are **operator premeasurement assessments**, not model judgments. Each cited survivor remains byte-for-byte in the unchanged signal after the intended claim is deleted. The full [deletion audit](../fault-localized-calibration-v0.2/review/authoring-audit.json) preserves the original span, ablated mapping, survivor offsets, accepted instrument inference, and materiality rationale.

### Analysis of Competing Hypotheses

Candidate: [H1-d1627a69d327](../fault-localized-calibration-v0.2/authoring-attempts/H1-d1627a69d327.json). Deleted claim:

> The stable inconsistency patterns establish the absence of score manipulation and bidder-specific requirement tailoring throughout the preparation and award of procurement P-17.

Surviving source text:

> The matrix assigns more important inconsistencies to recorded-score alteration than contemporaneous scoring and to bidder-specific authorship than prior generic drafting.

The unchanged signal explicitly contains the comparative inconsistency ordering for both focal allegations. The accepted ACH instrument licenses weakening explanations with greater important inconsistency. Weakening those allegations is a material bounded answer to the frozen target. Removing an assertion of complete absence does not remove that ordering or require a new hypothesis, observation, control, or target framing.

### Step-response probing

Candidate: [H1-962b78aacf56](../fault-localized-calibration-v0.2/authoring-attempts/H1-962b78aacf56.json). Deleted claim:

> The repeated reversible responses identify the intake scheduler and approval batching code as the internal causes of the two-hour and three-hour delay effects in process P-17.

Surviving source text:

> The priority step repeatedly reduces settled intake and end-to-end delay by two hours, with approval delay unchanged.

The unchanged signal already states the focal process’s bounded end-to-end effect. The reversal and settling observations remain in the same field. Step-response probing supplies a distinctive input-to-output response characterization. This is precisely the requested bounded delay-reduction evidence. Identifying internal code as the cause is unnecessary; deletion removes the internal-cause assertion, not the empirical intervention payoff.

### Chain-of-custody verification

Candidate: [H1-64d7a0a30eb5](../fault-localized-calibration-v0.2/authoring-attempts/H1-64d7a0a30eb5.json). Deleted claim:

> The continuous handling histories establish that the opening and closing sections of draft D-17 underwent no unrecorded textual revision between the witnessed assembly events.

Surviving source text:

> The opening-section chain is continuous and documents its witnessed attachment before the binding event.

The unchanged signal explicitly records the focal section’s before-binding assembly constraint. Stable identifiers, reliable witnesses and safeguarding remain stipulated. Continuous custody connects that event to the draft under inquiry. The target asks for assembly constraints, not proof that no unrecorded revision occurred. The surviving constraint is material without replacing the deleted claim.

### Delta debugging

Candidate: [H1-725f224527b8](../fault-localized-calibration-v0.2/authoring-attempts/H1-725f224527b8.json). Deleted claim:

> The repeated reduction tests identify the request-path pair and background-path trio as the unique internal causal explanations of deployment D-17’s observed latency failure.

Surviving source text:

> The request-path reduction retains two changes: the pair fails, and removing either makes that failure disappear.

The unchanged signal states sufficiency under the fixed replay and failure of both single removals. Those facts are the test-relative 1-minimal reproduction property, which is a material answer to the bounded reproduction target. Inferring a unique internal cause is unnecessary. Neither a new test nor a repaired causal inference is required to preserve this payoff.

### What the redesign attempts establish

The direct-branch version leaves explicit branch conclusions. The first conditional version gates those statements but still repeats material content in its reporting leaf. The revised version removes that repetition and balances lengths; it still leaves informative focal signals. Thus the final rejection does not rest on an accidentally redundant leaf alone.

The hidden graph’s C-to-branch edges omit an available signal-to-payoff route. Adding a conditional phrase can encode a reporting dependency, but it cannot make an already-stated bounded effect, witnessed event order, or sufficient reproduction disappear. Under H’s unchanged rubric, a material inference already present or directly entailed by surviving content may count. This is exactly the additional CORE authoring audit the user required.

No repair was used to demonstrate these survivors: no added measurement, hypothesis, control, target framing, or inference rule. Citations point to unchanged mapping text; the accepted instrument supplies the source-derived interpretation. These operator judgments are contestable, but the examples are explicit enough that treating them as valid fatal-bridge designs would be unjustified.

This does **not** prove that every possible same-focal, fixed-signal construction is impossible. It establishes failure of these concrete constructions and explains why merely conditionalizing their descendants does not fix them.

## Measurement outcomes and requested diagnostics

| Item | Result |
|---|---|
| Claim judgments / artifact judgments | 0 / 0 |
| LOCAL / SCOPE / CORE primary outcomes | Not measured |
| Control A: mechanism death | Not authored or measured |
| Control B: generic remainder | Not authored or measured |
| Control C: mechanism uncertainty | Not authored or measured |
| Control D: target uncertainty | Not authored or measured |
| DOES_NOT_SURVIVE / GENERIC_REMAINDER | 0 observed / 0 observed; no observations |
| UNCERTAIN_LOAD_BEARING / CORE_INVALID | 0 observed / 0 observed; no observations |
| Post-result operator review categories | Not applicable; no provider results |
| Premeasurement rejected CORE designs | 4 revised candidates; 12 across three attempts |
| Judge dependency errors / plausible alternatives | Not assessed; no judge outputs |

All claim, artifact, mechanism, target-contribution, cascade and remainder distributions in [metrics.json](../fault-localized-calibration-v0.2/metrics.json) are zero-count empty observation sets. In particular, the absence of observed CORE_INVALID is **not** the experiment’s proposed strong negative finding: no Astra measurements occurred. No strongest-surviving-inference provider field exists to audit. Twelve operator deletion citations were checked instead.

The planned post-freeze six-check review and five categories have not been performed. The implementing operator’s present review is a premeasurement design audit, not independent-rater evidence. It must not be recast as a blinded review of model performance.

## Preservation and tests

All 11 local tests passed. All 44 read-only historical checks passed, including H’s 13 tests and H publication verification. Preservation verifies 3,490 inherited tracked files and 9,259 inherited runtime files. See [historical verification](../fault-localized-calibration-v0.2/review/historical-verification.json).

The historical adapter checks live inherited tracked/runtime hashes, pins only historical Git queries with an implicit working-tree endpoint to the H base, and filters only H.1 additions from inherited untracked-file queries. Explicit historical ranges stay untouched. It does not change historical artifacts or rerun their provider measurements.

Local checks cover byte-identical rubrics/contracts/schemas; target freeze; accepted instruments; triple fields, slots and topology; exact lengths/fractions; rank balance; deletion-only transformations; surviving citations; no hidden metadata in case bodies; no final cases or measurement artifacts; and rejection of the failed authoring gate. H’s scoring tests cover the decisive combinations and conflict override, including hard-failure override.

## Interpretation and next step

H’s ownership and length cues were removed mechanically in the revised drafts. **Whether CORE_INVALID sensitivity survives confound removal remains untested.** No primary or control classification was measured, so none of the ten scientific research questions has a provider-based answer. Status-versus-length association also remains unmeasured.

H.1 does not materially strengthen or weaken empirical confidence in fault-localized viability. It weakens confidence in this attempted construction as a valid calibration: apparently central overclaims were not genuinely necessary for all material payoff. The unchanged scoring instrument correctly constrained authoring; no model-performance conclusion follows.

Limitations include narrow targets, operator-authored/reviewed cases, only three draft formulations, no independent semantic review, no exhaustive search of possible constructions, and no provider data. Supported/unsupported design intentions themselves were never measured.

Recommended next step: resolve feasibility with one demonstrably load-bearing same-focal triple before any provider measurement. If doing so requires altering the fixed-signal/claim-only invariants, explicitly revise the protocol first. A fresh natural-output admission experiment is not justified by this unmeasured H.1. **The recommendation was not executed.**

No main merge, H/G/F modification, E resumption, natural-output experiment, model qualification or production integration occurred. The H.1 branch publishes an explicit incomplete design-stage stop.
