# PDF Toolbook Skill — Requirements Specification

> **Project:** 4i_e-acc Investment Document Workspace
> **Created:** 2026-07-28
> **Status:** Built · See `.workbuddy/skills/pdf-toolbook/` for implementation

---

## 1. Overview

A project-level Skill for the 4i_e-acc workspace that aggregates Markdown investment documents into a complete PDF toolbook with full book formatting and DollarHua (花有财) brand styling.

## 2. Core Requirements

### 2.1 Input

- **Source:** User-specified `.md` documents within the workspace
- **Supported:** Markdown files (`.md`) with Chinese content, images, code blocks, tables

### 2.2 Ordering

- **Default:** By directory structure (preserving folder hierarchy)
- Users can override ordering by editing the generated index file

### 2.3 Output Format

- **Format:** PDF
- **Layout:** Full book format with:
  - Cover — DollarHua brand styling
  - Table of Contents — auto-generated with page numbers
  - Headers/Footers — chapter name / book title + page numbers
  - Image placement — embedded in body text
  - CJK typography — proper Chinese font support
  - Code highlighting — syntax-colored code blocks
  - Table rendering — clean Markdown table output
- **Brand:** DollarHua signature pink (`#FEC6CD`) as primary, Bond Navy (`#1D1E50`) for text

### 2.4 Output Location

- Presented via conversation for user to save locally
- **Not committed to the repo** (public repo, per AGENTS.md)

## 3. Technical Approach (Confirmed)

### Selected: LaTeX + Pandoc

| Component | Purpose |
|-----------|---------|
| **Pandoc** | Convert Markdown → `.tex` (LaTeX source) |
| **Custom LaTeX template** | Cover, brand styling, headers/footers |
| **XeLaTeX** | Compile `.tex` → PDF, CJK support via `ctex` |
| **Python** | Orchestrate: MD → Pandoc → XeLaTeX → PDF |

### Dependencies

| Dependency | Install | Status |
|-----------|---------|--------|
| MacTeX / BasicTeX + ctex | brew | Not installed in environment |
| Pandoc | brew install pandoc | Not installed in environment |
| Python 3 | Workspace has it | Available |
| CJK fonts | macOS system (PingFang / Songti) | Available |

## 4. Branding (DollarHua)

See `assets/dollarhua/README.md` for authoritative specs:
- **Primary:** `#FEC6CD` (Signature Pink) — cover, chapter decor, page numbers
- **Text:** `#1D1E50` (Bond Navy) — body text, headings
- **Full palette:** 8-color standard in `references/dollarhua-brand.md`

## 5. Actual Skill Structure

```
.workbuddy/skills/pdf-toolbook/
├── SKILL.md                        # Main doc: triggers, 6-step workflow
├── scripts/
│   ├── build_pdf.py                # Main entry: scan/check/build/tex
│   └── install_deps.sh             # Dependency checker
├── references/
│   ├── dollarhua-brand.md          # 8-color palette + LaTeX defs
│   ├── latex-pitfalls.md           # Agent-required: escaping, CJK, Pandoc, debug
│   └── troubleshooting.md          # Known limitations and workarounds
└── assets/template/
    └── pandoc-template.tex         # Custom Pandoc LaTeX template
```
