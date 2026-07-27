# LaTeX Pitfall Guide

> Agent-required reading. Investment Markdown documents contain LaTeX-sensitive characters — read this before compiling anything.
> Ordered by frequency: the top items are the most common causes of build failure.

---

## 1. Special Character Handling (Critical Understanding)

Investment docs are full of `$` (tickers), `%` (ratios), `_` (variable names), `&` (AT&T).
These are all LaTeX special characters — but **Pandoc handles them automatically**.

### ⚠️ Golden Rule: Do NOT Manually Escape Before Pandoc

Pandoc **natively auto-escapes** all LaTeX special characters when converting Markdown → LaTeX.
If you manually escape them beforehand, you cause **double-escaping** and **Markdown syntax corruption**:

| What you do | Input | After manual escape | After Pandoc | PDF output | Problem |
|-------------|-------|---------------------|-------------|------------|---------|
| ❌ Escape `#` before Pandoc | `# Heading` | `\# Heading` | `\textbackslash{}\# Heading` | `# Heading` as body text | Heading structure lost |
| ❌ Escape `_` before Pandoc | `_italic_` | `\_italic\_` | `\textbackslash{}\_italic\textbackslash{}\_` | `_italic_` literal | Emphasis lost |
| ❌ Escape `$` before Pandoc | `$AAPL` | `\$AAPL` | `\\$AAPL` | `\$AAPL` literal | Double-escaped |
| ✅ Let Pandoc handle it | `$AAPL` | `$AAPL` | `\$AAPL` | `$AAPL` | Correct! |

### What Pandoc DOES Handle (No Action Needed)

| Char | LaTeX Meaning | Investment Examples | Pandoc Auto-Escapes? |
|------|-------------|---------------------|---------------------|
| `$` | Math mode | `$AAPL`, `$500M` | ✅ Yes |
| `%` | Comment | `ROE 15%`, `30%` | ✅ Yes |
| `&` | Alignment tab | `AT&T`, `S&P 500` | ✅ Yes |
| `_` | Subscript | `fund_name` | ✅ Yes |
| `#` | Macro param | `#1 stock` | ✅ Yes |
| `~` | Non-breaking space | `~3 years` | ✅ Yes |
| `^` | Superscript | `E=MC^2` | ✅ Yes |
| `{` `}` | Grouping | JSON braces | ✅ Yes |
| `\` | Command prefix | Windows paths | ✅ Yes |

### What Pandoc Does NOT Handle (Preprocessing Required)

These are the ONLY things that need manual preprocessing:

| Issue | Example | Fix |
|-------|---------|-----|
| HTML tags | `<img src="...">`, `<div>` | Convert to Markdown / strip (Pandoc passes HTML through to LaTeX) |
| Task lists | `- [ ]`, `- [x]` | Convert to plain `- ` (Pandoc doesn't support task list → LaTeX) |
| Emoji | `🎉` `📊` `✅` | Strip (LaTeX cannot render Unicode emoji) |

### When Manual Escaping IS Needed (Post-Pandoc Only)

In rare edge cases, you may need to patch the generated `.tex` file **after** Pandoc:
- Raw HTML embedded in Markdown that Pandoc passed through
- Table cells with special characters in certain Pandoc versions
- `\` characters in code that `lstlisting` doesn't handle

In these cases, use `escape_latex_special_chars()` in `build_pdf.py` as a **post-Pandoc** patching tool, never as a pre-Pandoc preprocessing step.

---

## 2. Chinese Typography Issues

### 2.1 Missing Font → Compile Failure

**Most common error**: `! LaTeX Error: File 'xxx.sty' not found`

**Cause**: XeLaTeX cannot find the CJK font.

**Fix:**

1. Ensure `pandoc-template.tex` uses `\usepackage{xeCJK}` (NOT the old `CJK` package)
2. Font names must match macOS system fonts **exactly**:

```tex
\setCJKmainfont{PingFang SC}         % System default ✅
\setCJKsansfont{PingFang SC}
\setCJKmonofont{STSongti-SC-Regular} % Songti ✅
```

3. **ALWAYS compile with `xelatex`, never `pdflatex` or `lualatex`!**

### 2.2 CJK Line Breaking

XeLaTeX + xeCJK handles Chinese line breaks automatically. If issues occur:
- Verify `\XeTeXlinebreaklocale "zh"` is set
- Ensure you're using `xeCJK`, not the legacy `CJK` package

### 2.3 Mixed CJK/Latin Spacing

xeCJK automatically inserts `\CJKecglue` between Chinese and Latin text. No extra handling needed.

---

## 3. Pandoc Conversion Traps

### 3.1 Nested Lists

```markdown
- Level 1
  - Level 2
