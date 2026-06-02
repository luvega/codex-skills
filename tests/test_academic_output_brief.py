import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_academic_output_brief.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures"


class AcademicOutputBriefTests(unittest.TestCase):
    def run_checker(self, fixture_name: str):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE_DIR / fixture_name), "--format", "json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_valid_review_outline_passes(self):
        result = self.run_checker("valid_review_outline_brief.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["issues"], [])
        self.assertEqual(payload["summary"]["brief_type"], "review_outline")

    def test_valid_ppt_storyboard_passes(self):
        result = self.run_checker("valid_ppt_storyboard_brief.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["issues"], [])
        self.assertEqual(payload["summary"]["brief_type"], "ppt_storyboard")

    def test_valid_lesson_plan_passes(self):
        result = self.run_checker("valid_lesson_plan_brief.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["issues"], [])
        self.assertEqual(payload["summary"]["brief_type"], "lesson_plan")

    def test_valid_algorithm_explanation_passes(self):
        result = self.run_checker("valid_algorithm_explanation_brief.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["issues"], [])
        self.assertEqual(payload["summary"]["brief_type"], "algorithm_explanation")

    def test_ppt_storyboard_missing_audience_slide_plan_and_evidence_map_fails(self):
        result = self.run_checker("invalid_ppt_storyboard_brief.json")
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        codes = {issue["code"] for issue in payload["issues"]}
        self.assertIn("MISSING_FIELD", codes)
        self.assertIn("EMPTY_SLIDE_PLAN", codes)
        self.assertIn("EMPTY_EVIDENCE_MAP", codes)

    def test_lesson_plan_missing_objectives_and_assessment_fails(self):
        result = self.run_checker("invalid_lesson_plan_brief.json")
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        pointers = {issue["pointer"] for issue in payload["issues"]}
        self.assertIn("/learning_objectives", pointers)
        self.assertIn("/assessment_prompts", pointers)


if __name__ == "__main__":
    unittest.main()
