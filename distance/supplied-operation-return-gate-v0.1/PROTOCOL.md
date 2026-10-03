# H6.R4 — Minimal supplied-operation return-gate calibration

Base: `c76f645d5fcbf150f1a009df0dd2c48213319b6e` on
`policy-evaluator-stop-rule`. Work and push only
`experiment-h6r4-operation-return-gate`; do not merge to main.
H.6, H6.R1/R2/R3 and the evaluator-stop policy remain byte-for-byte unchanged.

## Evaluator-work gate

**Observed decision failure:**
A TARGET_SUPPLIED or SOURCE_SUPPLIED operation can be actively prescribed by the mapping yet receive only fidelity treatment, allowing a mechanism-incompatible, irrelevant, or inapplicable action to survive without OPERATION_LICENSE.

**Admission consequence:**
supplied operation
→ no functional operation scrutiny
→ invalid action retained as acceptable claim
→ potentially false-retained transfer or corrupted surviving remainder

**Minimum intervention:**
Route an asserted supplied operation through its fidelity contract plus OPERATION_LICENSE, while leaving a merely referenced supplied premise as GROUNDING_REF. Test exactly one negative supplied operation, one positive supplied operation, and one referenced-premise control.

**Scientific success evidence:**
1. Negative supplied operation: fidelity SATISFIED + OPERATION_LICENSE VIOLATED + overall VIOLATED.
2. Positive supplied operation: fidelity SATISFIED + OPERATION_LICENSE SATISFIED + overall SATISFIED.
3. Referenced supplied premise: GROUNDING_REF only, with no unnecessary functional warrant obligation.

**Stop condition:**
If all three observations are scientifically interpretable and pass as specified, and no remaining issue has a concrete demonstrated admission consequence, stop evaluator calibration and return to fresh natural-transfer testing.

## Scope and selection

Exactly three scientific observations: one negative supplied operation, one
positive supplied operation and one unchanged supplied referenced premise. No
fourth case, post-result expansion or post-hoc replacement. Prefer frozen H.6
natural mappings/claims, then H6.R1 natural claims, then other frozen natural
output. H6.R2/R3 synthetic controls cannot silently replace missing natural cases.

Use content and frozen source/target conditions for offline selection, not old
warrant status. Inspect the exact proposition, scope, mapping use and positive
evidence of supply. A negative requires an already inspectable incompatible,
irrelevant or inapplicable operation while fidelity remains satisfied. A generated
recommendation mislabeled as supplied cannot establish this contrast. A possible
failure obtained only by removing a condition is not a clean candidate.

If classification is genuinely uncertain, reject that candidate before measurement
and inspect another natural candidate. Do not add origins/functions, redesign
governance or remainder viability, expand compound-obligation machinery, reopen
H.5, or create a classification experiment.

**If any slot lacks a clean natural candidate, stop before provider measurement
at step 5 below.** Freeze the scan and absent slot. Do not promote a partial
shortlist into the three-case scientific selection. A later narrow synthetic
substitute requires explicit user authorization. Do not fabricate natural lineage.

## Evidence records and blindness

[EVIDENCE-RECORD.md](EVIDENCE-RECORD.md) and
[evidence-record.schema.json](evidence-record.schema.json) define the prospective
case record. Record original identity/text/scope, source experiment, exact source
references and file hashes, classification, routing, selection reason and hidden
operator hypotheses. Hypotheses are not scientific verdicts. Screening records
are not measurements or extra scientific cases.

Provider packets may contain only neutral case/obligation identity, the exact
claim and scope, the relevant contract, the prospective response schema and the
frozen obligation evidence bundle. Exclude selection reason, expected contracts
as a hypothesis, expected verdicts, old H.6 warrant status, historical evaluator
interpretation and previous stage reasoning/verdicts. Selection files are never
passed wholesale to a provider.

## Routing and interface

[ROUTING.md](ROUTING.md) freezes the only scientific correction and the unchanged
contracts. Supplied asserted operations receive the corresponding fidelity
contract plus OPERATION_LICENSE. Supplied REFERENCED_PREMISE receives GROUNDING_REF
with no provider obligation merely for that reference.

