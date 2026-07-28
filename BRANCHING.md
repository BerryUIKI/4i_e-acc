# Branching & Collaboration Workflow

This repository follows **GitHub Flow**: `main` is always releasable, and every change ships through a short-lived branch + Pull Request. Branch protection forbids direct pushes to `main` (force-push and branch deletion are also blocked). As the repository owner you may self-merge PRs (pragmatic mode) — you still must open a PR; you just don't need an external approver.

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

- Branch **from the latest `main`**; target **only `main`**. No long-lived `develop` / `release` branches — a docs repo does not need them.
- Keep branches **short-lived**; one concern per branch.
- **Squash-merge** to keep history linear; delete the branch after merge.
- Never commit secrets — the repo is **public**.

## Lifecycle

1. `git switch -c <prefix>/<name>`
2. Edit, then commit. This repo sets `commit.gpgsign=true` via a 1Password SSH key; if signing is unavailable in your environment, use `git -c commit.gpgsign=false commit …`.
3. `git push -u origin <prefix>/<name>`
4. Open a PR to `main` → review / self-merge (squash) → delete the branch.

See `AGENTS.md` for the agent-facing summary and `CONTRIBUTING.md` for the full human-facing workflow.
