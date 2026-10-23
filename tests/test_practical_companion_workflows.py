"""Static regression guards for optional operational review workflows (offline)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PracticalCompanionWorkflowsTest(unittest.TestCase):
    def test_operational_safety_and_evidence_contract(self):
        doc = (ROOT / "assistant/policies/companion-review-workflows.md").read_text(encoding="utf-8")
        for expected in ("project_verify", "project_build", "file_read", "artifact_download_link",
                         "PWA Preview", "Browser Screenshot", "DR-*", "VA-*",
                         "NOT VERIFIED", "environment_limited", "Radera preview",
                         "Stäng session", "tokens", "GitHub CI", "källkodsläsning"):
            self.assertIn(expected, doc)

    def test_skills_reference_optional_workflow(self):
        for skill in ("source-analysis", "design-review", "design-review-workflow"):
            doc = (ROOT / f"assistant/skills/{skill}.md").read_text(encoding="utf-8")
            self.assertIn("assistant/policies/companion-review-workflows.md", doc)
            self.assertIn("valfria", doc.lower())

    def test_existing_core_stays_small(self):
        core = (ROOT / "assistant/core.md").read_text(encoding="utf-8")
        self.assertLess(len(core), 6000)


if __name__ == "__main__":
    unittest.main()