```

Pandoc may misinterpret indentation as code blocks. **Fix**: use consistent 2-space or 4-space indentation, never mix with tabs.

### 3.2 Table Special Characters

Investment table example:

```
| Metric     | Q1   | Q2   |
|------------|------|------|
| Gross Margin | 45%  | 48%  |
| ROE        | 12.5%| 11.8%|
```

Pandoc auto-escapes `%`, `$`, `&`, `_`, `#` in table cells, same as body text.
If you encounter issues with table escaping in a specific Pandoc version, use
`pandoc --version` to check and consider upgrading.

### 3.3 Task Lists

```
- [x] Done
- [ ] Pending
```

Pandoc doesn't support task list → LaTeX by default. **Fix**: convert to plain lists before processing.

### 3.4 HTML Tags

Embedded `<div>`, `<span>`, `<img>` tags are **passed through verbatim to LaTeX** by Pandoc — causing compile failure.

**Fix** (before Pandoc):
- `<img src="...">` → convert to Markdown `![]()` syntax
- `<div>` / `<span>` → strip tags, keep inner text
- `<br>` → keep (Pandoc handles it)

### 3.5 Emoji

`🎉` `📊` `✅` etc. cannot be rendered by LaTeX.

**Solution**: strip all Unicode emoji before compilation.
```python
re.sub(r'[\U0001F300-\U0001FFFF]', '', text)
```

---

## 4. Image Issues

### 4.1 Format Support Matrix

| Format | XeLaTeX | Notes |
|--------|---------|-------|
| PNG | ✅ | Recommended |
| JPG/JPEG | ✅ | Recommended |
| PDF | ✅ | Best for vector |
| SVG | ❌ | Convert to PDF/PNG via `rsvg-convert` |
| WebP | ❌ | Convert to PNG/JPG |
| GIF | ❌ | Only first frame, not recommended |

### 4.2 Special Characters in Image Paths

Paths with spaces or CJK characters → XeLaTeX `\includegraphics` may fail.

**Fix**: copy images to a temp directory with sanitized paths before compilation.

### 4.3 Oversized Images

Large images cause `dimension too large` error.

**Fix**: add size limits in template: `\includegraphics[width=\textwidth,height=0.8\textheight,keepaspectratio]`

---

## 5. Multi-Pass Compilation (CRITICAL)

### Why 2 Passes Are Required

XeLaTeX **must run at least twice** for correct output. A single pass produces:

| Issue | Cause | Fixed by |
|-------|-------|---------|
| Empty TOC | `.toc` file generated on pass 1, read on pass 2 | Pass 2 |
| `??` for cross-references | `.aux` file generated on pass 1, read on pass 2 | Pass 2 |
| Wrong page numbers in TOC | Page numbers shift after content is typeset | Pass 2 |
| "Rerun to get cross-references right" | LaTeX explicitly warns about this | Pass 2 (or 3) |

### Compilation Flow

```
1. xelatex main.tex     → generates main.aux, main.toc (reference data)
                           TOC appears empty, references show ??
2. xelatex main.tex     → reads .aux/.toc, resolves everything
                           Final correct output
3. xelatex main.tex     → (only if "Rerun" warning still appears)
```

### Implementation in build_pdf.py

The `build` command runs 2 passes automatically via `run_xelatex(tex_path, work_dir, passes=2)`.
It checks for "Rerun" warnings and reports them.

**DO NOT skip passes** — the TOC will be empty and all cross-references will show `??`.

---

## 6. File Splitting Strategy

### When to Split

A single monolithic `.tex` file for a book-length document causes:
- Extremely slow compiles (every minor change recompiles everything)
- Hard-to-diagnose errors (where did this come from?)
- Files too large for some editors

**Thresholds** (in `build_pdf.py`):
- Merged MD > **100KB** → split
- More than **5 chapters** → split
- Both checked; first match triggers split

### Split Architecture

```
output/tex/
├── main.tex          # Preamble + cover + TOC + \input{chapter_01} + \end{document}
├── chapter_01.tex    # Body content for chapter 1
├── chapter_02.tex    # Body content for chapter 2
└── chapter_03.tex    # ...
```

