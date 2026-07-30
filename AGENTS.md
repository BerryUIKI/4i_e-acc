# AGENTS.md — Repository Root

Baseline rules for all AI agents operating in this repo. Sub-directory `AGENTS.md` files may add module-specific rules but cannot override any hard rule below.

**Inheritance priority**: current-dir `AGENTS.md` > parent-dir `AGENTS.md` > this file. Hard rules (marked 🚫) are non-overridable at any level.

**Language**: All content under this file and `agents/` directory MUST be written in English only.

## 🚫 Hard rules

- **Never push to `main`.** Branch + PR only. Squash-merge.
- **Never force-push** on any shared branch. Silently erases other agents' commits.
- **Never commit secrets.** Tokens/keys stay outside the repo tree.
- **English folder names only.** Document content may be bilingual.
- **ASCII-only repo paths.** No spaces, no CJK characters. Use kebab-case.
- **Data provenance required.** Every chart, table, and data file must cite its source. See `agents/shared/references/data-provenance.md`.

## Workflow

1. Branch: `article/`, `fix/`, `feat/`, `ci/`, `docs/`, `chore/` prefix — never `main`.
2. Commit. If GPG signing unavailable: `git -c commit.gpgsign=false commit ...`.
3. Push + open PR to `main` (squash-merge).
4. Verify: `python .github/scripts/check_links.py` and `check_style.py` before push.

## Agent Identity & Git Traceability

### ID generation (shared algorithm for Main & Sub agents)
SHA256 of: `[device_fp]|[role]|[bound_main_short_id]|[UTC_register_ms]|[repo_salt]`
- `device_fp`: SHA256 of `{hostname}-{username}`, truncated to 16 hex chars (desensitized).
- `role`: `[domain]-[task-type]` format. Domains: `code` / `ci` / `doc` / `deploy` / `audit`.
- `bound_main_short_id`: `ROOT` for Main agents; bound Main's ShortAgentID for Sub agents.
- `repo_salt`: See `agents/0101aaa313a11c56/f78f1d3e/roster.md` for the fixed repo salt value.

**ShortAgentID**: last 8 hex chars of the full SHA256 UID.

### 🚫 Commit traceability
Every commit message MUST start with the `[ShortAgentID]` tag. Example: `[f78f1d3e] docs: fix typo in README`

### 🚫 Push restriction (Sub agents)
Sub agents SHALL NOT push to `main` or integration branches. They MAY push to their own feature branch (`sub/{ShortAgentID}/*`). Only bound Main agents execute pushes to `main` or integration branches.

### 🚫 Git local identity binding
1. **Main agent activation**: upon activation, Main agent MUST configure repo-local git identity using:
   ```
   git config user.name "[{ShortAgentID}]"
   git config user.email "{ShortAgentID}@agents.local"
   ```
   This is repo-local (`--local` scope). Never modify global git config.
2. **Sub agents MUST configure git local identity** using their own ShortAgentID, same format as Main (repo-local scope).
3. **🟡 CI double validation on PR merge**: CI extracts both the git committer identity AND the `[ShortAgentID]` tag from each commit message. It then cross-references against `agents/0101aaa313a11c56/f78f1d3e/roster.md`:
   - If commit message tag is a Sub agent ShortAgentID → verify the git committer is its bound Main agent.
   - If commit message tag is a Main agent ShortAgentID → verify the git committer matches that Main agent.
   - Block merge if the binding relationship is not confirmed.
4. **Roster record**: each agent entry in `agent-roster.md` MUST include git local identity fields (`git_user_name`, `git_user_email`).

### 🚫 Agent lifecycle validation on merge
CI pre-merge check extracts `[ShortAgentID]` from commit messages and validates against `agents/0101aaa313a11c56/f78f1d3e/roster.md`. Merge is blocked if the ShortAgentID does not exist or its lifecycle status is `SUSPENDED`, `RETIRED`, or `DRAFT`.

**Lifecycle states**: `ACTIVE` | `SUSPENDED` | `RETIRED` | `DRAFT`. See `agents/0101aaa313a11c56/f78f1d3e/roster.md`.

### Registration workflow

#### Main Agent registration
1. Main agent collects device fingerprint, role, and UTC register timestamp.
2. Compute full SHA256 UID + ShortAgentID.
3. Insert record into `agents/{main-id}/roster.md` with status `DRAFT`.
4. Main agent validates metadata and updates status to `ACTIVE`.

#### Sub Agent registration (self-registration)
1. Main agent writes a registration handoff with the Sub Agent's role and allowed workspaces.
2. Sub agent computes its own ShortAgentID (using the bound Main's ShortAgentID and device FP).
3. Sub agent creates `sub-agents/{name}.md` and `context/{name}.md`.
4. Sub agent inserts its record into `agents/{main-id}/roster.md` with status `ACTIVE`.
5. Sub agent configures git local identity, creates branch `sub/{ShortAgentID}/{task-slug}`, commits, and pushes.

### Handoff documents
- All handoff documents live in `agents/{main-id}/handoffs/` (per Main Agent).
- Naming: `handoff-{ShortAgentID}-{UTC_YYYYMMDD-HHMM}.md`.
- Template: `agents/shared/templates/handoff.md`.
- Roster: `agents/0101aaa313a11c56/f78f1d3e/roster.md`.
- Draft/temporary handoff files must be added to `.gitignore`; only finalized handoffs are committed.

### Main ↔ Sub communication
`agents/{main-id}/handoffs/` is the authorized communication medium between windows. SUB windows have no write access outside their allowed workspaces. See `agents/shared/workflows/multi-agent-collaboration.md`.

## Project structure

- **`articles/`**: one folder per essay `<yyyy>-<english-slug>/`. Rules in `articles/STYLE.md`.
- **`assets/dollarhua/`**: shared mascot IP. Read `agents/shared/references/dollarhua-ip.md` before generating visuals.
- **Doc folders** (`reports/`, `data/`, `research/`, etc.): drop investment docs, cross-link with relative paths.

## Sub-directory AGENTS.md template

When creating a module-level `AGENTS.md`, open with:

```markdown
# AGENTS.md — <module-name>
> Inherits from: `../../AGENTS.md` (non-overridable hard rules listed there).

## Module-specific rules
<!-- Only rules unique to this module. Do not repeat root rules. -->
```

## Further reference

| Topic | File |
|-------|------|
| Agent roster & lifecycle | `agents/0101aaa313a11c56/f78f1d3e/roster.md` |
| Handoff template | `agents/shared/templates/handoff.md` |
| Long-term roadmap | `agents/0101aaa313a11c56/f78f1d3e/roadmap.md` |
| IP character (DollarHua) | `agents/shared/references/dollarhua-ip.md` |
| Data provenance rules | `agents/shared/references/data-provenance.md` |
| File naming conventions | `agents/shared/references/file-naming.md` |
| Multi-window workflow | `agents/shared/workflows/multi-agent-collaboration.md` |
| Git safety + API push | `agents/shared/workflows/git-safety.md` |
| Multi-window architecture | `agents/0101aaa313a11c56/f78f1d3e/decisions/multi-window-architecture.md` |
