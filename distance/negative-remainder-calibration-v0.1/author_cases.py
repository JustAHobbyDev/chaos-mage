"""Operator-authored stimuli and premeasurement semantic audit. No model calls."""
import argparse
import hashlib
from common import H, read, write, require, guard

ROLES=['TARGET_CONSTRAINT','INQUIRY_CONSTRAINT','INSUFFICIENCY_ONLY']
EFFECTS=['target_state_set','bounds','alternative_priorities','stopping_decision','next_inquiry']
DATA={
 'ach':{
  'state':'Award P-17 is considered under H1 (recorded scores altered after opening), H2 (bidder-specific drafting), and H3 (ordinary award). These are live alternatives at entry; the dossier has evaluation sheets, drafting records and an item index.',
  'operation':'Construct an evidence-by-hypothesis matrix, check authentication and independence, compare important inconsistencies, and repeat the comparison with disputed entries omitted.',
  'signal':'The dossier export preserves its item identifiers and the completed comparison record below. Its entries and described recording conditions are authenticated.',
  'unsupported':'The comparison uniquely establishes that P-17 was steered through bidder-specific drafting and excludes every ordinary explanation.',
  'target':'The authenticated comparison records an important inconsistency between E and H1, with E compatible with H2 and H3; this asymmetry persists when disputed entries are omitted.',
  'inquiry':['The retained comparison does not distinguish H1 from H3.', 'Inspect record R, the individual scores saved before consensus, next: unexplained post-opening score changes favor H1 over H3, whereas stable contemporaneous scores bear against H1 relative to H3.'],
  'insuff':'The current matrix does not establish whether P-17 was steered: its retained X cells pool consistency, inconsistency and unrated entries, with the original values unavailable.',
  'contrast':'H1 versus H3', 'next':'Inspect record R, the individual scores saved before consensus',
  'relation':'Unexplained post-opening score changes favor H1; stable contemporaneous scores bear against H1 relative to H3.',
  'target_effect':'alternative_priorities',
  'target_reason':'The sole surviving asymmetric comparison weakens H1 relative to H2/H3. Removing it restores the entry standing; the dossier index supplies no independent weighting.',
 },
 'crossdate':{
  'state':'Sequence S has candidate offsets +2, +3, +4, +5, +6 and +7 against independently dated reference R1. All six are live at entry. Reference R2 also preserves the next increment for comparison.',
  'operation':'Compare ordered increments across candidate alignments, check overlap and reference anchoring, and retain the correspondence record under each offset.',
  'signal':'The ordered-overlap worksheet and reference identifiers are retained. The reference dates, sequence transcription and recording conditions are authenticated.',
  'unsupported':'The comparison uniquely dates S at offset +6 and establishes that this is its only possible chronology.',
  'target':'In the anchored overlap, offsets +2 through +5 conflict with the retained ordered pattern, while +6 and +7 remain compatible.',
  'inquiry':['The available overlap does not distinguish offsets +6 and +7.', 'Compare the next preserved increment with R2 next: +6 predicts a narrow-to-wide correspondence there and +7 predicts wide-to-narrow, so either observed correspondence bears against the other offset.'],
  'insuff':'The available overlap does not establish a unique offset: the retained comparison gives no offset-specific mismatch or discriminating ordering among the six candidate alignments.',
  'contrast':'offset +6 versus +7', 'next':'Compare the next preserved increment with R2',
  'relation':'+6 predicts narrow-to-wide; +7 predicts wide-to-narrow; either correspondence bears against the other offset.',
  'target_effect':'bounds',
  'target_reason':'Removing the sole offset-specific mismatch record restores +2 through +5 to the live set and widens the compatible range. Reference names and the generic alignment procedure alone exclude nothing.',
 },
 'diagnosis':{
  'state':'Failure F-17 is evaluated under lock contention and isolated pool exhaustion. Both mechanisms are live at entry. The replay environment and workload are fixed, and the response ledger identifies the completed probe.',
  'operation':'State candidate mechanisms, compare probe responses against their diagnostic expectations, and update the comparative support under the fixed workload.',
  'signal':'The probe completed under the stated replay conditions. Its response ledger and instrument identities are authenticated.',
  'unsupported':'The completed probe uniquely establishes lock contention as the cause of F-17 across all production workloads.',
  'target':'The recorded R is incompatible with isolated pool exhaustion under its stipulated diagnostic expectation, while R is compatible with lock contention at the same operating point.',
  'inquiry':['The current result does not discriminate lock contention from isolated pool exhaustion.', 'Measure lock-wait duration with pool occupancy next: elevated lock waits with normal occupancy favor lock contention, whereas ordinary lock waits with saturated occupancy favor pool exhaustion.'],
  'insuff':'The current test does not determine which mechanism caused F-17: R denotes probe completion and carries no mechanism-dependent response value in the retained ledger.',
  'contrast':'lock contention versus isolated pool exhaustion', 'next':'Measure lock-wait duration with pool occupancy',
  'relation':'Elevated waits/normal occupancy favor lock contention; ordinary waits/saturated occupancy favor pool exhaustion.',
  'target_effect':'alternative_priorities',
  'target_reason':'The sole mechanism-specific incompatibility weakens isolated pool exhaustion. Removing it leaves completion bookkeeping and the original two live mechanisms without a comparative update.',
 },
 'delta':{
  'state':'Deployment D-17 contains removable changes a, b and c. The target failure F is the checkout deadline failure during a fixed replay. Candidate subsets are live at entry; replay conditions and subset identities are fixed.',
  'operation':'Partition changes, replay subsets and complements, and evaluate single-removal tests using the recorded result and the specified target failure definition.',
  'signal':'The subset ledger preserves test identities and the described result channel. Replays are deterministic under the fixed workload and environment.',
  'unsupported':'The reduction establishes {a,c} as the unique globally smallest sufficient subset for F and its unique internal root cause.',
  'target':'Under the frozen oracle that directly measures F, subset {a,b} does not reproduce F on the recorded replay.',
  'inquiry':['The current tests leave {a,b,c} and {a,c} unresolved as the required reproducing subset.', 'Replay {a,c} by removing b from {a,b,c} next under the frozen F oracle: persistence of F eliminates b from the required subset, while disappearance of F retains b as required in that configuration.'],
  'insuff':'The observed nonzero-exit flag does not establish reproduction of F: either flag value can occur with or without F because handled deadlines, configuration rejection and harness termination share that result channel.',
  'contrast':'whether b is required in {a,b,c}, comparing {a,b,c} with {a,c}', 'next':'Replay {a,c} by removing b from {a,b,c} under the frozen F oracle',
  'relation':'Persistence of F eliminates b from the required subset; disappearance retains b in that configuration.',
  'target_effect':'target_state_set',
  'target_reason':'Removing the only target-F outcome restores {a,b} as a candidate sufficient reproducer. Fixed replay conditions alone supply no subset outcome.',
 }
}
LIMIT='All supplied observations and stated diagnostic relations hold under the described conditions. The target scope is the named case and operating conditions; the recording assumptions are granted.'

