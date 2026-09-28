"""One-shot world authoring, run before any mapping is authored. Exclusive writes."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

def dump(path, obj):
    with path.open('x') as f:
        f.write(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def world(tid, facts, artifacts, observations, uncertainties, affordances, constraints, ledger, hidden):
    baseline_bytes = (ROOT/'distance/comparative-displacement-v0.3/baselines'/f'{tid}.json').read_bytes()
    with (HERE/'baselines'/f'{tid}.json').open('xb') as f:
        f.write(baseline_bytes)
    baseline = json.loads(baseline_bytes)
    common = {
        'target': {'domain': baseline['target_domain'], 'question': baseline['target_task']},
        'native_baseline': baseline,
        'shared_state': {
            'facts': ['Authored synthetic environment; no real persons or organizations.'] + facts,
            'artifacts': artifacts,
            'initial_observations': observations,
            'known_uncertainties': uncertainties,
            'available_affordances': affordances,
            'constraints': constraints,
        },
        'investigation_budget': {'primary_operations': 1, 'immediate_followups': 1,
                                 'new_external_sources': 0, 'resource_ledger': ledger,
                                 'other_constraints': ['Both branches start from an independent reset of this same world.',
                                   'A procedure may contain elementary trials, but all consume the common ledger.',
                                   'Unused resources are allowed; proposed later inquiries are not performed within this budget.']},
    }
    dump(HERE/'common-states'/f'{tid}.json', common)
    dump(HERE/'worlds'/f'{tid}.json', {
        'world_id': 'W-'+tid, 'target_id': tid,
        'observable_start': common,
        'facts': hidden,
        'mutation_policy': 'Immutable world. Interventions select specified counterfactual response functions; neither branch changes the other.',
        'authorship_limit': 'Synthetic stipulations support internal consistency, not empirical validation or practitioner consensus.'})

def main():
    world('T01', [
        'Configurations old and new differ only in the deployed cache-policy flag. Live traffic volume also changed, so the live association alone is confounded.',
        'An isolated resettable replay can cross either configuration with low or high load on any listed route. A route trial returns endpoint latency in ms.',
        'Independent calibration in this replay established an additive service-delay model at fixed load, endpoint measurement error bounded by 1 ms, and stable route membership. Calibration does not reveal current component delays.',
        'Candidate explanations are a deployment effect on the B-containing dependency, a deployment effect confined to A, and load-only variation. Alternatives may be incomplete.'
    ], {'routes': {'r1':['A','B','D'], 'r2':['A','C','D'], 'r3':['B','C'], 'r4':['A','B','C']},
        'deployment_log': ['old then new cache-policy flag; no other configuration change'],
        'live_summary': {'old_median_ms':40, 'new_median_ms':70, 'old_load':'low', 'new_load':'high'}},
        ['The aggregate live route-r1 latency rose by 30 ms; attribution and component contributions are unresolved.'],
        ['No component-level timings are available. Replay effects need not generalize to every live workload.'],
        ['inspect supplied logs', 'compare hypotheses against supplied records', 'run endpoint replay(route, configuration, load)', 'fit candidate additive delay maps', 'test a held-out route'],
        ['No internal service probes or live deployment changes.', 'All analyses use the same supplied route catalog.'],
        {'endpoint_trials':10, 'analysis_passes':2, 'maximum_replay_slots':10},
        {'base_delay_ms':{'A':10,'B':20,'C':30,'D':10}, 'new_increment_ms':{'A':0,'B':18,'C':0,'D':2},
         'high_load_endpoint_increment_ms':10, 'measurement_error_ms':0,
         'route_membership':{'r1':['A','B','D'],'r2':['A','C','D'],'r3':['B','C'],'r4':['A','B','C']}})

    records = [
        {'id':'p1','day':1,'origin':'bidder draft','document':'BD','clause':'K','text':'three regional depots','recipient':'bidder'},
        {'id':'p2','day':3,'origin':'independent mail receipt','document':'attachment hash BD','clause':'unknown','text':'attachment received','recipient':'official'},
        {'id':'p3','day':4,'origin':'official editing log','document':'O1','clause':'K','text':'three regional depots inserted','recipient':'official'},
        {'id':'p4','day':5,'origin':'public register','document':'O1','clause':'K','text':'three regional depots','recipient':'public'},
        {'id':'p5','day':2,'origin':'older policy register','document':'P0','clause':'generic','text':'regional service capacity','recipient':'public'},
        {'id':'p6','day':4,'origin':'official memo','document':'memo','clause':'K','text':'capacity rationale; author of wording unstated','recipient':'committee'},
    ]
    world('T02', ['The full authenticated records below are available to either investigation. Mail receipt p2 was independently generated; summaries of it are not additional sources.',
                  'BD hash identifies the complete bidder draft; the exact distinctive clause K is present in BD and O1. No source establishes motive or rules out an unrecorded common origin.'],
          {'records':records}, ['The awarded bidder met clause K; competing bidders did not all meet it.'],
          ['Advance access and clause transmission can be supported without establishing intentional steering.'],
          ['inspect every supplied record', 'track whole-document custody', 'track clause-level copying', 'cross-check source independence', 'compare alternative explanations'],
          ['No new interviews, documents or external searches.'], {'record_accesses':12,'analysis_passes':2,'work_minutes':90},
          {'records':records,'document_identity':{'BD':'attachment hash BD'},'unknowns':['motive','unrecorded common source','who chose clause K']})

    manuscript = {
        'custody':[{'leaf':'A','person':'editor','day':7},{'leaf':'B','person':'editor','day':9},{'leaf':'C','person':'editor','day':9}],
        'features':[{'id':'join','observation':'A fastening through B is physically overlain by the C attachment; B attached before C.'},
                    {'id':'quote','observation':'Authenticated day-12 letter quotes replacement R on A.'},
                    {'id':'witness','observation':'Independent day-4 witness contains reading Q; it does not locate Q on A.'},
                    {'id':'paper','observation':'Paper batch suggests day 8 but this dating is disputed.'}],
        'hypotheses':{'H1':'A revised before B then C were attached','H2':'A revised after B then C were attached','H3':'C attached before B; A revision time open'},
    }
    world('T03', ['All documentary and visible material observations below are shared.',
                  'A has a bounded erased patch under R. A calibrated non-destructive optical probe responds to residual ink material; controls and known cross-reactants are characterized. It localizes responsive material, not an event or date.',
                  'If responsive material is found, a separately calibrated spectral collation can compare its legible pattern with Q or known cross-reactants. This follow-up can establish a local reading; it cannot date assembly.',
                  'The physical B-before-C join observation is reliable. Paper dating remains uncertain.'],
          manuscript, ['Ordinary inspection cannot read the erased patch. H1 and H2 both fit the currently visible observations.'],
          ['Custody does not equal composition. The relative timing of A revision and B attachment is not directly observed.'],
          ['cross-check supplied custody links', 'compare every feature against hypotheses', 'remove disputed dating and repeat comparison', 'probe erased patch and controls', 'collate responsive undertext with witness Q'],
          ['No destructive sampling or new archive sources.'], {'physical_assays':4,'record_accesses':12,'analysis_passes':2,'work_minutes':120},
          {'records':manuscript,'patch':{'responsive':True,'reading':'Q','below':'R'},
           'controls':{'positive':True,'negative':False},'assembly':{'B_before_C':True,'revision_relative_to_B':'unrecorded'}})

    world('T04', ['A resettable ticket testbed represents teams A, B and C with known overlapping routes. At fixed staffing/demand, independently checked end-to-end waits are additive within 0.2 hours.',
                  'Historical low-demand endpoint waits are listed. New-period live tickets mix ordinary and busy slots. Busy slots add a common two-hour intake wait outside these three teams.',
                  'A ticket observation returns route, demand slot and end-to-end wait; internal stage waits are unavailable. All branches can choose any route and demand slot.'],
          {'routes':{'ab':['A','B'],'ac':['A','C'],'bc':['B','C']},'historical_low_wait_hours':{'ab':7,'ac':5,'bc':8},'live_ab_hours':[11,13]},
          ['Delay increased on the main A-B route; whether the pattern persists and which internal team contributes remain open.'],
          ['The testbed is bounded; staffing remedies still require separate live assessment.'],
          ['inspect supplied histories', 'repeat comparable route observations', 'send controlled tickets along overlapping paths', 'fit delay maps', 'compare fixed staffing intervention in testbed'],
          ['No internal timestamps or live staffing change.'], {'ticket_trials':8,'analysis_passes':2,'maximum_slots':8},
          {'old_wait_hours':{'A':2,'B':5,'C':3},'new_wait_hours':{'A':2,'B':9,'C':3},'busy_intake_hours':2,
           'routes':{'ab':['A','B'],'ac':['A','C'],'bc':['B','C']},'test_staffing_B_reduction_hours':2})

    revisions = [[],['A'],['A','D'],['A','B','D'],['A','B','C','D'],['A','B','C','D','E'],['A','B','C','D','E','F'],list('ABCDEFG')]
    world('T05', ['A deterministic onboarding replay is calibrated against the fixed activation task. Each permitted rule subset is executable and resets completely; one trial returns pass/fail for activation. This is not a model of population-wide user necessity.',
                  'Eight executable revisions form a nested history. Independent certification establishes repeatability and exactly one pass-to-fail transition on this chain, without disclosing its location. Revision 0 passes; revision 7 fails.',
                  'Rules A-G are separable toggles. A is welcome copy, B an identity prerequisite, C a theme, D a navigation guard, E a tooltip, F an optional survey, G a confirmation banner.',
                  'Plausible explanations include copy confusion, either guard alone, and interactions. Existing replay traces show a guard wait but do not identify its cause.'],
          {'revisions':{str(i):v for i,v in enumerate(revisions)},'current_rules':list('ABCDEFG'),'known_endpoints':{'0':'pass','7':'fail'}},
          ['Current replay cannot reach activation; deciding which proposal parts require joint investigation remains open.'],
          ['Replay minimality, revision association and real-user necessity are different claims.'],
          ['inspect existing traces and revision manifests', 'test any rule subset', 'test any archived revision', 'partition rules or revisions', 'update competing explanations'],
          ['No new participant study; no changing the replay success criterion.'], {'replay_trials':20,'analysis_passes':2,'maximum_slots':20},
          {'revisions':{str(i):v for i,v in enumerate(revisions)},'failure_interaction':['B','D'],'rule_names':list('ABCDEFG'),
           'predicate':'fail exactly when both B and D are enabled; all other configurations pass'})

    archive = {'calendar':{'10':'fair','11':'flood','12':'election','13':'fire','14':'oath','15':'frost','16':'fair'},
               'letter_sequence':[{'letter':'L1','event':'flood'},{'letter':'L2','event':'election'},{'letter':'L3','event':'fire'},{'letter':'L4','event':'frost'}],
               'receipts':[{'letter':'L1','dispatch_week':11},{'letter':'L3','dispatch_week':13},{'letter':'L4','dispatch_week':15}],
               'custody':[{'object':'bundle','person':'recipient','week':16},{'object':'bundle','person':'archive','week':40}]}
    world('T06', ['All calendar, letters and custody records below are independently authenticated and available in full.',
                  'Each listed letter describes the event of its dispatch week; this contemporaneity link is established independently. The letter sequence preserves weekly order but can omit weeks.',
                  'Receipt weeks are direct dispatch anchors, not composition dates. The calendar and receipt series have separate origins.'],
          archive, ['The bundle is undated as a whole; L2 has no direct dispatch receipt.'],
          ['Letters may have been composed earlier; an omitted letter is not evidence no letter existed.'],
          ['cross-check custody and dispatch records', 'align ordered event patterns to dated calendar', 'identify omitted weeks', 'check independent anchors'],
          ['No new collections or documents.'], {'record_accesses':20,'analysis_passes':2,'work_minutes':90},
          {'records':archive,'dispatch_weeks':{'L1':11,'L2':12,'L3':13,'L4':15},'composition_weeks':'unknown'})

    release_records=[
        {'id':'l1','source':'signer process','schedule':'s2','observation':'signer timeout'},
        {'id':'l2','source':'summary copied from l1','schedule':'s2','observation':'signer timeout'},
        {'id':'l3','source':'independent registry receipt','schedule':'s2','observation':'publication absent'},
        {'id':'l4','source':'mirror process','schedule':'s4','observation':'mirror unavailable'},
        {'id':'l5','source':'independent registry receipt','schedule':'s4','observation':'publication absent'},
        {'id':'l6','source':'registry receipt','schedule':'s1','observation':'published'},
        {'id':'l7','source':'registry receipt','schedule':'s3','observation':'published'}]
    world('T07', ['An isolated release workflow can replay the four fixed schedules with an optional signing dependency enabled or bypassed, then restore it. Reset removes carryover; artifact contents and all other settings are fixed.',
                  'Existing authenticated logs below are accessible to both branches. l2 copies l1 and is not independent corroboration.',
                  'A trial returns publication success/failure; a remedy here is limited to this schedule set. Bypass is safe only in this isolated workflow.'],
          {'records':release_records,'schedule_set':['s1','s2','s3','s4'],'dependency_graph':['build -> signer -> registry','build -> mirror -> registry']},
          ['With signing enabled, s1/s3 published and s2/s4 did not; absent publication may have multiple causes.'],
          ['Existing associations do not prove that signing is responsible or that bypass cures all failures.'],
          ['cross-check supplied logs and receipts', 'audit source dependence', 'replay schedules with signing enabled or bypassed', 'restore signing and repeat'],
          ['No live release or new external sources.'], {'replay_trials':12,'record_accesses':14,'analysis_passes':2,'maximum_slots':12},
          {'records':release_records,'signer_failure_schedules':['s2'],'mirror_failure_schedules':['s4'],
           'publication_rule':'failure if mirror fails, or signing enabled and signer fails; otherwise success'})

    world('T08', ['Two isolated, representative rollout replicas can be reset to the same starting state. One controls cohort exposure; another controls support-routing fraction. Either is available to both branches.',
                  'A known 0-to-1 step can be applied to either input. Independent calibration establishes stable comparable controls and reliable time sampling for each channel, but does not disclose the current response trajectory.',
                  'One time sample returns treated and comparison error rates and support-queue counts. The observation horizon is six hourly samples. Holding current settings is also available.',
                  'Baseline error is 2 percent and baseline support queue is 4. A routing experiment affects the support subsystem; any inference about cohort deterioration needs the cohort channel too.'],
          {'initial_metrics':{'error_percent':2,'queue':4},'current_snapshot':{'error_percent':3,'queue':8},'channels':['cohort_error_percent','support_queue'],
           'inputs':['exposure','routing','hold'],'sample_hours':[1,2,3,4,5,6]},
          ['The current snapshot is adverse; persistence, transient shape, and the next safe observation window remain unresolved.'],
          ['Six hours cannot establish long-run equilibrium or a unique causal mechanism; replicas may not generalize.'],
          ['repeat matched measurements while holding settings', 'step exposure', 'step routing fraction', 'measure both channels and controls', 'compare response delay peak and persistence'],
          ['At most one input step in the primary procedure; no real-user rollout change.'],
          {'time_samples':6,'input_steps':1,'analysis_passes':2,'horizon_hours':6},
          {'control_error':[2,2,2,2,2,2],'control_queue':[4,4,4,4,4,4],
           'exposure_error':[3,6,5,4,4,4],'exposure_queue':[8,12,10,8,8,8],
           'routing_error':[2,2,2,2,2,2],'routing_queue':[8,12,6,4,4,4],
           'hold_error':[3,4,4,4,4,4],'hold_queue':[8,9,8,8,8,8],
           'response_model':'The listed time-series are the fixed finite-horizon potential observations for the three available inputs; no extrapolation beyond hour 6 is defined.'})

    paths=[p for folder in ('baselines','common-states','worlds') for p in (HERE/folder).glob('*.json')]
    paths += [HERE/'author_worlds.py', ROOT/'docs/PROBLEM_FRAMES-common-evidence-displacement-v0.3.md']
    dump(HERE/'worlds-freeze.json', {'starting_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
         'construction_order':'target and baseline, then world and observable state/affordances/budget, then commit; mappings and outcomes do not yet exist',
         'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}})
    tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    private=[p for p in (ROOT/'.runtime').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    dump(HERE/'preservation.json', {'starting_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
         'files':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in tracked if p},
         'private_files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in private}})

if __name__ == '__main__': main()
