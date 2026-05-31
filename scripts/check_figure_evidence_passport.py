"""Validate figure evidence passport fixtures and handoff artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_LOCAL_ROOTS = (
    "literature/pdfs/",
    "literature/extracted/",
    "figure_skills_output/",
    "tmp/",
)
ALLOWED_SOURCE_STATUS = {
    "explicit in caption/text",
    "visible in page image",
    "user observation",
    "inferred",
    "not reported in PDF",
}
ALLOWED_AUDIT_STATUS = {"pass", "warning", "fail", "not_checked"}
ALLOWED_CONFIDENCE = {"exact", "strong", "weak", "no_match"}


def normalize_path(value: str) -> str:
    return value.replace("\\", "/").lstrip("./")


def add_issue(issues: list[dict[str, Any]], code: str, pointer: str, **extra: Any) -> None:
    payload = {"code": code, "pointer": pointer}
    payload.update(extra)
    issues.append(payload)


def validate_local_path(value: str, pointer: str, issues: list[dict[str, Any]]) -> None:
    normalized = normalize_path(value)
    if normalized.startswith(("http://", "https://")) or ":" in normalized[:3]:
        add_issue(issues, "NON_LOCAL_ONLY_PATH", pointer, value=value)
        return
    if not normalized.startswith(ALLOWED_LOCAL_ROOTS):
        add_issue(issues, "NON_LOCAL_ONLY_PATH", pointer, value=value)


def validate_passport(payload: dict[str, Any]) -> tuple[dict[str, int], list[dict[str, Any]]]:
    issues: list[dict[str, Any]] = []
    for field in ("schema_version", "passport_id", "source", "figure_cards", "plot_recipes", "qc_reports"):
        if field not in payload:
            add_issue(issues, "MISSING_FIELD", f"/{field}")

    source = payload.get("source", {})
    if isinstance(source, dict):
        for field in ("pdf_path", "extracted_text_path"):
            value = source.get(field)
            if not value:
                add_issue(issues, "MISSING_FIELD", f"/source/{field}")
            elif isinstance(value, str):
                validate_local_path(value, f"/source/{field}", issues)

    cards = payload.get("figure_cards", [])
    if not isinstance(cards, list):
        add_issue(issues, "INVALID_TYPE", "/figure_cards", expected="list")
        cards = []
    card_ids: set[str] = set()
    for index, card in enumerate(cards):
        pointer = f"/figure_cards/{index}"
        if not isinstance(card, dict):
            add_issue(issues, "INVALID_TYPE", pointer, expected="object")
            continue
        card_id = str(card.get("id", ""))
        if card_id:
            card_ids.add(card_id)
        for field in ("id", "card_path", "caption_excerpt", "source_status", "audit_status"):
            if not card.get(field):
                add_issue(issues, "MISSING_FIELD", f"{pointer}/{field}")
        if card.get("card_path"):
            validate_local_path(str(card["card_path"]), f"{pointer}/card_path", issues)
        if card.get("source_status") and card["source_status"] not in ALLOWED_SOURCE_STATUS:
            add_issue(issues, "INVALID_SOURCE_STATUS", f"{pointer}/source_status", value=card["source_status"])
        if card.get("audit_status") and card["audit_status"] not in ALLOWED_AUDIT_STATUS:
            add_issue(issues, "INVALID_AUDIT_STATUS", f"{pointer}/audit_status", value=card["audit_status"])
        text_evidence = card.get("text_evidence")
        if not isinstance(text_evidence, dict) or not text_evidence.get("excerpt"):
            add_issue(issues, "MISSING_TEXT_EVIDENCE", f"{pointer}/text_evidence")
        image_evidence = card.get("image_evidence")
        if not isinstance(image_evidence, dict) or not image_evidence.get("page_image") or not image_evidence.get("observed_elements"):
            add_issue(issues, "MISSING_IMAGE_EVIDENCE", f"{pointer}/image_evidence")
        elif isinstance(image_evidence.get("page_image"), str):
            validate_local_path(image_evidence["page_image"], f"{pointer}/image_evidence/page_image", issues)

    recipes = payload.get("plot_recipes", [])
    if not isinstance(recipes, list):
        add_issue(issues, "INVALID_TYPE", "/plot_recipes", expected="list")
        recipes = []
    for index, recipe in enumerate(recipes):
        pointer = f"/plot_recipes/{index}"
        if not isinstance(recipe, dict):
            add_issue(issues, "INVALID_TYPE", pointer, expected="object")
            continue
        for field in ("id", "card_id", "recipe_path", "plot_type"):
            if not recipe.get(field):
                add_issue(issues, "MISSING_FIELD", f"{pointer}/{field}")
        if recipe.get("recipe_path"):
            validate_local_path(str(recipe["recipe_path"]), f"{pointer}/recipe_path", issues)
        if recipe.get("card_id") and recipe["card_id"] not in card_ids:
            add_issue(issues, "UNKNOWN_CARD_ID", f"{pointer}/card_id", value=recipe["card_id"])
        match = recipe.get("figureya_match", {})
        if isinstance(match, dict) and match.get("confidence") not in ALLOWED_CONFIDENCE:
            add_issue(issues, "INVALID_FIGUREYA_CONFIDENCE", f"{pointer}/figureya_match/confidence")

    qc_reports = payload.get("qc_reports", [])
    if not isinstance(qc_reports, list):
        add_issue(issues, "INVALID_TYPE", "/qc_reports", expected="list")
        qc_reports = []
    for index, report in enumerate(qc_reports):
        pointer = f"/qc_reports/{index}"
        if not isinstance(report, dict):
            add_issue(issues, "INVALID_TYPE", pointer, expected="object")
            continue
        if report.get("qc_path"):
            validate_local_path(str(report["qc_path"]), f"{pointer}/qc_path", issues)
        if report.get("status") and report["status"] not in ALLOWED_AUDIT_STATUS:
            add_issue(issues, "INVALID_AUDIT_STATUS", f"{pointer}/status", value=report["status"])

    summary = {
        "cards": len(cards),
        "plot_recipes": len(recipes),
        "qc_reports": len(qc_reports),
    }
    return summary, issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("passport")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    path = Path(args.passport)
    payload = json.loads(path.read_text(encoding="utf-8"))
    summary, issues = validate_passport(payload)
    result = {"path": str(path), "summary": summary, "issues": issues}
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in issues:
            print(f"{item['code']}: {item['pointer']}")
        if not issues:
            print(f"Validated passport with {summary['cards']} card(s).")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
