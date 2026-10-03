"""Post-freeze operator comparison. Never imported by packet construction."""
from collections import Counter
import contracts as c

SEMANTIC_CODES = ('OBLIGATION_OMISSION', 'OVERTRIGGER', 'WRONG_SECONDARY_CONTRACT',
                  'DEPENDENCY_DUPLICATION', 'RECURSIVE_EXPLOSION')


def operator_template(hypotheses):
    return {'status':'PENDING','claim_reviews':[{'claim_id':h['claim_id'],
        'expected_dependency_matches':[{'expected_index':i,'dependency_ids':[],
          'finding':'PENDING','rationale':''} for i,_ in enumerate(h['expected_secondary_obligations'])],
        'semantic_checks':[{'code':code,'finding':'PENDING','rationale':''} for code in SEMANTIC_CODES], 'notes':''}
        for case in hypotheses for h in case['hidden_operator_hypotheses']]}


def report(assignments, discoveries, evaluations, aggregates, hypotheses, diagnostics, review):
    c.require(review['status']=='COMPLETE','Semantic dependency audit incomplete')
    reviews={x['claim_id']:x for x in review['claim_reviews']}
    c.require(set(reviews)==set(assignments) and len(reviews)==len(review['claim_reviews']),
              'Audit claim coverage/identity mismatch')
    events=list(diagnostics);cases=[]
    by_claim={cid:[v for v in evaluations if v['claim_id']==cid] for cid in assignments}
    for case in hypotheses:
        records=[]
        for h in case['hidden_operator_hypotheses']:
            cid=h['claim_id'];r=reviews[cid];a=assignments[cid];b=discoveries.get(cid)
            s=b['claim_obligation_set'] if b else None
            deps={d['dependency_id']:d for d in s['dependencies']} if s else {}
            matches=r['expected_dependency_matches']
            c.require(sorted(x['expected_index'] for x in matches)==list(range(len(h['expected_secondary_obligations']))),
                      'Audit expectation coverage mismatch')
            added=[]
            for match in matches:
                c.require(match['finding'] in ('PRESENT','OMITTED','UNMEASURED') and match['rationale'].strip(),
                          'Unfinished semantic alignment')
                c.require(set(match['dependency_ids'])<=set(deps),'Audit references unknown dependency')
                if match['finding']=='PRESENT':c.require(bool(match['dependency_ids']),'Present match needs dependency')
                if match['finding']=='OMITTED':
                    c.require(not match['dependency_ids'] and s is not None,'Invalid omission match')
                    added.append({'code':'OBLIGATION_OMISSION','claim_id':cid,
                                  'detail':{'expected_index':match['expected_index'],'rationale':match['rationale']}})
            c.require(sorted(x['code'] for x in r['semantic_checks'])==sorted(SEMANTIC_CODES), 'Semantic checks incomplete')
            for d in r['semantic_checks']:
                c.require(d['finding'] in ('PRESENT','ABSENT','UNMEASURED') and d['rationale'].strip(), 'Invalid semantic finding')
                if d['finding']=='PRESENT':
                    added.append({'code':d['code'],'claim_id':cid,'detail':d['rationale']})
            observed=by_claim[cid];agg=aggregates[cid]
            if s:
                for ref in h['claim_refs']:
                    if not any(d['resolution']=='CLAIM_REF' and d['claim_ref']==ref for d in deps.values()):
                        added.append({'code':'OBLIGATION_OMISSION','claim_id':cid,'detail':'Missing expected CLAIM_REF '+ref})
                violations=[x for x in agg['results'] if x.get('verdict')=='VIOLATED']
                if violations and agg['overall'] not in ('VIOLATED',None):
                    added.append({'code':'FAILURE_NONPROPAGATION','claim_id':cid,'detail':violations})
                if agg.get('missing_obligations') and any(x['verdict']=='VIOLATED' for x in observed):
                    added.append({'code':'SHORT_CIRCUIT','claim_id':cid,'detail':agg['missing_obligations']})
                gov_pass=any(v['contract']=='GOVERNANCE_COHERENCE' and v['verdict']=='SATISFIED' for v in observed)
                inline_ids={d['dependency_id'] for d in deps.values() if d['resolution']=='INLINE_OBLIGATION'}
                secondary_failed=any(v['obligation_id'] in inline_ids and v['verdict']=='VIOLATED' for v in observed)
                secondary_failed |= any(x.get('claim_ref') and x['verdict']=='VIOLATED' for x in agg['results'])
                omitted=any(x['code']=='OBLIGATION_OMISSION' for x in events+added if x['claim_id']==cid)
                if gov_pass and agg['overall']=='SATISFIED' and (secondary_failed or omitted):
                    added.append({'code':'GOVERNANCE_LAUNDERING','claim_id':cid,
                                  'detail':'Governance and overall SATISFIED despite omitted/failed required content'})
            events.extend(added)
            records.append({'claim_id':cid,'hypothesis':h,'classification':a,'obligation_set':s,
                            'judgments':observed,'aggregation':agg,'semantic_review':r})
        cases.append({'control_id':case['control_id'],'case_id':case['case_id'],'claims':records})
    # Diagnostic count unit: affected claims, with all event details retained separately.
    counts={code:len({x['claim_id'] for x in events if x['code']==code}) for code in c.DIAGNOSTICS}
    counts_by_event={code:sum(x['code']==code for x in events) for code in c.DIAGNOSTICS}
    return {'cases':cases,'case_count':12,'claim_count':13,'provider_judgments':len(evaluations),
      'origin_counts':dict(Counter(x['content_origin']['kind'] or 'ORIGIN_UNCERTAIN' for x in assignments.values())),
      'function_counts':dict(Counter(x['epistemic_function']['kind'] or 'FUNCTION_UNCERTAIN' for x in assignments.values())),
      'origin_function_combinations':dict(Counter((x['content_origin']['kind'] or 'ORIGIN_UNCERTAIN')+' + '+
          (x['epistemic_function']['kind'] or 'FUNCTION_UNCERTAIN') for x in assignments.values())),
      'atomicity_counts':dict(Counter(x['atomicity'] for x in assignments.values())),
      'obligation_counts_by_contract':dict(Counter(v['contract'] for v in evaluations)),
      'secondary_obligations_discovered':sum(len(b['claim_obligation_set']['dependencies']) for b in discoveries.values()),
      'claim_ref_count':sum(d['resolution']=='CLAIM_REF' for b in discoveries.values() for d in b['claim_obligation_set']['dependencies']),
      'diagnostic_count_unit':'affected claims; event counts and evidence also retained',
      'diagnostic_counts':counts,'diagnostic_event_counts':counts_by_event,'diagnostic_events':events,
      'overall_counts':dict(Counter(v['overall'] or v['status'] for v in aggregates.values())),
      'scientific_success_not_inferred_from_completion':True}
