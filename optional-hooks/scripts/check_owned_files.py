#!/usr/bin/env python3
import re
from pathlib import Path
from hooklib import load_config, changed_files, read_text, report, rel
cfg=load_config()
if not cfg.get('checks',{}).get('owned_files',False): raise SystemExit(0)
h=Path(cfg.get('paths',{}).get('session_handoff','docs/SESSION_HANDOFF.md'))
text=read_text(h); issues=[]; owned=[]; inside=False
if not text: raise SystemExit(report('owned files',[f'{h}: missing or empty'],cfg))
for line in text.splitlines():
    if 'Files Owned' in line and line.startswith('##'):
        inside=True; continue
    if inside and line.startswith('## '): break
    if inside:
        m=re.match(r'\s*-\s+`?([^`]+?)`?\s*$',line)
        if m and m.group(1).strip()!='UNKNOWN': owned.append(m.group(1).strip())
if not owned: raise SystemExit(report('owned files',['No owned files found in SESSION_HANDOFF'],cfg))
for p in changed_files():
    r=rel(p)
    if r.startswith('docs/SESSION_HANDOFF.md') or r.startswith('docs/handoffs/') or r.startswith('docs/HANDOFF_INDEX.md'): continue
    if not any(r==o or r.startswith(o.rstrip('/')+'/') for o in owned): issues.append(f'{r}: changed but not listed in owned files')
raise SystemExit(report('owned files guard',issues,cfg))
