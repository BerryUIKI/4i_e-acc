# AGENTS.md — Repository Root

Baseline rules for all AI agents operating in this repo. Sub-directory `AGENTS.md` files may add module-specific rules but cannot override any hard rule below.

**Inheritance priority**: current-dir `AGENTS.md` > parent-dir `AGENTS.md` > this file. Hard rules (marked 🚫) are non-overridable at any level.

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

## Project structure

- **`articles/`**: one folder per essay `<yyyy>-<english-slug>/`. Rules in `articles/STYLE.md`.
- **`assets/dollarhua/`**: shared mascot IP. Read `agents/references/dollarhua-ip.md` before generating visuals.
- **Doc folders** (`reports/`, `data/`, `research/`, etc.): drop investment docs, cross-link with relative paths.

## Agent collaboration

Multiple agents share this repo. See `agents/workflows/multi-agent-collaboration.md` for the full protocol: handoff format, sub-agent prompt template, and session checklist.

**Git safety**: if local git is broken (sandbox), use the GitHub REST API. Guide at `agents/workflows/git-safety.md`.

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
| IP character (DollarHua) | `agents/references/dollarhua-ip.md` |
| Data provenance rules | `agents/references/data-provenance.md` |
| File naming conventions | `agents/references/file-naming.md` |
| Multi-agent workflow | `agents/workflows/multi-agent-collaboration.md` |
| Git safety + API push | `agents/workflows/git-safety.md` |
| Session handoffs | `agents/handoffs/` |
