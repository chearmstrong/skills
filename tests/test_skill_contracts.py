from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).parents[1]


class SkillContractTests(unittest.TestCase):
    def test_execute_plan_does_not_duplicate_support_and_verification_sections(self) -> None:
        skill = (
            REPO_ROOT
            / "skills"
            / "execute-plan-with-gates"
            / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertNotIn("## Related skills", skill)
        self.assertNotIn("## Verification expectations", skill)

    def test_copilot_check_only_requests_are_read_only(self) -> None:
        skill = (
            REPO_ROOT
            / "skills"
            / "gh-address-copilot-comments"
            / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "Treat requests limited to checking, inspecting, triaging, or verifying as read-only",
            skill,
        )


if __name__ == "__main__":
    unittest.main()
