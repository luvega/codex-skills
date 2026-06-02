"""Validate academic output briefs for reviews, slides, lessons, and algorithms."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_BRIEF_TYPES = {
    "review_outline",
    "ppt_storyboard",
    "lesson_plan",
    "algorithm_explanation",
}
ALLOWED_STATUS = {"supported", "partial", "needs evidence", "unsupported"}
COMMON_REQUIRED = ("schema_version", "brief_id", "brief_type", "audience", "evidence_map")
TYPE_REQUIRED = {
    "review_outline": (
        "scope",
        "taxonomy_axes",
        "evidence_matrix",
        "controversy_map",
        "knowledge_gaps",
        "candidate_figures",
        "future_directions",
    ),
    "ppt_storyboard": ("purpose", "slide_plan", "visual_assets"),
    "lesson_plan": (
        "topic",
        "learning_objectives",
        "session_plan",
        "case_studies",
        "discussion_questions",
        "assessment_prompts",
    ),
    "algorithm_explanation": (
        "task_definition",
        "algorithm_summary",
        "inputs_outputs",
        "evaluation_plan",
        "failure_modes",
        "biomedical_meaning",
    ),
}


def add_issue(issues: list[dict[str, Any]], code: str, pointer: str, **extra: Any) -> None:
    payload = {"code": code, "pointer": pointer}
    payload.update(extra)
    issues.append(payload)


def require_non_empty_list(payload: dict[str, Any], field: str, issues: list[dict[str, Any]], code: str | None = None) -> None:
    pointer = f"/{field}"
    value = payload.get(field)
    if not isinstance(value, list):
        add_issue(issues, "INVALID_TYPE", pointer, expected="list")
    elif not value:
        add_issue(issues, code or "EMPTY_LIST", pointer)


def validate_evidence_entries(value: Any, pointer: str, issues: list[dict[str, Any]]) -> int:
    if not isinstance(value, list):
        add_issue(issues, "INVALID_TYPE", pointer, expected="list")
        return 0
    if not value:
        add_issue(issues, "EMPTY_EVIDENCE_MAP", pointer)
        return 0
    for index, item in enumerate(value):
        item_pointer = f"{pointer}/{index}"
        if not isinstance(item, dict):
            add_issue(issues, "INVALID_TYPE", item_pointer, expected="object")
            continue
        for field in ("claim", "evidence", "status"):
            if not str(item.get(field, "")).strip():
                add_issue(issues, "MISSING_FIELD", f"{item_pointer}/{field}")
        status = str(item.get("status", "")).lower()
        if status and status not in ALLOWED_STATUS:
            add_issue(issues, "INVALID_STATUS", f"{item_pointer}/status", value=item.get("status"))
        if status == "supported" and not str(item.get("evidence", "")).strip():
            add_issue(issues, "SUPPORTED_WITHOUT_EVIDENCE", item_pointer)
    return len(value)


def validate_review_outline(payload: dict[str, Any], issues: list[dict[str, Any]]) -> None:
    require_non_empty_list(payload, "taxonomy_axes", issues)
    validate_evidence_entries(payload.get("evidence_matrix"), "/evidence_matrix", issues)
    for field in ("controversy_map", "knowledge_gaps", "candidate_figures", "future_directions"):
        require_non_empty_list(payload, field, issues)


def validate_ppt_storyboard(payload: dict[str, Any], issues: list[dict[str, Any]]) -> None:
    slide_plan = payload.get("slide_plan")
    if not isinstance(slide_plan, list):
        add_issue(issues, "INVALID_TYPE", "/slide_plan", expected="list")
        return
    if not slide_plan:
        add_issue(issues, "EMPTY_SLIDE_PLAN", "/slide_plan")
        return
    for index, slide in enumerate(slide_plan):
        pointer = f"/slide_plan/{index}"
        if not isinstance(slide, dict):
            add_issue(issues, "INVALID_TYPE", pointer, expected="object")
            continue
        for field in ("action_title", "core_point", "evidence_refs"):
            if field not in slide or slide.get(field) in ("", []):
                add_issue(issues, "MISSING_FIELD", f"{pointer}/{field}")


def validate_lesson_plan(payload: dict[str, Any], issues: list[dict[str, Any]]) -> None:
    for field in ("learning_objectives", "session_plan", "case_studies", "discussion_questions", "assessment_prompts"):
        require_non_empty_list(payload, field, issues)


def validate_algorithm_explanation(payload: dict[str, Any], issues: list[dict[str, Any]]) -> None:
    inputs_outputs = payload.get("inputs_outputs")
    if not isinstance(inputs_outputs, dict):
        add_issue(issues, "INVALID_TYPE", "/inputs_outputs", expected="object")
    else:
        for field in ("inputs", "outputs"):
            if not isinstance(inputs_outputs.get(field), list) or not inputs_outputs.get(field):
                add_issue(issues, "MISSING_FIELD", f"/inputs_outputs/{field}")
    for field in ("evaluation_plan", "failure_modes"):
        require_non_empty_list(payload, field, issues)


def validate_brief(payload: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    issues: list[dict[str, Any]] = []
    for field in COMMON_REQUIRED:
        if field not in payload:
            add_issue(issues, "MISSING_FIELD", f"/{field}")
        elif field != "evidence_map" and not str(payload.get(field, "")).strip():
            add_issue(issues, "EMPTY_FIELD", f"/{field}")

    brief_type = payload.get("brief_type")
    if brief_type and brief_type not in ALLOWED_BRIEF_TYPES:
        add_issue(issues, "INVALID_BRIEF_TYPE", "/brief_type", value=brief_type)

    for field in TYPE_REQUIRED.get(str(brief_type), ()):
        if field not in payload:
            add_issue(issues, "MISSING_FIELD", f"/{field}")

    evidence_count = validate_evidence_entries(payload.get("evidence_map"), "/evidence_map", issues)

    if brief_type == "review_outline":
        validate_review_outline(payload, issues)
    elif brief_type == "ppt_storyboard":
        validate_ppt_storyboard(payload, issues)
    elif brief_type == "lesson_plan":
        validate_lesson_plan(payload, issues)
    elif brief_type == "algorithm_explanation":
        validate_algorithm_explanation(payload, issues)

    summary = {
        "brief_id": payload.get("brief_id", ""),
        "brief_type": payload.get("brief_type", ""),
        "evidence_items": evidence_count,
    }
    return summary, issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    path = Path(args.brief)
    payload = json.loads(path.read_text(encoding="utf-8"))
    summary, issues = validate_brief(payload)
    result = {"path": str(path), "summary": summary, "issues": issues}
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in issues:
            print(f"{item['code']}: {item['pointer']}")
        if not issues:
            print(f"Validated academic output brief: {summary['brief_id']}.")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
