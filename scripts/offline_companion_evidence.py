"""Offline reference decision model for Design Reviewer evidence gathering.

Pure planning code: does not call MCP, network, local files or processes.
A planned operation is NEVER a completed observation.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewDecision:
    actions: tuple[str, ...]
    evidence: str
    report: str
    validation_action: bool
    limitation: str | None


def choose(*, source_readable=True, agent=False, agent_compatible=False,
           agent_error=False, local_probe=False, github_ci=False, mode="zip",
           preview=False, safe_to_publish=False, static_artifact=False,
           existing_url=False, browser=False, browser_interactive=False,
           browser_error=False, requires_runtime_evidence=False,
           requires_ui_evidence=False):
    if mode not in ("zip", "github"):
        raise ValueError("invalid mode")
    if not source_readable:
        return ReviewDecision((), "not_verified", "blocked", True, "source_unavailable")

    actions = ["read_source"]
    probe = False
    if requires_runtime_evidence:
        if mode == "github" and github_ci:
            actions.append("github_ci_probe")
            probe = True
        elif local_probe:
            actions.append("local_probe")
            probe = True
        elif agent and agent_compatible and not agent_error:
            actions.append("agent_workspace_probe")
            probe = True

    accessible_url = existing_url
    if requires_ui_evidence and not accessible_url and preview and safe_to_publish and static_artifact:
        actions.append("pwa_preview_create")
        accessible_url = True
    browser_possible = requires_ui_evidence and accessible_url and browser and not browser_error
    interactive = browser_possible and browser_interactive
    if interactive:
        actions.append("browser_interactive_smoke")
    elif browser_possible:
        actions.append("browser_visual_only")

    missing = (requires_runtime_evidence and not probe) or (
        requires_ui_evidence and not interactive)
    reason = None
    if requires_runtime_evidence and not probe:
        reason = "runtime_evidence_unavailable"
    elif requires_ui_evidence and not interactive:
        reason = "interaction_evidence_unavailable"
    return ReviewDecision(tuple(actions), "planned_not_observed" if not missing else "insufficient",
                          "draft_with_limits" if missing else "draft_pending_execution",
                          missing, reason)
