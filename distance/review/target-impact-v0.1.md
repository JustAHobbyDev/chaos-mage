# H8 — Target-facing impact of frozen Chaos-Mage survivors

**Result: all three survivors show at least one material, survivor-attributable change in target-facing reasoning. Four frozen differences support this primary result. All eight planned scientific calls completed; none was retried or replaced.**

This is descriptive Level 1 evidence from this fixed model test. It does not show that augmented responses are better overall, that every added idea came from the survivor, or that real-world outcomes improve. The native responses had six material contributions absent from the augmented responses. One augmented retain/revert rule was materially different but unsupported by its frozen survivor.

## Identity and checkpoints

- Base: `c62b622b69ed900b9debcc9e41e133536287be59`.
- Branch: `experiment-h8-target-impact`; only this branch is pushed to origin.
- H7 and all earlier tracked bytes remain unchanged: 18,477 historical files verified.
- The closing completion commit contains the final report and freeze; its SHA is reported in the completion message. Earlier checkpoints are listed below.

| Checkpoint SHA | Purpose |
|---|---|
| `bb3881fcf42d952598b6f97426fffce1e2c38f25` | Freeze H8 neutral survivor packets and bounded target-impact protocol |
| `dedaed49c50f3d10b54d290b204e6daa2a9754f6` | Freeze both H8 native target responses before augmentation |
| `771fe6b42f36039686bdc47a7490f69255f59753` | Freeze H8 temperature and chronology augmented responses |
| `5fe19a8ac31b48d84eaecd723c7fc0b8fb698db9` | Freeze all five H8 target-facing responses |
| `374fc899dfc4d8f0e0e862688a71a8238163d05c` | Freeze blinded H8 pair order and impact packets before judgments |
| `b42d04812c9a23f484434f52cff7ae5c0c92ff0c` | Freeze first two blinded H8 impact judgments |
| `80fb6c514f17608531dbb83aa53c251c504fab81` | Freeze all three blinded H8 judgments before unblinding |
| `18ae25a95a391ecc3946c76b49faf4007e3cea1b` | Unblind H8 differences mechanically after complete judgment freeze |
| `59127f0a83577d343484edd84f8ea1a7a67e8e57` | Freeze scoped H8 survivor attribution and primary outcomes |

## Frozen question, corpus and fidelity

> A Chaos-Mage transfer has target-facing impact when its frozen admitted survivor causes a material change in the target's inquiry, prioritization, action, decision rule, constraint structure, or decision-relevant problem representation compared with the same target considered without that survivor.

Terminology, extra detail, longer output and source-framework mentions alone do not count. A material difference must change or plausibly govern evidence gathering, uncertainty priority, action/withholding, future action triggers, ruled-out conclusions/actions, or the representation used to choose among them.

| Frozen survivor | Source instrument (report only) | H7 admission | Positive candidates | Audit |
|---|---|---|---:|---|
| H7-T01-1 | Analysis of Competing Hypotheses | KEEP_WITH_REDUCED_SCOPE | 15 | PASS |
| H7-T03-1 | Crossdating | KEEP_WITH_WARRANT_FLAGS | 9 | PASS |
| H7-T03-2 | Chain-of-custody verification | KEEP_WITH_REDUCED_SCOPE | 8 | PASS |

Packets contain the allowlisted candidates’ value and scope verbatim, assigned neutral V IDs in allowlist order, plus restrictive artifact cautions. No substantive neutralization rewrite was necessary. Crosswalks, source rationale and H7 status stayed outside provider inputs. All 32 positive items map to definite viable candidates; no deleted, unresolved, nonviable or insufficiency-only candidate was promoted.

The T01 packet supplies no logger rotation/field-sampling design. The chronology packet excludes unresolved K14 and explicitly denies a chronology-to-intervention-priority license. The continuity packet excludes intervention selection, causal comparison, retain/revert and purchasing-decision machinery. All candidate scopes remain intact.

[Protocol](../target-impact-v0.1/PROTOCOL.md) · [Manifest](../target-impact-v0.1/manifest.json) · [Survivor packets](../target-impact-v0.1/survivor-packets/) · [Fidelity audits and crosswalks](../target-impact-v0.1/survivor-audits/)

## Execution and blinding

Two native responses were generated and frozen first, followed by three augmented responses. All calls requested GPT-6 Astra/high in fresh ephemeral contexts with tools/history/config inheritance disabled. Common target instructions and the same structured schema applied to all five responses. No previous response was visible to another generation.

Three comparison packets contained only the target frame and visible A/B responses, alongside common judgment instructions. Hidden survivor_basis metadata was stripped. A/B assignment used the first-byte parity of SHA256(`H8|<base SHA>|<pair_id>`), frozen before judgments. All three judgments froze at `80fb6c51` before mechanical unblinding at `18ae25a9`. Judges were not asked for winners and did not revise judgments after unblinding.

**PAIR-02 and PAIR-03 reuse the identical T03 native response. The three comparisons are correlated cases, not three independent samples.**

The fixed plan remained 2 native + 3 augmented + 3 impact calls. Eight unique reservations finished successfully, with no provider no-observation, malformed observation, retry, replacement or skipped slot. Five bounded batches recorded before/after allowance and available token usage. Account data remains ignored under `.runtime/`. No clean quota calibration was inferred from concurrent account work; costs and remaining-work quota estimates stayed unknown. No reset credits were redeemed. Existing below-30% consent policy was unchanged.

Available provider token totals: `{"cache_write_input_tokens": 0, "cached_input_tokens": 7936, "input_tokens": 96648, "output_tokens": 15059, "reasoning_output_tokens": 2753}`. These are not billed-dollar or allowance conversions. Requested model/high reasoning and CLI fingerprints are recorded; returned model snapshot identifiers were unavailable. Provider-internal retry behavior remains unobservable.

An offline preparation performance issue was fixed before measurement by hashing a single Git archive instead of starting a Git process per historical file. Superseded local preparation manifests were archived; no scientific observation existed or changed. No measurement-stage recovery was needed.

## Primary outcomes and category counts

| Pair | Survivor | Frozen comparison | Primary impact status | Attributable material differences |
|---|---|---|---|---|
| PAIR-01 | H7-T01-1 | YES | MATERIAL_TARGET_CHANGE | D02 |
| PAIR-02 | H7-T03-1 | YES | MATERIAL_TARGET_CHANGE | D1 |
| PAIR-03 | H7-T03-2 | YES | MATERIAL_TARGET_CHANGE | D4, D5 |

Outcome counts: MATERIAL_TARGET_CHANGE **3**; MINOR_OR_NONMATERIAL_CHANGE **0**; NO_MATERIAL_CHANGE **0**; UNCERTAIN_TARGET_CHANGE **0**; UNMEASURED **0**. No pass percentage is defined.

There are **16 frozen material differences**: six native-only and ten with augmented contributions (including BOTH_DIFFERENT). Of those ten, **four are attributable**, three target-only/generic, two uncertain in full-record attribution, and one unsupported by the frozen survivor. A seventeenth difference, PAIR-01 D06, has uncertain materiality and is excluded from material counts.

| Category | All frozen material differences, either direction | Survivor-attributable material differences |
|---|---:|---:|
| PROBLEM_REPRESENTATION_CHANGE | 4 | 3 |
| INQUIRY_CHANGE | 10 | 3 |
| PRIORITY_CHANGE | 2 | 1 |
| ACTION_CHANGE | 3 | 2 |
| DECISION_RULE_CHANGE | 8 | 2 |
| CONSTRAINT_CHANGE | 7 | 3 |

Each category counts once per difference. A difference can have multiple categories, so column totals are not counts of unique changes. The attributable column credits the augmented side of PAIR-03 D5’s BOTH_DIFFERENT record; it does not credit the native side’s stock tracking.

## Pair results, direction and attribution

### PAIR-01 — H7-T01-1

Blinded order: **A = SURVIVOR_AUGMENTED; B = NATIVE**. Frozen semantic equivalence: **NO**; overall material difference: **YES**.

The responses share the unresolved-cause assessment, selective tracing strategy and proportionate interim precautions. Material differences remain in measurement-validation prerequisites, hypothesis evaluation, within-delivery sampling, the trigger for targeted correction and the response to an inconclusive fortnight.

[Frozen judgment](../target-impact-v0.1/impact-judgments/PAIR-01.json) · [Mechanical unblinding](../target-impact-v0.1/unblinded/PAIR-01.json) · [Full attribution audit](../target-impact-v0.1/attribution-audit/PAIR-01.json)

