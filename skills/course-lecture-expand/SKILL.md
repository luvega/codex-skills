---
name: course-lecture-expand
description: Use when expanding short weekly course scripts from scaffold or placeholder notes into teacher-usable lecture notes with classroom activities, evidence boundaries, and assessment prompts.
version: "0.6.0"
last_updated: "2026-06-03"
status: active
data_access_level: verified_or_redacted
task_type: writing
related_skills: [course-skill-router, course-evidence-review, academic-chinese-style, academic-presentation-teaching, biomedical-research-framework]
---

# Course Lecture Expand

## Overview

Use this skill when a weekly `course/weeks/week_XX/script.md` is too short, only repeats a slide outline, or lacks concrete teaching moves. The target is a teacher-usable lecture script, not a bullet summary.

## Inputs

Read in this order when the project has these files:

1. `course/weeks/week_XX/materials.md`
2. `course/weeks/week_XX/outline.md`
3. `course/weeks/week_XX/script.md`
4. `course/evaluation/lecture_script_standard.md`
5. Relevant `knowledge/` pages named by the week materials
6. `course/syllabus/` files for course-level continuity

## Target Depth

| Level | CJK chars | Status |
| --- | ---: | --- |
| scaffold | 800-1500 | Not enough for PPT production |
| pilot-script | 3500-5500 | Good target for first usable lecture draft |
| full-lecture | 6500-9000 | Later formal teaching handout |

## Required Structure

Each expanded `script.md` should include:

- direct teacher-facing opening;
- why this topic matters for the course audience;
- core concept explanations in complete paragraphs;
- one small classroom dataset, table, graph-reading task, code-reading task, or case prompt;
- teacher questions, expected student answers, follow-up questions, and corrections;
- AI collaboration prompt and AI output audit checklist;
- common misunderstandings;
- board, slide, or pacing notes;
- closing transition to the next week;
- post-class exercise and scoring points.

## Writing Rules

- Match the students' background; do not assume advanced programming, statistics, or domain knowledge unless the course has already taught it.
- Keep standard English technical terms when they are the normal classroom term, such as `DESeq2`, `log2FoldChange`, `padj`, `UMAP`, `metadata`, or `count matrix`.
- Do not invent biological facts, software behavior, database claims, or source conclusions.
- If a claim needs database or literature review, mark it as `needs evidence`.
- Write in teaching language that can be read aloud.
- Do not paste long external source text.

## Validation

Run the project checks when available. For AI_Course-style repositories, typical commands are:

```powershell
python scripts/maintenance/course_script_depth.py --write docs/course_script_depth_report.md
python scripts/maintenance/course_quality_check.py --check
python scripts/maintenance/course_km_index.py --check
```
