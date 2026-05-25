from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "paper-figure-extractor"
    / "scripts"
    / "validate_figure_cards.py"
)


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_figure_cards", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ValidateFigureCardsTests(unittest.TestCase):
    def test_locates_figure_label_page_from_markdown_text(self) -> None:
        validator = load_validator()
        pages = validator.parse_page_markdown(
            """
## Page 1

Article title and abstract.

## Page 4

Fig. 1 | Driver genes in breast cancer. This caption describes panels.
"""
        )

        self.assertEqual(validator.find_figure_pages(pages, "Fig1_oncogrid"), [4])

    def test_main_figure_lookup_ignores_supplementary_and_extended_context(self) -> None:
        validator = load_validator()
        pages = validator.parse_page_markdown(
            """
## Page 1

The cohort design is shown in Supplementary Fig. 1.

## Page 2

Extended Data Fig. 1 | Full cohort overview.

## Page 4

Fig. 1 | Driver genes in breast cancer.
"""
        )

        self.assertEqual(validator.find_figure_pages(pages, "Fig1_oncogrid"), [4])

    def test_figure_lookup_prefers_caption_page_over_body_mentions(self) -> None:
        validator = load_validator()
        pages = validator.parse_page_markdown(
            """
## Page 2

The driver list is summarized in Fig. 1 and Extended Data Fig. 2.

## Page 3

Fig. 1 | Driver genes in breast cancer.
"""
        )

        self.assertEqual(validator.find_figure_pages(pages, "Fig1_oncogrid"), [3])

    def test_audits_page_number_mismatch_and_noncanonical_status(self) -> None:
        validator = load_validator()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cards_dir = root / "cards"
            text_dir = root / "literature" / "extracted" / "paper_a" / "text"
            cards_dir.mkdir()
            text_dir.mkdir(parents=True)
            (cards_dir / "paper_a_Fig1_oncogrid.md").write_text(
                """
# Figure Extraction Card

paper_id: paper_a
figure_panel: Fig1_oncogrid
page_number: 1
caption_excerpt: Fig1_oncogrid: What alterations recur?
source_status: inferred from PDF text/caption snippets
""".strip(),
                encoding="utf-8",
            )
            (text_dir / "full_text.md").write_text(
                """
## Page 1

Introduction.

## Page 4

Fig. 1 | Driver genes in breast cancer.
""".strip(),
                encoding="utf-8",
            )

            result = validator.audit_cards(cards_dir, root / "literature" / "extracted")
            issue_codes = {issue.code for issue in result.issues}

        self.assertIn("PAGE_MISMATCH", issue_codes)
        self.assertIn("NONCANONICAL_SOURCE_STATUS", issue_codes)

    def test_flags_image_evidence_without_rendered_page(self) -> None:
        validator = load_validator()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cards_dir = root / "cards"
            text_dir = root / "literature" / "extracted" / "paper_b" / "text"
            cards_dir.mkdir()
            text_dir.mkdir(parents=True)
            (cards_dir / "paper_b_Fig2_spatial.md").write_text(
                """
# Figure Extraction Card

paper_id: paper_b
figure_panel: Fig2_spatial
page_number: 2
caption_excerpt: Fig. 2 | Spatial map.
source_status: visible in page image
""".strip(),
                encoding="utf-8",
            )
            (text_dir / "full_text.md").write_text(
                """
## Page 2

Fig. 2 | Spatial map.
""".strip(),
                encoding="utf-8",
            )

            result = validator.audit_cards(cards_dir, root / "literature" / "extracted")

        self.assertIn("IMAGE_PAGE_MISSING", {issue.code for issue in result.issues})

    def test_markdown_report_includes_suggested_page(self) -> None:
        validator = load_validator()
        issue = validator.Issue(
            card_path=Path("cards/paper_a_Fig1.md"),
            code="PAGE_MISMATCH",
            severity="error",
            message="Card page_number is 1, but Fig. 1 was found on page 4.",
            suggestion="Set page_number to 4 or explain the alternate locator.",
        )
        report = validator.render_markdown_report(
            validator.AuditResult(card_count=1, issue_count=1, issues=[issue])
        )

        self.assertIn("PAGE_MISMATCH", report)
        self.assertIn("Set page_number to 4", report)


if __name__ == "__main__":
    unittest.main()
