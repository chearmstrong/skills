import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "triage_copilot_threads.py"


class TriageOverviewTests(unittest.TestCase):
    def run_triage(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        payload = {
            "pull_request": {"owner": "example", "repo": "repo", "number": 1, "url": "https://example.test/pr/1"},
            "summary": {"selected_threads": 0, "suppressed_parse_statuses": ["present_unparsed"]},
            "threads": [], "suppressed_findings": [],
            "review_overviews": [{
                "id": "PRR_1", "suppressed_parse_status": "present_unparsed",
                "body": "### Previously missed (1)\nUnrecognised format",
            }],
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "inventory.json"
            source.write_text(json.dumps(payload), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(source), *arguments],
                check=False, capture_output=True, text=True,
            )

    def test_text_warns_when_an_overview_cannot_be_parsed(self) -> None:
        result = self.run_triage()

        self.assertEqual(result.returncode, 0)
        self.assertIn("PRR_1", result.stdout)
        self.assertIn("present_unparsed", result.stdout)

    def test_json_retains_raw_overview_for_manual_inspection(self) -> None:
        result = self.run_triage("--json")

        self.assertEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["review_overviews"][0]["body"], "### Previously missed (1)\nUnrecognised format")


if __name__ == "__main__":
    unittest.main()
