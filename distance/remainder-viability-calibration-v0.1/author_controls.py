"""Four boundary controls, authored before claim inventory/measurement."""
import secrets
from common import H, read, write, span, git

def main():
    targets={x['mechanism_key']:x for x in read(H/'targets.json')}
    pairs={x['mechanism_key']:x for x in read(H/'hidden-design/pairs.json')}
    controls=[]
    for letter,key,hypothesis,reason in [
        ('A','ach','KEEP_WITH_REDUCED_SCOPE','tiny_viable_remainder'),
        ('B','crossdate','CORE_INVALID','generic_remainder'),
        ('C','custody','CORE_INVALID','target_payoff_loss'),
        ('D','diagnosis','UNCERTAIN_LOAD_BEARING','uncertain')]:
        t=targets[key];cid='H2-'+secrets.token_hex(6)
        case={'source':t['source'],'target':t['target'],'mapping':{}}
        if letter=='A':
            case['mapping']={
                'state':'Award P-17 is investigated for steering. The advertised analysis covers scoring, specification drafting, contacts and intent; the supplied evidential fragment concerns one score entry only.',
                'operation':'List score alteration and unchanged scoring as competing explanations for the examined entry. Compare the signed original and the independently retained contemporaneous duplicate. Keep other steering routes separate.',
                'signal':'Both authenticated independent copies contain the same examined score, and neither contains an intervening alteration. No other scores, drafting records, contact records or intent evidence is supplied.',
                'inference':'The comparison establishes that every score used for award P-17 was free of manipulation throughout the full evaluation.\nThe comparison establishes that all specifications for award P-17 were drafted without bidder-specific influence.\nThe comparison establishes that every private contact concerning award P-17 was lawful and unrelated to steering.\nThe comparison establishes that all participants in award P-17 acted with impartial intent throughout the process.\nAlteration of the one examined score is weakened.',
                'limit':'The stated independence and authentication hold for this score entry. The fragment contains no evidence about other entries, specifications, contacts or intentions; matching copies do not certify every stage of the award.'}
            dimensions=['YES']*4
            why='One comparative elimination constraint changes the steering inquiry despite loss of four broad advertised contributions.'
        elif letter=='B':
            case=read(H/'cases'/f'{pairs[key]["case_ids"][1]}.json')
            case['mapping']['operation']+='\nTranscribe the docket date in a catalog entry. Preserve the document identifier and transcription date in separate columns. Inventory the envelopes and record visible postmarks without attributing them to an unlinked letter. Separate dates of copying from dates mentioned inside a text. Maintain a list of undated entries. Store digital images in sequence order with stable filenames. Note missing pages in the catalog. Retain alternative catalog arrangements. Record which facts come from the docket and which from a reference. Keep a change history for the catalog. Provide the reader with a legible chronological index of the dated reference documents.'
            dimensions=['YES','NO','YES','YES']
            why='The docket-based copying date is useful ordinary archival chronology. Many coherent catalog tasks do not restore ordered overlap or an offset inference.'
        elif letter=='C':
            case=read(H/'cases'/f'{pairs[key]["case_ids"][1]}.json')
            case['mapping']['signal']+=' Independent signatures and intact seals corroborate each transfer; the packet is the same packet throughout the three-day archive-loan interval.'
            dimensions=['YES','YES','NO','NO']
            why='Actual custody continuity survives, but the exact target concerns pre-accession assembly order; that identity is already fixed and no history is discriminated.'
        else:
            case['mapping']={
                'state':'Failure pattern F-17 is checkout latency in the focal service. The specified differential is lock contention versus connection-pool exhaustion. A test trace from segment Q of that service is supplied. The segment-to-failing-request association is absent from the supplied routing record.',
                'operation':'Compare the response of segment Q under the two specified mechanisms using the validated test predictions. Apply a controlled capacity increase under the fixed replay and record response and lock waits. Preserve the segment identifier.',
                'signal':'The capacity increase leaves Q latency unchanged while Q lock waits remain elevated. The validated predictions give a decrease for isolated pool exhaustion and no decrease for isolated lock contention. Execution and sensitivity checks pass. The trace contains no failing-request identifier linking Q to F-17.',
                'inference':'The recorded test establishes that lock contention is the sole cause of every occurrence of F-17 throughout the service, with no other contributing mechanism.\nFor segment Q, the response favors lock contention over isolated pool exhaustion and supports inspecting Q lock ownership and hold times.',
                'limit':'Test interpretation within Q is established; only Q membership in the F-17 request path is unspecified. If Q is on that path its diagnostic priority bears on the target; otherwise it concerns another segment activity. No routing fact resolves that single boundary. The observations cannot exclude co-occurrence or unlisted mechanisms.'}
            dimensions=['YES','YES','YES','UNCERTAIN']
            why='The source comparison and local inquiry are warranted. The one missing routing association determines whether they bear on the exact failure target; do not infer either membership or exclusion.'
        lines=case['mapping']['inference'].split('\n')
        deletions=[span(case,'inference',x) for x in lines[:-1]]
        survivor=lines[-1]
        candidate={'remainder_id':'R1','inference':survivor,'source_spans':[span(case,'inference',survivor),span(case,'signal',case['mapping']['signal'])],**dict(zip(['warranted','source_derived','material','target_relevant'],dimensions)),'rationale':why}
        write(H/'cases'/f'{cid}.json',case)
        write(H/'hidden-design'/f'{cid}.json',{'case_id':cid,'is_control':True,'control':letter,'mechanism_key':key,'hypothesis':hypothesis,'control_purpose':reason,'focal_object':t['focal_object'],'target_checkpoint':'928984a28' if False else git('log','-1','--format=%H','--',str(H/'targets.json')).decode().strip(),'intended_deletions':deletions})
        ablated=dict(case['mapping'])
        for deletion in reversed(deletions):
            ablated['inference']=ablated['inference'][:deletion['start']]+'[DELETED INTENDED CLAIM]'+ablated['inference'][deletion['end']:]
        controls.append({'case_id':cid,'control':letter,'hypothesis':hypothesis,'ablated_mapping':ablated,'candidate_remainders':[candidate],
            'search_record':'Inspected every mapping field. For B/C the primary core audit applies as well; added catalog procedures/identity corroboration add no alignment/assembly-order relation. For A no evidence beyond one entry is supplied. For D only segment membership is unresolved.',
            'primary_audit_reference':pairs[key]['case_ids'][1] if letter in ['B','C'] else None,
            'all_fields_searched':list(case['mapping']), 'provider_calls':0})
    write(H/'authoring-audit/controls.json',controls)

if __name__=='__main__':main()
