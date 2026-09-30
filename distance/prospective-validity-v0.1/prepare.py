"""Lossless historical import and frozen textual decomposition, no classification."""
from collections import Counter
from pathlib import Path
import json
import random
import subprocess
import yaml
import contracts as c

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
E = ROOT/'distance/anti-collapse-natural-recovery-v0.1'
BASE = 'da8cb8d91505d68e65ea8f2d3910f4ca34a03c3b'

def git(*args): return subprocess.check_output(['git',*args], cwd=ROOT)
def dump(p,v):
    if p.exists():
        c.require(c.read(p)==v, 'Existing preparation differs: '+str(p)); return
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f: json.dump(v,f,indent=2,ensure_ascii=False); f.write('\n')
def copy(p,b):
    if p.exists():
        c.require(p.read_bytes()==b, 'Existing preparation differs: '+str(p)); return
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f: f.write(b)
def rel(p): return str(p.relative_to(ROOT))
def provenance(p):
    b=p.read_bytes(); c.require(git('show',f'{BASE}:{rel(p)}')==b,'Source differs from base')
    return {'path':rel(p),'sha256':c.digest(b),'source_commit':git('log','-1','--format=%H',BASE,'--',rel(p)).decode().strip(),'verified_at_commit':BASE}

# Exact focused substrings; the complete original supplies all shared grammar,
# methods and qualifications. Lists of examples/methods are not separate requirements.
SPLITS = {
'E001-A-0':['independently dated, comparable reference series','securely ordered opposite endpoints'],
'E001-A-1':['reproducible feature classification','support for a single persistent transition'],
'E001-A-2':['the bundle’s relevant documents are comparable to the references','feature states reflect contemporaneous, exclusive use'],
'E002-A-0':['usable request-path, traversal-count and version/configuration records','a comparable pre-regression window'],
'E002-A-1':['candidate separability','overlapping load coverage'],
'E002-A-4':['Establish bounded causal contribution through the proposed removal and controlled reintroduction at comparable load, demonstrating disappearance and restoration of the residual.','If replay is used, establish its representativeness for the production paths and load strata covered by the claim.'],
'E002-B-1':['A pre-regression window with comparable instrumentation must exist','load covariates overlapping the post-regression load range'],
'E008-A-0':['usable documentary sequences','overlapping shared developments'],
'E009-B-2':['anchored units exist','their dates are sound'],
'E009-B-4':['Chance-match rate','independence of feature classes'],
'E010-A-1':['proposed checks discriminate among retained mechanisms','can detect a mechanism before using contradiction to eliminate it','assess pilot responses under comparable demand, staffing and case mix while checking concurrent changes and adjacent-handoff delay'],
'E011-A-0':['multiple authentic, sufficiently independent series','overlap'],
'E011-A-1':['reliable calendar anchors','internal ordering'],
'E012-A-0':['access to original physical items','suitable imaging equipment',"the conservator's exposure and handling approval"],
'E014-B-0':['The candidate functions','the activation definition','the user scenarios','the checkpoint requirements'],
'E014-B-3':['the full variant reaches activation at baseline','each omission variant remains a functioning prototype without altering unrelated checkpoint requirements','restoration recovers activation under comparable conditions'],
'E015-A-0':['participation by multiple bidders','authenticated records covering multiple checkpoints'],
'E015-B-0':['more than one bidder took part','authenticated records exist for more than one bidder at more than one checkpoint'],
'E017-A-0':['Identify the proposed components and dependencies','verify through implementation checks or pilot probes that component or bundle removal produces the intended availability change while preserving the other specified conditions'],
'E017-A-1':['Define and validate observable activation and timestamped progress measurements.','Establish whether the study measures executable activation or only prototype completion, retaining the mapping\'s corresponding inference limits.'],
'E017-A-2':['manipulation fidelity','starting-state comparability'],
'E017-B-0':["enumerating the proposed redesign's components from the proposal",'mapping their dependencies, designating inseparable sets as bundles before probing'],
'E017-B-1':['defining activation observably','confirming it can be recorded in an executable flow'],
'E017-B-4':['Resolving power','window adequacy'],
'E018-A-1':['Fix and document the activation definition and observation window before withdrawal','measure the full-design baseline to establish that completion occurs sufficiently often for a drop to be observable'],
'E018-B-2':['Cohort comparability','noise floor'],
'E021-A-0':['comparable timestamps','reconstructable routes'],
'E021-B-0':['whether ticket histories exist for the chosen case family and period','consistent start, end and intermediate events'],
'E022-A-0':['Verify timestamp accuracy against actual workflow movements','confirm that stage queues and waiting times can be reconstructed'],
'E022-A-1':['Confirm that an authorized input change can be applied abruptly, quantified and held','document baseline queues, in-flight work, demand and staffing'],
'E022-B-0':['stage-level timestamps must exist','record when work actually moved rather than when it was logged'],
'E022-B-3':['baseline backlog, in-flight items, staffing and demand must be documented','the observation window must cover several multiples of the longest stage, batch or meeting cycle'],
'E022-B-4':['the workflow, staffing and shared approvers must stay comparable during the run','behavioural reactions to the announced change must not dominate the response'],
'E023-A-0':['version and configuration labels','latency measurement reliability','workload and load comparability'],
'E023-A-1':['Establish a discriminating empirical contrast through the proposed repeated version-by-load comparisons, with sufficient precision and controls for warm-up, order and changing dependencies.','Attribution to an individual change requires technically valid isolation through the proposed revision or revert tests.'],
'E025-A-3':["Verify that the checkpoint ordering represents the cohort's route",'measurements across probes are comparable','For any claimed pilot support, establish comparable case composition, demand, staffing and timing definitions before and after the confined change.'],
'E025-B-5':['The route must be genuinely sequential for the case type','collapsing parallel approvals or rework loops into single checkpoints must not hide the delay-bearing step'],
'E028-A-0':['Fix the latency metric, exceedance margin, inconclusive band, and repeat count before testing','use repeated baseline and full-delta replay runs to establish baseline pass, full-delta failure, and distinguishable outcomes under identical load'],
'E028-A-2':['Verify control stability through interleaved runs','confirm that the retained configuration repeatedly reproduces the exceedance','Claim 1-minimality only when every single-member removal has a resolved nonfailing result.'],
'E028-B-1':['fully enumerated','can be applied or reverted individually or in groups'],
'E029-A-0':['a stable activation definition','funnel instrumentation','follow-up window'],
'E029-A-1':['components can be independently withheld','configurations held fixed'],
'E029-B-4':['the proposed redesign is, or will be, implemented','exposed to live signup cohorts large enough per arm that the reference band is narrower than the shifts of interest'],
'E030-B-0':['Existence','coverage of contemporaneous records for the post-compositional phase'],
'E030-B-3':['number of surviving witnesses','whether the draft is manuscript, typescript or mixed','how many hands are present'],
'E030-B-4':['candidate assembly sequences differ at transitions supported by independently graded evidence','the ranking is stable under alternative unit segmentation','is not driven by uneven record survival'],
}

