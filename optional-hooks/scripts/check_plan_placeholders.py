#!/usr/bin/env python3
import re
from hooklib import load_config, staged_files, text_files, read_text, report, rel
cfg=load_config()
if not cfg.get('checks',{}).get('plan_placeholders',True): raise SystemExit(0)
issues=[]
for p in text_files(staged_files()):
    r=rel(p)
    if not (r.startswith('docs/plans/') or r.startswith('docs/specs/')): continue
    text=read_text(p)
    for pat in cfg.get('placeholder_patterns',[]):
        if re.search(re.escape(str(pat)),text,re.I): issues.append(f'{r}: contains placeholder-like text `{pat}`')
raise SystemExit(report('plan/spec placeholder scan',issues,cfg))
