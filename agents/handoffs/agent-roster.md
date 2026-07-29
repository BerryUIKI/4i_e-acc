# Agent Roster — Central Registry

> **Repo fixed salt**: `022a2e4326219260` (SHA256 of `BerryUIKI/4i_e-acc|quadruple-cognition`, truncated to 16 hex chars).  
> Use this salt in ALL agent ID computations for this repo.

ShortAgentID is the last 10 hex chars of the full SHA256 UID. Full algorithm: see `../../AGENTS.md` section "Agent Identity & Git Traceability".

---

| ShortAgentID | Type | Bound Main | Role | Status | Device FP | Registered (UTC ms) |
|---|---|---|---|---|---|---|
| `305cde212a` | MAIN | ROOT | `doc-writer` | ACTIVE | `0101aaa313a11c56` | `1785297428514` |

---

## Full records

### `305cde212a`

| Field | Value |
|---|---|
| ShortAgentID | `305cde212a` |
| Full SHA256 UID | `f48eccdd8da6f61fafc44bc0cd8f7338589a645d1b056c3d5b8eb6305cde212a` |
| Agent Type | MAIN |
| Bound Main Agent ShortID | ROOT |
| Desensitized Device Fingerprint | `0101aaa313a11c56` |
| Agent Role Name | `doc-writer` |
| UTC Register Timestamp (ms) | `1785297428514` |
| Lifecycle Status | ACTIVE |
| Allowed Workspaces | Full repo: `articles/`, `agents/`, `.github/`, `skills/`, `assets/` |
| Permissions | Register sub-agents, generate handoff dispatch files, aggregate outputs, execute git push |
| Human-facing name | 小花蟹 (Little Flower Crab) |
