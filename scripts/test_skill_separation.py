#!/usr/bin/env python3
"""Guard modular Skill separation and runtime script footprint."""
from pathlib import Path
import argparse
import zipfile
import yaml

IDS = ["source-analysis", "design-review", "solution-strategy", "implementation-planning", "design-review-workflow"]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--project-root",default=".")
    p.add_argument("--version",default="0.0.0-ci")
    a=p.parse_args()
    root=Path(a.project_root)
    cfg=yaml.safe_load((root/"gpt-project.yaml").read_text(encoding="utf-8"))
    assert cfg["instructions"]["mode"] == "modular_skills"
    core=(root/cfg["instructions"]["core"]).read_text()
    assert len(core)<6000, "Core is unnecessarily monolithic"
    for skill in cfg["skills"]["definitions"]:
        source=skill.get("source")
        assert source, f"Missing canonical source: {skill['id']}"
        assert (root/source).is_file()
    for target in ("plugin","claude-skills"):
        archive=root/"dist"/f"design-reviewer-{target}-{a.version}.zip"
        with zipfile.ZipFile(archive) as z:
            for skill in IDS:
                paths=[x for x in z.namelist() if x.endswith(f"/{skill}/SKILL.md")]
                assert len(paths)==1,(target,skill,paths)
                doc=z.read(paths[0]).decode()
                assert len(doc)<11500, (target,skill,len(doc))
                assert "## Evidens och precision" in doc
                assert "## När den aktiveras" in doc
                if skill=="source-analysis":
                    assert any(x.endswith("/source-analysis/scripts/analyze_source_tree.py") for x in z.namelist())
                    assert any(x.endswith("/source-analysis/scripts/lib/source_inventory.py") for x in z.namelist())
    print("PASS: concise modular skills and optional Python analysis tool without Engine ZIP")

if __name__=="__main__":
    main()
