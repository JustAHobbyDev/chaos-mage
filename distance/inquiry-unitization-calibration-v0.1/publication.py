"""H.4 postmeasurement publication; reads immutable results, never runs a provider."""
import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import authoring as a
import extractor as e
import runner as r
import validation as v
H=r.H;R=r.R;REPORT=R/'distance/review/inquiry-unitization-calibration-v0.1.md'

def checkpoint(path):return r.git('log','-1','--format=%H','--',r.rel(path)).decode().strip()
def counts(items,labels):
    c=Counter(items);return {k:c[k] for k in labels}

def compute():
    r.verify_results();m=a.read(H/'manifest.json');f=a.read(H/'judgments-freeze.json');rows=[]
    for spec in m['cases']:
        cid=spec['case_id'];value=a.read(H/'judgments'/f'{cid}.json');result=v.validate(r.case(cid),value)
        units=[x['inquiry_unit'] for x in value['semantic_units']]
        gold=e.extract_inquiry_units(r.case(cid)['mapping'])
        rows.append({**spec,'judgment_sha256':a.sha(H/'judgments'/f'{cid}.json'),
          'deterministic_complete_units':sum(e.complete(x) for x in gold),
          'model_role_counts':counts((x['role'] for x in units),['INQUIRY_CONSTRAINT','NOT_INQUIRY_CONSTRAINT','UNCERTAIN']),
          'raw_productivity_counts':counts((x['productivity'] for x in units),['YES','NO','UNCERTAIN']),
          'accepted_complete_productivity_counts':counts((x['productivity'] for x in units if result['downstream_allowed'] and x['role']=='INQUIRY_CONSTRAINT'),['YES','NO','UNCERTAIN']),
          'validation':result,'model_summary':value['inquiry_role_coverage'],
          'mapping_fields':list(r.case(cid)['mapping']),'canonical_structure':e.canonical(gold[0])})
    errors=[x for row in rows for x in row['validation']['errors']]
    byform={}
    for form in ['negative','affirmative','distributed']:
        group=[x for x in rows if x['kind']=='primary' and x['formulation']==form]
        byform[form]={'cases':len(group),'complete_units_found':sum(x['deterministic_complete_units'] for x in group),
          'inquiry_constraints_emitted':sum(x['model_role_counts']['INQUIRY_CONSTRAINT'] for x in group),
          'validated_cases':sum(x['validation']['validation_passed'] for x in group),
          'failures':[{'case_id':x['case_id'],'errors':x['validation']['errors']} for x in group if x['validation']['errors']]}
    cps={
      'schema_and_rule':checkpoint(H/'INQUIRY-UNIT.md'),
      'primary_cases':checkpoint(H/'cases'/next(x['case_id']+'.json' for x in m['cases'] if x['kind']=='primary')),
      'six_controls':checkpoint(H/'manifest.json'),
      'h3_regression_fixtures':checkpoint(H/'regression-fixtures/H3-4d30014ef73c.json'),
      'extractor_and_tests_initial':checkpoint(H/'tests/test_inquiry.py'),
      'final_extractor_and_packets':checkpoint(H/'prepared.json'),
      'preflight':checkpoint(H/'review/preflight.json'),
      'eighteen_judgments':checkpoint(H/'judgments-freeze.json'),
      'coverage_validation':checkpoint(H/'coverage/summary.json')}
    role_counts={k:sum(x['model_role_counts'][k] for x in rows) for k in ['INQUIRY_CONSTRAINT','NOT_INQUIRY_CONSTRAINT','UNCERTAIN']}
    regression=a.read(H/'review/authoring-gate.json')['regressions']
    return {'status':'COMPLETE','base_sha':m['base_sha'],'base_branch':m['base_branch'],'branch':m['branch'],
      'checkpoints':cps,'completion_sha_resolution':'git log -1 --format=%H -- distance/inquiry-unitization-calibration-v0.1/publication-manifest.json',
      'cases_completed':18,'provider_calls':18,'unique_sessions':len({x['validation']['metadata']['session_id'] for x in f['runs']}),
      'complete_units_found':sum(x['deterministic_complete_units'] for x in rows),'role_counts':role_counts,
      'accepted_complete_productivity_counts':{k:sum(x['accepted_complete_productivity_counts'][k] for x in rows) for k in ['YES','NO','UNCERTAIN']},
      'raw_productivity_counts':{k:sum(x['raw_productivity_counts'][k] for x in rows) for k in ['YES','NO','UNCERTAIN']},
      'validation_failure_occurrences':counts((x['code'] for x in errors),v.CODES),
      'validation_failure_case_counts':{code:sum(any(err['code']==code for err in row['validation']['errors']) for row in rows) for code in v.CODES},
      'validated_cases':sum(x['validation']['validation_passed'] for x in rows),
      'all_cases_validation_passed':not errors,'by_formulation':byform,
      'h3_regressions':[{'case_id':x['case_id'],'coverage':x['validation']['inquiry_role_coverage'],'validation_passed':x['validation']['validation_passed']} for x in regression],
      'polarity_gating_in_discovery':False,'coverage_mechanically_enforced_within_bounded_grammar':True,
      'historical_preservation':a.preserve(),'cases':rows,
      'provider_limitations':{'verified_served_snapshots':[None],'harness_retries':0,'exposed_internal_retry_events':sum(len(x['validation']['metadata']['internal_retry_events']) for x in f['runs']),
        'no_served_snapshot_claim':'Requested gpt-6-astra/high. An unavailable returned served identifier remains unknown.'},
      'operator_review':a.read(H/'review/operator.json'),
      'recommended_next_step':('Design a separate pre-registered broader-language inquiry extraction challenge before returning to remainder viability or natural outputs; retain this bounded coverage invariant.' if not errors else 'Run a separately frozen, narrow source-span/annotation serialization calibration before returning to remainder viability or natural outputs. Preserve the H.4 rule and all raw judgments; do not integrate this instrument into production yet.')}

