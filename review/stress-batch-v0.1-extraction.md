# Stress Batch v0.1 — Extraction Pass

Status: extraction complete; required adjudication completed. See [stress-batch-v0.1-classification.md](stress-batch-v0.1-classification.md).

The ten preregistered candidates were extracted under the frozen five-field schema and extraction decision rule. This document records only the extractor's proposed classifications and observed pressure points. It does not calculate calibration thresholds or adjudicate borderline cases.

| Candidate | Proposed status | Primary pressure | Extractor note |
| --- | --- | --- | --- |
| Seismic tomography | accepted | composite | Multi-stage inverse workflow, but one coherent propagation-to-hidden-structure chain is preserved. |
| System identification | provisional | composite | Candidate may bundle excitation/measurement, model fitting, and validation. Proposed issue is granularity, not schema relevance. |
| Chromatography | accepted | composite | Separation itself extracts cleanly when identification is kept downstream. |
| Source corroboration | accepted | nonphysical signal | Signal is relational convergence/contradiction among assessed independent sources. |
| Provenance reconstruction | accepted | nonphysical / temporal signal | Signal is documentary chronological coherence plus explicit gaps. |
| Analysis of Competing Hypotheses | accepted | eliminative / nonphysical | Signal is comparative inconsistency across explicit alternatives. |
| Regression bisection | accepted | eliminative | Binary tests repeatedly remove intervals from an ordered history. |
| Delta debugging | accepted | eliminative | Repeated removal tests reduce a failure-inducing configuration. |
| Dendrochronological crossdating | accepted | temporal / relational | Signal is alignment among multiple ordered records. |
| Step-response probing | accepted | temporal | Known perturbation produces an observed response trajectory. |

## Extractor-proposed schema relevance

No candidate currently proposes a schema-relevant failure or gap signature.

This is **not** an adjudicated finding. Mandatory adjudication is still required for the provisional system-identification extraction and for any other case triggered by the preregistered adjudication rule.

## Observed extraction pressure

### Candidate granularity

System identification produced the clearest candidate-boundary concern. Seismic tomography also contains multiple real-world stages, but the extractor judged those stages subordinate to one coherent inverse-imaging operation.

Chromatography helped distinguish a tool from downstream interpretation: chromatographic separation extracted cleanly only when definitive identification was excluded from its inferential claim.

### Nonphysical signals

Source corroboration, provenance reconstruction, and crossdating all admitted signals that are relational rather than sensory events:

- convergence/contradiction among independent sources;
- chronological compatibility among documentary traces;
- sequence alignment across independent temporal records.

No additional schema field was required during extraction.

### Eliminative inference

ACH, regression bisection, and delta debugging represented elimination in different spaces:

- named explanatory alternatives;
- intervals in an ordered history;
- components of a failure-inducing configuration.

Each could express the observable distinction under `signal` and the resulting narrowing under `inference`.

### Temporal signals

Crossdating and step-response probing both extracted without requiring a separate temporal field. Time is part of the structure of the signal rather than separate metadata.

## Completion

The mandatory system-identification adjudication is recorded under `review/adjudications/`. The final preregistered batch calculation is recorded in [stress-batch-v0.1-classification.md](stress-batch-v0.1-classification.md).
