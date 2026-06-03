---
name: course-ppt-storyboard
description: Use when creating reviewable course PPT storyboards, slide briefs, or deck plans before generating editable PPTX files.
version: "0.6.0"
last_updated: "2026-06-03"
status: active
data_access_level: verified_or_redacted
task_type: workflow
related_skills: [course-skill-router, course-lecture-expand, course-evidence-review, academic-presentation-teaching, nature-figure-compliance]
---

# Course PPT Storyboard

## Overview

Use this skill before generating a course PPTX. The first output is a reviewable storyboard or brief, not a binary deck. This keeps teaching logic, evidence notes, visual intent, and risk boundaries inspectable before slide production.

## Inputs

1. `course/weeks/week_XX/outline.md`
2. `course/weeks/week_XX/script.md`
3. `course/weeks/week_XX/materials.md`
4. Any week review or rubric under `course/evaluation/`
5. Relevant source, concept, or synthesis pages under `knowledge/`

## Storyboard Contract

Each slide should include:

- action title: a sentence-level teaching point, not a topic label;
- visual intent: table, workflow, small dataset, schematic, code fragment, graph, or board plan;
- teacher note: what the instructor says or asks;
- student action: what students calculate, inspect, discuss, or submit;
- evidence/source note: where the content comes from;
- risk note: what must not be overclaimed.

## PPT Boundary

- Do not generate PPTX until the storyboard is reviewable.
- Do not put dense paragraphs on slides.
- Every technical figure needs source, data, or generated-example status.
- AI-generated diagrams are acceptable as teaching schematics, not as source evidence.
- Final PPTX should be visually checked through exported slide previews when deck generation is requested.

## Output Format

Prefer a Markdown table or structured brief with these fields:

```markdown
| Slide | Action title | Visual intent | Teacher note | Student action | Evidence/source | Risk note |
| --- | --- | --- | --- | --- | --- | --- |
```

## Validation

Run the normal course checks plus any PPT-specific preview export when a deck is generated:

```powershell
python scripts/maintenance/course_quality_check.py --check
python scripts/maintenance/course_km_index.py --check
```
