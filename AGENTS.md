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

## Multi-Agent Collaboration

This repo is maintained by multiple AI agents across different sessions and devices. Human user "花花" bridges agents by passing handoff documents.

### Agent identity
- Each agent MUST self-identify at the start of every session (name, role, session date).
- Primary agent on this project: **小花蟹 (Little Flower Crab)** — research assistant, data + charts + CI.
- Sub-agents may be spawned for illustration generation, proofreading, or other scoped tasks.

### Communication protocol
1. **Primary agent writes a handoff `.md`** file at the repo root: `HANDOFF-YYYY-MM-DD.md`.
2. Agent tells the user: "花，帮我开个子 Agent，Prompt 如下："
3. Agent provides the prompt (task description, context, inputs, expected outputs) in a **code block**.
4. User opens a sub-agent session, pastes the prompt, and returns results.
5. Primary agent integrates results and pushes to the branch.

### Handoff document schema (mandatory fields)
Every `HANDOFF-YYYY-MM-DD.md` MUST include:

```markdown
# Handoff — YYYY-MM-DD

## Session identity
- **Agent:** <name>
- **Session date:** YYYY-MM-DD
- **Repo:** https://github.com/BerryUIKI/4i_e-acc
- **Branch:** <branch-name>
- **PR:** <#N or N/A>

## Agency trigger / purpose
<!-- Why this handoff was written. What happened in this session. -->

## Completed work
<!-- Concrete list of changes made: files, commits, decisions. -->

## Remaining tasks (priority-ordered)
- [ ] P0: ...
- [ ] P1: ...
- [ ] P2: ...

## Key decisions & rationale
<!-- Why we chose X over Y. Design trade-offs made. -->

## Gotchas & known issues
<!-- Bugs left unfixed, fragile areas, things to watch. -->

## Handoff to sub-agent (if applicable)
<!-- Self-contained: prompt, input paths, output paths, reference files. -->
<!-- NEVER reference files the sub-agent cannot access. Embed or link with full URL. -->
```

### Git safety for multi-agent workflows
- **NEVER force-push (`git push --force`, `--force-with-lease`)** on any shared branch. Force-push silently erases other agents' commits — we lost analysis scripts and chapter content this way on 2026-07-28.
- **Use GitHub REST API** if local git is in a broken sandbox state (common on this project). Steps:
  1. GET `https://api.github.com/repos/BerryUIKI/4i_e-acc/contents/<path>?ref=<branch>` for SHA.
  2. Base64-encode the local file.
  3. PUT with `{message, content, sha, branch}`.
- **Never commit tokens or secrets.** PAT lives in `~/.workbuddy/MEMORY.md` (outside the repo tree).
- **Never commit `_push.py`** or other scripts that embed tokens.

### Data provenance rule
Every data file, chart, or table committed to this repo MUST document its source:
- **Python scripts**: docstring with data source name, acquisition URL, and update method (see `articles/2026-quadruple-long-life/analysis/src/` for examples).
- **Markdown tables**: inline footnote with source and retrieval date.
- **External data (CSV/JSON)**: companion `.md` or `.txt` with provenance info.
- **Mathematical simulations**: label clearly as "Pure mathematical model" and document all parameters.

### File naming conventions
- **Repo paths**: ASCII only, no spaces, no Chinese characters. Use hyphens (`kebab-case`).
- **Output PDFs**: English slug (e.g., `quadruple-cognition-long-life.pdf`).
- **Illustrations**: `NN-descriptive-name.png` (e.g., `00-cover.png`, `07-asset-tree.png`).
- **Analysis scripts**: `chNN_topic.py` matching the chapter they serve.

### Sub-agent prompt template
When delegating to a sub-agent, provide a self-contained code block:

````markdown
花，帮我开个子 Agent，Prompt 如下：

```
Task: <one-line summary>

Context:
- Repo: https://github.com/BerryUIKI/4i_e-acc
- Branch: article/2026-quadruple-long-life
- Reference files: <list exact paths or inline content>

Inputs:
- <file 1 with full path or embedded content>
- <file 2 ...>

Expected outputs:
- <output file 1>: <description>
- <output file 2>: <description>

Constraints:
- <any rules or style guidelines>
```
````

**Critical**: never reference files by relative path alone if the sub-agent cannot access the repo. Either embed the content or provide full GitHub raw URLs.

### Workspace handoff checklist (before ending a session)
- [ ] All work pushed to remote (check `git log --oneline -5` or verify on GitHub).
- [ ] `HANDOFF-YYYY-MM-DD.md` written and up to date.
- [ ] Temporary scripts cleaned up (`_push.py`, `/tmp/*`, debug files).
- [ ] Daily memory log updated: `articles/2026-quadruple-long-life/.workbuddy/memory/YYYY-MM-DD.md`.
- [ ] No tokens, keys, or secrets in committed files.

## Gotchas
- Repo is **public** — never commit secrets (keys/tokens stay in `~/.ssh`, outside the repo).
- Top-level doc folders are one level deep: link the root with `../README.md`, **not** `../../`.
- **Never force-push.** See Multi-Agent Collaboration section above.
