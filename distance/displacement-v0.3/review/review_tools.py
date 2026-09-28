"""Post-freeze inventory and supplementary ordering; never invokes providers."""
import argparse
from collections import Counter
from datetime import datetime
from itertools import combinations
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import runner as r
import metrics as m

def compute():
 r.verify_admission(True)
 values=r.published('displacement');r.frozen('displacement',True)
 rows={x['case_id']:x for x in r.manifest()};ad={x['case_id']:x for x in r.read(r.HERE/'admission.json')['cases']}
 inventory=[]
 for cid in sorted({k[0] for k in values}):
  a,b=(values[(cid,f)] for f in 'AB')
  inventory.append({'case_id':cid,'target_id':rows[cid]['target_id'],'core':rows[cid]['core'],'variant_of':rows[cid]['variant_of'],'cohort':ad[cid]['cohort'],'classes':{'A':a['class'],'B':b['class']},'boundary':{f:values[(cid,f)]['boundary_status'] for f in 'AB'},'post_result_status':m.post_result_status(a,b),'dimension_disagreements':{d:{'A':a['dimensions'][d]['level'],'B':b['dimensions'][d]['level']} for d in r.c.DIMS if a['dimensions'][d]['level']!=b['dimensions'][d]['level']}})
 relations=[]
 for target in sorted({x['target_id'] for x in inventory}):
  for x,y in combinations([x for x in inventory if x['target_id']==target],2):
   cid,did=x['case_id'],y['case_id'];cohorts=[ad[c]['cohort'] for c in (cid,did)]
   relations.append({'target_id':target,'case_1':cid,'case_2':did,'cohorts':cohorts,'comparison_group':cohorts[0] if cohorts[0]==cohorts[1] else 'cross-cohort','core_only':rows[cid]['core'] and rows[did]['core'],**{f:m.relation(r.c.BANDS.index(values[(cid,f)]['class']),r.c.BANDS.index(values[(did,f)]['class'])) for f in 'AB'}})
 # Cross-cohort relations are described separately; never included in either reliability cohort.
 ordering={'relations':relations,'counts':dict(Counter(x['comparison_group'] for x in relations)),'cross_cohort_agreement':m.agreement((x['A'],x['B']) for x in relations if x['comparison_group']=='cross-cohort')}
 freezes={stage:r.frozen(stage,True) for stage in ('validity','displacement')}
 sessions=[];audit={}
 for p in r.read(r.HERE/'preflight.json')['entries']:sessions.append(p['audit']['metadata']['session_id'])
 for stage,freeze in freezes.items():
  previous=None;retry={f:0 for f in 'AB'};returned={f:set() for f in 'AB'}
  for run in freeze['runs']:
   reservation=run['reservation'];result=run['audit'];metadata=result['metadata'];sessions.append(metadata['session_id'])
   started=datetime.fromisoformat(reservation['started_at']);finished=datetime.fromisoformat(result['finished_at'])
   r.require(started<=finished and (previous is None or previous<=started),'Nonsequential execution timestamps');previous=finished
   r.require(reservation['configuration']==r.config(),'Execution configuration changed')
   retry[run['family']]+=metadata['formatting_retries']['observed_formatting_retries'];returned[run['family']].update(metadata['returned_model_identifiers'])
  audit[stage]={'planned_judgments':len(r.order(stage)),'observed_judgments':len(freeze['runs']),'first_started_at':freeze['runs'][0]['reservation']['started_at'],'last_finished_at':freeze['runs'][-1]['audit']['finished_at'],'exposed_formatter_retries':retry,'returned_identifiers':{f:sorted(v) for f,v in returned.items()},'served_snapshots':{'A':None,'B':None}}
 r.require(len(sessions)==len(set(sessions)),'Session reused across stages or probes')
 audit['unique_sessions_including_probes']=len(sessions)
 # Check each family received byte-identical substantive packets, from raw hashes.
 for stage,freeze in freezes.items():
  by={ (x['case_id'],x['family']):x for x in freeze['runs']}
  for cid in {x['case_id'] for x in freeze['runs']}:
   r.require(by[(cid,'A')]['reservation']['packet_sha256']==by[(cid,'B')]['reservation']['packet_sha256'],'Family packet asymmetry')
 audit['identical_family_packets']=True
 # Verify chronology from committed checkpoints and frozen execution evidence.
 prep=r.git('log','-1','--format=%H','--',str(r.HERE/'prepared.json')).decode().strip()
 admission=r.git('log','-1','--format=%H','--',str(r.HERE/'admission-freeze.json')).decode().strip()
 baseline=r.read(r.HERE/'checkpoint.json')['baseline_commit']
 for older,newer in ((baseline,prep),(prep,admission)):
  r.require(older!=newer and r.subprocess.run(['git','merge-base','--is-ancestor',older,newer],cwd=r.ROOT).returncode==0,'Checkpoint ancestry invalid')
 probes=r.read(r.HERE/'preflight.json')
 r.require(datetime.fromisoformat(r.read(r.HERE/'prepared.json')['created_at'])<datetime.fromisoformat(probes['frozen_at'])<datetime.fromisoformat(audit['validity']['first_started_at']),'Preparation/probe/measurement ordering invalid')
 r.require(datetime.fromisoformat(audit['validity']['last_finished_at'])<=datetime.fromisoformat(freezes['validity']['at'])<datetime.fromisoformat(r.read(r.HERE/'admission.json')['at'])<datetime.fromisoformat(audit['displacement']['first_started_at']),'Validity freeze/admission/displacement ordering invalid')
 r.require(datetime.fromisoformat(audit['displacement']['last_finished_at'])<=datetime.fromisoformat(freezes['displacement']['at']),'Results reviewed before freeze')
 return {'inventory.json':inventory,'all-target-ordering.json':ordering,'execution-audit.json':audit}

def build():
 for name,value in compute().items():r.write_new(HERE/name,value)

def verify():
 for name,value in compute().items():r.require(r.read(HERE/name)==value,f'Review artifact changed: {name}')
 # Supplement frozen completion verifier without changing its prepared bytes.
 for row in r.read(r.HERE/'packet-index.json'):
  path=r.ROOT/row['path'];r.require(r.c.sha(path)==row['sha256'],'Published packet hash mismatch')
  r.require(path.read_bytes()==r.packet({'case_id':row['case_id']},'displacement').encode(),'Published packet differs from measured prompt')
 import verify_completion
 result=verify_completion.verify(True)
 print(result)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['build','verify']);args=p.parse_args();globals()[args.command]()
