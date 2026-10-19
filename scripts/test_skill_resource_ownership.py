#!/usr/bin/env python3
"""Validate canonical resource ownership in generated skill distributions."""
from pathlib import Path
import argparse
import zipfile
import yaml

TOOL = "analyze_source_tree.py"
OWNERS = {"source-analysis", "design-review-workflow"}
SKILLS = {"source-analysis", "design-review", "solution-strategy", "implementation-planning", "design-review-workflow"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--project-root", default=".")
    p.add_argument("--version", default="0.0.0-ci")
    a = p.parse_args()
    root = Path(a.project_root)
    cfg = yaml.safe_load((root / "gpt-project.yaml").read_text(encoding="utf-8"))
    definitions = cfg["skills"]["definitions"]
    assert cfg["skills"]["resource_policy"] == "explicit"
    assert {s["id"] for s in definitions} == SKILLS
    for skill in definitions:
        for key in ("references", "assets", "scripts"):
            assert isinstance(skill.get(key), list), (skill["id"], key)
        assert (TOOL in " ".join(skill["scripts"])) == (skill["id"] in OWNERS)

    for runtime in ("chat", "opencode", "plugin", "claude-skills"):
        archive = root / "dist" / f"design-reviewer-{runtime}-{a.version}.zip"
        with zipfile.ZipFile(archive) as z:
            names = z.namelist()
            for skill in SKILLS:
                dirs = [n.rsplit("/SKILL.md", 1)[0] for n in names if n.endswith(f"/{skill}/SKILL.md")]
                assert len(dirs) == 1, (runtime, skill, dirs)
                prefix = dirs[0] + "/"
                tools = [n for n in names if n.startswith(prefix) and n.endswith("/" + TOOL)]
                if skill in OWNERS:
                    assert len(tools) == 1, (runtime, skill, tools)
                    assert any(n.startswith(prefix) and n.endswith("/lib/source_inventory.py") for n in names)
                else:
                    assert not tools, (runtime, skill, tools)
                    text = z.read(prefix + "SKILL.md").decode("utf-8")
                    assert "Required script runtime/language: python" not in text, (runtime, skill)
    print("PASS: only source-analysis and workflow Skills own Python analysis scripts")

if __name__ == "__main__":
    main()
