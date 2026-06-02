# Domain Rules

## Bioinformatics

Check the analysis chain before interpreting biology:

- QC: sample quality, library metrics, missingness, doublets, mapping rate, or feature filtering.
- Design: biological replicate, batch, patient-level grouping, paired/unpaired structure, and covariates.
- Differential analysis: test method, multiple testing, effect size, contrast direction, and threshold.
- Enrichment: correct gene universe, ranked versus thresholded input, redundancy, and database version.
- Single-cell: annotation evidence, marker specificity, cell-state versus cell-type wording, integration artifacts, and donor-level replication.
- Trajectory or cell communication: treat inferred direction or ligand-receptor links as hypotheses unless validated.

## Tumor Immunology

Separate immune composition, immune function, and treatment-response inference:

- Cell abundance changes do not prove functional activation.
- Exhaustion, cytotoxicity, antigen presentation, and interferon response require marker-level evidence.
- TCR/BCR clonality needs repertoire evidence, not only expression clusters.
- ICI response claims need cohort definition, therapy line, response criteria, and patient-level statistics.
- Tumor microenvironment interpretations should consider tumor purity, stromal content, biopsy site, and treatment timing.

## Medicinal Chemistry

Keep chemical, biochemical, and biological evidence distinct:

- Target engagement, MOA, SAR, ADMET, toxicity, and efficacy are separate claim types.
- Docking supports pose hypotheses; it does not replace binding or activity assays.
- IC50, EC50, Ki, Kd, and AUC cannot be interchanged without assay context.
- SAR claims need matched analogs and consistent assay conditions.
- ADMET and off-target risks should be reported before clinical or translational claims.

## AI Methods

Interpret models through the task and validation design:

- Define unit of prediction, labels, data split, leakage risk, baseline, metric, and calibration.
- AUROC is insufficient for imbalanced or clinical decision settings; include PR-AUC, sensitivity/specificity, calibration, or decision analysis when relevant.
- Explainability plots show model associations, not biological causality.
- Ablations should map to design choices.
- External validation and subgroup failure analysis determine whether generalization can be claimed.
