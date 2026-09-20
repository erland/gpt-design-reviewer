#!/usr/bin/env python3
import argparse, json, sys, zipfile
from pathlib import Path

RUNTIMES = {
    'chat': ('design-reviewer-chat-', 'assistant/runtime-contract.json'),
    'custom-gpt': ('design-reviewer-custom-gpt-', 'builder/runtime-contract.json'),
    'claude': ('design-reviewer-claude-', 'project/runtime-contract.json'),
    'opencode': ('design-reviewer-opencode-', '.opencode/design-reviewer-runtime.json'),
}
SECTIONS = ('capabilities','artifacts','workspace_state')

def latest_zip(dist: Path, prefix: str):
    matches = sorted(dist.glob(prefix+'*.zip'))
    return matches[-1] if matches else None

def read_contract(zpath: Path, member: str):
    with zipfile.ZipFile(zpath) as z:
        return json.loads(z.read(member).decode('utf-8'))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    args=ap.parse_args()
    root=Path(args.project_root).resolve(); dist=root/'dist'
    contracts={}; failures=[]
    for name,(prefix,member) in RUNTIMES.items():
        z=latest_zip(dist,prefix)
        if not z:
            failures.append(f'{name}: distribution missing')
            continue
        try: contracts[name]=read_contract(z,member)
        except Exception as e: failures.append(f'{name}: runtime contract unreadable: {e}')
    if failures:
        print('RUNTIME PARITY: FAIL'); [print(' -',x) for x in failures]; return 1
    base=contracts['chat']
    for section in SECTIONS:
        for name,c in contracts.items():
            if c.get(section)!=base.get(section): failures.append(f'{name}: {section} differs from chat canonical contract')
    expected_outputs={'design-review.md','recommended-solution-strategy.md','implementation-plan.md'}
    outputs=base.get('artifacts',{}).get('outputs',{})
    names={v.get('filename_pattern') for v in outputs.values() if isinstance(v,dict) and v.get('filename_pattern')}
    if not expected_outputs.issubset(names): failures.append(f'canonical artifacts missing: {sorted(expected_outputs-names)}')
    if failures:
        print('RUNTIME PARITY: FAIL'); [print(' -',x) for x in failures]; return 1
    print('RUNTIME PARITY: PASS')
    print('Canonical sections identical across chat, custom-gpt, claude and opencode: capabilities, artifacts, workspace_state')
    return 0

if __name__=='__main__': sys.exit(main())
