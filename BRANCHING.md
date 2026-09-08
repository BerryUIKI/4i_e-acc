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
| `epic/<milestone>` | **On-demand only.** Theme branch for a milestone that needs independent acceptance (e.g. `epic/book-v0.2`). Collects several feature branches; squash back to `dev` when the milestone is accepted, then delete. Never permanent. |
| `release/vX.Y` | **On-demand only.** Release-freeze branch cut from `dev` when a milestone is close to publishing; fix bugs there, merge to `main` (and back to `dev`), tag `vX.Y`, delete. Never permanent. |

Examples: `docs/macro-q3-outlook`, `article/2026-quadruple-long-life`, `fix/broken-readme-links`, `ci/link-checker`.

## Rules

- Branch **from the latest `dev`** (or `main` for hotfixes); **target `dev`** for normal work.
- Keep branches **short-lived**; one concern per branch.
- **Squash-merge** to keep history linear; delete the branch after merge.
- **Promote to `main` only when the content is release-ready** (whole book complete, assets in place, checks passing) — open a PR from `dev` → `main`.
- Never commit secrets — the repo is **public**.

## Trunk model (adopted 2026-09-07)

Two **permanent** trunks only: `main` (stable release) and `dev` (rolling integration).

- Every regular change: short-lived feature branch → PR → `dev` → (when release-ready) → `main`.
- `epic/` and `release/` branches are **on-demand, temporary** — they add a layer only while a milestone needs it, then disappear. They must never be kept around as a permanent third trunk; otherwise `dev` loses its role as the single integration point and every merge costs an extra hop.
- Use **on-demand `epic/<milestone>`** when a large milestone should be reviewed/accepted as one unit (multiple related features merged into it, then squash back to `dev`).
- Use **on-demand `release/vX.Y`** when publishing: cut from `dev`, fix only release-blocking bugs there, merge to `main`, tag `vX.Y` on `main`, then also merge back to `dev` and delete.
- Published versions are tracked with tags on `main` (e.g. `v0.1`).

## Lifecycle

1. `git switch -c <prefix>/<name>` (branch from `dev`)
2. Edit, then commit. This repo sets `commit.gpgsign=true` via a 1Password SSH key; if signing is unavailable in your environment, use `git -c commit.gpgsign=false commit …`.
3. `git push -u origin <prefix>/<name>`
4. Open a PR to `dev` → review / self-merge (squash) → delete the branch.
5. When the milestone is release-ready, open a PR `dev` → `main` → merge (squash).
6. Optional — independent milestone acceptance: cut `epic/<milestone>` from `dev`, merge several feature branches into it via PRs, then squash the whole epic back to `dev` and delete it.
7. Optional — publishing: cut `release/vX.Y` from `dev`, fix release-blocking bugs, merge to `main` (and back to `dev`), tag `vX.Y` on `main`, delete the branch.

See `AGENTS.md` for the agent-facing summary and `CONTRIBUTING.md` for the full human-facing workflow.
