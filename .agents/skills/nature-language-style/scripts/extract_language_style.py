#!/usr/bin/env python
"""Extract deterministic language-style signals from local Nature-family text."""

from __future__ import annotations

import argparse
import csv
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


PHRASE_PATTERNS = {
    "here_we": r"\bHere,?\s+we\b",
    "we_present": r"\bwe\s+present\b",
    "we_show": r"\bwe\s+show\b",
    "we_demonstrate": r"\bwe\s+demonstrate\b",
    "we_identified": r"\bwe\s+identified?\b",
    "we_found": r"\bwe\s+found\b",
    "we_developed": r"\bwe\s+developed?\b",
    "these_findings": r"\bThese\s+findings\b",
    "suggest": r"\bsuggest(?:s|ed|ing)?\b",
    "may": r"\bmay\b",
    "could": r"\bcould\b",
    "remains_challenging": r"\bremains?\s+challenging\b",
    "however": r"\bHowever\b",
    "using": r"\bUsing\b",
    "to_our_knowledge": r"\bto\s+our\s+knowledge\b",
}

SECTION_KEYWORDS = {
    "abstract": {"abstract"},
    "introduction": {"introduction"},
    "results": {"results"},
    "discussion": {"discussion"},
    "methods": {"methods", "materials and methods"},
}


@dataclass
class Sample:
    paper_id: str
    source_file: str
    section_guess: str
    sample_type: str
    word_count: int
    sentence_count: int
    trigger_tokens: str
    text_excerpt: str


def normalize_text(text: str) -> str:
    replacements = {
        "\u00a0": " ",
        "\u2009": " ",
        "\u202f": " ",
        "\ufeff": "",
        "\u00ad": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text


def clean_block(block: str) -> str:
    block = normalize_text(block)
    block = re.sub(r"\n+", " ", block)
    block = re.sub(r"\s+", " ", block).strip()
    return block


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z0-9+\-]*", text)


def split_sentences(text: str) -> list[str]:
    pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text.strip())
    return [piece.strip() for piece in pieces if len(words(piece)) >= 3]


def short_excerpt(text: str, max_words: int = 18) -> str:
    tokens = text.split()
    excerpt = " ".join(tokens[:max_words])
    if len(tokens) > max_words:
        excerpt += " ..."
    return excerpt


def detect_tokens(text: str) -> list[str]:
    return [
        name
        for name, pattern in PHRASE_PATTERNS.items()
        if re.search(pattern, text, flags=re.IGNORECASE)
    ]


def section_guess(block: str, current: str) -> str:
    low = block.lower().strip()
    plain = re.sub(r"[^a-z ]", "", low).strip()
    for section, names in SECTION_KEYWORDS.items():
        if plain in names:
            return section
    if re.match(r"^(fig\.|figure|extended data fig\.)\s*\d+", low):
        return "figure_legend"
    return current


def sample_type(block: str, current: str, index: int) -> str:
    low = block.lower()
    wc = len(words(block))
    if current == "figure_legend":
        return "figure_caption"
    if index < 12 and 70 <= wc <= 260 and any(token in low for token in ("here we", "here, we", "we present", "we show", "we demonstrate")):
        return "abstract_candidate"
    if wc <= 12 and not block.endswith("."):
        return "heading"
    return "body_paragraph"


def iter_text_files(input_dir: Path) -> list[Path]:
    files = sorted(input_dir.glob("*/text/full_text.md"))
    if files:
        return files
    return sorted(input_dir.rglob("*.md"))


