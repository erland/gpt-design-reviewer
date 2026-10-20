#!/usr/bin/env python3
"""Verify built Engine ZIP integrity, version, parity and execute original selftest."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    archive = root / "dist" / f"design-reviewer-engine-{args.version}.zip"
    plugin = root / "dist" / f"design-reviewer-plugin-{args.version}.zip"
    with zipfile.ZipFile(archive) as engine, zipfile.ZipFile(plugin) as skills:
        assert engine.testzip() is None
        manifest = json.loads(engine.read("engine-package.json"))
        assert manifest["version"] == args.version
        assert manifest["engine_id"] == "design-reviewer"
        files = manifest["files"]
        assert set(manifest["required_files"]) <= set(files)
        for name, expected in files.items():
            data = engine.read(name)
            assert hashlib.sha256(data).hexdigest() == expected, name
        for skill in ("source-analysis", "design-review-workflow"):
            for rel in ("analyze_source_tree.py", "lib/source_inventory.py", "lib/__init__.py"):
                source = engine.read("scripts/" + rel)
                installed = skills.read(f"skills/{skill}/scripts/{rel}")
                assert source == installed, (skill, rel)
        with tempfile.TemporaryDirectory(prefix="design-reviewer-engine-test-") as temp:
            destination = Path(temp)
            for name in files:
                target = destination / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(engine.read(name))
            script = destination / manifest["entrypoint"]
            result = subprocess.run([sys.executable, "-B", str(script)],
                                    cwd=destination, capture_output=True,
                                    text=True, timeout=30)
            assert result.returncode == 0, result.stderr
            assert "PASS" in result.stdout, result.stdout
            print(result.stdout.strip())
    print("PASS: Engine version, hashes, canonical parity and selftest")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
