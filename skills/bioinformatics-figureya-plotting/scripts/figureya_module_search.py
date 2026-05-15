#!/usr/bin/env python3
"""Search and index FigureYa biomedical plotting modules."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_DIR / "references"
DEFAULT_LOCAL_INDEX = REFERENCES / "module-index-local.tsv"
DEFAULT_TASK_MAP = REFERENCES / "task-map.tsv"
DEFAULT_COVERAGE = REFERENCES / "upstream-local-coverage.tsv"


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def tokenize(text: str) -> list[str]:
    return [t for t in re.split(r"[^a-zA-Z0-9_+\-.]+", text.lower()) if t]


def append_unique_semicolon(existing: str, value: str) -> str:
    values = [v for v in existing.split(";") if v]
    if value and value not in values:
        values.append(value)
    return ";".join(values)


def append_unique_words(existing: str, value: str) -> str:
    seen = set(tokenize(existing))
    words = existing.split() if existing else []
    for word in value.split():
        key = word.lower()
        if key not in seen:
            words.append(word)
            seen.add(key)
    return " ".join(words)


def append_unique_sentence(existing: str, value: str) -> str:
    value = value.strip()
    if not value:
        return existing
    if value in existing:
        return existing
    return (existing + " " + value).strip()


def scan_repo(repo: Path) -> list[dict[str, str]]:
    repo = repo.resolve()
    modules = []
    for child in sorted(repo.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir():
            continue
        if not child.name.startswith("FigureYa"):
            continue
        if child.name in {".trash", "__MACOSX"}:
            continue
        files = [p for p in child.rglob("*") if p.is_file() and "__MACOSX" not in p.parts]
        rels = [p.relative_to(repo).as_posix() for p in files]
        rmd = [p for p in rels if p.lower().endswith(".rmd")]
        html = [p for p in rels if p.lower().endswith(".html")]
        inputs = [
            p
            for p in rels
            if re.search(r"/?(easy_input|input|example)[^/]*$", p, flags=re.I)
        ]
        outputs = [
            p
            for p in rels
            if re.search(r"/?(output|plot|result)[^/]*$", p, flags=re.I)
            or p.lower().endswith((".pdf", ".png", ".jpg", ".jpeg", ".webp"))
        ]
        modules.append(
            {
                "module": child.name,
                "local_status": "scanned-local",
                "rmd_count": str(len(rmd)),
                "html_count": str(len(html)),
                "rmd": ";".join(rmd[:12]),
                "html": ";".join(html[:8]),
                "sample_inputs": ";".join(inputs[:8]),
                "sample_outputs": ";".join(outputs[:8]),
            }
        )
    return modules


def build_records(local_index: Path, task_map: Path, coverage: Path) -> list[dict[str, str]]:
    by_module: dict[str, dict[str, str]] = {}
    for row in read_tsv(local_index):
        by_module[row["module"]] = dict(row)

    for row in read_tsv(coverage):
        module = row.get("module", "")
        if not module:
            continue
        by_module.setdefault(
            module,
            {
                "module": module,
                "local_status": "upstream-only",
                "rmd_count": "",
                "html_count": "",
                "rmd": "",
                "html": "",
                "sample_inputs": "",
                "sample_outputs": "",
            },
        )
        if row.get("local_available", "").lower() == "true":
            by_module[module]["upstream_status"] = "present-upstream-and-local"
        else:
            by_module[module]["upstream_status"] = "upstream-only"

    task_rows = read_tsv(task_map)
    for task in task_rows:
        modules = []
        modules.extend(task.get("recommended_modules", "").split(";"))
        modules.extend(task.get("local_first", "").split(";"))
        for module in [m.strip() for m in modules if m.strip()]:
            by_module.setdefault(
                module,
                {
                    "module": module,
                    "local_status": "task-map-only",
                    "rmd_count": "",
                    "html_count": "",
                    "rmd": "",
                    "html": "",
                    "sample_inputs": "",
                    "sample_outputs": "",
                },
            )
            rec = by_module[module]
            rec["tasks"] = append_unique_semicolon(rec.get("tasks", ""), task.get("task", ""))
            rec["keywords"] = append_unique_words(rec.get("keywords", ""), task.get("keywords", ""))
            rec["notes"] = append_unique_sentence(rec.get("notes", ""), task.get("notes", ""))

    return list(by_module.values())


def score_record(record: dict[str, str], query_terms: list[str]) -> int:
    haystack_fields = [
        "module",
        "tasks",
        "keywords",
        "notes",
        "rmd",
        "html",
        "sample_inputs",
        "sample_outputs",
    ]
    haystack = " ".join(record.get(field, "") for field in haystack_fields).lower()
    score = 0
    module_name = record.get("module", "").lower()
    compact_query = "".join(query_terms)
    exact_module_query = compact_query == module_name or (
        compact_query.startswith("figureya") and compact_query in module_name
    )
    for term in query_terms:
        if term in module_name:
            score += 8
        if term in record.get("tasks", "").lower():
            score += 6
        if term in record.get("keywords", "").lower():
            score += 5
        if term in haystack:
            score += 1
    if query_terms and score == 0:
        return 0
    if record.get("local_status", "").endswith("local"):
        score += 2
    if record.get("local_status") in {"upstream-only", "task-map-only"} and not exact_module_query:
        score -= 8
    if record.get("rmd"):
        score += 1
    return score


def command_search(args: argparse.Namespace) -> int:
    local_index = Path(args.local_index) if args.local_index else DEFAULT_LOCAL_INDEX
    if args.repo:
        live_rows = scan_repo(Path(args.repo))
        local_index = Path(args.cache_index) if args.cache_index else local_index
        if args.cache_index:
            fields = [
                "module",
                "local_status",
                "rmd_count",
                "html_count",
                "rmd",
                "html",
                "sample_inputs",
                "sample_outputs",
            ]
            write_tsv(local_index, live_rows, fields)
        else:
            temp = {row["module"]: row for row in read_tsv(local_index)}
            for row in live_rows:
                temp[row["module"]] = row
            tmp_path = None
            records = list(temp.values())
            task_map = read_tsv(DEFAULT_TASK_MAP)
            coverage = read_tsv(DEFAULT_COVERAGE)
            local_path = None
            # Build in-memory equivalent with task and coverage rows.
            by_module = {r["module"]: dict(r) for r in records}
            for row in coverage:
                module = row.get("module", "")
                by_module.setdefault(module, {"module": module, "local_status": "upstream-only"})
            for task in task_map:
                for module in (task.get("recommended_modules", "") + ";" + task.get("local_first", "")).split(";"):
                    module = module.strip()
                    if not module:
                        continue
                    rec = by_module.setdefault(module, {"module": module, "local_status": "task-map-only"})
                    rec["tasks"] = append_unique_semicolon(rec.get("tasks", ""), task.get("task", ""))
                    rec["keywords"] = append_unique_words(rec.get("keywords", ""), task.get("keywords", ""))
                    rec["notes"] = append_unique_sentence(rec.get("notes", ""), task.get("notes", ""))
            records = list(by_module.values())
    else:
        records = build_records(local_index, DEFAULT_TASK_MAP, DEFAULT_COVERAGE)

    query_terms = tokenize(args.query)
    ranked = []
    for rec in records:
        if args.local_only and rec.get("local_status") in {"upstream-only", "task-map-only"}:
            continue
        score = score_record(rec, query_terms)
        if score > 0 or not query_terms:
            ranked.append((score, rec))
    ranked.sort(key=lambda item: (-item[0], item[1].get("module", "")))

    if not ranked:
        print("No matching FigureYa modules found.")
        return 1

    for score, rec in ranked[: args.limit]:
        rmd = rec.get("rmd", "")
        first_rmd = rmd.split(";")[0] if rmd else ""
        print(
            "\t".join(
                [
                    str(score),
                    rec.get("module", ""),
                    rec.get("local_status", ""),
                    rec.get("tasks", ""),
                    first_rmd,
                    rec.get("notes", "")[:180],
                ]
            )
        )
    return 0


def command_index(args: argparse.Namespace) -> int:
    rows = scan_repo(Path(args.repo))
    fields = [
        "module",
        "local_status",
        "rmd_count",
        "html_count",
        "rmd",
        "html",
        "sample_inputs",
        "sample_outputs",
    ]
    write_tsv(Path(args.out), rows, fields)
    print(f"Indexed {len(rows)} modules into {args.out}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search", help="search FigureYa modules")
    search.add_argument("query", help="search terms, e.g. 'volcano DEG'")
    search.add_argument("--repo", help="optional FigureYa checkout to scan")
    search.add_argument("--local-index", help="override bundled local index")
    search.add_argument("--cache-index", help="write scanned repo index to this TSV")
    search.add_argument("--local-only", action="store_true", help="hide upstream-only/task-map-only modules")
    search.add_argument("--limit", type=int, default=12)
    search.set_defaults(func=command_search)

    index = sub.add_parser("index", help="index a FigureYa checkout")
    index.add_argument("repo", help="FigureYa checkout path")
    index.add_argument("--out", required=True, help="output TSV path")
    index.set_defaults(func=command_index)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
