# CODEX.md

Entry point for Codex maintaining this repository.

**Read `AGENTS.md` first** — it has the full layout and the editing rules. This file only adds
Codex-specific notes.

- This repo is the workflow framework package itself, not an application. There is no build or app
  to run; the work is editing templates under `templates/target/` plus the manifest and hooks.
- Before modifying files, confirm what you are allowed to touch and keep changes scoped to the
  edit at hand. If you add/rename/remove a file under `templates/target/`, update
  `templates/FILE_ADOPTION_MANIFEST.md` in the same change.
- Verification command for any change here:
  `python3 scripts/check_framework_consistency.py` (Windows: `python scripts\check_framework_consistency.py`).
  It must exit 0.
- Shell scripts and git hooks must stay LF. Keep Python dependency-free and `python3`/`python`
  compatible.
