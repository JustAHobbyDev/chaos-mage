#!/usr/bin/env python3
"""Offline H8 inputs: exact H7 survivors, neutral projection, common schemas."""
import hashlib
import json
from pathlib import Path

H = Path(__file__).resolve().parent
R = H.parents[1]
H7 = R / 'distance/natural-admission-v0.2'
BASE = 'c62b622b69ed900b9debcc9e41e133536287be59'
SURVIVORS = ['H7-T01-1', 'H7-T03-1', 'H7-T03-2']
CATEGORIES = ['PROBLEM_REPRESENTATION_CHANGE', 'INQUIRY_CHANGE', 'PRIORITY_CHANGE',
              'ACTION_CHANGE', 'DECISION_RULE_CHANGE', 'CONSTRAINT_CHANGE']
FIELDS = {'top_uncertainties': ['uncertainty', 'why_it_matters'],
          'next_inquiries': ['inquiry', 'operation_or_observation', 'decision_relevance'],
          'priorities': ['rank', 'item', 'rationale'],
          'immediate_actions': ['action', 'rationale'],
          'decision_rules': ['condition', 'consequence', 'rationale'],
          'important_distinctions': ['distinction', 'consequence'],
          'constraints': ['constraint', 'implication'],
          'do_not_conclude': ['statement', 'reason']}
CAUTIONS = {
 'H7-T01-1': 'These considerations support analysis of available interpretable observations and conditional paired receiving measurements. They do not provide a cross-delivery logger rotation or field-sampling design, establish successful measurement, or remove implementation and reliability conditions. Failed or inadequate traces remain inconclusive.',
 'H7-T03-1': 'The chronology may structure inquiry, but it does not by itself establish which intervention should be prioritized. Empirical applicability, reliable anchors and successful alignment are not established.',
 'H7-T03-2': 'These considerations support household-specific inquiry, documentation and continuity-based attribution. They do not select an intervention, establish a causal comparison, supply a retain-or-revert rule, or determine the purchasing commitment. Reliable linkage and observed explanations or aggregate effects are not established.'}
INSTRUCTION = '''Analyze the target problem as a decision-support task. Produce a concise, operational response using only information supplied in this packet. Do not invent observations or claim that proposed tests have already been run. Distinguish present facts from proposed inquiries. Focus on what should currently be believed, investigated, prioritized, done, constrained, and used as a future decision rule.
If the packet contains additional vetted considerations, use them only where they materially bear on the target. Do not mention that they came from another framework or source domain. Express the reasoning entirely in the target's own language. You may ignore considerations that do not materially bear on the target.
Return only JSON matching the supplied schema. Keep each item concise; list limits are maxima, not quotas. For survivor_basis, provide hidden traceability only for response items actually supported by additional considerations; use their V IDs. It is not part of visible reasoning. Use zero-based item_index, or 0 for current_position. An item based only on target material needs no entry. With no additional considerations, return survivor_basis as an empty list.'''
IMPACT_INSTRUCTION = '''Compare Response A and Response B for substantive differences in reasoning about the supplied target. Do not choose a winner, infer hidden experimental conditions, or reward length, terminology, elaboration or formatting. No extra observations or tests have been performed.
A difference is material only if it could change what evidence is gathered, what uncertainty is resolved first, what action is taken or withheld, what future condition triggers action, what conclusion/action is ruled out, or the decision-relevant representation used to choose among these. Material does not mean proven beneficial.
Categories:
PROBLEM_REPRESENTATION_CHANGE: a different decision-relevant distinction, state decomposition, causal partition, temporal representation, evidentiary structure or boundary. It counts as material only with a documented downstream inquiry, priority, action, decision-rule or constraint consequence.
INQUIRY_CHANGE: a substantively different observation, comparison, test, evidence request or discriminating question.
PRIORITY_CHANGE: a changed justified ordering of live questions, explanations, evidence needs or work.
ACTION_CHANGE: a different immediate concrete action or withholding of an action the other would take.
DECISION_RULE_CHANGE: a different condition determining future action.
CONSTRAINT_CHANGE: a different bound, prohibition, prerequisite, stopping condition or do-not-conclude/do-not-act rule.
NO_MATERIAL_CHANGE: semantically equivalent recommendations or merely wording, elaboration, formatting or generic detail. Represent this by overall_material_difference NO and differences [] when no material or plausibly material differences exist. Do not manufacture differences.
For each difference, introduced_in is A_ONLY when B lacks that substantive contribution, B_ONLY when A lacks it, or BOTH_DIFFERENT when the responses take different substantive approaches. An absent side should be described explicitly, referencing the closest relevant field if helpful. Include exact zero-based response locations, content faithful to each response, and a concrete consequence in each present side's downstream_consequence; use an empty string if no consequence is established. A difference may have multiple categories. Avoid counting the same substantive change twice. Include plausible uncertain differences as UNCERTAIN. semantic_equivalence YES means equivalent target reasoning, NO means established substantive difference, UNCERTAIN means unresolved.
Return only JSON matching the schema. Do not identify a preferred response.'''

def read(p): return json.loads(p.read_text())
def write(p, x):
 p.parent.mkdir(parents=True, exist_ok=True)
 with p.open('x') as f: json.dump(x, f, indent=2); f.write('\n')
def text(p, x):
 p.parent.mkdir(parents=True, exist_ok=True)
 with p.open('x') as f: f.write(x+'\n')
