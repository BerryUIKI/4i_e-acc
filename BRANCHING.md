# Branching & Collaboration Workflow

This repository follows a **two-tier trunk workflow**: feature branches → `dev` → `main`.

- `main` is always releasable. Branch protection forbids direct pushes (force-push and deletion blocked, admins included).
- `dev` is the integration branch for ongoing writing. Branch protection requires a PR (direct pushes blocked, admins included).
- Every change ships: short-lived feature branch → **PR to `dev`** (writing / content work) → **PR to `main`** (release).
- As the repository owner you may self-merge PRs (pragmatic mode) — you still must open a PR; you just don't need an external approver. `dev` allows self-merge with 0 approvals; `main` requires 1 approval (owner can self-approve via a temporary protection downgrade if needed).

## Branch naming

Prefix by intent. All lowercase, hyphenated, short. Keep one logical change per branch.

| Prefix | Use for |
|--------|---------|
| `docs/<topic>` | Investment-doc / README content (`reports/`, `research/`, `portfolio/`, `market/`, `strategies/`, `data/`, `archive/`, `assets/`) |
| `article/<yyyy-slug>` | New or revised long-form essay under `articles/` |
| `fix/<desc>` | Broken links, typos, structural fixes |
| `ci/<desc>` | CI / GitHub Actions / scripts under `.github/` |
| `feat/<desc>` | New structural features (folder schemes, templates) |
| `chore/<desc>` | Repo maintenance (e.g. this branching doc) |

Examples: `docs/macro-q3-outlook`, `article/2026-quadruple-long-life`, `fix/broken-readme-links`, `ci/link-checker`.

## Rules

- Branch **from the latest `dev`** (or `main` for hotfixes); **target `dev`** for normal work.
- Keep branches **short-lived**; one concern per branch.
- **Squash-merge** to keep history linear; delete the branch after merge.
- **Promote to `main` only when the content is release-ready** (whole book complete, assets in place, checks passing) — open a PR from `dev` → `main`.
- Never commit secrets — the repo is **public**.

## Lifecycle

1. `git switch -c <prefix>/<name>` (branch from `dev`)
2. Edit, then commit. This repo sets `commit.gpgsign=true` via a 1Password SSH key; if signing is unavailable in your environment, use `git -c commit.gpgsign=false commit …`.
3. `git push -u origin <prefix>/<name>`
4. Open a PR to `dev` → review / self-merge (squash) → delete the branch.
5. When the milestone is release-ready, open a PR `dev` → `main` → merge (squash).

See `AGENTS.md` for the agent-facing summary and `CONTRIBUTING.md` for the full human-facing workflow.
