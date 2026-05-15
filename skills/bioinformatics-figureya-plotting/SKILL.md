---
name: bioinformatics-figureya-plotting
description: Use when creating, adapting, or troubleshooting biomedical and bioinformatics plots with FigureYa, R, R Markdown, or module-style examples for gene expression, survival, DEG, enrichment, mutation, immune, drug, single-cell, multi-omics, ROC, heatmap, volcano, circos, WGCNA, GSVA, GSEA, and publication-ready figure tasks.
---

# Bioinformatics FigureYa Plotting

## Overview

Use FigureYa modules as executable plot templates, not as black boxes. Prefer a local FigureYa checkout for concrete Rmd/input/output examples, then use the upstream module list to identify newer or missing modules.

## Workflow

1. Clarify the plot target: data modality, biological question, required figure type, input files, grouping variables, statistical comparison, and output format.
2. Locate modules with `scripts/figureya_module_search.py`; search by plot type and biology terms, for example `heatmap DEG`, `survival risk`, `single cell marker`, `immune subtype`, `GSEA`, `mutation oncoplot`, or `drug IC50`.
3. Prefer local tracked modules from `references/module-index-local.tsv`. If a needed module is only in `references/upstream-all-included.txt`, tell the user it must be fetched from upstream or the compressed FigureYa archive before execution.
4. Read the chosen module's `*.Rmd`, `easy_input_*`, `example.png`, and existing `*.html` report before writing code. Treat `install_dependencies.R` as dependency documentation; do not run installers blindly.
5. Adapt by copying the minimal required module files into a task-specific working folder or output folder. Do not overwrite the original FigureYa module unless the user explicitly asks to modify the module itself.
6. Map user data into the module's expected `easy_input_*` schema. Preserve gene/sample IDs, group labels, survival time/status encoding, and factor order explicitly.
7. Render or run the adapted R code. Verify outputs exist, are non-empty, and visually inspect PDFs/PNGs/HTML when layout matters.
8. Report the selected module, data transformation assumptions, output paths, and any dependencies or missing upstream assets.

## Module Search

Run from the skill directory, or replace `<skill-dir>` with the installed skill path:

```powershell
python <skill-dir>\scripts\figureya_module_search.py search "volcano DEG"
```

When a local FigureYa checkout is available, pass it with `--repo`:

```powershell
python <skill-dir>\scripts\figureya_module_search.py search "single cell marker heatmap" --repo <path-to-FigureYa>
```

To refresh a local module index from a checkout:

```powershell
python <skill-dir>\scripts\figureya_module_search.py index <path-to-FigureYa> --out module-index-local.tsv
```

## Choosing Modules

Use `references/task-map.tsv` first for common tasks:

- heatmap: expression heatmaps, marker heatmaps, p-value heatmaps, signature heatmaps
- volcano and DEG: differential expression, multi-class DEG, scRNA DEG
- survival and risk: Cox/KM/nomogram/risk score/timeROC/RF survival
- immune and TME: immunotherapy response, immune infiltration, immune subtypes, IPS, TIME
- enrichment: GSEA, GSVA, ssGSEA, GO clustering, pathway simulation
- mutation and multi-omics: oncoplot, mutation signatures, SNV, methylation, CNV, circos
- single-cell: scRNA markers, scDEG, scHeatmap, AUCell, CellChat, RNA velocity, cNMF
- drug and target: GDSC, CMap, target networks, CMAP/XSum, oncoPredict-style tasks
- machine learning: SVM, Elastic Net, repeated LASSO, GMM, random forest survival

If several modules fit, choose the one whose sample inputs most closely match the user's data shape. Avoid forcing data into a visually similar module when its statistics answer a different biological question.

## FigureYa Conventions

- Main analysis usually lives in `FigureYa*/FigureYa*.Rmd`.
- Inputs are commonly named `easy_input_*`, `input_*`, or documented in the Rmd.
- `example.png` shows expected visual style or target figure layout.
- HTML reports are useful for understanding the intended result, even when reproducing only the R code.
- PDFs/PNGs in a module are expected outputs, not inputs, unless the Rmd says otherwise.
- Zip files are offline bundles and should not be edited directly. Use extracted module directories.

## Safety

- Keep original modules read-only unless the task is to update FigureYa itself.
- Do not commit or copy large local data, `.trash/`, zip bundles, caches, or generated outputs into a project repository without explicit user intent.
- Prefer project-local output directories such as `outputs/<task-name>/` or `results/<date-task>/`.
- For clinical/survival plots, verify status coding and censoring direction before rendering final figures.
- For DEG/enrichment plots, verify organism, gene ID type, contrast direction, and adjusted p-value column.
- For single-cell plots, use existing AnnData/Seurat objects only after confirming memory cost; consider the persistent-analysis-session skill for repeated large-object work.

## References

- `references/task-map.tsv`: curated task-to-module map.
- `references/module-index-local.tsv`: generated snapshot of tracked modules from the local checkout used when the skill was built.
- `references/upstream-all-included.txt`: upstream FigureYa module list from `ying-ge/FigureYa`.
- `references/upstream-local-coverage.tsv`: which upstream modules are present locally by exact name.
- `references/figureya-usage.md`: operational notes for adapting modules.
