"""Deterministic premeasurement gate and historical byte preservation."""
import hashlib
import inspect
import json
from pathlib import Path
import subprocess
import extractor as e
import validation as v
H=Path(__file__).resolve().parent;R=H.parents[1]
BASE='8f488b3b02973370e26fd970a5fd5a8d56e8bec6'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def allowed(p):return p.startswith('distance/inquiry-unitization-calibration-v0.1/') or p in ['docs/PROBLEM_FRAMES-inquiry-unitization-calibration-v0.1.md','distance/review/inquiry-unitization-calibration-v0.1.md']
def preserve():
    p=read(H/'preservation.json');require(p['baseline']==BASE,'Baseline')
    for path,digest in {**p['tracked'],**p['runtime']}.items():require(sha(R/path)==digest,'Historical bytes changed: '+path)
    changes=subprocess.check_output(['git','diff','--name-only',BASE,'--'],cwd=R,text=True).splitlines()+subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines()
    require(all(allowed(x) for x in changes),'Out-of-scope changes')
    require(subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip()=='experiment-h4-inquiry-unitization','Wrong branch')
    subprocess.check_call(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=R)
    return {'tracked_files':len(p['tracked']),'historical_runtime_files':len(p['runtime']),'unchanged':True}
def gate():
    m=read(H/'manifest.json');require(len(m['cases'])==len(m['case_order'])==18,'18 cases')
    rows=[];canonical={}
    for row in m['cases']:
        case=read(H/'cases'/f"{row['case_id']}.json");units=e.extract_inquiry_units(case['mapping'])
        require(len(units)==1,'One semantic structure per authored case')
        require(sum(e.complete(u) for u in units)==row['expected_complete'],'Completeness '+row['case_id'])
        require(set(e.missing(units[0]))==set(row['expected_missing']),'Missing component '+row['case_id'])
        a=v.assess_deterministically(case);result=v.validate(case,a);require(result['validation_passed'],'Deterministic validation '+str(result))
        require(not v.polarity_audit(case),'IQ_POLARITY_GATING')
        if row['kind']=='primary':canonical.setdefault(row['mechanism'],set()).add(e.canonical(units[0]))
        rows.append({'case_id':case['case_id'],'fields_scanned':list(case['mapping']),'scan':e.scan(case['mapping']),'coverage':result,'missing':e.missing(units[0])})
    require(len(canonical)==4 and all(len(x)==1 for x in canonical.values()),'Triplet equivalence')
    require('negative_inference' not in inspect.getsource(e),'IQ_POLARITY_GATING')
    regressions=[]
    for p in sorted((H/'regression-fixtures').glob('*.json')):
        case=read(p);source=R/case['historical_packet'];require(sha(source)==case['historical_packet_sha256'],'H3 packet')
        require(case['mapping']==json.loads(source.read_text().split('CASE PACKET\n')[1])['ablated_mapping'],'Historical mapping changed')
        assessment=v.assess_deterministically(case);result=v.validate(case,assessment)
        require(result['validation_passed'] and result['inquiry_role_coverage']['complete_units_found']==1,'H3 coverage gap')
        regressions.append({'case_id':case['case_id'],'assessment':assessment,'validation':result})
    require(len(regressions)==2,'Two offline fixtures')
    return {'provider_calls':0,'cases':rows,'regressions':regressions,'primary_complete':12,'calibration_complete':13,'triplet_equivalence':True,'polarity_gate_absent':True,'preservation':preserve()}
if __name__=='__main__':print(json.dumps(gate(),indent=2))
