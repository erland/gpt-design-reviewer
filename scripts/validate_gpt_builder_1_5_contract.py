#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def fail(errors):
    print("FAILED: GPT Builder 1.5 canonical contract normalization")
    for e in errors:
        print("-", e)
    return 1

def main():
    errors=[]
    normalized=yaml.safe_load((ROOT/"gpt-builder-1.5-contract.yaml").read_text(encoding="utf-8"))
    project=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    status=yaml.safe_load((ROOT/"project-status.yaml").read_text(encoding="utf-8"))
    instruction=(ROOT/project["instructions"]["canonical"]).read_text(encoding="utf-8")

    if normalized["builder"]["target_version"]!="1.5.0":
        errors.append("target builder version must be 1.5.0")
    if normalized["builder"]["behavior_preserving"] is not True:
        errors.append("migration must remain behavior-preserving")
    if project["instructions"]["canonical"]!=normalized["canonical"]["instruction"]:
        errors.append("canonical instruction mismatch")

    capabilities={x["id"]:x for x in project["capabilities"]["capability_catalog"]}
    for cid in normalized["contracts"]["capabilities"]["required"]:
        if cid not in capabilities or capabilities[cid].get("requirement")!="required":
            errors.append(f"required capability mismatch: {cid}")

    outputs=project["artifacts"]["outputs"]
    for aid,filename in normalized["contracts"]["artifacts"]["required"].items():
        if aid not in outputs:
            errors.append(f"required artifact missing: {aid}")
        elif outputs[aid].get("filename_pattern")!=filename:
            errors.append(f"artifact filename mismatch: {aid}")

    ws=project["workspace_state"]
    state=ws["state"]
    analysis=ws["analysis_state"]
    expected=normalized["contracts"]["state"]
    if state.get("authority")!=expected["authority"]:
        errors.append("workspace state authority mismatch")
    if state.get("path")!=expected["state_path"]:
        errors.append("workspace state path mismatch")
    if state.get("persistence")!=expected["persistent"]:
        errors.append("workspace state persistence mismatch")
    if state.get("conversation_fallback") is not False:
        errors.append("conversation history must not be authoritative state")
    if ws["workspace"].get("portable") is not True or ws["workspace"].get("separate_from_assistant") is not True:
        errors.append("workspace must remain portable and separate from assistant")
    if analysis.get("checkpoint_policy")!=expected["checkpoint_policy"]:
        errors.append("checkpoint policy mismatch")
    if analysis.get("resume_command")!=expected["resume_command"]:
        errors.append("resume command mismatch")
    if analysis.get("incremental") is not True:
        errors.append("incremental analysis must remain enabled")

    tools={x["id"]:x for x in project["tools"]["tools"]}
    for tid in normalized["contracts"]["tools"]["required"]:
        if tid not in tools:
            errors.append(f"required tool contract missing: {tid}")
    script=tools.get("source-tree-inventory-script",{})
    if script.get("script")!="scripts/analyze_source_tree.py":
        errors.append("source-tree inventory script mismatch")
    if project["deterministic_analysis_tools"].get("evidence_only") is not True:
        errors.append("deterministic analysis tools must remain evidence-only")
    if project["deterministic_analysis_tools"].get("core_review_blocks_if_unavailable") is not False:
        errors.append("core review must degrade rather than block when deterministic script is unavailable")

    workflow=project["analysis_workflow"]
    if workflow.get("modes")!=["focused","progressive"]:
        errors.append("analysis modes mismatch")
    if workflow.get("final_stage_requires_evidence_gate") is not True:
        errors.append("final evidence gate must remain required")
    if workflow.get("resume_command")!="Gör nästa steg":
        errors.append("analysis workflow resume command mismatch")

    if project["observation_model"].get("severity_is_not_priority") is not True:
        errors.append("severity_is_not_priority must remain true")
    if project["solution_prioritization"].get("numeric_score_required") is not False:
        errors.append("numeric priority scoring must remain disabled")
    if project["implementation_planning"].get("sizing_model")!="one_prompt_one_checkpoint":
        errors.append("implementation sizing model mismatch")
    if project["resume"].get("requires_previous_chat_history") is not False:
        errors.append("resume must not require previous chat history")

    for marker in [
        "## Design Review",
        "## Evidens",
        "## Tre slutartefakter",
        "## Stegvis analys",
        "Gör nästa steg",
    ]:
        if marker not in instruction:
            errors.append(f"canonical instruction missing behavior marker: {marker}")

    progress=status.get("progress",{})
    if progress.get("last_completed_step")!=20 or progress.get("current_phase")!="complete":
        errors.append("product development status must remain 20/20 complete")

    if errors:
        return fail(errors)

    print("OK: GPT Builder 1.5 canonical contract normalization")
    print("Capabilities, artifacts, workspace/state, tools and resume semantics preserved")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