- `main.tex` contains the full preamble, cover, TOC, and `\input{chapter_XX}` for each chapter
- Each `chapter_XX.tex` is a self-contained chapter body (no preamble)
- `xelatex main.tex` resolves all cross-references across chapters
- For partial rebuilds: use `\includeonly{chapter_03}` in main.tex to compile only that chapter (page numbers and cross-refs stay correct from previous runs)

### How the Script Handles It

1. `compile_pdf()` generates `.tex` via Pandoc
2. `should_split()` checks size and chapter count
3. `split_tex_into_chapters()` parses the monolithic `.tex`, extracts preamble + chapters, writes structured output
4. Returns path to `main.tex` for compilation

---

## 7. Compile Command Reference

### Correct Pandoc Command (generating .tex)

```bash
pandoc merged.md \
  -o output.tex \
  --template=assets/template/pandoc-template.tex \
  --metadata=title:"Toolbook Title" \
  --metadata=author:"Author Name" \
  -V CJKmainfont="PingFang SC" \
  -V mainfont="PingFang SC" \
  --toc --toc-depth=2 \
  --listings \
  --standalone
```

### Correct XeLaTeX Command (2 passes)

```bash
# Pass 1
xelatex -interaction=nonstopmode -output-directory=build main.tex
# Pass 2
xelatex -interaction=nonstopmode -output-directory=build main.tex
```

### Common Error Quick-Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `! LaTeX Error: File 'ctex.sty' not found` | ctex not installed | `sudo tlmgr install ctex` |
| `! Undefined control sequence \CJK...` | Using old CJK package | Switch to `xeCJK` |
| `! Improper alphabetic constant` | CJK not recognized | Verify xelatex engine |
| `! Missing $ inserted` | Unescaped `$` in body | Preprocess: `$` → `\$` |
| `! Misplaced alignment tab character &` | Unescaped `&` in body | Preprocess: `&` → `\&` |
| `! Dimension too large` | Oversized image | Add size limits to `\includegraphics` |
| `! Unknown graphics extension` | Unsupported image format (SVG/WebP) | Convert to PNG/PDF |
| Empty TOC | Only 1 XeLaTeX pass | Run pass 2 |

---

## 8. Preprocessing Checklist (Before Every Compile)

Apply to **each source document** before merging:

1. **[HTML tags]** `<img>` → `![]()`, strip `<div>/<span>` (Pandoc passes HTML through to LaTeX)
2. **[Emoji]** Strip all Unicode emoji (LaTeX cannot render them)
3. **[Task lists]** `- [ ]` → `- `, `- [x]` → `- ` (Pandoc doesn't support task list → LaTeX)
4. **[Image formats]** Check references — convert SVG/WebP/GIF to PNG
5. **[Image paths]** Ensure no spaces or CJK special chars in paths

**Do NOT manually escape LaTeX special characters** — Pandoc handles `$`, `%`, `&`, `_`, `#`, `~`, `^`, `{`, `}`, `\` automatically. Manual escaping before Pandoc causes double-escaping and Markdown syntax corruption (see Section 1).

The `preprocess_markdown()` function in `build_pdf.py` handles steps 1–3 automatically.

---

## 9. Quick Debug Flow

When compilation fails, diagnose in this order:

```
1. Pandoc error or LaTeX error?
   ├─ Pandoc → check MD syntax (nested indents, HTML tags not stripped)
   └─ LaTeX → continue ↓

2. Double-escaping? (most common if you manually escaped)
   ├─ Literal \$ or \% in output → you escaped BEFORE Pandoc (don't!)
   ├─ Headings missing → you escaped # before Pandoc (don't!)
   └─ Emphasis missing → you escaped _ before Pandoc (don't!)
   Fix: remove manual escaping, let Pandoc handle it (see Section 1)

3. CJK/font issue?
   ├─ ctex.sty not found → install ctex
   ├─ Font not found → verify font name spelling
   └─ Improper alphabetic constant → confirm xelatex (not pdflatex)

4. Image issue?
   ├─ File not found → check image path resolution
   ├─ Unknown graphics extension → unsupported format (SVG/WebP)
   └─ Dimension too large → oversized image

5. Empty TOC / ?? references?
   └─ Only ran 1 XeLaTeX pass → run pass 2!

6. Still failing?
   Run `build_pdf.py tex` to generate .tex source only,
   then debug by commenting out sections.
   Check the .log file for detailed error context.
```
