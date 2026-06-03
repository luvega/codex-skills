# sci_skills Architecture

This repository is a Codex skill suite for biomedical figure evidence, reproducible plotting, figure compliance, manuscript-facing academic writing, domain result interpretation, academic deliverables, and courseware-first teaching workflows. The architecture keeps the skills independent, but defines shared evidence handoffs so figures, prose, reviews, PPT plans, teaching materials, lecture scripts, and course knowledge indexes can be checked without silently inventing claims.

## Workflow Stages

| Stage | Skill | Input | Output | Gate |
| --- | --- | --- | --- | --- |
| 1. Extract | `paper-figure-extractor` | Local PDF, rendered page image, caption, full text | Figure card, source locators, abstract plot grammar | No copyrighted figure reproduction; text and image evidence kept separate |
| 2. Code | `nature-biofigure-coder` | Figure card or plot recipe | R/Python plotting template, plot data contract | Statistics and grouping must come from source or user data |
| 3. Reuse | `bioinformatics-figureya-plotting` | Plot intent and user data | FigureYa module match and adapted runnable example | FigureYa is external and read-only; confidence must be visible |
| 4. QC | `nature-figure-compliance` | Figure package, export files, QC notes | Compliance report and multi-expert review | Missing raw data or image evidence must be reported |
| 5. Interpret | `biomedical-research-framework` | Result summaries, figure/table evidence, datasets, literature, passport locators | Research interpretation card, allowed claim, alternative explanations, validation plan | Observation, association, mechanism, and extrapolation must be separated |
| 6. Write | `academic-chinese-style` / `nature-language-style` | Manuscript text, figure/table evidence, passport locators, interpretation cards | Revised prose and claim-evidence map | Unsupported claims are weakened, removed, or marked `needs evidence` |
| 7. Deliver | `academic-presentation-teaching` | Interpretation cards, claim-evidence maps, figures, source notes | Review outline, PPT storyboard, lesson plan, algorithm explanation brief | Audience, evidence map, slide/lesson plan, and assessment prompts must be visible |
| 8. Courseware | `course-skill-router` / `course-lecture-expand` / `course-ppt-storyboard` / `course-evidence-review` / `course-update-vault` | Syllabus, week folders, materials, knowledge indexes, local rules | Expanded lecture script, PPT storyboard, evidence review, index/report refresh | Course truth layer comes first; lecture depth, source boundary, broken links, and stale week mapping must be checkable |

## Artifact Handoff

The first shared handoff object is the figure evidence passport. It links:

- source PDF and extracted text;
- page image and visual observation;
- figure card and caption excerpt;
- plot recipe and FigureYa match;
- QC report and manuscript-facing claims.

The schema lives at `schemas/figure_evidence_passport.schema.json`. Example fixtures live under `tests/fixtures/`. A passport may point to local-only files, but those files stay outside Git.

The second shared handoff object is the research interpretation card. It links:

- domain and method context;
- finding and evidence sources;
- conservative interpretation and allowed claim;
- alternative explanations and validation needed.

The schema lives at `schemas/research_interpretation_card.schema.json`, with deterministic checks in `scripts/check_research_interpretation_card.py`.

Academic deliverables use `academic_output_brief` objects for review outlines, PPT storyboards, lesson plans, and algorithm explanations. The schema lives at `schemas/academic_output_brief.schema.json`, with checks in `scripts/check_academic_output_brief.py`.

Courseware skills reuse the same evidence-first principle at project scale. They do not require a new database or RAG layer. Instead, they expect a repository to expose semantic folders, rule files, week indexes, standard Markdown links, and deterministic maintenance commands. The common handoff is:

- `course/weeks/week_XX/` for the active teaching product;
- `knowledge/` for supporting source notes, concepts, and synthesis;
- `materials/raw/` as a read-only source boundary when present;
- `docs/` for persistent review, depth, or maintenance reports.

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
- Domain interpretations require a method context, evidence locator, alternative explanation, and validation note.
- AI or algorithm claims require task, input/output, split, metric, baseline, failure mode, and biomedical meaning when available.
- PPT storyboards require audience, action-title slide plan, visual assets or planned visuals, and an evidence map.
- Lesson plans require learning objectives, teaching activities, discussion questions, and assessment prompts.
- Course lecture scripts require sufficient depth, student-facing activities, teacher prompts, common-misunderstanding corrections, AI-output audit notes, and assessment points.
- Course vault maintenance requires regenerated indexes, link checks, stale mapping checks, and stable repeated runs when scripts are available.
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

v0.5 borrows architecture ideas from research workflow skill projects: stage gates, material/passport-style handoff, reviewer roles, claim-evidence maps, paragraph-flow checks, scientific skill taxonomies, and academic Office/PPT workflows. Implementation in this repository is intentionally narrower: it supports biomedical figure, interpretation, writing, and academic-deliverable workflows, not a full paper-writing or Office automation orchestrator. See `docs/ATTRIBUTION.md` for source repositories, adaptation boundaries, and license notes.
