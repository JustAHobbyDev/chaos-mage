"""Author new fixed mappings only after the world checkpoint exists."""
import itertools
import json
from pathlib import Path
import random
import subprocess
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ROWS = []

def add(target, key, source, state, operation, signal, inference, limit):
    ROWS.append({'target_id':target,'key':key,'source_path':'instruments/'+source+'.yaml',
                 'mapping':dict(zip(('state','operation','signal','inference','limit'),(state,operation,signal,inference,limit)))})

def main():
    sha=subprocess.check_output(['git','log','-1','--format=%H','--',str(HERE/'worlds-freeze.json')],cwd=ROOT,text=True).strip()
    assert sha and subprocess.check_output(['git','show','-s','--format=%s',sha],cwd=ROOT,text=True).strip()=='Freeze B.2 common worlds and baselines'
    add('T01','diagnosis','clinical-diagnosis--differential-diagnosis',
        'The live checkout regression admits deployment and load explanations.',
        'Compare the three stated explanations. Run r1 under old/new at low/high load, update which explanations survive; immediately follow with old/new low-load r2 to discriminate an A-confined effect from other deployment effects.',
        'Configuration and load contrasts may support, contradict or fail to distinguish candidate causes.',
        'Narrow plausible explanations for the deployment-associated regression and select a dependency for later investigation; do not claim a unique mechanism.',
        'Unlisted causes, uninformative contrasts and replay generalization limit diagnosis. Tests distinguish alternatives only to their sensitivity.')
    add('T01','matrix','intelligence-analysis--analysis-of-competing-hypotheses',
        'Three supplied explanations compete for the same checkout evidence.',
        'Build a full evidence-by-hypothesis inconsistency matrix from the supplied live records. Obtain old/new low-load r1 and r2 contrasts and compare each against every explanation. Follow up by dropping the confounded live aggregate and repeating the matrix, emphasizing surviving contradictions rather than support counts.',
        'The cross-hypothesis pattern of contradictions may remain or disappear when uncertain live evidence is removed.',
        'Weaken incompatible explanations and expose the next discriminating route or missing hypothesis, without treating a surviving explanation as proved.',
        'Missing alternatives, dependent records and subjective diagnosticity can mislead; the replay findings are bounded to the calibrated regime.')
    add('T01','inverse','seismology-geophysics--seismic-tomography',
        'Unknown service-delay changes affect travel times on overlapping checkout routes.',
        'Measure old/new low-load endpoint times on r1-r3. Predict differences from candidate service-delay maps, iteratively adjust them to reduce route residuals and retain the non-unique solution set. Follow up on held-out r4 at old/new low load, checking predicted residuals rather than choosing a preferred internal map.',
        'Measured route differences and held-out residuals constrain compatible internal delay-change combinations.',
        'Localize deployment-associated delay contributions under the shared additive replay model and direct later service inspection; this is a bounded contribution to attribution, not proof of a code mechanism.',
        'Sparse paths, non-uniqueness, model error and measurement limits remain. Do not substitute hidden component truth for measured constraints or generalize beyond replay.')
    add('T02','whole','archival-provenance-research--provenance-reconstruction',
        'Tender-document custody and copying have dated but incomplete traces.',
        'Track BD and O1 as whole documents through p1-p6, cross-check receipts, editing logs and public registration; follow up by marking missing links and comparing the older policy record without treating clause identity as document identity.',
        'Compatible or conflicting dated custody and possession links emerge at document granularity.',
        'Bound document possession before publication and identify gaps relevant to possible steering, without establishing motive or clause authorship.',
        'Incomplete transfers, common origins and mistaken document identity limit reconstruction; possession is not proof of intentional steering.')
    add('T02','clause','archival-provenance-research--provenance-reconstruction',
        'The custody and copying of distinctive clause K may differ from the histories of whole documents.',
        'Track the exact K wording as the object across p1-p6, connecting dated bidder possession, independently authenticated attachment receipt and official insertion; follow up by checking generic P0 wording and explicitly preserving missing authorship and common-origin links.',
        'Compatible or conflicting clause-transmission links identify what is actually supported beyond whole-document possession.',
        'Reconstruct a bounded pre-publication clause history bearing on steering, distinguishing transmission support from motive or final attribution.',
        'Identical wording need not establish a unique origin; missing transactions, copying and incomplete records constrain the history.')
    add('T03','custody','archival-provenance-research--provenance-reconstruction',
        'The draft leaves have partial dated custody and assembly traces.',
        'Cross-check the A/B/C custody records and physical join feature to reconstruct supported people, places and ordering links. Follow up by marking gaps between possession, attachment and composition rather than filling them from disputed paper dating.',
        'Consistent dated possession links and physical relative-order constraints may coexist with unresolved revision timing.',
        'Bound the surviving draft assembly history while preserving uncertainty about when A was revised relative to attachment.',
        'Custody does not establish composition; missing witnesses or undocumented earlier transfers remain possible.')
    add('T03','assembly','intelligence-analysis--analysis-of-competing-hypotheses',
        'Three stated revision-and-assembly sequences fit different portions of the shared manuscript evidence.',
        'Compare every supplied documentary and physical feature against H1-H3 in an explicit inconsistency matrix; emphasize diagnostic contradictions. Follow up by removing disputed paper dating and checking which exclusions survive.',
        'Cross-hypothesis consistency patterns and sensitivity to disputed dating distinguish elimination from mere best fit.',
        'Weaken contradicted formation sequences and state the unresolved assembly-versus-revision questions for subsequent inquiry.',
        'Unlisted sequences, dependent features and subjective interpretation may mislead; surviving the matrix is not proof of a chronology.')
    add('T03','probe','forensic-investigation--luminol-latent-trace-detection',
        'Ink-associated material may persist invisibly in the erased patch beneath R.',
        'Apply the independently calibrated non-destructive optical probe to the patch and positive/negative controls. If responsive material is found, use the single follow-up spectral collation to compare its reading with witness Q and known cross-reactants; otherwise report detection limits without substituting another assay.',
        'A localized probe response supports responsive residual material; the independent follow-up may or may not identify a local earlier reading.',
        'Constrain the local earlier-reading/replacement sequence only if supported by the separate collation and shared dated documentary bridge. The detection itself supports presence and location, not an event or date.',
        'Cross-reactants, degradation and detection limits restrict absence claims. A local reading does not settle complete draft assembly or whether revision preceded attachment.')
    add('T04','monitor','clinical-diagnosis--serial-monitoring',
        'Main-route approval delay may be sustained or just demand-related fluctuation.',
        'Repeat A-B endpoint waits in four comparable new-period slots, alternating low/busy demand and stratifying against the supplied historical low-demand baseline. Follow up with two further low-demand observations to check persistence; keep expected two-hour intake variation separate.',
        'The repeated stratified trajectory distinguishes a sustained main-route increase from busy-slot variation.',
        'Locate persistent delay on the A-B path and prioritize those handoffs for further bounded investigation; do not identify a unique hidden team from a route total.',
        'Mix changes, sampling and testbed generalization limit inference; repeatability does not itself localize a component.')
    add('T04','inverse','seismology-geophysics--seismic-tomography',
        'Hidden internal team waits contribute to end-to-end ticket travel on overlapping paths.',
        'Send two low-demand tickets on each of ab/ac/bc. Predict endpoint times from candidate internal wait maps and iteratively reduce residuals, checking coverage and non-uniqueness. Follow up with two low-demand ab tickets under the available bounded B-staffing intervention to compare its effect with the fitted map.',
        'Path-structured residual constraints and the bounded intervention response restrict hidden-wait explanations.',
        'Localize possible accumulation and evaluate one testbed staffing change as a bounded contribution to reducing approval delays.',
        'The additive model is calibrated only here; measurement error and live queue dynamics limit localization and remedy generalization.')
    add('T05','diagnosis','clinical-diagnosis--differential-diagnosis',
        'The fixed activation failure has copy, individual-guard and interaction explanations.',
        'Use the shared current replay and rule roles to retain competing explanations. Test current rules without A, without B and without D, comparing every result to those explanations. Follow up by testing B alone and D alone to distinguish individual-guard accounts from an interaction possibility.',
        'Discriminating replay outcomes support, contradict or leave open candidate dependency explanations.',
        'Narrow which parts plausibly obstruct activation and which interaction deserves the next inquiry, without asserting all necessary product features.',
        'Unlisted mechanisms and replay-specific sensitivity limit diagnosis; individually harmless rules may interact and do not prove population-wide necessity.')
    add('T05','reduction','software-debugging-testing--delta-debugging',
        'The current failing onboarding rule set can be partitioned and reduced under a fixed reproducible oracle.',
        'Use deterministic ddmin with alphabetic contiguous partitions: test subsets then complements, retain a failing reduction, and increase partition count if no reduction succeeds, stopping at the shared trial cap. Follow up by testing the final set and each permitted single deletion while budget remains; label untested minimality unresolved.',
        'Some reduced sets reproduce failure while others pass, defining a test-relative minimality boundary if fully checked.',
        'Identify a bounded failure-inducing interaction set and whether any tested single deletion preserves failure, directing joint feature investigation rather than independent ranking.',
        'Search order, budget and oracle scope constrain minimality; a minimal failing set is neither a unique causal mechanism nor general user necessity.')
    add('T05','bisection','software-debugging-testing--regression-bisection',
        'The certified executable revision chain brackets one reproducible activation transition.',
        'Bisect the passing-0/failing-7 revision interval using floor midpoints and discard the incompatible half after each replay. Follow up by replaying both boundary revisions and inspecting their manifest difference without testing separate causal roles for each changed rule.',
        'Each pass/fail outcome shrinks the revision interval containing the transition.',
        'Locate the first failing revision and its changed proposal parts as a bounded dependency lead, leaving interaction necessity for later testing.',
        'The monotonicity and repeatability certifications are essential; the boundary establishes revision association, not an independent feature effect or general user necessity.')
    add('T06','custody','archival-provenance-research--provenance-reconstruction',
        'The bundle and individual letters have incomplete but independently dated dispatch and custody traces.',
        'Cross-check all receipt, custody and contemporaneous event records to connect letters to dated dispatch and possession links. Follow up by reconciling L2 with its event reference and marking unsupported composition intervals.',
        'Independent compatible dates constrain dispatch order and show gaps in documented history.',
        'Establish bounded relative and calendar dispatch chronology, keeping original composition and missing transfers uncertain.',
        'Incomplete custody is not proof of continuity; dispatch is distinct from composition and records can share hidden errors.')
    add('T06','alignment','dendrochronology-paleoclimate--crossdating',
        'The ordered letter-event sequence overlaps the independently dated calendar with possible omitted weeks.',
        'Shift the event sequence against the calendar and compare distinctive multi-week patterns, allowing omitted weeks while preserving order. Retain all compatible alignments. Follow up by checking them against the independent receipt anchors and explicitly identifying gaps.',
        'Repeated event-pattern agreement across the calendar and receipt witnesses constrains offsets and missing increments.',
        'Assign bounded calendar positions to the event-linked dispatches and retain uncertainty about composition and omitted letters.',
        'Repetitive events, short overlap, wrong references or a failed contemporaneity bridge would mislead; no composition date follows merely from dispatch alignment.')
    add('T07','corroboration','intelligence-analysis--source-corroboration',
        'Reported workflow failures have sources with different access and dependence.',
        'Cross-check l1-l7 by claim, access, authenticity and independence, treating l2 as a copy of l1. Follow up by separating corroborated failure locations from unsupported signing-remedy claims and identifying missing causal evidence.',
        'Independent receipts and process records converge or conflict about specific failed dependencies.',
        'Increase support for bounded failure-location claims and specify which remedy test is still needed; do not infer that bypassing signing repairs every failure.',
        'Shared bugs, incomplete observation and dependent summaries can create false convergence; corroboration of location is not a causal remedy experiment.')
    add('T07','reversal','clinical-diagnosis--dechallenge-rechallenge',
        'Signing is present in the failing workflow and can be removed then restored without carryover in the isolated replay.',
        'Compare each fixed schedule with signing enabled and bypassed, counterbalancing trial order across schedules. Follow up by restoring signing and rerunning all four schedules, holding artifact contents and other settings fixed.',
        'Diminution and recurrence of failures, or their absence, bear on signing as a contributor; persistent failures may have other causes.',
        'Assess the bounded causal contribution of signing and the extent of bypass as a tested remedy for this schedule set.',
        'The controlled replay does not prove universal necessity or safety of a live bypass; other dependencies may sustain failures.')
    add('T08','monitor','clinical-diagnosis--serial-monitoring',
        'An adverse rollout snapshot may reflect transient variation or sustained deterioration.',
        'Hold current settings and repeat matched treated/comparison error and support-queue measurements at hours 1-4. Follow up at hours 5-6; compare trajectories with baseline and use two consecutive error measurements above 3 percent as the stated investigation alert, not as a causal proof.',
        'Persistence or reversal of matched adverse trajectories distinguishes a sustained change from an isolated snapshot.',
        'Constrain whether the segment is deteriorating and whether to investigate or pause, while leaving causal explanation open.',
        'Mix shifts, concurrent inputs and six-hour censoring limit conclusions; a monitoring threshold is not an ontological score or proof of rollout harm.')
    add('T08','narrow_step','control-systems-engineering--step-response-probing',
        'Support routing is a controllable input with a time-varying duplicate-alert queue response.',
        'Apply the calibrated routing-fraction step and record both available channels and controls at hours 1-4, characterizing the queue delay, peak and return behavior. Follow up at hours 5-6 to test persistence. Use the imported response analysis only for this support subtask, then hand its bounded result to ordinary full-segment review.',
        'The queue trajectory can reveal transient shape or persistent change at this routing operating point.',
        'Choose an appropriate support-alert observation window without concluding that the cohort as a whole is or is not deteriorating.',
        'Finite horizon, disturbances and nonlinearity limit the dynamic inference; queue behavior alone cannot settle the full rollout task.')
    add('T08','broad_step','control-systems-engineering--step-response-probing',
        'Cohort exposure is a controllable input whose time-varying segment response bears directly on rollout decisions.',
        'Apply the calibrated exposure step and record both channels and controls at hours 1-4. Characterize delay, peak, overshoot and possible later shift in errors and queue, then follow up at hours 5-6 to test persistence. Let the measured temporal response determine the next observation window and reversible exposure inquiry.',
        'The paired trajectories can reveal lagged, transient or persisting effects of this exposure step.',
        'Characterize bounded segment response for rollout observation and reversible-action choices without identifying a unique mechanism or assuming equilibrium.',
        'Six hours may not show settling; disturbances, initial state and nonlinear response limit extrapolation beyond this operating point.')

    ids=[f'M{i:03}' for i in range(1,len(ROWS)+1)]
    random.Random(20260928021).shuffle(ids)
    manifest=[]
    for row,mid in zip(ROWS,ids):
        source=yaml.safe_load((ROOT/row['source_path']).read_text())
        assert source['extraction']['status']=='accepted'
        common=json.loads((HERE/'common-states'/f'{row["target_id"]}.json').read_text())
        obj={'case_id':mid,'source':{'name':source['extraction']['name'],'practice':source['extraction']['practice'],'instrument':source['instrument']},
             'target':{**common['target'],'evidence':[json.dumps(common,ensure_ascii=False,sort_keys=True)]},'mapping':row['mapping']}
        write(HERE/'mappings'/f'{mid}.json',obj)
        manifest.append({k:row[k] for k in ('target_id','key','source_path')}|{'mapping_id':mid,'world_commit':sha})
    tags={
      'T01':['close-dominance','clear-dominance','surface-exoticness'],
      'T02':['same-source','close-dominance'],
      'T03':['local-depth-vs-task-reach','tradeoff'],
      'T04':['clear-dominance','surface-exoticness'],
      'T05':['close-dominance','clear-dominance','surface-exoticness'],
      'T06':['approximately-equal'],
      'T07':['close-dominance','approximately-equal'],
      'T08':['local-depth-vs-task-reach','same-source','clear-dominance']}
    pairs=[]
    for tid in sorted(tags):
        for a,b in itertools.combinations([x for x in manifest if x['target_id']==tid],2):
            pairs.append({'target_id':tid,'mapping_1':min(a['mapping_id'],b['mapping_id']),'mapping_2':max(a['mapping_id'],b['mapping_id']),
                          'tags':sorted(set(tags[tid]+['same-source' if a['source_path']==b['source_path'] else 'different-source'])),
                          'intent':'Coverage hypothesis only; not a reference answer.'})
    assert len(pairs)==16
    write(HERE/'operator-manifest.json',{'mappings':manifest,'pair_designs':pairs,'intent_policy':'Never exposed to judges or used as accuracy labels.'})
    write(HERE/'design.json',{'seeds':dict(zip(('identities','orientation','controls','validity','prospective','consequence'),range(20260928021,20260928027))),
          'planned_pairs':16,'planned_mappings':20,'triangle_targets':['T01','T03','T05','T08'],'orientation_controls':4,
          'attrition':'Exclude failed admission without replacement; continue if at least one pair survives.'})

def write(path,obj):
    with path.open('x') as f:f.write(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__': main()
