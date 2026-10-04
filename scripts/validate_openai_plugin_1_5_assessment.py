#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def main():
    errors=[]
    registry=yaml.safe_load((ROOT/"runtime-distribution-registry.yaml").read_text(encoding="utf-8"))
    normalized=yaml.safe_load((ROOT/"gpt-builder-1.5-contract.yaml").read_text(encoding="utf-8"))
    project=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    doc=(ROOT/"docs/openai-plugin-1.5-assessment.md").read_text(encoding="utf-8").casefold()

    plugin=registry.get("targets",{}).get("plugin",{})
    if plugin.get("status")!="active":
        errors.append("registry plugin status must be active")
    if plugin.get("compatibility")!="equivalent_runtime_dependent":
        errors.append("registry plugin compatibility must be equivalent_runtime_dependent")
    if plugin.get("runtime_id")!="openai_plugin":
        errors.append("registry plugin runtime_id must be openai_plugin")

    nplugin=normalized.get("runtime_policy",{}).get("openai_plugin",{})
    if nplugin.get("status")!="active":
        errors.append("normalized plugin status must be active")
    if nplugin.get("target")!="equivalent_runtime_dependent":
        errors.append("normalized plugin target must be equivalent_runtime_dependent")
    if nplugin.get("advisory_only") is not False:
        errors.append("normalized plugin must not be advisory_only")

    if "plugin" not in registry.get("active_targets",[]):
        errors.append("OpenAI Plugin must be active")
    if "plugin" not in project.get("build_system",{}).get("targets",[]):
        errors.append("OpenAI Plugin must be in build_system.targets")
    if not project.get("runtime",{}).get("plugin",{}).get("enabled"):
        errors.append("OpenAI Plugin runtime must be enabled")

    required_markers=[
        "active",
        "equivalent_runtime_dependent",
        "filesystem",
        "persistent workspace/state",
        "project-status.yaml",
        "gör nästa steg",
        "design-review.md",
        "recommended-solution-strategy.md",
        "implementation-plan.md",
        "code execution",
        "recommended",
        "degrade",
        "unrun verification",
        "får aldrig redovisas som pass",
    ]
    for marker in required_markers:
        if marker.casefold() not in doc:
            errors.append(f"assessment missing marker: {marker}")

    if errors:
        print("FAILED: OpenAI Plugin GPT Builder 1.5 compatibility assessment")
        for e in errors: print("-",e)
        return 1
    print("OK: OpenAI Plugin active with equivalent_runtime_dependent compatibility")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
