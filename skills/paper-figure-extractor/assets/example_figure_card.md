# Figure Extraction Card

## Source

paper_id: Example2026_Biofigure
citation: Example citation only; replace with real citation
doi:
figure_panel: Fig1a
pdf_path: literature/pdfs/example.pdf
page_number: 3
caption_excerpt: Short locator text only

## Biological question

question: Which cell states are present across treatment groups?
comparison_direction: treatment versus control
disease_or_context: solid tumor immune microenvironment
source_status: user observation
confidence: medium

## Data type

primary_data_type: scRNA-seq
observation_unit: cell
feature_unit: gene
metadata_required: cell_id, sample_id, patient_id, condition, cell_type, UMAP_1, UMAP_2
matrix_or_table_shape: one row per cell with embedding coordinates and metadata
source_status: inferred
confidence: medium

## Plot grammar

plot_type: UMAP embedding
x_mapping: UMAP_1
y_mapping: UMAP_2
color_mapping: cell_type
size_mapping: fixed point size
shape_mapping:
facet_mapping: condition
ordering_rule: draw rare cell types last if label visibility matters
annotation_rule: direct labels or compact legend
source_status: visible in page image
confidence: medium

## Statistical layer

statistical_test: not reported in PDF
multiple_testing: not reported in PDF
effect_size: not reported in PDF
n_definition: not reported in PDF
paired_or_unpaired: not reported in PDF
comparison_direction: treatment versus control
source_status: not reported in PDF
confidence: not applicable

## Visual style

background: white
font: Arial or Helvetica
axis_style: axes hidden for embedding
grid_style: none
legend_style: compact categorical legend
point_style: small semi-opaque points
line_style:
label_density: sparse
panel_border: none
source_status: inferred
confidence: low

## Palette

palette_type: semantic categorical
biological_color_logic: immune lineages use cool colors; stromal cells use gray/brown; tumor cells use muted red
hex_colors_if_extractable:
avoidance_rules: avoid rainbow and red-green-only contrast
source_status: inferred
confidence: low

## Nature compliance

figure_kind: main
target_width_class: single-column 89 mm or double-column 183 mm, chosen by panel density
panel_layout_rule: arrange panels alphabetically with minimal white space
panel_label_rule: lowercase bold upright panel labels
font_size_rule: 5-7 pt body text; 8 pt panel labels
axis_units_rule: not applicable for embedding axes unless coordinates are explicitly interpreted
accessibility_rule: avoid red-green-only palette; keep legend keys distinct under color-blind simulation
image_integrity_rule: not applicable to computed embedding unless microscopy underlay is added
chemical_structure_rule: not applicable
export_format_rule: editable vector output for main figure; RGB color
compliance_conflicts: not assessed
source_status: inferred
confidence: medium

## Reusable rule

This plot is useful when: showing major cell-state structure and sample conditions in a single-cell atlas
Do not use this plot when: quantitative group comparison is the main evidence; use sample-level statistics instead
Required QC: verify embedding columns, group labels, cell count per group, and color mapping
