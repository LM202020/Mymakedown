# AGENTS.md

Root entry point for any agent (Claude, Codex, or other) working in **this** repository.

This repo is **not an application** — it is the Project Agent Workflow Framework package itself.
It produces workflow scaffolding for *other* projects. When you edit here, you are editing the
framework, so follow the framework's own rules and keep it internally consistent.

Claude-specific notes: `CLAUDE.md`. Codex-specific notes: `CODEX.md`.

## What lives where

| Path | Purpose |
|---|---|
| `README.md`, `NATURAL_LANGUAGE_OVERVIEW.md` | what the framework is |
| `SAFE_ADOPTION_POLICY.md`, `INSTALL_OR_ADOPT_WORKFLOW.md` | how it gets applied to a project |
| `templates/FILE_ADOPTION_MANIFEST.md` | the rule table: every target file + its `adoption_mode` |
| `templates/target/` | the actual content that lands in a target project (everything is a template) |
| `optional-hooks/` | the opt-in pre-commit/pre-push layer for *target* projects |
| `scripts/check_framework_consistency.py` | integrity guard for *this* repo |

## Rules for editing this framework

1. **Content goes under `templates/target/`.** Nothing in that tree is copied blindly into a
   project — it is governed by `templates/FILE_ADOPTION_MANIFEST.md`.
2. **Keep the manifest in sync.** If you add, rename, or remove a file under `templates/target/`,
   update the manifest row(s) accordingly. Unreferenced content files are flagged by the checker.
3. **Always keep the `target/` segment in template paths** (`templates/target/root/...`); never
   drop it to the legacy un-prefixed form.
4. **Handoff size limits have one source.** The numbers (currently 300/250/200 lines) live only in
   `templates/target/docs/HANDOFF_POLICY.md.template` (human source) and
   `optional-hooks/config/hooks-config.yaml` (machine-enforced). Everywhere else references the
   policy — do not restate the numbers.
5. **Version strings.** The framework version (currently `v7`) appears in root doc titles and in
   `scripts/check_framework_consistency.py` (`EXPECTED_VERSION`). Bump them together.
6. **Cross-platform.** Shell scripts and git hooks must stay LF (`.gitattributes` enforces this).
   Python is invoked as `python3` with a fallback to `python`; keep scripts pure-Python and
   dependency-free.
7. **Preserve the core conventions.** The `UNKNOWN`/`N/A` fill markers, file-ownership maps,
   no-placeholder gates, size limits, and the Agent Output Contract are the most valuable part of
   the templates. Do not water them down.

## Before you finish

Run the integrity checker and make sure it exits clean:

```bash
python3 scripts/check_framework_consistency.py   # Windows: python scripts\check_framework_consistency.py
```

It verifies: every manifest reference exists, no template paths missing the `target/` segment,
handoff size numbers stay single-sourced, and root titles match the expected version.
