#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def main():
    errors=[]
    registry=yaml.safe_load((ROOT/"runtime-distribution-registry.yaml").read_text(encoding="utf-8"))
    project=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    normalized=yaml.safe_load((ROOT/"gpt-builder-1.5-contract.yaml").read_text(encoding="utf-8"))

    if registry["builder_contract"]["target_version"]!="1.5.0":
        errors.append("registry target_version must be 1.5.0")
    if registry["builder_contract"]["runtime_selection"]!="active_targets":
        errors.append("runtime selection must use active_targets")
    if registry["builder_contract"]["artifact_policy"]!="exact_active_target_set":
        errors.append("artifact policy must be exact_active_target_set")

    active=registry["active_targets"]
    if active!=normalized["runtime_policy"]["active"]:
        errors.append("active targets differ from normalized 1.5 contract")

    configured=project["build_system"]["targets"]
    if configured!=["project",*active]:
        errors.append("gpt-project build_system.targets must equal project + active_targets")

    for rid in active:
        target=registry["targets"].get(rid,{})
        source=project["build_system"]["runtime_targets"].get(rid,{})
        if target.get("status")!="active":
            errors.append(f"{rid}: registry status must be active")
        if target.get("runtime_id")!=source.get("runtime_id"):
            errors.append(f"{rid}: runtime_id mismatch")
        if target.get("runtime_key")!=source.get("runtime_key"):
            errors.append(f"{rid}: runtime_key mismatch")
        if target.get("builder")!=source.get("builder"):
            errors.append(f"{rid}: builder mismatch")
        expected=(source.get("filename_pattern") or "").replace("<project-id>",project["project"]["id"]).replace("<version>","{version}")
        if target.get("artifact_pattern")!=expected:
            errors.append(f"{rid}: artifact pattern mismatch")

    plugin=registry["targets"].get("plugin",{})
    if plugin.get("status")!="active":
        errors.append("OpenAI Plugin registry target must be active")
    if plugin.get("compatibility")!="equivalent_runtime_dependent":
        errors.append("OpenAI Plugin compatibility must be equivalent_runtime_dependent")
    if plugin.get("runtime_id")!="openai_plugin":
        errors.append("OpenAI Plugin runtime_id mismatch")

    release=registry["release"]
    if release.get("runtime_assets_from")!="active_targets":
        errors.append("release assets must derive from active_targets")
    if release.get("wildcard_runtime_selection") is not False:
        errors.append("wildcard runtime selection must be false")

    if errors:
        print("FAILED: GPT Builder 1.5 runtime distribution registry")
        for e in errors: print("-",e)
        return 1
    print("OK: GPT Builder 1.5 runtime distribution registry")
    print("Active runtimes, artifact patterns and compatibility are synchronized")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
