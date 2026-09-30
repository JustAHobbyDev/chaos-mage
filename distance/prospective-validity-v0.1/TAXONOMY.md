# Condition taxonomy v0.1

Classify only the identified atomic condition, using the unchanged source instrument,
target and mapping. Parent excerpts supply shared qualifications and resolution context;
do not classify other clauses just because they occur in that context. Do not invent
requirements, repair the mapping, judge the whole mapping, or consult external context.
Return the exact condition_id and the structured response required by the schema.

- execution_precondition: ability to instantiate or run an otherwise coherent mapped
  procedure. Establishing it does not materially change mechanism, evidential warrant,
  inference or target. Examples: obtain records, instrument, calibrate, gain access,
  collect observations or run trials. This does not by itself change validity.
- mechanism_condition: truth determines whether state→operation→signal instantiates
  the source's distinctive operational mechanism, such as overlapping paths or genuine
  removal/restoration of the relevant factor.
- warrant_condition: required for signal to justify inference, such as identifiability,
  causal discrimination, feature specificity or an independent evidential bridge.
- target_fidelity_condition: required for the inference to address the retained target
  question. A justified bounded contribution is sufficient; complete solution is not.
- mixed: more than one inseparable functional requirement remains. Use only when
  further decomposition would materially distort the condition; explain the links.
- uncertain: available context cannot settle the category. Explain the missing context.

Categories are not a scale. Test functional role: if false merely prevents running the
procedure, it may be execution; if the source chain ceases to be instantiated, mechanism;
if the signal would not mean what is claimed, warrant; if the inference would not address
the question, target. Being testable or labeled a 'check' does not make a bridge execution.
Checking ordinary instantiation requirements can itself be part of execution. Absence
of an observed outcome alone does not invalidate a coherent prospective procedure.

For execution, populate if_execution.verification_or_satisfaction_method and set
if_validity_relevant to null. For mechanism/warrant/target, set if_execution to null
and affected_link to state_operation_signal / signal_inference / inference_target,
respectively. For mixed use the applicable non-null structures and explain inseparability;
for uncertain these may be null, and uncertainty must explain what cannot be determined.
Preserve uncertainty and disagreements rather than guessing a category.
