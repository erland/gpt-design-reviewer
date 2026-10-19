#!/usr/bin/env python3
"""Check modular Design Reviewer skills in source and generated runtime ZIPs."""
import argparse
from pathlib import Path
import zipfile
import yaml

EXPECTED = {"source-analysis", "design-review", "solution-strategy", "implementation-planning", "design-review-workflow"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--project-root", default=".")
    p.add_argument("--version", default="0.0.0-ci")
    a = p.parse_args()
    root = Path(a.project_root)
    cfg = yaml.safe_load((root / "gpt-project.yaml").read_text())
    canonical = cfg["skills"]["definitions"]
    opencode = cfg["runtime"]["opencode"]["skills"]["definitions"]
    for label, defs in (("canonical", canonical), ("OpenCode", opencode)):
        ids = [x["id"] for x in defs]
        assert len(ids) == len(set(ids)), f"Duplicate {label} skill IDs"
        assert EXPECTED.issubset(ids), f"{label}: missing {EXPECTED - set(ids)}"
        for skill in defs:
            assert skill.get("description"), f"Incomplete skill {skill['id']}"
    text = (root / "assistant/instructions.md").read_text()
    for token in ("DR-*", "RS-*", "IP-*", "project-status.yaml"):
        assert token in text, f"Missing routing contract {token}"
    for target in ("chat", "plugin", "claude-skills", "opencode"):
        z = root / "dist" / f"design-reviewer-{target}-{a.version}.zip"
        assert z.is_file(), f"Distribution not built: {z}"
        with zipfile.ZipFile(z) as archive:
            names = archive.namelist()
            for skill in EXPECTED:
                matches = [name for name in names if name.endswith(f"/{skill}/SKILL.md")]
                assert matches, f"{target} missing {skill} SKILL.md"
                for name in matches:
                    doc = archive.read(name).decode("utf-8")
                    assert len(doc) > 100, f"Empty skill {name}"
    print("PASS: five modular/orchestrator skills in source and four skill-supporting distributions")

if __name__ == "__main__":
    main()
