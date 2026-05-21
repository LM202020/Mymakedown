# CLAUDE.md

Entry point for Claude (incl. Claude Code) maintaining this repository.

**Read `AGENTS.md` first** — it has the full layout and the editing rules. This file only adds
Claude-specific notes.

- This repo is the workflow framework package itself, not an application. Most work here is
  editing markdown templates under `templates/target/` and keeping `templates/FILE_ADOPTION_MANIFEST.md`
  in sync.
- Claude is well suited to the review/consistency side: when changing the templates, reason about
  cross-file impact (the same concept often appears in `IMPLEMENTATION_WORKFLOW`, `HANDOFF_POLICY`,
  `PROMPT_LIBRARY`, `USAGE`, and `QUICK_PROMPTS`) and avoid reintroducing duplication.
- After any edit, run `python3 scripts/check_framework_consistency.py` and make it pass before
  considering the change done.
- Do not restate handoff size numbers; see rule 4 in `AGENTS.md`.
