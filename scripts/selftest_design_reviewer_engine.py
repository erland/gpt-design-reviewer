#!/usr/bin/env python3
"""Verify the unmodified Design Reviewer Engine analyzer in an isolated fixture."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
import tempfile

def main() -> int:
    script = Path(__file__).resolve().parent / "analyze_source_tree.py"
    with tempfile.TemporaryDirectory(prefix="design-reviewer-engine-") as temp:
        fixture = Path(temp) / "sample"
        fixture.mkdir()
        (fixture / "order.py").write_text(
            "def calculate_total(price, quantity):\n    return price * quantity\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, "-B", str(script), str(fixture)],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode:
            print(result.stderr, file=sys.stderr)
            return result.returncode
        data = json.loads(result.stdout)
        if "order.py" not in json.dumps(data):
            raise AssertionError("Analyzer output missing fixture source")
        print("PASS: original analyzer imports and analyzes sample source")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
