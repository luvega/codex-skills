# Algorithm Explanation

Use this when explaining AI, ML, statistical, or computational methods to biomedical readers.

Required elements:

- `task_definition`: prediction, classification, clustering, ranking, generation, or inference task.
- `algorithm_summary`: what the method optimizes or estimates.
- `inputs_outputs`: input data, labels, outputs, and units.
- `evaluation_plan`: split, metrics, baselines, ablations, calibration, and validation.
- `failure_modes`: leakage, confounding, imbalance, shift, overfitting, or poor interpretability.
- `biomedical_meaning`: what the output can and cannot mean biologically or clinically.
- `evidence_map`: claim-evidence-status entries.

Rules:

- Explain the model around the scientific task, not around implementation details first.
- Distinguish predictive utility from mechanism.
- Do not call feature importance causal evidence.
- Include the simplest baseline a reviewer would expect.
