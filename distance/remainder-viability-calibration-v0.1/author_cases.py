"""Operator-authored H.2 drafts. Never included in provider context."""
import json
import secrets
import subprocess
from pathlib import Path

H = Path(__file__).resolve().parent

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as out:
        json.dump(value, out, indent=2, ensure_ascii=False)
        out.write('\n')

# Each pair changes the evidence licensing the remainder, never focal ownership.
# The first inference is the intended unsupported span; the second is a candidate
# remainder. Audits must also inspect all non-inference fields for direct entailments.
PAIRS = {
 'ach': {
  'state': 'Award P-17 is examined under three hypotheses: altered recorded scores, bidder-specific specification drafting, and an ordinary award without either practice. The dossier contains evaluation sheets, drafting records and an indexed chronology. The inquiry concerns only this award.',
  'operation': 'List the three hypotheses. Enter each dossier item in an evidence-by-hypothesis table, check independence and rate inconsistency. Recheck the comparison after removal of disputed items. Preserve the item identifiers and locations in the dossier.',
  'reduced': {
   'signal': 'Independently retained evaluation sheets agree with the announced scores, including the retained scoring history. No post-evaluation change appears in either independent copy. Dated drafting records establish that the examined specification was fixed before bidder identities were available. The comparison is stable after disputed items are removed.',
   'inference': [
    'The comparative record establishes that steering is the best surviving explanation of award P-17, with an ordinary unsteered award ruled out.',
    'Recorded-score alteration and bidder-specific authorship of the examined specification are weakened; obtain the unexamined contact log to investigate other steering routes.'
   ],
   'limit': 'Copies and dates are authenticated and independent. The evidence concerns the two named routes only; it does not record unexamined contacts or prove honest intent. The contact log is a named missing record, not assumed evidence.'
  },
  'core': {
   'signal': 'The table contains dossier identifiers and descriptions, but its comparison cells contain only the export symbol X. In the exported table X replaces every rating, including consistency, inconsistency and unrated entries. The source ratings and their item contents were not retained. The index still gives each dossier item a shelf location.',
   'inference': [
    'The comparative record establishes that score alteration is the best surviving explanation of award P-17, with an ordinary unsteered award ruled out.',
    'The surviving index permits retrieval by dossier identifier and shelf location; the three named hypotheses and the recorded table layout can be reported.'
   ],
   'limit': 'X has no diagnostic ordering or recoverable original value. The supplied index describes file categories, not their evidential contents. No sensitivity result, hypothesis-specific conflict or specific discriminating missing record is supplied.'
  }
 },
 'step': {
  'state': 'Process P-17 runs at the stated operating point. The tested input is a bounded increase in its intake-priority setting. The operator can apply, hold and reverse the setting while recording a time series. All stated execution conditions are satisfied.',
  'operation': 'Apply the priority step, hold it for the observation window, reverse it and repeat. Keep staffing and arrival schedule fixed. Record the output trajectory through the transient and the later window, and retain the step and reversal timestamps.',
  'reduced': {
   'signal': 'The measured output is end-to-end delay in hours. Each of three repetitions settles from five hours to three hours after the step and returns to five hours after reversal. No other input changes or disturbances occur during these observations.',
   'inference': [
    'The repeated response identifies intake scheduling as the unique internal cause of the measured end-to-end delay in P-17 at this operating point.',
    'The tested priority step reduces settled end-to-end delay by two hours at this operating point; it is a bounded candidate change for P-17.'
   ],
   'limit': 'The delay measurement is calibrated and all trajectories settle inside the window. The observations identify neither internal stages nor behavior at other operating points; they do not establish a unique cause or zero remaining delay.'
  },
  'core': {
   'signal': 'The archived trajectory is the smoothed submitted-priority register in command units. In each of three repetitions it settles two units below its initial value after the step and returns after reversal. The acquisition filter generates the transient from the submitted command before the work-item scheduler acts.',
   'inference': [
    'The repeated response establishes a two-hour reduction in end-to-end delay from the tested intake-priority change in P-17 at this operating point.',
    'The recorded timestamps and register values permit a plot of the submitted priority trajectory through the step and reversal windows of P-17.'
   ],
   'limit': 'The register records submitted input, not queue state, completion times or application to work items. No process-output channel or conversion from command units to delay is supplied. Execution of the stated input operation is already granted; the filter is part of the recorder, not P-17 processing.'
  }
 },
 'custody': {
  'state': 'Draft D-17 has identified leaves and an archive handling ledger. Its opening-section assembly is the focal textual-formation question. The records concern D-17 throughout; no second draft supplies substitute evidence.',
  'operation': 'Match identifiers at recorded transfers, inspect witnessed handling events and audit continuity between them. Separate recorded assembly events from unobserved authorial decisions. Retain the responsible handler, event time and recorded purpose.',
  'reduced': {
   'signal': 'Two reliable witnesses record the identified opening leaves being attached to D-17 on 4 June. A continuous safeguarded chain connects that packet to a witnessed binding of D-17 on 7 June. The identifiers match at each transfer and no unexplained transition occurs in that interval.',
   'inference': [
    'The continuous handling record proves that D-17 preserves its unchanged original authorial arrangement and settles the complete order of every textual revision.',
    'The witnessed opening-section attachment precedes the witnessed binding of the same D-17 packet; this constrains that portion of its assembly history.'
   ],
   'limit': 'The stated witnesses, identifiers and safeguarding are reliable. The ledger covers only these events and provides no record of earlier composition, unobserved rearrangements or authorial intention.'
  },
  'core': {
   'signal': 'After the completed D-17 packet entered a sealed archive box, reliable handlers record its shelf-to-reading-room and return transfers. The sealed-box identifiers match at every transfer. No entry describes internal leaf position, revision, attachment or binding, and all entries postdate assembly.',
   'inference': [
    'The continuous handling record proves that D-17 preserves its unchanged original authorial arrangement and settles the complete order of every textual revision.',
    'The documented sealed-box transfers account for the archive handling of the identified D-17 packet during the recorded post-assembly interval.'
   ],
   'limit': 'Packet identity is already fixed in the target question and is not disputed by the competing assembly histories. No opening, alteration or assembly event is observed during this interval. The histories differ only in pre-accession internal order, not later handling.'
  }
 },
 'delta': {
  'state': 'Deployment D-17 introduced removable changes a, b and c. Failure F is a checkout deadline failure under a frozen replay. Each test runs the specified subset in the same environment; all listed repetitions are deterministic and no test is unresolved.',
  'operation': 'Partition the deployed changes, test subsets and complements, and reduce the configuration using the recorded outcome. Finish by separately removing each retained change. Preserve the replay, subset and output for each test.',
  'reduced': {
   'signal': 'The oracle measures the defined checkout deadline failure F directly. Subset {a,b} produces F on every replay. Subsets {a} and {b} do not produce F on any replay. The same F definition and oracle apply to the full configuration and every reduction.',
   'inference': [
    'The reduction establishes that a and b are the unique underlying root cause of failure F in production and excludes all alternative causal mechanisms.',
    'Subset {a,b} is sufficient and 1-minimal for reproducing F under the frozen replay: removal of either retained change eliminates that defined failure.'
   ],
   'limit': 'The oracle distinguishes the defined F from other failures. No claim about globally smallest cardinality, other workloads or unique internal causes follows from single-removal minimality.'
  },
  'core': {
   'signal': 'The retained output is a generic nonzero process-exit flag. Subset {a,b} produces that flag on every replay; {a} and {b} do not. The exit flag pools checkout deadline failures with configuration rejection and early harness termination. Failure-specific traces were not retained.',
   'inference': [
    'The reduction establishes that every nonzero exit is the defined failure F itself and therefore that a and b are its unique underlying root cause.',
    'Subset {a,b} is 1-minimal for producing the recorded nonzero-exit flag under the replay: removing either change eliminates that flag.'
   ],
   'limit': 'A checkout deadline failure can return a handled response with zero process exit; a nonzero exit can occur before checkout runs. Thus both flag values occur with or without F. No target-F trace or result is recorded for any reduced subset; the flag is not a timing bound.'
  }
 },
 'crossdate': {
  'state': 'S is an ordered correspondence activity sequence whose chronological placement is in question. Two independently dated reference records and a copyist docket accompany S. The docket dates the physical transcription to 1912 and is independent of the pattern comparison.',
  'operation': 'Tabulate the sequence and reference entries. Compare their ordered high/low patterns at candidate offsets, inspect overlap and check independent anchors. Record dated documentary facts separately from inferred pattern alignment.',
  'reduced': {
   'signal': 'S positions 4 through 11 share eight consecutive annual influences with both independent references. Their distinctive high/low sequence matches reference years 1901 through 1908 at one local offset; adjacent shifts fail in both records. Independent anchors confirm the endpoints. Outside that segment no overlap has been established.',
   'inference': [
    'The observed correspondence fixes a unique global chronology for every position of S, including all entries outside the observed overlap, without remaining alternatives.',
    'The independent overlapping pattern supports placing S positions 4 through 11 at 1901 through 1908; the rest of S is not dated by this alignment.'
   ],
   'limit': 'Ordered annual increments, shared influence and reference dates hold for the stated overlap. The 1912 docket dates copying, not each represented event. Unobserved portions may contain gaps or duplicated increments.'
  },
  'core': {
   'signal': 'The pattern table lists only separate counts of high and low entries for S and each reference; the export discarded order and position. No overlap window or shared-influence relation is recorded. The copyist docket reads 1912. The references carry dates, but no S entry is linked to one of them.',
   'inference': [
    'The observed correspondence fixes a unique global chronology for every position of S, aligning all its entries with the dated references without remaining alternatives.',
    'The independent docket places the physical transcription of S in 1912; the reference dates and separate high/low counts can be listed alongside it.'
   ],
   'limit': 'The counts cannot reconstruct ordered patterns or positional overlap. The docket is an ordinary documentary date, not an alignment anchor for an identified S increment. No discriminating offset, overlap-derived exclusion or candidate shift is supplied.'
  }
 },
 'diagnosis': {
  'state': 'Failure pattern F-17 is repeated checkout latency after deployment. The specified differential contains lock contention and connection-pool exhaustion. The same focal service, replay and two mechanisms are used throughout the inquiry.',
  'operation': 'List the two mechanisms, inspect the recorded response to a controlled test and compare the implications for each mechanism. Revise relative plausibility only from a discriminating observation. Preserve the response record and test definition.',
  'reduced': {
   'signal': 'Under the fixed replay, enlarging the connection pool leaves latency unchanged while lock-wait traces remain elevated. The supplied validated test predicts a latency decrease under isolated pool exhaustion but no decrease under isolated lock contention. The capacity step is applied successfully and response sensitivity is adequate.',
   'inference': [
    'The recorded response proves that lock contention is certainly the sole cause of F-17, excluding every co-occurring or unlisted mechanism without further inquiry.',
    'Within the specified differential the response favors lock contention over isolated pool exhaustion; inspect lock ownership and hold times next.'
   ],
   'limit': 'The stated test predictions, execution and observations are reliable. The comparison is relative to these two isolated mechanisms; co-occurrence and unlisted mechanisms have not been excluded.'
  },
  'core': {
   'signal': 'Under the fixed replay, the supplied test produces response code R on three repetitions. The retained definition says only that R is a completed-test code. It contains neither a latency result nor a mechanism-dependent prediction, sensitivity value or diagnostic interpretation.',
   'inference': [
    'The recorded response proves that lock contention is certainly the sole cause of F-17, because the completed-test code exclusively identifies that mechanism.',
    'The run ledger records three completed tests for F-17 and preserves their response code R together with the names of the two specified mechanisms.'
   ],
   'limit': 'Completion certifies execution, not a diagnostic outcome. No supplied relation assigns R different or equal likelihoods under the two mechanisms. The retained test definition specifies neither the measured quantity nor the predictions for either mechanism.'
  }
 }
}

