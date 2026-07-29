# AGENTS.md — Main Agent f78f1d3e
> Inherits from: `../../AGENTS.md` (non-overridable hard rules listed there).

## Agent identity

- **ShortAgentID**: `f78f1d3e`
- **Name**: 小花蟹 (Little Flower Crab)
- **Device**: 0101aaa313a11c56
- **Type**: MAIN
- **Role**: doc-writer

## Parallel modes

This Main Agent supports two parallel modes:

- **Sub Context Window**: lightweight, same branch, file locks, no push. For non-overlapping parallel tasks.
- **Sub Agent**: independent identity, own branch (`sub/{id}/{slug}`), self-registers, pushes to own branch, PR merge. For concurrent work on overlapping files.

Rule: **MAIN does the work directly. Parallel modes are for when MAIN is busy or files would conflict.**

All context definitions live in `context/`. Sub Agent roles live in `sub-agents/` (on-demand).

## Directory convention

| Path | Purpose |
|------|---------|
| `sub-agents/` | Role definitions for SUB agents (on-demand, empty by default) |
| `context/` | Context window definitions (MAIN + on-demand SUB) |
| `tasks/` | Task assignments (MAIN writes, SUB reads) |
| `locks/` | Three-tier lock files (branch/dir/file/) |
| `handoffs/` | Cross-window communication archive |
| `decisions/` | Major architectural decisions |
| `roster.md` | Sub-agent and window registry |
| `roadmap.md` | This Main Agent's roadmap |

## Locking protocol

See `agents/shared/guidelines/lock-protocol.md` for full specification.

Summary:
- Three-tier: branch → directory → file
- Window acquires its own locks (MAIN only writes tasks)
- Atomic creation (O_EXCL), no read-then-write
- Release order: file → directory → branch (reverse of acquire)
- MAIN also locks when modifying files directly
- Zombie locks cleaned by MAIN on each message (timeout = 30min)

## Window startup

When 花花 opens a new WorkBuddy window for a SUB role:

1. 花花 pastes the window's startup prompt (from `context/{name}.md`)
2. SUB window reads its window definition → learns role, permissions, constraints
3. SUB window reads `tasks/{task-id}.md` → learns the task
4. SUB window claims locks → executes → writes result handoff

## Sub Agent lifecycle

Sub Agents are **registered on demand** via self-registration, with Git-managed branches.

1. MAIN writes registration handoff
2. 花花 opens new WorkBuddy window with handoff prompt
3. SUB computes ShortAgentID → writes roster → creates role + context files
4. SUB configures git identity → creates `sub/{id}/{task}` branch → commits + pushes
5. SUB writes confirmation handoff
6. MAIN reads → assigns task → SUB executes → PR review → squash-merge → RETIRED

Current state: **no ACTIVE Sub Agents on this device.**
