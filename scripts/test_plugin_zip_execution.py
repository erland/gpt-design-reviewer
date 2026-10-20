#!/usr/bin/env python3
"""End-to-end test the original analyzer extracted from the built Plugin ZIP."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

SKILLS = ("source-analysis", "design-review-workflow")

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--project-root",default=".")
    p.add_argument("--version",required=True)
    args=p.parse_args()
    archive=Path(args.project_root)/"dist"/f"design-reviewer-plugin-{args.version}.zip"
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        assert z.testzip() is None
        for skill in ("source-analysis", "design-review", "solution-strategy", "implementation-planning", "design-review-workflow"):
            doc=z.read(f"skills/{skill}/SKILL.md").decode()
            assert f"  version: {args.version}" in doc, f"Version missing in {skill}"
        with tempfile.TemporaryDirectory(prefix="design-reviewer-plugin-e2e-") as tmp:
            root=Path(tmp)
            fixtures=root/"sample-project"
            fixtures.mkdir()
            (fixtures/"service.py").write_text(
                "from storage import write_order\n\ndef checkout(order):\n"
                "    return write_order(order)\n",encoding="utf-8"
            )
            (fixtures/"storage.py").write_text(
                "def write_order(order):\n    return {'id': 1, 'order': order}\n",encoding="utf-8"
            )
            for skill in SKILLS:
                prefix=f"skills/{skill}/scripts/"
                resources=[n for n in names if n.startswith(prefix) and n.endswith(".py")]
                assert any(n.endswith("analyze_source_tree.py") for n in resources)
                assert any(n.endswith("/lib/source_inventory.py") for n in resources)
                for n in resources:
                    target=root/n
                    target.parent.mkdir(parents=True,exist_ok=True)
                    target.write_bytes(z.read(n))
                tool=root/prefix/"analyze_source_tree.py"
                proc=subprocess.run([sys.executable,str(tool),str(fixtures)],
                                    cwd=root,capture_output=True,text=True,timeout=30)
                assert proc.returncode==0,(skill,proc.stderr)
                result=json.loads(proc.stdout)
                assert isinstance(result,dict),(skill,result)
                serialized=json.dumps(result)
                assert "service.py" in serialized and "storage.py" in serialized, (skill,result)
                print(f"PASS {skill}: original packaged Python analyzer executed on realistic source fixture")
    print("PASS: plugin ZIP executable integration and all five explicit skill versions")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
