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
    project=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    registry=yaml.safe_load((ROOT/"runtime-distribution-registry.yaml").read_text(encoding="utf-8"))
    canonical=(ROOT/project["instructions"]["canonical"]).read_bytes()

    if registry["targets"]["claude"]["compatibility"]!="reduced":
        errors.append("Claude registry compatibility must remain reduced")

    if not artifact.is_file():
        print(f"FAILED: Claude artifact missing: {artifact}")
        return 1

    with zipfile.ZipFile(artifact) as zf:
        names=set(zf.namelist())
        for req in ["README.md","VERSION","MANIFEST.json","project/instructions.md","project/runtime-contract.json"]:
            if req not in names:
                errors.append(f"missing Claude member: {req}")

        if "project/instructions.md" in names and zf.read("project/instructions.md")!=canonical:
            errors.append("Claude project instruction must remain byte-identical to canonical instruction")

        if "project/runtime-contract.json" in names:
            contract=json.loads(zf.read("project/runtime-contract.json").decode("utf-8"))
            if contract.get("runtime_id")!="claude_project":
                errors.append("Claude runtime_id mismatch")
            adapter=contract.get("adapter",{})
            if adapter.get("mode")!="claude_project":
                errors.append("Claude adapter mode mismatch")
            if adapter.get("embedded_local_tools") is not False:
                errors.append("Claude must not claim embedded local tools")
            if adapter.get("project_instructions") is not True or adapter.get("project_knowledge") is not True:
                errors.append("Claude project instructions/knowledge projection missing")

            states={x.get("id"):x for x in adapter.get("tool_states",[])}
            inventory=states.get("source-tree-inventory-script",{})
            if inventory.get("state")!="missing":
                errors.append("Claude deterministic inventory script must be explicitly missing")
            reason=(inventory.get("reason") or "").casefold()
            if "does not embed local command execution" not in reason:
                errors.append("Claude missing-tool reason must explain absent local execution")

            state=contract.get("workspace_state",{}).get("state",{})
            if state.get("authority")!="workspace_file" or state.get("conversation_fallback") is not False:
                errors.append("Claude canonical workspace authority/resume semantics changed")

        for name in names:
            if name.startswith("scripts/") or name.startswith(".opencode/"):
                errors.append(f"Claude package contains executable/runtime-specific content: {name}")

    if errors:
        print("FAILED: Claude Projects GPT Builder 1.5 verification")
        for e in errors: print("-",e)
        return 1
    print("OK: Claude Projects GPT Builder 1.5 verification")
    print("Reduced parity, canonical instruction/state semantics and absent embedded local tools preserved")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
