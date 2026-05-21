# File Adoption Manifest

This manifest defines how every framework target file should be adopted into a project.

No target file may be copied blindly.

## adoption_mode values

| Mode | Meaning |
|---|---|
| `create_if_missing` | create from template only when missing |
| `managed_block_merge` | append/update only a managed block |
| `propose_if_exists` | create if missing; if exists, write proposed file instead |
| `append_index` | append compact index rows only |
| `generated_runtime` | generated during workflow, never blindly copied |
| `archive_only` | archive location only, no automatic deletion |
| `directory_create` | create directory only |
| `never_overwrite` | do not write; analyze and create plan |

## Manifest

| Target Path | Template Path | adoption_mode | Existing File Behavior | Notes |
|---|---|---|---|---|
| `AGENTS.md` | `templates/target/root/AGENTS.md.template` | `managed_block_merge` | preserve existing; append/update managed block | root agent entry |
| `CLAUDE.md` | `templates/target/root/CLAUDE.md.template` | `managed_block_merge` | preserve existing; append/update managed block | Claude entry |
| `CODEX.md` | `templates/target/root/CODEX.md.template` | `managed_block_merge` | preserve existing; append/update managed block | Codex entry |
| `README.md` | `templates/target/root/README.agent-workflow-snippet.md` | `managed_block_merge` | preserve existing; append/update managed block | project README pointer |
| `README.md` | `templates/target/root/README.md.template` | `create_if_missing` | create full README only if missing; if it exists, the managed_block_merge row above governs | full project README for new projects |
| `USAGE.md` | `templates/target/root/USAGE.md.template` | `create_if_missing` | do not overwrite | framework usage guide |
| `QUICK_PROMPTS.md` | `templates/target/root/QUICK_PROMPTS.md.template` | `create_if_missing` | do not overwrite | quick prompt cheat sheet |
| `PROJECT_AGENT_WORKFLOW_TEMPLATE.md` | `templates/target/root/PROJECT_AGENT_WORKFLOW_TEMPLATE.md.template` | `create_if_missing` | do not overwrite | framework overview |
| `docs/IMPLEMENTATION_WORKFLOW.md` | `templates/target/docs/IMPLEMENTATION_WORKFLOW.md.template` | `propose_if_exists` | write proposed file if exists | canonical workflow |
| `docs/PROMPT_LIBRARY.md` | `templates/target/docs/PROMPT_LIBRARY.md.template` | `propose_if_exists` | write proposed file if exists | natural language prompts |
| `docs/DOCUMENT_INDEX.md` | `templates/target/docs/DOCUMENT_INDEX.md.template` | `propose_if_exists` | write proposed file if exists | doc routing |
| `docs/SESSION_HANDOFF.md` | `templates/target/docs/SESSION_HANDOFF.md.template` | `generated_runtime` | never overwrite active handoff | current state |
| `docs/HANDOFF_POLICY.md` | `templates/target/docs/HANDOFF_POLICY.md.template` | `propose_if_exists` | write proposed file if exists | handoff size policy |
| `docs/HANDOFF_INDEX.md` | `templates/target/docs/HANDOFF_INDEX.md.template` | `append_index` | append/index only | handoff history index |
| `docs/PROJECT_CONTEXT.md` | `templates/target/docs/PROJECT_CONTEXT.md.template` | `propose_if_exists` | write proposed file if exists | stable project context |
| `docs/PROJECT_BASELINE.md` | `templates/target/docs/PROJECT_BASELINE.md.template` | `generated_runtime` | generated during adoption | old project baseline |
| `docs/DOC_MIGRATION_MAP.md` | `templates/target/docs/DOC_MIGRATION_MAP.md.template` | `generated_runtime` | generated during adoption | old/new doc mapping |
| `docs/DOC_CONFLICTS.md` | `templates/target/docs/DOC_CONFLICTS.md.template` | `append_index` | append conflicts only | conflict tracking |
| `docs/ENTRYPOINT_MERGE_POLICY.md` | `templates/target/docs/ENTRYPOINT_MERGE_POLICY.md.template` | `propose_if_exists` | write proposed file if exists | root merge rules |
| `docs/adoption/ENTRYPOINT_MERGE_PLAN.md` | `templates/target/docs/adoption/ENTRYPOINT_MERGE_PLAN.md.template` | `generated_runtime` | generated during entry-point merge; seeded from template | per-adoption merge plan |
| `docs/AGENT_ROSTER.md` | `templates/target/docs/AGENT_ROSTER.md.template` | `propose_if_exists` | write proposed file if exists | agent roles |
| `docs/ARCHITECTURE.md` | `templates/target/docs/ARCHITECTURE.md.template` | `propose_if_exists` | write proposed file if exists | architecture |
| `docs/API_PATHS.md` | `templates/target/docs/API_PATHS.md.template` | `propose_if_exists` | write proposed file if exists | API/module boundaries |
| `docs/DB_CONVENTIONS.md` | `templates/target/docs/DB_CONVENTIONS.md.template` | `propose_if_exists` | write proposed file if exists | database conventions |
| `docs/TEST_CONVENTIONS.md` | `templates/target/docs/TEST_CONVENTIONS.md.template` | `propose_if_exists` | write proposed file if exists | test conventions |
| `docs/DEPLOYMENT.md` | `templates/target/docs/DEPLOYMENT.md.template` | `propose_if_exists` | write proposed file if exists | deployment |
| `docs/SECURITY.md` | `templates/target/docs/SECURITY.md.template` | `propose_if_exists` | write proposed file if exists | security |
| `docs/RISK_REGISTER.md` | `templates/target/docs/RISK_REGISTER.md.template` | `append_index` | append structured risks only | risk tracking |
| `docs/DECISIONS.md` | `templates/target/docs/DECISIONS.md.template` | `append_index` | append structured decisions only | decision log |
| `docs/specs/` | N/A | `directory_create` | create if missing | specs directory |
| `docs/plans/` | N/A | `directory_create` | create if missing | plans directory |
| `docs/reviews/` | N/A | `directory_create` | create if missing | reviews directory |
| `docs/handoffs/` | N/A | `directory_create` | create if missing | handoffs directory |
| `docs/handoffs/artifacts/` | N/A | `directory_create` | create if missing | large logs |
| `docs/handoffs/archive/` | N/A | `directory_create` | create if missing | old handoff archive |
| `docs/retros/` | N/A | `directory_create` | create if missing | retros directory |
| `docs/archive/` | N/A | `archive_only` | do not move/delete automatically | old docs archive |
| `docs/adoption/` | N/A | `directory_create` | create if missing | adoption docs |
| `docs/adoption/proposed/` | N/A | `directory_create` | create if missing | proposed files |
| `docs/adoption/backups/` | N/A | `directory_create` | create if missing | optional backups |
| `docs/specs/SPEC_TEMPLATE.md` | `templates/target/docs/specs/SPEC_TEMPLATE.md.template` | `create_if_missing` | do not overwrite | spec template |
| `docs/plans/IMPLEMENTATION_PLAN_TEMPLATE.md` | `templates/target/docs/plans/IMPLEMENTATION_PLAN_TEMPLATE.md.template` | `create_if_missing` | do not overwrite | plan template |
| `docs/reviews/REVIEW_TEMPLATE.md` | `templates/target/docs/reviews/REVIEW_TEMPLATE.md.template` | `create_if_missing` | do not overwrite | review template |
| `docs/handoffs/HANDOFF_TEMPLATE.md` | `templates/target/docs/handoffs/HANDOFF_TEMPLATE.md.template` | `create_if_missing` | do not overwrite | handoff template |
| `docs/retros/RETRO_TEMPLATE.md` | `templates/target/docs/retros/RETRO_TEMPLATE.md.template` | `create_if_missing` | do not overwrite | retro template |

