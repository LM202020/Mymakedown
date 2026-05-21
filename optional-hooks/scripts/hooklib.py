#!/usr/bin/env python3
from __future__ import annotations
import subprocess, re
from pathlib import Path
ROOT=Path.cwd()
CONFIG_PATH=ROOT/'optional-hooks/config/hooks-config.yaml'
def parse_scalar(v):
    v=v.strip().strip('"').strip("'")
    if v in ('true','True'): return True
    if v in ('false','False'): return False
    try: return int(v)
    except ValueError: return v
def load_config():
    cfg={'mode':'warn','checks':{},'limits':{},'paths':{},'protected_root_files':[],'protected_doc_files':[],'placeholder_patterns':[],'secret_patterns':[]}
    if not CONFIG_PATH.exists(): return cfg
    cur=None
    for raw in CONFIG_PATH.read_text(encoding='utf-8',errors='replace').splitlines():
        line=raw.rstrip(); s=line.strip()
        if not s or s.startswith('#'): continue
        if not raw.startswith(' ') and s.endswith(':'):
            cur=s[:-1]; cfg.setdefault(cur,{}); continue
        if not raw.startswith(' ') and ':' in s:
            k,v=s.split(':',1); cfg[k.strip()]=parse_scalar(v); cur=None; continue
        if cur and s.startswith('- '):
            if not isinstance(cfg.get(cur),list): cfg[cur]=[]
            cfg[cur].append(s[2:].strip().strip('"').strip("'")); continue
        if cur and ':' in s:
            if not isinstance(cfg.get(cur),dict): cfg[cur]={}
            k,v=s.split(':',1); cfg[cur][k.strip()]=parse_scalar(v)
    return cfg
def git(args):
    try: return subprocess.check_output(['git']+args,cwd=ROOT,text=True,stderr=subprocess.DEVNULL)
    except Exception: return ''
def staged_files():
    out=git(['diff','--cached','--name-only','--diff-filter=ACMR'])
    return [ROOT/x.strip() for x in out.splitlines() if x.strip()]
def changed_files():
    vals=set()
    for out in (git(['diff','--name-only','--diff-filter=ACMR']),git(['diff','--cached','--name-only','--diff-filter=ACMR'])):
        for x in out.splitlines():
            if x.strip(): vals.add(ROOT/x.strip())
    return sorted(vals)
def read_text(p):
    try: return Path(p).read_text(encoding='utf-8',errors='replace')
    except FileNotFoundError: return ''
def rel(p):
    try: return str(Path(p).relative_to(ROOT))
    except ValueError: return str(p)
def is_binary(p):
    try: return b'\0' in Path(p).read_bytes()[:2048]
    except Exception: return True
def text_files(paths):
    for p in paths:
        if Path(p).is_file() and not is_binary(p): yield Path(p)
def report(title,issues,cfg):
    if not issues:
        print('OK: '+title); return 0
    print('WARNING: '+title)
    for i in issues: print('- '+i)
    if cfg.get('mode')=='block':
        print('Mode is block. Failing check.'); return 1
    print('Mode is warn. Continuing.'); return 0
