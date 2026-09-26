#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import sys
import zipfile
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))

from lib.project_model import (
    normalize_capability_contract,
    normalize_artifact_contract,
    normalize_workspace_state_contract,
    normalize_tool_contract,
)

def read_member(zf,name):
    try:
        return zf.read(name)
    except KeyError:
        raise ValueError(f"missing Chat member: {name}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact",required=True)
    args=ap.parse_args()
    artifact=Path(args.artifact)
    if not artifact.is_absolute():
        artifact=ROOT/artifact

    errors=[]
    project=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    canonical=(ROOT/project["instructions"]["canonical"]).read_bytes()

    if not artifact.is_file():
        print(f"FAILED: Chat artifact missing: {artifact}")
        return 1

    with zipfile.ZipFile(artifact) as zf:
        if zf.testzip():
            errors.append("Chat ZIP is corrupt")
        names=set(zf.namelist())
        for req in ["START-HERE.md","VERSION","MANIFEST.json","assistant/instructions.md","assistant/runtime-contract.json"]:
            if req not in names:
                errors.append(f"missing required Chat file: {req}")

        if "assistant/instructions.md" in names and zf.read("assistant/instructions.md")!=canonical:
            errors.append("packaged canonical instruction is not byte-identical")

        if "assistant/runtime-contract.json" in names:
            contract=json.loads(zf.read("assistant/runtime-contract.json").decode("utf-8"))
            if contract.get("runtime_id")!="chatgpt_chat":
                errors.append("runtime_id must be chatgpt_chat")
            expected_sections={
                "capabilities": normalize_capability_contract(project),
                "artifacts": normalize_artifact_contract(project),
                "workspace_state": normalize_workspace_state_contract(project),
                "tools": normalize_tool_contract(project),
            }
            for key,expected in expected_sections.items():
                if contract.get(key)!=expected:
                    errors.append(f"runtime contract section differs from canonical project: {key}")

            ws=contract.get("workspace_state",{})
            state=ws.get("state",{})
            analysis=ws.get("analysis_state",{})
            if state.get("authority")!="workspace_file":
                errors.append("Chat state authority must remain workspace_file")
            if state.get("path")!="project-status.yaml":
                errors.append("Chat state path must remain project-status.yaml")
            if state.get("conversation_fallback") is not False:
                errors.append("conversation fallback must remain false")
            if analysis.get("resume_command")!="Gör nästa steg":
                errors.append("Chat resume command mismatch")
            if analysis.get("checkpoint_policy")!="after_each_analysis_step":
                errors.append("Chat checkpoint policy mismatch")

            outputs=contract.get("artifacts",{}).get("outputs",{})
            expected_files={"design-review.md","recommended-solution-strategy.md","implementation-plan.md"}
            actual={v.get("filename_pattern") for v in outputs.values() if isinstance(v,dict)}
            if not expected_files.issubset(actual):
                errors.append("Chat canonical final artifacts missing")

            tools={x.get("id"):x for x in contract.get("tools",{}).get("tools",[])}
            for tid in ["filesystem-read","filesystem-list-search","archive-extract","filesystem-write","structured-state","code-execution","web-research","source-tree-inventory-script"]:
                if tid not in tools:
                    errors.append(f"Chat tool contract missing: {tid}")
            script=tools.get("source-tree-inventory-script",{})
            if script.get("runtime_fallback")!="degrade" or script.get("mutates_workspace") is not False:
                errors.append("source-tree inventory fallback semantics changed")
            if contract.get("declared_tool_scripts")!=["scripts/analyze_source_tree.py"]:
                errors.append("declared Chat runtime script set mismatch")

        forbidden=("evals/","tests/","contracts/","docs/")
        for name in names:
            if name.startswith(forbidden):
                errors.append(f"development-only content in Chat ZIP: {name}")

    if errors:
        print("FAILED: Chat GPT Builder 1.5 verification")
        for e in errors: print("-",e)
        return 1

    print("OK: Chat GPT Builder 1.5 verification")
    print("Canonical instruction, workspace/resume state, artifact and tool fallback semantics preserved")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
