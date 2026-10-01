# Experiment H.4 — Inquiry-unitization and mandatory role coverage v0.1

All 18 fresh assessments were preserved, but H.4 has validation failures. The deterministic coverage guard operates; the complete annotation instrument is not ready to return to remainder-viability or natural-output measurement.

## Lineage and frozen checkpoints

Base `8f488b3b02973370e26fd970a5fd5a8d56e8bec6` on `experiment-h3-negative-remainders`. Publication branch: `experiment-h4-inquiry-unitization`. No main merge.
The final SHA is the commit containing publication-manifest.json; metrics.json gives its resolution command.

| Checkpoint | SHA |
|---|---|
| schema_and_rule | `692de78579b91666c2bca76507d3c4177769c20a` |
| primary_cases | `41852bc6ef9f8da731fce09e66f25e5e73dacb23` |
| six_controls | `7e7b50dc4503a0b6f707c10c3fb048ebb7b78b81` |
| h3_regression_fixtures | `d7a282a92dd43fce2d33ffb79f0b017c78adcc25` |
| extractor_and_tests_initial | `08924e53f222fa1a2992e84dce4e92b6361f0e12` |
| final_extractor_and_packets | `3a8436ce6275ab74b77196f40c7bbed0b58cca41` |
| preflight | `cf5a35635e120c048a57c3d3b8d65b02bf6e3af6` |
| eighteen_judgments | `7a0311673cebe9f90870484ea6917d5f794b1818` |
| coverage_validation | `dcda6092e39c184048161ec60ddac1ff0417d652` |

## Frozen rule and forcing invariant

Inquiry-role annotation is semantic rather than polarity-based. A surviving inquiry constraint exists whenever the mapping explicitly preserves (a) an unresolved set of live alternatives, (b) a specific next operation, and (c) an outcome relation under which possible results bear differently on those alternatives. These elements may occur in affirmative or negative language and may span multiple clauses. Every such complete unit must receive INQUIRY_CONSTRAINT role assessment regardless of any negative_inference flag. Mere non-discrimination language remains INSUFFICIENCY_ONLY when no complete discriminating inquiry unit is supplied.

```python
complete_inquiry_unit = (
    unresolved_contrast.present is True
    and len(unresolved_contrast.alternatives) >= 2
    and next_operation.present is True
    and differential_outcome_relation.present is True
    and len(differential_outcome_relation.outcomes) >= 2
    and provenance_complete is True
    and outcomes_are_discriminating(unit)
)
if complete_inquiry_unit:
    assert exactly_one_role_assessment(unit_id)
    assert role == "INQUIRY_CONSTRAINT"
```

The scan accepts only the mapping and searches every field. No negative_inference metadata enters discovery. The validator independently rescans the full text and cited spans, rejects missing/wrong/duplicate assessments, and blocks downstream success when any validation fails. It never supplies a repaired model role.
Ordinary insufficiency sentences retain INSUFFICIENCY_ONLY; the composite inquiry structure receives the inquiry role. Source spans use exact UTF-8 bytes, zero-based and end exclusive.

## Corpus and manifest

Four mechanisms each have a negative, affirmative and distributed formulation of the same decision structure. The distributed form places the live contrast, declarative selected operation and outcome logic in separate fields. Six controls complete the 18-case corpus. The first five are incomplete; the sixth has two independent textual bundles deduplicated into one complete unit.

