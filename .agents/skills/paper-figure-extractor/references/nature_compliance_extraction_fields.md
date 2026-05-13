# Nature Compliance Extraction Fields

Use these fields when the source paper is Nature-family or the requested output should be Nature-style. The fields are for abstract rule capture only; do not copy published panels or layouts.

## Fields

| Field | Capture |
| --- | --- |
| `figure_kind` | `main`, `extended-data`, `chemical-structure`, `summary-paragraph`, `mixed`, or `not assessed` |
| `target_width_class` | `single-column 89 mm`, `double-column 183 mm`, `extended-data 180 mm`, `unknown`, or `not assessed` |
| `panel_layout_rule` | Alphabetical order, space-efficient layout, asymmetric panel sizing, or source-specific layout note |
| `panel_label_rule` | Lowercase bold panel labels, label position, or `not visible/not assessed` |
| `font_size_rule` | Observed or required range such as `5-7 pt body, 8 pt panel labels` |
| `axis_units_rule` | Whether axes include units in parentheses or units are not applicable |
| `accessibility_rule` | Color-blind safe palette, red-green risk, colored text risk, keyline/key usage |
| `image_integrity_rule` | Notes on microscopy, gels/blots, splicing, insets, contrast, raw data needs |
| `chemical_structure_rule` | Notes on structure drawing, atom labels, wedges, arrows, ChemDraw settings |
| `export_format_rule` | Main figure vector/editable output or Extended Data raster/EPS output requirement |
| `compliance_conflicts` | Any conflict between a published example and current Nature guidance |

## Defaults

Use `not assessed` when the field was outside scope. Use `not reported in PDF` only when the PDF text/caption should have reported a fact but did not.
