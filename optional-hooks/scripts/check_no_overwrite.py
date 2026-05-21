#!/usr/bin/env python3
from hooklib import load_config, staged_files, git, read_text, report, rel
cfg=load_config()
if not cfg.get('checks',{}).get('no_overwrite',True): raise SystemExit(0)
protected=set(cfg.get('protected_root_files',[]))|set(cfg.get('protected_doc_files',[]))
issues=[]
for p in staged_files():
    r=rel(p)
    if r not in protected: continue
    status=git(['status','--porcelain','--',r]).strip()
    text=read_text(p)
    if 'PROJECT_AGENT_WORKFLOW' in text: continue
    if status and not status.startswith('A'):
        issues.append(f'{r}: protected existing file modified without PROJECT_AGENT_WORKFLOW managed block')
raise SystemExit(report('no-overwrite guard',issues,cfg))