| Difference | Direction | Materiality | Attribution | Target-facing difference |
|---|---|---|---|---|
| D01 | SURVIVOR_AUGMENTED | YES | UNCERTAIN_ATTRIBUTION | Measurement-validity prerequisites, paired-reference checks and sensitivity tests; bundled acquisition extensions leave full-record attribution uncertain. |
| D02 | SURVIVOR_AUGMENTED | YES | ATTRIBUTABLE_TO_SURVIVOR | Advance predictions; explicit explanation comparison; contradiction weighting and within-delivery dependence. |
| D03 | NATIVE | YES | NATIVE_ONLY — not a survivor claim | Native requests additional within-delivery package readings and an explicit representativeness boundary. |
| D04 | BOTH_DIFFERENT | YES | UNCERTAIN_ATTRIBUTION | Investigate a stage versus authorize targeted corrective action after repeated evidence; attribution of the full trigger/action contrast remains uncertain. |
| D05 | NATIVE | YES | NATIVE_ONLY — not a survivor claim | Native supplies an explicit end-of-fortnight rule to retain precautions and continue focused sampling. |
| D06 | BOTH_DIFFERENT | UNCERTAIN | ATTRIBUTABLE_TO_SURVIVOR | Timing/scope of receiving standardization differs ambiguously; materiality remains UNCERTAIN. |

Native overlap:

- Both propose package-linked selective temperature tracing, comparisons across operating conditions, receiving-method checks, proportionate handling precautions and uncertainty about causes.
- Native already distinguishes loading-air readings from package history and changes follow-up according to observed intervals.
- Native has additional within-delivery package sampling and an explicit end-of-fortnight continuation rule; these native-only material contributions are preserved.

**D01: UNCERTAIN_ATTRIBUTION.** Package-link verification, paired reference/shared-error conditions, sensitivity analysis and indeterminate/missing-trace treatment have direct frozen support. The frozen difference also bundles before-deployment clock alignment and handoff-recording requirements, extending from interpretability conditions into acquisition design. The record cannot be credited in full without separating that extension; the frozen judgment is not split or rewritten. V02 leaves the linkage check and criteria unspecified. V06 expressly supplies no timestamp-collection protocol; V08 is sensitivity analysis, not a new acquisition design. Supported subparts are visible but this bundled difference receives no primary credit.
Frozen cited support: V02 → K03, V03 → K04, V04 → K05, V08 → K09, V09 → K11.

**D02: ATTRIBUTABLE_TO_SURVIVOR.** The augmented response explicitly requires predictions before review, consistent/inconsistent/indeterminate comparison, qualitative weighting of reliable contradictions, attention to discriminating observations and within-delivery dependence. These are the cited definite candidates, and the native response lacks this combined prescribed assessment. The downstream preparation task and evidence-priority rule are stated in the frozen judgment. Credit is limited to analytical procedure on available interpretable observations. It adds no logger rotation, timestamp protocol, numerical weight, established cause or cross-delivery independence assumption.
Frozen cited support: V01 → K01, V05 → K06, V06 → K07, V07 → K08, V11 → K15, V14 → K21.

**D04: UNCERTAIN_ATTRIBUTION.** The cited survivors plausibly support conditional, monitored-case stage inquiry. However, the judged contrast is also a changed evidentiary trigger and the absence of a corrective-action authorization present in the native response. These candidates do not directly prescribe withholding corrective action or the native-versus-augmented trigger difference. Attribution of that full contrast is unresolved. Do not convert a limit on eliminative conclusions into a new intervention rule, or count an omitted native action as a demonstrated survivor prohibition.
Frozen cited support: V01 → K01, V06 → K07, V10 → K14.

**D06: ATTRIBUTABLE_TO_SURVIVOR.** The conditional standardized receiving action is directly supported by V12/K16, but the frozen judge marks its practical timing/scope difference UNCERTAIN because the native investigation already introduces a common procedure. Attribution does not upgrade materiality. Reliable comparable readings, capacity and handling conditions remain required. This uncertain materiality record is excluded from primary counts.
Frozen cited support: V12 → K16.

### PAIR-02 — H7-T03-1

Blinded order: **A = NATIVE; B = SURVIVOR_AUGMENTED**. Frozen semantic equivalence: **NO**; overall material difference: **YES**.

The responses share the core inquiry into comparable cohorts, refill need and actionable barriers. They differ materially in temporal corroboration, task demonstration, location-level comparison, and explicit rules for purchasing assumptions and post-trial continuation.

[Frozen judgment](../target-impact-v0.1/impact-judgments/PAIR-02.json) · [Mechanical unblinding](../target-impact-v0.1/unblinded/PAIR-02.json) · [Full attribution audit](../target-impact-v0.1/attribution-audit/PAIR-02.json)

| Difference | Direction | Materiality | Attribution | Target-facing difference |
|---|---|---|---|---|
| D1 | SURVIVOR_AUGMENTED | YES | ATTRIBUTABLE_TO_SURVIVOR | Corroborated chronology, fixed anchors, alternative sequences and limits on temporal conclusions. |
| D2 | NATIVE | YES | NATIVE_ONLY — not a survivor claim | Native requests a behavioral refill-task demonstration. |
| D3 | SURVIVOR_AUGMENTED | YES | TARGET_ONLY_OR_GENERIC | Augmented response adds individual collection-point comparisons without a survivor basis. |
| D4 | NATIVE | YES | NATIVE_ONLY — not a survivor claim | Native explicitly adjusts purchasing assumptions to supported replenishment intervals. |
| D5 | NATIVE | YES | NATIVE_ONLY — not a survivor claim | Native states a post-trial continuation rule with a service-deterioration condition. |

Native overlap:

- Both examine complete cohort windows, replenishment readiness, voluntary follow-up, actionable barriers and a bounded process trial.
- Native already distinguishes no refill need from blocked replenishment and warns against interpreting complaints as population prevalence.
- Native uniquely specifies a refill-task demonstration, purchasing-interval response and post-trial continuation rule in the frozen comparison.

**D1: ATTRIBUTABLE_TO_SURVIVOR.** Fixed recorded anchors, explicit unknown intervals, corroborated need-before-obstacle ordering, supplementary elapsed-time comparisons, and leaving competing sequences unresolved directly trace to cited definite chronology candidates. The frozen material consequence is additional temporal evidence gathering and withholding unsupported sequence conclusions. This establishes no observed household classification, cause, population explanation or intervention priority. Unresolved K14 is absent and unnecessary; the response explicitly denies that documented sequence determines the best intervention.
Frozen cited support: V01 → K01, V02 → K03, V03 → K04, V05 → K06, V06 → K07, V08 → K13, V09 → K17.

**D3: TARGET_ONLY_OR_GENERIC.** Comparing identifiable individual collection points is a target-derived refinement. The model supplied no survivor_basis for this inquiry; no chronology candidate selects a collection-point subgroup comparison. Do not infer attribution merely because this useful-looking inquiry occurs in the augmented response.

### PAIR-03 — H7-T03-2

Blinded order: **A = NATIVE; B = SURVIVOR_AUGMENTED**. Frozen semantic equivalence: **NO**; overall material difference: **YES**.

The responses share the central distinction between nonpurchase and dissatisfaction and propose similarly bounded trials. They nevertheless differ in specific inquiries, evidence-linkage requirements, trial measurements and the evidence required to retain a change. These differences can alter what is gathered, which conclusions are withheld and what happens after the trial.

[Frozen judgment](../target-impact-v0.1/impact-judgments/PAIR-03.json) · [Mechanical unblinding](../target-impact-v0.1/unblinded/PAIR-03.json) · [Full attribution audit](../target-impact-v0.1/attribution-audit/PAIR-03.json)

| Difference | Direction | Materiality | Attribution | Target-facing difference |
|---|---|---|---|---|
| D1 | SURVIVOR_AUGMENTED | YES | TARGET_ONLY_OR_GENERIC | Augmented response adds collection-point comparisons without a survivor basis. |
| D2 | SURVIVOR_AUGMENTED | YES | TARGET_ONLY_OR_GENERIC | Augmented response asks directly about satisfaction; its broader V01 field citation does not supply that addition. |
| D3 | NATIVE | YES | NATIVE_ONLY — not a survivor claim | Native requests a refill-task demonstration and associated support-message review. |
| D4 | SURVIVOR_AUGMENTED | YES | ATTRIBUTABLE_TO_SURVIVOR | Order-linked accounts, source/time documentation, discrepancy preservation, clarification/exclusion and household-level inference limits. |
| D5 | BOTH_DIFFERENT | YES | ATTRIBUTABLE_TO_SURVIVOR | Separate assignment, receipt, step completion and ordering; require necessary exposure/outcome links for dependent explanations. |
| D6 | BOTH_DIFFERENT | YES | UNSUPPORTED_BY_FROZEN_SURVIVOR | Augmented retention rule requires a supporting comparison and otherwise reversion/inconclusiveness; unsupported by the frozen survivor. |

Native overlap:

- Both examine cohort windows, remaining stock, expected timing, customer barriers and limited trials.
- Native already separates nonpurchase from satisfaction and warns about incomplete follow-up and confounding.
- Native has a refill demonstration and explicit remaining-stock trial tracking; the continuity packet does not replace all native contributions.

**D1: TARGET_ONLY_OR_GENERIC.** The target identifies collection points, and the model adds a conditional location comparison without a survivor_basis entry. None of the continuity candidates selects this comparison. Material in the frozen comparison, but not established as an effect traceable to the survivor.

**D2: TARGET_ONLY_OR_GENERIC.** The inquiry cites V01, which supports stock, refill timing, difficulties, attempts and household-specific explanation. The distinct addition identified by the judge is a direct satisfaction question; that content is not in V01. It is a generic inquiry into an explicitly live target explanation. The field-level citation is broader than its support for this particular addition. Record the attribution limit; no provenance calibration is needed.