| Case | Mechanism | Formulation | Complete units | Inquiry roles | Validation |
|---|---|---|---:|---:|---|
| `H4-38f9f7ba7473` | ach | negative | 1 | 1 | pass |
| `H4-289159bec29d` | ach | affirmative | 1 | 1 | pass |
| `H4-3a0c6da65d58` | ach | distributed | 1 | 1 | pass |
| `H4-850fb18146b9` | delta | negative | 1 | 1 | pass |
| `H4-1265065df754` | delta | affirmative | 1 | 1 | pass |
| `H4-0b63cfc8b069` | delta | distributed | 1 | 1 | pass |
| `H4-30c5ce7f3a71` | crossdating | negative | 1 | 1 | pass |
| `H4-b4b42be0c2d3` | crossdating | affirmative | 1 | 1 | pass |
| `H4-e4b01303ecd8` | crossdating | distributed | 1 | 1 | pass |
| `H4-f9c70c724ec5` | diagnosis | negative | 1 | 1 | pass |
| `H4-92b93353dbc9` | diagnosis | affirmative | 1 | 1 | pass |
| `H4-c28733e05bb9` | diagnosis | distributed | 1 | 1 | pass |
| `H4-f070ba17a9b7` | ach | generic_evidence | 0 | 0 | IQ_COMPONENT_MISMATCH |
| `H4-4c0495aa839d` | ach | no_outcomes | 0 | 0 | pass |
| `H4-6ad954a30ef5` | ach | no_operation | 0 | 0 | pass |
| `H4-ea0f90adf577` | ach | nondiscriminating | 0 | 0 | pass |
| `H4-dc676b428599` | ach | resolved | 0 | 0 | pass |
| `H4-86f4954813b3` | ach | redundant_complete | 1 | 1 | IQ_INVENTED_COMPONENT, IQ_UNCITED_SPAN |

Complete source formulations are preserved in cases/ and provider packets in packets/. Deterministic structures and exact spans are in review/authoring-gate.json; no hidden expected answers or extracted units were supplied to the provider.

## Counts and formulation results

18/18 fresh Astra/high observations; 18 distinct sessions. Complete semantic units found: 13. Raw role counts: `{"INQUIRY_CONSTRAINT": 13, "NOT_INQUIRY_CONSTRAINT": 5, "UNCERTAIN": 0}`. Cases passing all validation: 16.
Accepted complete-unit productivity: `{"NO": 0, "UNCERTAIN": 0, "YES": 12}`. Raw productivity across all annotated structures, including incomplete or rejected ones: `{"NO": 2, "UNCERTAIN": 0, "YES": 16}`. Raw counts are descriptive only; rejected cases do not contribute accepted productivity evidence.

| Formulation | Cases | Complete units | Inquiry roles | Validated cases |
|---|---:|---:|---:|---:|
| negative | 4 | 4 | 4 | 4 |
| affirmative | 4 | 4 | 4 | 4 |
| distributed | 4 | 4 | 4 | 4 |

## Six controls and duplicate behavior

- **generic_evidence** (`H4-f070ba17a9b7`): deterministic complete=0; emitted inquiry roles=0; intended missing boundary=['operation', 'outcome_relation']; validation=False.
- **no_outcomes** (`H4-4c0495aa839d`): deterministic complete=0; emitted inquiry roles=0; intended missing boundary=['outcome_relation']; validation=True.
- **no_operation** (`H4-6ad954a30ef5`): deterministic complete=0; emitted inquiry roles=0; intended missing boundary=['operation']; validation=True.
- **nondiscriminating** (`H4-ea0f90adf577`): deterministic complete=0; emitted inquiry roles=0; intended missing boundary=['discrimination']; validation=True.
- **resolved** (`H4-dc676b428599`): deterministic complete=0; emitted inquiry roles=0; intended missing boundary=['unresolved_contrast']; validation=True.
- **redundant_complete** (`H4-86f4954813b3`): deterministic complete=1; emitted inquiry roles=1; intended missing boundary=none; redundant bundles deduplicate; validation=False.

Repeated equivalent clauses are one semantic unit with unioned provenance. They are not two independently assessed roles. Whole-unit deletion removes both textual formulations; deleting only one would test a different counterfactual. A separate independent inquiry unit could still justify the same next inquiry and give productivity NO, but the exact-duplicate control is not such a separate unit. Membership with productivity NO is covered by a validator test, not a new artifact-viability experiment.

## H.3 offline regression fixtures

