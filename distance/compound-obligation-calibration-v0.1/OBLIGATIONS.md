# Compound obligations v0.1

Each claim retains exactly one primary function. A direct secondary obligation is
required when DISTINCT substantive embedded content is MATERIAL to accepting that
claim and UNEVALUATED as a separate frozen claim. If any condition is absent, do not
add an inline secondary judgment. Existing claims take precedence through CLAIM_REF.

Materiality test: if the embedded content were false, unjustified or removed while
everything else remained, could the primary claim still be accepted at essentially
the same meaning and scope? If yes, no secondary obligation; if no, required.

Discovery records embedded subject function/rationale in embedded_classifications,
keyed by dependency_id, before routing. This companion artifact leaves the supplied
claim_obligation_set schema intact. The trigger must match that frozen function;
FACT routes to FACT_WARRANT, INFERENCE to DERIVED_WARRANT, and so forth. Existing
claim references reuse the separately frozen claim classification and overall result.
Unresolvable referents/contracts go in unresolved_dependencies, closure
DEPENDENCY_UNCERTAIN, never guessed subjects or silent omission.

Governance prescribing substantive diagnosis, observation, comparison, experiment,
intervention, transformation or target modification requires OPERATION_LICENSE
unless separately evaluated. Ordinary stop, pause, continue and rollback to the
prior safe state do not alone trigger it. An embedded empirical bridge also needs
its own warrant; governance cannot shield it. Pure prospective normative thresholds
have no empirical obligation merely because they contain numbers. An empirical harm
onset assertion does. Operation discrimination logic requires CONDITIONAL_LICENSE.
Generated limits can require factual, inferential or scope-premise obligations.

One level only: primary claim -> base and direct obligations -> stop. A secondary
requiring another materially distinct obligation sets SPLIT_REQUIRED. Claim refs
form a DAG: reject DEPENDENCY_CYCLE, without inferring a resolution order. Acyclic
references reuse frozen claim results; no recursive model discovery is launched.

All required obligations are evaluated despite scientific failures. Aggregate
VIOLATED > UNCERTAIN > CONDITIONAL > SATISFIED. DEPENDENCY_UNCERTAIN adds a mechanical
UNCERTAIN closure constraint (not a provider judgment), dominated by VIOLATED.
SPLIT_REQUIRED is excluded, with no scientific overall verdict. Referenced excluded
or unmeasured claims prevent complete acceptance. Missing provider observations
keep measurement incomplete; do not manufacture UNCERTAIN provider responses.
