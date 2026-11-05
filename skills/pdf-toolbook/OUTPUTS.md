# PDF output layout

Run commands from the repository root:

```powershell
python skills/pdf-toolbook/scripts/build_pdf.py build book-task.md
```

- `output/pdf/quadruple-long-life.pdf`: current reader-facing PDF.
- `output/build/quadruple-long-life/`: merged Markdown, generated TeX and split chapter files. Auxiliary logs are cleaned after a successful build.
- `output/previews/`: rendered pages and visual QA sheets.
- `output/archive/2026-11-05/`: previous local artifacts retained during cleanup.

The `tex` command defaults to `output/build/quadruple-long-life/book.tex`. Explicit PDF output paths are supported; their intermediates remain under `output/build/<pdf-stem>/`. Use different stems for independent builds.

Source art stays in `assets/illustrations/` and the book's `assets/`; chart images stay in the book's `analysis/output/`, next to their source scripts and provenance. The builder resolves source images and the cover directly and does not copy images into the output root. Build artifacts are ignored by Git. CI uploads only the exact final PDF, never an arbitrary file found recursively.

Old tracked output copies were removed from the repository index. Local copies were archived rather than erased; their earlier versions also remain in Git history.
