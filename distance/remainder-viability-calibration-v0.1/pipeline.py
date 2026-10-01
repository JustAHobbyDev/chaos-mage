"""Frozen extraction, packet reconstruction and stage verification for H.2."""
import json
import re
import secrets
import subprocess
import contracts as c
import runner as r
from common import guard

H,R=r.H,r.R

def units(text):
    # All corpus units are plain prose; newlines and terminal periods separate
    # independently inspectable units. Semicolon clauses retain their parent.
    for m in re.finditer(r'[^.\n]+(?:\.|(?=\n)|$)',text):
        start=m.start()
        while start<m.end() and text[start].isspace():start+=1
        if start<m.end():yield start,m.end(),text[start:m.end()]

def claim_parts(field,text):
    if field=='inference':
        # Independent coordinated conclusions and next-inquiry clauses each get
        # their own context-preserving atomic observation.
        cuts=[m.start() for m in re.finditer(r'; | and settles | and therefore | and excludes ',text)]
        ends=[0,*cuts,len(text)]
        return [(a,b) for a,b in zip(ends,ends[1:]) if a<b]
    if field=='limit' and any(x in text.lower() for x in ['cannot ','do not ','does not ','no claim ','thus ','if q ']):
        return [(0,len(text))]
    return []

def inventory():
    c.require(not list((r.RT/'runs').rglob('attempt.json')),'Measurement already started')
    guard()
    from audit_authoring import verify as author_verify
    c.require(author_verify()['passed'],'Primary authoring gate failed')
    order=sorted(p.stem for p in (H/'cases').glob('*.json'))
    atoms=[];audit=[]
    for cid in order:
        case=r.candidate(cid)
        for field,parent in case['mapping'].items():
            for start,end,text in units(parent):
                ids=[]
                for a,b in claim_parts(field,text):
                    identity='C-'+secrets.token_hex(6);ids.append(identity)
                    atoms.append({'claim_id':identity,'case_id':cid,'source_field':'mapping.'+field,
                        'parent_start':start,'parent_end':end,'exact_parent_text':text,
                        'span_start':start+a,'span_end':start+b,'exact_claim_span':text[a:b],
                        'local_context':parent[max(0,start-160):min(len(parent),end+160)],
                        'downstream_references':[]})
                audit.append({'case_id':cid,'source_field':'mapping.'+field,'start':start,'end':end,
                    'exact_text':text,'claim_ids':ids,'disposition':'represented' if ids else 'supplied_context',
                    'operator_reason':'Explicit inferential assertion or inferential limit, measured in its full parent context.' if ids else
                    'Stipulated state/observation, executable procedure, measurement definition, missing-data statement or scope assumption; does not assert a further licensed target inference.'})
    r.write(H/'claims/inventory.json',atoms);r.write(H/'claims/extraction-audit.json',audit)
    for atom in atoms:r.raw(r.packet('claim-warrant',atom['claim_id']),r.reconstructed_claim_packet(atom).encode())
    for stage in r.STAGES:
        path=H/'schemas'/f'{stage}.schema.json'
        if path.exists():c.require(c.read(path)==c.schema(stage),'Inherited claim schema changed')
        else:r.write(path,c.schema(stage))
    r.write(H/'instrument-reuse.json',{'claim_rubric_sha256':c.sha(H/'CLAIM-WARRANT.md'),
        'claim_schema_sha256':c.sha(H/'schemas/claim-warrant.schema.json'),
        'source':'distance/fault-localized-calibration-v0.1','artifact_rule':'VIABILITY.md replaces H diagnostic precedence'})
    files=list((H/'cases').glob('*.json'));hidden=list((H/'hidden-design').glob('*.json'))+list((H/'authoring-audit').glob('*.json'))
    r.write(H/'manifest.json',{'base_sha':r.git('rev-parse','5d22364').decode().strip(),
        'branch':'experiment-h2-remainder','construct_checkpoint':r.git('rev-parse','0874cb6').decode().strip(),
        'target_checkpoint':r.git('rev-parse','928984a').decode().strip(),
        'primary_checkpoint':r.git('rev-parse','fb06260').decode().strip(),
        'controls_checkpoint':r.git('rev-parse','a77b3cf').decode().strip(),
        'case_order':order,'claim_order':[a['claim_id'] for a in atoms],
        'case_files':r.inventory(files),'hidden_files':r.inventory(hidden),
        'expected_artifact_count':16,'artifact_eligibility':'all cases, including empty measured deletion sets',
        'hypotheses_are_not_answer_keys':True})
    print(json.dumps({'cases':len(order),'claims':len(atoms)}))

