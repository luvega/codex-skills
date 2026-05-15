# Figure Contract QC

Use this when reviewing a Nature-family figure package before final export or submission.

## Claim and Panel Logic

- Is there a one-sentence core conclusion with a clear verb?
- Does every panel map to a unique part of the conclusion?
- Is the evidence hierarchy explicit: hero evidence, validation evidence, controls, robustness, and subgroup analysis?
- Is the figure archetype declared: `quantitative_grid`, `schematic_led_composite`, `image_plate_plus_quant`, or `asymmetric_mixed_modality`?
- Are repeated panels, redundant legends, or equal-size panels hiding the real evidence hierarchy?

## Statistics Minimum

For each quantitative panel, check:

```text
n definition:
biological replicates:
technical replicates:
center statistic:
spread_or_interval:
test:
multiple_testing_correction:
p_value_display:
source_data_file:
```

For machine-learning or model panels, also check:

```text
train_validation_test_split:
number_of_seeds_or_folds:
metric_definition:
confidence_or_variability_definition:
baseline_definition:
```

## Image Integrity Minimum

For image-led panels, check:

```text
raw_file_available:
processed_file:
crop_scope:
brightness_contrast_gamma:
pseudo_color:
scale_calibration:
stitching_or_compositing:
reuse_in_other_figures:
quantification_link:
```

Global adjustments are generally safer than selective local edits. If an adjustment changes relevant background, faint bands, cell boundaries, or spatial context, flag it.

## Export Review

- Confirm the selected backend or toolchain produced the final visual outputs.
- Confirm text remains editable in vector files unless a special symbol requires outlining.
- Confirm raster image elements have sufficient real resolution at final size.
- Confirm source data, scripts, editable vector, raster preview, and QC notes travel together when requested.
