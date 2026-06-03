---
name: course-update-vault
description: Use when maintaining course project indexes, skill registries, links, week mapping, script depth reports, or courseware quality gates after meaningful content changes.
version: "0.6.0"
last_updated: "2026-06-03"
status: active
data_access_level: verified_or_redacted
task_type: workflow
related_skills: [course-skill-router, course-lecture-expand, course-ppt-storyboard, course-evidence-review, academic-presentation-teaching]
---

# Course Update Vault

## Overview

Use this skill after meaningful ingest, courseware drafting, skill loading, folder moves, refactors, or stale retrieval. It applies the AI-native knowledge-management pattern to a courseware project: directory semantics, rule files, indexes, standard workflow entry points, and deterministic checks.

## Maintenance Scope

- Rebuild generated indexes.
- Check standard Markdown links.
- Check stale week mapping or historical topic drift.
- Check sample-week quality markers.
- Check lecture script depth.
- Check local and global skill registry.
- Write reports under `docs/` when the result should persist.

## Typical Commands

Use project-specific commands when available. For AI_Course-style repositories:

```powershell
python scripts/maintenance/course_km_index.py --write
python scripts/maintenance/course_km_index.py --check
python scripts/maintenance/course_quality_check.py --check
python scripts/maintenance/course_script_depth.py --write docs/course_script_depth_report.md
python scripts/maintenance/course_skill_inventory.py --check
python -m pytest -q
```

## Boundaries

- Maintenance reports problems; it does not create new scientific claims.
- Do not move or delete `materials/raw/` unless the user explicitly asks.
- Do not use Obsidian wiki links unless the project policy requires them.
- Do not push or change remote visibility without explicit user confirmation.

## Completion

Report:

1. commands run;
2. generated or updated index/report files;
3. remaining stale links, missing summaries, or weak evidence markers;
4. whether repeated checks are stable.