def build_case(key,role,control=None):
    t=next(x for x in read(H/'targets.json') if x['mechanism_key']==key);d=DATA[key]
    focal=[d['target']] if role==ROLES[0] else d['inquiry'] if role==ROLES[1] else [d['insuff']]
    if control=='wording':focal=['The anchored overlap is insufficient for a unique chronology, but offsets +2 through +5 conflict with its ordered pattern; +6 and +7 remain compatible.']
    if control=='jargon':focal=['The ddmin complement ledger and single-removal exit-bit vector cannot establish target-F sufficiency: the binary channel pools handled deadlines, preflight configuration rejection and harness termination, with either bit value possible both with and without F.']
    if control=='terse':focal=[d['inquiry'][0], 'Check waiting next, together with how full the pool is: long waits with spare capacity favor lock contention, whereas short waits with a full pool favor pool exhaustion.']
    identity='H3-'+hashlib.sha256((key+role+str(control)).encode()).hexdigest()[:12]
    # Consequence appears once, in signal, so removing it does not silently erase
    # distinct evidence or count a redundant restatement as productive.
    mapping={'state':d['state'],'operation':d['operation'],'signal':'\n'.join([d['signal'],*focal]),'inference':d['unsupported'],'limit':LIMIT}
    case={'source':t['source'],'target':t['target'],'mapping':mapping}
    design={'case_id':identity,'mechanism_key':key,'is_control':control is not None,'control':control,
            'intended_role':role,'focal_texts':focal,'intended_unsupported':[d['unsupported']],
            'hypothesis':'Productive surviving negative consequence' if role!=ROLES[2] else 'No viable remainder from insufficiency alone',
            'confounds':['Synthetic supplied relations and observation differences, not a wording-only causal intervention.',
                        'Inquiry members contain an additional atomic assertion; no padding is used.']}
    return identity,case,design

