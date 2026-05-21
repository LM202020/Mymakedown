#!/usr/bin/env python3
from pathlib import Path
from hooklib import load_config, report
cfg=load_config()
if not cfg.get('checks',{}).get('adoption_manifest',True): raise SystemExit(0)
p=Path(cfg.get('paths',{}).get('adoption_manifest','templates/FILE_ADOPTION_MANIFEST.md'))
issues=[]
if not p.exists(): issues.append(f'{p}: missing')
else:
    t=p.read_text(encoding='utf-8',errors='replace')
    for x in ['create_if_missing','managed_block_merge','propose_if_exists','append_index','generated_runtime','directory_create']:
        if x not in t: issues.append(f'{p}: missing adoption_mode `{x}`')
    for x in ['AGENTS.md','CLAUDE.md','CODEX.md','docs/IMPLEMENTATION_WORKFLOW.md','docs/SESSION_HANDOFF.md','docs/PROMPT_LIBRARY.md']:
        if x not in t: issues.append(f'{p}: missing target `{x}`')
raise SystemExit(report('adoption manifest',issues,cfg))
