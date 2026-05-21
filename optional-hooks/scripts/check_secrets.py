#!/usr/bin/env python3
import re
from hooklib import load_config, staged_files, text_files, read_text, report, rel
cfg=load_config()
if not cfg.get('checks',{}).get('secrets',True): raise SystemExit(0)
issues=[]
for p in text_files(staged_files()):
    r=rel(p); name=p.name.lower(); text=read_text(p)
    if (name=='.env' or name.endswith('.env')) and 'example' not in name and 'template' not in name:
        issues.append(f'{r}: environment file appears staged')
    for pat in cfg.get('secret_patterns',[]):
        try:
            if re.search(pat,text,re.I): issues.append(f'{r}: matched possible secret pattern `{pat}`')
        except re.error: pass
raise SystemExit(report('secret scan',issues,cfg))
