---
name: pdf-toolbook
description: >
  PDF toolbook generator. Aggregates Markdown investment documents from the workspace
  into a complete PDF book with DollarHua brand styling.
  Trigger words (EN): PDF toolbook, make a toolbook, build a PDF, compile to PDF,
  aggregate docs, export to PDF.
  Trigger words (ZH): PDF 工具书、合成工具书、生成 PDF、导出 PDF、制作工具书、
  聚合文档。
  Should trigger immediately when user says "turn directory X into a PDF toolbook".
agent_created: true
---

# PDF Toolbook Generator

Aggregate Markdown investment documents from the 4i_e-acc workspace into a complete PDF book
with full book formatting and DollarHua brand styling, powered by Pandoc + XeLaTeX.

## Quick Reference

| Action | Command |
|--------|---------|
| Scan a directory for MD files | `python scripts/build_pdf.py scan <directory>` |
| Check if xelatex + pandoc installed | `bash scripts/install_deps.sh` |
| Build PDF from index file | `python scripts/build_pdf.py build <index_file>` |
| Generate .tex only (no compile) | `python scripts/build_pdf.py tex <index_file>` |

> **Script location:** `skills/pdf-toolbook/scripts/build_pdf.py`
> **Working directory:** Always run from the workspace root

## When to Trigger

Trigger when the user wants to compile Markdown documents into a PDF toolbook:
- "turn the research/ folder into a PDF toolbook"
- "compile market/ documents into a PDF"
- "帮我做一本工具书"
- "把 research/ 的内容导出成 PDF"

## Important Constraints

- **Do NOT commit generated PDFs to the repo.** The repo is public (per AGENTS.md). PDFs are for local use only. The `output/` directory is in `.gitignore`.
- **Read `references/latex-pitfalls.md` before first compilation.** It contains critical guidance on Pandoc escaping behavior, Chinese typography, and debugging.
- **Check `references/troubleshooting.md` when compilation fails.** It documents known design limitations (split regex sensitivity, hardcoded lang, task.md overwrite) and their workarounds.

## Workflow

### Step 1 — Understand the User's Intent

Determine:
- **Source directory** — which workspace directory to scan (e.g. `research/`, `market/`)
- **Book title** — derive from directory name if not explicitly given (e.g. `research/` → "Research Reports Toolbook")
- **Cover preference** — defaults to DollarHua-branded cover

### Step 2 — Generate Index for Confirmation

Recursively scan the target directory, collect all `.md` files (excluding `README-zh_CN.md` and `_`-prefixed files), sort by directory structure, and generate an index file as `task.md`:

```markdown
# Toolbook TOC — [title]

> Scanned: `directory/` · Total: N documents

1. [Doc Title](./relative/path/to/doc1.md)
2. [Doc Title](./relative/path/to/doc2.md)
...
```

Run: `python scripts/build_pdf.py scan <directory>`

Present the index to the user. They may confirm, adjust (remove/reorder items), or cancel.

### Step 3 — Dependency Check

Check for `xelatex` and `pandoc` availability:
```bash
bash scripts/install_deps.sh
```

If dependencies are missing, ask the user to choose:
- **A)** Give me the commands, I'll install manually → show `brew install --cask basictex && brew install pandoc`
- **B)** Auto-install via `brew install` → run the install commands
- **C)** Generate `.tex` source only, I'll compile myself → use `build_pdf.py tex <index_file>` instead of `build`

### Step 4 — Document Preprocessing (mandatory, never skip)

Preprocess every source document **before** Pandoc conversion.

**Required reading:** `references/latex-pitfalls.md` — complete LaTeX pitfall guide.

**What to preprocess (and what NOT to):**

| Step | Action | Why |
|------|--------|-----|
| 1 | HTML tags → Markdown | Pandoc passes raw HTML to LaTeX → compile failure |
| 2 | Task lists → plain lists | Pandoc doesn't support `- [ ]` → LaTeX |
| 3 | Strip Unicode emoji | LaTeX cannot render emoji |

