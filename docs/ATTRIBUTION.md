# Attribution And Adaptation Notes

v0.4 adapts workflow ideas from external open repositories without copying their prompt text or code wholesale.

## Imbad0202/academic-research-skills

- Repository: `https://github.com/Imbad0202/academic-research-skills`
- Ideas adapted: staged research workflow, material/passport-style handoff, integrity gates, reviewer roles, and claim/citation audit framing.
- Boundary: sci_skills implements a narrower biomedical figure and writing workflow. Do not copy its full orchestrator, agent prompts, schemas, or long reference text without checking the upstream license and attribution requirements.

## Master-cai/Research-Paper-Writing-Skills

- Repository: `https://github.com/Master-cai/Research-Paper-Writing-Skills`
- License noted during review: MIT.
- Upstream source acknowledged by that project: Peng Sitao's public research-writing notes.
- Ideas adapted: section-specific paper writing guides, mini-outline before rewriting, paragraph flow, reverse outlining, claim-evidence maps, and reviewer-facing self-review.
- Boundary: sci_skills keeps these as derived compact rules for biomedical Chinese writing. Avoid verbatim copying of external guide text unless attribution and license conditions are explicitly handled.

## SNL-UCSB/paper-writing-skill

- Repository: `https://github.com/SNL-UCSB/paper-writing-skill`
- Reviewed commit: `a7654ab`.
- License noted during review: MIT.
- Ideas adapted: project context before prose, claim-evidence alignment, section rhetorical moves, evaluation-to-claim mapping, figure specification, and result takeaway discipline.
- Boundary: sci_skills uses these as derived workflow checks for biomedical interpretation and writing. Do not copy the upstream author profile, long prompts, examples, or lab-specific voice rules wholesale.

## K-Dense-AI/scientific-agent-skills

- Repository: `https://github.com/K-Dense-AI/scientific-agent-skills`
- Reviewed commit: `9312485`.
- Repository license noted during review: MIT; individual skills may declare different licenses.
- Ideas adapted: broad scientific skill taxonomy, domain-specific routing, validation scripts, data-analysis safety gates, scientific-writing and slide-deliverable patterns.
- Boundary: sci_skills does not vendor the skill collection. Before importing any specific code, fixture, or reference text, check that item's declared license and keep attribution.

## zLanqing/codex-claude-academic-skills

- Repository: `https://github.com/zLanqing/codex-claude-academic-skills`
- Reviewed commit: `7ed6377`.
- License noted during review: MIT.
- Ideas adapted: Chinese-first academic workflow, evidence labels, Word/PPT source boundaries, academic report structure, PPT storyboard and quality-gate framing.
- Boundary: sci_skills adapts only the workflow shape. It does not inherit that project's optoelectronics domain defaults or copy its bundled Office scripts.

## Local Project Policy

- Use external repositories as design references, not as hidden source material.
- Prefer local wording, short derived rules, and deterministic checks.
- Record provenance when a future update imports substantial text, schemas, code, examples, or fixtures.

## AI_Course Courseware Workflow

- Source: local AI_Course teaching-production workflow.
- Ideas adapted: course truth layer before knowledge synthesis, week-level lecture expansion, PPT storyboard before binary deck generation, claim-evidence review for biomedical teaching content, and deterministic maintenance of indexes, links, week mapping, script depth, and skill registry.
- Boundary: the upstream `course-*` skills are generalized workflow entries. They do not include local course files, raw teaching materials, generated reports, private paths, or project-specific scripts.
