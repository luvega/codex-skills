# Biofigure Plot QC

Run this checklist before claiming a plotting template is ready.

## Input QC

- Confirm the input file exists.
- Record row and column counts.
- Verify required columns before plotting.
- Record missing values in mapped columns.
- Record group order and facet order.
- Confirm observation unit: cell, spot, sample, patient, gene, pathway, clone, perturbation, or other.

## Statistical QC

- Use only statistics provided by the recipe or explicitly requested by the user.
- Record the statistical test, effect size, p-value column, adjusted p-value column, and multiple-testing correction.
- For single-cell data, avoid treating cells as independent biological replicates when the claim is sample- or patient-level.
- If statistics are unavailable, mark `statistical_test: user must provide` rather than inventing a method.

## Visual QC

- Save color mapping.
- Avoid rainbow and red-green-only contrast.
- Use Nature-compatible text sizes: 5-7 pt body text and 8 pt panel labels.
- Use Arial or Helvetica and keep text editable.
- Use line and stroke widths between 0.25 pt and 1 pt.
- Confirm main figure width is 89 mm or 183 mm, or Extended Data page width is no more than 180 mm.
- Confirm figure height is no more than 170 mm unless the output is explicitly not Nature-targeted.
- For matplotlib, set `pdf.fonttype = 42` and `svg.fonttype = none`.
- Check long labels, legend wrapping, and facet labels.
- Keep axes and annotation text legible at final export size.
- Save vector and raster outputs.

## Output QC

- Save `plot_data.tsv`.
- For main figures, save editable vector output, preferably `figure.pdf`; keep `.svg` as a working review format when useful.
- For Extended Data, save an accepted raster/EPS output (`.jpg`, `.tiff`, or `.eps`) and keep file size below 10 MB.
- Save raster previews at 450 dpi for main figures where possible and 300 dpi for Extended Data.
- Save `figure_qc.md` with input dimensions, output dimensions, figure kind, width class, column checks, group order, statistics, palette, and package versions.
