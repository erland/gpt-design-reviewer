#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact",required=True)
    ns=ap.parse_args()
    artifact=Path(ns.artifact)
    errors=[]

    with zipfile.ZipFile(artifact) as zf:
        names=set(zf.namelist())
        required={
            "plugin.json",
            "runtime-contract.json",
            "README.md",
            "VERSION",
            "MANIFEST.json",
            "skills/design-review-workflow/SKILL.md",
            "skills/design-review-workflow/scripts/analyze_source_tree.py",
            "skills/design-review-workflow/scripts/lib/source_inventory.py",
        }
        missing=sorted(required-names)
        if missing:
            errors.append("missing plugin members: "+", ".join(missing))

        if "runtime-contract.json" in names:
            contract=json.loads(zf.read("runtime-contract.json").decode("utf-8"))
            if contract.get("runtime_id")!="openai_plugin":
                errors.append("runtime_id mismatch")
            adapter=contract.get("adapter",{})
            if adapter.get("compatibility")!="equivalent_runtime_dependent":
                errors.append("compatibility mismatch")
            req=adapter.get("runtime_requirements",{})
            if req.get("filesystem",{}).get("read")!="required" or req.get("filesystem",{}).get("write")!="required":
                errors.append("filesystem read/write requirements missing")
            if req.get("persistent_state",{}).get("level")!="required":
                errors.append("persistent state requirement missing")
            if req.get("code_execution",{}).get("level")!="recommended":
                errors.append("code execution must be recommended")
            resources=adapter.get("script_resources",{})
            if "scripts/analyze_source_tree.py" not in resources.get("packaged",[]):
                errors.append("analyze_source_tree.py not declared as packaged script resource")
            if resources.get("mcp_required_for_resource_use") is not False:
                errors.append("script resource must not require MCP wrapper")

        if "skills/design-review-workflow/SKILL.md" in names:
            skill=zf.read("skills/design-review-workflow/SKILL.md").decode("utf-8")
            for marker in (
                "name: design-review-workflow",
                "## Runtime requirements",
                "Code execution is recommended",
                "continue semantic analysis",
                "## Canonical behavior",
                "## Scripts",
            ):
                if marker not in skill:
                    errors.append(f"SKILL.md missing marker: {marker}")

    if errors:
        print("FAILED: OpenAI Plugin GPT Builder 1.5 runtime")
        for e in errors:
            print("-",e)
        return 1
    print("OK: OpenAI Plugin GPT Builder 1.5 runtime")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