| Historical case | Complete found | Inquiry emitted | Coverage |
|---|---:|---:|---|
| `H3-4d30014ef73c` | 1 | 1 | True |
| `H3-d6134c9f4c74` | 1 | 1 | True |

Both fixture mappings are exact copies of the historical ablated mappings, with packet hashes verified. Their affirmative diagnostic operations are found with negative_inference=false. This restores offline coverage without recoding H.3 judgments or making new H.3 provider calls.

## Every validation failure code

Counts below are observed validation occurrences and distinct affected cases. Deliberately injected failures in unit tests are not provider observations.

| Code | Occurrences | Cases |
|---|---:|---:|
| `IQ_MISSING_ROLE` | 0 | 0 |
| `IQ_WRONG_ROLE` | 0 | 0 |
| `IQ_MISSING_CONTRAST` | 0 | 0 |
| `IQ_TOO_FEW_ALTERNATIVES` | 0 | 0 |
| `IQ_MISSING_OPERATION` | 0 | 0 |
| `IQ_GENERIC_OPERATION` | 0 | 0 |
| `IQ_MISSING_OUTCOME_RELATION` | 0 | 0 |
| `IQ_TOO_FEW_OUTCOMES` | 0 | 0 |
| `IQ_NONDISCRIMINATING_OUTCOMES` | 0 | 0 |
| `IQ_INVENTED_COMPONENT` | 4 | 1 |
| `IQ_POLARITY_GATING` | 0 | 0 |
| `IQ_DUPLICATE_UNIT` | 0 | 0 |
| `IQ_UNCITED_SPAN` | 1 | 1 |
| `IQ_COMPONENT_MISMATCH` | 1 | 1 |
| `IQ_COVERAGE_SUMMARY` | 0 | 0 |
| `IQ_PRODUCTIVITY` | 0 | 0 |
| `IQ_SCHEMA` | 0 | 0 |
| `IQ_UNKNOWN_UNIT` | 0 | 0 |

Detailed failures:

### H4-f070ba17a9b7 — generic_evidence

```json
[
  {
    "code": "IQ_COMPONENT_MISMATCH",
    "unit_id": "IQ1",
    "detail": "Canonical component values differ"
  }
]
```

### H4-86f4954813b3 — redundant_complete

```json
[
  {
    "code": "IQ_UNCITED_SPAN",
    "unit_id": "IQ1",
    "detail": ""
  },
  {
    "code": "IQ_INVENTED_COMPONENT",
    "unit_id": "IQ1",
    "detail": ""
  },
  {
    "code": "IQ_INVENTED_COMPONENT",
    "unit_id": "IQ1",
    "detail": "unresolved_contrast"
  },
  {
    "code": "IQ_INVENTED_COMPONENT",
    "unit_id": "IQ1",
    "detail": "next_operation"
  },
  {
    "code": "IQ_INVENTED_COMPONENT",
    "unit_id": "IQ1",
    "detail": "differential_outcome_relation"
  }
]
```


## Post-freeze operator interpretation

The intended semantic role boundary is respected in all 18 raw judgments: 13 inquiry roles, five non-inquiry roles, no polarity or deduplication failure. Full validation passes 16 cases. The duplicate control has incorrect byte offsets despite correct quoted text. The generic control exposes a punctuation-sensitive canonicalization defect despite a correct rejection. These two findings prevent declaring the entire annotation instrument ready. Coverage counts alone do not establish valid provenance. No judgment, source citation, frozen packet or validator was repaired.

