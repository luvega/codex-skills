# Figure Package Reviewer Mode

Use this mode when a figure package needs simulated multi-expert review before submission or internal release.

Fixed reviewer roles:

1. Figure compliance reviewer: dimensions, typography, export format, editability, accessibility, and Nature-family constraints.
2. Bioinformatics methods reviewer: statistical tests, grouping variables, transformations, plot type, factor order, and reproducibility.
3. Evidence-chain reviewer: whether every visual and textual claim maps to a card, source locator, figure evidence passport, or user-provided evidence.
4. Reproducibility reviewer: scripts, dependencies, input/output tables, random seeds, and local-only data boundaries.
5. Chinese paper-writing reviewer: section role, claim-evidence alignment, paragraph flow, restrained wording, and terminology consistency.
6. Devil's Advocate: the strongest reviewer objection likely to survive a normal self-review.

Output contract:

- Overall readiness: `ready`, `minor revision`, `major revision`, or `not ready`.
- Findings grouped as P0/P1/P2.
- For each finding: role, evidence, risk, recommended revision.
- Explicitly list checks that could not be performed because raw data, page images, source text, or scripts were missing.

Do not invent visual observations. If image evidence is unavailable, mark the relevant finding as unverified.
