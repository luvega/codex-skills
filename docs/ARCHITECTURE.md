# sci_skills Architecture

This repository is a Codex skill suite for biomedical figure evidence, reproducible plotting, figure compliance, and manuscript-facing academic writing. The v0.4 architecture keeps the skills independent, but defines a shared evidence workflow so outputs can be reviewed and reused without silently inventing claims.

## Workflow Stages

| Stage | Skill | Input | Output | Gate |
| --- | --- | --- | --- | --- |
| 1. Extract | `paper-figure-extractor` | Local PDF, rendered page image, caption, full text | Figure card, source locators, abstract plot grammar | No copyrighted figure reproduction; text and image evidence kept separate |
| 2. Code | `nature-biofigure-coder` | Figure card or plot recipe | R/Python plotting template, plot data contract | Statistics and grouping must come from source or user data |
| 3. Reuse | `bioinformatics-figureya-plotting` | Plot intent and user data | FigureYa module match and adapted runnable example | FigureYa is external and read-only; confidence must be visible |
| 4. QC | `nature-figure-compliance` | Figure package, export files, QC notes | Compliance report and multi-expert review | Missing raw data or image evidence must be reported |
| 5. Write | `academic-chinese-style` / `nature-language-style` | Manuscript text, figure/table evidence, passport locators | Revised prose and claim-evidence map | Unsupported claims are weakened, removed, or marked `needs evidence` |

## Artifact Handoff

The shared handoff object is the figure evidence passport. It links:

- source PDF and extracted text;
- page image and visual observation;
- figure card and caption excerpt;
- plot recipe and FigureYa match;
- QC report and manuscript-facing claims.

The schema lives at `schemas/figure_evidence_passport.schema.json`. Example fixtures live under `tests/fixtures/`. A passport may point to local-only files, but those files stay outside Git.

## Data Access Levels

Each skill declares a `data_access_level` in `SKILL.md` frontmatter:

- `raw`: may inspect source PDFs, extracted text, or page images.
- `verified_or_redacted`: works from checked cards, recipes, or user-provided data tables.
- `verified_only`: reviews declared artifacts and evidence, not raw copyrighted sources by default.
- `redacted`: revises manuscript text and style using supplied evidence and locators.

`scripts/check_skill_metadata.py` enforces the frontmatter fields and accepted enum values.

## Quality Gates

- Visual claims require `image_evidence`.
- Textual or biological claims require `text_evidence`, figure/table evidence, literature evidence, or a passport locator.
- Abstract and Introduction claims must be represented in a claim-evidence map.
- Unsupported claims must be downgraded to `partial`, `needs evidence`, or `unsupported`.
- Generated figures must include editable exports, plot data, and a QC note when files are available.

## Local-Only Boundary

The following directories are working data and are ignored by Git:

- `literature/`
- `figure_skills_output/`
- `tmp/`

Do not commit published PDFs, rendered page images, extracted full text, copied panels, or bulk generated figures. Commit only reusable rules, schemas, tests, templates, and small redacted fixtures.

## External Inspirations

v0.4 borrows architecture ideas from research workflow skill projects: stage gates, material/passport-style handoff, reviewer roles, claim-evidence maps, and paragraph-flow checks. Implementation in this repository is intentionally narrower: it supports biomedical figure and writing workflows, not a full paper-writing orchestrator. See `docs/ATTRIBUTION.md` for source repositories, adaptation boundaries, and license notes.
