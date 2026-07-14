from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).parents[1]
    / "skills"
    / "review-comments"
    / "scripts"
    / "validate_handoff.py"
)
SPEC = importlib.util.spec_from_file_location("validate_handoff", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATE_HANDOFF = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATE_HANDOFF
SPEC.loader.exec_module(VALIDATE_HANDOFF)


class NormalisedHandoffTests(unittest.TestCase):
    def test_round_trips_quotes_and_backslashes(self) -> None:
        text = 'Preserve "quoted text" and the path C:\\work\\file.py.'
        comment = VALIDATE_HANDOFF.Comment(
            path="src/example.py",
            start=4,
            end=4,
            text=text,
            source_line=1,
        )

        parsed = VALIDATE_HANDOFF.parse_handoff(VALIDATE_HANDOFF.normalise([comment]))

        self.assertEqual([], parsed.errors)
        self.assertEqual([text], [item.text for item in parsed.comments])


if __name__ == "__main__":
    unittest.main()
