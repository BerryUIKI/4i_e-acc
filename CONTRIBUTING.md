# Contributing

This repository uses a **pull-request-based** workflow. The default branch is `main`. The repository is **public**, and `main` is branch-protected.

> **Branch protection — pragmatic mode.** Every change to `main` must arrive via a Pull Request. For collaborators (non-admins) at least **1** approving review is required. `enforce_admins` is **off**, so the repository owner may open a PR and **self-merge** it. Direct `git push` to `main` is therefore technically possible for the owner but is discouraged — please always go through a PR. Force pushes and branch deletions on `main` are blocked for everyone.

## Workflow

1. **Never commit directly to `main`.** Always start from a working branch.
2. **Branch naming** (English, lowercase, hyphenated): see [`BRANCHING.md`](./BRANCHING.md) for the full prefix table. Short form:
   - `docs/<short-topic>` — documentation changes (e.g. `docs/bilingual-readme`)
   - `article/<yyyy-slug>` — a new essay under `articles/` (e.g. `article/2026-quadruple-long-life`)
   - `fix/<short-topic>` — fixes
   - `ci/<short-topic>` — CI / tooling
   - `feat/<short-topic>` — new content or sections
   - `chore/<short-topic>` — repo maintenance
3. **Commit** with clear messages. Conventional Commits are recommended, e.g. `docs: add contributing guide`.
4. **Push** the branch: `git push -u origin <branch>`.
5. **Open a Pull Request** targeting `main`. CODEOWNERS auto-requests review from `@BerryUIKI`.
6. **Review & merge.** Prefer squash-merge for a clean linear history. Delete the branch after merge.

## Articles

Essays live under `articles/` and follow `articles/STYLE.md` (Chinese-primary with English inline) plus the per-essay scaffold in `articles/_template/`.

## Notes

- To enable stricter enforcement later (owner also blocked from self-merge), turn `enforce_admins` on — but then a second GitHub account is needed to approve the owner's own PRs.
- CI runs GitHub Actions on every PR that touches `.md` files and on a weekly schedule (see `.github/workflows/docs-checks.yml`).