**D4: ATTRIBUTABLE_TO_SURVIVOR.** The response preserves source/time/order links, distinguishes records from recollections and corrections, treats unresolved links as evidence gaps, and requires clarification or exclusion only for conclusions needing those links. The cited definite candidates support the additional linkage inquiry and household-versus-aggregate inference boundary. Credit covers documentation and conditional household attribution, not complete historical truth, aggregate causal inference, successful linkage, intervention selection or purchasing commitment.
Frozen cited support: V01 → K01, V02 → K02, V03 → K05, V04 → K07, V05 → K08, V06 → K09, V08 → K15.

**D5: ATTRIBUTABLE_TO_SURVIVOR.** The augmented side of the frozen BOTH_DIFFERENT record requires separate assignment, actual receipt, step completion and subsequent-order documentation, with necessary exposure/outcome linkage for dependent explanations. V07/K10 supplies those event distinctions and V02/K02 supplies the linkage prerequisite. Credit only the conditional documentation requirements if a trial occurs. The target-facing model also selects a trial in this field, but that common target-derived proposal is not the material contribution credited here. No randomization, causal-comparison, retention or purchasing rule is licensed.
Frozen cited support: V02 → K02, V07 → K10.

**D6: UNSUPPORTED_BY_FROZEN_SURVIVOR.** The stricter requirement for a supporting comparison before provisional retention, with reversion or inconclusiveness otherwise, has no cited survivor basis. The frozen packet explicitly excludes causal-comparison and retain/revert branches. Necessary exposure linkage does not supply this intervention continuation rule. This is an apparent material effect in an explicitly excluded branch, not primary evidence. It may overconstrain continuation when comparison is infeasible; no evidence establishes that the stricter rule improves the target decision. The model was not exposed to deleted H7 text, so this does not establish literal leakage or dependence on unseen claims.

## Strongest supported changes

- **Temperature inquiry:** the native response proposes monitoring and ordinary follow-up. The augmented response adds predictions before review, an evidence-by-explanation comparison, reliable-contradiction weighting and within-delivery dependence. This changes immediate preparation, evidence priorities and future assessment rules (PAIR-01 D02).
- **Chronology inquiry:** the augmented response requires corroborated event timing, fixed recorded anchors and unresolved competing sequences to remain unresolved. This changes evidence gathering and constrains temporal explanations without licensing intervention priority (PAIR-02 D1).
- **Continuity inquiry:** the augmented response adds source/time/order linkage, preserved discrepancies and clarification or exclusion for conclusions requiring missing links. It changes which household accounts can support specific conclusions (PAIR-03 D4).
- **Conditional trial documentation:** where a trial occurs, the augmented response separates assignment, actual receipt, completed step and ordering, with linkage prerequisites for dependent explanations. This changes documentation and inference constraints, not which trial or purchasing decision to choose (PAIR-03 D5).

## Negative evidence, limits and non-effects

**Native responses already reproduce substantial ordinary machinery.** Cohort comparisons, replenishment readiness, voluntary barrier inquiry, limited trials, package tracing, method comparisons and cautious causal interpretation occur without survivor packets. Those ideas are not credited as source-derived effects. Native-only sampling, task-demonstration and continuation/purchasing rules remain material contributions that augmentation did not preserve in these samples. No survivor has a NO_MATERIAL_CHANGE outcome, but many individual considerations added no separately established material effect. The uncertain receiving-standardization contrast is not upgraded.

**Excluded H7 branches reappear in generated responses.** Both T01 responses propose logger rotation, despite its exclusion from the survivor packet. The augmented item has no survivor_basis and is not a novel survivor effect. Both T03 conditions generate trial/decision machinery from the target task; that is not a license to credit the frozen continuity survivor with it. PAIR-03 D6’s stricter comparison-dependent retain/revert rule is an apparent material effect in an explicitly excluded branch and is rejected as survivor evidence. It could overconstrain action when comparison is infeasible; no measured quality benefit justifies that stricter trigger.

**No credited primary effect requires deleted or unresolved H7 content.** H7-T03-1 K14 remains absent. We do not infer that unseen deleted text caused a generated proposal: the contexts did not contain it. The finding is that some apparent augmented effects cannot be supported by the admitted survivor. PAIR-01 D01 and D04 are left uncertain in attribution rather than splitting or repairing their frozen judgments to obtain more positive counts.

**Explicit source identity is absent from all augmented packets and visible responses.** The four credited changes therefore survived removal of framework names and decorative pedigree. This does not mean all source semantics were absent: the source-derived operational structure was intentionally retained.

A field-level citation can support part of a response without supporting its incremental difference: PAIR-03’s satisfaction question illustrates this. Existing provenance is sufficient to identify that limit. This incidental issue does not justify further evaluator/provenance calibration under the stop rule; none was run.

## Interpretation, limitations and next step

**Yes, the current evidence shows admitted survivors materially changing target-facing model reasoning in this fixed test.** The strongest evidence is the four scoped changes in investigation, evidentiary structure and constraints after explicit source identity was removed. This extends beyond merely demonstrating defensible foreign mappings. H7 admission statuses remain unchanged.

Limits: one sample per condition/judgment; one model family for generation and assessment; two distinct targets with a shared T03 baseline; stochastic response variation; model-simulated decisions; operator attribution rather than independent attribution replication; coarse field-level basis metadata; unavailable served model snapshots/provider-internal retry observability; no external outcome or quality measure. The design adds vetted information and scope cautions together, so it does not isolate individual considerations or the effect of the “vetted” framing. It establishes neither economic benefit nor better actions, human preference, production economics, cross-family repeatability or real-world causal improvement. No exhaustion probability or quota-cost conversion is claimed.

**Recommended next scientific step:** prospectively define one bounded target decision task using real records and a prespecified decision-quality outcome, then compare native and frozen-survivor assistance under a fixed protocol. Assess whether the changed evidence choices or constraints help the decision. Do not begin that study, regenerate H7, enlarge H8, test successive ontology transformations, refine evaluators or merge main without separate direction.

## Validation

26 H8 offline checks pass, including all 18,477 historical files, exact executed requests/responses, eight unique sessions, freeze barriers, metadata stripping, shared native bytes, mechanical direction and attribution/count reconstruction. The 22 existing budget and 22 existing usage checks passed before measurement. No scientific provider call was used for these checks. See [final verification](../target-impact-v0.1/review/final-verification.json).

## Appendix A — Two native target responses

### Native T01

[Immutable response](../target-impact-v0.1/responses/native/T01.json)