The frozen input bundle owns source IDs and SUPPORT/CONTEXT roles. Before every
scientific call, verify equality of the obligation's source-ID set and the rendered
packet's allowed source-ID set, and exact equality of associated roles and
harness-owned source text. Verify source-file and selected-text hashes against
their frozen lineage. No added, removed, substituted or wrong-packet source is
permitted. A source ID is local to its frozen case/evidence namespace, not an
unqualified identifier across experiments.

Responses use [response.schema.json](response.schema.json): `evidence_used`
contains objects with `source_id` only. Every cited ID must belong to that frozen
obligation's allowed set. Validate this membership against the frozen bundle, not
just JSON syntax. No response-side SUPPORT/CONTEXT echo is requested or compared.
Do not reject a judgment solely for a different role word in its prose. This is
an interface simplification, not another provenance calibration; input roles and
text remain strict. Unknown response IDs are preserved and pause measurement.

## Measurement stages

**A — offline classification:** freeze origin, function, assertion mode and routing
for all three selected cases before any provider work. Classification uncertainty
blocks that candidate; no classifier session is authorized.

**B — fidelity:** one fresh isolated GPT-6 Astra/high judgment per asserted
operation, preferably two fresh judgments in total. Exact uncontested frozen
role-specific fidelity may be reused only under the identical contract,
proposition and evidence, with provenance recorded before measurement. Freeze
both fidelity judgments before any operation evaluation. VIOLATED or UNCERTAIN
fidelity does not establish the supplied-operation contrast; preserve the result,
block the return gate and do not replace the case. CONDITIONAL also fails the
required SATISFIED pattern. Stop further calls if this necessary gate has failed.

**C — operation license:** one fresh isolated Astra/high judgment for each
asserted operation, with its operation claim, source mechanism, target applicability
context and frozen allowed sources. No historical or Stage B verdicts. Freeze
both before aggregation. No grounding provider call is needed merely to reference
a premise. If a proposed premise actually restates an assertion requiring fidelity,
resolve that before selection; do not silently increase this plan's fan-out.

**D — aggregation:** use existing precedence
`VIOLATED > UNCERTAIN > CONDITIONAL > SATISFIED`. Missing observations remain null
and cannot become a scientific verdict. Grounding-only has no scientific verdict.

## Return decision and diagnostics

PASS requires all three:

- Negative: fidelity SATISFIED, OPERATION_LICENSE VIOLATED, overall VIOLATED.
- Positive: fidelity SATISFIED, OPERATION_LICENSE SATISFIED, overall SATISFIED.
- Referenced premise: GROUNDING_REF and no unnecessary FACT_WARRANT,
  DERIVED_WARRANT, OPERATION_LICENSE, CONDITIONAL_LICENSE or LIMIT_WARRANT.

No aggregate score or perfect metadata requirement. If all pass and no remaining
observed issue has a demonstrated admission consequence: **The known
supplied-operation decision-boundary defect is adequately resolved for purposes
of returning to natural-output testing. Stop evaluator refinement.** Recommend
fresh natural-transfer admission testing next, subject to separate authorization
and budget/usage gates; do not execute it.

BLOCKED requires a concrete admission-relevant defect and must name the actual
decision-boundary problem and minimum intervention. Unfinished measurement is
INCOMPLETE; a missing natural negative case leaves the known false-retention path
untested but is not itself a measured evaluator defect. Representation/interface
imperfections without scientific classification effects do not block return.
The compact decision rule below controls the final return-gate status.

Use only SUPPLIED_OPERATION_LICENSE_MISSING, SUPPLIED_OPERATION_OVERSTRICT,
SUPPLIED_PREMISE_OVERTRIGGER, GROUNDING_REF_MISCLASSIFICATION,
INPUT_PROVENANCE_FAILURE, RESPONSE_SOURCE_UNKNOWN and RETURN_GATE_BLOCKED.
Report counts with denominators. Zero observed failures with zero measurements is
not a pass. Do not expand diagnostic vocabulary without a measured gate need.

## Provider, budget and recovery

Only OpenAI GPT-6 Astra with high reasoning, fresh isolated contexts, serial calls,
no tools, duplicate sampling, model substitutions, probes or retries. Capacity or
transport failure pauses further scheduling, preserves the attempt and is reported;
do not formalize a general no-observation policy. Never repair scientific responses.

