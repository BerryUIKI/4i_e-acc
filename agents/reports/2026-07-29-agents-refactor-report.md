# Refactoring Work Report — AGENTS.md & agents/ System

**Date**: 2026-07-29  
**Branch**: `article/2026-quadruple-long-life`  
**Executor**: `[305cde212a]` (doc-writer, ACTIVE)  

---

## 1. Final Repository Directory Tree

```
<repo-root>/
├── AGENTS.md                                    # Rewritten (4.7 KB, hard rules only)
├── .gitignore                                   # Updated (+ handoff draft exclusions)
└── agents/
    ├── handoffs/
    │   ├── agent-roster.md                      # New — central registration ledger (1 agent)
    │   ├── handoff-template.md                  # New — standardized 8-section template
    │   └── roadmap.md                           # New — Q3 2026 – 2027 planning
    ├── references/
    │   ├── data-provenance.md                   # New — chart/table/data source rules
    │   ├── dollarhua-ip.md                      # New — mascot IP reference (migrated from AGENTS.md)
    │   └── file-naming.md                       # New — ASCII/kebab-case conventions (migrated from AGENTS.md)
    └── workflows/
        ├── git-safety.md                        # New — force-push ban, REST API push guide
        └── multi-agent-collaboration.md         # New — sub-agent protocol, prompt template, checklist
```

**No redundant sub-directory AGENTS.md files exist.** Only the root `AGENTS.md` carries mandatory rules.

---

## 2. File Operations Summary

### Rewritten (1)
| File | Before | After |
|------|--------|-------|
| `AGENTS.md` | 7.5 KB mixed rules + long-form content | 4.7 KB hard constraints + pointers only |

### Newly Created (9)
| File | Purpose |
|------|---------|
| `agents/handoffs/agent-roster.md` | Central agent registry with lifecycle states, SHA256 ID, git config |
| `agents/handoffs/handoff-template.md` | Unified 8-section template with mandatory metadata header |
| `agents/handoffs/roadmap.md` | Long-term iteration plan (Q3 2026 – 2027) |
| `agents/references/data-provenance.md` | Data source documentation requirements |
| `agents/references/dollarhua-ip.md` | Mascot IP usage rules |
| `agents/references/file-naming.md` | ASCII / kebab-case naming conventions |
| `agents/workflows/git-safety.md` | Force-push ban, GitHub REST API push guide |
| `agents/workflows/multi-agent-collaboration.md` | Sub-agent dispatch protocol, prompt template, session checklist |
| `agents/handoffs/` (directory) | Structural root for all handoff + identity artifacts |

### Updated (1)
| File | Change |
|------|--------|
| `.gitignore` | Added `agents/handoffs/draft-*`, `tmp-*`, `.wip-*` exclusion patterns |

### Deleted (3)
| File | Reason |
|------|--------|
| `HANDOFF-2026-07-28.md` (root) | Moved to `agents/handoffs/`, then deleted (served purpose) |
| `articles/2026-quadruple-long-life/illustrations/HANDOFF-TO-NEXT.md` | Moved to `agents/handoffs/`, then deleted (served purpose) |
| `agents/handoffs/2026-07-28.md` & `illustrations-2026-07-28.md` | Historical handoff records; deleted after serving purpose |

### Relevant Commits (this session)
```
15da894  [305cde212a] feat: add git local identity binding rules + roster git config fields
7baae1f  [305cde212a] feat: agent identity system, handoff template, roster, roadmap, git trace rules
c2996d5  chore: delete handoff files, fix Chinese in dollarhua-ip.md
879f6d3  chore: remove old handoff (moved to agents/handoffs/)
2ae9a53  refactor: slim root AGENTS.md, create agents/ with references/workflows/handoffs
f1207a0  docs(agents): add multi-agent collaboration standard
```

---

## 3. Key Implementation Points

### 3.1 Agent ID Generation (SHA256)
- **Algorithm**: `SHA256(device_fp|role|bound_main_short_id|UTC_register_ms|repo_salt)`
- **Device fingerprint**: SHA256 of `{hostname}-{username}`, truncated to 16 hex (desensitized, reproducible)
- **Repo salt**: `022a2e4326219260` (fixed, derived from `BerryUIKI/4i_e-acc|quadruple-cognition`)
- **ShortAgentID**: last 10 hex chars of the full digest
- Both Main and Sub agents use identical algorithm; only difference is `bound_main_short_id` (`ROOT` vs actual ShortAgentID)

