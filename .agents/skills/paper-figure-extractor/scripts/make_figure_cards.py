#!/usr/bin/env python
"""Create a starter figure extraction card for one panel."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEMPLATE = """# Figure Extraction Card

## Source

paper_id: {paper_id}
citation: {citation}
doi: {doi}
figure_panel: {figure_panel}
pdf_path: {pdf_path}
page_number: {page_number}
caption_excerpt: {caption_excerpt}

## Biological question

question:
comparison_direction:
disease_or_context:
source_status:
confidence:

## Data type

primary_data_type:
observation_unit:
feature_unit:
metadata_required:
matrix_or_table_shape:
source_status:
confidence:

## Plot grammar

plot_type:
x_mapping:
y_mapping:
color_mapping:
size_mapping:
shape_mapping:
facet_mapping:
ordering_rule:
annotation_rule:
source_status:
confidence:

## Statistical layer

statistical_test: not reported in PDF
multiple_testing: not reported in PDF
effect_size: not reported in PDF
n_definition: not reported in PDF
paired_or_unpaired: not reported in PDF
comparison_direction:
source_status:
confidence:

## Visual style

background:
font:
axis_style:
grid_style:
legend_style:
point_style:
line_style:
label_density:
panel_border:
source_status:
confidence:

## Palette

palette_type:
biological_color_logic:
hex_colors_if_extractable:
avoidance_rules:
source_status:
confidence:

## Nature compliance

figure_kind: not assessed
target_width_class: not assessed
panel_layout_rule: not assessed
panel_label_rule: not assessed
font_size_rule: not assessed
axis_units_rule: not assessed
accessibility_rule: not assessed
image_integrity_rule: not assessed
chemical_structure_rule: not assessed
export_format_rule: not assessed
compliance_conflicts: not assessed
source_status:
confidence:

## Bioinformatics workflow inferred

input_data_shape:
preprocessing: not reported in PDF
normalization: not reported in PDF
transformation: not reported in PDF
feature_selection: not reported in PDF
model_or_test: not reported in PDF
output_table:
source_status:
confidence:

## R implementation

candidate_packages:
core_functions:
notes:

## Python implementation

candidate_packages:
core_functions:
notes:

## Reusable rule

This plot is useful when:
Do not use this plot when:
Required QC:

## Codex instruction candidate

Generate R and Python code to reproduce this abstract plot type using my own data, not the original paper data.

## Cautions

- Do not reproduce original figures.
- Do not infer missing statistics.
- Keep citation and locator metadata, not reusable image assets.
"""


def slugify(value: str) -> str:
    value = value.strip().replace(" ", "_")
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value)
    return value.strip("._") or "figure_panel"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a starter figure extraction card.")
    parser.add_argument("--paper-id", required=True)
    parser.add_argument("--figure-panel", required=True)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--citation", default="")
    parser.add_argument("--doi", default="")
    parser.add_argument("--pdf-path", default="")
    parser.add_argument("--page-number", default="")
    parser.add_argument("--caption-excerpt", default="")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    output = args.out_dir / f"{slugify(args.paper_id)}_{slugify(args.figure_panel)}.md"
    if output.exists() and not args.overwrite:
        raise SystemExit(f"Refusing to overwrite existing card: {output}")

    output.write_text(
        TEMPLATE.format(
            paper_id=args.paper_id,
            figure_panel=args.figure_panel,
            citation=args.citation,
            doi=args.doi,
            pdf_path=args.pdf_path,
            page_number=args.page_number,
            caption_excerpt=args.caption_excerpt,
        ),
        encoding="utf-8",
        newline="\n",
    )
    print(output)


if __name__ == "__main__":
    main()