```json
{
  "current_position": {
    "statement": "The reported receiving exceptions warrant investigation, but existing records do not locate their cause. Multiple contributors remain plausible.",
    "rationale": "Loading logs measure room temperature, packages are untracked between staging and loading, and receiving uses one package reading with methods that vary by site. Exceptions occur on both short and long routes."
  },
  "top_uncertainties": [
    {
      "uncertainty": "Where and when temperature changes occur.",
      "why_it_matters": "Staging, loading, transit and receiving require different corrective actions."
    },
    {
      "uncertainty": "How much receiving methods contribute to the reported exceptions.",
      "why_it_matters": "Different methods and single-package sampling limit comparability and delivery-wide conclusions."
    },
    {
      "uncertainty": "Whether exceptions share one cause or reflect several contributors.",
      "why_it_matters": "A single change may leave other sources of temperature deviation unresolved."
    }
  ],
  "next_inquiries": [
    {
      "inquiry": "Follow selected packages across the delivery process.",
      "operation_or_observation": "For two weeks, rotate available loggers through identified sample packages from staging through receiving. Record logger placement and staging, loading, departure, arrival and receiving-reading times.",
      "decision_relevance": "Relates temperature changes to handling intervals instead of inferring cause from endpoints."
    },
    {
      "inquiry": "Assess receiving measurement consistency.",
      "operation_or_observation": "Document site methods, package selection and delay before measurement. On sampled deliveries, add a common measurement procedure and, where feasible, readings from additional packages.",
      "decision_relevance": "Tests whether method differences or package variation help explain reported exceptions."
    },
    {
      "inquiry": "Compare plausible operating contributors.",
      "operation_or_observation": "Distribute the limited samples across all three bays, both carriers, short and long routes, and differing receiving sites. Link each sample to its bay, carrier, route and receiving method; repeat informative comparisons where feasible.",
      "decision_relevance": "Identifies patterns worth targeting while reducing reliance on isolated events."
    }
  ],
  "priorities": [
    {
      "rank": 1,
      "item": "Make sampled temperature readings comparable and link them to packages and handling times.",
      "rationale": "These gaps currently prevent reliable interpretation."
    },
    {
      "rank": 2,
      "item": "Obtain temperature histories spanning staging through receiving.",
      "rationale": "Locating the interval of change is more actionable than collecting additional unlinked endpoint readings."
    },
    {
      "rank": 3,
      "item": "Use emerging evidence to focus repeat observations.",
      "rationale": "Logger capacity and staff time are limited."
    }
  ],
  "immediate_actions": [
    {
      "action": "Reinforce required cold handling and reduce avoidable staging, loading and receiving delays.",
      "rationale": "This is a defensible temporary precaution while the responsible interval remains unknown."
    },
    {
      "action": "Assign logger rotation, sample identification and a short shared observation record before the next deliveries.",
      "rationale": "The two-week investigation needs consistent execution with limited equipment."
    },
    {
      "action": "Apply existing food-handling requirements to out-of-range deliveries while documenting the measurement and handling circumstances.",
      "rationale": "The investigation does not suspend normal handling requirements."
    }
  ],
  "decision_rules": [
    {
      "condition": "Repeated, comparable observations locate temperature increases within a particular handling interval.",
      "consequence": "Target corrective action and further monitoring at that interval.",
      "rationale": "Time-linked evidence supports a more specific intervention."
    },
    {
      "condition": "Reported exceptions vary with measurement procedure or measurement delay.",
      "consequence": "Standardize the relevant receiving practice and reassess exceptions while continuing temperature tracing.",
      "rationale": "Measurement effects may explain part of the pattern without excluding handling problems."
    },
    {
      "condition": "The two-week sample remains mixed or inconclusive.",
      "consequence": "Retain proportionate precautions and focus further sampling on unresolved intervals or conditions.",
      "rationale": "Limited coverage cannot establish a single cause or demonstrate that the problem has disappeared."
    }
  ],
  "important_distinctions": [
    {
      "distinction": "Loading-room temperature differs from the temperature history of an individual package.",
      "consequence": "Acceptable bay logs do not establish acceptable package conditions throughout staging and loading."
    },
    {
      "distinction": "One package reading differs from a delivery-wide assessment.",
      "consequence": "Avoid treating a single reading as representative of every package."
    }
  ],
  "constraints": [
    {
      "constraint": "Routine deliveries must continue, logger coverage is limited, and additional observations are feasible for two weeks.",
      "implication": "Use rotating samples and brief records rather than universal instrumentation."
    },
    {
      "constraint": "Normal food-handling requirements remain in force, and fleet replacement has no budget.",
      "implication": "Keep interim changes within required handling practices and available operating resources."
    }
  ],
  "do_not_conclude": [
    {
      "statement": "Acceptable loading logs prove the carrier caused the receiving exceptions.",
      "reason": "Pre-loading package conditions and receiving effects remain unresolved."
    },
    {
      "statement": "Route duration alone explains the problem.",
      "reason": "Exceptions occur on both short and long routes; duration may still contribute alongside other factors."
    }
  ]
}
```

### Native T03

[Immutable response](../target-impact-v0.1/responses/native/T03.json)

```json
{
  "current_position": {
    "statement": "The decline in second orders within eight weeks is established; its cause and implications for satisfaction remain unresolved.",
    "rationale": "Consumption timing is unknown, promotions and collection-point expansion coincided, and support messages capture only customers who contacted the service."
  },
  "top_uncertainties": [
    {
      "uncertainty": "Do recent customers need a refill within eight weeks?",
      "why_it_matters": "Unused stock or longer purchase intervals could explain nonpurchase without dissatisfaction."
    },
    {
      "uncertainty": "Did customer composition change, or did comparable customers become less likely to reorder?",
      "why_it_matters": "Promotions and new collection points may have attracted customers with different needs or introduced different experiences."
    },
    {
      "uncertainty": "Which barriers actually prevent a needed second purchase?",
      "why_it_matters": "Leaks, collection hours and refill confusion suggest different interventions; complaint counts cannot establish their prevalence."
    }
  ],
  "next_inquiries": [
    {
      "inquiry": "Verify the decline using comparable observation periods and order characteristics.",
      "operation_or_observation": "Compare first-order cohorts with eight complete weeks of follow-up. Examine product, quantity, discount and fulfillment option; separate starter and refill purchases if product records permit.",
      "decision_relevance": "Distinguishes incomplete follow-up and changes in purchase mix from declines within comparable groups; does not establish causality."
    },
    {
      "inquiry": "Determine whether customers are ready to replenish and what happens when they are.",
      "operation_or_observation": "During week one, invite a limited, varied set of repeat and nonrepeat customers to voluntary follow-up. Ask about remaining stock, actual use, expected refill timing, attempted reorders, leaks, collection access and refill understanding.",
      "decision_relevance": "Separates lack of current need from barriers that a fulfillment or communication change could address."
    },
    {
      "inquiry": "Check whether reported friction blocks the customer task.",
      "operation_or_observation": "Ask willing participants to describe a recent collection or demonstrate how they would arrange a refill. Review relevant support messages alongside these accounts.",
      "decision_relevance": "Provides concrete evidence for selecting one process change without treating support-message frequency as representative."
    }
  ],
  "priorities": [
    {
      "rank": 1,
      "item": "Establish comparable cohorts and replenishment readiness.",
      "rationale": "These checks determine whether the eight-week measure reflects a service problem or a timing mismatch."
    },
    {
      "rank": 2,
      "item": "Identify one actionable barrier among customers who need more product.",
      "rationale": "Only one fulfillment or communication process can change for a month."
    },
    {
      "rank": 3,
      "item": "Use the bounded trial to inform the purchasing commitment.",
      "rationale": "The five-week deadline requires a decision with explicit residual uncertainty."
    }
  ],
  "immediate_actions": [
    {
      "action": "Use week one for the cohort review and limited voluntary follow-up.",
      "rationale": "Leaves approximately one month to try a selected change before the purchasing deadline."
    },
    {
      "action": "Select one supported process change and define its eligible customers, intended effect, success criterion and stop condition before launch.",
      "rationale": "Keeps the trial interpretable and bounded. Where feasible, compare with similar customers receiving the existing process."
    },
    {
      "action": "Track the targeted barrier, successful refill or collection attempts, observed orders and remaining stock reported by participants.",
      "rationale": "These observations can inform the commitment, while a one-month trial cannot establish an eight-week repeat-purchase effect for newly enrolled customers."
    }
  ],
  "decision_rules": [
    {
      "condition": "Follow-up indicates substantial remaining stock and later expected replenishment.",
      "consequence": "Interpret eight-week nonpurchase cautiously and plan purchasing around a range of replenishment intervals.",
      "rationale": "An order is not yet due for those households."
    },
    {
      "condition": "Customers needing a refill encounter a recurring, demonstrable communication or fulfillment barrier.",
      "consequence": "Trial one change addressing that barrier: clearer refill instructions for confusion, or a collection-process adjustment for access problems.",
      "rationale": "The intervention should match the observed obstacle."
    },
    {
      "condition": "The trial meets its predefined criterion, with supporting comparison evidence where feasible and no material service deterioration.",
      "consequence": "Continue the change provisionally and monitor later repeat orders.",
      "rationale": "Near-term improvement supports continuation but does not yet prove durable retention."
    }
  ],
  "important_distinctions": [
    {
      "distinction": "No second order versus no need for more product.",
      "consequence": "Assess replenishment readiness before interpreting nonpurchase."
    },
    {
      "distinction": "A reported problem versus its prevalence across customers.",
      "consequence": "Use support messages and voluntary follow-up to identify mechanisms; account for selective participation."
    }
  ],
  "constraints": [
    {
      "constraint": "No mandatory subscription or unsolicited repeated contact.",
      "implication": "Keep follow-up voluntary and do not use forced recurrence to improve the metric."
    },
    {
      "constraint": "One process change for one month; purchasing due in five weeks; major packaging redesign unavailable.",
      "implication": "Choose a feasible intervention and base the commitment on observed demand plus explicit uncertainty, without assuming trial benefits will persist."
    }
  ],
  "do_not_conclude": [
    {
      "statement": "Promotions or new collection points caused the decline.",
      "reason": "Their simultaneous introduction and possible customer differences prevent that conclusion from timing alone."
    },
    {
      "statement": "Silent customers are satisfied, or nonrepeat customers are dissatisfied.",
      "reason": "Neither support contact nor nonpurchase directly measures satisfaction."
    }
  ]
}
```

## Appendix B — Three survivor-augmented target responses

### Augmented H7-T01-1

[Immutable response with hidden attribution metadata](../target-impact-v0.1/responses/augmented/H7-T01-1.json)

