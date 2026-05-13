# Local Corpus Language Profile

Source basis: deterministic extraction from `literature/extracted/` on 2026-05-13. The corpus contained 16 Nature-family full-text extractions.

## Corpus Metrics

| Metric | Value |
| --- | ---: |
| Papers processed | 16 |
| Samples recorded | 1451 |
| Sentences counted | 12398 |
| Mean sentence length | 23.0 words |
| Median sentence length | 16.0 words |
| Sentences above 30 words | 1798 |

## Frequent Move Tokens

| Token | Count | Papers |
| --- | ---: | ---: |
| `using` | 970 | 16 |
| `suggest` | 129 | 16 |
| `may` | 118 | 15 |
| `however` | 87 | 16 |
| `could` | 82 | 15 |
| `these_findings` | 48 | 12 |
| `we_identified` | 44 | 11 |
| `we_found` | 43 | 12 |
| `we_developed` | 21 | 7 |
| `here_we` | 19 | 11 |

## Extracted Style Rules

- Contribution sentences frequently use compact first-person scientific moves such as `Here we`, `we present`, `we show`, `we identified`, or `we developed`.
- Method framing often starts with `Using ...` when the method is essential to the claim.
- Interpretive claims frequently use `suggest`, `may`, and `could`; preserve this hedging unless the underlying evidence is stronger.
- Contrast moves often use `however` to isolate a gap, limitation, or exception before the present contribution.
- Results prose should keep orientation, observation, and quantitative support close together.
- Discussion prose should add interpretation, comparison, limitation, or implication rather than rephrasing the same observation.

## Limits

- PDF text extraction artifacts can affect exact wording and sentence splitting. Verify critical language against the source PDF.
- The profile summarizes style, not scientific truth. Do not transfer mechanisms, novelty, or evidence strength from corpus papers to the user's manuscript.
- Snippets generated in `figure_skills_output/language_style/local_corpus/style_samples.tsv` are short locators, not reusable prose.
