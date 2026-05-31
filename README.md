# sci_skills

`sci_skills` is a local Codex skills workspace for biomedical figure extraction, Nature-style figure QC, Nature-language support, and reproducible bioinformatics figure generation.

The repository tracks reusable skill instructions, deterministic helper scripts, schemas, references, and tests. Source PDFs, extracted paper text/cards/pages, and generated figure outputs are local working data and are intentionally excluded from Git.

## Skills

- `paper-figure-extractor`: extracts source-grounded figure cards and plot grammar from biomedical papers.
- `nature-biofigure-coder`: turns figure cards or plot recipes into R/Python plotting templates.
- `nature-figure-compliance`: checks figure packages against Nature-family requirements.
- `nature-language-style`: extracts and applies Nature-family manuscript language style.

## Local Data Boundaries

Tracked in Git:

- `.agents/skills/**`
- `.agents/references/**`
- `tests/**`
- `literature/manifest/paper_manifest.tsv`
- `README.md`, `requirements.txt`, `VERSION`

Local-only by design:

- `literature/pdfs/*.pdf`
- `literature/extracted/**`
- `figure_skills_output/**`
- `tmp/**`

Do not commit published PDFs, rendered page images, extracted article text, copied figure panels, or bulk generated outputs. Reusable skill assets should store abstract plot grammar, short source locators, and schema-backed metadata only.

## Setup

Use Python 3.10 or newer.

```powershell
python -m pip install -r requirements.txt
```

`PyMuPDF` is required for PDF text extraction and page rendering. The unit tests only use the Python standard library.

## Verification

Run the test suite:

```powershell
python -m unittest discover -s tests -v
```

Check whitespace in tracked diffs:

```powershell
git diff --check
```

Audit one paper's figure cards:

```powershell
python .agents\skills\paper-figure-extractor\scripts\validate_figure_cards.py `
  literature\extracted\YOUR_PAPER_ID\cards `
  --literature-dir literature\extracted `
  --strict
```

Render PDF pages for visual inspection:

```powershell
python .agents\skills\paper-figure-extractor\scripts\extract_pdf_pages.py `
  literature\pdfs\YOUR_PAPER.pdf `
  literature\extracted\YOUR_PAPER_ID\pages
```

## FigureYa Backend

FigureYa is treated as an external read-only R template backend. Do not copy FigureYa modules into this repository. Match plot recipes to a local FigureYa checkout with:

```powershell
python .agents\skills\nature-biofigure-coder\scripts\figureya_module_audit.py match `
  figure_skills_output\plot_recipes `
  --repo YOUR_FIGUREYA_REPO `
  --out tmp\figureya_recipe_matches.tsv `
  --markdown tmp\figureya_recipe_matches.md
```

On this workstation, the local FigureYa checkout may be `F:\FigureYa`; keep that as a command argument or local note, not as a hard-coded skill rule.

## Current Validation Baseline

As of the v0.3 remediation pass:

- all local PDF page renders are kept under `literature/extracted/**/pages/`;
- the existing 24 local figure cards include `text_evidence`, `image_evidence`, and `audit_status`;
- `validate_figure_cards.py` reports `MISSING_REQUIRED_FIELD` when evidence fields are absent;
- FigureYa recipe matching reports `top_confidence` so heuristic matches are not treated as guaranteed module choices.
