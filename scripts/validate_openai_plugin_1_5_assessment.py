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

    plugin=registry.get("inactive_targets",{}).get("openai_plugin",{})
    if plugin.get("status")!="not_active":
        errors.append("registry plugin status must be not_active")
    if plugin.get("compatibility")!="reduced":
        errors.append("registry plugin compatibility must be reduced")
    if plugin.get("advisory_only") is not True:
        errors.append("registry plugin must remain advisory_only")

    nplugin=normalized.get("runtime_policy",{}).get("openai_plugin",{})
    if nplugin.get("status")!="not_active":
        errors.append("normalized plugin status must be not_active")
    if nplugin.get("target")!="reduced":
        errors.append("normalized plugin target must be reduced")
    if nplugin.get("advisory_only") is not True:
        errors.append("normalized plugin must remain advisory_only")

    if "openai_plugin" in registry.get("active_targets",[]):
        errors.append("OpenAI Plugin must not be active")
    if "openai_plugin" in registry.get("targets",{}):
        errors.append("OpenAI Plugin must not have an active distribution target")
    if "openai_plugin" in project.get("build_system",{}).get("targets",[]):
        errors.append("OpenAI Plugin must not be in build_system.targets")

    required_markers=[
        "not_active",
        "reduced",
        "advisory_only",
        "källkodsträd",
        "persistent workspace/state",
        "project-status.yaml",
        "gör nästa steg",
        "design-review.md",
        "recommended-solution-strategy.md",
        "implementation-plan.md",
        "unrun verification",
        "får aldrig redovisas som pass",
        "ingen openai plugin-distribution",
    ]
    for marker in required_markers:
        if marker.casefold() not in doc:
            errors.append(f"assessment missing marker: {marker}")

    if errors:
        print("FAILED: OpenAI Plugin GPT Builder 1.5 compatibility assessment")
        for e in errors: print("-",e)
        return 1
    print("OK: OpenAI Plugin remains not_active/reduced/advisory_only")
    print("No active distribution, release asset or full peer-runtime parity is claimed")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
