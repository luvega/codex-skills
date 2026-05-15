# FigureYa Usage Notes

## Source Assumptions

- Upstream repository: `https://github.com/ying-ge/FigureYa`.
- `references/module-index-local.tsv` is a generated snapshot from the local checkout used when the skill was built.
- The local checkout is intentionally curated: zip bundles, `.trash/`, and local-only legacy modules are excluded from the active Git project.
- The local generated index has 113 tracked top-level FigureYa modules. The upstream `all_included.txt` snapshot bundled here has 199 modules, so some upstream modules are not locally available by exact name.

## Practical Adaptation Pattern

1. Search for candidate modules by task terms.
2. Inspect the module Rmd and sample inputs.
3. Copy only the needed files to a clean working folder.
4. Convert the user's data into the module's expected input schema.
5. Run the smallest useful R script/render path.
6. Verify generated files and record exact assumptions.

## What to Inspect in a Module

- `*.Rmd`: dependencies, input expectations, statistical method, plotting function, output filenames.
- `easy_input_*`: required columns and example value formats.
- `example.png`: intended visual target.
- `*.html`: rendered report and explanatory prose.
- `install_dependencies.R`: dependency hints. Use cautiously; prefer existing R environments when possible.

## Common Failure Modes

- Survival plots use inverted event coding.
- DEG plots use the wrong contrast direction.
- Gene IDs mix symbols, Ensembl IDs, and aliases.
- Single-cell modules require large intermediate objects that should not be reloaded repeatedly.
- Immune infiltration scores from different tools are treated as interchangeable.
- A module is visible in upstream but missing locally; fetch it before trying to execute.
