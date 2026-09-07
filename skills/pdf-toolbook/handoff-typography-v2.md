# Handoff — 4i Toolbook Typesetting (v2) for External Agents

> Written for other Agents that continue typesetting work on this book.
> Source of truth for the v2 typography rebuild. Part of PR #57 (`fix/pdf-toolbook-typography-v2` → `dev`).

## The book

- **Title**: 《四倍做多认知，长期做多人生》
- **Source**: 40+ Markdown docs under `articles/2026-quadruple-long-life/`
  - `Front-Matter/` — 开篇/序言（FM00x）
  - `Main-Text/` — 33 章正文（A00x / B00x 编号）
  - `Appendices/` — 附录
- **Order manifest**: `book-task.md` (repo root) — single source of truth for chapter sequence.
- **Deliverable**: `output/toolbook-v2.pdf` (192 pages / 2.18 MB as of 2026-09-07).

## Build pipeline

```
book-task.md (index)
  → skills/pdf-toolbook/scripts/build_pdf.py merge
      · strip YAML frontmatter (with key:value guard — see pitfalls)
      · strip source's own first h1/h2 (script prepends # {title})
      · preprocess markdown
      · convert "**第N部分 · 标题**" banners → \partdivider raw-LateX block
      · rewrite image paths (strip ../analysis/output/ prefix)
      · \frontmatter / \mainmatter / \backmatter switches
  → pandoc --top-level-division=chapter --template=pandoc-template.tex
  → 2× xelatex (run in output/tex/, graphicspath resolves ./)
  → output/toolbook-v2.pdf
```

### Rebuild command (run from repo root)

```bash
python skills/pdf-toolbook/scripts/build_pdf.py build book-task.md output/toolbook-v2.pdf "四倍做多认知，长期做多人生" "花花 | @BerryUIKI" "2026-09-07"
```

Sub-command `tex` generates `.tex` only (fast validation, no PDF):

```bash
python skills/pdf-toolbook/scripts/build_pdf.py tex book-task.md output/toolbook-v2.tex "四倍做多认知，长期做多人生" "花花 | @BerryUIKI" "2026-09-07"
```

TeX Live 2025 (`xelatex`) is available on this machine.

## Files that changed in v2

| File | What |
|------|------|
| `skills/pdf-toolbook/assets/template/pandoc-template.tex` | v2.0 template: literal `titlepage` cover, `\titleformat[display]` chapter bands, `\partdivider`, tocloft-colored TOC, epigraph styling, fancyhdr header/footer, CJK spacing |
| `skills/pdf-toolbook/scripts/build_pdf.py` | preprocessing chain: YAML guard, chapter-heading strip, part-divider conversion, image path rewrite, front/main/back matter switches, `--top-level-division=chapter` |

## What was broken in v1 (99-page build) and fixed

1. **Chapters emitted as `\section`** — source MDs use `## 第N章`; pandoc needed `--top-level-division=chapter` to emit `\chapter`, so all chapter decorations never fired.
2. **Chapter openings swallowed** — `strip_yaml_frontmatter` treated `--- 题词 ---` thematic breaks as YAML metadata and silently discarded the epigraph + chapter title. Fix: only treat `---` blocks as YAML if they contain a `key: value` line.
3. **Duplicated chapter titles** ("第N章 第N章 · …") — source MD's own first heading collided with script-prepended `# {title}`. Fix: `strip_chapter_heading` scans for the first h1/h2 anywhere in the file.
4. **Subsection numbering `1.0.x`** — redefined `\thesubsection` as `\thechapter.\arabic{subsection}`.
5. **Cover fell back to bare `\maketitle`** — ctex ignores redefined `\@maketitle`; moved to a literal `titlepage` environment in the template body.
6. **Broken chart paths** — `../analysis/output/...` failed when xelatex ran from `output/tex/`. `rewrite_image_paths` strips directory prefixes; images resolve via `\graphicspath{{./}{./assets/}}`.
7. **Manual TOC (FM003) duplicated** — template emits `\tableofcontents`; FM003 is skipped in merge. Numbering switches: front matter roman (i, ii, …), main matter arabic (1–33+), back matter unnumbered.

## Known pitfalls (learned the hard way)

- `\titleformat[display]` label slot rejects `\par`/`\vspace`; use `\vskip`/`\hrule`/`\titlerule` instead.
- `strip_yaml_frontmatter` must NOT strip plain thematic breaks (`---` without key:value inside).
- Image paths baked as `../...` into `.tex` break at compile time; strip to bare filenames and rely on `\graphicspath`.
- Rebuild output lands in `output/`; PDFs are `.gitignore`d and never committed.
- Never touch `main` / `dev` directly — branch + PR, squash-merge.

## Where to tweak for further typesetting work

| Goal | Edit |
|------|------|
| Chapter spacing / bands / colors | `\titleformat{\chapter}` block in `pandoc-template.tex` (titlesec) |
| TOC styling | `\tocloft` block in `pandoc-template.tex` |
| Header/footer | `fancyhdr` block in `pandoc-template.tex` |
| Bulk body-text preprocessing | `preprocess_markdown` / merge steps in `build_pdf.py` |
| Part divider pages | `\partdivider` macro in `pandoc-template.tex` |

## Visual verification checklist (spot pages in the 192-page build)

- p1 cover — studio subtitle + main title + EN subtitle + gold/pink rules + edition date
- p2–8 auto TOC — navy chapter names, blossom dot leaders
- p32 first part divider ("第二部分 · 理解收益、复利与风险")
- chapter openings — top rule + "第 N 章" soft label + big title + bottom rule
- appendix pages — unnumbered chapters with roman lettering
