#!/usr/bin/env python
"""Extract PDF text into a page-delimited Markdown file."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract PDF text to Markdown.")
    parser.add_argument("pdf_path", type=Path)
    parser.add_argument("out_path", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.pdf_path.exists():
        raise SystemExit(f"PDF not found: {args.pdf_path}")

    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise SystemExit("Missing dependency: PyMuPDF. Install with `python -m pip install pymupdf`.") from exc

    args.out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(args.pdf_path)

    with args.out_path.open("w", encoding="utf-8", newline="\n") as handle:
        for index, page in enumerate(doc, start=1):
            handle.write(f"\n\n# Page {index}\n\n")
            handle.write(page.get_text())

    print(f"Extracted text from {len(doc)} pages to {args.out_path}")


if __name__ == "__main__":
    main()
