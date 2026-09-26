#!/usr/bin/env python3
from pathlib import Path
import argparse, json, zipfile, yaml

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact",required=True)
    ns=ap.parse_args()
    artifact=Path(ns.artifact)
    if not artifact.is_absolute():
        artifact=ROOT/artifact
    errors=[]
    registry=yaml.safe_load((ROOT/"runtime-distribution-registry.yaml").read_text(encoding="utf-8"))

    if registry["targets"]["opencode"]["compatibility"]!="equivalent":
        errors.append("OpenCode registry compatibility must remain equivalent")

    if not artifact.is_file():
        print(f"FAILED: OpenCode artifact missing: {artifact}")
        return 1

    with zipfile.ZipFile(artifact) as zf:
        names=set(zf.namelist())
        for req in [
            "AGENTS.md","opencode.json","VERSION","MANIFEST.json",
            ".opencode/design-reviewer-runtime.json",
            ".opencode/skills/design-review-workflow/SKILL.md",
            ".opencode/tools/gpt_source_tree_inventory_script.ts",
            ".opencode/runtime-scripts/analyze_source_tree.py",
        ]:
            if req not in names:
                errors.append(f"missing OpenCode member: {req}")

        if ".opencode/design-reviewer-runtime.json" in names:
            contract=json.loads(zf.read(".opencode/design-reviewer-runtime.json").decode("utf-8"))
            if contract.get("runtime_id")!="opencode":
                errors.append("OpenCode runtime_id mismatch")
            adapter=contract.get("adapter",{})
            if adapter.get("mode")!="opencode_workspace" or adapter.get("workspace_first") is not True:
                errors.append("OpenCode must remain workspace-first")
            if adapter.get("tool_integration")!="custom_tools":
                errors.append("OpenCode must retain custom tool integration")
            if "design-review-workflow" not in adapter.get("skills",[]):
                errors.append("OpenCode design-review workflow skill missing")
            integrations={x.get("id"):x for x in adapter.get("tool_integrations",[])}
            inv=integrations.get("source-tree-inventory-script",{})
            if inv.get("opencode_tool")!="gpt_source_tree_inventory_script":
                errors.append("OpenCode inventory custom tool mapping mismatch")
            if inv.get("permission")!="allow":
                errors.append("non-mutating OpenCode inventory tool must remain allow")
            state=contract.get("workspace_state",{}).get("state",{})
            if state.get("authority")!="workspace_file" or state.get("conversation_fallback") is not False:
                errors.append("OpenCode canonical workspace authority/resume semantics changed")

        if "opencode.json" in names:
            config=json.loads(zf.read("opencode.json").decode("utf-8"))
            permission=config.get("permission",{})
            if permission.get("bash")!="ask":
                errors.append("OpenCode bash permission must remain ask")
            if permission.get("edit")!="ask":
                errors.append("OpenCode edit permission must remain ask")
            if permission.get("gpt_source_tree_inventory_script")!="allow":
                errors.append("OpenCode non-mutating inventory custom tool must remain allow")

        if ".opencode/tools/gpt_source_tree_inventory_script.ts" in names:
            wrapper=zf.read(".opencode/tools/gpt_source_tree_inventory_script.ts").decode("utf-8")
            for marker in ["tool.schema.string().optional()","projectRoot","path.resolve(context.worktree"]:
                if marker not in wrapper:
                    errors.append(f"OpenCode typed tool/projectRoot marker missing: {marker}")

        if "AGENTS.md" in names:
            agents=zf.read("AGENTS.md").decode("utf-8")
            for marker in [
                "Pass projectRoot to generated tools",
                "workspace/state",
                "Gör nästa steg",
            ]:
                if marker.casefold() not in agents.casefold():
                    errors.append(f"OpenCode AGENTS marker missing: {marker}")

    if errors:
        print("FAILED: OpenCode GPT Builder 1.5 verification")
        for e in errors: print("-",e)
        return 1
    print("OK: OpenCode GPT Builder 1.5 verification")
    print("Equivalent workspace parity, skill/custom tool integration, projectRoot and permission policy preserved")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