```json
{
  "current_position": {
    "statement": "The cause remains unresolved; staging/loading, transit, receiving and measurement differences may contribute together.",
    "rationale": "Acceptable loading-room temperatures and one receiving package reading do not locate when package temperatures changed. Exceptions on short and long routes do not isolate transit duration."
  },
  "top_uncertainties": [
    {
      "uncertainty": "Where and when affected packages become elevated.",
      "why_it_matters": "The appropriate handling change depends on the stage involved."
    },
    {
      "uncertainty": "Whether receiving readings are reliable and comparable across sites.",
      "why_it_matters": "Different methods may create or obscure apparent exceptions."
    }
  ],
  "next_inquiries": [
    {
      "inquiry": "Establish whether limited package-linked monitoring is interpretable.",
      "operation_or_observation": "Before deployment, define and verify logger-to-package identification, sensor placement, clock alignment and handoff recording. Establish what each sensor measures and whether its response can distinguish relevant stages.",
      "decision_relevance": "Unverified linkage or inadequate timing prevents reliable package or stage attribution."
    },
    {
      "inquiry": "Observe selected deliveries across relevant operating conditions.",
      "operation_or_observation": "Propose a feasible two-week logger rotation covering both carriers, all three bays, short and long routes, and differing receiving practices as capacity permits. Track selected packages through staging, loading, arrival and receipt measurement; record handoff times and delays.",
      "decision_relevance": "This can reveal stage-specific patterns in monitored cases; incomplete coverage limits wider conclusions."
    },
    {
      "inquiry": "Compare usual and standardized receiving measurements where feasible.",
      "operation_or_observation": "On a verified tracked package, pair usual and standardized readings without compromising handling. Document method, location and delay; first establish reference reliability, timing/location tolerances and possible shared errors.",
      "decision_relevance": "Interpretable disagreement supports investigating measurement differences; reliable agreement on elevation weakens those differences as the sole explanation."
    }
  ],
  "priorities": [
    {
      "rank": 1,
      "item": "Secure interpretable observations before expanding monitoring.",
      "rationale": "More readings will not resolve the cause if package identity, measurement meaning or timing is uncertain."
    },
    {
      "rank": 2,
      "item": "Compare competing explanations, then target remaining ambiguities.",
      "rationale": "Reliable contradictions and observations distinguishing surviving alternatives matter more than counts of supporting readings."
    }
  ],
  "immediate_actions": [
    {
      "action": "Before reviewing new results, write expected observations for each stage and measurement explanation, including combinations.",
      "rationale": "Explicit predictions make subsequent comparisons assessable."
    },
    {
      "action": "During the fortnight, minimize avoidable staging and receiving delays within existing food-handling requirements; record any changes.",
      "rationale": "This is a limited precaution against possible exposure, not evidence that delays caused the exceptions."
    },
    {
      "action": "Use a common approved receiving method where it can provide reliable, comparable readings within staff capacity.",
      "rationale": "Standardization can improve interpretation, but approval or uniformity alone does not establish reliability."
    }
  ],
  "decision_rules": [
    {
      "condition": "Reliable package-linked observations distinguish temperatures before and after a stage.",
      "consequence": "Elevation already present before loading supports investigating staging/loading; a subsequent rise supports investigating the stage containing that rise.",
      "rationale": "These patterns inform monitored cases and may support multiple contributors; they do not establish a unique cause."
    },
    {
      "condition": "Interpretable observations are available.",
      "consequence": "Compare each explanation against them as consistent, inconsistent or indeterminate, recording reasons and confidence. Weight reliable contradictions by importance and treat repeated records within a delivery as dependent.",
      "rationale": "Supporting counts can exaggerate evidence and conceal consequential contradictions."
    },
    {
      "condition": "Readings or stage boundaries are uncertain.",
      "consequence": "Repeat comparisons excluding unreliable readings and varying plausible handoff times and sensor-response assumptions. Mark affected comparisons indeterminate when resolution, placement or comparability is inadequate.",
      "rationale": "Lag, clock/device errors, package variation and measurement locations can create apparent contradictions."
    }
  ],
  "important_distinctions": [
    {
      "distinction": "Surrounding-air temperature and package temperature are different measurements.",
      "consequence": "Use air records as contextual evidence without treating them as direct package-temperature readings."
    },
    {
      "distinction": "Evidence against an explanation in monitored cases differs from excluding it across operations.",
      "consequence": "Restrict any elimination to the conditions actually tested and supported by reliable evidence."
    }
  ],
  "constraints": [
    {
      "constraint": "Food-handling requirements remain in force and routine deliveries must continue.",
      "implication": "Monitoring and paired measurements must fit safe handling without delaying deliveries unnecessarily."
    },
    {
      "constraint": "Logger availability and added staff observations are limited to a two-week effort; fleet replacement is unfunded.",
      "implication": "Use selective monitoring and feasible handling changes, and explicitly report coverage gaps."
    }
  ],
  "do_not_conclude": [
    {
      "statement": "Missing or failed traces show that a stage was satisfactory.",
      "reason": "Absent evidence is inconclusive; retain only interpretable portions of affected records."
    },
    {
      "statement": "The fortnight necessarily ends with a causal diagnosis.",
      "reason": "Unstable rankings or inadequate coverage block a causal declaration. Sensitivity to omitted mechanisms, subjective judgments or shared assumptions requires an explicitly uncertain conclusion."
    }
  ]
}
```

### Augmented H7-T03-1

[Immutable response with hidden attribution metadata](../target-impact-v0.1/responses/augmented/H7-T03-1.json)

```json
{
  "current_position": {
    "statement": "The decline in second orders within eight weeks is a signal to investigate; its cause and the appropriate change remain unresolved.",
    "rationale": "Order records do not establish refill need. Promotions and new collection points changed together, and support messages cannot establish how common each problem is."
  },
  "top_uncertainties": [
    {
      "uncertainty": "Were nonreturning households ready to refill within eight weeks?",
      "why_it_matters": "Unused stock or a longer purchase interval requires a different response from an obstacle encountered after stock ran low."
    },
    {
      "uncertainty": "Does the decline reflect a changed customer mix, fulfillment problems, refill confusion or dissatisfaction?",
      "why_it_matters": "These explanations imply different investigations and changes."
    },
    {
      "uncertainty": "How representative are complaints and voluntary follow-up responses?",
      "why_it_matters": "Silent customers and nonparticipants may have different experiences; reported frequencies cannot establish population prevalence."
    }
  ],
  "next_inquiries": [
    {
      "inquiry": "Locate the decline in comparable customer groups.",
      "operation_or_observation": "Compare cohorts with a complete eight-week observation window, separating product, quantity, discount and fulfillment option. Compare individual collection points and starter versus existing-container orders only if identifiable in the records.",
      "decision_relevance": "Shows where to focus follow-up while checking whether acquisition mix or incomplete observation contributes to the apparent decline."
    },
    {
      "inquiry": "Distinguish lack of refill need from barriers to returning.",
      "operation_or_observation": "Invite a limited mix of repeat and nonrepeat customers across discounts and fulfillment options, including customers without support messages. Ask about remaining stock, use, expected refill timing, refill understanding, attempted collection, leaks and reasons for returning or not returning.",
      "decision_relevance": "Tests competing explanations without equating nonpurchase with dissatisfaction."
    },
    {
      "inquiry": "Establish whether refill need preceded a reported obstacle.",
      "operation_or_observation": "Keep recorded order dates fixed; distinguish reported events, date ranges and unknown intervals. Seek corroboration of stock status and obstacles through agreed follow-up. Compare calendar dates, time since first order and, where sufficiently dated, depletion.",
      "decision_relevance": "A supported sequence can distinguish some households with no refill need from those whose need preceded an obstacle; unresolved timing must remain unresolved."
    }
  ],
  "priorities": [
    {
      "rank": 1,
      "item": "Check cohort comparability and refill need.",
      "rationale": "These checks determine whether the eight-week measure reflects a service problem the team can address."
    },
    {
      "rank": 2,
      "item": "Identify a supported, changeable fulfillment or communication barrier.",
      "rationale": "Leaks, collection hours and refill confusion are inquiry leads; complaint counts alone cannot rank them."
    },
    {
      "rank": 3,
      "item": "Test one process change with an outcome observable before purchasing.",
      "rationale": "A month-long trial cannot establish a complete eight-week repeat rate for newly enrolled customers."
    }
  ],
  "immediate_actions": [
    {
      "action": "Use the first week to audit eligible cohorts and conduct limited voluntary follow-up.",
      "rationale": "This preserves approximately one month for a bounded trial before the five-week purchasing deadline."
    },
    {
      "action": "Before any trial, specify the eligible customers, one process change, a comparison where feasible, an observable success measure and a stop condition.",
      "rationale": "For example, test successful collection among households with established refill need if collection access is supported as the barrier. Avoid judging success solely by aggregate orders."
    }
  ],
  "decision_rules": [
    {
      "condition": "Inquiry sufficiently distinguishes a barrier addressable through one fulfillment or communication process.",
      "consequence": "Run the corresponding month-long change and assess the prespecified outcome before the purchasing commitment.",
      "rationale": "The intervention should follow evidence about the obstacle and fit the available time and authority."
    },
    {
      "condition": "No explanation is sufficiently distinguished.",
      "consequence": "Do not select a purported remedy or assume a retention uplift in the purchasing decision; carry the unresolved demand uncertainty explicitly.",
      "rationale": "An inconclusive inquiry does not justify treating a plausible explanation as established."
    },
    {
      "condition": "Recalled event timing permits equally plausible sequences or lacks reliable corroboration.",
      "consequence": "Leave the sequence unresolved; clarify only through agreed follow-up and never insert events or force dates to fit.",
      "rationale": "Chronology can narrow an explanation only within supported dates and event ordering."
    }
  ],
  "important_distinctions": [
    {
      "distinction": "No second order versus no refill need versus unmet refill need.",
      "consequence": "Establish stock status and expected timing before calling an order delayed or a household dissatisfied."
    },
    {
      "distinction": "A documented sequence versus a causal or population explanation.",
      "consequence": "Even corroborated need followed by an obstacle does not establish that the obstacle caused the overall decline or determines the best intervention."
    }
  ],
  "constraints": [
    {
      "constraint": "Follow-up is limited and voluntary; mandatory subscriptions and unsolicited repeated contact are excluded.",
      "implication": "Use agreed contact and preserve uncertainty about customers who do not participate."
    },
    {
      "constraint": "Purchasing is due in five weeks; only one fulfillment or communication process can change for a month, and major packaging redesign is unavailable.",
      "implication": "Keep the trial narrow and distinguish short-term process evidence from longer-term repeat-purchase evidence."
    }
  ],
  "do_not_conclude": [
    {
      "statement": "Nonpurchase or complaint frequency directly measures satisfaction.",
      "reason": "Neither establishes refill need, and most customers send no support message."
    },
    {
      "statement": "Promotions or new collection points caused the decline.",
      "reason": "They were introduced during the same quarter; subgroup differences alone cannot isolate their effects."
    }
  ]
}
```

