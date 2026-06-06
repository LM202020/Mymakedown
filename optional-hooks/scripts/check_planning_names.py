#!/usr/bin/env python3
from pathlib import Path
from hooklib import load_config, git, report
cfg=load_config()
if not cfg.get('checks',{}).get('planning_names',True): raise SystemExit(0)
# Planning/review artifacts are unique by construction: their filename carries this
# session's branch/worktree slug (see IMPLEMENTATION_WORKFLOW §3.2). Derive the slug
# from the current branch; skip on a base branch or detached HEAD, where it is not a
# session branch and the rule cannot be enforced meaningfully.
branch=git(['symbolic-ref','--short','HEAD']).strip()  # works on an unborn branch; empty on detached HEAD
slug=branch.split('/')[-1] if branch else ''
BASE={'main','master','develop','trunk','HEAD',''}
if branch in BASE or slug in BASE: raise SystemExit(0)
DIRS=('docs/specs/','docs/plans/','docs/reviews/','docs/retros/')
issues=[]
# Only newly added files: a modified file keeps the slug of the session that created it.
for raw in git(['diff','--cached','--name-only','--diff-filter=A']).splitlines():
    r=raw.strip()
    if not r.endswith('.md') or not any(r.startswith(d) for d in DIRS): continue
    name=Path(r).name
    if name=='README.md' or 'TEMPLATE' in name: continue
    if slug not in name:
        issues.append(f'{r}: filename is missing this session slug `{slug}`; name it YYYY-MM-DD-<feature>-{slug}… (see IMPLEMENTATION_WORKFLOW §3.2)')
raise SystemExit(report('planning artifact naming',issues,cfg))
