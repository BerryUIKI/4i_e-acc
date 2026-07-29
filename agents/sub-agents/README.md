# Sub-Agent Status Files

Each sub-agent bound to Main Agent `305cde212a` maintains its own status file here.

## Convention

- **Filename**: `{ShortAgentID}.md`
- **Status lifecycle**: `DISPATCHED` → `IN_PROGRESS` → `DONE` | `FAILED`
- **Monitored by**: Main Agent `305cde212a` (the coordinator)
- **Sub-agents cannot push**: the Main Agent integrates and pushes completed work.

## Template

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
{issues, decisions, context for Main Agent reviewer}
```

## Active Sub-Agents

| File | Status |
|------|--------|
| (none yet) | |
