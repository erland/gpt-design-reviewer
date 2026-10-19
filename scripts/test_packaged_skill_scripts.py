#!/usr/bin/env python3
"""Smoke-test all packaged copies of the design-review source analyzer."""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    copies = {
        "chat": "build/chat/assistant/skills/design-review-workflow/scripts/analyze_source_tree.py",
        "opencode": "build/opencode/.opencode/skills/design-review-workflow/scripts/analyze_source_tree.py",
        "plugin": "build/plugin/skills/design-review-workflow/scripts/analyze_source_tree.py",
        "claude-skills": "build/claude-skills/skills/design-review-workflow/scripts/analyze_source_tree.py",
    }
    for runtime, relative in copies.items():
        script = root / relative
        dep = script.parent / "lib/source_inventory.py"
        if not script.is_file() or not dep.is_file():
            print(f"FAIL {runtime}: missing script or dependency: {script}; {dep}", file=sys.stderr)
            return 1
        proc = subprocess.run([sys.executable, str(script), "--help"], cwd=root, capture_output=True, text=True)
        if proc.returncode != 0 or "usage:" not in proc.stdout.lower():
            print(f"FAIL {runtime}: {proc.stderr}", file=sys.stderr)
            return 1
        print(f"PASS {runtime}: script imports and CLI startup")
    return 0

if __name__ == "__main__":
    sys.exit(main())