def extract_candidates(cid):
    """Operator policy: retain every surviving explicit claim plus signal evidence.

    Exact-text signal candidates deliberately make observations available as possible
    direct entailments even when an explicit surviving inference was missed/deleted.
    No viability labels, hidden audit rationales or intended classes are projected.
    """
    case=r.candidate(cid);deleted=r.unsupported(cid);rows=[]
    def add(inference,field,quote,kind,dependencies):
        source=[{'source_field':field,'exact_text':quote}]
        c.cited_spans(source,case,deleted,surviving=True,mapping_only=True)
        if any(x['inference']==inference and x['source_spans']==source for x in rows):return
        rows.append({'remainder_id':f'R{len(rows)+1:02d}','inference':inference,
            'source_spans':source,'provenance':kind,'dependency_references':dependencies})
    deleted_ids={a['claim_id'] for a in deleted}
    for atom in r.claims():
        if atom['case_id']!=cid or atom['claim_id'] in deleted_ids:continue
        add(atom['exact_claim_span'],atom['source_field'],atom['exact_claim_span'],'exact_surviving_claim',[atom['claim_id']])
    # Independently surviving observations may already embody the useful result.
    # Split around any deleted signal claims; never restore a deleted whole field.
    signal=case['mapping']['signal']
    for start,end,text in units(signal):
        if any(a['source_field']=='mapping.signal' and start<a['span_end'] and end>a['span_start'] for a in deleted):continue
        add(text,'mapping.signal',text,'exact_observation_candidate',[])
    return {'case_id':cid,'ablated_mapping_sha256':c.digest(json.dumps(r.delete_claims(case['mapping'],deleted),sort_keys=True).encode()),
        'candidates':rows,'extraction_audit':{'fields_searched':c.FIELDS,
        'policy':'All surviving measured inferential spans and independent signal units; stated operations are executable context, not newly asserted results. Judge may add cited direct entailments.',
        'no_viability_labels':True}}

def prepare(stage):
    guard()
    if stage=='artifact':
        r.committed(H/'claim-warrant-freeze.json');r.verify_results('claim-warrant',True)
        cases=c.read(H/'manifest.json')['case_order']
        for cid in cases:r.write(H/'remainder-candidates'/f'{cid}.json',extract_candidates(cid))
        r.write(H/'artifact-manifest.json',{'claim_freeze_commit':r.git('log','-1','--format=%H','--',r.rel(H/'claim-warrant-freeze.json')).decode().strip(),
            'claim_freeze_sha256':c.sha(H/'claim-warrant-freeze.json'),'case_order':cases,
            'deletions':{cid:[a['claim_id'] for a in r.unsupported(cid)] for cid in cases},
            'empty_deletion_cases':[cid for cid in cases if not r.unsupported(cid)],
            'subsets':False,'repair':False,'candidate_files':r.inventory((H/'remainder-candidates').glob('*.json'))})
        for cid in cases:r.raw(r.packet('artifact',cid),r.ablation_text(cid).encode())
    paths=list(H.rglob('*'))+[R/'docs/EXPERIMENT-RECOVERY-POLICY.md',R/'docs/PROBLEM_FRAMES-remainder-viability-calibration-v0.1.md']
    r.write(H/f'{stage}-prepared.json',{'at':r.now(),'parent_commit':r.head(),'stage':stage,'files':r.inventory(paths),'order':r.order(stage)})
    verify(stage)

