# Example Corpus Usage

The PDFs under `literature/pdfs/` are example Nature-family articles for style calibration and figure-pattern extraction. Use them only as examples of how published figures are commonly organized.

## Rules

- Do not copy published panels, figure layouts, or visual assets into reusable outputs.
- Use `paper-figure-extractor` when extracting plot grammar or figure cards from these papers.
- Use this skill to compare candidate outputs against Nature requirements, not to imitate a specific published paper.
- If a published example conflicts with current Nature guidance, follow the current Nature guidance and record the conflict.
- Do not load every PDF by default. Select papers relevant to the figure type and stay within the token budget.

## Current Example Corpus

At creation time, `literature/pdfs/` contained Nature-family examples spanning Nature, Nature Methods, Nature Genetics, Nature Cancer, Nature Cell Biology, and Nature Communications. Treat this as a changing local corpus rather than a fixed bundled dependency.
