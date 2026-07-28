# AGENTS.md

Guidance for AI agents operating in this repo — a **bilingual investment-document workspace**. Folder names stay English; `README.md` is the English default and `README-zh_CN.md` is the Chinese version. Docs are cross-linked with relative paths.

## Hard rules (must obey)
- **Never push to `main`.** All changes require a branch + Pull Request. Branch protection blocks direct pushes, force-pushes, and deletion of `main`.
- **Admin self-merges** PRs (pragmatic mode) — don't wait for an external reviewer when none exists.
- **Folder names in English**; document titles may be bilingual.

## How to make a change
1. Branch per `BRANCHING.md` (prefix by intent: `docs/`, `article/`, `fix/`, `ci/`, `feat/`, `chore/`; never `main`).
2. Edit, then commit. This repo sets `commit.gpgsign=true` via a 1Password SSH key; if signing is unavailable in the agent environment, commit with `git -c commit.gpgsign=false commit …` (don't let it fail silently).
3. Push: `git push -u origin <branch>`.
4. Open a PR to `main` (squash-merge) and give the user the link to merge.

## Structure pointers (read the files; don't duplicate)
- **Doc folders** (`reports/`, `research/`, `portfolio/`, `market/`, `strategies/`, `data/`, `archive/`, `assets/`): each has a bilingual README index — drop investment docs there.
- **`articles/`**: long-form essays and books. One folder per project `<yyyy>-<english-slug>/`. Short essays use `manuscript.md` (Chinese-primary, English inline), `notes.md`, `references.md`, `assets/` — rules live in `articles/STYLE.md`; scaffold in `articles/_template/`. **Book-length projects** may use their own layout and conventions — see their `agents.md` (e.g. `2026-quadruple-long-life/`).
- **`CONTRIBUTING.md` / `CONTRIBUTING-zh_CN.md`**: human-facing workflow and the rationale for the PR-only policy.

## Shared IP asset — DollarHua (花有财)
A **reusable mascot IP** lives at `assets/dollarhua/` (character pack v1.4 Lite, designed by the repo owner). It is the **single source of truth** for the workspace's friendly brand face — use it for headers, callouts, cards, article heroes, status banners, etc.

- Read `assets/dollarhua/README.md` (EN) / `README-zh_CN.md` (中文) before generating anything with the character.
- Identity, the 8-color standard, the file map, and the base prompt (`prompt_seed.txt`) are all defined there.
- Respect the rules: keep the signature pink (`#FEC6CD`) as the primary identity color, never recolor the bronze coin pendant to bright yellow gold, and treat the reference PNGs as authoritative for rendered appearance.
- Always pull from `assets/dollarhua/` — do not introduce a divergent copy elsewhere in the repo.

## Flagship book -- 《四倍做多认知，长期做多人生》
`articles/2026-quadruple-long-life/` is a 30-chapter + epilogue + 12-appendices investment guidebook.
It uses a multi-directory layout (`Front-Matter/`, `Main-Text/`, `Appendices/`, `illustrations/`)
and follows its own `agents.md` rather than `articles/STYLE.md`.
See its [README](./articles/2026-quadruple-long-life/README.md) for the full structure and writing conventions.

## Multi-agent / Multi-device Collaboration

This repo is worked on by multiple AI agents across multiple devices.
To avoid history disconnects, lost work, and PR failures, follow these rules.

### Sync protocol — every time, no exceptions
1. **Pull before anything:** `git fetch && git pull --ff-only`. Verify you are on the latest remote.
2. **Push regularly:** commit + `git push` after each meaningful chunk. Small, frequent pushes prevent conflicts.
3. **NEVER force-push** (`--force`, `--force-with-lease`). Force-push rewrites shared history and can disconnect the branch from `main`, breaking PR creation entirely.
4. **Before handing off:** `git push` everything. No half-committed state should be the handoff point.

### Handoff document — `HANDOFF-YYYY-MM-DD.md`
When passing work to another agent/device, write this file at the **workspace root**.

```markdown
# HANDOFF-YYYY-MM-DD

## Current state
- Branch: `<name>`
- Last pushed commit: `git log --oneline -1` (paste the output)
- CI status: pass / fail / not applicable

## Work completed
- [Bullet list of what was done since last handoff]

## Work in progress (not yet finished / not yet pushed)
- [Bullet list — empty if everything is pushed]

## To-do / Next steps
- [Prioritised list for the receiving agent]

## Data gaps / Blockers
- [Missing data, external dependencies, known issues]

## Prompt for receiving agent
> [Copy-paste ready prompt — code block format. Be specific about which files
> to work on, what to do, where to commit, and whether to push.]
```

**After receiving:** read the handoff → `git fetch && git pull --ff-only` → verify → continue from "Next steps".

## Verify before pushing
- `python .github/scripts/check_links.py` — offline relative-link check.
- `python .github/scripts/check_style.py` — structure/style check per `STYLE.md`.
- Both also run in CI on every PR and weekly.

## Gotchas
- Repo is **public** — never commit secrets (keys/tokens stay in `~/.ssh`, outside the repo).
- Top-level doc folders are one level deep: link the root with `../README.md`, **not** `../../`.
