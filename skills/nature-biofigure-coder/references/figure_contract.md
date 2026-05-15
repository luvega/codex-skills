# Figure Contract

Use this before writing final plotting code or assembling a multi-panel figure. For exploratory recipe tests, record a shorter contract in the QC report.

## Required Fields

```text
core_conclusion:
figure_archetype: quantitative_grid | schematic_led_composite | image_plate_plus_quant | asymmetric_mixed_modality
target_output: main | extended-data | internal-review
backend_policy: both_templates | python_only | r_only
final_size:
panel_map:
evidence_hierarchy:
statistics_needed:
source_data_needed:
palette_vocabulary:
image_integrity_notes:
reviewer_risks:
```

## Rules

- Start from the core conclusion, not from a favorite template.
- Every panel must answer a unique scientific question. If removing a panel does not weaken the argument, merge or remove it.
- Separate hero evidence from validation, controls, robustness, and subgroup evidence.
- Keep condition and cell-type colors stable across panels.
- Prefer shared legends or direct labels when repeated legends would waste figure space.
- Record `n`, replicate definition, center, spread or interval, statistical test, correction, and source-data table for every quantitative panel.
- For microscopy, blots, gels, spatial images, or representative image panels, record raw-file traceability, crop, contrast, pseudo-color, scale calibration, and quantification link.