def prepare():
    c.require(not (HERE/'taxonomy-prepared.json').exists(), 'Preparation already frozen')
    # Read all required source directories in full. Record every byte, including
    # artifacts not admitted to judge packets. Never write to those directories.
    required = [ROOT/p for p in ['distance/review/anti-collapse-natural-recovery-v0.1.md','distance/review/anti-collapse-benchmark-v0.1.md','distance/MODEL-v0.3.md','distance/review/transfer-validity-calibration-v0.3.md']]
    for folder in (E, ROOT/'distance/anti-collapse-v0.1'):
        required += [p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    sources = {rel(p):provenance(p) for p in required}
    preserved = {}
    for name in git('ls-tree','-r','--name-only',BASE).decode().splitlines():
        if name in ('docs/HANDOFF-prospective-validity.md','docs/PROBLEM_FRAMES.md'): continue
        p=ROOT/name; b=p.read_bytes(); c.require(b==git('show',f'{BASE}:{name}'),'Historical byte drift: '+name)
        preserved[name]=c.digest(b)
    dump(HERE/'preservation.json', {'base_commit':BASE,'files':preserved})
    manifest=c.read(E/'operator-manifest.json'); admission=c.read(E/'admission.json')
    generations={x['case_id']:x for x in c.read(E/'generation-freeze.json')['runs']}
    judgments={x['id']:x for x in c.read(E/'validity-freeze.json')['runs']}
    inputs=[]; parents=[]; children=[]; seen_splits=set()
    for row in manifest['mappings']:
        cid=row['case_id']; src=ROOT/row['source_path']; sources[rel(src)]=provenance(src)
        y=yaml.safe_load(src.read_text()); c.require(c.sha(src)==row['source_sha256'],'Instrument hash')
        ip=E/'generation-inputs'/f'{cid}.json'; gp=E/'generations'/f'{cid}.json'
        inp=c.read(ip); gen=c.read(gp)
        c.require(c.sha(gp)==generations[cid]['response_sha256'],'Generation hash')
        c.require(inp['source']=={'name':y['extraction']['name'],'practice':y['extraction']['practice'],'instrument':y['instrument']},'Instrument import')
        c.require(inp['target']==gen['target'],'Target drift')
        copy(HERE/'imports/generations'/gp.name,gp.read_bytes())
        # The packet assessment unit is the unchanged five-field mapping; whole
        # generated payload is imported for independent byte-level verification.
        clean={'source':inp['source'],'target':{**inp['target'],'evidence':[]},'mapping':gen['mapping']}
        dump(HERE/'imports/candidates'/f'{cid}.json',clean)
        inputs.append({**row,'generation':provenance(gp),'input':provenance(ip),'fidelity_pass':next(x['audit_pass'] for x in admission['cases'] if x['case_id']==cid)})
        for family in 'AB':
            jp=E/'validity'/f'validity-{cid}-{family}.json'; j=c.read(jp); v=j['validity']
            c.require(c.sha(jp)==judgments[jp.stem]['response_sha256'],'Judgment hash')
            copy(HERE/'imports/historical-judgments'/jp.name,jp.read_bytes())
            for i,statement in enumerate(v['unresolved_conditions']):
                key=f'{cid}-{family}-{i}'; pid=f'P{len(parents)+1:04}'
                parents.append({'parent_condition_id':pid,'case_id':cid,'original_family':family,'original_model':'gpt-6-astra' if family=='A' else 'claude-fable-5-1[1m]', 'original_final_status':v['final_status'],'original_criterion':None,'criterion_attribution_note':'No explicit condition-to-criterion association in source array; not inferred from rationale.','verbatim_condition':statement,'verbatim_resolution_method_if_present':statement,'resolution_encoding':'Embedded in condition text; no separate resolution field exists. Full text retained without inferred extraction.','verbatim_rationale_context':{k:v[k]['rationale'] for k in ('mechanism_fidelity','target_fidelity','operational_coherence')},'verbatim_overall_rationale':v['rationale'],'source':provenance(jp),'source_field':f'/validity/unresolved_conditions/{i}','extraction_key':key})
                clauses=SPLITS.get(key,[statement])
                if key in SPLITS: seen_splits.add(key)
                for clause in clauses:
                    c.require(statement.count(clause)==1, f'Nonunique/missing span {key}: {clause}')
                    start=statement.index(clause)
                    children.append({'parent_condition_id':pid,'case_id':cid,'source_field':f'/validity/unresolved_conditions/{i}','source':provenance(jp),'span_start':start,'span_end':start+len(clause),'atomic_text':clause,'shared_qualifying_context':statement,'decomposition_note':'Independent clauses separated; full parent retains shared scope and methods.' if len(clauses)>1 else 'Retained as one condition; method/example lists and mutually dependent qualifications remain together.'})
    c.require(seen_splits==set(SPLITS),'Unused split override')
    c.require(len(parents)==139 and Counter(p['original_family'] for p in parents)=={'A':52,'B':87},'Parent coverage')
    # IDs deliberately reveal neither case nor historical source family.
    ids=list(range(1,len(children)+1)); random.Random(20260930071).shuffle(ids)
    for child, n in zip(children,ids): child['atomic_condition_id']=f'Q{n:04}'
    dump(HERE/'condition-inventory/parents.json',parents)
    dump(HERE/'condition-inventory/atomic.json',children)
    dump(HERE/'condition-inventory/coverage.json',{'parents':139,'by_historical_family':{'A':52,'B':87},'atomic_count':len(children),'split_parent_count':len(SPLITS),'policy':'Exact source spans; no category labels; separately sourced overlaps retained.'})
    dump(HERE/'operator-manifest.json',{'cases':inputs,'fidelity_source':provenance(E/'admission.json'),'sources':sources,'operator_blinded':False,'prospective_comparison_boundary':'No old/new comparison during prospective measurement.'})
    for child in children:
        body={**c.read(HERE/'imports/candidates'/f'{child["case_id"]}.json'),'condition_id':child['atomic_condition_id'],'atomic_condition':child['atomic_text'],'necessary_source_excerpt':child['shared_qualifying_context']}
        prompt=(HERE/'TAXONOMY.md').read_text()+'\nCASE PACKET\n'+json.dumps(body,indent=2,ensure_ascii=False)+'\n'
        copy(HERE/'packets/taxonomy'/f'{child["atomic_condition_id"]}.txt',prompt.encode())
    order=[x['atomic_condition_id'] for x in children]; random.Random(20260930072).shuffle(order)
    dump(HERE/'execution-orders/taxonomy.json',{'seed':20260930072,'order':order})
    for stage in ('taxonomy',):
        dump(HERE/'schemas'/f'{stage}.schema.json',c.schema(stage)); dump(HERE/'schemas'/f'{stage}-wire.schema.json',c.wire(c.schema(stage)))
    cfg=c.read(E/'execution-config.json')
    cfg['families']={'A':cfg['families']['A']}; cfg['expected_cli_versions']={'A':'codex-cli 0.157.1'}; cfg['executable_sha256']={'A':cfg['executable_sha256']['A']}
    binary=Path(cfg['families']['A']['cli']).resolve(); native=binary.parents[2]/'codex-linux-x64/vendor/x86_64-unknown-linux-musl/codex/codex'
    c.require(c.sha(binary)==cfg['executable_sha256']['A'],'CLI wrapper drift')
    cfg.update({'scheduler':'Sequential independently frozen Experiment F order','harness_retries':0,'allowed_stages':['taxonomy','prospective'],'probe_limit_per_stage':1,'authorized_measurements':len(children)+30,'model_status':'Historically accepted research judge; no candidate qualification claim','entrypoint_realpath':str(binary)})
    # Discover native executable selected by the pinned package, without reading auth.
    package=binary.parents[1]
    natives=list(package.glob('**/vendor/*/bin/codex'))
    c.require(len(natives)==1,'Expected one native Codex executable')
    cfg['native_executable']={'path':str(natives[0]),'sha256':c.sha(natives[0])}
    dump(HERE/'execution-config.json',cfg)
    dump(HERE/'source-read-evidence.json',{'required_sources':sources,'read_mode':'Full bytes read; JSON decoded for extraction; Git source bytes and hashes verified','base_commit':BASE})
    print(json.dumps({'parents':len(parents),'atomic':len(children),'authorized_total_calls':len(children)+32}))

if __name__=='__main__': prepare()
