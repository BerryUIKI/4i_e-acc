# File Naming — Agent Rule

## Repo path rules

- **ASCII only.** No spaces, no CJK characters, no special characters beyond `-` and `_`.
- **kebab-case** for file and directory names. Use hyphens, not underscores, as word separators.
- **Lowercase** throughout (except for all-caps files like `README.md`, `LICENSE`).

## Specific conventions

| Context | Pattern | Example |
|---------|---------|---------|
| Output PDFs | English slug | `quadruple-cognition-long-life.pdf` |
| Illustrations | `NN-descriptive-name.ext` | `00-cover.png`, `07-asset-tree.png` |
| Analysis scripts | `chNN_topic.py` | `ch06_inflation.py` |
| Chapter files | `XNNN-description.md` | `E004-family-case-studies.md` |
| Handoff documents | `agents/{main-id}/handoffs/handoff-{id}-{date}.md` | `agents/0101aaa313a11c56/f78f1d3e/handoffs/handoff-f78f1d3e-20260729-2100.md` |

## Rationale

Non-ASCII characters in terminal paths cause encoding bugs in git, shell scripts, and LaTeX toolchains. This repo's CI pipeline (pandoc → xelatex) is especially sensitive.
