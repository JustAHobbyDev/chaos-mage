"""Deterministic finite-world replay. No provider results are read here."""
import copy
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

class Facts:
    def __init__(self, values):self.values=values;self.used=set()
    def __getitem__(self,key):self.used.add(key);return copy.deepcopy(self.values[key])

def derive(row):
    tid,key,mid=row['target_id'],row['key'],row['mapping_id']
    world=read(HERE/'worlds'/f'{tid}.json'); common=read(HERE/'common-states'/f'{tid}.json')
    before=copy.deepcopy(world);f=Facts(world['facts']);steps=[];used={k:0 for k in common['investigation_budget']['resource_ledger']}
    def step(phase, action, parameters, signal, **cost):
        assert action in common['shared_state']['available_affordances'],action
        for k,v in cost.items():used[k]+=v
        steps.append({'phase':phase,'affordance':action,'parameters':parameters,'resulting_signal':signal,'resource_use':cost})
    if tid=='T01':
        def trial(route,config='new',load='low',phase='primary'):
            latency=sum(f['base_delay_ms'][n]+(f['new_increment_ms'][n] if config=='new' else 0) for n in f['route_membership'][route])
            latency+=(f['high_load_endpoint_increment_ms'] if load=='high' else 0)+f['measurement_error_ms']
            step(phase,'run endpoint replay(route, configuration, load)',{'route':route,'configuration':config,'load':load},{'endpoint_latency_ms':latency},endpoint_trials=1,maximum_replay_slots=1)
            return latency
        if key=='diagnosis':
            for load in ('low','high'):
                for config in ('old','new'):trial('r1',config,load)
            for config in ('old','new'):trial('r2',config,phase='followup')
        elif key=='matrix':
            for route in ('r1','r2'):
                for config in ('old','new'):trial(route,config)
            values=[s['resulting_signal']['endpoint_latency_ms'] for s in steps]
            step('primary','compare hypotheses against supplied records',{'evidence':'live aggregate plus both controlled contrasts'},
                 {'r1_change_ms':values[1]-values[0],'r2_change_ms':values[3]-values[2],
                  'load_only':'inconsistent with fixed-load differences','A_confined':'inconsistent with unequal differences on two A-containing routes','B_containing_dependency':'not eliminated, but a B-only effect does not explain r2'},analysis_passes=1)
            step('followup','compare hypotheses against supplied records',{'omit':'confounded live aggregate'},
                 {'controlled_contradictions_unchanged':True,'unresolved':'B-associated explanation needs another contribution for r2; missing hypotheses remain'},analysis_passes=1)
        else:
            differences={}
            for route in ('r1','r2','r3'):
                old=trial(route,'old');new=trial(route);differences[route]=new-old
            step('primary','fit candidate additive delay maps',{'constraints':differences},
                 {'zero_map_residual_ms':differences,'equations':['dA+dB+dD=20','dA+dC+dD=2','dB+dC=18'],
                  'compatible_family':'dB=18, dC=0, dA+dD=2; A and D not separated',
                  'held_out_prediction':'r4 difference = 18+dA; not a unique number yet'},analysis_passes=1)
            old=trial('r4','old',phase='followup');new=trial('r4',phase='followup')
            step('followup','fit candidate additive delay maps',{'held_out_r4_difference_ms':new-old},
                 {'fit_increment_ms':{'A':new-old-18,'B':18,'C':0,'D':20-(new-old)},'residuals_ms':{'r1':0,'r2':0,'r3':0,'r4':0},
                  'limit':'Exact fit in this synthetic additive replay; no code-level or live-world attribution.'},analysis_passes=1)
    elif tid=='T02':
        records=f['records']
        if key=='whole':
            identity=f['document_identity']
            signal={'BD_possession_days':[r['day'] for r in records if r['document'] in ('BD',identity['BD'])],
                    'O1_edit_and_publication_days':[r['day'] for r in records if r['document']=='O1']}
            action='track whole-document custody'
        else:
            signal={'K_occurrences':[{'record':r['id'],'day':r['day'],'document':r['document']} for r in records if r['clause']=='K'],
                    'independent_receipt':records[1]};action='track clause-level copying'
        step('primary',action,{'record_ids':[r['id'] for r in records]},signal,record_accesses=6,analysis_passes=1,work_minutes=45)
        step('followup','cross-check source independence',{'compare_records':['p2','p5','p6']},
             {'generic_policy_wording':records[4]['text'],'wording_authorship':records[5]['text'],'unresolved':f['unknowns']},record_accesses=3,analysis_passes=1,work_minutes=30)
    elif tid=='T03':
        records=f['records']
        if key=='custody':
            step('primary','cross-check supplied custody links',{'leaves':['A','B','C']},{'custody':records['custody'],'relative_join':records['features'][0]},record_accesses=4,analysis_passes=1,work_minutes=45)
            step('followup','cross-check supplied custody links',{'check':'composition versus possession'},
                 {'revision_before_day':12,'revision_relative_to_B':'not determined','basis':records['features'][1]},record_accesses=2,analysis_passes=1,work_minutes=20)
        elif key=='assembly':
            matrix={'H1':{'join':'consistent','quote':'consistent','witness':'consistent','paper':'uncertain'},
                    'H2':{'join':'consistent','quote':'consistent','witness':'consistent','paper':'uncertain'},
                    'H3':{'join':'inconsistent','quote':'consistent','witness':'consistent','paper':'uncertain'}}
            assert 'B attached before C' in records['features'][0]['observation']
            step('primary','compare every feature against hypotheses',{'hypotheses':records['hypotheses']},{'matrix':matrix},record_accesses=7,analysis_passes=1,work_minutes=60)
            step('followup','remove disputed dating and repeat comparison',{'omit':'paper'},
                 {'matrix':{h:{k:v for k,v in cells.items() if k!='paper'} for h,cells in matrix.items()},'remaining':['H1','H2']},record_accesses=3,analysis_passes=1,work_minutes=30)
        else:
            patch=f['patch'];controls=f['controls']
            step('primary','probe erased patch and controls',{'patch':'under R'},
                 {'localized_response':patch['responsive'],'positive_control':controls['positive'],'negative_control':controls['negative']},physical_assays=3,analysis_passes=1,work_minutes=60)
            if patch['responsive']:
                step('followup','collate responsive undertext with witness Q',{'comparison':'Q and characterized cross-reactants'},
                     {'identified_reading':patch['reading'],'below_reading':patch['below'],'dated_bridge':[records['features'][1],records['features'][2]],
                      'unresolved':'The local Q-before-R sequence does not establish revision relative to attaching B.'},physical_assays=1,record_accesses=2,analysis_passes=1,work_minutes=30)
    elif tid=='T04':
        def ticket(route,demand='low',phase='primary',staff=False):
            waits=f['new_wait_hours'];nodes=f['routes'][route]
            value=sum(waits[n] for n in nodes)+(f['busy_intake_hours'] if demand=='busy' else 0)
            if staff and 'B' in nodes:value-=f['test_staffing_B_reduction_hours']
            action='compare fixed staffing intervention in testbed' if staff else ('repeat comparable route observations' if key=='monitor' else 'send controlled tickets along overlapping paths')
            step(phase,action,{'route':route,'demand':demand,'staffing_B_intervention':staff},{'wait_hours':value},ticket_trials=1,maximum_slots=1)
            return value
        if key=='monitor':
            for demand in ('low','busy','low','busy'):ticket('ab',demand)
            for _ in range(2):ticket('ab',phase='followup')
        else:
            observations={route:[ticket(route) for _ in range(2)] for route in ('ab','ac','bc')}
            ab,ac,bc=[observations[x][0] for x in ('ab','ac','bc')]
            fit={'A':(ab+ac-bc)/2,'B':(ab+bc-ac)/2,'C':(ac+bc-ab)/2}
            step('primary','fit delay maps',{'initial_candidate':'zero internal waits','observations':observations},
                 {'initial_residual_hours':{'ab':ab,'ac':ac,'bc':bc},'fitted_wait_hours':fit,'final_residual_hours':[0,0,0]},analysis_passes=1)
            for _ in range(2):ticket('ab',phase='followup',staff=True)
    elif tid=='T05':
        interaction=set(f['failure_interaction']); f['predicate']
        def test(rules,phase='primary',revision=None):
            failure=interaction<=set(rules)
            step(phase,'test any archived revision' if revision is not None else 'test any rule subset',
                 {'rules':sorted(rules),'revision':revision},{'activation':'fail' if failure else 'pass'},replay_trials=1,maximum_slots=1)
            return failure
        current=f['rule_names']
        if key=='diagnosis':
            for remove in ('A','B','D'):test([x for x in current if x!=remove])
            for rule in ('B','D'):test([rule],'followup')
        elif key=='bisection':
            revisions=f['revisions'];lo,hi=0,7
            while hi-lo>1:
                midpoint=(lo+hi)//2
                if test(revisions[str(midpoint)],revision=midpoint):hi=midpoint
                else:lo=midpoint
            for i in (lo,hi):test(revisions[str(i)],'followup',i)
            step('followup','inspect existing traces and revision manifests',{'boundary':[lo,hi]},
                 {'added_rules':sorted(set(revisions[str(hi)])-set(revisions[str(lo)])),'limit':'Revision association only.'},analysis_passes=1)
        else:
            items=current[:];n=2
            # Reserve four trials for the explicit final-set/deletion checks.
            while len(items)>=2 and used['replay_trials']<16:
                parts=[items[i*len(items)//n:(i+1)*len(items)//n] for i in range(n)]
                reduced=False
                candidates=parts+[[x for x in items if x not in part] for part in parts]
                for subset in candidates:
                    if used['replay_trials']>=16:break
                    if test(subset):items=subset;n=max(n-1,2);reduced=True;break
                if not reduced:
                    if n==len(items):break
                    n=min(2*n,len(items))
            tests=[items]+[[x for x in items if x!=removed] for removed in items]
            checked=[]
            for subset in tests:
                if used['replay_trials']>=20:break
                checked.append({'rules':subset,'failure':test(subset,'followup')})
            step('followup','partition rules or revisions',{'final_set':items},
                 {'checked':checked,'all_final_checks_completed':len(checked)==len(tests),
                  'limit':'Only tested permitted reductions support minimality; no unique mechanism or population necessity.'},analysis_passes=1)
    elif tid=='T06':
        records=f['records'];calendar=records['calendar'];letters=records['letter_sequence']
        if key=='custody':
            dates={r['letter']:r['dispatch_week'] for r in records['receipts']}
            step('primary','cross-check custody and dispatch records',{'records':'all receipts and custody links'},
                 {'dispatch_anchors':dates,'custody':records['custody']},record_accesses=5,analysis_passes=1,work_minutes=45)
            event=next(x['event'] for x in letters if x['letter']=='L2')
            step('followup','check independent anchors',{'letter':'L2','contemporaneous_event':event},
                 {'compatible_dispatch_weeks':[int(k) for k,v in calendar.items() if v==event],'composition':'unknown'},record_accesses=8,analysis_passes=1,work_minutes=30)
        else:
            options=[[int(k) for k,v in calendar.items() if v==r['event']] for r in letters]
            alignments=[list(p) for p in itertools.product(*options) if list(p)==sorted(set(p))]
            step('primary','align ordered event patterns to dated calendar',{'letter_order':[r['letter'] for r in letters]},
                 {'compatible_calendar_alignments':alignments},record_accesses=11,analysis_passes=1,work_minutes=55)
            anchors={r['letter']:r['dispatch_week'] for r in records['receipts']}
            retained=[p for p in alignments if all(p[i]==anchors[r['letter']] for i,r in enumerate(letters) if r['letter'] in anchors)]
            step('followup','check independent anchors',{'receipt_anchors':anchors},
                 {'retained_alignments':retained,'omitted_weeks':sorted(set(range(min(retained[0]),max(retained[0])+1))-set(retained[0])) if len(retained)==1 else [],'composition':'unknown'},record_accesses=3,analysis_passes=1,work_minutes=25)
    elif tid=='T07':
        if key=='corroboration':
            records=f['records']
            step('primary','cross-check supplied logs and receipts',{'records':[r['id'] for r in records]},
                 {'s2_independent_sources':[records[0],records[2]],'s4_independent_sources':[records[3],records[4]],'successful_schedules':[records[5],records[6]]},record_accesses=7,analysis_passes=1)
            step('followup','audit source dependence',{'copied_record':'l2'},
                 {'l2_additional_independent_support':False,'remedy':'No intervention outcome is present in these records.'},record_accesses=2,analysis_passes=1)
        else:
            f['publication_rule']
            def trial(schedule,enabled,phase):
                fail=schedule in f['mirror_failure_schedules'] or enabled and schedule in f['signer_failure_schedules']
                step(phase,'restore signing and repeat' if phase=='followup' else 'replay schedules with signing enabled or bypassed',
                     {'schedule':schedule,'signing_enabled':enabled},{'publication':'failure' if fail else 'success'},replay_trials=1,maximum_slots=1)
            for i,s in enumerate(('s1','s2','s3','s4')):
                for enabled in ((True,False) if i%2==0 else (False,True)):trial(s,enabled,'primary')
            for s in ('s1','s2','s3','s4'):trial(s,True,'followup')
    elif tid=='T08':
        input_name={'monitor':'hold','narrow_step':'routing','broad_step':'exposure'}[key]
        error,queue=f[input_name+'_error'],f[input_name+'_queue']
        ce,cq=f['control_error'],f['control_queue'];f['response_model']
        if input_name!='hold':
            step('primary','step routing fraction' if input_name=='routing' else 'step exposure',{'from':0,'to':1},{'step_applied':True},input_steps=1)
        for i in range(6):
            step('primary' if i<4 else 'followup','repeat matched measurements while holding settings' if key=='monitor' else 'measure both channels and controls',{'hour':i+1},
                 {'treated_error_percent':error[i],'control_error_percent':ce[i],'treated_queue':queue[i],'control_queue':cq[i]},time_samples=1,horizon_hours=1)
        if key!='monitor':
            channels={'queue':queue} if key=='narrow_step' else {'error':error,'queue':queue}
            summary={name:{'peak':max(series),'first_peak_hour':series.index(max(series))+1,'last_two':series[-2:],
                           'equilibrium':'not established beyond six hours'} for name,series in channels.items()}
            step('followup','compare response delay peak and persistence',{'analyzed_channels':list(channels)},summary,analysis_passes=2)
    else:raise ValueError(tid)
    # Each executed procedure phase includes one bounded interpretation pass.
    phase_count=len({s['phase'] for s in steps})
    extra=phase_count-used['analysis_passes']
    if extra:
        steps[-1]['resource_use']['analysis_passes']=steps[-1]['resource_use'].get('analysis_passes',0)+extra
        used['analysis_passes']+=extra
    assert world==before,'World mutation'
    assert all(0<=v<=common['investigation_budget']['resource_ledger'][k] for k,v in used.items()),(tid,key,used)
    return {'mapping_id':mid,'target_id':tid,'world_id':world['world_id'],'world_sha256':sha(HERE/'worlds'/f'{tid}.json'),
            'common_state_sha256':sha(HERE/'common-states'/f'{tid}.json'),'mapping_sha256':sha(HERE/'mappings'/f'{mid}.json'),
            'operation_performed':{'recipe':key,'steps':steps},'world_facts_used':sorted(f.used),
            'resulting_signal':[s['resulting_signal'] for s in steps],
            'derivation':{'engine_sha256':sha(Path(__file__)),'method':'Deterministic replay of the declared operation using only the identified frozen facts; inspect this source for arithmetic and qualitative record transforms.'},
            'resource_use':used,'limits':read(HERE/'mappings'/f'{mid}.json')['mapping']['limit']}

def public_outcome(value):
    return {'operations_and_observations':value['operation_performed']['steps'],'resource_use':value['resource_use'],
            'limits':value['limits'],'status':'Simulated realized observations in the common authored world; no omniscient facts supplied.'}

def main():
    for row in read(HERE/'operator-manifest.json')['mappings']:
        value=derive(row)
        with (HERE/'outcomes'/f'{row["mapping_id"]}.json').open('x') as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')

if __name__=='__main__':main()
