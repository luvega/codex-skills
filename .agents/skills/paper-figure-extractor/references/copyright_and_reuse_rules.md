# Copyright and Reuse Rules

The skill extracts reusable plot grammar. It must not package published figures as reusable assets.

## Allowed in skill outputs

- Citation, DOI, journal, year, and paper ID.
- Figure and panel locator, page number, and brief caption locator text.
- Abstract plot type, data shape, variable mappings, ordering logic, statistical rule, and annotation rule.
- Semantic color rules and approximate style tokens when clearly marked as observed or inferred.
- R/Python package suggestions and implementation notes.

## Do not store in reusable skills

- Full PDFs.
- Cropped published figure panels.
- Original figure images as templates or assets.
- Long verbatim figure legends or article text.
- Reusable materials that trace or recreate a specific published figure.

## Required wording

Use phrases such as:

- `source_status: explicit in caption/text`
- `source_status: visible in page image`
- `source_status: inferred`
- `statistical_test: not reported in PDF`
- `palette_hex_if_extractable: visually approximated; confidence low`

When a user asks to recreate a published figure, redirect to generating a new figure for the user's own data using the abstract grammar.