def obj(props): return {'type':'object','properties':props,'required':list(props),'additionalProperties':False}
def string(): return {'type':'string'}
def enum(values): return {'type':'string','enum':values}
def array(item, maximum=None):
 d={'type':'array','items':item}
 if maximum is not None: d['maxItems']=maximum
 return d

def prepare():
 visible={'current_position':obj({'statement':string(),'rationale':string()})}
 for field, keys in FIELDS.items():
  visible[field]=array(obj({k:({'type':'integer','minimum':1,'maximum':3} if k=='rank' else string()) for k in keys}),4 if field=='important_distinctions' else 3)
 basis=obj({'response_field':enum(list(visible)), 'item_index':{'type':'integer','minimum':0}, 'consideration_ids':array(string())})
 write(H/'schemas/target.schema.json',obj({'target_response':obj(visible),'survivor_basis':array(basis)}))
 side=obj({'content':string(),'response_locations':array(string()),'downstream_consequence':string()})
 diff=obj({'difference_id':string(),'introduced_in':enum(['A_ONLY','B_ONLY','BOTH_DIFFERENT']),
           'categories':array(enum(CATEGORIES)), 'response_a':side,'response_b':side,
           'materially_changes_target_reasoning':enum(['YES','NO','UNCERTAIN']),'rationale':string()})
 write(H/'schemas/impact.schema.json',obj({'impact_judgment':obj({'pair_id':string(),
  'semantic_equivalence':enum(['YES','NO','UNCERTAIN']),'differences':array(diff),
  'overall_material_difference':enum(['YES','NO','UNCERTAIN']),'rationale':string()})}))
 text(H/'target-instruction.txt',INSTRUCTION); text(H/'impact-instruction.txt',IMPACT_INSTRUCTION)
 for sid in SURVIVORS:
  j=read(H7/'artifact-judgments'/f'{sid}.json'); r=read(H7/'remainder-inventory'/f'{sid}.json')
  candidates={c['candidate_id']:c for c in r['candidates']}; deleted=set(read(H7/'ablations'/f'{sid}.json')['deleted_claim_ids'])
  considerations=[]; crosswalk=[]
  for n,kid in enumerate(j['definite_viable_candidate_ids'],1):
   c=candidates[kid]; assert all(v['value']=='YES' for v in c['viability'].values())
   assert not (set(c['surviving_claim_ids']) & deleted)
   vid=f'V{n:02}'
   considerations.append({'id':vid,**{k:c['component'][k] for k in ('value','scope')}})
   crosswalk.append({'consideration_id':vid,'candidate_id':kid,'component_id':c['component']['component_id'],
     'surviving_claim_ids':c['surviving_claim_ids'],'neutralization_edits':[],
     'source_path':str((H7/'remainder-inventory'/f'{sid}.json').relative_to(R))})
  packet={'considerations':considerations,'cautions':[CAUTIONS[sid]]}
  write(H/'survivor-packets'/f'{sid}.json',packet)
  write(H/'survivor-audits'/f'{sid}.json',{'survivor_packet_audit':{'packet_id':sid,
   'definite_candidates_expected':j['definite_viable_candidate_ids'],
   'definite_candidates_present':[x['candidate_id'] for x in crosswalk],
   'deleted_claims_reintroduced':False,'unresolved_content_promoted':False,'scope_conditions_preserved':True,
   'source_identity_removed':True,'passed':True},'crosswalk':crosswalk,
   'operator_review':'All value/scope fields retained verbatim. Reviewed against frozen candidate scopes, deletion inventories and artifact cautions; no source identity occurs in this projection. Cautions constrain use and add no positive machinery.',
   'admission':j['scientific_status']})
 for tid in ('T01','T03'):
  target=read(H7/'targets'/f'{tid}.json')
  p={'target_frame':target}; write(H/'native-packets'/f'{tid}.json',p)
  text(H/'native-packets'/f'{tid}.txt',INSTRUCTION+'\n\nINPUT\n'+json.dumps(p,indent=2))
 for sid in SURVIVORS:
  p={'target_frame':read(H7/'targets'/f'{sid.split("-")[1]}.json'),
     'additional_vetted_considerations':read(H/'survivor-packets'/f'{sid}.json')}
  write(H/'augmented-packets'/f'{sid}.json',p)
  text(H/'augmented-packets'/f'{sid}.txt',INSTRUCTION+'\n\nINPUT\n'+json.dumps(p,indent=2))
 config=read(H7/'execution-config.json')
 config.update(allowed_stages=['native','augmented','impact'],measurements={'native':2,'augmented':3,'impact':3},
               sampling='One fresh context per slot; serial; at most two calls per batch; no retries or replacement.')
 write(H/'execution-config.json',config)
 pairs=[{'pair_id':f'PAIR-{i:02}','target_id':sid.split('-')[1],'survivor_id':sid,
         'native_slot':sid.split('-')[1],'augmented_slot':sid} for i,sid in enumerate(SURVIVORS,1)]
 write(H/'manifest.json',{'base_sha':BASE,'branch':'experiment-h8-target-impact','survivors':SURVIVORS,'pairs':pairs,
   'stage_order':{'native':['T01','T03'],'augmented':SURVIVORS,'impact':[p['pair_id'] for p in pairs]},
   'ordering_rule':'SHA256 UTF-8 H8|<base SHA>|<pair_id>; even first byte => native A; odd => native B',
   'scientific_calls':8,'shared_baseline':'The same T03 native response is used in PAIR-02 and PAIR-03; pairs are correlated.'})
if __name__=='__main__': prepare()
