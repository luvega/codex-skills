#!/usr/bin/env python
"""Render PDF pages to PNG files for figure inspection."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render PDF pages to PNG files.")
    parser.add_argument("pdf_path", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--dpi", type=int, default=200)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.pdf_path.exists():
        raise SystemExit(f"PDF not found: {args.pdf_path}")

    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise SystemExit("Missing dependency: PyMuPDF. Install with `python -m pip install pymupdf`.") from exc

    args.out_dir.mkdir(parents=True, exist_ok=True)
    zoom = args.dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    doc = fitz.open(args.pdf_path)
    for index, page in enumerate(doc, start=1):
        pixmap = page.get_pixmap(matrix=matrix, alpha=False)
        pixmap.save(args.out_dir / f"page_{index:03d}.png")

    print(f"Rendered {len(doc)} pages to {args.out_dir}")


if __name__ == "__main__":
    main()