def parse_paper(path: Path) -> tuple[str, list[Sample], Counter[str], list[int]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    paper_id_match = re.search(r"^paper_id:\s*(\S+)", raw, flags=re.MULTILINE)
    paper_id = paper_id_match.group(1) if paper_id_match else path.parent.parent.name

    blocks = [clean_block(block) for block in re.split(r"\n\s*\n", raw)]
    blocks = [block for block in blocks if block and not block.startswith("# Page ")]

    samples: list[Sample] = []
    phrase_counts: Counter[str] = Counter()
    sentence_lengths: list[int] = []
    current_section = "front_matter"

    for idx, block in enumerate(blocks):
        if block.startswith("#") or block.startswith("paper_id:") or block.startswith("pages:") or block.startswith("## Page"):
            continue
        current_section = section_guess(block, current_section)
        wc = len(words(block))
        if wc == 0:
            continue

        sentences = split_sentences(block)
        sentence_lengths.extend(len(words(sentence)) for sentence in sentences)

        for name, pattern in PHRASE_PATTERNS.items():
            phrase_counts[name] += len(re.findall(pattern, block, flags=re.IGNORECASE))

        stype = sample_type(block, current_section, idx)
        keep_block = (
            stype == "heading"
            or stype == "abstract_candidate"
            or stype == "figure_caption"
            or 35 <= wc <= 260
        )
        if keep_block:
            tokens = detect_tokens(block)
            samples.append(
                Sample(
                    paper_id=paper_id,
                    source_file=str(path),
                    section_guess=current_section,
                    sample_type=stype,
                    word_count=wc,
                    sentence_count=len(sentences),
                    trigger_tokens=";".join(tokens),
                    text_excerpt=short_excerpt(block),
                )
            )

        for sentence in sentences:
            sentence_wc = len(words(sentence))
            sentence_tokens = detect_tokens(sentence)
            if sentence_tokens and 8 <= sentence_wc <= 45:
                samples.append(
                    Sample(
                        paper_id=paper_id,
                        source_file=str(path),
                        section_guess=current_section,
                        sample_type="sentence",
                        word_count=sentence_wc,
                        sentence_count=1,
                        trigger_tokens=";".join(sentence_tokens),
                        text_excerpt=short_excerpt(sentence),
                    )
                )

    return paper_id, samples, phrase_counts, sentence_lengths


def write_samples(samples: list[Sample], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(Sample.__annotations__.keys()), delimiter="\t")
        writer.writeheader()
        for sample in samples:
            writer.writerow(sample.__dict__)


def write_phrase_counts(counts: Counter[str], paper_hits: dict[str, set[str]], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["phrase", "count", "papers"], delimiter="\t")
        writer.writeheader()
        for phrase, count in counts.most_common():
            writer.writerow({"phrase": phrase, "count": count, "papers": len(paper_hits[phrase])})


def write_profile(paper_count: int, samples: list[Sample], counts: Counter[str], sentence_lengths: list[int], out_path: Path) -> None:
    type_counts = Counter(sample.sample_type for sample in samples)
    section_counts = Counter(sample.section_guess for sample in samples)
    top_phrases = counts.most_common(10)
    lines = [
        "# Local Nature Language Style Profile",
        "",
        f"papers_processed: {paper_count}",
        f"samples_recorded: {len(samples)}",
        f"sentence_count: {len(sentence_lengths)}",
        f"mean_sentence_words: {statistics.mean(sentence_lengths) if sentence_lengths else 0:.1f}",
        f"median_sentence_words: {statistics.median(sentence_lengths) if sentence_lengths else 0:.1f}",
        f"over_30_word_sentences: {sum(1 for value in sentence_lengths if value > 30)}",
        "",
        "## Sample Types",
        "",
        "| Type | Count |",
        "| --- | ---: |",
    ]
    lines.extend(f"| {name} | {count} |" for name, count in sorted(type_counts.items()))
    lines.extend(["", "## Section Guesses", "", "| Section | Count |", "| --- | ---: |"])
    lines.extend(f"| {name} | {count} |" for name, count in sorted(section_counts.items()))
    lines.extend(["", "## Frequent Move Tokens", "", "| Token | Count |", "| --- | ---: |"])
    lines.extend(f"| {name} | {count} |" for name, count in top_phrases)
    lines.extend(
        [
            "",
            "## Derived Style Notes",
            "",
            "- Abstract-like front-matter often uses a compact context-gap-approach-result-implication sequence.",
            "- `Here we`, `we present`, `we show`, and related tokens mark the main contribution sentence.",
            "- Hedging tokens such as `suggest`, `may`, and `could` should be preserved when evidence is associative or mechanistic support is incomplete.",
            "- Results prose should keep figure orientation, observation, and quantitative support together.",
            "- Discussion prose should add interpretation and boundary rather than restating every result.",
            "",
            "## Limits",
            "",
            "- This profile is deterministic and does not judge scientific validity.",
            "- Snippets in `style_samples.tsv` are short locator excerpts, not reusable prose.",
            "- OCR or PDF extraction artifacts may affect counts; verify critical wording against the source PDF.",
        ]
    )
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract language-style metrics from local Nature-family text.")
    parser.add_argument("--input-dir", type=Path, default=Path("literature/extracted"))
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--max-papers", type=int, default=0, help="Optional limit for smoke tests.")
    args = parser.parse_args()

    files = iter_text_files(args.input_dir)
    if args.max_papers:
        files = files[: args.max_papers]
    if not files:
        raise SystemExit(f"No extracted text files found under {args.input_dir}")

    all_samples: list[Sample] = []
    total_counts: Counter[str] = Counter()
    paper_hits: dict[str, set[str]] = defaultdict(set)
    all_sentence_lengths: list[int] = []

    for path in files:
        paper_id, samples, counts, sentence_lengths = parse_paper(path)
        all_samples.extend(samples)
        total_counts.update(counts)
        for phrase, count in counts.items():
            if count:
                paper_hits[phrase].add(paper_id)
        all_sentence_lengths.extend(sentence_lengths)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_samples(all_samples, args.out_dir / "style_samples.tsv")
    write_phrase_counts(total_counts, paper_hits, args.out_dir / "phrase_counts.tsv")
    write_profile(len(files), all_samples, total_counts, all_sentence_lengths, args.out_dir / "language_style_profile.md")
    print(args.out_dir / "language_style_profile.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
