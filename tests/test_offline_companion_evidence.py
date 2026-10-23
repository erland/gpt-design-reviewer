"""Offline tests: simulated capabilities, no live MCP invocation."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from offline_companion_evidence import choose


class OfflineEvidenceMatrix(unittest.TestCase):
    def test_all_available(self):
        d=choose(agent=True,agent_compatible=True,preview=True,safe_to_publish=True,
                 static_artifact=True,browser=True,browser_interactive=True,
                 requires_runtime_evidence=True,requires_ui_evidence=True)
        self.assertEqual(d.actions,("read_source","agent_workspace_probe","pwa_preview_create","browser_interactive_smoke"))
        self.assertEqual(d.evidence,"planned_not_observed")
        self.assertFalse(d.validation_action)

    def test_agent_absent(self):
        d=choose(requires_runtime_evidence=True)
        self.assertTrue(d.validation_action)
        self.assertEqual(d.limitation,"runtime_evidence_unavailable")

    def test_agent_unsupported_runtime(self):
        d=choose(agent=True,agent_compatible=False,requires_runtime_evidence=True)
        self.assertNotIn("agent_workspace_probe",d.actions)
        self.assertTrue(d.validation_action)

    def test_agent_error(self):
        d=choose(agent=True,agent_compatible=True,agent_error=True,requires_runtime_evidence=True)
        self.assertEqual(d.report,"draft_with_limits")

    def test_local_execution_preferred(self):
        d=choose(local_probe=True,agent=True,agent_compatible=True,requires_runtime_evidence=True)
        self.assertEqual(d.actions,("read_source","local_probe"))

    def test_github_ci_preferred(self):
        d=choose(mode="github",github_ci=True,agent=True,agent_compatible=True,requires_runtime_evidence=True)
        self.assertEqual(d.actions,("read_source","github_ci_probe"))

    def test_zip_without_github(self):
        d=choose(mode="zip",local_probe=True,requires_runtime_evidence=True)
        self.assertEqual(d.actions,("read_source","local_probe"))

    def test_preview_absent_limits_ui(self):
        d=choose(browser=True,browser_interactive=True,requires_ui_evidence=True)
        self.assertTrue(d.validation_action)
        self.assertEqual(d.actions,("read_source",))

    def test_preview_private_source_not_exposed(self):
        d=choose(preview=True,static_artifact=True,safe_to_publish=False,requires_ui_evidence=True)
        self.assertNotIn("pwa_preview_create",d.actions)

    def test_existing_url_skips_preview(self):
        d=choose(existing_url=True,preview=True,safe_to_publish=True,static_artifact=True,
                 browser=True,browser_interactive=True,requires_ui_evidence=True)
        self.assertEqual(d.actions,("read_source","browser_interactive_smoke"))

    def test_browser_absent(self):
        d=choose(existing_url=True,requires_ui_evidence=True)
        self.assertEqual(d.report,"draft_with_limits")

    def test_browser_error(self):
        d=choose(existing_url=True,browser=True,browser_error=True,requires_ui_evidence=True)
        self.assertEqual(d.evidence,"insufficient")

    def test_visual_screenshot_not_interactive(self):
        d=choose(existing_url=True,browser=True,requires_ui_evidence=True)
        self.assertIn("browser_visual_only",d.actions)
        self.assertTrue(d.validation_action)

    def test_missing_source_blocks(self):
        d=choose(source_readable=False,requires_runtime_evidence=True)
        self.assertEqual(d.report,"blocked")
        self.assertEqual(d.evidence,"not_verified")

    def test_static_review_needs_no_plugins(self):
        d=choose()
        self.assertEqual(d.actions,("read_source",))
        self.assertFalse(d.validation_action)

    def test_not_claiming_pass_for_planned_operations(self):
        d=choose(existing_url=True,browser=True,browser_interactive=True,requires_ui_evidence=True)
        self.assertNotEqual(d.evidence,"PASS")
        self.assertEqual(d.report,"draft_pending_execution")

    def test_pure_reference_has_no_external_clients(self):
        source=(Path(__file__).resolve().parents[1]/"scripts/offline_companion_evidence.py").read_text()
        for token in ("mcp__", "requests", "httpx", "urllib", "socket", "subprocess"):
            self.assertNotIn(token,source)


if __name__=="__main__":
    unittest.main()
