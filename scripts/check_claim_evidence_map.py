"""Check claim-evidence maps and lightweight paragraph-flow issues."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ALLOWED_STATUS = {"supported", "partial", "needs evidence", "unsupported"}
VAGUE_PHRASES = (
    "重要意义",
    "广泛关注",
    "很好",
    "很多",
    "突破性",
    "革命性",
    "完全不同",
)


def add_issue(issues: list[dict[str, Any]], code: str, pointer: str, **extra: Any) -> None:
    payload = {"code": code, "pointer": pointer}
    payload.update(extra)
    issues.append(payload)


def parse_claim_line(line: str) -> dict[str, str] | None:
    line = line.lstrip("\ufeff")
    if "Claim:" not in line or "Evidence:" not in line or "Status:" not in line:
        return None
    parts = [part.strip() for part in line.split("|")]
    parsed: dict[str, str] = {}
    for part in parts:
        if ":" not in part:
            continue
        key, value = part.split(":", 1)
        parsed[key.strip().lower()] = value.strip()
    if {"claim", "evidence", "status"} <= set(parsed):
        return parsed
    return None


def check_paragraph_flow(text: str, issues: list[dict[str, Any]]) -> None:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    for index, paragraph in enumerate(paragraphs):
        if paragraph.startswith("#") or "Claim:" in paragraph:
            continue
        sentence_count = len([item for item in re.split(r"[。！？.!?]", paragraph) if item.strip()])
        vague_hits = [phrase for phrase in VAGUE_PHRASES if phrase in paragraph]
        if sentence_count >= 3 and vague_hits:
            add_issue(
                issues,
                "WEAK_PARAGRAPH_FLOW",
                f"/paragraphs/{index}",
                reason="paragraph mixes multiple messages or uses vague reviewer-facing claims",
                phrases=vague_hits,
            )


def validate_text(text: str) -> tuple[dict[str, int], list[dict[str, Any]]]:
    issues: list[dict[str, Any]] = []
    claims = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        parsed = parse_claim_line(line)
        if not parsed:
            continue
        claims.append(parsed)
        pointer = f"/claims/{len(claims) - 1}"
        if not parsed["claim"]:
            add_issue(issues, "EMPTY_CLAIM", pointer, line=line_number)
        if not parsed["evidence"]:
            add_issue(issues, "EMPTY_EVIDENCE", pointer, line=line_number)
        status = parsed["status"].lower()
        if status not in ALLOWED_STATUS:
            add_issue(issues, "INVALID_STATUS", pointer, line=line_number, value=parsed["status"])
        if status == "supported" and not parsed["evidence"]:
            add_issue(issues, "SUPPORTED_WITHOUT_EVIDENCE", pointer, line=line_number)

    check_paragraph_flow(text, issues)
    return {"claims": len(claims)}, issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("text_file")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    path = Path(args.text_file)
    summary, issues = validate_text(path.read_text(encoding="utf-8"))
    payload = {"path": str(path), "summary": summary, "issues": issues}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in issues:
            print(f"{item['code']}: {item['pointer']}")
        if not issues:
            print(f"Validated {summary['claims']} claim(s).")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
