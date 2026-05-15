#!/usr/bin/env python
"""Summarize figure extraction cards into a TSV table."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


FIELDS = [
    "paper_id",
    "citation",
    "doi",
    "figure_panel",
    "page_number",
    "question",
    "primary_data_type",
    "observation_unit",
    "plot_type",
    "x_mapping",
    "y_mapping",
    "color_mapping",
    "facet_mapping",
    "ordering_rule",
    "statistical_test",
    "multiple_testing",
    "comparison_direction",
    "palette_type",
    "figure_kind",
    "target_width_class",
    "panel_label_rule",
    "accessibility_rule",
    "image_integrity_rule",
    "chemical_structure_rule",
    "export_format_rule",
    "compliance_conflicts",
    "background",
    "font",
    "candidate_packages",
    "This plot is useful when",
    "Do not use this plot when",
]


FIELD_RE = re.compile(r"^([A-Za-z0-9_][A-Za-z0-9_ ]*):\s*(.*)$")


def parse_card(path: Path) -> dict[str, str]:
    values: dict[str, str] = {"card_path": str(path)}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = FIELD_RE.match(line.strip())
        if match:
            key, value = match.groups()
            values[key.strip()] = value.strip()
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize figure cards into TSV.")
    parser.add_argument("cards_dir", type=Path)
    parser.add_argument("output_tsv", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.cards_dir.exists():
        raise SystemExit(f"Cards directory not found: {args.cards_dir}")

    cards = sorted(args.cards_dir.glob("*.md"))
    args.output_tsv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_tsv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["card_path", *FIELDS], delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for card in cards:
            writer.writerow(parse_card(card))

    print(f"Wrote {len(cards)} cards to {args.output_tsv}")


if __name__ == "__main__":
    main()