def verify(stage=None,commit=False):
    counts=guard();m=c.read(H/'manifest.json');cases=m['case_order']
    from audit_authoring import verify as author_verify
    c.require(author_verify()['passed'],'Primary authoring gate failed')
    c.require(len(cases)==16 and len(set(cases))==16,'Wrong case count')
    r.hashes(m['case_files']);r.hashes(m['hidden_files'])
    for cid in cases:
        c.require(re.fullmatch(r'H2-[0-9a-f]{12}',cid),'Nonopaque case ID')
        c.require(set(r.candidate(cid))=={'source','target','mapping'},'Hidden case fields')
    designs=[c.read(H/'hidden-design'/f'{cid}.json') for cid in cases]
    c.require(sum(not d['is_control'] for d in designs)==12,'Primary count')
    c.require({d['control'] for d in designs if d['is_control']}==set('ABCD'),'Control identities')
    for name in ['PROTOCOL.md','VIABILITY.md','CLAIM-WARRANT.md']:
        r.committed(H/name,m['construct_checkpoint'])
    r.committed(H/'targets.json',m['target_checkpoint'])
    for checkpoint in ['primary_checkpoint','controls_checkpoint']:
        subprocess.check_call(['git','merge-base','--is-ancestor',m['target_checkpoint'],m[checkpoint]],cwd=R)
    reuse=c.read(H/'instrument-reuse.json')
    old=H.with_name('fault-localized-calibration-v0.1')
    c.require((H/'CLAIM-WARRANT.md').read_bytes()==(old/'CLAIM-WARRANT.md').read_bytes(),'Claim rubric changed')
    c.require((H/'schemas/claim-warrant.schema.json').read_bytes()==(old/'schemas/claim-warrant.schema.json').read_bytes(),'Claim schema changed')
    atoms=r.claims();byid={a['claim_id']:a for a in atoms}
    c.require(len(atoms)==len(byid) and list(byid)==m['claim_order'],'Claim coverage/order')
    audit=c.read(H/'claims/extraction-audit.json');covered=[]
    for atom in atoms:
        text=r.candidate(atom['case_id'])['mapping'][atom['source_field'].split('.')[1]]
        c.require(text[atom['span_start']:atom['span_end']]==atom['exact_claim_span'],'Claim span drift')
        c.require(text[atom['parent_start']:atom['parent_end']]==atom['exact_parent_text'],'Parent drift')
        c.require(atom['parent_start']<=atom['span_start']<atom['span_end']<=atom['parent_end'],'Claim outside parent')
        c.require(r.packet('claim-warrant',atom['claim_id']).read_text()==r.reconstructed_claim_packet(atom),'Claim packet changed')
    for row in audit:covered+=row['claim_ids']
    c.require(sorted(covered)==sorted(byid),'Extraction claim coverage')
    for cid in cases:
        for field in c.FIELDS:
            text=r.candidate(cid)['mapping'][field];cursor=0
            rows=[a for a in audit if a['case_id']==cid and a['source_field']=='mapping.'+field]
            for row in rows:
                c.require(row['start']>=cursor and not text[cursor:row['start']].strip(),'Extraction gap/overlap')
                c.require(text[row['start']:row['end']]==row['exact_text'],'Extraction citation drift');cursor=row['end']
            c.require(not text[cursor:].strip(),'Unaudited text')
    for stage_name in ([stage] if stage else r.STAGES):
        c.require(c.read(H/'schemas'/f'{stage_name}.schema.json')==c.schema(stage_name),'Schema drift')
        p=H/f'{stage_name}-prepared.json'
        if p.exists():
            prep=c.read(p);r.hashes(prep['files'])
            if commit:
                r.committed(p)
                for path in prep['files']:r.committed(R/path)
    if (H/'artifact-manifest.json').exists():
        r.committed(H/'claim-warrant-freeze.json')
        manifest=c.read(H/'artifact-manifest.json');c.require(manifest['case_order']==cases,'Artifact eligibility drift')
        r.hashes(manifest['candidate_files'])
        for cid in cases:
            c.require(c.read(H/'remainder-candidates'/f'{cid}.json')==extract_candidates(cid),'Candidate extraction drift')
            c.require(r.packet('artifact',cid).read_text()==r.ablation_text(cid),'Artifact packet/deletion drift')
    return {'historical_preservation':counts,'claims':len(atoms),'cases':cases}

if __name__=='__main__':
    import sys
    if sys.argv[1]=='inventory':inventory()
    else:raise ValueError('Unknown action')
