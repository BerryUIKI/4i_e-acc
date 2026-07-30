# Agent Roster — Central Registry

ShortAgentID = last 8 hex chars of SHA256(`[device_fp]|[role]|[bound_main]|[UTC_register_ms]|[repo_salt]`).

| ShortAgentID | Type | Bound Main | Role | Status |
|---|---|---|---|---|---|
| `f78f1d3e` | MAIN | ROOT | `doc-writer` | ACTIVE |
| `5cde212a` | MAIN | ROOT | `doc-writer` | RETIRED |
| `9b1fd0b6` | SUB | `f78f1d3e` | `ci-sub` | RETIRED |
| `dfea5fc1` | SUB | `f78f1d3e` | `doc-data` | RETIRED |

---

## Main Agent: `f78f1d3e`

| Field | Value |
|---|---|
| ShortAgentID | `f78f1d3e` |
| Agent Type | MAIN |
| Role | `doc-writer` |
| Status | ACTIVE |
| Git user name | `[f78f1d3e]` |
| Git user email | `f78f1d3e@agents.local` |
| Human-facing name | 小花蟹 (Little Flower Crab) |
| Successor of | `5cde212a` |
| Permissions | Full repo R/W + push |

### Bound Sub Agents (all RETIRED)

| ShortAgentID | Role | Status |
|---|---|---|
| `9b1fd0b6` | `ci-sub` | RETIRED — last active 2026-07-29 |
| `dfea5fc1` | `doc-data` | RETIRED — last active 2026-07-29 |

---

## Sub Agent lifecycle

Sub Agents are **registered on demand**. When MAIN needs parallel execution:

1. MAIN generates a new ShortAgentID (device footprint + role + timestamp)
2. Records it in this roster with status `ACTIVE`
3. Writes its role definition in `sub-agents/{name}.md`
4. Writes its context window definition in `context/{name}.md`
5. When the sub-task completes, MAIN marks it `RETIRED`
6. `sub-agents/` and `context/` files for retired subs are kept as archive

No pre-registered Sub Agents. No ACTIVE Sub Agent when there's no parallel work.

---

## Main Agent: `5cde212a` (RETIRED)

| Field | Value |
|---|---|
| ShortAgentID | `5cde212a` |
| Agent Type | MAIN |
| Role | `doc-writer` |
| Status | RETIRED |
| Human-facing name | 小花蟹 (Little Flower Crab) |
| Successor | `f78f1d3e` |

---

## Sub Agent: `9b1fd0b6` (RETIRED)

| Field | Value |
|---|---|
| ShortAgentID | `9b1fd0b6` |
| Agent Type | SUB |
| Bound Main | `f78f1d3e` |
| Role | `ci-sub` |
| Status | RETIRED |
| Allowed Workspaces | `.github/`, `skills/` |
| Human-facing name | dev-box-ci-sub |

---

## Sub Agent: `dfea5fc1` (RETIRED)

| Field | Value |
|---|---|
| ShortAgentID | `dfea5fc1` |
| Agent Type | SUB |
| Bound Main | `f78f1d3e` |
| Role | `doc-data` |
| Status | RETIRED |
| Allowed Workspaces | `articles/` |
| Human-facing name | dev-box-doc-data |
