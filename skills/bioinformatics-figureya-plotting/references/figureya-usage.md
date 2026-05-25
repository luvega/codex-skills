# FigureYa Usage Notes

## Source Assumptions

- Upstream repository: `https://github.com/ying-ge/FigureYa`.
- `F:\FigureYa\docs\module_inventory.tsv` is the preferred current local inventory when that checkout is available.
- `references/module-index-local.tsv` is a generated fallback snapshot from the local checkout used when the skill was built.
- The local checkout is intentionally curated: zip bundles, `.trash/`, and local-only legacy modules are excluded from the active Git project.
- The local generated index has 113 tracked top-level FigureYa modules. The upstream `all_included.txt` snapshot bundled here has 199 modules, so some upstream modules are not locally available by exact name.

## Practical Adaptation Pattern

1. Search for candidate modules by task terms.
2. Refresh `F:\FigureYa\docs\module_inventory.tsv` if the local checkout changed.
3. For publication-facing or Nature-family figures, refresh `F:\FigureYa\docs\nature_style_audit.tsv` with `python F:\FigureYa\scripts\figureya_nature_style_audit.py --repo F:\FigureYa --inventory F:\FigureYa\docs\module_inventory.tsv --out F:\FigureYa\docs\nature_style_audit.tsv --report F:\FigureYa\docs\nature_style_summary.md`.
4. Inspect the module Rmd, sample inputs, example image, HTML report, and Nature style audit row.
5. Copy only the needed files to a clean working folder.
6. Convert the user's data into the module's expected input schema.
7. For Nature-style output, source `F:\FigureYa\styles\nature_figure_style.R` and replace module defaults that conflict with Nature width, height, text, color, or export requirements.
8. Run the smallest useful R script/render path.
9. Verify generated files and record exact assumptions.

## What to Inspect in a Module

- `*.Rmd`: dependencies, input expectations, statistical method, plotting function, output filenames.
- `easy_input_*`: required columns and example value formats.
- `example.png`: intended visual target.
- `*.html`: rendered report and explanatory prose.
- `install_dependencies.R`: dependency hints. Use cautiously; prefer existing R environments when possible.
- `docs\nature_style_audit.tsv`: static flags for palette, export-size, raster-output, font/text-size, input/example, and manual-review risks.
- `styles\nature_figure_style.R`: reusable Nature-style ggplot2 theme, palette, and export helper to apply in copied/adapted task code.

## Common Failure Modes

- Survival plots use inverted event coding.
- DEG plots use the wrong contrast direction.
- Gene IDs mix symbols, Ensembl IDs, and aliases.
- Single-cell modules require large intermediate objects that should not be reloaded repeatedly.
- Immune infiltration scores from different tools are treated as interchangeable.
- A module is visible in upstream but missing locally; fetch it before trying to execute.
- A copied module keeps oversized `ggsave()`/`pdf()` defaults from the template; replace these with explicit Nature width and height before publication output.
- A heatmap or gradient uses rainbow, red-green, or unreviewed `scale_*_gradientn()` colors; replace with accessible semantic colors and document the mapping.
