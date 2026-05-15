# Codex Skills

Personal Codex skills collected in one repository for easier reuse across machines.

## Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/
    references/
    scripts/
```

Each skill is self-contained under `skills/<skill-name>/` so it can be installed independently.

## Included Skills

| Skill | Purpose |
| --- | --- |
| `bioinformatics-figureya-plotting` | Find and adapt FigureYa biomedical plotting modules for publication-ready bioinformatics figures. |

## Install

Install one skill:

```powershell
python $env:CODEX_HOME\skills\.system\skill-installer\scripts\install-skill-from-github.py --repo luvega/codex-skills --path skills/bioinformatics-figureya-plotting
```

If `CODEX_HOME` is not set, use the default Codex home:

```powershell
python $HOME\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --repo luvega/codex-skills --path skills/bioinformatics-figureya-plotting
```

Restart Codex after installing new skills.

## Add New Skills

1. Create a new directory under `skills/<skill-name>/`.
2. Keep each skill self-contained: required `SKILL.md`, optional `agents/`, `references/`, `scripts/`, and `assets/`.
3. Keep repo-level files generic; put skill-specific documentation inside the skill folder.
4. Validate the skill before publishing:

```powershell
python $env:CODEX_HOME\skills\.system\skill-creator\scripts\quick_validate.py skills\<skill-name>
```
