"""Validate sci_skills SKILL.md frontmatter metadata."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = {
    "name",
    "description",
    "version",
    "last_updated",
    "status",
    "data_access_level",
    "task_type",
    "related_skills",
}

ALLOWED_STATUS = {"active", "draft", "deprecated"}
ALLOWED_DATA_ACCESS = {"raw", "redacted", "verified_only", "verified_or_redacted"}
ALLOWED_TASK_TYPES = {"open-ended", "extraction", "coding", "review", "writing", "workflow"}


def parse_frontmatter(path: Path) -> tuple[dict[str, object], list[dict[str, str]]]:
    issues: list[dict[str, str]] = []
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, [{"code": "MISSING_FRONTMATTER", "path": str(path)}]
    try:
        _, raw, _ = text.split("---", 2)
    except ValueError:
        return {}, [{"code": "MALFORMED_FRONTMATTER", "path": str(path)}]

    metadata: dict[str, object] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") and current_key:
            metadata.setdefault(current_key, [])
            if isinstance(metadata[current_key], list):
                metadata[current_key].append(stripped[2:].strip().strip('"'))
            continue
        if ":" not in line:
            issues.append({"code": "MALFORMED_METADATA_LINE", "path": str(path), "line": line})
            continue
        key, value = line.split(":", 1)
        current_key = key.strip()
        value = value.strip()
        if value == "[]":
            metadata[current_key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            metadata[current_key] = [item.strip().strip('"') for item in inner.split(",") if item.strip()]
        else:
            metadata[current_key] = value.strip('"')
    return metadata, issues


def issue(code: str, path: Path, **extra: str) -> dict[str, str]:
    payload = {"code": code, "path": str(path)}
    payload.update(extra)
    return payload


def validate_skill(skill_dir: Path) -> tuple[dict[str, object], list[dict[str, str]]]:
    path = skill_dir / "SKILL.md"
    if not path.exists():
        return {"name": skill_dir.name, "path": str(path)}, [issue("MISSING_SKILL_MD", path)]

    metadata, issues = parse_frontmatter(path)
    missing = REQUIRED_FIELDS - set(metadata)
    for field in sorted(missing):
        issues.append(issue("MISSING_FIELD", path, field=field))

    name = str(metadata.get("name", ""))
    if name and name != skill_dir.name:
        issues.append(issue("NAME_DIRECTORY_MISMATCH", path, expected=skill_dir.name, actual=name))
    if name and not re.fullmatch(r"[a-z0-9-]+", name):
        issues.append(issue("INVALID_NAME", path, value=name))

    description = str(metadata.get("description", ""))
    if description and not description.startswith("Use when"):
        issues.append(issue("DESCRIPTION_TRIGGER_FORMAT", path))

    status = str(metadata.get("status", ""))
    if status and status not in ALLOWED_STATUS:
        issues.append(issue("INVALID_STATUS", path, value=status))

    data_access = str(metadata.get("data_access_level", ""))
    if data_access and data_access not in ALLOWED_DATA_ACCESS:
        issues.append(issue("INVALID_DATA_ACCESS_LEVEL", path, value=data_access))

    task_type = str(metadata.get("task_type", ""))
    if task_type and task_type not in ALLOWED_TASK_TYPES:
        issues.append(issue("INVALID_TASK_TYPE", path, value=task_type))

    related = metadata.get("related_skills")
    if related is not None and not isinstance(related, list):
        issues.append(issue("RELATED_SKILLS_NOT_LIST", path))

    return {"name": name or skill_dir.name, "path": str(path), "metadata": metadata}, issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skills_root", nargs="?", default="skills")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    skills_root = Path(args.skills_root)
    skills = []
    issues: list[dict[str, str]] = []
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        skill, skill_issues = validate_skill(skill_dir)
        skills.append(skill)
        issues.extend(skill_issues)

    payload = {"skills": skills, "issues": issues}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in issues:
            print(f"{item['code']}: {item['path']}")
        if not issues:
            print(f"Validated {len(skills)} skills.")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
