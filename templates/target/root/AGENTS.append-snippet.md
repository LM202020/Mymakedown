<!-- BEGIN PROJECT_AGENT_WORKFLOW -->

## Project Agent Workflow

For non-trivial code changes, follow `docs/IMPLEMENTATION_WORKFLOW.md`.

Before continuing work, read:

1. `docs/IMPLEMENTATION_WORKFLOW.md`
2. `docs/DOCUMENT_INDEX.md`
3. `docs/SESSION_HANDOFF.md`
4. `docs/HANDOFF_POLICY.md`

Do not implement directly from a user request or spec. First review the spec, convert it into an implementation plan, review the plan, then execute task-by-task with tests and review gates.

Session save does not happen automatically. Before switching agents, switching sessions, compacting context, or stopping mid-task, update:

1. `docs/SESSION_HANDOFF.md`
2. `docs/handoffs/<timestamp>-<handoff>.md`
3. `docs/HANDOFF_INDEX.md`
4. active implementation plan task status

Do not touch credentials, secrets, deployment, systemd, production infrastructure, database migrations, or destructive operations unless explicitly approved in the active plan.

<!-- END PROJECT_AGENT_WORKFLOW -->
