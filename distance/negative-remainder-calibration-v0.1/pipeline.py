"""Audited all-field extraction, immutable packets and H.3 stage verification."""
import hashlib
import json
import re
import subprocess
import contracts as c
import runner as r
from common import guard
from author_cases import verify as author_verify
H,R=r.H,r.R

def units(text):
    cursor=0
    for line in text.splitlines(keepends=True):
        quote=line.rstrip('\n')
        if quote.strip():yield cursor,cursor+len(quote),quote
        cursor+=len(line)

def atomic_parts(text):
    # The contrast in a single comparative assertion is one claim. These two
    # constructions instead coordinate independently assessable conclusions.
    cuts=[0]
    for delimiter in [', but ', ' and its unique internal root cause']:
        if delimiter in text:cuts.append(text.index(delimiter))
    cuts=sorted(cuts)+[len(text)]
    return list(zip(cuts,cuts[1:]))

def inventory():
    guard();author_verify();c.require(not r.RT.exists(),'Runtime already exists')
    ids=sorted(p.stem for p in (H/'cases').glob('*.json'));atoms=[];audit=[]
    # The operator authoring audit covers every mapping unit. Matching exact
    # authored spans identifies explicit claims, not keyword-based field shortcuts.
    for cid in ids:
        case=r.candidate(cid);d=c.read(H/'hidden-design'/f'{cid}.json')
        explicit=set(d['focal_texts']+d['intended_unsupported'])
        for field,parent in case['mapping'].items():
            for start,end,text in units(parent):
                claims=[]
                if text in explicit:
                    for a,b in atomic_parts(text):
                        identity='C-'+hashlib.sha256((cid+field+str(start+a)).encode()).hexdigest()[:12];claims.append(identity)
                        atoms.append({'claim_id':identity,'case_id':cid,'source_field':'mapping.'+field,
                            'parent_start':start,'parent_end':end,'exact_parent_text':text,
                            'span_start':start+a,'span_end':start+b,'exact_claim_span':text[a:b],
                            'local_context':parent,'downstream_references':[]})
                audit.append({'case_id':cid,'source_field':'mapping.'+field,'start':start,'end':end,'exact_text':text,
                    'claim_ids':claims,'disposition':'atomic_target_assertion' if claims else 'supplied_context',
                    'operator_reason':'Single comparative consequence, evidence limitation, test-selection decision with outcome rationale, or target conclusion.' if claims else
                    'Inspected entry state, baseline procedure, recording context or granted conditions; no separate target result or selected discriminating inquiry.'})
    r.write(H/'claims/inventory.json',atoms);r.write(H/'claims/extraction-audit.json',audit)
    for atom in atoms:r.raw(r.packet('claim-warrant',atom['claim_id']),r.reconstructed_claim_packet(atom).encode())
    for stage in r.STAGES:r.write(H/'schemas'/f'{stage}.schema.json',c.schema(stage))
    r.write(H/'manifest.json',{'base_sha':'e35948a601fefabb648218cde728aa7fdc1651d2','branch':'experiment-h3-negative-remainders',
        'construct_checkpoint':r.git('rev-parse','ebc9ea0').decode().strip(),'target_checkpoint':r.git('rev-parse','24d5aee').decode().strip(),
        'primary_checkpoint':r.git('rev-parse','f4cf37e').decode().strip(),'controls_checkpoint':r.git('rev-parse','dbabb95').decode().strip(),
        'case_order':ids,'claim_order':[a['claim_id'] for a in atoms],
        'case_files':r.inventory((H/'cases').glob('*.json')),
        'hidden_files':r.inventory([*(H/'hidden-design').glob('*.json'),*(H/'authoring-audit').glob('*.json')]),
        'expected_artifact_count':15,'artifact_eligibility':'all cases, including empty measured deletion sets',
        'hypotheses_are_not_answer_keys':True})
    print(json.dumps({'cases':len(ids),'claims':len(atoms)}))

def extract_candidates(cid):
    case=r.candidate(cid);deleted=r.unsupported(cid);deleted_ids={a['claim_id'] for a in deleted}
    rows=[];audit=[]
    for unit in c.read(H/'claims/extraction-audit.json'):
        if unit['case_id']!=cid:continue
        surviving=[x for x in unit['claim_ids'] if x not in deleted_ids]
        candidate_ids=[]
        for claim_id in surviving:
            atom=next(a for a in r.claims() if a['claim_id']==claim_id)
            rid=f'R{len(rows)+1:02d}';candidate_ids.append(rid)
            rows.append({'remainder_id':rid,'inference':atom['exact_claim_span'],
                'source_spans':[{'source_field':atom['source_field'],'exact_text':atom['exact_claim_span']}],
                'provenance':'exact_surviving_claim','dependency_references':[claim_id]})
        audit.append({**unit,'candidate_ids':candidate_ids,'survives':not bool(set(unit['claim_ids'])&deleted_ids),
            'candidate_disposition':'inventoried' if candidate_ids else 'deleted' if unit['claim_ids'] else 'context_only',
            'search_categories':['exclusion','bound','reprioritization','stopping','next_inquiry','insufficiency','negative_evidence'],
            'survival_review':'Surviving explicit target claim included without a role label; other complete units rechecked as entry context or generic procedure with no additional target consequence.'})
    return {'case_id':cid,'ablated_mapping_sha256':c.digest(json.dumps(r.delete_claims(case['mapping'],deleted),sort_keys=True).encode()),
            'candidates':rows,'extraction_audit':audit,'fields_searched':c.FIELDS,'no_role_labels':True}

