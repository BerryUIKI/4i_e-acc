# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`4i_e-acc` is a **content-first** repo, not an application. It publishes one deliverable — the Chinese book 《四倍做多认知，长期做多人生》 (*Quadruple Leverage on Cognition, Long Life*) — through four coupled surfaces that all read the same sources:

| Surface | Source of truth | Ships as |
|---|---|---|
| Book manuscript | `articles/2026-quadruple-long-life/` (Markdown) | Pandoc + XeLaTeX PDF → GitHub Releases |
| Web toolbox | `tools/<slug>/index.html` (self-contained, no CDN) | GitHub Pages via `gh-pages` branch |
| Desktop app | `desktop/` (Tauri 2 + Rust) | Reuses `tools/` as `frontendDist` |
| Landing page | `index.html` at repo root | GitHub Pages |

Everything else (`reports/`, `research/`, `portfolio/`, `market/`, `strategies/`, `data/`, `archive/`) is a bilingual doc folder following the same README contract.

## Authoritative rules — read before editing

- [`AGENTS.md`](AGENTS.md) — hard rules (no direct push to `main`/`dev`, no force-push, ASCII kebab-case paths, data provenance, commit traceability). These override anything here.
- [`BRANCHING.md`](BRANCHING.md) — two permanent trunks (`main`, `dev`); `epic/` and `release/` only on demand.
- [`articles/STYLE.md`](articles/STYLE.md) — short-essay style. Book projects are explicitly **excluded** from it.
- [`articles/2026-quadruple-long-life/agents.md`](articles/2026-quadruple-long-life/agents.md) — book-scoped conventions (structure, voice, illustration specs). Its PR-frequency rule ("accumulate commits, open one PR when the whole book is release-ready") narrows the root workflow for book edits; it does not override hard rules.
- [`skills/pdf-toolbook/references/latex-pitfalls.md`](skills/pdf-toolbook/references/latex-pitfalls.md) — required reading before touching the PDF pipeline.

## Commands

Run all verification from the repo root.

```bash
python .github/scripts/check_links.py && python .github/scripts/check_style.py
```

```bash
python scripts/verify_pages.py
```

**Windows gotcha:** both check scripts print emoji and crash with `UnicodeEncodeError` under the default cp1252 console. Prefix with `PYTHONIOENCODING=utf-8` locally (CI on Linux is unaffected).

### PDF build

```bash
python skills/pdf-toolbook/scripts/build_pdf.py tex book-task.md output/toolbook.tex
```

```bash
python skills/pdf-toolbook/scripts/build_pdf.py build book-task.md output/toolbook.pdf "四倍做多认知，长期做多人生" "花花 | @BerryUIKI"
```

- `build` = merge MD → `.tex` → XeLaTeX (2-pass, 3-pass if references remain). `tex` = source only, no compile.
- `book-task.md` at the repo root is the **single source of truth for chapter order**. `parse_index()` only accepts numbered lines of the form `N.` followed by a markdown link to a `.md` path relative to the working directory — reformat it and the build silently drops entries.
- Paths inside `book-task.md` resolve against the **current working directory**, so always run from the repo root.
- Never commit generated PDFs.

### Charts

```bash
cd articles/2026-quadruple-long-life/analysis/src && python ch07_drawdowns.py
```

Requires `matplotlib pandas numpy`; `_style.py` handles CJK font discovery and the shared palette. Output lands in `../output/`, which is exactly where the chapter image references under `Main-Text/` point.

### Desktop

```bash
cd desktop && pnpm install && pnpm tauri dev
```

Requires **Node.js 24 LTS or newer** (`.nvmrc`/`.node-version` pin it, `engines` enforces it) and **Rust 1.77+**.

## Architecture: the couplings that matter

**`tools/` is a dual-target frontend.** Tauri's `frontendDist` is literally `../../tools` — there is no build step and no copy. Editing a tool changes both the web toolbox and the desktop app. Anything that only works in a browser (`window.__TAURI__` absent, `localStorage`) is the normal path; the desktop branch is the exception.

**Every tool page is a contract.** Each `tools/<slug>/index.html` is a single file carrying its own CSS and JS and must keep these markers, which `scripts/verify_pages.py` asserts:

- `<!DOCTYPE html>`, `<link rel="icon" …>` pointing at `../../assets/favicon.svg`
- `export-fab-btn` — the floating export button; downloads a `.txt` in browsers, calls `invoke("export_result")` in Tauri
- `ql-toolbox:` — localStorage key prefix, namespaced per path by the shared persistence script
- `tool-select` — the cross-tool `<select>` switcher; a new tool must also be added to that options list **in every other tool**