## Required behavior

If a target file exists and the mode is not `managed_block_merge` or `append_index`, do not overwrite it.

Instead write a proposed file under:

```text
docs/adoption/proposed/
```

and record the mapping in:

```text
docs/DOC_MIGRATION_MAP.md
```

---

## Optional Hooks Files

These files are part of the framework package and should not be copied over existing project files blindly.

| Target Path | Template Path | adoption_mode | Existing File Behavior | Notes |
|---|---|---|---|---|
| `optional-hooks/README.md` | package file | `create_if_missing` | do not overwrite | optional hooks docs |
| `optional-hooks/config/hooks-config.yaml` | package file | `propose_if_exists` | write proposed config if exists | hook config |
| `optional-hooks/install-hooks.sh` | package file | `create_if_missing` | do not overwrite | installer |
| `optional-hooks/uninstall-hooks.sh` | package file | `create_if_missing` | do not overwrite | uninstaller |
| `optional-hooks/git-hooks/pre-commit` | package file | `create_if_missing` | do not overwrite | git hook template |
| `optional-hooks/git-hooks/pre-push` | package file | `create_if_missing` | do not overwrite | git hook template |
| `optional-hooks/scripts/*.py` | package file | `create_if_missing` | do not overwrite | hook scripts |
| `.git/hooks/pre-commit` | generated install output | `generated_runtime` | created only by install script | not tracked |
| `.git/hooks/pre-push` | generated install output | `generated_runtime` | created only by install script | not tracked |
