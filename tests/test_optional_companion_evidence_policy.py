"""Offline static contract tests for optional companion-evidence policy."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class OptionalEvidencePolicyTest(unittest.TestCase):
    def test_core_is_short_and_optional(self):
        core = (ROOT / "assistant/core.md").read_text(encoding="utf-8")
        self.assertLess(len(core), 6000)
        for term in ("Agent Workspace", "PWA Preview", "Browser Screenshot", "VA-åtgärd", "valfria"):
            self.assertIn(term, core)

    def test_review_does_not_confuse_evidence_with_inference(self):
        text = (ROOT / "assistant/policies/optional-companion-evidence.md").read_text(encoding="utf-8")
        for term in ("NOT VERIFIED", "environment_limited", "DR-observation", "VA-valideringsåtgärd",
                     "skärmbild", "smoke", "källrevision", "backendtimeout"):
            self.assertIn(term.casefold(), text.casefold())

    def test_zip_and_privacy_remain_safe(self):
        text = (ROOT / "assistant/policies/optional-companion-evidence.md").read_text(encoding="utf-8")
        self.assertIn("ZIP-läge kräver inte GitHub", text)
        self.assertIn("offentlig temporär exponering", text)
        self.assertIn("inte anropa live-MCP", text)


if __name__ == "__main__":
    unittest.main()
