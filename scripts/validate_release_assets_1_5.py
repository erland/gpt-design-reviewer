#!/usr/bin/env python3
from pathlib import Path
import argparse
import yaml

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"runtime-distribution-registry.yaml"

def expected_assets(version):
    registry=yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assets=[]
    if registry["release"].get("include_project_artifact"):
        assets.append(registry["project_artifact"]["artifact_pattern"])
    for rid in registry["active_targets"]:
        assets.append(registry["targets"][rid]["artifact_pattern"].format(version=version))
    for key in registry["release"].get("include_derived_artifacts",[]):
        assets.append(registry["derived_artifacts"][key])
    return assets

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--version",required=True)
    ap.add_argument("--dir",default="dist")
    ap.add_argument("--print-paths",action="store_true")
    ns=ap.parse_args()
    out=Path(ns.dir)
    if not out.is_absolute():
        out=ROOT/out

    expected=expected_assets(ns.version)
    missing=[name for name in expected if not (out/name).is_file()]
    expected_zips=sorted(name for name in expected if name.endswith(".zip"))
    actual_zips=sorted(p.name for p in out.glob("*.zip"))

    if missing:
        raise SystemExit("FAILED: missing release assets: "+", ".join(missing))
    if actual_zips!=expected_zips:
        raise SystemExit(f"FAILED: exact ZIP asset set mismatch: actual={actual_zips} expected={expected_zips}")

    if ns.print_paths:
        for name in expected:
            print(out/name)
    else:
        print("OK: exact registry-driven release asset set verified")
        for name in expected:
            print(name)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
