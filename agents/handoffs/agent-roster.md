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
| Git user name | `[305cde212a]` |
| Git user email | `305cde212a@agents.local` |
| Primary Device Fingerprint | `0101aaa313a11c56` |
| Bound Device Fingerprints | `0101aaa313a11c56` |
| Human-facing name | 小花蟹 (Little Flower Crab) |

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
6. **Retain old UIDs** in an `## Archived UIDs` section for historical audit (commits tagged with old ShortAgentIDs remain traceable).
7. **Update git config**: each Main agent reconfigures `user.name` / `user.email` with the new ShortAgentID.
8. **Resume operations**: remove the freeze, announce completion via handoff.

### Current salt history
| Salt | Active Period | Status |
|---|---|---|
| `022a2e4326219260` | 2026-07-29 – present | ACTIVE |

## Archived UIDs
<!-- Populated after first salt rotation. Maps old-UID → new-UID for audit continuity. -->
(None — no rotation has occurred yet.)