**⚠️ Do NOT manually escape LaTeX special characters!** Pandoc natively escapes `$`, `%`, `&`, `_`, `#`, `~`, `^`, `{`, `}` when converting Markdown → LaTeX. Manual escaping before Pandoc causes:
- Double-escaping: `$AAPL` → `\$AAPL` → `\\$AAPL` (renders as literal `\$AAPL`)
- Markdown syntax corruption: `# Heading` → `\# Heading` (Pandoc won't recognize headings)

The `preprocess_markdown()` function in `build_pdf.py` handles steps 1–3 automatically and correctly does NOT escape special characters.

### Step 5 — Image Path Resolution

Resolve relative image paths in Markdown to workspace absolute paths:
- **Default (Plan A)** — auto-resolve `![](assets/foo.png)` relative to the MD file's directory
- **Fallback (Plan B)** — copy all referenced images to a temp directory if Plan A fails

### Step 6 — Generate PDF

1. Read all selected MD documents
2. Apply Step 4 preprocessing pipeline
3. Handle large documents (see "File Splitting" below)
4. Convert MD → `.tex` via Pandoc with the custom LaTeX template
5. Compile `.tex` → `.pdf` with **XeLaTeX, 2-pass minimum** (see "Multi-Pass Compilation" below)
6. If compilation fails, consult `references/latex-pitfalls.md` section 9 for debugging
7. Present the PDF via `present_files`
8. **Do NOT commit the PDF** — it's for local use only

#### File Splitting Strategy

**Rule:** If the merged Markdown exceeds **100KB** or spans **more than 5 chapters**, split into a multi-file LaTeX project instead of a monolithic `.tex` file.

- Generate a `main.tex` with preamble, cover, TOC → `\input{chapter_01.tex}`, `\input{chapter_02.tex}`, ...
- Each chapter gets its own `.tex` file containing only the body content for that section
- Benefits: faster compile, partial recompile support, smaller individual files, easier debugging

The `build_pdf.py` script handles this automatically via `should_split()` and `split_tex_into_chapters()`.

#### Multi-Pass Compilation (CRITICAL)

XeLaTeX **must be run at least twice** to produce correct output:

| Pass | What it does |
|------|-------------|
| **Pass 1** | Generates `.aux` and `.toc` files (cross-reference data, TOC entries) |
| **Pass 2** | Reads `.aux`/`.toc` → resolves all cross-references, TOC page numbers, forward refs |
| **Pass 3** (optional) | Only needed if Pass 2 still reports unresolved references (rare) |

**DO NOT** run XeLaTeX only once — the TOC will be empty and all cross-references will show `??`.

Script command: `python scripts/build_pdf.py build <index_file>`

## Brand Guidelines

All visuals must follow the DollarHua color system (see `references/dollarhua-brand.md` for full reference):

| Color | Hex | PDF Usage |
|-------|-----|-----------|
| Signature Pink | `#FEC6CD` | Chapter title decor lines, page numbers |
| Bond Navy | `#1D1E50` | Body text, heading text |
| Amber Gold | `#E3A04B` | Decorative accents, emphasis lines |
| Soft White | `#FCFDFD` | Page background |

Source of truth: `assets/dollarhua/color_standard.json` in the workspace.

## Bundled Resources

### scripts/
- `build_pdf.py` — Main entry: scan directories, preprocess MD, compile PDF (with 2-pass XeLaTeX and auto file-splitting)
- `install_deps.sh` — Dependency checker and install guide

### references/
- `dollarhua-brand.md` — DollarHua 8-color palette, typography specs, LaTeX color definitions
- `latex-pitfalls.md` — **Agent-required reading**: Pandoc escaping behavior, Chinese typography, Pandoc quirks, image handling, multi-pass compilation, file splitting, debug flow
- `troubleshooting.md` — **Known limitations and workarounds**: split regex fragility, lang hardcoded, task.md overwrite, WORKSPACE_ROOT depth, escape function warnings

### assets/template/
- `pandoc-template.tex` — Custom Pandoc LaTeX template (cover, TOC, headers/footers, chapter styling, code highlighting, tables, callout boxes)
