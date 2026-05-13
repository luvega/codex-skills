---
name: nature-language-style
description: Use when Codex needs to extract, summarize, polish, or apply Nature-family academic language style from local PDFs, full_text.md files, abstracts, titles, figure legends, summary paragraphs, or Chinese/English manuscript drafts. Trigger for Nature-style prose, section moves, hedging, overclaim checks, title or abstract rewriting, and corpus-derived language tokens.
---

# Nature Language Style

## Overview

Extract and apply Nature-family academic prose rules from local papers without inventing claims, data, references, or novelty. Use this skill for language, not for figure geometry or plotting code.

## Required Operating Rules

Before using this skill, read and follow `../../references/agent_operating_rules.md`. State assumptions, keep edits surgical, use deterministic scripts for text extraction and metrics, use the model only for classification, summary, polishing, and overclaim judgement, and report skipped or uncertain checks.

## Source Boundaries

- Use local PDFs or extracted `full_text.md` files as a style corpus, not as text to copy.
- Store only short locator snippets and derived rules. Do not copy long abstract, caption, or paragraph text into reusable skill references.
- Preserve source grounding when revising text: record section, paper ID, page, or source block when available.
- If the user asks to translate an entire paper or build a bilingual reader, use a reader workflow instead of this style skill.
- If the user asks for figure cards or plot recipes, use `paper-figure-extractor`.
- If the user asks for plotting code, use `nature-biofigure-coder`.
- If the user asks for final figure/package compliance, use `nature-figure-compliance`.

## Workflow

1. Define the language task: `extract-style`, `polish`, `translate-polish`, `title`, `abstract`, `summary-paragraph`, `figure-legend`, `results`, `discussion`, or `methods`.
2. State the document type and section. Do not use one writing logic for all sections.
3. For corpus extraction, run `scripts/extract_language_style.py` on `literature/extracted/` or a selected paper subset.
4. Read `references/local_corpus_usage.md` and the generated corpus profile before applying local style tokens.
5. Read `references/nature_language_guardrails.md` for section moves, sentence rules, hedging, and integrity checks.
6. For summary paragraphs, also read `../nature-figure-compliance/references/summary_paragraph_rules.md`.
7. Before rewriting, diagnose the main failure mode: weak argument, wrong section logic, claim without evidence, evidence without claim, missing boundary, overclaim, or sentence clutter.
8. Rewrite only the requested text. Preserve data, statistics, gene names, model names, citations, units, and comparison direction.
9. Report revision notes and any claims that require author verification.

## Language Rules

- Language serves the scientific argument. Fix section logic before sentence polish.
- Results state what was observed, under which condition, and with what quantitative support.
- Discussion explains what the results may mean, how they compare with prior work, and where the interpretation may fail.
- Abstracts move from context to gap, approach, key result, and implication.
- Titles should be searchable, specific, restrained, and defensible.
- Prefer precise hedging over inflated certainty: `show`, `suggest`, `may reflect`, `is consistent with`.
- Flag unsupported `first`, `novel`, `prove`, `conclusively`, `unprecedented`, `best`, and broad causality claims.
- Aim for clear sentences in the 10-30 word range. Split sentences that carry more than one main proposition.
- Use British English when targeting Nature-style prose unless the user requests another house style.
- Avoid polishing text into confidence when the evidence is incomplete.

## Outputs

For corpus extraction, write:

- `language_style_profile.md`
- `style_samples.tsv`
- `phrase_counts.tsv`

For prose revision, return:

1. Revised text as plain prose.
2. `Revision notes:` with the major structural and stylistic changes.
3. `Author checks:` for claims, numbers, citations, or terminology needing verification.

## References

- `references/nature_language_guardrails.md`: section moves, hedging, sentence control, overclaim checks.
- `references/local_corpus_usage.md`: how to use local Nature PDFs safely.
- `references/local_corpus_language_profile.md`: distilled rules from the current local Nature-family PDF corpus.
- `references/language_style_schema.yml`: fields for extracted language-style records.

## Scripts

- `scripts/extract_language_style.py --input-dir literature/extracted --out-dir figure_skills_output/language_style/local_corpus`

The script extracts short snippets, metrics, and phrase counts. It does not decide whether a rewrite is scientifically valid.
