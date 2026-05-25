#!/usr/bin/env python
"""Index FigureYa modules and match plot recipes to local templates."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import NamedTuple


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parents[0]
DEFAULT_BACKEND_MAP = SKILL_DIR / "references" / "figureya_backend_map.tsv"

MODULE_FIELDS = [
    "module",
    "module_path",
    "rmd",
    "html",
    "sample_inputs",
    "examples",
    "sample_outputs",
    "r_packages",
    "text_preview",
]

MATCH_FIELDS = [
    "recipe_id",
    "plot_type",
    "top_module",
    "top_score",
    "top_rmd",
    "top_inputs",
    "top_examples",
    "top_r_packages",
    "candidate_modules",
    "backend_notes",
]


class ModuleRecord(NamedTuple):
    module: str
    module_path: str
    rmd: str
    html: str
    sample_inputs: str
    examples: str
    sample_outputs: str
    r_packages: str
    text_preview: str


def read_text_lossy(path: Path, limit: int = 40000) -> str:
    data = path.read_bytes()[:limit]
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def tokenize(text: str) -> list[str]:
    return [token for token in re.split(r"[^A-Za-z0-9_+\-.]+", text.casefold()) if token]


def unique_join(values: list[str], limit: int = 20) -> str:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        ordered.append(value)
        seen.add(value)
        if len(ordered) >= limit:
            break
    return ";".join(ordered)


def extract_r_packages(text: str) -> str:
    packages: list[str] = []
    for pattern in (r"\blibrary\s*\(\s*['\"]?([A-Za-z0-9_.]+)", r"\brequire\s*\(\s*['\"]?([A-Za-z0-9_.]+)"):
        packages.extend(re.findall(pattern, text))
    return unique_join(packages, limit=50)


def rel_paths(files: list[Path], repo: Path) -> list[str]:
    return [path.relative_to(repo).as_posix() for path in files]


def index_module(module_dir: Path, repo: Path) -> ModuleRecord:
    files = [path for path in module_dir.rglob("*") if path.is_file() and "__MACOSX" not in path.parts]
    rmd_files = sorted([path for path in files if path.suffix.casefold() == ".rmd"])
    html_files = sorted([path for path in files if path.suffix.casefold() == ".html"])
    input_files = sorted(
        [
            path
            for path in files
            if re.search(r"(^|/)(easy_input|input)[^/]*$", path.relative_to(module_dir).as_posix(), re.I)
        ]
    )
    example_files = sorted([path for path in files if path.name.casefold().startswith("example")])
    output_files = sorted(
        [
            path
            for path in files
            if path.suffix.casefold() in {".pdf", ".png", ".jpg", ".jpeg", ".svg"}
            and path not in example_files
        ]
    )
    rmd_text = "\n".join(read_text_lossy(path) for path in rmd_files[:3])
    preview = " ".join(tokenize(f"{module_dir.name} {rmd_text}")[:80])

    return ModuleRecord(
        module=module_dir.name,
        module_path=module_dir.relative_to(repo).as_posix(),
        rmd=unique_join(rel_paths(rmd_files, repo)),
        html=unique_join(rel_paths(html_files, repo)),
        sample_inputs=unique_join(rel_paths(input_files, repo)),
        examples=unique_join(rel_paths(example_files, repo)),
        sample_outputs=unique_join(rel_paths(output_files, repo)),
        r_packages=extract_r_packages(rmd_text),
        text_preview=preview,
    )


def index_modules(repo: Path) -> list[ModuleRecord]:
    repo = repo.resolve()
    records: list[ModuleRecord] = []
    for child in sorted(repo.iterdir(), key=lambda path: path.name.casefold()):
        if child.is_dir() and child.name.startswith("FigureYa"):
            records.append(index_module(child, repo))
    return records


def read_backend_map(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def parse_recipe(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    fields = {
        "recipe_id": path.stem,
        "plot_type": "",
        "purpose": "",
        "text": text,
    }
    for key in ("recipe_id", "plot_type", "purpose"):
        match = re.search(rf"^{key}:\s*(.+)$", text, re.MULTILINE)
        if match:
            fields[key] = match.group(1).strip().strip("\"'")
    package_match = re.search(r"r_packages:\s*\[([^\]]+)\]", text)
    if package_match:
        fields["r_packages"] = package_match.group(1).replace(",", " ")
    else:
        fields["r_packages"] = ""
    return fields


def matching_backend_rows(recipe: dict[str, str], backend_map: list[dict[str, str]]) -> list[dict[str, str]]:
    haystack = f"{recipe.get('recipe_id', '')} {recipe.get('plot_type', '')} {recipe.get('purpose', '')}".casefold()
    matched: list[dict[str, str]] = []
    for row in backend_map:
        pattern = row.get("recipe_pattern", "").casefold()
        if pattern and recipe_pattern_matches(pattern, haystack):
            matched.append(row)
    return matched


def recipe_pattern_matches(pattern: str, haystack: str) -> bool:
    normalized_pattern = pattern.replace("_", " ")
    normalized_haystack = haystack.replace("_", " ")
    pattern_tokens = [token for token in re.split(r"[^a-z0-9]+", normalized_pattern) if token]
    haystack_tokens = [token for token in re.split(r"[^a-z0-9]+", normalized_haystack) if token]
    if not pattern_tokens:
        return False
    if len(pattern_tokens) == 1 and len(pattern_tokens[0]) <= 3:
        return pattern_tokens[0] in haystack_tokens
    return pattern in haystack or normalized_pattern in normalized_haystack


def score_module(record: ModuleRecord, query: str, preferred_modules: set[str]) -> int:
    terms = tokenize(query)
    haystack = " ".join(
        [
            record.module,
            record.rmd,
            record.html,
            record.sample_inputs,
            record.examples,
            record.sample_outputs,
            record.r_packages,
            record.text_preview,
        ]
    ).casefold()
    score = 0
    module_name = record.module.casefold()
    for term in terms:
        if term in module_name:
            score += 10
        if term in record.r_packages.casefold():
            score += 4
        if term in record.sample_inputs.casefold():
            score += 4
        if term in haystack:
            score += 1
    if record.module in preferred_modules:
        score += 100
    if record.rmd:
        score += 2
    if record.examples:
        score += 2
    return score


def match_recipe(
    recipe: dict[str, str],
    records: list[ModuleRecord],
    backend_rows: list[dict[str, str]],
    top_n: int,
) -> dict[str, str]:
    keywords = " ".join(row.get("keywords", "") for row in backend_rows)
    preferred_modules = {
        module.strip()
        for row in backend_rows
        for module in row.get("preferred_modules", "").split(";")
        if module.strip()
    }
    query = " ".join(
        [
            recipe.get("recipe_id", ""),
            recipe.get("plot_type", ""),
            recipe.get("purpose", ""),
            recipe.get("r_packages", ""),
            keywords,
        ]
    )
    ranked = sorted(
        [(score_module(record, query, preferred_modules), record) for record in records],
        key=lambda item: (-item[0], item[1].module),
    )
    ranked = [item for item in ranked if item[0] > 0][:top_n]
    top_score, top = ranked[0] if ranked else (0, None)
    candidate_modules = ";".join(f"{record.module}:{score}" for score, record in ranked)
    backend_notes = " ".join(row.get("notes", "") for row in backend_rows).strip()

    return {
        "recipe_id": recipe.get("recipe_id", ""),
        "plot_type": recipe.get("plot_type", ""),
        "top_module": top.module if top else "",
        "top_score": str(top_score),
        "top_rmd": top.rmd if top else "",
        "top_inputs": top.sample_inputs if top else "",
        "top_examples": top.examples if top else "",
        "top_r_packages": top.r_packages if top else "",
        "candidate_modules": candidate_modules,
        "backend_notes": backend_notes,
    }


def match_recipes(
    recipes_dir: Path,
    records: list[ModuleRecord],
    backend_map: list[dict[str, str]],
    top_n: int = 5,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(recipes_dir.glob("*.yml")):
        recipe = parse_recipe(path)
        rows.append(match_recipe(recipe, records, matching_backend_rows(recipe, backend_map), top_n))
    return rows


def write_tsv(path: Path, rows: list[dict[str, str] | ModuleRecord], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row._asdict() if isinstance(row, ModuleRecord) else row)


def render_match_markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        "# FigureYa Recipe Match Report",
        "",
        f"- Recipes checked: {len(rows)}",
        "",
        "| Recipe | Plot type | Top FigureYa module | Score | Evidence files | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        evidence = "; ".join(value for value in (row["top_rmd"], row["top_inputs"], row["top_examples"]) if value)
        lines.append(
            "| {recipe} | {plot_type} | {module} | {score} | {evidence} | {notes} |".format(
                recipe=escape_table(row["recipe_id"]),
                plot_type=escape_table(row["plot_type"]),
                module=escape_table(row["top_module"] or "no local match"),
                score=escape_table(row["top_score"]),
                evidence=escape_table(evidence),
                notes=escape_table(row["backend_notes"]),
            )
        )
    return "\n".join(lines) + "\n"


def escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def command_index(args: argparse.Namespace) -> int:
    records = index_modules(args.repo)
    write_tsv(args.out, records, MODULE_FIELDS)
    print(f"Wrote {len(records)} FigureYa module records to {args.out}")
    return 0


def command_match(args: argparse.Namespace) -> int:
    records = index_modules(args.repo)
    rows = match_recipes(args.recipes_dir, records, read_backend_map(args.map), args.top_n)
    write_tsv(args.out, rows, MATCH_FIELDS)
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(render_match_markdown(rows), encoding="utf-8", newline="\n")
    print(f"Matched {len(rows)} recipes against {len(records)} FigureYa modules")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Index FigureYa modules and match recipe files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index", help="Index a local FigureYa checkout.")
    index_parser.add_argument("repo", type=Path)
    index_parser.add_argument("--out", type=Path, required=True)
    index_parser.set_defaults(func=command_index)

    match_parser = subparsers.add_parser("match", help="Match plot recipes to FigureYa modules.")
    match_parser.add_argument("recipes_dir", type=Path)
    match_parser.add_argument("--repo", type=Path, required=True)
    match_parser.add_argument("--map", type=Path, default=DEFAULT_BACKEND_MAP)
    match_parser.add_argument("--out", type=Path, required=True)
    match_parser.add_argument("--markdown", type=Path)
    match_parser.add_argument("--top-n", type=int, default=5)
    match_parser.set_defaults(func=command_match)

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
