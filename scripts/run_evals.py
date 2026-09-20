#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Design Reviewer eval suite")
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()

    contract_path = root / "contracts/eval-suite-contract.yaml"
    contract = load_yaml(contract_path)
    schema_path = root / contract["suite"]["case_schema"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    pattern = str(root / contract["suite"]["cases_glob"])
    files = [Path(p) for p in sorted(glob.glob(pattern))]
    errors: list[str] = []
    ids: set[str] = set()
    tags: set[str] = set()

    if not files:
        errors.append("No eval cases found")

    for path in files:
        data = load_yaml(path)
        for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
            loc = ".".join(map(str, error.path)) or "<root>"
            errors.append(f"{path.relative_to(root)}:{loc}: {error.message}")
        case_id = data.get("id") if isinstance(data, dict) else None
        if case_id in ids:
            errors.append(f"Duplicate eval id: {case_id}")
        if case_id:
            ids.add(case_id)
        if isinstance(data, dict):
            tags.update(data.get("coverage_tags", []))
            expected = data.get("expected", [])
            forbidden = data.get("forbidden", [])
            if set(expected) & set(forbidden):
                errors.append(f"{case_id}: same statement appears in expected and forbidden")

    required_tags = set(contract.get("required_coverage_tags", []))
    missing_tags = sorted(required_tags - tags)
    if missing_tags:
        errors.append("Missing required coverage tags: " + ", ".join(missing_tags))

    if errors:
        print("EVAL SUITE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("EVAL SUITE: PASS")
    print(f"Cases: {len(files)}")
    print(f"Coverage tags: {len(tags)}")
    for path in files:
        data = load_yaml(path)
        print(f"- {data['id']}: {data['title']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