### Augmented H7-T03-2

[Immutable response with hidden attribution metadata](../target-impact-v0.1/responses/augmented/H7-T03-2.json)

```json
{
  "current_position": {
    "statement": "The eight-week repeat-purchase decline is a signal requiring explanation, not an established decline in satisfaction.",
    "rationale": "Order records do not show household consumption, promotions and collection-point openings overlapped, and support messages cover only customers who contacted the service."
  },
  "top_uncertainties": [
    {
      "uncertainty": "How much nonpurchase reflects remaining stock or an expected refill interval longer than eight weeks?",
      "why_it_matters": "Customers without current need require a different response from customers prevented or discouraged from refilling."
    },
    {
      "uncertainty": "Does the decline concentrate in particular promotion, product, quantity or fulfillment groups?",
      "why_it_matters": "Customer mix and service difficulties suggest different changes; coincident introductions prevent simple causal attribution."
    },
    {
      "uncertainty": "Which difficulties prevent customers with refill needs from completing an order?",
      "why_it_matters": "Leaks, collection hours and refill confusion are candidate explanations, but complaint frequency does not establish their prevalence or effect."
    }
  ],
  "next_inquiries": [
    {
      "inquiry": "Locate the decline using comparable observation periods.",
      "operation_or_observation": "Compare first-order cohorts with a complete eight-week follow-up, grouped by recorded product, quantity, discount and fulfillment option. Examine collection-point differences only if records identify the points.",
      "decision_relevance": "Identifies where to focus follow-up without treating group differences as causal effects."
    },
    {
      "inquiry": "Distinguish delayed need from barriers and dissatisfaction.",
      "operation_or_observation": "Invite a limited, varied set of repeat and nonrepeat customers, including customers without support messages. Ask consenting participants about remaining stock, use, expected refill timing, satisfaction, difficulties and attempted refills or collections.",
      "decision_relevance": "Tests competing household-level explanations; voluntary responses cannot establish population prevalence."
    },
    {
      "inquiry": "Check whether each account supports an order-specific conclusion.",
      "operation_or_observation": "Link accounts to orders where possible. Record source, time or uncertain interval, purpose and order/product/container links. Establish starter status only with support; retain records, recollections, discrepancies and corrections separately.",
      "decision_relevance": "Corroborated stock or failed-attempt evidence can support a household-specific explanation. Missing links require clarification within agreed follow-up or exclusion from conclusions requiring those links."
    }
  ],
  "priorities": [
    {
      "rank": 1,
      "item": "Separate refill need from inability or reluctance to refill.",
      "rationale": "This distinction most directly determines whether a process change could help."
    },
    {
      "rank": 2,
      "item": "Select one supported, feasible fulfillment or communication difficulty.",
      "rationale": "The team can change only one process for a month before the purchasing deadline."
    }
  ],
  "immediate_actions": [
    {
      "action": "Use the first week for cohort analysis and voluntary follow-up; select the trial at the end of that week.",
      "rationale": "Reserves four weeks for a bounded change and review before the five-week purchasing deadline."
    },
    {
      "action": "Prepare a one-month trial specifying the affected customer group, changed step, comparison where feasible, success measure and rollback condition before launch.",
      "rationale": "For example, supported refill confusion could justify clearer refill instructions. Selection should depend on inquiry findings rather than complaint counts."
    }
  ],
  "decision_rules": [
    {
      "condition": "Reliable household evidence indicates remaining stock and a later expected refill date.",
      "consequence": "Treat delayed need as supported for that household and assess subsequent ordering against that timing.",
      "rationale": "An eight-week absence alone does not establish dissatisfaction or explain the aggregate decline."
    },
    {
      "condition": "Follow-up supports a recurring, actionable difficulty that one permitted process change can address.",
      "consequence": "Trial that change for one month. Record assignment if used, actual receipt, completion of the affected step and subsequent ordering separately.",
      "rationale": "A change cannot explain outcomes through a customer step unless relevant exposure and outcome links are supported."
    },
    {
      "condition": "The trial meets its predefined improvement criterion without unacceptable worsening, and the comparison supports the conclusion.",
      "consequence": "Retain the change provisionally; otherwise revert or treat the result as inconclusive. Make the purchasing commitment using explicit demand scenarios, without assuming an unobserved repeat-purchase recovery.",
      "rationale": "A month can reveal process improvement but cannot supply complete eight-week repeat outcomes for newly enrolled customers."
    }
  ],
  "important_distinctions": [
    {
      "distinction": "Missing documentation versus customer dissatisfaction.",
      "consequence": "Keep absent use histories and unresolved links classified as evidence gaps."
    },
    {
      "distinction": "A supported household explanation versus an explanation of the overall decline.",
      "consequence": "Preserve source traceability and check linkage quality; even reliable individual histories do not establish aggregate effects."
    }
  ],
  "constraints": [
    {
      "constraint": "Follow-up must be voluntary, with no mandatory subscription or unsolicited repeated contact.",
      "implication": "Keep contact and clarification within participants' agreement."
    },
    {
      "constraint": "Only one fulfillment or communication process can change for a month; purchasing is due in five weeks.",
      "implication": "Keep the trial narrow and report incomplete outcome windows explicitly."
    },
    {
      "constraint": "Major packaging redesign is unavailable within the decision period.",
      "implication": "Investigate leaks if relevant, but do not make the current plan depend on redesign."
    }
  ],
  "do_not_conclude": [
    {
      "statement": "Nonpurchase or complaint frequency directly measures satisfaction.",
      "reason": "Refill need is unknown, and most customers send no support message."
    },
    {
      "statement": "Promotions, new collection points or a selected process change caused the observed repeat-purchase pattern.",
      "reason": "Concurrent changes, customer selection and incomplete follow-up require a credible comparison before causal attribution."
    }
  ]
}
```

## Appendix C — Frozen blinded judgments

The following judgments are reproduced unchanged. Condition direction was added only in the separate unblinding records.

### PAIR-01

