# Troubleshooting & Known Limitations

> Agent reference: known design limitations and their workarounds. Read this before debugging compilation failures.

---

## Known Limitations

### L1: Split Regex — Pandoc Version Sensitivity

**Issue:** `split_tex_into_chapters()` uses regex to detect `\hypertarget{...}{%\n\chapter{...}}`
patterns in Pandoc-generated .tex. The regex assumes Unix line endings (`\n`).
On Windows systems or with different Pandoc versions, the output may use
`\r\n` or slightly different formatting, causing the regex to miss chapter boundaries.

**Workaround:** If split fails (falls back to monolithic .tex), check the generated
.tex manually. Look for `\hypertarget` and `\chapter` patterns and verify they match
the regex:
```
(\\hypertarget\{[^}]*\}\{%\s*\n)?\s*(\\chapter\{[^}]*\})
```
For Windows-generated files, replace `\r\n` with `\n` before splitting.

### L2: Language Hardcoded to zh-CN

**Issue:** `generate_tex()` in `build_pdf.py` always passes `--metadata=lang:zh-CN` to Pandoc.
For purely English books, this means ctexbook auto-generates "第X章" chapter prefixes
alongside English titles. There is no CLI flag to override this.

**Workaround:** After generating the `.tex`, manually edit:
- Change `lang:zh-CN` to `lang:en` in the generated .tex metadata
- Or hand-edit the `.tex` to remove ctexbook chapter localization
- Recompile with `xelatex` 2-pass

### L3: `task.md` Overwrite Behavior

**Issue:** Running `build_pdf.py scan <directory>` always overwrites the workspace root
`task.md` without confirmation. If the user previously hand-edited an index file,
a subsequent scan silently overwrites it.

**Agent action required:** Before running scan, check if `task.md` exists at the
workspace root. If it does, warn the user that it will be overwritten and ask
for confirmation. Alternatively, specify a different output file:
```
python scripts/build_pdf.py scan research/ task_research.md
```

### L4: WORKSPACE_ROOT Depth Assumption

**Issue:** `WORKSPACE_ROOT` is computed as:
```python
Path(__file__).resolve().parent.parent.parent.parent.parent
```
This assumes exactly 5 parent directories from `scripts/build_pdf.py` to the workspace
root. If the skill directory is moved, symlinked, or the directory structure changes,
this path breaks silently.

**Workaround:** The agent should verify `WORKSPACE_ROOT` exists before running commands:
```python
# In build_pdf.py, WORKSPACE_ROOT validity is assumed but not checked.
# The agent should verify by checking for a known marker file:
#   AGENTS.md, README.md, or .git at the workspace root.
```

### L5: `escape_latex_special_chars()` — Retained but Unsafe

**Issue:** The `escape_latex_special_chars()` function in `build_pdf.py` is retained for
reference but has two fatal flaws:
1. Using it before Pandoc causes double-escaping and Markdown syntax corruption
2. The `known_commands` restoration list is incomplete (LaTeX has hundreds of commands)

**DO NOT USE** this function in the main pipeline. If post-Pandoc .tex patching is
needed, use targeted regex substitutions instead.

---

## Common Error Patterns

### Pandoc Fails with "Unexpected" or "Parse error"

**Likely cause:** MD syntax issue — unclosed code fences, inconsistent indentation
in nested lists, or raw HTML that Pandoc can't handle.

**Debug:** Run with `--verbose` flag (add `pandoc_args.append("--verbose")`).
Check that `preprocess_markdown()` successfully converted all HTML tags before
Pandoc sees the content.

### XeLaTeX Fails with "Font not found"

**Likely cause:** Font name mismatch on the system. Pandoc template specifies system
font names (`PingFang SC`, `STSongti-SC-Regular`, `SF Mono`) which must match
exactly.

**Debug:** On macOS, check available fonts:
```bash
fc-list :lang=zh | grep -i ping
fc-list | grep -i "sf mono"
```
If fonts are missing, adjust the template or Pandoc `-V` flags.

### XeLaTeX "Improper alphabetic constant"

**Likely cause:** XeLaTeX not being used as the engine. This error occurs when
pdflatex encounters CJK characters.

**Check:** Ensure the compilation command uses `xelatex`, not `pdflatex` or `lualatex`.
The `build_pdf.py` script always uses xelatex, but manual compilation needs
the correct engine.

### Empty TOC / "??" References

**Likely cause:** Only 1 XeLaTeX pass was run. TOC and cross-references require
at least 2 passes.

**Fix:** `build_pdf.py build` runs 2 passes automatically. For manual compilation:
```bash
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

### Split Produces Wrong Number of Chapters

**Likely cause:** The split regex failed to match some chapter patterns (see L1 above).
Fallback: the function returns the original monolithic .tex path.

**Fix:** Manually inspect the generated .tex for chapter markers, patch the regex
in `split_tex_into_chapters()`, or accept the monolithic output for small books.

---

## Quick Recovery Steps

1. **Pandoc fails** → check MD syntax (unclosed code blocks, malformed tables)
2. **XeLaTeX fails** → read `.log` file; check for "!" error markers
3. **Empty output** → re-run with `passes=3` in `run_xelatex()`
4. **Wrong fonts** → verify system fonts with `fc-list`
5. **Monolithic output (no split)** → document is small enough (<100KB, <6 chapters) or split regex failed (see L1)
6. **Files not found** → verify `WORKSPACE_ROOT` depth assumption (see L4)