### 3.2 Registered Agent
| Field | Value |
|-------|-------|
| ShortAgentID | `305cde212a` |
| Type | MAIN |
| Role | `doc-writer` |
| Status | ACTIVE |
| Git user name | `[305cde212a]` |
| Git user email | `305cde212a@agents.local` |

### 3.3 Main–Sub Agent Handover
- `agents/handoffs/` is the **only authorized communication medium**.
- Main → Sub: task dispatch handoff file (based on `handoff-template.md`).
- Sub → Main: result delivery handoff file with own ShortAgentID.
- Sub agents cannot access Main agent private workspace; all context is via handoff files.
- Naming: `handoff-{ShortAgentID}-{UTC_YYYYMMDD-HHMM}.md`.

### 3.4 Lifecycle Status Control
Four states: `ACTIVE` | `SUSPENDED` | `RETIRED` | `DRAFT`.
- Registration starts as `DRAFT` → Main agent validates → `ACTIVE`.
- CI merge validation blocks commits from `SUSPENDED` / `RETIRED` / `DRAFT` agents.
- `SUSPENDED`: cannot generate new handoffs or trigger git push; history retained.
- `RETIRED`: permanent deactivation; all trace data retained for audit.

### 3.5 Git Traceability
- Every commit message MUST start with `[ShortAgentID]`. Example: `[305cde212a] docs: ...`
- CI pre-merge extracts `[ShortAgentID]` → validates against `agent-roster.md` status.

### 3.6 Git Local Identity Binding
- Main agent activates: `git config --local user.name "[{ShortAgentID}]"` and `user.email "{ShortAgentID}@agents.local"`.
- Sub agents cannot modify git config.
- CI double validation: committer identity MUST match the agent bound to the commit message's ShortAgentID.
- Binding relationship recorded in `agent-roster.md` (`git_user_name`, `git_user_email`).

---

## 4. Hard Constraints Embedded in Root AGENTS.md

All marked with 🚫 (non-overridable by any sub-directory `AGENTS.md`):

| # | Rule |
|---|------|
| 1 | Never push to `main` — branch + PR only, squash-merge |
| 2 | Never force-push on any shared branch |
| 3 | Never commit secrets (tokens/keys stay outside repo tree) |
| 4 | English folder names only |
| 5 | ASCII-only repo paths, kebab-case, no CJK characters |
| 6 | Data provenance required on every chart/table/data file |
| 7 | Every commit message must start with `[ShortAgentID]` |
| 8 | Sub agents SHALL NOT push to remote origin |
| 9 | Agent lifecycle validation on merge (block SUSPENDED/RETIRED/DRAFT) |
| 10 | Git local identity binding (repo-local config, no global changes) |

---

## 5. Unfinished Items & Potential Risks

### Unfinished
- [ ] CI pre-merge check script (ShortAgentID extraction + roster validation) — **not yet implemented**. Spec is defined in `AGENTS.md` but `.github/workflows/` has no enforcement pipeline.
- [ ] CI git committer identity double-validation script — spec defined, not implemented.
- [ ] Sub-agent end-to-end test: register a DRAFT sub-agent, generate dispatch handoff, execute task, deliver result, main agent aggregate — **workflow defined but never exercised**.

### Potential Compatibility Risks
- **Sandbox environments**: local git is frequently broken on this project. The REST API push fallback (documented in `agents/workflows/git-safety.md`) bypasses normal git identity — commits made via API won't carry the `[ShortAgentID]` git committer signature. This creates a gap in the traceability chain for API-pushed commits.
- **Multi-device fingerprint**: the device fingerprint algorithm uses `{hostname}-{username}`. If a Main agent moves between devices (e.g., desktop ↔ laptop), it will generate a different fingerprint and thus a different UID. The roster currently has no mechanism for device migration or multi-device binding.
- **Salt rotation**: the repo salt is hardcoded in `agent-roster.md`. If compromised or needs rotation, all existing agent UIDs become invalid. No rotation procedure is defined.
- **Language boundary**: `multi-agent-collaboration.md` contains Chinese proper nouns (花花, 小花蟹) and a Chinese prompt template — these are operational necessities but break the English-only rule. Marked as intentional exceptions.
