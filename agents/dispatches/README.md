# Task Dispatches

Sub-agent task specifications. Main Agent writes detailed requirements here; sub-agents read them and execute. The user-facing prompt is a one-liner referencing the file.

## Convention

- **Filename**: `{yyyyMMdd}-{slug}.md` (date prefix for chronological ordering)
- **Lifecycle**: DISPATCHED → IN_PROGRESS → DONE → ARCHIVED
- **Cleanup**: after integration, Main Agent moves to `dispatches/archive/` or deletes

## How to use

### Main Agent
1. Write detailed task spec here.
2. Tell user: "让子 Agent 读 `agents/dispatches/{file}` 后执行"
3. Monitor `agents/sub-agents/{ID}.md` for completion.

### Sub Agent (instructions embedded in every dispatch)
1. Read `AGENTS.md` (root) for hard rules.
2. Read this dispatch file.
3. Read `agents/workflows/multi-agent-collaboration.md` for your responsibilities.
4. Execute. Update your status file. DO NOT push.

## Active dispatches

| File | Task | Status |
|------|------|--------|
| `20260729-ci-xcolor.md` | Fix xcolor loading order in pandoc-template.tex | DISPATCHED |
