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
- **Data provenance required.** Every chart, table, and data file must cite its source. See `agents/references/data-provenance.md`.

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
- `repo_salt`: See `agents/handoffs/agent-roster.md` for the fixed repo salt value.

**ShortAgentID**: last 10 hex chars of the full SHA256 UID.

### 🚫 Commit traceability
Every commit message MUST start with the `[ShortAgentID]` tag. Example: `[305cde212a] docs: fix typo in README`

### 🚫 Push restriction (Sub agents)
Sub agents SHALL NOT push to remote origin. Only bound Main agents execute `git push`. All code changes and handoff archives are aggregated and pushed by the bound Main agent exclusively.

### 🚫 Git local identity binding
1. **Main agent activation**: upon activation, Main agent MUST configure repo-local git identity using:
   ```
   git config user.name "[{ShortAgentID}]"
   git config user.email "{ShortAgentID}@agents.local"
   ```
   This is repo-local (`--local` scope). Never modify global git config.
2. **Sub agents cannot modify git config.** Sub agents do not configure `user.name` / `user.email`; their commits are not pushed directly.
3. **🟡 CI double validation on PR merge**: CI extracts both the git committer identity AND the `[ShortAgentID]` tag from each commit message. It then cross-references against `agents/handoffs/agent-roster.md`:
   - If commit message tag is a Sub agent ShortAgentID → verify the git committer is its bound Main agent.
   - If commit message tag is a Main agent ShortAgentID → verify the git committer matches that Main agent.
   - Block merge if the binding relationship is not confirmed.
4. **Roster record**: each agent entry in `agent-roster.md` MUST include git local identity fields (`git_user_name`, `git_user_email`).

### 🚫 Agent lifecycle validation on merge
CI pre-merge check extracts `[ShortAgentID]` from commit messages and validates against `agents/handoffs/agent-roster.md`. Merge is blocked if the ShortAgentID does not exist or its lifecycle status is `SUSPENDED`, `RETIRED`, or `DRAFT`.

**Lifecycle states**: `ACTIVE` | `SUSPENDED` | `RETIRED` | `DRAFT`. See `agents/handoffs/agent-roster.md`.

### Registration workflow
1. Main agent collects device fingerprint, role, and UTC register timestamp.
2. Compute full SHA256 UID + ShortAgentID.
3. Insert record into `agents/handoffs/agent-roster.md` with status `DRAFT`.
4. Main agent validates metadata and updates status to `ACTIVE`.

### Handoff documents
- All handoff documents live in `agents/handoffs/`.
- Naming: `handoff-{ShortAgentID}-{UTC_YYYYMMDD-HHMM}.md`.
- Template: `agents/handoffs/handoff-template.md`.
- Roster: `agents/handoffs/agent-roster.md`.
- Draft/temporary handoff files must be added to `.gitignore`; only finalized handoffs are committed.

### 🚫 Handoff reception
Upon receiving any handoff document in `agents/handoffs/`, every agent MUST execute the full validation workflow defined in `agents/workflows/handoff-reception.md`:
1. **Roster validation** — reject unregistered or non-ACTIVE agents; ask user for confirmation.
2. **Role scope check** — reject tasks outside the receiving agent's domain; Sub agents must reject push-required handoffs.
3. **Push status check** — verify issuer's work is on remote.
4. **File integrity check** — verify all referenced files exist.
5. **Cleanup** — delete the handoff file after acceptance; remove stale handoffs.

Failure at step 1 or role-scope push violation is a hard abort. All other failures require explicit user confirmation before proceeding.

## Project structure

- **`articles/`**: one folder per essay `<yyyy>-<english-slug>/`. Rules in `articles/STYLE.md`.
- **`assets/dollarhua/`**: shared mascot IP. Read `agents/references/dollarhua-ip.md` before generating visuals.
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
| Agent roster & lifecycle | `agents/handoffs/agent-roster.md` |
| Handoff template | `agents/handoffs/handoff-template.md` |
| Long-term roadmap | `agents/handoffs/roadmap.md` |
| IP character (DollarHua) | `agents/references/dollarhua-ip.md` |
| Data provenance rules | `agents/references/data-provenance.md` |
| File naming conventions | `agents/references/file-naming.md` |
| Doc-writer agent init (305cde212a) | `agents/doc-writer.md` |
| Sub-agent status files | `agents/sub-agents/` |
| Task dispatch specs | `agents/dispatches/` |
| Multi-agent workflow | `agents/workflows/multi-agent-collaboration.md` |
| Handoff reception & validation | `agents/workflows/handoff-reception.md` |
| Git safety + API push | `agents/workflows/git-safety.md` |
