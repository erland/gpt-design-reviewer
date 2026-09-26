#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import zipfile
import yaml

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact",required=True)
    args=ap.parse_args()
    artifact=Path(args.artifact)
    if not artifact.is_absolute():
        artifact=ROOT/artifact

    errors=[]
    project=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    cfg=project["runtime"]["custom_gpt"]

    if not artifact.is_file():
        print(f"FAILED: Custom GPT artifact missing: {artifact}")
        return 1

    with zipfile.ZipFile(artifact) as zf:
        names=set(zf.namelist())
        required=[
            "builder/instructions.md",
            "builder/conversation-starters.md",
            "builder/capabilities.md",
            "builder/runtime-contract.json",
            "builder/compilation-report.json",
            "README.md",
            "COMPATIBILITY.md",
            "VERSION",
            "MANIFEST.json",
        ]
        for name in required:
            if name not in names:
                errors.append(f"missing Custom GPT member: {name}")

        if "builder/instructions.md" in names:
            instruction=zf.read("builder/instructions.md").decode("utf-8")
            if len(instruction)>int(cfg["instruction"]["max_characters"]):
                errors.append("compiled instruction exceeds configured budget")
            folded=instruction.casefold()
            for marker in [
                "## design review",
                "## evidens",
                "## tre slutartefakter",
                "## stegvis analys",
                "gör nästa steg",
                "unrun verification",
                "får aldrig redovisas som pass",
                "workspace-state har uppdaterats",
                "slutartefakter har skapats",
            ]:
                if marker not in folded:
                    errors.append(f"compiled instruction missing 1.5 marker: {marker}")

        if "builder/compilation-report.json" in names:
            report=json.loads(zf.read("builder/compilation-report.json").decode("utf-8"))
            inst=report.get("instruction",{})
            if inst.get("compiled_characters",999999)>inst.get("max_characters",0):
                errors.append("compilation report exceeds instruction budget")
            knowledge=report.get("knowledge",{})
            if knowledge.get("selected_files",999)>knowledge.get("max_files",0):
                errors.append("Knowledge selection exceeds platform limit")
            if len(knowledge.get("selected",[]))!=knowledge.get("selected_files"):
                errors.append("Knowledge selection traceability mismatch")

        if "builder/runtime-contract.json" in names:
            contract=json.loads(zf.read("builder/runtime-contract.json").decode("utf-8"))
            if contract.get("runtime_id")!="chatgpt_custom":
                errors.append("runtime_id must be chatgpt_custom")
            adapter=contract.get("adapter",{})
            if adapter.get("tool_execution")!="not_embedded":
                errors.append("Custom GPT tool_execution must remain not_embedded")
            states={x.get("id"):x for x in adapter.get("tool_states",[])}
            required_blocking=["filesystem-read","filesystem-list-search"]
            for tid in required_blocking:
                if states.get(tid,{}).get("state")!="missing":
                    errors.append(f"{tid} must remain explicitly missing when required capability is unavailable")
            inventory=states.get("source-tree-inventory-script",{})
            if inventory.get("state")!="reduced" or inventory.get("runtime_fallback")!="degrade":
                errors.append("deterministic inventory script must remain reduced/degrade")

            ws=contract.get("workspace_state",{})
            state=ws.get("state",{})
            if state.get("authority")!="workspace_file":
                errors.append("workspace state authority mismatch")
            if state.get("conversation_fallback") is not False:
                errors.append("conversation must not become authoritative state")

        knowledge_files=[n for n in names if n.startswith("builder/knowledge-package/") and not n.endswith("/")]
        if len(knowledge_files)>int(cfg["knowledge"]["max_files"]):
            errors.append("packaged Knowledge file count exceeds limit")

        forbidden_prefixes=("scripts/","tests/","evals/","contracts/")
        for name in names:
            if name.startswith(forbidden_prefixes):
                errors.append(f"forbidden development/runtime content in Custom GPT ZIP: {name}")

    if errors:
        print("FAILED: Custom GPT GPT Builder 1.5 verification")
        for e in errors: print("-",e)
        return 1

    print("OK: Custom GPT GPT Builder 1.5 verification")
    print("Instruction budget, Knowledge traceability, reduced tools/state semantics and no-false-PASS preserved")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