def freeze_coverage():
    r.verify_results();summary=[]
    for cid in r.order():
        value=a.read(H/'judgments'/f'{cid}.json');result=v.validate(r.case(cid),value)
        r.write(H/'coverage'/f'{cid}.json',{'case_id':cid,'semantic_units':value['semantic_units'],
          'inquiry_role_coverage':result['inquiry_role_coverage'],'model_coverage_summary':value['inquiry_role_coverage'],
          'validation':result,'judgment_sha256':a.sha(H/'judgments'/f'{cid}.json'),
          'note':'Model units are unchanged; summary and errors are independently derived, never a repaired judgment.'})
        summary.append({'case_id':cid,**result})
    r.write(H/'coverage/summary.json',{'judgment_freeze_sha256':a.sha(H/'judgments-freeze.json'),'cases':summary})

def render(m):
    good=m['all_cases_validation_passed'];rows=m['cases'];controls=[x for x in rows if x['kind']=='control']
    text=['# Experiment H.4 — Inquiry-unitization and mandatory role coverage v0.1','',
      ('All 18 fresh assessments satisfy the frozen validator. Polarity-independent unitization and mandatory role coverage are demonstrated within this bounded authored grammar.' if good else 'All 18 fresh assessments were preserved, but H.4 has validation failures. The deterministic coverage guard operates; the complete annotation instrument is not ready to return to remainder-viability or natural-output measurement.'),'',
      '## Lineage and frozen checkpoints','',f'Base `{m["base_sha"]}` on `{m["base_branch"]}`. Publication branch: `{m["branch"]}`. No main merge.',
      'The final SHA is the commit containing publication-manifest.json; metrics.json gives its resolution command.','',
      '| Checkpoint | SHA |','|---|---|']
    text += [f'| {name} | `{sha}` |' for name,sha in m['checkpoints'].items()]
    text += ['', '## Frozen rule and forcing invariant','', (H/'INQUIRY-UNIT.md').read_text().split('\n\n')[1], '',
      '```python', 'complete_inquiry_unit = (',
      '    unresolved_contrast.present is True',
      '    and len(unresolved_contrast.alternatives) >= 2',
      '    and next_operation.present is True',
      '    and differential_outcome_relation.present is True',
      '    and len(differential_outcome_relation.outcomes) >= 2',
      '    and provenance_complete is True',
      '    and outcomes_are_discriminating(unit)',')',
      'if complete_inquiry_unit:',
      '    assert exactly_one_role_assessment(unit_id)',
      '    assert role == "INQUIRY_CONSTRAINT"','```','',
      'The scan accepts only the mapping and searches every field. No negative_inference metadata enters discovery. The validator independently rescans the full text and cited spans, rejects missing/wrong/duplicate assessments, and blocks downstream success when any validation fails. It never supplies a repaired model role.',
      'Ordinary insufficiency sentences retain INSUFFICIENCY_ONLY; the composite inquiry structure receives the inquiry role. Source spans use exact UTF-8 bytes, zero-based and end exclusive.','',
      '## Corpus and manifest','',
      'Four mechanisms each have a negative, affirmative and distributed formulation of the same decision structure. The distributed form places the live contrast, declarative selected operation and outcome logic in separate fields. Six controls complete the 18-case corpus. The first five are incomplete; the sixth has two independent textual bundles deduplicated into one complete unit.','',
      '| Case | Mechanism | Formulation | Complete units | Inquiry roles | Validation |','|---|---|---|---:|---:|---|']
    for x in rows:text.append(f'| `{x["case_id"]}` | {x["mechanism"]} | {x["formulation"]} | {x["deterministic_complete_units"]} | {x["model_role_counts"]["INQUIRY_CONSTRAINT"]} | {"pass" if x["validation"]["validation_passed"] else ", ".join(sorted({e["code"] for e in x["validation"]["errors"]}))} |')
    text += ['', 'Complete source formulations are preserved in cases/ and provider packets in packets/. Deterministic structures and exact spans are in review/authoring-gate.json; no hidden expected answers or extracted units were supplied to the provider.','',
      '## Counts and formulation results','',
      f'18/18 fresh Astra/high observations; {m["unique_sessions"]} distinct sessions. Complete semantic units found: {m["complete_units_found"]}. Raw role counts: `{json.dumps(m["role_counts"],sort_keys=True)}`. Cases passing all validation: {m["validated_cases"]}.',
      f'Accepted complete-unit productivity: `{json.dumps(m["accepted_complete_productivity_counts"],sort_keys=True)}`. Raw productivity across all annotated structures, including incomplete or rejected ones: `{json.dumps(m["raw_productivity_counts"],sort_keys=True)}`. Raw counts are descriptive only; rejected cases do not contribute accepted productivity evidence.','',
      '| Formulation | Cases | Complete units | Inquiry roles | Validated cases |','|---|---:|---:|---:|---:|']
    for k,x in m['by_formulation'].items():text.append(f'| {k} | {x["cases"]} | {x["complete_units_found"]} | {x["inquiry_constraints_emitted"]} | {x["validated_cases"]} |')
    text += ['', '## Six controls and duplicate behavior','']
    for x in controls:text += [f'- **{x["formulation"]}** (`{x["case_id"]}`): deterministic complete={x["deterministic_complete_units"]}; emitted inquiry roles={x["model_role_counts"]["INQUIRY_CONSTRAINT"]}; intended missing boundary={x["expected_missing"] or "none; redundant bundles deduplicate"}; validation={x["validation"]["validation_passed"]}.']
    text += ['', 'Repeated equivalent clauses are one semantic unit with unioned provenance. They are not two independently assessed roles. Whole-unit deletion removes both textual formulations; deleting only one would test a different counterfactual. A separate independent inquiry unit could still justify the same next inquiry and give productivity NO, but the exact-duplicate control is not such a separate unit. Membership with productivity NO is covered by a validator test, not a new artifact-viability experiment.','',
      '## H.3 offline regression fixtures','',
      '| Historical case | Complete found | Inquiry emitted | Coverage |','|---|---:|---:|---|']
    for x in m['h3_regressions']:text.append(f'| `{x["case_id"]}` | {x["coverage"]["complete_units_found"]} | {x["coverage"]["inquiry_constraints_emitted"]} | {x["validation_passed"]} |')
    text += ['', 'Both fixture mappings are exact copies of the historical ablated mappings, with packet hashes verified. Their affirmative diagnostic operations are found with negative_inference=false. This restores offline coverage without recoding H.3 judgments or making new H.3 provider calls.','',
      '## Every validation failure code','',
      'Counts below are observed validation occurrences and distinct affected cases. Deliberately injected failures in unit tests are not provider observations.','',
      '| Code | Occurrences | Cases |','|---|---:|---:|']
    for code,n in m['validation_failure_occurrences'].items():text.append(f'| `{code}` | {n} | {m["validation_failure_case_counts"][code]} |')
    text += ['', 'Detailed failures:','']
    failures=[x for x in rows if x['validation']['errors']]
    if not failures:text.append('None.')
    for x in failures:
        text += [f'### {x["case_id"]} — {x["formulation"]}','', '```json',json.dumps(x['validation']['errors'],indent=2),'```','']
    text += ['', '## Post-freeze operator interpretation','',m['operator_review']['summary'],'']
    for finding in m['operator_review']['findings']:
        text += [f"- **{finding['case_id']}**: {finding['interpretation']}"]
    text += ['', 'Operator review is descriptive, not an independent rater or a repair. Exact byte diagnostics are in review/operator.json.','', '## Research questions and mechanical enforcement','',
      '1. Negative, affirmative and distributed primary triplets canonicalize to the same deterministic unit in all four mechanisms; provider outcomes are separated above.',
      '2. Cross-field components compose into one unit; the test also moves the whole inquiry into every field and an unfamiliar field name.',
      '3. negative_inference=false does not suppress discovery. Flipping/removing the flag preserves output; an intentionally gated legacy adapter raises IQ_POLARITY_GATING.',
      '4. Every discovered complete unit requires exactly one INQUIRY_CONSTRAINT assessment. Omissions, wrong roles and duplicate IDs/structures are rejected before downstream success.',
      '5. Generic evidence requests fail the specific-operation and outcome-relation requirements.',
      '6. A specific operation without differential outcomes remains incomplete.',
      '7. Outcome implications without a selected operation remain incomplete; hypothetical mentions do not select operations.',
      '8. Identical evidence-gathering consequences are nondiscriminating and cannot qualify.',
      '9. An already-resolved contrast is not an unresolved inquiry constraint even if its abstract test remains discriminating.',
      '10. Repeated complete textual formulations are one semantic unit, with provenance from both bundles.',
      '11. Both H.3 coverage-gap fixtures now satisfy deterministic offline coverage.',
      '12. Exact source-byte checks, independent rediscovery, schema validation and mandatory coverage checks enforce the invariant. Provider disagreements remain failures, not operator repairs.','',
      '## Preservation, limitations and readiness','',
      f'Historical preservation: `{json.dumps(m["historical_preservation"],sort_keys=True)}`. Preflight ran H.3 runner/publication verification, its original and recovery test suites, and all 32 H.4 tests. Historical verification adapters scope branch/diff checks to the exact H.3 publication without changing historical files. Postmeasurement verification is recorded separately.',
      'The grammar is deliberately bounded to explicit relational language for four operations and the two H.3 diagnostic phrasings. It is not a universal semantic parser: unrestricted paraphrases, anaphora, nested scope, qualifiers and multiple distinct operations within a single mechanism are not established. Vocabulary and cases were authored together. Mechanical coverage is guaranteed relative to discovered supported units, not every inquiry that arbitrary prose might contain.',
      'The model must follow frozen component-copy and span conventions. Validation may expose representation/annotation problems as well as conceptual mistakes; the raw observations and post-freeze operator review distinguish these without changing the instrument.',
      'One fresh observation per case does not establish repeatability, an independent rater estimate or generalization. The duplicate control does not test a distinct independent-unit marginal redundancy scenario. No numerical accuracy threshold was defined.',
      f'Provider limitations: `{json.dumps(m["provider_limitations"],sort_keys=True)}`.',
      ('Polarity gating is eliminated and mandatory coverage is demonstrated for this corpus. H.3’s specific offline coverage gap is closed. A return to broader inquiry/remainder work requires a separate scope decision and broader-language calibration; production readiness is not claimed.' if good else 'Polarity gating is absent from the deterministic scanner and H.3’s specific offline gap is closed, but the observed validation failures prevent a claim that the whole annotation instrument is ready. No operator repair was used to obtain passing coverage.'),
      '', '**Recommended next step:** '+m['recommended_next_step'], '',
      'The recommendation was not executed. Work stops after H.4: no H.3 viability rerun, Experiment E continuation, fresh natural outputs, production integration or merge to main.','']
    return '\n'.join(text)