Follow [the budget gate](../../docs/EXPERIMENT-BUDGET-GATE.md),
[usage preflight](../../docs/USAGE-FORECAST.md) and
[recovery policy](../../docs/EXPERIMENT-RECOVERY-POLICY.md). After selection and
packet freeze, calculate the actual cumulative plan (normally two fidelity plus
two operation sessions), include unknown costs explicitly, and present its hash,
session limits and fresh percentage-point scenarios. Preserve the 10-point reserve.
Obtain any required financial and usage approval before dispatch. Each launch must
reserve through the shared Gate immediately before the provider call. Refresh
usage before each stage and bounded batch of at most two calls, retaining matched
before/after calibration bookkeeping under `.runtime/`; no extra calibration calls.

Selection failure creates no executable provider plan and needs no account reads
or spending approval. Premeasurement engineering corrections may occur before
their freeze; measured cases, input lineage and observations cannot be repaired
or replaced. Frozen historical experiments stay frozen regardless of approval.

## Freeze sequence

1. Freeze this evaluator-work gate.
2. Freeze supplied-operation routing correction.
3. Freeze source-ID-only response interface and evidence-record schema.
4. Freeze offline natural candidate scan.
5. Freeze exactly three selected cases, or stop with absent slots recorded.
6. Freeze routing/classification records for the complete selection.
7. Freeze provider packets and premeasurement checks.
8. Run budget/usage gates and obtain required approval.
9. Freeze fidelity judgments.
10. Freeze operation-license judgments.
11. Freeze mechanical aggregation.
12. Evaluate the natural-output return gate.
13. Complete the report.

Before measurement, verify both supplied-operation routes; supplied-premise
grounding; no grounding calls; response source-ID shape and allowed-ID membership;
exact input projection; no post-hoc case replacement; and historical preservation.
If step 5 fails, do not build an unused provider runner or proceed to steps 6–11.
Report the selection blocker and stop. This does not claim the premeasurement
execution checks passed.

## Return-gate evidence record

Create `distance/supplied-operation-return-gate-v0.1/return-gate-evidence.yaml`
with this compact schema (the alternatives below describe allowed values):

```yaml
return_gate_evidence:
  experiment_id: H6.R4

  status:
    IN_PROGRESS |
    COMPLETE

  cases:

    negative_supplied_operation:
      case_id: string
      source_experiment: string
      original_claim_id: string | null

      frozen_classification:
        content_origin:
          TARGET_SUPPLIED |
          SOURCE_SUPPLIED
        epistemic_function: OPERATION
        assertion_mode: ASSERTED_COMPONENT

      expected_contracts:
        - TARGET_FIDELITY | SOURCE_FIDELITY
        - OPERATION_LICENSE

      observed_verdicts:
        fidelity:
          SATISFIED |
          CONDITIONAL |
          VIOLATED |
          UNCERTAIN |
          UNMEASURED
        operation_license:
          SATISFIED |
          CONDITIONAL |
          VIOLATED |
          UNCERTAIN |
          UNMEASURED
        overall:
          SATISFIED |
          CONDITIONAL |
          VIOLATED |
          UNCERTAIN |
          INCOMPLETE

      expected_pattern:
        fidelity: SATISFIED
        operation_license: VIOLATED
        overall: VIOLATED

      passed: true | false | null
      blocker: string | null

    positive_supplied_operation:
      case_id: string
      source_experiment: string
      original_claim_id: string | null

      frozen_classification:
        content_origin:
          TARGET_SUPPLIED |
          SOURCE_SUPPLIED
        epistemic_function: OPERATION
        assertion_mode: ASSERTED_COMPONENT

      expected_contracts:
        - TARGET_FIDELITY | SOURCE_FIDELITY
        - OPERATION_LICENSE

      observed_verdicts:
        fidelity:
          SATISFIED |
          CONDITIONAL |
          VIOLATED |
          UNCERTAIN |
          UNMEASURED
        operation_license:
          SATISFIED |
          CONDITIONAL |
          VIOLATED |
          UNCERTAIN |
          UNMEASURED
        overall:
          SATISFIED |
          CONDITIONAL |
          VIOLATED |
          UNCERTAIN |
          INCOMPLETE

      expected_pattern:
        fidelity: SATISFIED
        operation_license: SATISFIED
        overall: SATISFIED

      passed: true | false | null
      blocker: string | null

    supplied_referenced_premise:
      case_id: string
      source_experiment: string
      original_claim_id: string | null

      frozen_classification:
        content_origin:
          TARGET_SUPPLIED |
          SOURCE_SUPPLIED
        epistemic_function:
          FACT |
          INFERENCE |
          CONDITIONAL_RELATION |
          OPERATION |
          GOVERNANCE_RULE |
          LIMIT
        assertion_mode: REFERENCED_PREMISE

      expected_resolution: GROUNDING_REF

      forbidden_contracts:
        - FACT_WARRANT
        - DERIVED_WARRANT
        - OPERATION_LICENSE
        - CONDITIONAL_LICENSE
        - LIMIT_WARRANT

      observed:
        resolution:
          GROUNDING_REF |
          CLAIM_REF |
          INLINE_OBLIGATION |
          UNRESOLVED
        generated_contracts: []
        overall:
          SATISFIED |
          CONDITIONAL |
          VIOLATED |
          UNCERTAIN |
          INCOMPLETE |
          NOT_APPLICABLE

      expected_pattern:
        resolution: GROUNDING_REF
        generated_contracts: []

      passed: true | false | null
      blocker: string | null

  diagnostics:
    SUPPLIED_OPERATION_LICENSE_MISSING: 0
    SUPPLIED_OPERATION_OVERSTRICT: 0
    SUPPLIED_PREMISE_OVERTRIGGER: 0
    GROUNDING_REF_MISCLASSIFICATION: 0
    INPUT_PROVENANCE_FAILURE: 0
    RESPONSE_SOURCE_UNKNOWN: 0

  final_decision:
    status:
      PASS |
      BLOCKED |
      INCOMPLETE

    criteria:
      negative_case_passed: true | false | null
      positive_case_passed: true | false | null
      referenced_premise_passed: true | false | null
      scientifically_interpretable: true | false | null
      remaining_admission_blocker: true | false | null

    blocker: string | null

    next_scientific_work:
      FRESH_NATURAL_TRANSFER_TEST |
      MINIMUM_EVALUATOR_CORRECTION |
      NONE_YET
```