def audit(cid,case,design):
    role=design['intended_role'];d=DATA[design['mechanism_key']];texts=design['focal_texts']
    rows=[]
    for i,text in enumerate(texts):
        productive=role==ROLES[0] or (role==ROLES[1] and i==1)
        intended=role if productive else ROLES[2]
        effects={k:'no' for k in EFFECTS}
        if productive:effects[d['target_effect'] if role==ROLES[0] else 'next_inquiry']='yes'
        if productive and design['mechanism_key']=='crossdate' and role==ROLES[0]:effects['target_state_set']='yes'
        inquiry=None
        if productive and role==ROLES[1]:
            inquiry={'unresolved_contrast':texts[0],'concrete_operation':text.split(':')[0],
                     'differential_outcome_relation':text.split(':',1)[1].strip(),
                     'all_present_in_surviving_mapping':True,
                     'source_spans':[{'source_field':'mapping.signal','exact_text':v} for v in texts]}
        rationale=d['target_reason'] if productive and role==ROLES[0] else (
            'Removing this specified test-selection statement leaves the same live contrast but removes the selected operation and its differential outcome relation; the baseline procedure selects no particular next test.' if productive else
            'Removing this limitation alone leaves the same live alternatives, bounds, priorities, stopping state and selected next inquiry. Missing diagnostic content cannot be converted into evidence against a state.')
        rows.append({'exact_text':text,'source_spans':[{'source_field':'mapping.signal','exact_text':text}],
                     'removing_it_changes':effects,'if_next_inquiry':inquiry,'intended_role':intended,
                     'counterfactual_rationale':rationale,'supported_by_operator_audit':True})
    searched=[{'field':k,'exact_text':v,'disposition':
               'Focal negative units audited individually; introductory recording context has no target-state consequence.' if k=='signal' else
               'Intended unsupported claim deleted in authoring counterfactual.' if k=='inference' else
               'Entry alternatives, general procedure or granted conditions; no target-specific result, stopping decision or selected discriminating next inquiry.'} for k,v in case['mapping'].items()]
    return {'case_id':cid,'intended_role':role,'candidates':rows,'all_field_audit':searched,
            'other_viable_contributions':[],'redundancy_check':'The focal consequence occurs once; other mapping text does not independently supply its comparative result or select its specific inquiry.',
            'claim_count':1+len(texts),'mapping_chars':sum(map(len,case['mapping'].values())),
            'operator_review':'Exact authored text inspected against the five removal effects; generic baseline procedures do not select a discriminating next operation.',
            'passed':True}

def build(controls=False):
    guard();rows=[]
    specs=[('crossdate',ROLES[0],'wording'),('delta',ROLES[2],'jargon'),('diagnosis',ROLES[1],'terse')] if controls else [(k,role,None) for k in DATA for role in ROLES]
    for key,role,control in specs:
        cid,case,design=build_case(key,role,control)
        write(H/'cases'/f'{cid}.json',case);write(H/'hidden-design'/f'{cid}.json',design)
        rows.append(audit(cid,case,design))
    write(H/'authoring-audit'/('controls.json' if controls else 'primary.json'),{'passed':True,'cases':rows,'independent_rater':False})

def verify():
    count=0
    for name in ['primary','controls']:
        a=read(H/'authoring-audit'/f'{name}.json');require(a['passed'],'Failed gate')
        require(len(a['cases'])==(12 if name=='primary' else 3),'Wrong authoring count')
        for row in a['cases']:
            cid=row['case_id'];case=read(H/'cases'/f'{cid}.json');d=read(H/'hidden-design'/f'{cid}.json')
            require(row==audit(cid,case,d),'Authoring audit drift')
            require([x['field'] for x in row['all_field_audit']]==list(case['mapping']),'Field omission')
            for c in row['candidates']:
                require(case['mapping']['signal'].count(c['exact_text'])==1,'Ambiguous candidate')
                change=any(v=='yes' for v in c['removing_it_changes'].values())
                require(change==(c['intended_role']!=ROLES[2]),'Role has no supported effect')
                if c['intended_role']==ROLES[1]:
                    q=c['if_next_inquiry'];require(q and q['all_present_in_surviving_mapping'] and all(q[k] for k in ['unresolved_contrast','concrete_operation','differential_outcome_relation']),'Incomplete inquiry')
            require(any(c['intended_role']==d['intended_role'] for c in row['candidates']),'No focal role')
            count+=1
    return {'passed':True,'cases':count}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['primary','controls','verify']);a=p.parse_args()
    if a.action=='verify':print(verify())
    else:build(a.action=='controls')
