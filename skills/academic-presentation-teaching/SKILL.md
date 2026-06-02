---
name: academic-presentation-teaching
description: Use when creating or reviewing academic presentations, group-meeting PPT plans, paper-reading slides, course decks, lesson plans, speaker notes, teaching cases, or storyboard briefs for biomedical, bioinformatics, medicinal-chemistry, or AI research topics.
version: "0.5.0"
last_updated: "2026-06-02"
status: active
data_access_level: verified_or_redacted
task_type: workflow
related_skills: [biomedical-research-framework, academic-chinese-style, nature-figure-compliance]
---

# Academic Presentation Teaching

## Overview

Use this skill to convert verified research material into presentation or teaching plans. Default output is a structured brief, storyboard, or lesson plan. Do not generate binary `.pptx` unless the user explicitly asks for an editable deck workflow.

## Workflow

1. Identify output type: `review_outline`, `ppt_storyboard`, `lesson_plan`, or `algorithm_explanation`.
2. Read the relevant reference:
   - PPT/storyboard: `references/ppt-storyboard.md`
   - Teaching plan: `references/lesson-plan.md`
   - Algorithm explanation: `references/algorithm-explanation.md`
3. Define audience, duration, source material, and evidence map.
4. Use action titles: each slide or lesson section states a conclusion or learning action.
5. Route scientific claims through `biomedical-research-framework` when interpretation risk is high.
6. Validate JSON briefs with `scripts/check_academic_output_brief.py` when available.

## Quality Rules

- One slide or lesson segment carries one core point.
- Figures, tables, formulas, and examples carry the technical argument.
- Long prose belongs in speaker notes, not slide bodies.
- Quantitative claims need evidence locators.
- Teaching plans need learning objectives and assessment prompts.
- Keep Chinese explanation natural; preserve English terms, formulas, gene/drug/model names, software commands, and citations.

## Completion

Report the output type, audience assumptions, evidence sources used, unsupported claims, and any checks performed.
