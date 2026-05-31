import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_claim_evidence_map.py"


class ClaimEvidenceMapTests(unittest.TestCase):
    def run_checker(self, text: str):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as handle:
            handle.write(text)
            temp_path = Path(handle.name)
        try:
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(temp_path), "--format", "json"],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
        finally:
            temp_path.unlink(missing_ok=True)

    def test_supported_claim_evidence_map_passes(self):
        result = self.run_checker(
            "## Claim-Evidence Map\n"
            "Claim: The method improves cell-state separation. | "
            "Evidence: Fig. 2b shows a higher silhouette score. | "
            "Status: supported\n"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["issues"], [])

    def test_utf8_bom_claim_line_is_detected(self):
        result = self.run_checker(
            "\ufeffClaim: The method improves separation. | "
            "Evidence: Fig. 1b shows higher silhouette score. | "
            "Status: supported\n"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["claims"], 1)

    def test_missing_evidence_and_weak_paragraph_flow_are_reported(self):
        result = self.run_checker(
            "本文提出了一种新方法。该方法很好。另一个完全不同的观点也在这里出现。"
            "此外，相关研究很多，因此本文具有重要意义。\n\n"
            "Claim: The method is broadly applicable. | Evidence:  | Status: supported\n"
        )
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        codes = {issue["code"] for issue in payload["issues"]}
        self.assertIn("EMPTY_EVIDENCE", codes)
        self.assertIn("WEAK_PARAGRAPH_FLOW", codes)


if __name__ == "__main__":
    unittest.main()
