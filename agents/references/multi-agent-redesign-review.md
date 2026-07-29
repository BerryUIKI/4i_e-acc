# Multi-Agent Parallel Mode & Branch Management — Redesign Review

> **Date**: 2026-07-29  
> **Author**: 花花 (human user) with 小花蟹 (Main Agent)  
> **Status**: 审阅完成，待 Main Agent 消化后讨论执行

---

## 1. Current State

| Dimension | Status |
|-----------|--------|
| Agent count | 1 Main (`42f78f1d3e`) + 2 Sub (`8f9b1fd0b6` ci-sub, `c8dfea5fc1` doc-data) |
| Communication | Handoff files + Dispatch files, human-relayed |
| Branch model | GitHub Flow (single-line: feature branch → PR → squash-merge to main) |
| Push authority | Main Agent only; Sub Agents commit-only |
| CI validation | Planned but not implemented (`agent-audit.yml`, `check_agent_roster.py`, `check_agent_binding.py`) |
| Identity system | SHA256 UID + device fingerprint + salt rotation |

---

## 2. Problems Found

### 2.1 No true parallelism

The current model is effectively sequential: Sub Agent finishes → human relays results → Main Agent aggregates → push. Two Sub Agents cannot work concurrently on the same branch because commit ordering and conflict resolution all land on the Main Agent.

### 2.2 Handoff communication is low-bandwidth

The `multi-agent-collaboration.md` flow is: "花，帮我开个子 Agent" → human pastes prompt → human returns results. This is human-in-the-loop message passing, not agent-to-agent collaboration. Every handoff requires cross-session waiting.

### 2.3 Branch model does not support multi-agent parallelism

Two Sub Agents modifying different files under `articles/2026-quadruple-long-life/` on the same branch risk conflicts. No branch-per-agent isolation, no file-level lock registration.

### 2.4 Identity system is over-engineered

SHA256 UID + device fingerprint binding + salt rotation is excessive for a single-user docs repo. All agents share the same device (`0101aaa313a11c56`). The maintenance cost (roster updates, CI scripts, handoff template fields) outweighs the traceability benefit.

### 2.5 Git push pipeline is fragile

Sandbox restrictions force REST API push workarounds, which lose git committer identity and require manual handoff logging to compensate. Each extra link in this chain is a breakage point.

### 2.6 Handoff and Dispatch overlap in purpose

`agents/handoffs/` (date-based naming) and `agents/dispatches/` (sequence-based naming) serve the same function — Main Agent assigning tasks to Sub Agents. Two formats add cognitive load and template maintenance.

### 2.7 CI validation exists only on paper

The Roadmap lists three Q3 targets — `check_agent_roster.py`, `check_agent_binding.py`, `agent-audit.yml` — none implemented. PR merges have zero agent identity validation.

---

## 3. Redesign Proposals

### 3.1 Branch-per-Agent parallel model

```
main
 └── article/2026-quadruple-long-life  (Main Agent integration branch)
      ├── sub/S02/doc-data-fill        (Sub: doc-data, isolated branch)
      └── sub/S01/ci-pdf-fix           (Sub: ci-sub, isolated branch)
```

Each Sub Agent works on its own `sub/<ShortID>/<task>` branch. Main Agent becomes a **branch merger**, not a commit aggregator. File lock registration via `agents/locks/<task-id>.md` prevents two agents from touching the same file.

### 3.2 Simplify identity system

| Current | Proposed |
|---------|----------|
| SHA256 UID (64 hex chars) | Short IDs: M01 (Main), S01, S02 (Sub) |
| Device fingerprint binding | Remove — single-user single-device |
| Salt rotation procedure | Remove — unnecessary for 1-person repo |
| Handoff template: 8 metadata fields | Reduce to 4: Agent, Task, Files Touched, Status |

Commit messages retain `[ShortID]` prefix for traceability. `agent-roster.md` shrinks from ~150 lines to ~30.

### 3.3 Merge Handoff + Dispatch → Unified Task Board

Replace `agents/handoffs/` + `agents/dispatches/` with a single `agents/tasks/` directory:

```markdown
# TASK-001 — Fill data markers
- Assigned: S02 (doc-data)
- Branch: sub/S02/doc-data-fill
- Files: articles/2026-quadruple-long-life/Main-Text/B002~G001.md
- Status: DISPATCHED → IN_PROGRESS → DONE → REVIEWED → MERGED
- Output branch: sub/S02/doc-data-fill
```

One file, one lifecycle. No duplicate templates.

### 3.4 Two-stage PR pipeline

```
Sub Agent branch  → PR#1 to integration branch (Main Agent reviews)
Integration branch → PR#2 to main (final squash-merge)
```

Benefits:
- PR#1 gives Main Agent a GitHub UI diff for review
- Multiple Sub Agent PR#1s can coexist without blocking
- PR#2 is a clean squash merge; main history stays linear

### 3.5 Abandon REST API push workaround

Accept sandbox limitations. Let the human user handle all pushes from their local machine. This eliminates the traceability gap entirely.

### 3.6 Simplify agent hierarchy

Merge `doc-data` and `ci-sub` into a single general-purpose Sub Agent. Two agents total is sufficient for this repo's scale.

| Agent | Role | Permissions |
|-------|------|-------------|
| Main (小花蟹) | Content editing + integration + push | Full repo R/W + push |
| Sub (general) | Data fill + CI fixes + charts | `articles/` + `.github/` + `skills/` (commit on own branch only) |

---

## 4. Priority

| Priority | Change | Rationale |
|----------|--------|-----------|
| **P0** | Unify Handoff/Dispatch → Task Board | Eliminates duplication; currently confusing |
| **P0** | Branch-per-Agent model | Prerequisite for parallelism |
| **P1** | Simplify identity system | Reduces handoff fill cost |
| **P1** | Two-stage PR pipeline | Non-blocking, review-friendly |
| **P2** | Merge Sub Agents | Reduces maintenance |
| **P2** | Abandon REST API push | Still usable for now, not urgent |

---

## 5. Core Principle

> Let Sub Agents own their branches. Make the Main Agent a merge decision-maker, not a push machine.
