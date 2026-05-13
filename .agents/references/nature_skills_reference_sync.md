# Nature Skills Reference Sync

Source basis: `https://github.com/Yuan1z0825/nature-skills`, checked on 2026-05-13.

## Adopted Patterns

- Keep Nature work split by task: figure extraction, figure code generation, figure compliance, and language style.
- Start final figure generation from a figure contract: core conclusion, evidence hierarchy, panel map, export target, statistics, source data, and reviewer risk.
- Keep source grounding explicit for paper-derived work. Use page, block, figure, table, and caption anchors instead of copying long source text.
- Treat language polishing as section-aware: title, abstract, introduction, results, discussion, methods, figure legend, and summary paragraph each have different jobs.
- Use deterministic scripts for extraction, metrics, file checks, dimensions, and output routing. Use the model for classification, summarization, polishing, and judgement.

## Local Conflict Resolution

The referenced `nature-figure` skill enforces a single plotting backend after selection. This project keeps a different default for bioinformatics templates:

- Exploratory recipe generation may produce both R and Python when the user asks for both.
- Final submission figures, selected-backend tasks, and visual QA should use one backend consistently.
- Missing runtime or package support must be reported instead of silently switching backend.

## Not Adopted

- Do not copy upstream README files into local skills.
- Do not copy published prose or figure content as reusable examples.
- Do not expose private local paths or provenance unless the user explicitly asks for an audit trail.
