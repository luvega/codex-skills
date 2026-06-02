"""Validate biomedical research interpretation cards."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_DOMAINS = {
    "bioinformatics",
    "tumor-immunology",
    "medicinal-chemistry",
    "ai-methods",
    "mixed",
}
ALLOWED_STATUS = {"supported", "partial", "needs evidence", "unsupported"}
ALLOWED_EVIDENCE_TYPES = {
    "figure",
    "table",
    "text",
    "dataset",
    "code",
    "literature",
    "passport",
    "user_data",
}
REQUIRED_FIELDS = (
    "schema_version",
    "card_id",
    "domain",
    "finding",
    "method_context",
    "evidence_sources",
    "interpretation",
    "alternative_explanations",
    "validation_needed",
    "allowed_claim",
    "claim_status",
)


def add_issue(issues: list[dict[str, Any]], code: str, pointer: str, **extra: Any) -> None:
    payload = {"code": code, "pointer": pointer}
    payload.update(extra)
    issues.append(payload)


def has_locator(evidence_sources: list[Any]) -> bool:
    for item in evidence_sources:
        if isinstance(item, dict) and str(item.get("locator", "")).strip():
            return True
    return False


def validate_evidence_sources(value: Any, issues: list[dict[str, Any]]) -> list[Any]:
    if not isinstance(value, list):
        add_issue(issues, "INVALID_TYPE", "/evidence_sources", expected="list")
        return []
    if not value:
        add_issue(issues, "EMPTY_EVIDENCE_SOURCES", "/evidence_sources")
    for index, item in enumerate(value):
        pointer = f"/evidence_sources/{index}"
        if not isinstance(item, dict):
            add_issue(issues, "INVALID_TYPE", pointer, expected="object")
            continue
        evidence_type = item.get("type")
        if not evidence_type:
            add_issue(issues, "MISSING_FIELD", f"{pointer}/type")
        elif evidence_type not in ALLOWED_EVIDENCE_TYPES:
            add_issue(issues, "INVALID_EVIDENCE_TYPE", f"{pointer}/type", value=evidence_type)
        if not str(item.get("locator", "")).strip():
            add_issue(issues, "MISSING_EVIDENCE_LOCATOR", f"{pointer}/locator")
        if not str(item.get("summary", "")).strip():
            add_issue(issues, "MISSING_FIELD", f"{pointer}/summary")
    return value


def validate_non_empty_list(payload: dict[str, Any], field: str, issues: list[dict[str, Any]]) -> None:
    value = payload.get(field)
    pointer = f"/{field}"
    if not isinstance(value, list):
        add_issue(issues, "INVALID_TYPE", pointer, expected="list")
    elif not value:
        code = "EMPTY_VALIDATION_NEEDED" if field == "validation_needed" else "EMPTY_LIST"
        add_issue(issues, code, pointer)


def validate_card(payload: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    issues: list[dict[str, Any]] = []
    for field in REQUIRED_FIELDS:
        if field not in payload:
            add_issue(issues, "MISSING_FIELD", f"/{field}")

    domain = payload.get("domain")
    if domain and domain not in ALLOWED_DOMAINS:
        add_issue(issues, "INVALID_DOMAIN", "/domain", value=domain)

    status = str(payload.get("claim_status", "")).lower()
    if status and status not in ALLOWED_STATUS:
        add_issue(issues, "INVALID_CLAIM_STATUS", "/claim_status", value=payload.get("claim_status"))

    method_context = payload.get("method_context")
    if method_context is not None and not isinstance(method_context, dict):
        add_issue(issues, "INVALID_TYPE", "/method_context", expected="object")

    evidence_sources = validate_evidence_sources(payload.get("evidence_sources"), issues)
    if status == "supported" and not has_locator(evidence_sources):
        add_issue(issues, "SUPPORTED_WITHOUT_EVIDENCE_LOCATOR", "/evidence_sources")
    if status in {"supported", "partial"} and not evidence_sources:
        add_issue(issues, "CLAIM_WITHOUT_EVIDENCE", "/evidence_sources", status=status)

    for field in ("finding", "interpretation", "allowed_claim"):
        if field in payload and not str(payload.get(field, "")).strip():
            add_issue(issues, "EMPTY_FIELD", f"/{field}")

    validate_non_empty_list(payload, "alternative_explanations", issues)
    validate_non_empty_list(payload, "validation_needed", issues)

    summary = {
        "card_id": payload.get("card_id", ""),
        "domain": payload.get("domain", ""),
        "claim_status": payload.get("claim_status", ""),
        "evidence_sources": len(evidence_sources),
    }
    return summary, issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("card")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    path = Path(args.card)
    payload = json.loads(path.read_text(encoding="utf-8"))
    summary, issues = validate_card(payload)
    result = {"path": str(path), "summary": summary, "issues": issues}
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in issues:
            print(f"{item['code']}: {item['pointer']}")
        if not issues:
            print(f"Validated research interpretation card: {summary['card_id']}.")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