```json
{
  "impact_judgment": {
    "pair_id": "PAIR-01",
    "semantic_equivalence": "NO",
    "differences": [
      {
        "difference_id": "D01",
        "introduced_in": "A_ONLY",
        "categories": [
          "INQUIRY_CHANGE",
          "PRIORITY_CHANGE",
          "CONSTRAINT_CHANGE",
          "DECISION_RULE_CHANGE"
        ],
        "response_a": {
          "content": "Requires verification of package linkage, sensor meaning and response, clock alignment and handoffs before deployment. Paired measurements require checks on reference reliability and shared errors. Uncertain records trigger exclusion and sensitivity comparisons; inadequate comparisons remain indeterminate, and missing traces cannot establish satisfactory handling.",
          "response_locations": [
            "response_a.next_inquiries[0].operation_or_observation",
            "response_a.next_inquiries[2].operation_or_observation",
            "response_a.priorities[0]",
            "response_a.decision_rules[2]",
            "response_a.do_not_conclude[0]"
          ],
          "downstream_consequence": "Staff must resolve specified measurement-validity questions before using observations for attribution, and must test whether apparent stage patterns survive plausible timing and sensor assumptions."
        },
        "response_b": {
          "content": "Prioritizes comparable, package-linked readings and records placement and handling times, but does not specify these predeployment verification checks, sensitivity comparisons or missing-trace rules.",
          "response_locations": [
            "response_b.priorities[0]",
            "response_b.next_inquiries[0].operation_or_observation",
            "response_b.next_inquiries[1].operation_or_observation"
          ],
          "downstream_consequence": ""
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "A adds concrete evidence requests and prerequisites that can postpone attribution or render an apparent interval-specific result indeterminate; these go beyond B's general comparability requirement."
      },
      {
        "difference_id": "D02",
        "introduced_in": "A_ONLY",
        "categories": [
          "PROBLEM_REPRESENTATION_CHANGE",
          "ACTION_CHANGE",
          "PRIORITY_CHANGE",
          "DECISION_RULE_CHANGE"
        ],
        "response_a": {
          "content": "Requires expected observations for each explanation, including combinations, before reviewing results. It then classifies explanations as consistent, inconsistent or indeterminate, prioritizes reliable contradictions and discriminating observations, and treats repeated records within a delivery as dependent.",
          "response_locations": [
            "response_a.immediate_actions[0]",
            "response_a.priorities[1]",
            "response_a.decision_rules[1]"
          ],
          "downstream_consequence": "The team must prepare explicit predictions and evaluate evidence by its ability to distinguish explanations, rather than allowing numerous correlated supporting readings to dominate follow-up choices."
        },
        "response_b": {
          "content": "Compares operating contributors, repeats informative comparisons and uses emerging evidence to focus observations, without prescribing advance predictions, explicit explanation classifications or a dependence-aware contradiction assessment.",
          "response_locations": [
            "response_b.next_inquiries[2]",
            "response_b.priorities[2]"
          ],
          "downstream_consequence": ""
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "A introduces an actionable evidentiary structure and an immediate preparation task that can change which explanations remain live and which observations receive priority."
      },
      {
        "difference_id": "D03",
        "introduced_in": "B_ONLY",
        "categories": [
          "PROBLEM_REPRESENTATION_CHANGE",
          "INQUIRY_CHANGE",
          "CONSTRAINT_CHANGE"
        ],
        "response_a": {
          "content": "Tracks selected packages and pairs usual and standardized readings on a verified tracked package. It mentions package variation as a possible source of apparent contradictions but does not explicitly request additional packages within sampled deliveries or impose a delivery-wide representativeness rule.",
          "response_locations": [
            "response_a.next_inquiries[1].operation_or_observation",
            "response_a.next_inquiries[2].operation_or_observation",
            "response_a.decision_rules[2].rationale"
          ],
          "downstream_consequence": ""
        },
        "response_b": {
          "content": "Documents receiving package selection, adds readings from additional packages where feasible, and explicitly distinguishes one package reading from a delivery-wide assessment.",
          "response_locations": [
            "response_b.top_uncertainties[1]",
            "response_b.next_inquiries[1]",
            "response_b.important_distinctions[1]"
          ],
          "downstream_consequence": "Some limited observation capacity goes to within-delivery package comparisons, and a single reading cannot be used to characterize every package in the delivery."
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "B makes within-delivery variation a direct sampling question and establishes a corresponding inference boundary, rather than merely acknowledging package variation as measurement uncertainty."
      },
      {
        "difference_id": "D04",
        "introduced_in": "BOTH_DIFFERENT",
        "categories": [
          "DECISION_RULE_CHANGE",
          "ACTION_CHANGE"
        ],
        "response_a": {
          "content": "Reliable package-linked observations distinguishing temperatures before and after a stage support investigating the stage involved, without establishing a unique cause.",
          "response_locations": [
            "response_a.decision_rules[0]"
          ],
          "downstream_consequence": "An interpretable observed rise can redirect investigation to an interval, but this rule does not itself authorize a targeted corrective intervention."
        },
        "response_b": {
          "content": "Repeated, comparable observations locating increases within an interval trigger corrective action and further monitoring at that interval.",
          "response_locations": [
            "response_b.decision_rules[0]"
          ],
          "downstream_consequence": "Once an interval-specific pattern is repeated, the team proceeds to a targeted handling correction as well as additional monitoring."
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "The rules differ both in their stated evidentiary trigger and in what that trigger authorizes: investigation in A versus corrective action plus monitoring in B."
      },
      {
        "difference_id": "D05",
        "introduced_in": "B_ONLY",
        "categories": [
          "DECISION_RULE_CHANGE"
        ],
        "response_a": {
          "content": "Says unstable rankings or inadequate coverage block a causal declaration at the end of the fortnight, but does not give an explicit end-of-period rule for retaining precautions and continuing focused sampling.",
          "response_locations": [
            "response_a.do_not_conclude[1]",
            "response_a.immediate_actions[1]",
            "response_a.priorities[1]"
          ],
          "downstream_consequence": ""
        },
        "response_b": {
          "content": "If the two-week sample remains mixed or inconclusive, retain proportionate precautions and focus further sampling on unresolved intervals or conditions.",
          "response_locations": [
            "response_b.decision_rules[2]"
          ],
          "downstream_consequence": "Inconclusive results trigger continued precautions and a focused follow-up sampling effort rather than only an uncertain conclusion."
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "Both responses resist unsupported diagnosis, but B additionally specifies the operational response to unresolved uncertainty at the two-week decision point."
      },
      {
        "difference_id": "D06",
        "introduced_in": "BOTH_DIFFERENT",
        "categories": [
          "ACTION_CHANGE",
          "DECISION_RULE_CHANGE"
        ],
        "response_a": {
          "content": "Immediately recommends a common approved receiving method wherever it can provide reliable, comparable readings within staff capacity.",
          "response_locations": [
            "response_a.immediate_actions[2]"
          ],
          "downstream_consequence": "Receiving-method standardization can begin before new evidence shows that procedure or delay contributes to exceptions."
        },
        "response_b": {
          "content": "Adds a common measurement procedure on sampled deliveries, then explicitly calls for standardizing the relevant receiving practice and reassessing exceptions if reported exceptions vary with procedure or measurement delay.",
          "response_locations": [
            "response_b.next_inquiries[1].operation_or_observation",
            "response_b.decision_rules[1]"
          ],
          "downstream_consequence": "The explicit rule for changing relevant receiving practice is tied to observed procedure or delay effects, while common measurements already begin within the investigation."
        },
        "materially_changes_target_reasoning": "UNCERTAIN",
        "rationale": "The responses may differ in the timing or scope of operational standardization, but A does not specify its breadth and B already introduces a common procedure during sampling. The practical difference is therefore unresolved."
      }
    ],
    "overall_material_difference": "YES",
    "rationale": "The responses share the unresolved-cause assessment, selective tracing strategy and proportionate interim precautions. Material differences remain in measurement-validation prerequisites, hypothesis evaluation, within-delivery sampling, the trigger for targeted correction and the response to an inconclusive fortnight."
  }
}
```

### PAIR-02

```json
{
  "impact_judgment": {
    "pair_id": "PAIR-02",
    "semantic_equivalence": "NO",
    "differences": [
      {
        "difference_id": "D1",
        "introduced_in": "B_ONLY",
        "categories": [
          "PROBLEM_REPRESENTATION_CHANGE",
          "INQUIRY_CHANGE",
          "CONSTRAINT_CHANGE"
        ],
        "response_a": {
          "content": "A assesses replenishment readiness and attempted reorders but does not specify reconstructing event chronology, corroborating dates, or comparing alternative event sequences.",
          "response_locations": [
            "next_inquiries[1]",
            "important_distinctions[0]"
          ],
          "downstream_consequence": ""
        },
        "response_b": {
          "content": "B distinguishes recorded dates, recalled events, date ranges and unknown intervals; seeks corroboration; and compares calendar time, time since first order and sufficiently dated depletion. Ambiguous or uncorroborated sequences must remain unresolved.",
          "response_locations": [
            "next_inquiries[2]",
            "decision_rules[2]",
            "important_distinctions[1]"
          ],
          "downstream_consequence": "The team would gather timing and corroboration evidence to determine whether refill need preceded an obstacle, withholding a sequence-based explanation when multiple orderings remain plausible."
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "B adds a specific temporal evidence structure with additional inquiry and explicit limits on conclusions drawn from recalled chronology."
      },
      {
        "difference_id": "D2",
        "introduced_in": "A_ONLY",
        "categories": [
          "INQUIRY_CHANGE"
        ],
        "response_a": {
          "content": "A asks willing participants to describe a recent collection or demonstrate how they would arrange a refill, reviewing relevant support messages alongside these accounts.",
          "response_locations": [
            "next_inquiries[2]"
          ],
          "downstream_consequence": "The team could observe how a customer attempts the refill task and use concrete task difficulties to select a process change."
        },
        "response_b": {
          "content": "B asks about refill understanding, attempted collection and obstacles, but does not request a demonstration of arranging a refill.",
          "response_locations": [
            "next_inquiries[1]",
            "next_inquiries[2]"
          ],
          "downstream_consequence": ""
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "A introduces a behavioral demonstration that can supply different evidence from reported understanding or corroborated event timing."
      },
      {
        "difference_id": "D3",
        "introduced_in": "B_ONLY",
        "categories": [
          "INQUIRY_CHANGE"
        ],
        "response_a": {
          "content": "A compares cohorts by product, quantity, discount and fulfillment option, with starter versus refill purchases separated if possible. It does not explicitly compare individual collection points.",
          "response_locations": [
            "next_inquiries[0]"
          ],
          "downstream_consequence": ""
        },
        "response_b": {
          "content": "B additionally compares individual collection points if they are identifiable in the records.",
          "response_locations": [
            "next_inquiries[0].operation_or_observation",
            "next_inquiries[0].decision_relevance"
          ],
          "downstream_consequence": "Where records permit, the team would investigate differences between collection locations and use them to focus customer follow-up."
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "Comparing individual locations adds a discriminating comparison beyond separating delivery from collection."
      },
      {
        "difference_id": "D4",
        "introduced_in": "A_ONLY",
        "categories": [
          "DECISION_RULE_CHANGE"
        ],
        "response_a": {
          "content": "If follow-up indicates substantial remaining stock and later expected replenishment, A directs the team to plan purchasing around a range of replenishment intervals.",
          "response_locations": [
            "decision_rules[0]"
          ],
          "downstream_consequence": "Evidence of slower consumption would explicitly change the timing assumptions used for the purchasing commitment."
        },
        "response_b": {
          "content": "B investigates remaining stock and expected refill timing and carries unresolved demand uncertainty into purchasing, but supplies no corresponding purchasing rule for supported evidence of later replenishment.",
          "response_locations": [
            "next_inquiries[1]",
            "decision_rules[1]",
            "important_distinctions[0]"
          ],
          "downstream_consequence": ""
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "A connects a particular inquiry result to a concrete change in purchasing assumptions, beyond recognizing that nonpurchase may reflect lack of need."
      },
      {
        "difference_id": "D5",
        "introduced_in": "A_ONLY",
        "categories": [
          "DECISION_RULE_CHANGE",
          "CONSTRAINT_CHANGE"
        ],
        "response_a": {
          "content": "A permits provisional continuation when the trial meets its predefined criterion, has supporting comparison evidence where feasible, and causes no material service deterioration; later repeat orders should then be monitored.",
          "response_locations": [
            "decision_rules[2]"
          ],
          "downstream_consequence": "The team has an explicit post-trial continuation rule, including a service-deterioration condition that can prevent continuation despite meeting the success measure."
        },
        "response_b": {
          "content": "B requires a prespecified success measure and stop condition and assessment before purchasing, but does not state a post-trial continuation rule or an explicit service-deterioration condition.",
          "response_locations": [
            "immediate_actions[1]",
            "decision_rules[0]"
          ],
          "downstream_consequence": ""
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "A specifies what evidence supports continuing the change and an additional condition that can withhold continuation."
      }
    ],
    "overall_material_difference": "YES",
    "rationale": "The responses share the core inquiry into comparable cohorts, refill need and actionable barriers. They differ materially in temporal corroboration, task demonstration, location-level comparison, and explicit rules for purchasing assumptions and post-trial continuation."
  }
}
```

