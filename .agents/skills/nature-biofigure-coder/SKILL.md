---
name: nature-biofigure-coder
description: Use when Codex needs to generate reproducible R or Python plotting code for biomedical and bioinformatics figures from structured figure cards, plot_recipe.yml files, or extraction tables. Trigger for UMAP, dot plot, heatmap, volcano, enrichment, cell composition, survival, forest, spatial transcriptomics, TCR/BCR, CRISPR, drug response, multi-omics, trajectory, RNA velocity, GSEA, UpSet, alluvial, oncoprint, CNV, Manhattan, circos, genome tracks, WGCNA, ligand-receptor, QC, and method benchmark plots.
---

# Nature Biofigure Coder

## Overview

Generate editable, reproducible plotting code from structured figure cards or plot recipes. The generated code must use the user's own data, preserve the card's declared statistics, and export both plotting data and publication-ready figures.

This skill complements `paper-figure-extractor`: the extractor creates abstract plot recipes, and this skill turns those recipes into R/Python templates.

## Required Operating Rules

Before using this skill, read and follow `../../references/agent_operating_rules.md`. In particular: state assumptions, ask on material ambiguity, keep plotting changes surgical, use the model for recipe interpretation while deterministic code handles validation/routing/retries, define success criteria, test plotting intent, checkpoint multi-step work, and make skipped checks or uncertain statistics visible.

## Nature Compliance Sync

When the target output is Nature-family, read `../nature-figure-compliance/references/nature_figure_specs.yml` and `../nature-figure-compliance/references/nature_figure_requirements.md` before generating code. Treat those files as the source of truth for hard output constraints. Use `paper-figure-extractor` cards only for plot grammar and biological mapping, not for overriding current Nature requirements.

## Figure Contract and Backend Policy

Before writing plotting code for a final figure, read `references/figure_contract.md` and define the figure's one-sentence conclusion, evidence hierarchy, archetype, panel map, source data, statistics, and reviewer risks.

Backend policy:

- For recipe exploration, benchmarking, and user requests that explicitly ask for both languages, generate both R and Python templates.
- For final submission figures, or when the user chooses one language, use the selected backend for plotting, previews, exports, and visual QA.
- Do not silently switch backend because a package is missing. Report the blocker, write install notes if useful, or ask permission to install.
- The non-selected language may inspect files or convert tables only when it does not create the visual output.

## Inputs

- A figure extraction card, `plot_recipe.yml`, or extraction table row.
- A user data path and required columns.
- Preferred language: R, Python, or both.
- Output directory.
- Figure kind: `main` or `extended-data`.
- Width class: `single-column`, `double-column`, or `extended-data`.
- Comparison direction, group order, statistical test, and multiple-testing correction when relevant.

For plot-family selection, consult `references/bioinformatics_plot_type_atlas.md` before inventing a new recipe name.

## Workflow

1. Read the card or recipe and identify plot type, observation unit, required columns, data shape, mappings, statistics, and palette semantics.
2. Define the figure contract for final figures, or record why a lightweight recipe contract is enough for exploratory templates.
3. Validate the user's input file exists and contains the required columns before generating plot code.
4. Load `references/style_tokens.yml` and `references/palettes.yml` only when styling or palette choices are needed.
5. Use `references/r_python_package_map.md` to choose packages that match the plot type and input data.
6. Do not invent missing statistics. If the recipe says `not reported in PDF`, generate code that either omits the test or exposes a parameter the user must set.
7. Apply Nature hard specs when requested: 89 mm or 183 mm main-figure widths, 170 mm maximum height, 5-7 pt body text, 8 pt panel labels, 0.25-1 pt line widths, editable text, RGB output, color-blind-safe palettes, and `pdf.fonttype=42` for matplotlib.
8. Generate script(s) that save the plotting table, editable vector output, high-resolution raster output, and a QC markdown report.
9. Record package versions or session information.

## Standard Outputs

Use these names unless the user requests a different structure:

- `script.R`
- `script.py`
- `plot_data.tsv`
- `figure.pdf`
- `figure.svg`
- `figure.png`
- `figure_qc.md`

For Nature main figures, prefer editable vector output (`.pdf` plus `.svg` for working review). For Extended Data, also support `.jpg`/`.jpeg`, `.tif`/`.tiff`, or `.eps` according to the target package.

## Visual Rules

- Use a white background, Arial or Helvetica, thin axes, compact legends, and explicit statistical annotations.
- Keep text editable; do not outline text.
- Keep body text between 5 pt and 7 pt unless the user explicitly targets a non-Nature output.
- Use 8 pt bold upright lowercase panel labels for multi-panel Nature figures.
- Keep line and stroke widths between 0.25 pt and 1 pt.
- Avoid rainbow gradients, red-green-only contrast, heavy borders, decorative backgrounds, and unneeded chart junk.
- Use semantic colors from `references/palettes.yml`; preserve group-to-color mappings in the QC report.
- Keep one restrained palette per figure: a neutral family, a signal family, and an accent family. Avoid assigning every panel an unrelated color vocabulary.
- Keep group order, facet order, and comparison direction explicit.
- For single-cell and spatial plots, keep cell-level visualization separate from sample- or patient-level statistical claims.

## Bundled Helpers

- R theme helpers: `scripts/r/theme_nature_bio.R`
- R palette helpers: `scripts/r/palettes.R`
- Python style helpers: `scripts/python/style_nature_bio.py`
- Python palette helpers: `scripts/python/palettes.py`
- Figure contract: `references/figure_contract.md`

These helpers are optional starting points. Generated scripts may inline equivalent code when that makes the result easier to run.

## QC Requirements

Before finishing generated plotting code, verify:

- Input dimensions and required columns are recorded.
- Group order and comparison direction are recorded.
- Statistical test and multiple-testing correction are recorded or explicitly marked as user-supplied.
- Color mapping is saved.
- Output dimensions, figure kind, width class, and max-height compliance are recorded.
- Output formats include at least one editable vector format and one high-resolution raster format.
- The plotting table used for the figure is saved separately from the source data.
