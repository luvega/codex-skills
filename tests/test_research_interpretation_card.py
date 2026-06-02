import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_research_interpretation_card.py"
VALID = ROOT / "tests" / "fixtures" / "valid_research_interpretation_card.json"
INVALID = ROOT / "tests" / "fixtures" / "invalid_research_interpretation_card.json"


class ResearchInterpretationCardTests(unittest.TestCase):
    def run_checker(self, fixture: Path):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(fixture), "--format", "json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_valid_card_passes_with_supported_claim_locator(self):
        result = self.run_checker(VALID)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["issues"], [])
        self.assertEqual(payload["summary"]["domain"], "tumor-immunology")
        self.assertEqual(payload["summary"]["evidence_sources"], 2)

    def test_invalid_domain_and_supported_claim_without_locator_fail(self):
        result = self.run_checker(INVALID)
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        codes = {issue["code"] for issue in payload["issues"]}
        self.assertIn("INVALID_DOMAIN", codes)
        self.assertIn("SUPPORTED_WITHOUT_EVIDENCE_LOCATOR", codes)
        self.assertIn("EMPTY_VALIDATION_NEEDED", codes)


if __name__ == "__main__":
    unittest.main()