def main():
    targets = json.loads((H/'targets.json').read_text())
    checkpoint = subprocess.check_output(['git','log','-1','--format=%H','--',str(H/'targets.json')],text=True).strip()
    rows = []
    for target in targets:
        key = target['mechanism_key']
        pair = PAIRS[key]
        ids = []
        for role in ['reduced','core']:
            spec = pair[role]
            cid = 'H2-' + secrets.token_hex(6)
            ids.append(cid)
            case = {'source': target['source'], 'target': target['target'], 'mapping': {
                'state': pair['state'], 'operation': pair['operation'],
                'signal': spec['signal'], 'inference': '\n'.join(spec['inference']), 'limit': spec['limit']}}
            write(H/'authoring-attempts'/f'{cid}.json',case)
            defect = spec['inference'][0]
            write(H/'hidden-design'/f'{cid}.json',{
                'case_id':cid,'mechanism_key':key,'pair_role':role,'is_control':False,
                'focal_object':target['focal_object'],'target_checkpoint':checkpoint,
                'hypothesis':'KEEP_WITH_REDUCED_SCOPE' if role=='reduced' else 'CORE_INVALID',
                'intended_deletion':{'source_field':'mapping.inference','start':0,'end':len(defect),'exact_text':defect},
                'claim_graph_hypothesis':{'nodes':['advertised_contribution','residual_claim'], 'edges':[]},
                'graph_interpretation':'Diagnostic only: assess direct entailments independently of the two explicit inference sentences.'})
        rows.append({'mechanism_key':key,'case_ids':ids,'target_checkpoint':checkpoint})
    write(H/'hidden-design/pairs.json',rows)

if __name__ == '__main__':
    main()
