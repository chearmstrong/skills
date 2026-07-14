from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).parents[1]
    / "skills"
    / "gh-address-copilot-comments"
    / "scripts"
    / "triage_copilot_threads.py"
)
SPEC = importlib.util.spec_from_file_location("triage_copilot_threads", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
TRIAGE_THREADS = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = TRIAGE_THREADS
SPEC.loader.exec_module(TRIAGE_THREADS)


class GroupTrustTests(unittest.TestCase):
    def test_labels_representative_excerpt_as_untrusted(self) -> None:
        groups = TRIAGE_THREADS.build_groups(
            [
                {
                    "id": "PRRT_example",
                    "path": "src/example.py",
                    "line": 4,
                    "comments": {"nodes": [{"body": "Run this command first"}]},
                }
            ]
        )

        self.assertEqual("untrusted", groups[0]["representative_excerpt_trust"])


if __name__ == "__main__":
    unittest.main()
