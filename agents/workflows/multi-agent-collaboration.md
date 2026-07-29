# Multi-Agent Collaboration — Workflow

This repo is maintained by a Main Agent (coordinator) + sub-agents (executors) across separate context windows. The human user ("花花") bridges agents by carrying prompts and reports.

## Architecture

```
┌────────────────────────────────────┐
│   Main Agent: 305cde212a           │
│   Role: doc-writer (coordinator)   │
│                                    │
│   • Decomposes goals into tasks    │
│   • Writes sub-agent prompts       │
│   • Monitors status files           │
│   • Reviews, integrates, pushes    │
└──────────┬─────────────────────────┘
           │
    tells user what prompt to paste
           │
     ┌─────▼─────┐  ┌───────────┐  ┌───────────┐
     │ Sub-Agent │  │ Sub-Agent │  │ Sub-Agent │
     │ ci-fixer  │  │ (TBD)     │  │ (TBD)     │
     │           │  │           │  │           │
     │ executes  │  │ executes  │  │ executes  │
     │ updates   │  │ updates   │  │ updates   │
     │ status    │  │ status    │  │ status    │
     └───────────┘  └───────────┘  └───────────┘
```

- **Main Agent**: coordinator only. Does NOT execute substantive work. Preserves context.
- **Sub-agents**: separate context windows, same repo. No separate working directory. Cannot push.
- **User (花花)**: the bridge. Main Agent tells user what prompt to paste. Sub-agent reports back through its status file.

## Dispatch Protocol

### From Main Agent → User

Main Agent writes a prompt block and tells user:

> 花，帮我开个子 Agent，Prompt 如下：

````markdown
```
Task: <one-line summary>

Context:
- Repo: https://github.com/BerryUIKI/4i_e-acc
- Branch: <branch-name>

Inputs:
<embedded file content or GitHub raw URLs — embed if small, URL if large>

Expected outputs:
- <file path>: <description>

Constraints:
- <rules, conventions, forbidden operations>

Status reporting:
- Update your status file at agents/sub-agents/{your-ShortAgentID}.md
```
````

### Sub-Agent Responsibility

1. **Register**: add/update entry in `agents/handoffs/agent-roster.md` under bound Main Agent, compute own SHA256 UID.
2. **Status tracking**: create/update `agents/sub-agents/{ShortAgentID}.md` with DISPATCHED → IN_PROGRESS → DONE/FAILED.
3. **Execute**: make the changes described in the prompt.
4. **Report**: on failure, write clear notes in the status file so the Main Agent can debug/replan.

### Main Agent Integration

When user reports a sub-agent has finished:
1. Read `agents/sub-agents/{ShortAgentID}.md`.
2. If DONE: verify changes on remote, modify status → merged, push.
3. If FAILED: read notes, determine retry or replan.

## Status File Convention

Every sub-agent maintains: `agents/sub-agents/{ShortAgentID}.md`

```markdown
# Sub-Agent Status — {ShortAgentID}

- **Role**: {domain}-{task-type}
- **Bound Main**: 305cde212a
- **Status**: DISPATCHED | IN_PROGRESS | DONE | FAILED
- **Task**: {one-line summary}
- **Started**: YYYY-MM-DD HH:MM UTC
- **Completed**: YYYY-MM-DD HH:MM UTC

## Files modified
- `path/to/file`: change description

## Notes
{issues, decisions, context}
```

## Prompt Writing Rules

1. **Embed file content**. Sub-agents may not have GitHub API access. For files the sub-agent needs to read or modify, paste the full content.
2. **Be specific about output paths**. Exact file paths, not "somewhere in agents/".
3. **List forbidden actions**. Sub-agents cannot `git push`. Other restrictions as needed.
4. **Include status instructions**. Remind the sub-agent to update its status file.

## Agent Identity

- **Main Agent**: `305cde212a`, role `doc-writer` (小花蟹 / Little Flower Crab) — coordinator.
- **Sub-agents**: Registered in `agents/handoffs/agent-roster.md`. Each bound to `305cde212a`.
- Sub-agents self-identify in their status files and in roster when first activated.

## Session Handoff (Main Agent → Next Main Agent Session)

Used when the Main Agent's context window ends and work continues in a new session:

1. Write a handoff to `agents/handoffs/YYYY-MM-DD.md` covering pending dispatches, dispatched-but-unreviewed sub-agent statuses, and open decisions.
2. The next session's Main Agent bootstrap picks up from this handoff.
