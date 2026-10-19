#!/usr/bin/env python3
import argparse,hashlib,json,re,sys
from pathlib import Path
import yaml
p=argparse.ArgumentParser();p.add_argument('--version',required=True);p.add_argument('--project-root',default='.');a=p.parse_args();root=Path(a.project_root);d=root/'dist';cfg=yaml.safe_load((root/'gpt-project.yaml').read_text());ident=cfg['project']['id'];names={ident+'-project-'+a.version+'.zip'}|{ident+'-'+suffix+'-'+a.version+'.zip' for suffix in ['chat','plugin','claude-project','claude-skills','opencode']};actual={x.name for x in d.glob('*.zip')};errors=[]
if actual!=names: errors.append(f'asset mismatch missing={names-actual}, extra={actual-names}')
checksums=d/'SHA256SUMS.txt';manifest=d/'DELIVERY-MANIFEST.json';
if not checksums.exists() or not manifest.exists():errors.append('missing checksum or manifest')
else:
 lines=checksums.read_text().splitlines();found={}
 for line in lines:
  match=re.match(r'^([a-f0-9]{64})\s+\*?(.+)$',line)
  if not match:errors.append('bad checksum line: '+line);continue
  h,name=match.groups(); found[name]=h
  if not (d/name).is_file() or hashlib.sha256((d/name).read_bytes()).hexdigest()!=h:errors.append('checksum mismatch: '+name)
 if not names.issubset(set(found)):errors.append('checksums missing assets')
 try:json.loads(manifest.read_text())
 except Exception as e:errors.append('bad delivery manifest '+str(e))
print('PASS: modern release assets' if not errors else 'FAIL: '+ '; '.join(errors));sys.exit(bool(errors))
