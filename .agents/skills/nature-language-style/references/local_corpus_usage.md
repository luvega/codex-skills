# Local Corpus Usage

The local corpus under `literature/pdfs/` and `literature/extracted/` is used to calibrate Nature-family language style.

## Rules

- Prefer extracted `full_text.md` files when available. Use PDFs only to regenerate text or verify layout.
- Do not load every paper by default. Select relevant journals, paper types, and sections.
- Do not store long copyrighted passages in skill references or reusable outputs.
- Store short snippets only as locators for style features; keep each snippet under 20 words.
- Treat the corpus as evidence of observed style patterns, not as a source of scientific claims for the user's manuscript.
- If a corpus pattern conflicts with explicit user instructions or current journal rules, surface the conflict and choose the rule that best matches the target output.

## Recommended Extraction Command

```bash
python .agents/skills/nature-language-style/scripts/extract_language_style.py \
  --input-dir literature/extracted \
  --out-dir figure_skills_output/language_style/local_corpus
```

## Interpreting Outputs

- `language_style_profile.md`: corpus-level metrics and style patterns.
- `style_samples.tsv`: short excerpts with section guesses and trigger tokens.
- `phrase_counts.tsv`: deterministic counts for common Nature-style moves.

Use the generated profile to inform prose decisions, then use judgement to decide whether each rule fits the user's actual section and evidence.
