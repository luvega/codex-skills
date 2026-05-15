#!/usr/bin/env python
"""Deterministic checks for Nature-style figure package basics."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


MM_PER_POINT = 25.4 / 72.0


@dataclass
class Finding:
    severity: str
    path: str
    check: str
    message: str


MAIN_PREFERRED = {".ai", ".eps", ".pdf"}
MAIN_ACCEPTABLE = {".ps", ".svg", ".xls", ".xlsx"}
MAIN_REJECTED = {".jpg", ".jpeg", ".tif", ".tiff", ".png"}
EXTENDED_ACCEPTED = {".jpg", ".jpeg", ".tif", ".tiff", ".eps"}


def page_size_mm(path: Path) -> tuple[float, float] | None:
    if path.suffix.lower() != ".pdf":
        return None
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError:
        return None

    reader = PdfReader(str(path))
    if not reader.pages:
        return None
    box = reader.pages[0].mediabox
    width = float(box.width) * MM_PER_POINT
    height = float(box.height) * MM_PER_POINT
    return width, height


def raster_info(path: Path) -> tuple[int, int, float | None, float | None] | None:
    if path.suffix.lower() not in {".jpg", ".jpeg", ".tif", ".tiff", ".png"}:
        return None
    try:
        from PIL import Image  # type: ignore
    except ImportError:
        return None
    with Image.open(path) as image:
        dpi = image.info.get("dpi", (None, None))
        xdpi = float(dpi[0]) if dpi and dpi[0] else None
        ydpi = float(dpi[1]) if dpi and dpi[1] else None
        return image.width, image.height, xdpi, ydpi


def check_file(path: Path, kind: str) -> list[Finding]:
    findings: list[Finding] = []
    label = str(path)
    if not path.exists():
        return [Finding("ERROR", label, "exists", "File does not exist.")]

    ext = path.suffix.lower()
    size_mb = path.stat().st_size / (1024 * 1024)

    if kind == "main":
        if ext in MAIN_REJECTED:
            findings.append(Finding("ERROR", label, "format", f"{ext} is not accepted for main figures. Use editable vector artwork such as PDF/EPS/AI."))
        elif ext not in MAIN_PREFERRED and ext not in MAIN_ACCEPTABLE:
            findings.append(Finding("WARN", label, "format", f"{ext or '[none]'} is not listed as a preferred or acceptable main-figure format."))
        elif ext in MAIN_ACCEPTABLE:
            findings.append(Finding("WARN", label, "format", f"{ext} is acceptable but not preferred; PDF/EPS/AI are preferred."))
        if size_mb > 50:
            findings.append(Finding("WARN", label, "file_size", f"{size_mb:.1f} MB exceeds the recommended 50 MB main-figure size."))

        size = page_size_mm(path)
        if size:
            width, height = size
            if width > 183.5 or height > 170.5:
                findings.append(Finding("ERROR", label, "page_size", f"First page is {width:.1f} x {height:.1f} mm; main figures should fit 183 x 170 mm."))
            elif abs(width - 89) > 2 and abs(width - 183) > 2:
                findings.append(Finding("WARN", label, "page_width", f"First page width is {width:.1f} mm; expected near 89 mm or 183 mm."))

    if kind == "extended-data":
        if ext not in EXTENDED_ACCEPTED:
            findings.append(Finding("ERROR", label, "format", f"{ext or '[none]'} is not accepted for Extended Data. Use JPG/JPEG, TIFF, or EPS."))
        if size_mb > 10:
            findings.append(Finding("ERROR", label, "file_size", f"{size_mb:.1f} MB exceeds the 10 MB Extended Data limit."))

        size = page_size_mm(path)
        if size:
            width, height = size
            if width > 180.5 or height > 170.5:
                findings.append(Finding("ERROR", label, "page_size", f"First page is {width:.1f} x {height:.1f} mm; Extended Data should fit 180 x 170 mm."))

    info = raster_info(path)
    if info:
        width_px, height_px, xdpi, ydpi = info
        if xdpi is None or ydpi is None:
            findings.append(Finding("WARN", label, "dpi", f"Raster image is {width_px} x {height_px} px but has no readable DPI metadata."))
        elif min(xdpi, ydpi) < 300:
            findings.append(Finding("ERROR", label, "dpi", f"Raster DPI is {xdpi:.0f} x {ydpi:.0f}; minimum image resolution is 300 dpi."))

    if not findings:
        findings.append(Finding("PASS", label, "basic_package", "No deterministic file-format, size, or page-dimension issues found."))
    return findings


def write_report(findings: list[Finding], out_path: Path | None) -> str:
    lines = [
        "# Nature Figure Package Check",
        "",
        "| Severity | File | Check | Message |",
        "| --- | --- | --- | --- |",
    ]
    for finding in findings:
        lines.append(f"| {finding.severity} | `{finding.path}` | {finding.check} | {finding.message} |")
    text = "\n".join(lines) + "\n"
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8", newline="\n")
    return text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Nature figure package file basics.")
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--kind", choices=["main", "extended-data"], required=True)
    parser.add_argument("--out", type=Path, help="Optional Markdown report path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    findings: list[Finding] = []
    for file_path in args.files:
        findings.extend(check_file(file_path, args.kind))
    report = write_report(findings, args.out)
    print(report)
    return 1 if any(item.severity == "ERROR" for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
