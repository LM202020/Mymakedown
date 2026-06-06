#!/usr/bin/env python3
from pathlib import Path
from hooklib import load_config, read_text, report
cfg=load_config(); limits=cfg.get('limits',{})
if not cfg.get('checks',{}).get('handoff_index',True): raise SystemExit(0)
issues=[]
idx=Path(cfg.get('paths',{}).get('handoff_index','docs/HANDOFF_INDEX.md'))
if idx.exists():
    text=read_text(idx)
    bars=[l.strip() for l in text.splitlines() if l.strip().startswith('|')]
    # keep only rows with real content (drops the |---|---| separator), then minus the header row
    content=[l for l in bars if l.replace('|','').replace('-','').replace(':','').strip()]
    rows=max(0,len(content)-1)
    m=int(limits.get('handoff_index_max_rows',200))
    if rows>m: issues.append(f'{idx}: {rows} index rows exceed max {m}; archive older rows by month under docs/handoffs/archive/')
raise SystemExit(report('handoff index size',issues,cfg))
