---
name: course-evidence-review
description: Use when reviewing course scripts, outlines, PPT storyboards, generated explanations, or biomedical teaching claims for claim-evidence alignment and overclaim risk.
version: "0.6.0"
last_updated: "2026-06-03"
status: active
data_access_level: verified_only
task_type: review
related_skills: [course-skill-router, course-lecture-expand, course-ppt-storyboard, biomedical-research-framework, academic-chinese-style]
---

# Course Evidence Review

## Overview

Use this skill to review course content before it becomes slides, lecture handouts, or student-facing material. The goal is to distinguish teaching simplification from unsupported claims.

## Review Axes

| Axis | Question |
| --- | --- |
| Course fit | Is the statement appropriate for the stated student audience and week objective? |
| Source grounding | Is the claim supported by syllabus, materials, knowledge pages, database evidence, literature, or a declared example? |
| Statistics | Are p-value, adjusted p-value, effect size, sample size, and model assumptions described correctly? |
| Biology | Are gene, pathway, cell type, mechanism, and clinical statements marked as verified or needing verification? |
| Visualization | Does graph interpretation distinguish what is shown from what is inferred? |
| AI boundary | Does the text separate AI suggestions from confirmed evidence? |

## Output Format

Use this structure:

```markdown
## Verdict

pass / revise-before-ppt / needs-source-review

## Findings

| Severity | Location | Issue | Fix |
| --- | --- | --- | --- |

## Claim-Evidence Gate

| Claim | Evidence status | Action |
| --- | --- | --- |

## Next Checks
```

## Hard Rules

- Do not accept unsupported gene function, pathway mechanism, clinical implication, or software behavior as fact.
- Do not accept causal language from a visualization, correlation, or association alone.
- Do not let `pilot_ready` mean `formal_ready`.
- When source evidence is missing, mark `needs-source-review` instead of inventing a citation.
