---
name: paper-figure-extractor
description: Use when Codex needs to analyze biomedical paper PDFs, figure captions, figure panels, legends, plot types, statistical annotations, palettes, or literature-derived bioinformatics plotting recipes. Trigger for PDF-to-figure-card extraction, page/text extraction, paper manifests, and abstract plot grammar capture. Do not reproduce copyrighted figures; extract reusable rules only.
---

# Paper Figure Extractor

## Overview

Extract structured, reusable figure-design information from biomedical papers. The output is a set of figure cards and plot-recipe candidates that describe abstract plot grammar, data shape, statistics, source grounding, and style rules for the user's own bioinformatics figures.

Do not recreate, trace, or package published figures. Use PDFs, page renders, captions, and user observations only to extract abstract design rules.

## Required Operating Rules

Before using this skill, read and follow `../../references/agent_operating_rules.md`. In particular: state assumptions, ask on material ambiguity, keep extraction changes surgical, use the model only for judgment/extraction, keep deterministic PDF routing and file handling in scripts, checkpoint multi-step work, and make skipped or uncertain fields visible.

## Nature Figure Sync

When extracting from Nature-family examples or building recipes for Nature-style output, read `../nature-figure-compliance/references/example_corpus_usage.md` and `references/nature_compliance_extraction_fields.md`. Extract only abstract compliance signals: figure kind, panel layout, text/font clues, accessibility cues, image-integrity issues, chemical-structure requirements, and export implications. Do not treat a published example as overriding current Nature requirements.

## Source-Grounded Extraction

Build a lightweight source map before creating reusable cards when traceability matters. Use stable IDs such as `P001` for body paragraphs, `C001` for captions, `F001` for figures, and `T001` for tables. Every card should point to a page number plus the closest source block, not to a copied figure image.

Separate each important field into `observed`, `inferred`, or `missing`. If the user asks for prose, abstract, title, figure legend, or manuscript language style rather than plot grammar, use `nature-language-style` instead of overloading this skill.

Use `caption_excerpt` for a short literal caption or source locator from the extracted Markdown. Put paraphrased biological questions in `question`, not in `caption_excerpt`.

When a card depends on visual evidence such as panel layout, plot geometry, color semantics, spatial images, microscopy images, or extracted hex colors, render the PDF page image first and mark the supporting field as `visible in page image`. Do not keep visual claims that only came from text extraction.

## Workflow

1. Create or update `literature/manifest/paper_manifest.tsv`. Use `references/paper_manifest_template.tsv` for the required columns.
2. Extract PDF text with `scripts/extract_pdf_text.py` into `literature/extracted/{paper_id}/text/full_text.md`.
3. Render PDF pages with `scripts/extract_pdf_pages.py` into `literature/extracted/{paper_id}/pages/`.
4. Create a source map for target captions, figure mentions, table mentions, and nearby body paragraphs when traceability is needed.
5. Identify target figure captions and panel references from the extracted text.
6. For each selected panel, create a card under `literature/extracted/{paper_id}/cards/`. Use `references/figure_card_template.md` or `scripts/make_figure_cards.py`.
7. Audit card grounding with `scripts/validate_figure_cards.py <cards_dir> --literature-dir literature/extracted --output <audit.md>`. Fix page-number, source-status, caption-locator, and missing-page-render issues before summarizing.
8. Fill the Nature compliance section when the source or target output is Nature-family.
9. Summarize cards into `literature/extracted/{paper_id}/extraction_table.tsv` with `scripts/summarize_extraction_table.py`.
10. Save reusable plot candidates under `figure_skills_output/plot_recipes/` only after the card fields separate observed facts from inferred interpretation.

## Extraction Rules

- Record biological question, data type, plot type, input data shape, variable mappings, ordering rules, statistical layer, annotation logic, palette logic, visual style, and R/Python package candidates.
- Mark unavailable facts as `not reported in PDF`. Do not invent statistical tests, sample sizes, multiple-testing correction, or preprocessing steps.
- Distinguish source status for important fields: `explicit in caption/text`, `visible in page image`, `user observation`, `inferred`, or `not reported in PDF`.
- Capture comparison direction, observation unit, feature unit, metadata columns, and input table shape for every plot.
- Convert colors into semantic palette rules. Avoid vague labels such as "Nature style" unless they are decomposed into fonts, line weights, palette roles, and spacing rules.
- Do not copy the original PDF, figure panels, or long caption excerpts into reusable skill assets. Keep citation, DOI, page number, and short locator text only.
- Keep figure extraction separate from manuscript polishing. Captions may inform plot grammar, but prose style tokens belong in `nature-language-style`.

## References

- `references/extraction_schema.yml`: canonical fields for cards and summary tables.
- `references/plot_type_dictionary.md`: common biomedical plot types, data shapes, and package choices.
- `references/figure_card_template.md`: panel-level card template.
- `references/copyright_and_reuse_rules.md`: what may and may not be stored in reusable skill outputs.
- `references/nature_compliance_extraction_fields.md`: Nature-specific compliance fields to capture during extraction.

## Scripts

- `scripts/extract_pdf_pages.py <pdf_path> <out_dir> [--dpi 200]`
- `scripts/extract_pdf_text.py <pdf_path> <out_path>`
- `scripts/make_figure_cards.py --paper-id ID --figure-panel Fig1a --out-dir DIR [other metadata]`
- `scripts/summarize_extraction_table.py <cards_dir> <output_tsv>`
- `scripts/validate_figure_cards.py <cards_dir> --literature-dir literature/extracted [--output audit.md] [--strict]`

The PDF scripts require PyMuPDF (`fitz`). If it is unavailable, report the missing dependency and ask before installing packages.

## Quality Check

Before finishing any extraction task, verify:

- No copyrighted figure image, cropped panel, or full PDF has been copied into reusable skill resources.
- `validate_figure_cards.py` has been run when extracted cards are available, and any page-number or missing-render issues are resolved or explicitly documented.
- Each figure card distinguishes observed information from inferred information.
- Unknown statistics and preprocessing steps are explicitly marked.
- The biological comparison direction and input data structure are recorded.
- R and Python implementation options are listed when the plot type has reasonable support in both ecosystems.
- Nature compliance fields are filled or explicitly marked `not assessed` for Nature-family outputs.
