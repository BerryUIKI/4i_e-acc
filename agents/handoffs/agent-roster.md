# Agent Roster — Central Registry

> **Repo fixed salt**: `022a2e4326219260` (SHA256 of `BerryUIKI/4i_e-acc|quadruple-cognition`, truncated to 16 hex chars).  
> Use this salt in ALL agent ID computations for this repo.

ShortAgentID is the last 10 hex chars of the full SHA256 UID. Full algorithm: see `../../AGENTS.md` section "Agent Identity & Git Traceability".

---

## Quick-lookup summary

| ShortAgentID | Type | Bound Main | Role | Status |
|---|---|---|---|---|
| `42f78f1d3e` | MAIN | ROOT | `doc-writer` | ACTIVE |
| `305cde212a` | MAIN | ROOT | `doc-writer` | RETIRED |
| `8f9b1fd0b6` | SUB | `42f78f1d3e` | `ci-sub` | ACTIVE |

---

## Main Agent: `42f78f1d3e`

### Metadata

| Field | Value |
|---|---|
| ShortAgentID | `42f78f1d3e` |
| Full SHA256 UID | `082f0e0d866198984b53b62740103be8178485e50e8e22ca10e9f642f78f1d3e` |
| Agent Type | MAIN |
| Agent Role Name | `doc-writer` |
| Lifecycle Status | ACTIVE |
| Primary Device Fingerprint | `0101aaa313a11c56` |
| Bound Device Fingerprints | `0101aaa313a11c56` |
| UTC Register Timestamp (ms) | `1785324315251` |
| Allowed Workspaces | Full repo: `articles/`, `agents/`, `.github/`, `skills/`, `assets/` |
| Permissions | Register sub-agents, generate handoff dispatch files, aggregate outputs, execute git push |
| Git user name | `[42f78f1d3e]` |
| Git user email | `42f78f1d3e@agents.local` |
| Human-facing name | 小花蟹 (Little Flower Crab) |
| Successor of | `305cde212a` |

### Bound Sub Agents

| ShortAgentID | Role | Status | Device FP | Registered (UTC ms) |
|---|---|---|---|---|
| `8f9b1fd0b6` | `ci-sub` | ACTIVE | `0101aaa313a11c56` | `1785320624265` |

---

## Main Agent: `305cde212a` (RETIRED)

### Metadata

| Field | Value |
|---|---|
| ShortAgentID | `305cde212a` |
| Full SHA256 UID | `f48eccdd8da6f61fafc44bc0cd8f7338589a645d1b056c3d5b8eb6305cde212a` |
| Agent Type | MAIN |
| Agent Role Name | `doc-writer` |
| Lifecycle Status | RETIRED |
| Primary Device Fingerprint | `0101aaa313a11c56` |
| Bound Device Fingerprints | `0101aaa313a11c56` |
| UTC Register Timestamp (ms) | `1785297428514` |
| Allowed Workspaces | Full repo: `articles/`, `agents/`, `.github/`, `skills/`, `assets/` |
| Permissions | Register sub-agents, generate handoff dispatch files, aggregate outputs, execute git push |
| Git user name | `[305cde212a]` |
| Git user email | `305cde212a@agents.local` |
| Human-facing name | 小花蟹 (Little Flower Crab) |
| Successor | `42f78f1d3e` |

---

## Sub Agent: `8f9b1fd0b6`

### Metadata

| Field | Value |
|---|---|
| ShortAgentID | `8f9b1fd0b6` |
| Agent Type | SUB |
| Bound Main | `42f78f1d3e` |
| Agent Role Name | `ci-sub` |
| Lifecycle Status | ACTIVE |
| Primary Device Fingerprint | `0101aaa313a11c56` |
| UTC Register Timestamp (ms) | `1785320624265` |
| Allowed Workspaces | `.github/`, `skills/pdf-toolbook/` |
| Permissions | Commit only; no push. Dispatch via `agents/dispatches/`. |
| Git Restrictions | Sub agents SHALL NOT push; commits tagged with own ShortAgentID |
| Human-facing name | dev-box-ci-sub |

---

## Multi-device binding

When a Main agent operates from multiple devices (e.g., desktop + laptop), each device generates a different device fingerprint, which would produce a different SHA256 UID. To maintain a single consistent agent identity:

### Binding rules
1. **Primary fingerprint**: the first registered device fingerprint is the canonical one. All new devices are bound to this identity.
2. **Bound fingerprints list**: the `Bound Device Fingerprints` field is a comma-separated list of all authorized device fingerprints for this agent.
3. **Registration flow for a new device**:
   - Generate the new device fingerprint using the same algorithm (`SHA256({hostname}-{username})[:16]`).
   - Append the fingerprint to the `Bound Device Fingerprints` field.
   - The agent continues using the original ShortAgentID and Full UID — no recomputation.
   - Record UTC timestamp of the binding in a handoff log entry.
4. **Validation**: CI checks that the git committer or handoff log references an agent whose `Bound Device Fingerprints` includes an entry matching the deployment environment's fingerprint.

---

## Repository salt rotation plan

If the repo fixed salt (`022a2e4326219260`) is compromised or needs rotation for policy reasons, all existing agent UIDs become invalid.

### Rotation procedure
1. **Announce rotation** via a dedicated handoff file in `agents/handoffs/` with at least 48 hours notice to all active Main agents.
2. **Freeze agent registration**: no new agent registrations during the rotation window.
3. **Generate new salt**: `SHA256({previous_salt}|{rotation_UTC_ms})[:16]`. Record both old and new salt in this file during the transition.
4. **Recompute all agent UIDs** using the new salt and the original registration timestamps.
5. **Update the summary table and full records** with new ShortAgentIDs and Full UIDs.
6. **Retain old UIDs** in the `Archived UIDs` section for historical audit (commits tagged with old ShortAgentIDs remain traceable).
7. **Update git config**: each Main agent reconfigures `user.name` / `user.email` with the new ShortAgentID.
8. **Resume operations**: remove the freeze, announce completion via handoff.

### Current salt history

| Salt | Active Period | Status |
|---|---|---|
| `022a2e4326219260` | 2026-07-29 – present | ACTIVE |

## Archived UIDs
<!-- Populated after first salt rotation. Maps old-UID → new-UID for audit continuity. -->
(None — no rotation has occurred yet.)
