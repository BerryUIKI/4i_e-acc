# Dispatch: Fix remaining PDF compilation errors

- **Dispatched by**: `dev-box-doc-main` (305cde212a)
- **Target agent**: `dev-box-ci-sub` (8f9b1fd0b6)
- **Permanent**: YES
- **Status**: DISPATCHED

---

## Before you start

1. Read `AGENTS.md` for hard rules.
2. Read `agents/workflows/multi-agent-collaboration.md`.
3. Branch: `article/2026-quadruple-long-life`.

---

## Problem

The CI Build Book PDF workflow still fails on xelatex compilation. The xcolor loading order has been fixed (commit `bcb53604`), but xelatex reports additional errors.

### Raw CI logs (in repo)

Read these files for full error output:

- `ci-compile-log.txt` — "Compile PDF (xelatex × 2)" step (7,567 lines). Contains all LaTeX errors, warnings, and font messages.
- `ci-gen-tex-log.txt` — "Generate LaTeX source" step. Shows pandoc output, split results.

### Context

- The generated `.tex` file uses `longtable` (from pandoc Markdown tables), `\color{...}\rule{...}` in `\titleformat` blocks, and the `≈` character in the book content.
- The template is at `skills/pdf-toolbook/assets/template/pandoc-template.tex`.
- The book has 37 chapters; compilation uses `ctexbook` + `xelatex` + `fontspec/xeCJK`.

---

## Expected output

1. Fix `skills/pdf-toolbook/assets/template/pandoc-template.tex` to resolve all three errors.
2. Update `agents/sub-agents/8f9b1fd0b6.md`: Status = DONE, list files modified.
3. Update `agents/dispatches/20260729-ci-remaining.md`: Status = DONE.

## Constraints

- English docs only under `agents/`.
- Branch `article/2026-quadruple-long-life`. Never main.
- No force-push.
- **You cannot push**. I will push after review.
- Commit format: `[{your-ShortAgentID}] fix: {description}`