def write():
    m=compute();r.write(H/'metrics.json',m);r.raw(REPORT,render(m).encode())
    r.raw(H/'README.md',('''# Experiment H.4 — Inquiry-unitization and mandatory role coverage v0.1

18/18 fresh GPT-6 Astra/high judgments are preserved. See the [full report](../review/inquiry-unitization-calibration-v0.1.md) for validation findings and limits.

The deterministic scanner finds 13 complete units across the 18-case calibration corpus
and one in each of the two offline H.3 fixtures. H.3 artifacts remain unchanged.

- [Frozen rule](INQUIRY-UNIT.md), [protocol](PROTOCOL.md), [bounded grammar](LANGUAGE.md)
- [Case manifest](manifest.json), [authoring gate](review/authoring-gate.json)
- [Coverage results](coverage/summary.json), [metrics](metrics.json)
- [Post-freeze operator review](review/operator.json)

```sh
python -B -m unittest discover -s distance/inquiry-unitization-calibration-v0.1/tests -p 'test_*.py'
python -B distance/inquiry-unitization-calibration-v0.1/runner.py verify-results
python -B distance/inquiry-unitization-calibration-v0.1/publication.py verify
```

Publication is restricted to experiment-h4-inquiry-unitization. No recommendation was
executed; no historical measurement, natural-output experiment or production policy changed.
''').encode())
    r.write(H/'final-runtime-freeze.json',{'state':r.state(),'files':r.inventory(r.RT.rglob('*'))})

