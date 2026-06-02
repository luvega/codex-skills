---
name: academic-chinese-style
description: Use when revising Chinese biomedical, bioinformatics, literature-review, grant, or manuscript prose for restrained academic style, section logic, overclaim control, citation safety, terminology consistency, and EndNote/Zotero provenance preservation.
version: "0.5.0"
last_updated: "2026-06-02"
status: active
data_access_level: redacted
task_type: writing
related_skills: [nature-language-style, paper-figure-extractor, nature-figure-compliance, biomedical-research-framework, academic-presentation-teaching]
---

# Academic Chinese Style

## Overview

Use this skill to revise Chinese biomedical and bioinformatics prose without changing the science. The priority order is:

1. Clarify the paper story and section role.
2. Align major claims with evidence.
3. Improve paragraph flow and terminology consistency.
4. Polish sentence-level style only after the argument is stable.

Core rule: improve language, not evidence. If a claim is not supported by the supplied manuscript, figure, table, citation, or figure evidence passport, weaken it, remove it, or mark it as `needs evidence`.

## Source Boundaries

- Preserve facts, numbers, statistics, units, gene/protein/drug names, model names, dataset names, citation tokens, BibTeX keys, Zotero keys, EndNote source names, file paths, and provenance labels.
- Do not add mechanisms, sample sizes, P values, software versions, clinical implications, causal links, novelty claims, or literature conclusions that are not present in the source material.
- Local PDFs, `full_text.md`, and figure cards can calibrate style and evidence boundaries. They are not automatic sources for new scientific facts.
- Do not copy long source paragraphs, abstracts, or captions into reusable skill notes. Keep derived rules, short locators, and claim-evidence maps instead.

## Paper Writing Workflow

1. Build a mini-outline before rewriting: section goal, paragraph roles, main claim, evidence source, and unresolved gaps.
2. Revise one paragraph around one message. The first sentence should state the paragraph function.
3. Run reverse outlining after each section: thesis, topic sentences, evidence under each topic sentence, and whether each paragraph maps back to the thesis.
4. Check every major claim in Abstract and Introduction against experiments, figures/tables, literature, or a figure evidence passport.
5. Finish with a reviewer-facing self-review: contribution, clarity, experimental strength, evaluation completeness, and method soundness.

## Section Guides

Load only the reference needed for the current writing target:

- Abstract: `references/paper-writing-abstract.md`
- Introduction: `references/paper-writing-introduction.md`
- Related Work: `references/paper-writing-related-work.md`
- Method: `references/paper-writing-method.md`
- Experiments: `references/paper-writing-experiments.md`
- Conclusion: `references/paper-writing-conclusion.md`
- Review writing: `references/review-writing-framework.md`
- Results and discussion interpretation: `references/results-discussion-interpretation.md`
- Algorithm explanation: `references/algorithm-explanation-writing.md`
- Domain expression rules: `references/domain-expression-rules.md`
- Paragraph flow: `references/paragraph-flow.md`
- Claim-evidence gate: `references/claim-evidence-gate.md`
- Submission self-review: `references/paper-self-review.md`

## Output Contract

For section drafting or revision, return:

1. `章节小纲`: 3-7 bullets describing paragraph roles.
2. `改写稿`: revised Chinese prose with stable terminology and evidence boundaries.
3. `Claim-Evidence Map`: one line per major claim using `Claim: ... | Evidence: ... | Status: supported/partial/needs evidence/unsupported`.
4. `自审问题`: unresolved reviewer-facing risks, not generic praise.

For short polishing tasks, return the revised paragraph, 2-4 concrete edit notes, and `需作者确认` only for scientific, citation, terminology, or provenance risks.

## Attribution

This skill adapts general paper-writing practices from open research-writing skill repositories and local sci_skills review work. The writing logic is a derived, compact workflow; do not copy external reference text verbatim unless license and attribution requirements are explicitly satisfied.
