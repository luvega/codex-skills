import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_figure_evidence_passport.py"
VALID = ROOT / "tests" / "fixtures" / "valid_figure_evidence_passport.json"
INVALID = ROOT / "tests" / "fixtures" / "invalid_figure_evidence_passport.json"


class FigureEvidencePassportTests(unittest.TestCase):
    def run_checker(self, fixture: Path):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(fixture), "--format", "json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_valid_passport_links_source_card_recipe_and_qc(self):
        result = self.run_checker(VALID)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["issues"], [])
        self.assertEqual(payload["summary"]["cards"], 1)
        self.assertEqual(payload["summary"]["plot_recipes"], 1)

    def test_missing_text_and_image_evidence_is_rejected(self):
        result = self.run_checker(INVALID)
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        codes = {issue["code"] for issue in payload["issues"]}
        self.assertIn("MISSING_TEXT_EVIDENCE", codes)
        self.assertIn("MISSING_IMAGE_EVIDENCE", codes)
        self.assertIn("NON_LOCAL_ONLY_PATH", codes)


if __name__ == "__main__":
    unittest.main()