def prepare(stage):
    guard();author_verify()
    if stage=='artifact':
        r.committed(H/'claim-warrant-freeze.json');r.verify_results('claim-warrant',True)
        cases=c.read(H/'manifest.json')['case_order']
        for cid in cases:r.write(H/'negative-remainders'/f'{cid}.json',extract_candidates(cid))
        r.write(H/'artifact-manifest.json',{'claim_freeze_sha256':c.sha(H/'claim-warrant-freeze.json'),'case_order':cases,
            'deletions':{cid:[a['claim_id'] for a in r.unsupported(cid)] for cid in cases},
            'empty_deletion_cases':[cid for cid in cases if not r.unsupported(cid)],'subsets':False,'repair':False,
            'candidate_files':r.inventory((H/'negative-remainders').glob('*.json'))})
        for cid in cases:r.raw(r.packet('artifact',cid),r.ablation_text(cid).encode())
    paths=list(H.rglob('*'))+[R/'docs/EXPERIMENT-RECOVERY-POLICY.md',R/'docs/PROBLEM_FRAMES-negative-remainder-calibration-v0.1.md']
    r.write(H/f'{stage}-prepared.json',{'at':r.now(),'parent_commit':r.head(),'stage':stage,'files':r.inventory(paths),'order':r.order(stage)})
    verify(stage)

def verify(stage=None,commit=False):
    counts=guard();author_verify();m=c.read(H/'manifest.json');ids=m['case_order']
    c.require(len(ids)==len(set(ids))==15,'Case count');r.hashes(m['case_files']);r.hashes(m['hidden_files'])
    for cid in ids:
        c.require(re.fullmatch(r'H3-[0-9a-f]{12}',cid),'Nonopaque ID')
        c.require(set(r.candidate(cid))=={'source','target','mapping'},'Hidden fields')
    designs=[c.read(H/'hidden-design'/f'{cid}.json') for cid in ids]
    c.require(sum(not d['is_control'] for d in designs)==12,'Primary count')
    c.require({d['control'] for d in designs if d['is_control']}=={'wording','jargon','terse'},'Controls')
    for k in ['construct','target','primary','controls']:
        subprocess.check_call(['git','merge-base','--is-ancestor',m[k+'_checkpoint'],'HEAD'],cwd=R)
    for name in ['PRODUCTIVITY.md','PROTOCOL.md','CLAIM-WARRANT.md']:r.committed(H/name,m['construct_checkpoint'])
    r.committed(H/'targets.json',m['target_checkpoint']);r.committed(H/'AUTHORING.md',m['target_checkpoint'])
    old=H.with_name('remainder-viability-calibration-v0.1')
    for name in ['CLAIM-WARRANT.md','schemas/claim-warrant.schema.json']:
        c.require((H/name).read_bytes()==(old/name).read_bytes(),'Claim instrument drift')
    atoms=r.claims();c.require([a['claim_id'] for a in atoms]==m['claim_order'] and len(atoms)==len(set(m['claim_order'])),'Claim coverage/order')
    audit=c.read(H/'claims/extraction-audit.json')
    c.require(sorted(x for row in audit for x in row['claim_ids'])==sorted(m['claim_order']),'Extraction coverage')
    for a in atoms:
        parent=r.candidate(a['case_id'])['mapping'][a['source_field'].split('.')[1]]
        c.require(parent[a['span_start']:a['span_end']]==a['exact_claim_span'],'Claim drift')
        c.require(parent[a['parent_start']:a['parent_end']]==a['exact_parent_text'],'Parent drift')
        c.require(r.packet('claim-warrant',a['claim_id']).read_text()==r.reconstructed_claim_packet(a),'Packet drift')
    for cid in ids:
        for field in c.FIELDS:
            text=r.candidate(cid)['mapping'][field];cursor=0
            for row in [x for x in audit if x['case_id']==cid and x['source_field']=='mapping.'+field]:
                c.require(row['start']>=cursor and not text[cursor:row['start']].strip(),'Extraction gap')
                c.require(text[row['start']:row['end']]==row['exact_text'],'Extraction quote drift');cursor=row['end']
            c.require(not text[cursor:].strip(),'Unaudited field text')
    for s in ([stage] if stage else r.STAGES):
        c.require(c.read(H/'schemas'/f'{s}.schema.json')==c.schema(s),'Schema drift')
        path=H/f'{s}-prepared.json'
        if path.exists():
            prep=c.read(path);r.hashes(prep['files'])
            if commit:
                r.committed(path)
                for p in prep['files']:r.committed(R/p)
    if (H/'artifact-manifest.json').exists():
        r.committed(H/'claim-warrant-freeze.json');am=c.read(H/'artifact-manifest.json');c.require(am['case_order']==ids,'Artifact order')
        r.hashes(am['candidate_files'])
        for cid in ids:
            c.require(c.read(H/'negative-remainders'/f'{cid}.json')==extract_candidates(cid),'Candidate drift')
            c.require(r.packet('artifact',cid).read_text()==r.ablation_text(cid),'Artifact packet drift')
    return {'historical_preservation':counts,'claims':len(atoms),'cases':len(ids)}

if __name__=='__main__':inventory()
