---
name: nature-figure-compliance
description: Use when Codex needs to prepare, review, or QC figures and summary text against Nature research figure requirements, including main figures, Extended Data, graph styling, accessibility, export formats, editable text, image integrity, gels/blots, chemical structures, and Nature-style summary paragraphs.
---

# Nature Figure Compliance

## Overview

Check research figures, figure packages, and summary paragraphs against Nature-style requirements. This skill is for compliance and QC; it does not recreate published figures or decide scientific conclusions.

Use `paper-figure-extractor` for extracting plot grammar from papers, `nature-biofigure-coder` for generating bioinformatics plotting code, and `nature-language-style` for manuscript prose, abstract, title, and figure-legend style. Use this skill before final export, submission packaging, or figure audit.

## Required Operating Rules

Before using this skill, read and follow `references/agent_operating_rules.md`. State assumptions, surface ambiguity, keep checks surgical, let deterministic scripts handle file routing and size/format checks, checkpoint multi-step work, and report every skipped or uncertain check.

## Workflow

1. State assumptions: target journal family, figure kind (`main`, `extended-data`, `chemical-structure`, `summary-paragraph`), available source files, and whether original raw image data are available.
2. Define success criteria: required dimensions, file formats, font/editability, accessibility, data integrity, and output report.
3. Use `references/figure_contract_qc.md` when a multi-panel figure needs claim, panel hierarchy, source-data, statistics, or reviewer-risk review.
4. Use `scripts/check_nature_figure_package.py` for deterministic file checks when files are available.
5. Use `references/nature_figure_requirements.md` for human review of graph, image, text, export, accessibility, and Extended Data rules.
6. Use `references/image_integrity_rules.md` when photographic images, microscopy, gels, blots, splicing, insets, contrast changes, or raw image data are involved.
7. Use `references/chemical_structure_rules.md` when structures, reaction schemes, atom labels, arrows, stereochemistry, salts, radicals, or ChemDraw exports are involved.
8. Use `references/summary_paragraph_rules.md` for structural compliance of Nature summary paragraphs; use `nature-language-style` for corpus-derived prose style and rewriting.
9. Use `references/example_corpus_usage.md` when comparing against the example Nature papers in `literature/pdfs/`.
10. Write a QC report using `assets/nature_figure_qc_report_template.md`.

## Model vs Deterministic Work

Let deterministic code decide:

- File existence, size, extension, page dimensions, and basic DPI metadata.
- Whether a file violates a declared hard limit.
- Whether required files are missing.

Use the model for:

- Classifying figure type.
- Summarizing rule conflicts.
- Extracting issues from visual review notes.
- Explaining why a figure is difficult to read or likely non-compliant.

Do not use the model to decide retry policies, file routing, or pass/fail thresholds that can be encoded.

## Completion Criteria

Before finishing, report:

- Files checked and figure kind.
- Deterministic checks run and their result.
- Manual or visual checks performed.
- Rules that pass, warn, fail, or could not be assessed.
- Any assumptions, skipped checks, or missing raw data.
