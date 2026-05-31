import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_skill_metadata.py"


class SkillMetadataTests(unittest.TestCase):
    def run_checker(self, skills_root: Path):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(skills_root), "--format", "json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_all_repo_skills_have_required_metadata(self):
        result = self.run_checker(ROOT / "skills")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertGreaterEqual(len(payload["skills"]), 6)
        self.assertEqual(payload["issues"], [])

    def test_missing_data_access_level_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "sample-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\n"
                "name: sample-skill\n"
                "description: Use when testing missing metadata.\n"
                "version: \"0.1\"\n"
                "last_updated: \"2026-05-31\"\n"
                "status: draft\n"
                "task_type: open-ended\n"
                "related_skills: []\n"
                "---\n",
                encoding="utf-8",
            )

            result = self.run_checker(Path(tmp))
            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertIn("MISSING_FIELD", {issue["code"] for issue in payload["issues"]})


if __name__ == "__main__":
    unittest.main()