Freeze the decision rule (`negative_case` and `positive_case` refer to the two
supplied-operation records above):

```text
PASS iff:

negative_case.passed = true
AND positive_case.passed = true
AND supplied_referenced_premise.passed = true
AND scientifically_interpretable = true
AND remaining_admission_blocker = false
```

Otherwise use INCOMPLETE when measurement did not finish, or BLOCKED only when
there is a concrete admission-relevant defect. For BLOCKED, `blocker` must identify
the actual decision-boundary problem, not incidental citation/schema/interface
imperfections. Unmeasured cases have `passed: null`; absence of a demonstrated
defect does not establish `remaining_admission_blocker: false`.

For PASS, require:

```yaml
final_decision:
  status: PASS
  blocker: null
  next_scientific_work: FRESH_NATURAL_TRANSFER_TEST
```

This record summarizes the already-frozen three-observation criterion. It adds no
evaluation layer, provider calls, scoring system or calibration. IN_PROGRESS
indicates incomplete scientific evidence; it is not an instruction to resume a
stopped experiment. Expected patterns are never observations.

Preselection availability: the schema above describes selected cases. When the
experiment stops before a complete selection, use null for an unavailable case
identity, source experiment, frozen classification or exact contract list. This
is a record-availability exception, not a new origin/function category. Existing
shortlist IDs may be cited as screening references, but their provisional
classifications must not be presented as frozen. Keep pass criteria null and
operation observations UNMEASURED/INCOMPLETE. The referenced-premise observation
is UNRESOLVED/INCOMPLETE until its classification/routing is frozen; an empty
contract list alone does not establish a pass. The current selection stop remains
in effect. The original scan's BLOCKED wording is retained as checkpoint evidence
and superseded for the current return decision by this clarification.

## Final report

Report base, branch and checkpoint SHAs; selected natural claims; each case's
classification, contracts/resolution and observed verdicts; diagnostic counts;
provider/budget incidents; response-interface and strict input-provenance status;
and the compact return decision. Distinguish UNMEASURED/INCOMPLETE from scientific
failure. If PASS, state that evaluator refinement stops and recommend fresh
natural-transfer testing, subject to separate authorization. If BLOCKED, name only
the concrete admission-relevant defect and minimum justified intervention. Do not
execute the recommendation. The completion report also states final SHA, branch
pushed, three-case selection status and provider session count.
