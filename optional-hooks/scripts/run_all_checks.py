#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
scripts=['check_secrets.py','check_handoff_size.py','check_no_overwrite.py','check_plan_placeholders.py','check_adoption_manifest.py','check_owned_files.py']
failed=0
for s in scripts:
    p=Path('optional-hooks/scripts')/s
    if not p.exists():
        print(f'SKIP: {p} missing'); continue
    print('\nRunning '+str(p))
    r=subprocess.run([sys.executable,str(p)])
    if r.returncode!=0: failed=r.returncode
raise SystemExit(failed)
