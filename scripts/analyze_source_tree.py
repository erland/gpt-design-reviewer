#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from lib.source_inventory import analyze_tree, dumps_json


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Collect deterministic source-tree evidence for Design Reviewer.')
    p.add_argument('root', help='Source tree to analyze')
    p.add_argument('--output', '-o', help='Write JSON evidence to this file; stdout if omitted')
    p.add_argument('--large-file-lines', type=int, default=500)
    p.add_argument('--large-function-lines', type=int, default=80)
    p.add_argument('--duplicate-block-lines', type=int, default=8)
    return p


def main() -> int:
    args = parser().parse_args()
    root = Path(args.root)
    if not root.is_dir():
        print(f'error: source root is not a directory: {root}', file=sys.stderr)
        return 2
    data = analyze_tree(
        root,
        large_file_lines=max(1, args.large_file_lines),
        large_function_lines=max(1, args.large_function_lines),
        duplicate_block_lines=max(3, args.duplicate_block_lines),
    )
    payload = dumps_json(data)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding='utf-8')
        print(f'wrote evidence: {out}')
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
