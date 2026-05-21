#!/usr/bin/env python3
from pathlib import Path
from hooklib import load_config, read_text, report
cfg=load_config(); limits=cfg.get('limits',{})
if not cfg.get('checks',{}).get('handoff_size',True): raise SystemExit(0)
issues=[]
def count(p):
    t=read_text(p); return len(t.splitlines()) if t else 0
session=Path(cfg.get('paths',{}).get('session_handoff','docs/SESSION_HANDOFF.md'))
if session.exists():
    n=count(session); m=int(limits.get('session_handoff_max_lines',300))
    if n>m: issues.append(f'{session}: {n} lines exceeds max {m}; run Handoff Compaction')
    text=read_text(session)
    for marker,msg in [('diff --git','full diff appears pasted'),('Traceback (most recent call last)','long traceback may be pasted'),('BEGIN RSA PRIVATE KEY','private key marker present'),('BEGIN OPENSSH PRIVATE KEY','private key marker present')]:
        if marker in text: issues.append(f'{session}: {msg}')
hand=Path('docs/handoffs'); sm=int(limits.get('handoff_snapshot_max_lines',250))
if hand.exists():
    for p in hand.glob('*.md'):
        n=count(p)
        if n>sm: issues.append(f'{p}: {n} lines exceeds max {sm}')
raise SystemExit(report('handoff size',issues,cfg))
