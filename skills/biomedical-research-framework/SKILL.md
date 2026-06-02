---
name: biomedical-research-framework
description: Use when interpreting biomedical research results, planning bioinformatics, tumor-immunology, medicinal-chemistry, or AI-method studies, building review frameworks, mapping findings to evidence, or deciding what a result can claim in papers, PPTs, or teaching materials.
version: "0.5.0"
last_updated: "2026-06-02"
status: active
data_access_level: verified_or_redacted
task_type: workflow
related_skills: [academic-chinese-style, paper-figure-extractor, nature-figure-compliance, bioinformatics-figureya-plotting]
---

# Biomedical Research Framework

## Overview

Use this skill to turn biomedical observations into defensible research claims. It does not invent mechanisms, data, citations, or clinical implications. It separates:

1. what the result shows;
2. what method produced it;
3. what interpretation is allowed;
4. what alternative explanations remain;
5. what validation is still needed.

## Workflow

1. Classify the domain: `bioinformatics`, `tumor-immunology`, `medicinal-chemistry`, `ai-methods`, or `mixed`.
2. Read only the relevant reference:
   - Domain checks: `references/domain-rules.md`
   - Result interpretation card: `references/research-interpretation-card.md`
   - Review and framework planning: `references/review-framework.md`
3. Build a research interpretation card before drafting prose or slides.
4. Map every major statement to figure, table, dataset, code, literature, passport, or user-data evidence.
5. Downgrade unsupported mechanisms or clinical claims to `partial`, `needs evidence`, or `unsupported`.
6. Hand off allowed claims to `academic-chinese-style`, `nature-language-style`, or `academic-presentation-teaching`.

## Output Contract

For result interpretation, return:

1. `研究问题`: task, cohort/model/system, and comparison.
2. `结果解释卡`: fields matching `schemas/research_interpretation_card.schema.json`.
3. `可写主张`: conservative claim text with `claim_status`.
4. `替代解释`: confounders, batch effects, assay limitations, model failures, or chemistry assay caveats.
5. `验证建议`: specific follow-up analyses or experiments.

Use `scripts/check_research_interpretation_card.py` when a JSON card is available.

## Boundaries

- A statistically significant association is not a mechanism.
- A docking pose is not binding affinity.
- A model's high AUROC is not clinical utility.
- A pathway term is not proof that the pathway is active.
- A single cohort, cell line panel, or benchmark is not broad generalization.
