---
name: course-skill-router
description: Use when routing courseware-first teaching project tasks to lecture expansion, PPT storyboard, evidence review, research ingest, or knowledge-vault maintenance workflows.
version: "0.6.0"
last_updated: "2026-06-03"
status: active
data_access_level: verified_or_redacted
task_type: workflow
related_skills: [course-lecture-expand, course-ppt-storyboard, course-evidence-review, course-update-vault, academic-presentation-teaching, biomedical-research-framework]
---

# Course Skill Router

## Overview

Use this skill as the local entry point for courseware production projects such as AI_Course. The course truth layer comes first: syllabus, week folders, lecture scripts, outlines, and teaching materials. Knowledge pages and external sources support preparation; they do not override the course plan.

## Read First

1. `AGENTS.md`
2. `memory.md`
3. `course/weeks/_index.md`
4. Target week folder, usually `course/weeks/week_XX/`
5. Relevant `knowledge/index.md` entries after the target week is clear

## Routing Matrix

| User intent | Use workflow | Typical support |
| --- | --- | --- |
| Expand a short weekly `script.md` | `course-lecture-expand` | `academic-chinese-style`, `biomedical-research-framework` |
| Create a PPT plan, deck brief, or storyboard | `course-ppt-storyboard` | `academic-presentation-teaching`, `nature-figure-compliance` |
| Review claims, statistics, biology, visualization interpretation, or AI output | `course-evidence-review` | `biomedical-research-framework`, `academic-chinese-style` |
| Add or summarize external teaching material | `course-update-vault`, then project research/material workflow | `building-llm-wiki` if installed |
| Rebuild indexes, check links, or refresh stale retrieval | `course-update-vault` | project maintenance scripts |

## Boundaries

- `course/syllabus/` and `course/weeks/` are the course truth layer.
- `knowledge/` supports preparation, indexing, and synthesis.
- `materials/raw/` is read-only unless the user explicitly changes the project policy.
- Use standard Markdown links, not Obsidian wiki links.
- Do not put generated PPT, image previews, logs, or raw external course files into Git unless the project policy explicitly allows it.
- Medical, biological, statistical, and source claims need documented evidence or an explicit `needs evidence` marker.

## Output Contract

When routing a task, state:

1. target workflow;
2. files to read first;
3. files that may be changed;
4. validation commands to run.

Example:

```text
Workflow: course-lecture-expand
Read: course/weeks/week_15/{materials,outline,script}.md, knowledge/index.md
Write: course/weeks/week_15/script.md, docs/course_script_depth_report.md
Validate: python scripts/maintenance/course_script_depth.py
```
