#!/usr/bin/env python3
"""H.1 authoring verification. Provider execution is blocked by the failed gate."""
import argparse, hashlib, json, math, re, subprocess
from pathlib import Path
import contracts as c
H=Path(__file__).resolve().parent;R=H.parent.parent
BASE='6d13e5203a40fbb4d3f0af10362eb57123beb524'
POLICY='b92cf1350a4cd658bff6f5c729deb9dd55da38ef'
ALLOWED=['distance/fault-localized-calibration-v0.2/','distance/review/fault-localized-calibration-v0.2.md','docs/PROBLEM_FRAMES-fault-localized-calibration-v0.2.md']
def allowed(p):return any(p.startswith(x) if x.endswith('/') else p==x for x in ALLOWED)
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def guard():
 p=c.read(H/'preservation.json');c.require(p['baseline']==BASE,'Wrong baseline')
 baseline=git('show',POLICY+':distance/fault-localized-calibration-v0.2/preservation.json')
 c.require(baseline==(H/'preservation.json').read_bytes(),'Preservation manifest changed')
 for name,digest in {**p['files'],**p['historical_runtime']}.items():c.require(c.sha(R/name)==digest,'Inherited bytes changed: '+name)
 changes=git('diff','--name-only',BASE,'--').decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines()
 c.require(all(allowed(x) for x in changes),'Out-of-scope changes')
 return {'tracked':len(p['files']),'runtime':len(p['historical_runtime'])}
def draft(cid):return c.read(H/'authoring-attempts'/f'{cid}.json')
def design_rows():return c.read(H/'hidden-design/authoring-attempts.json')+c.read(H/'hidden-design/revised-attempts.json')
def verify():
 counts=guard();reuse=c.read(H/'instrument-reuse.json');c.require(reuse['base']==BASE,'Scoring base')
 for name,digest in reuse['files'].items():
  expected=git('show',BASE+':distance/fault-localized-calibration-v0.1/'+name)
  c.require((H/name).read_bytes()==expected and c.sha(H/name)==digest,'Scoring/contracts/schema change')
 for name in ['targets.json','PROTOCOL.md','instrument-reuse.json']:
  c.require(git('show',POLICY+':distance/fault-localized-calibration-v0.2/'+name)==(H/name).read_bytes(),'Policy/target freeze changed')
 targets={t['mechanism_key']:t for t in c.read(H/'targets.json')};rows=design_rows()
 c.require(len(rows)==36 and len({r['case_id'] for r in rows})==36,'Draft coverage')
 c.require({p.stem for p in (H/'authoring-attempts').glob('*.json')}=={r['case_id'] for r in rows},'Unexpected/missing draft')
 results=[]
 for revision in ['direct','conditional','conditional_reporting_only']:
  shortest=set()
  for key,t in targets.items():
   group=[r for r in rows if r['revision']==revision and r['mechanism_key']==key]
   c.require(len(group)==3 and {r['intended_position'] for r in group}=={'local','scope','core'},'Triple composition')
   cases=[draft(r['case_id']) for r in group];first=cases[0]
   c.require(c.sha(R/t['source_input_path'])==t['source_input_sha256'],'Source input changed')
   frozen=c.read(R/t['source_input_path'])
   c.require(t['source']==frozen['source'],'Instrument altered')
   for row,case in zip(group,cases):
    c.require(re.fullmatch('H1-[0-9a-f]{12}',row['case_id']) is not None,'Nonopaque draft id')
    c.require(set(case)=={'source','target','mapping'},'Hidden data in draft')
    c.require(case['source']==t['source'] and case['target']==t['target'],'Source/target drift')
    for field in ['state','operation','signal','limit']:c.require(case['mapping'][field]==first['mapping'][field],'Primary field drift')
    c.require(row['claim_graph_hypothesis']==group[0]['claim_graph_hypothesis'],'Graph topology drift')
    slots=case['mapping']['inference'].split('\n');c.require(len(slots)==4,'Slot count')
    c.require(row['intended_defective_slot']=={'local':3,'scope':2,'core':0}[row['intended_position']],'Slot mapping')
    span=row['intended_defective_span'];text=case['mapping']['inference'];c.require(text[span['start']:span['end']]==span['exact_text']==slots[row['intended_defective_slot']],'Exact span')
    c.require(row['unsupported_span_chars']==len(span['exact_text']) and row['token_estimate']==math.ceil(len(span['exact_text'])/4),'Length estimate drift')
    c.require(row['unsupported_span_fraction']==len(span['exact_text'])/len('\n'.join(case['mapping'].values())),'Fraction drift')
    c.require(all(row['focal_identity_check'].values()),'Focal check failed')
   for slot in range(4):
    unmodified=[case['mapping']['inference'].split('\n')[slot] for row,case in zip(group,cases) if row['intended_defective_slot']!=slot]
    c.require(len(set(unmodified))==1,'Unselected slot changed')
   lengths={r['intended_position']:r['unsupported_span_chars'] for r in group};ratio=max(lengths.values())/min(lengths.values());shortest.update(k for k,v in lengths.items() if v==min(lengths.values()))
   if revision=='conditional_reporting_only':c.require(ratio<=1.10,'Revised length ratio failed')
   results.append({'revision':revision,'mechanism_key':key,'lengths':lengths,'ratio':ratio,'focal_fields_identical':True,'length_gate_passed':ratio<=1.10})
  if revision=='conditional_reporting_only':c.require(shortest=={'local','scope','core'},'Rank balance failed')
 audit=c.read(H/'review/authoring-audit.json')
 from audit_authoring import build
 c.require(audit==build(),'Authored audit/evidence drift')
 c.require(len(audit['core_candidate_audits'])==12,'Core audit coverage')
 for a in audit['core_candidate_audits']:
  case=draft(a['case_id']);span=a['deleted_span'];original=case['mapping']['inference'];ablated=dict(case['mapping']);ablated['inference']=original[:span['start']]+'[DELETED INTENDED CLAIM]'+original[span['end']:]
  c.require(a['ablated_mapping']==ablated,'Non-deletion alteration')
  survivor=a['surviving_material_answer'];c.require(ablated['signal'][survivor['start']:survivor['end']]==survivor['exact_text'],'Surviving citation invalid')
  c.cited_spans([{'source_field':survivor['source_field'],'exact_text':survivor['exact_text']}],case,[{'source_field':span['source_field'],'span_start':span['start'],'span_end':span['end']}],surviving=True,mapping_only=True)
 c.require(not list((H/'cases').glob('*.json')),'Invalid drafts promoted to cases')
 c.require(not list((H/'packets').rglob('*.txt')) and not list((H/'judgments').rglob('*.json')),'Measurement artifacts exist despite failed authoring gate')
 c.require(not list((R/'.runtime/fault-localized-calibration-v0.2').rglob('*')),'Unexpected provider runtime')
 return {'status':'STOPPED_PREMEASUREMENT_DESIGN_GATE','provider_calls':0,'final_cases':0,'planned_final_cases':16,'drafts':len(rows),'core_candidate_audits':len(audit['core_candidate_audits']),'rejected_revised_core_candidates':4,'historical_preservation':counts,'triple_checks':results,'scoring_unchanged':True}
def measurement_gate():
 verify()
 raise ValueError('H.1 authoring gate failed: source-derived material answers survive all revised CORE deletions. No provider launch authorized by this gate.')
def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['verify','measurement-gate']);a=p.parse_args()
 if a.action=='verify':print(json.dumps(verify(),indent=2))
 else:measurement_gate()
if __name__=='__main__':main()