- **H4-f070ba17a9b7**: Correctly rejects the generic evidence request as incomplete with NOT_INQUIRY_CONSTRAINT. The exact copied operation is "Collect more evidence."; the extractor canonicalizes it as "Collect more evidence". The frozen normalizer leaves this terminal punctuation unmatched for a generic operation, causing IQ_COMPONENT_MISMATCH. This is an overstrict representation check in the instrument, not a conceptual judge false positive. The failure remains uncorrected; changing the measured normalizer is not authorized recovery.
- **H4-86f4954813b3**: Correct semantic deduplication and inquiry role, but both whole-field citations end two bytes early (205 instead of 207; 209 instead of 211). IQ_UNCITED_SPAN is the root annotation error. Four IQ_INVENTED_COMPONENT occurrences are downstream missing-valid-provenance diagnostics, not evidence that the semantic contrast, action or outcomes were invented. Complete-unit productivity from this case is excluded from accepted counts.

Operator review is descriptive, not an independent rater or a repair. Exact byte diagnostics are in review/operator.json.

## Research questions and mechanical enforcement

1. Negative, affirmative and distributed primary triplets canonicalize to the same deterministic unit in all four mechanisms; provider outcomes are separated above.
2. Cross-field components compose into one unit; the test also moves the whole inquiry into every field and an unfamiliar field name.
3. negative_inference=false does not suppress discovery. Flipping/removing the flag preserves output; an intentionally gated legacy adapter raises IQ_POLARITY_GATING.
4. Every discovered complete unit requires exactly one INQUIRY_CONSTRAINT assessment. Omissions, wrong roles and duplicate IDs/structures are rejected before downstream success.
5. Generic evidence requests fail the specific-operation and outcome-relation requirements.
6. A specific operation without differential outcomes remains incomplete.
7. Outcome implications without a selected operation remain incomplete; hypothetical mentions do not select operations.
8. Identical evidence-gathering consequences are nondiscriminating and cannot qualify.
9. An already-resolved contrast is not an unresolved inquiry constraint even if its abstract test remains discriminating.
10. Repeated complete textual formulations are one semantic unit, with provenance from both bundles.
11. Both H.3 coverage-gap fixtures now satisfy deterministic offline coverage.
12. Exact source-byte checks, independent rediscovery, schema validation and mandatory coverage checks enforce the invariant. Provider disagreements remain failures, not operator repairs.

## Preservation, limitations and readiness

Historical preservation: `{"historical_runtime_files": 10451, "tracked_files": 4076, "unchanged": true}`. Preflight ran H.3 runner/publication verification, its original and recovery test suites, and all 32 H.4 tests. Historical verification adapters scope branch/diff checks to the exact H.3 publication without changing historical files. Postmeasurement verification is recorded separately.
The grammar is deliberately bounded to explicit relational language for four operations and the two H.3 diagnostic phrasings. It is not a universal semantic parser: unrestricted paraphrases, anaphora, nested scope, qualifiers and multiple distinct operations within a single mechanism are not established. Vocabulary and cases were authored together. Mechanical coverage is guaranteed relative to discovered supported units, not every inquiry that arbitrary prose might contain.
The model must follow frozen component-copy and span conventions. Validation may expose representation/annotation problems as well as conceptual mistakes; the raw observations and post-freeze operator review distinguish these without changing the instrument.
One fresh observation per case does not establish repeatability, an independent rater estimate or generalization. The duplicate control does not test a distinct independent-unit marginal redundancy scenario. No numerical accuracy threshold was defined.
Provider limitations: `{"exposed_internal_retry_events": 0, "harness_retries": 0, "no_served_snapshot_claim": "Requested gpt-6-astra/high. An unavailable returned served identifier remains unknown.", "verified_served_snapshots": [null]}`.
Polarity gating is absent from the deterministic scanner and H.3’s specific offline gap is closed, but the observed validation failures prevent a claim that the whole annotation instrument is ready. No operator repair was used to obtain passing coverage.

**Recommended next step:** Run a separately frozen, narrow source-span/annotation serialization calibration before returning to remainder viability or natural outputs. Preserve the H.4 rule and all raw judgments; do not integrate this instrument into production yet.

The recommendation was not executed. Work stops after H.4: no H.3 viability rerun, Experiment E continuation, fresh natural outputs, production integration or merge to main.
