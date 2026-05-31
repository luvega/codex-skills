from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "nature-biofigure-coder"
    / "scripts"
    / "figureya_module_audit.py"
)


def load_audit_module():
    spec = importlib.util.spec_from_file_location("figureya_module_audit", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FigureYaModuleAuditTests(unittest.TestCase):
    def test_indexes_module_inputs_examples_and_r_packages(self) -> None:
        audit = load_audit_module()

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            module_dir = repo / "FigureYa59volcanoV2"
            module_dir.mkdir()
            (module_dir / "FigureYa59volcanoV2.Rmd").write_text(
                """
library(ggplot2)
library(ggrepel)
x <- read.csv("easy_input_limma.csv")
""".strip(),
                encoding="utf-8",
            )
            (module_dir / "easy_input_limma.csv").write_text("gene,logFC,P.Value\nA,1,0.01\n", encoding="utf-8")
            (module_dir / "example.png").write_bytes(b"png")

            records = audit.index_modules(repo)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].module, "FigureYa59volcanoV2")
        self.assertIn("easy_input_limma.csv", records[0].sample_inputs)
        self.assertIn("example.png", records[0].examples)
        self.assertIn("ggplot2", records[0].r_packages)
        self.assertIn("ggrepel", records[0].r_packages)

    def test_matches_recipe_to_preferred_local_module(self) -> None:
        audit = load_audit_module()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "FigureYa"
            repo.mkdir()
            volcano = repo / "FigureYa59volcanoV2"
            heatmap = repo / "FigureYa9heatmap"
            volcano.mkdir()
            heatmap.mkdir()
            (volcano / "FigureYa59volcanoV2.Rmd").write_text("library(ggplot2)\nvolcano logFC pvalue", encoding="utf-8")
            (volcano / "easy_input_limma.csv").write_text("gene,logFC,P.Value\n", encoding="utf-8")
            (heatmap / "FigureYa9heatmap.Rmd").write_text("library(pheatmap)\nheatmap matrix", encoding="utf-8")

            recipes = root / "recipes"
            recipes.mkdir()
            (recipes / "volcano_differential_expression.yml").write_text(
                """
recipe_id: volcano_differential_expression
plot_type: Volcano differential expression plot
purpose: Summarize effect size and adjusted significance.
implementation:
  r_packages: [ggplot2, ggrepel]
""".strip(),
                encoding="utf-8",
            )
            map_path = root / "map.tsv"
            map_path.write_text(
                "recipe_pattern\tkeywords\tpreferred_modules\tnotes\n"
                "volcano\tvolcano differential expression logFC pvalue\tFigureYa59volcanoV2\tUse DE result table.\n",
                encoding="utf-8",
            )

            records = audit.index_modules(repo)
            rows = audit.match_recipes(recipes, records, audit.read_backend_map(map_path), top_n=2)

        self.assertEqual(rows[0]["recipe_id"], "volcano_differential_expression")
        self.assertEqual(rows[0]["top_module"], "FigureYa59volcanoV2")
        self.assertGreater(int(rows[0]["top_score"]), 0)
        self.assertEqual(rows[0]["top_confidence"], "high")

    def test_reports_no_confidence_when_no_module_matches(self) -> None:
        audit = load_audit_module()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "FigureYa"
            repo.mkdir()

            recipes = root / "recipes"
            recipes.mkdir()
            (recipes / "unknown_plot.yml").write_text(
                """
recipe_id: unclassified_plot
plot_type: Completely unrelated schematic
purpose: No shared biological plotting terms.
""".strip(),
                encoding="utf-8",
            )

            records = audit.index_modules(repo)
            rows = audit.match_recipes(recipes, records, backend_map=[], top_n=2)

        self.assertEqual(rows[0]["top_module"], "")
        self.assertEqual(rows[0]["top_confidence"], "none")

    def test_short_recipe_patterns_match_exact_tokens_only(self) -> None:
        audit = load_audit_module()
        backend_map = [
            {"recipe_pattern": "ma", "keywords": "MA plot", "preferred_modules": "FigureYa59volcanoV2", "notes": ""},
            {"recipe_pattern": "manhattan", "keywords": "Manhattan locus", "preferred_modules": "FigureYa74OmicCircos", "notes": ""},
        ]

        manhattan = {
            "recipe_id": "manhattan_locus_plot",
            "plot_type": "Manhattan or regional locus plot",
            "purpose": "",
        }
        ma = {
            "recipe_id": "ma_mean_difference",
            "plot_type": "MA mean-difference plot",
            "purpose": "",
        }

        self.assertEqual(
            [row["recipe_pattern"] for row in audit.matching_backend_rows(manhattan, backend_map)],
            ["manhattan"],
        )
        self.assertEqual(
            [row["recipe_pattern"] for row in audit.matching_backend_rows(ma, backend_map)],
            ["ma"],
        )


if __name__ == "__main__":
    unittest.main()