def seal():
    paths=[p for p in H.rglob('*') if p.is_file() and p.name!='publication-manifest.json']+[REPORT,R/'docs/PROBLEM_FRAMES-inquiry-unitization-calibration-v0.1.md']
    r.write(H/'publication-manifest.json',{'status':'COMPLETE','checkpoint_before_completion':r.head(),'files':r.inventory(paths)})

def verify():
    r.verify_results();m=compute();r.require(json.loads(json.dumps(m))==a.read(H/'metrics.json'),'Metrics drift')
    r.require(REPORT.read_text()==render(m),'Report drift');r.hashes(a.read(H/'publication-manifest.json')['files'])
    frozen=a.read(H/'final-runtime-freeze.json')['files'];r.hashes(frozen);r.require(r.inventory(r.RT.rglob('*'))==frozen,'Runtime drift')
    for row in m['cases']:
        coverage=a.read(H/'coverage'/f"{row['case_id']}.json")
        r.require(coverage['validation']==row['validation'],'Coverage drift')
        r.require(coverage['semantic_units']==a.read(H/'judgments'/f"{row['case_id']}.json")['semantic_units'],'Published units changed')
    return {k:m[k] for k in ['status','cases_completed','complete_units_found','role_counts','validated_cases','validation_failure_occurrences','historical_preservation']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['freeze-coverage','write','seal','verify']);args=p.parse_args()
    result=globals()[args.action.replace('-','_')]()
    if result:print(json.dumps(result,indent=2))