A new tool additionally needs an entry in the `TOOLS` array in `tools/index.html` (id, group A/B, number, source chapter, zh/en copy). The Rust side only needs touching for new native commands: `app_info` and `export_result` in [`desktop/src-tauri/src/lib.rs`](desktop/src-tauri/src/lib.rs), registered in `invoke_handler`.

**Book structure is load-bearing for the PDF.** `build_pdf.py` relies on:

- Chapter files named `XNNN-slug.md` where the prefix letter maps to a book part (A–I per the table in the book's `agents.md`); front matter is `FM00N-*`, the epilogue `H001-*`.
- Chapters as `##` headings; sections as `###`. Part banners are **bold labels after a `---` rule**, not headings — `merge_markdown()` converts `**第N部分 · …**` into a `\partdivider` raw-LaTeX block.
- Content before the first `第X章` entry goes into `\frontmatter`; an appendix entry switches to `\backmatter`; any entry titled `目录` is dropped because the LaTeX template emits `\tableofcontents` itself.

## CI and what triggers what

| Workflow | Trigger | Effect |
|---|---|---|
| `docs-checks.yml` | PR/push touching `*.md`, weekly cron | link check, style check, markdownlint (`continue-on-error`) |
| `pr-language-check.yml` | every PR | title must be ≤40% non-English, body ≤50% |
| `deploy-pages.yml` | push to `dev` touching `index.html`, `tools/**`, `assets/**`, `.nojekyll` | stages those four paths to `gh-pages` |
| `build-book-pdf.yml` | PR/push touching book Markdown or `skills/pdf-toolbook/**` | 3-pass XeLaTeX; on `main`, **auto-creates a `v0.x` GitHub Release** |

Two consequences worth remembering: merging book content to `main` publishes a release (the version number is "next unused v0.N", not derived from anything in the repo), and the PDF workflow fails if the generated `.tex` holds fewer than 10,000 CJK characters or the PDF lacks an embedded `SourceHan` font.

## Editing conventions that are easy to get wrong

- **Commit messages must start with `[ShortAgentID]`** (currently `[f78f1d3e]` for the active Main agent — verify against `agents/0101aaa313a11c56/f78f1d3e/roster.md`). Git identity is repo-local: `"[id]"` / `"id@agents.local"`. Signing may be unavailable → `git -c commit.gpgsign=false commit …`.
- **Language split is deliberate:** everything in `AGENTS.md`/`agents/` and all commit/PR text is English; the book body is Chinese-primary with English terms inline on first use (`复利 (compounding)`); doc folders need both `README.md` and `README-zh_CN.md` (enforced by `check_style.py`).
- **Do not escape LaTeX special characters before Pandoc.** It auto-escapes `$ % & _ # ~ ^ { }`. Manual escaping corrupts headings and double-escapes tickers. Only HTML tags, task lists, and emoji need preprocessing — `preprocess_markdown()` already does all three.
- **Data provenance is mandatory** for every chart, table, or dataset: a docstring/companion `.md` naming the source, the acquisition URL, and how to refresh. `analysis/src/*.py` is the reference implementation.
- **File naming:** ASCII, lowercase, kebab-case. Analysis scripts are `chNN_topic.py`, illustrations `NN-slug.png`, chapters `XNNN-slug.md`.
- **LFS:** `*.png *.jpg *.jpeg *.csv *.pdf` go through Git LFS, except chart PNGs and desktop icons which `.gitattributes` deliberately exempts so CI (which does not pull LFS) can embed them in XeLaTeX.
- **`output/` is gitignored** for new files; a handful of chart PNGs and `output/toolbook.tex` remain tracked from earlier builds. Do not add new artifacts under it. `skills/pdf-toolbook/assets/fonts/` is likewise ignored — `build_pdf.py` downloads ~495 MB of Source Han OTF there when no system font is found.

## Where to look first

- Book overview and part/chapter map: `articles/2026-quadruple-long-life/README.md`
- Tool inventory with source chapters: `TOOLBOX-ROADMAP.md` and `tools/index.html`
- PDF pipeline contract: `skills/pdf-toolbook/SKILL.md` + `references/troubleshooting.md` (known limitations: fragile split regex, hardcoded `lang:zh-CN`, `scan` overwriting `task.md`)
- Brand palette (pink `#FEC6CD`, navy `#1D1E50`, bronze `#B86C40`, cream `#FBF7F0`): `assets/dollarhua/color_standard.json`
