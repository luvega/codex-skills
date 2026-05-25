#!/usr/bin/env python
"""Audit figure extraction cards against extracted PDF text and page renders."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple


FIELD_RE = re.compile(r"^([A-Za-z0-9_][A-Za-z0-9_ ]*):\s*(.*)$")
PAGE_RE = re.compile(r"^## Page (\d+)\s*$", re.MULTILINE)
FIGURE_PANEL_RE = re.compile(r"(Extended\s*Data\s*Fig|ExtendedDataFig|Fig|Figure)[_.\s-]*(\d+)", re.I)

CANONICAL_SOURCE_STATUS_VALUES = {
    "explicit in caption/text",
    "visible in page image",
    "user observation",
    "inferred",
    "not reported in PDF",
}

IMAGE_REQUIRED_VALUES = {"visible in page image"}
EMPTY_VALUES = {"", "not assessed", "not reported in PDF", "not applicable"}


class FieldValue(NamedTuple):
    key: str
    value: str
    line_number: int
    section: str


class ParsedCard(NamedTuple):
    path: Path
    fields: dict[str, str]
    field_values: list[FieldValue]


class Issue(NamedTuple):
    card_path: Path
    code: str
    severity: str
    message: str
    suggestion: str = ""


class AuditResult(NamedTuple):
    card_count: int
    issue_count: int
    issues: list[Issue]


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def parse_card(path: Path) -> ParsedCard:
    fields: dict[str, str] = {}
    field_values: list[FieldValue] = []
    section = ""

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("## "):
            section = stripped.lstrip("#").strip()
            continue
        match = FIELD_RE.match(stripped)
        if not match:
            continue
        key, value = match.groups()
        key = key.strip()
        value = value.strip()
        fields.setdefault(key, value)
        field_values.append(FieldValue(key=key, value=value, line_number=line_number, section=section))

    return ParsedCard(path=path, fields=fields, field_values=field_values)


def parse_page_markdown(markdown: str) -> dict[int, str]:
    matches = list(PAGE_RE.finditer(markdown))
    pages: dict[int, str] = {}

    for index, match in enumerate(matches):
        page_number = int(match.group(1))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        pages[page_number] = markdown[start:end]

    return pages


def figure_label_patterns(figure_panel: str) -> list[re.Pattern[str]]:
    match = FIGURE_PANEL_RE.search(figure_panel)
    if not match:
        return []

    label_kind = match.group(1).casefold().replace(" ", "")
    figure_number = re.escape(match.group(2))
    if "extendeddata" in label_kind:
        return [
            re.compile(rf"\bExtended\s+Data\s+Fig\.?\s*{figure_number}\b", re.I),
            re.compile(rf"\bExtended\s+Data\s+Figure\s*{figure_number}\b", re.I),
        ]

    return [
        re.compile(rf"\bFig\.?\s*{figure_number}\b", re.I),
        re.compile(rf"\bFigure\s*{figure_number}\b", re.I),
    ]


def figure_caption_patterns(figure_panel: str) -> list[re.Pattern[str]]:
    match = FIGURE_PANEL_RE.search(figure_panel)
    if not match:
        return []

    label_kind = match.group(1).casefold().replace(" ", "")
    figure_number = re.escape(match.group(2))
    if "extendeddata" in label_kind:
        return [
            re.compile(rf"\bExtended\s+Data\s+Fig\.?\s*{figure_number}\s*\|", re.I),
            re.compile(rf"\bExtended\s+Data\s+Figure\s*{figure_number}\s*\|", re.I),
        ]

    return [
        re.compile(rf"\bFig\.?\s*{figure_number}\s*\|", re.I),
        re.compile(rf"\bFigure\s*{figure_number}\s*\|", re.I),
    ]


def is_extended_panel(figure_panel: str) -> bool:
    match = FIGURE_PANEL_RE.search(figure_panel)
    if not match:
        return False
    return "extendeddata" in match.group(1).casefold().replace(" ", "")


def is_disallowed_figure_context(page_text: str, match_start: int, extended_panel: bool) -> bool:
    prefix = page_text[max(0, match_start - 40) : match_start]
    normalized_prefix = re.sub(r"-\s*", "", prefix)
    if re.search(r"(Supplementary|Supplemental)\s+$", normalized_prefix, re.I):
        return True
    if not extended_panel and re.search(r"Extended\s+Data\s+$", normalized_prefix, re.I):
        return True
    return False


def find_pages_matching(
    pages: dict[int, str],
    patterns: list[re.Pattern[str]],
    extended_panel: bool,
) -> list[int]:
    if not patterns:
        return []

    matches: list[int] = []
    for page_number, page_text in pages.items():
        if any(
            not is_disallowed_figure_context(page_text, match.start(), extended_panel)
            for pattern in patterns
            for match in pattern.finditer(page_text)
        ):
            matches.append(page_number)
    return matches


def find_figure_pages(pages: dict[int, str], figure_panel: str) -> list[int]:
    extended_panel = is_extended_panel(figure_panel)
    caption_pages = find_pages_matching(pages, figure_caption_patterns(figure_panel), extended_panel)
    if caption_pages:
        return caption_pages
    return find_pages_matching(pages, figure_label_patterns(figure_panel), extended_panel)


def page_image_exists(paper_dir: Path, page_number: int) -> bool:
    pages_dir = paper_dir / "pages"
    candidates = [
        pages_dir / f"page_{page_number:03d}.png",
        pages_dir / f"page_{page_number}.png",
    ]
    return any(candidate.exists() for candidate in candidates)


def parse_page_number(value: str) -> int | None:
    match = re.search(r"\d+", value)
    if not match:
        return None
    return int(match.group(0))


def card_requires_image(card: ParsedCard) -> bool:
    for field in card.field_values:
        if field.key == "source_status" and field.value in IMAGE_REQUIRED_VALUES:
            return True
        if field.key == "hex_colors_if_extractable" and field.value.casefold() not in EMPTY_VALUES:
            return True
    return False


def caption_excerpt_found(caption_excerpt: str, pages: dict[int, str]) -> bool:
    if not caption_excerpt:
        return True
    normalized_caption = normalize_text(caption_excerpt)
    if not normalized_caption:
        return True
    whole_text = normalize_text("\n".join(pages.values()))
    return normalized_caption in whole_text


def audit_card(card: ParsedCard, literature_dir: Path) -> list[Issue]:
    issues: list[Issue] = []
    paper_id = card.fields.get("paper_id", "")
    figure_panel = card.fields.get("figure_panel", "")
    page_number_value = card.fields.get("page_number", "")
    caption_excerpt = card.fields.get("caption_excerpt", "")

    if not paper_id:
        issues.append(
            Issue(
                card_path=card.path,
                code="MISSING_PAPER_ID",
                severity="error",
                message="Card does not declare paper_id.",
                suggestion="Add paper_id so the card can be checked against literature/extracted/{paper_id}.",
            )
        )
        return issues

    paper_dir = literature_dir / paper_id
    text_path = paper_dir / "text" / "full_text.md"
    if not text_path.exists():
        issues.append(
            Issue(
                card_path=card.path,
                code="TEXT_NOT_FOUND",
                severity="error",
                message=f"Extracted text not found: {text_path}",
                suggestion="Run extract_pdf_text.py before auditing this card.",
            )
        )
        return issues

    pages = parse_page_markdown(text_path.read_text(encoding="utf-8"))

    if not figure_panel:
        issues.append(
            Issue(
                card_path=card.path,
                code="MISSING_FIGURE_PANEL",
                severity="error",
                message="Card does not declare figure_panel.",
                suggestion="Add a figure_panel such as Fig1a or ExtendedDataFig3b.",
            )
        )
    else:
        found_pages = find_figure_pages(pages, figure_panel)
        claimed_page = parse_page_number(page_number_value)
        if not found_pages:
            issues.append(
                Issue(
                    card_path=card.path,
                    code="FIGURE_LABEL_NOT_FOUND",
                    severity="warning",
                    message=f"No text mention of {figure_panel} was found in extracted Markdown.",
                    suggestion="Render the PDF page images and verify the panel visually.",
                )
            )
        elif claimed_page is None:
            issues.append(
                Issue(
                    card_path=card.path,
                    code="MISSING_PAGE_NUMBER",
                    severity="error",
                    message=f"{figure_panel} was found on page(s) {format_pages(found_pages)}, but card page_number is empty.",
                    suggestion=f"Set page_number to {found_pages[0]} or add a more precise locator.",
                )
            )
        elif claimed_page not in found_pages:
            issues.append(
                Issue(
                    card_path=card.path,
                    code="PAGE_MISMATCH",
                    severity="error",
                    message=(
                        f"Card page_number is {claimed_page}, but {figure_panel} was found "
                        f"on page(s) {format_pages(found_pages)}."
                    ),
                    suggestion=f"Set page_number to {found_pages[0]} or explain the alternate locator.",
                )
            )

    if not caption_excerpt_found(caption_excerpt, pages):
        issues.append(
            Issue(
                card_path=card.path,
                code="CAPTION_EXCERPT_NOT_FOUND",
                severity="warning",
                message="caption_excerpt does not appear verbatim in extracted Markdown.",
                suggestion="Use a short literal caption locator, or mark the field as an inferred question instead of an excerpt.",
            )
        )

    for field in card.field_values:
        if field.key != "source_status":
            continue
        if field.value and field.value not in CANONICAL_SOURCE_STATUS_VALUES:
            issues.append(
                Issue(
                    card_path=card.path,
                    code="NONCANONICAL_SOURCE_STATUS",
                    severity="warning",
                    message=(
                        f"Line {field.line_number} source_status uses {field.value!r}, "
                        "which is outside the extraction schema vocabulary."
                    ),
                    suggestion="Use one of: explicit in caption/text; visible in page image; user observation; inferred; not reported in PDF.",
                )
            )

    claimed_page = parse_page_number(page_number_value)
    if card_requires_image(card) and claimed_page is not None and not page_image_exists(paper_dir, claimed_page):
        issues.append(
            Issue(
                card_path=card.path,
                code="IMAGE_PAGE_MISSING",
                severity="warning",
                message=f"Card relies on page-image evidence, but page {claimed_page} render was not found.",
                suggestion="Run extract_pdf_pages.py for this paper and inspect the rendered PNG before keeping visual claims.",
            )
        )

    return issues


def audit_cards(cards_dir: Path, literature_dir: Path) -> AuditResult:
    cards = sorted(path for path in cards_dir.rglob("*.md") if path.is_file())
    issues: list[Issue] = []
    for path in cards:
        issues.extend(audit_card(parse_card(path), literature_dir))
    return AuditResult(card_count=len(cards), issue_count=len(issues), issues=issues)


def format_pages(pages: list[int]) -> str:
    return ", ".join(str(page) for page in pages)


def render_markdown_report(result: AuditResult) -> str:
    lines = [
        "# Figure Card Audit Report",
        "",
        f"- Cards checked: {result.card_count}",
        f"- Issues found: {result.issue_count}",
    ]

    if not result.issues:
        lines.extend(["", "No issues found."])
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            "",
            "| Severity | Code | Card | Message | Suggestion |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for issue in result.issues:
        lines.append(
            "| {severity} | {code} | {card} | {message} | {suggestion} |".format(
                severity=escape_markdown_table(issue.severity),
                code=escape_markdown_table(issue.code),
                card=escape_markdown_table(str(issue.card_path)),
                message=escape_markdown_table(issue.message),
                suggestion=escape_markdown_table(issue.suggestion),
            )
        )
    return "\n".join(lines) + "\n"


def escape_markdown_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate figure extraction cards against extracted PDF evidence.")
    parser.add_argument("cards_dir", type=Path, help="Directory containing figure extraction card Markdown files.")
    parser.add_argument(
        "--literature-dir",
        type=Path,
        default=Path("literature/extracted"),
        help="Directory containing extracted paper text and optional page renders.",
    )
    parser.add_argument("--output", type=Path, help="Optional Markdown report path.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when any issue is found.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.cards_dir.exists():
        raise SystemExit(f"Cards directory not found: {args.cards_dir}")
    if not args.literature_dir.exists():
        raise SystemExit(f"Literature extraction directory not found: {args.literature_dir}")

    result = audit_cards(args.cards_dir, args.literature_dir)
    report = render_markdown_report(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(report)

    if args.strict and result.issue_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
