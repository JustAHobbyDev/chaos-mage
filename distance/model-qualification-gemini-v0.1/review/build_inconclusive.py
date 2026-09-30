#!/usr/bin/env python3
"""Publish partial-run facts only; never decode historical judgments or call models."""
import importlib.util
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('gemini_partial_report', HERE/'runner.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


def main():
    r.verify(); r.committed(HERE/'partial-freeze.json')
    frozen = r.read(HERE/'partial-freeze.json'); r.verify_inventory(frozen['evidence'])
    r.require(not frozen['complete'] and not frozen['runs'], 'Only zero-primary partial run supported')
    d = HERE/'preflight/validity'; response = r.read(d/'http-body.json'); u = response['usageMetadata']
    r.require(u['serviceTier'] == 'standard', 'Different incident')
    p, c, t = (u[k] for k in ('promptTokenCount','candidatesTokenCount','thoughtsTokenCount'))
    r.require(p+c+t == u['totalTokenCount'], 'Usage cannot be reconciled')
    # Descriptive offline calculation, not a change to the frozen scheduler/accountant.
    amount = r.cost.estimate(p,c+t,r.pricing())
    partial = r.checkpoint(HERE/'partial-freeze.json'); prep = r.checkpoint(HERE/'prepared.json')
    shared = {'at':r.now(),'partial_freeze_commit':partial,'results_freeze_commit':None}
    cost = {**shared,'credential_source':'environment','input_tokens':p,'output_tokens':c,
        'thinking_tokens':t,'billable_output_tokens':c+t,'total_tokens':u['totalTokenCount'],
        'estimated_experiment_usd':str(amount),'estimated_primary_usd':'0',
        'estimated_preflight_usd':str(amount),'estimate_not_invoice':True,
        'raw_usage':u,'pricing_source':r.pricing()['source'],'service_tier':u['serviceTier'],
        'billable_interpretation':'prompt at $2/M; candidates + thoughts at $12/M; no double counting',
        'frozen_scheduler_unresolved_reservation_usd':str(r.cumulative()),
        'accounting_limitation':'Frozen accountant rejected lowercase service tier; this offline estimate does not clear its stop or reservation.'}
    r.write(HERE/'review/cost-summary.json',cost)
    metrics = {**shared,'qualification':'qualification_inconclusive',
        'planned_primary_judgments':12,'attempted_judgments':0,'successful_judgments':0,
        'provider_failures':0,'schema_failures':0,'harness_failures':1,
        'planned_artificial_probes':2,'attempted_artificial_probes':1,
        'successful_harness_probes':0,'offline_validated_artificial_responses':1,
        'input_tokens':p,'output_tokens':c,'thinking_tokens':t,'estimated_experiment_usd':str(amount),
        'validity':dict.fromkeys(('Valid','Conditional','Invalid')),
        'anti_collapse':dict.fromkeys(('CLEAR_COLLAPSE','BORDERLINE_KEEP','SUFFICIENT_DEPARTURE')),
        'anti_collapse_gate':{'keep':None,'reject':None},
        'qualitative_assessment':'not_performed_no_primary_evidence',
        'model_failure_cases':None,'ontology_specification_ambiguity_cases':None,
        'legitimate_reasoning_variation_cases':None,'historical_status_comparison':None}
    r.write(HERE/'metrics.json',metrics)
    r.write(HERE/'review/case-reviews.json',{**shared,'qualification':'qualification_inconclusive',
        'state':'not_performed','reason':'No primary measurements; complete-freeze gate remains closed',
        'cases':[],'unmeasured_cases':[{'qualification_id':c['qualification_id'],'source_case_id':c['source_case_id'],
            'stage':c['stage'],'assessment':None} for c in r.cases()]})
    r.write(HERE/'review/execution-audit.json',{**shared,'preparation_commit':prep,
        'primary_calls':{'gemini':0,'astra':0,'fable':0,'muse':0},'artificial_probes':1,
        'provider_http_successes':1,'harness_failures':1,'provider_failures':0,'schema_failures':0,
        'unique_request_sessions':1,'harness_retries':0,'experiment_f_calls':0,
        'historical_artifacts_unchanged':True,'historical_decoding_performed':False,
        'semantic_comparisons_performed':False,'second_probe_attempted':False,
        'stop_reason':'Cost accountant expected STANDARD but response serviceTier was standard',
        'credential_preparation':'Sandbox helper failure occurred before any reservation; identical authorized launcher succeeded with sandbox escalation',
        'credential_scan':{'scanned_artifacts':2104,'secret_present':False},
        'snapshot_limitation':'Exact preview alias returned; no immutable served snapshot exposed'})
    rows='\n'.join('| '+c['qualification_id']+' | '+c['stage']+' | `'+c['source_commit']+'` | `'+c['input_sha256']+'` |' for c in r.cases())
    hashes='\n'.join('- '+s+': classifier `'+next(c['classifier_sha256'] for c in r.cases() if c['stage']==s)+'`; canonical schema `'+next(c['canonical_schema_sha256'] for c in r.cases() if c['stage']==s)+'`.' for s in r.IDS)
    report=f'''# Gemini 3.1 Pro capability qualification v0.1

**Qualification: `qualification_inconclusive`.** No primary judgments were collected.
The first artificial probe returned successfully; a defect in the frozen harness's
billing-tier check stopped scheduling. This is no evidence for or against Gemini's
reasoning competence. No replacement Family B is declared.

## Provenance and checkpoints

- Starting SHA: `cb5ac745d4326bc6a097411b819c14563ae28c80` (local and remote matched).
- Preparation: `{prep}`.
- Partial preflight/result evidence freeze: `{partial}`.
- Successful preflight checkpoint: absent.
- Twelve-judgment result checkpoint: absent.
- Completion commit: the commit introducing this report, reported separately to avoid a self-reference.
- Contract original freeze: `1f51578aff8f8409b9a3c297a86ed84f8e6d7ee1`.
- Contract SHA-256: `21b2ce7aeda5eef39175eb838f31f148afa7339e8fe02719c6ea1a2bf7acf31a`.

The contract, historical qualification, D/E experiments, model-agnosticism principle,
and model policy remain unchanged. The unrelated untracked handoff is untouched.
The complete provenance manifest carries each source input, source freeze, classifier,
canonical schema, prior packet, and historical-output hash. Historical outputs were
hash-verified only; their judgments and reviews were not decoded for comparison.
The handoff's explicit complete-freeze embargo takes precedence over its read-first list.

| Case | Stage | Source commit | Input / packet SHA-256 |
|---|---|---|---|
{rows}

{hashes}

Every copied packet matches the prior qualification byte-for-byte. Coverage is six
validity and six anti-collapse cases. None was submitted to Gemini. Randomized
interleaved order was frozen before the artificial probe and remains unexecuted.

## Provider and artificial preflight

Requested and returned model: `gemini-3.1-pro-preview`.
Native endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent`.
Client: Python standard-library `urllib.request`; exact Python and jsonschema versions
are frozen in execution-config.json and the request reservation. No Google SDK.
Explicit `thinkingConfig.thinkingLevel: HIGH`, `maxOutputTokens: 32768`, temperature
1.0; top-p, top-k and seed unset/provider default. No legacy thinking budget.
The returned preview identifier establishes the requested model alias, not immutable
served weights. Response ID and raw metadata are retained with the artificial response.

The sole request was a synthetic validity formatting fixture in one fresh process,
one user message, an empty working directory, and no history, tools, grounding,
URL context, retrieval, code execution, or other cases. The serialized request and
schema are frozen. Native JSON output used responseMimeType/responseJsonSchema;
wire projection retained the historical structural projection. Offline inspection
confirmed exact fixture equality and full unchanged canonical/cross-field validation.
No response was rewritten. The anti-collapse artificial schema was never tested.

The API returned HTTP 200, finishReason STOP, the exact model ID, and coherent token
counts. It returned usageMetadata.serviceTier as lowercase `standard`. The harness
allowed only uppercase `STANDARD` (or an omitted tier), raising “Unexpected billing
service tier” before extracting the successful structured response. The original
validation artifact retains its generic provider_or_protocol_failure classification;
the audit correctly attributes it to the harness accountant, not the provider or schema.
The defect is in our adapter validation, not the model's response.

The original response is preserved in http-body.json, including opaque thought
signature metadata. No thought signature or history was replayed. High thinking was
explicitly serialized and accepted; internal execution cannot be independently inspected.
The response reports thinking tokens, not access to private reasoning.

A credential-helper sandbox failure preceded all reservations. The identical
launcher succeeded with approved escalation; this was credential setup, not an API
retry. Credential source: environment. Temporary helper file removed before the call;
no secret in argv, request artifacts or errors. A live-key artifact scan passed.

## Mechanical counts and cost

| Measurement | Count |
|---|---:|
| Planned primary judgments | 12 |
| Attempted primary judgments | 0 |
| Successful primary judgments | 0 |
| Planned artificial probes | 2 |
| Attempted artificial probes | 1 |
| Successful preflight sequences | 0 |
| HTTP-successful artificial responses | 1 |
| Offline canonical-valid artificial responses | 1 |
| Provider failures | 0 |
| Schema failures | 0 |
| Harness accounting failures | 1 |
| Retries / fresh historical-model calls / Experiment F calls | 0 |

All usage below belongs to the artificial probe; primary usage is zero:

- Input: {p} tokens.
- Candidate output: {c} tokens.
- Thinking: {t} tokens.
- Billable output including thinking: {c+t} tokens.
- Total: {u['totalTokenCount']} tokens.
- Estimated experiment cost: **${amount}**; ceiling **$2.00**.

Standard pricing checked 2026-09-29: $2/M input and $12/M output including thinking
at this context length ([Google pricing]({r.pricing()['source']})). Estimate:
`154 × 2 / 1,000,000 + (112 + 652) × 12 / 1,000,000 = 0.009476 USD`.
This is an offline estimate, not an invoice or a successful execution-ledger update.
The frozen scheduler conservatively retains its unresolved ${r.cumulative()}
reservation; its stop has not been cleared. No double counting of thoughts.

Validity, anti-collapse and keep/reject distributions are **unmeasured**, represented
as null rather than fabricated results. Historical raw-status matching is unmeasured.
Model-failure/ambiguity/variation counts and case IDs are unassessed, not zero findings.

## Capability findings and Muse comparison

There are no Gemini primary judgments and no case-level capability findings.
E006, E022 and E030 warrant reasoning are unmeasured. N001/N006 formalization,
N002 modest departure, N004 uncertainty and N009 coordinated departure are likewise
unmeasured. E003/E010/E014 and N010 are also unmeasured. No historical comparison,
majority vote, consensus score, or accuracy-against-model calculation was performed.

The operator handoff disclosed Muse's warrant failure pattern in E006/E022/E030.
That context was excluded from the artificial request and all frozen Gemini packets.
No Muse judgments or case reviews were opened. Whether Gemini reproduces any of
those failures is unknown. This stopped run cannot establish whether the capability
contract discriminates between these candidates; it supplies provider/harness
compatibility evidence only. No systematic Gemini pathology can be assessed.

## Verification, limitations and next step

Offline qualification tests, partial-evidence tests, the Gemini preparation verifier,
and the historical Muse hash/provenance verifier are recorded in review/verification.json.
All original tracked bytes are preserved. Completion/semantic historical suites remain
gated because they decode judgments, and the required twelve-result freeze does not
exist. They are explicitly deferred, not claimed as passing. No historical verifier
was allowed to overwrite its frozen report.

Publish this partial result as **qualification_inconclusive**. Leave MODEL-POLICY.md
unchanged. Before Experiment F, a separately authorized attempt must correct and test
the service-tier representation handling and establish both artificial schemas.
The present v0.1 adapter, request and stop remain frozen. Do not repair-and-continue,
retry the probe, run a primary judgment, choose another candidate, or execute F here.

Limitations: no capability evidence; incomplete preflight; untested anti-collapse wire
compatibility; alias-only served identity; estimated rather than invoiced billing;
provider-internal retries are not observable. The 32768-token cap and $2 guard have
only offline test coverage plus one low-consumption artificial response.
'''
    r.put(r.ROOT/'distance/review/model-qualification-gemini-v0.1.md',report.encode())


if __name__ == '__main__': main()
