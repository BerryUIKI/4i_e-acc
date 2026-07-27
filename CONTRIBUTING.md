# Contributing

This repository uses a **pull-request-based** workflow. The default branch is `main`.

> ⚠️ **Enforcement caveat.** `BerryUIKI/4i_e-acc` is currently a **private repository on a GitHub Free plan**. GitHub does not allow branch-protection rules (required reviews, "no direct push", etc.) on free private repos, so the rules below are a **convention, not a hard block** — direct pushes to `main` are still technically possible. Should the repo be upgraded to GitHub Pro or made public, the maintainer can switch on true branch protection (see *Future: enforced protection* below).

## Workflow

1. **Never commit directly to `main`.** Always start from a working branch.
2. **Branch naming** (English, lowercase, hyphenated):
   - `docs/<short-topic>` — documentation changes (e.g. `docs/bilingual-readme`)
   - `article/<slug>` — a new essay under `articles/` (e.g. `article/quadruple-long-life`)
   - `fix/<short-topic>` — fixes
   - `feat/<short-topic>` — new content or sections
3. **Commit** with clear messages. Conventional Commits are recommended, e.g. `docs: add contributing guide`.
4. **Push** the branch: `git push -u origin <branch>`.
5. **Open a Pull Request** targeting `main`. CODEOWNERS auto-requests review from `@BerryUIKI`.
6. **Review & merge.** Prefer squash-merge for a clean linear history. Delete the branch after merge.

## Articles

Essays live under `articles/` and follow `articles/STYLE.md` (Chinese-primary with English inline) plus the per-essay scaffold in `articles/_template/`.

## Future: enforced protection

If the repo becomes public or GitHub Pro is enabled, apply the following branch-protection rule on `main`:

- Require a pull request before merging
- Require at least **1** approving review
- `enforce_admins: true` (even the owner cannot bypass)
- Block force pushes and block branch deletions

A ready-to-run API payload for this is kept in the maintainer's notes.
