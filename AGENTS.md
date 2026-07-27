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
- **`articles/`**: long-form essays. One folder per essay `<yyyy>-<english-slug>/` containing `manuscript.md` (Chinese-primary, English inline), `notes.md`, `references.md`, `assets/`. Rules live in `articles/STYLE.md`; scaffold in `articles/_template/`.
- **`CONTRIBUTING.md` / `CONTRIBUTING-zh_CN.md`**: human-facing workflow and the rationale for the PR-only policy.

## Shared IP asset — DollarHua (花有财)
A **reusable mascot IP** lives at `assets/dollarhua/` (character pack v1.4 Lite, designed by the repo owner). It is the **single source of truth** for the workspace's friendly brand face — use it for headers, callouts, cards, article heroes, status banners, etc.

- Read `assets/dollarhua/README.md` (EN) / `README-zh_CN.md` (中文) before generating anything with the character.
- Identity, the 8-color standard, the file map, and the base prompt (`prompt_seed.txt`) are all defined there.
- Respect the rules: keep the signature pink (`#FEC6CD`) as the primary identity color, never recolor the bronze coin pendant to bright yellow gold, and treat the reference PNGs as authoritative for rendered appearance.
- Always pull from `assets/dollarhua/` — do not introduce a divergent copy elsewhere in the repo.

## Verify before pushing
- `python .github/scripts/check_links.py` — offline relative-link check.
- `python .github/scripts/check_style.py` — structure/style check per `STYLE.md`.
- Both also run in CI on every PR and weekly.

## Gotchas
- Repo is **public** — never commit secrets (keys/tokens stay in `~/.ssh`, outside the repo).
- Top-level doc folders are one level deep: link the root with `../README.md`, **not** `../../`.