### PAIR-03

```json
{
  "impact_judgment": {
    "pair_id": "PAIR-03",
    "semantic_equivalence": "NO",
    "differences": [
      {
        "difference_id": "D1",
        "introduced_in": "B_ONLY",
        "categories": [
          "INQUIRY_CHANGE"
        ],
        "response_a": {
          "content": "Groups cohort comparisons by recorded order characteristics, including fulfillment option, but does not explicitly compare individual collection points.",
          "response_locations": [
            "response_a.next_inquiries[0].operation_or_observation"
          ],
          "downstream_consequence": ""
        },
        "response_b": {
          "content": "Adds collection-point comparisons when records identify the points.",
          "response_locations": [
            "response_b.next_inquiries[0].operation_or_observation"
          ],
          "downstream_consequence": "Could focus follow-up on particular collection points rather than treating collection fulfillment as one group."
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "This adds a conditional comparison capable of distinguishing local collection difficulties from a broader fulfillment pattern."
      },
      {
        "difference_id": "D2",
        "introduced_in": "B_ONLY",
        "categories": [
          "INQUIRY_CHANGE"
        ],
        "response_a": {
          "content": "Asks about stock, use, timing, attempted reorders and specific difficulties, without explicitly asking about satisfaction.",
          "response_locations": [
            "response_a.next_inquiries[1].operation_or_observation"
          ],
          "downstream_consequence": ""
        },
        "response_b": {
          "content": "Explicitly asks consenting participants about satisfaction alongside stock, use, timing and difficulties.",
          "response_locations": [
            "response_b.next_inquiries[1].operation_or_observation"
          ],
          "downstream_consequence": "Collects direct self-reports relevant to dissatisfaction or reluctance even when no specific fulfillment obstacle is reported."
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "The additional question gathers evidence about a live explanation that stock and task-barrier questions alone do not directly assess."
      },
      {
        "difference_id": "D3",
        "introduced_in": "A_ONLY",
        "categories": [
          "INQUIRY_CHANGE"
        ],
        "response_a": {
          "content": "Asks willing participants to describe a recent collection or demonstrate arranging a refill, and reviews relevant support messages alongside their accounts.",
          "response_locations": [
            "response_a.next_inquiries[2].operation_or_observation"
          ],
          "downstream_consequence": "A refill demonstration can reveal where understanding or execution fails, providing concrete evidence for selecting the process change."
        },
        "response_b": {
          "content": "Asks about difficulties and attempted refills or collections, but does not propose a refill demonstration or reviewing support messages alongside those accounts.",
          "response_locations": [
            "response_b.next_inquiries[1].operation_or_observation",
            "response_b.next_inquiries[2].operation_or_observation"
          ],
          "downstream_consequence": ""
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "Demonstrating the refill task is a distinct evidence-gathering operation from reporting difficulties or validating account links."
      },
      {
        "difference_id": "D4",
        "introduced_in": "B_ONLY",
        "categories": [
          "PROBLEM_REPRESENTATION_CHANGE",
          "INQUIRY_CHANGE",
          "CONSTRAINT_CHANGE",
          "DECISION_RULE_CHANGE"
        ],
        "response_a": {
          "content": "Uses voluntary accounts to distinguish replenishment readiness and barriers, acknowledges selective participation, and uses later replenishment evidence to inform purchasing ranges. It does not require account-to-order linkage or prescribe handling unresolved links.",
          "response_locations": [
            "response_a.next_inquiries[1]",
            "response_a.decision_rules[0]",
            "response_a.important_distinctions[1]"
          ],
          "downstream_consequence": ""
        },
        "response_b": {
          "content": "Records sources, times and order/product/container links; separates records, recollections, discrepancies and corrections; requires clarification or exclusion when necessary links are missing. It distinguishes supported household explanations from explanations of the aggregate decline and assesses later ordering against supported household timing.",
          "response_locations": [
            "response_b.next_inquiries[2]",
            "response_b.decision_rules[0]",
            "response_b.important_distinctions[0]",
            "response_b.important_distinctions[1]"
          ],
          "downstream_consequence": "Adds linkage and clarification work, withholds conclusions requiring unresolved links, and restricts reliable individual histories to household-level explanations unless aggregate support is established."
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "The evidentiary structure changes which accounts can support particular conclusions and what follow-up is needed before using them."
      },
      {
        "difference_id": "D5",
        "introduced_in": "BOTH_DIFFERENT",
        "categories": [
          "INQUIRY_CHANGE",
          "ACTION_CHANGE",
          "CONSTRAINT_CHANGE"
        ],
        "response_a": {
          "content": "Tracks the targeted barrier, successful refill or collection attempts, observed orders and participants' remaining stock.",
          "response_locations": [
            "response_a.immediate_actions[2]"
          ],
          "downstream_consequence": "The trial explicitly gathers continuing stock information to interpret observed demand alongside process outcomes."
        },
        "response_b": {
          "content": "Separately records assignment if used, actual receipt of the change, completion of the affected step and subsequent ordering, and requires supported exposure and outcome links for explaining outcomes through that step.",
          "response_locations": [
            "response_b.decision_rules[1]"
          ],
          "downstream_consequence": "The trial distinguishes assignment from actual exposure and step completion, withholding a process-based explanation when the necessary links are unsupported."
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "These are different trial measurement requirements: A explicitly follows remaining stock, while B explicitly follows intervention exposure and its connection to outcomes."
      },
      {
        "difference_id": "D6",
        "introduced_in": "BOTH_DIFFERENT",
        "categories": [
          "DECISION_RULE_CHANGE",
          "CONSTRAINT_CHANGE"
        ],
        "response_a": {
          "content": "Continues the change provisionally when its predefined criterion is met without material service deterioration, using supporting comparison evidence where feasible.",
          "response_locations": [
            "response_a.decision_rules[2]"
          ],
          "downstream_consequence": "Allows provisional continuation without a supporting comparison when such a comparison is infeasible."
        },
        "response_b": {
          "content": "Requires the improvement criterion, acceptable worsening and a supporting comparison for provisional retention; otherwise it directs reversion or an inconclusive judgment.",
          "response_locations": [
            "response_b.decision_rules[2]",
            "response_b.do_not_conclude[1]"
          ],
          "downstream_consequence": "A trial meeting its process criterion without a supporting comparison does not qualify for provisional retention under the stated rule."
        },
        "materially_changes_target_reasoning": "YES",
        "rationale": "Although both prepare comparisons where feasible, their final continuation rules impose different requirements when comparison evidence is unavailable or unsupportive."
      }
    ],
    "overall_material_difference": "YES",
    "rationale": "The responses share the central distinction between nonpurchase and dissatisfaction and propose similarly bounded trials. They nevertheless differ in specific inquiries, evidence-linkage requirements, trial measurements and the evidence required to retain a change. These differences can alter what is gathered, which conclusions are withheld and what happens after the trial."
  }
}
```
