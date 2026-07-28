#!/usr/bin/env python3
"""
PDF Toolbook Builder
————————————————————
Scans workspace directories for Markdown investment documents,
compiles them into a brand-styled PDF using Pandoc + XeLaTeX.

Usage:
    python build_pdf.py scan <directory>        # Scan directory, generate index
    python build_pdf.py check                   # Check dependencies
    python build_pdf.py build <index_file>       # Build PDF from index
    python build_pdf.py tex <index_file>         # Generate .tex only (no PDF)
"""

import os
import sys
import shutil
import re
import subprocess
from pathlib import Path
from datetime import datetime

# ── Configuration ─────────────────────────────────────

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = SKILL_DIR / "assets" / "template"

# Thresholds for file splitting
SPLIT_SIZE_KB = 100        # Split if merged MD > 100KB
SPLIT_CHAPTER_MIN = 6       # Split if > 5 chapters (always split at 6+)

# ── Utility Functions ─────────────────────────────────


def cmd(name):
    """Check if a CLI command is available."""
    return shutil.which(name) is not None


def rprint(msg, level="info"):
    """Prefixed logging."""
    prefixes = {"info": "  📄", "ok": "  ✅", "warn": "  ⚠️", "err": "  ❌", "step": "🔧"}
    p = prefixes.get(level, "  ")
    print(f"{p} {msg}")


# ── LaTeX Preprocessing Pipeline ──────────────────────


def escape_latex_special_chars(text):
    """
    Escape LaTeX special characters in raw text.

    ⚠️⚠️⚠️ WARNING — DO NOT USE THIS FUNCTION ⚠️⚠️⚠️

    This function has TWO fatal flaws:

    1. Do NOT call this BEFORE Pandoc conversion!
       Pandoc already auto-escapes special characters when converting MD → LaTeX.
       Calling this before Pandoc causes double-escaping (e.g. $ → \\$ → renders
       as literal backslash-dollar) and Markdown syntax corruption (# headings break).

    2. The known_commands restoration list is INCOMPLETE.
       LaTeX has hundreds of commands. If any unrecognized command appears in the
       text (e.g. \\noindent, \\cite, \\footnote, \\hfill), the backslash
       replacement will corrupt it. There is no practical way to enumerate all
       possible LaTeX commands, making this function inherently unreliable.

    This function is retained ONLY for reference/documentation. It is NEVER called
    in the main preprocessing pipeline. The preprocess_markdown() function does
    NOT use it. If you need post-Pandoc .tex patching, prefer targeted regex
    replacements over this general-purpose escape function.
    """
    # ... (implementation retained for reference)
    lines = text.split("\n")
    result = []
    in_code_block = False
    in_math = False  # $$ ... $$ blocks

    for line in lines:
        # Detect code block boundaries
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        # Detect display math mode
        if line.strip() == "$$":
            in_math = not in_math
            result.append(line)
            continue

        # Skip code blocks and math blocks
        if in_code_block or in_math:
            result.append(line)
            continue

        # Escape special characters — ORDER MATTERS!
        # 0. Handle backslash FIRST, then restore known LaTeX commands
        line = line.replace("\\", "\\textbackslash{}")

        known_commands = [
            "textbackslash{}", "textit", "textbf", "texttt",
            "emph", "section", "subsection", "chapter",
            "begin", "end", "item", "label", "ref",
            "href", "url", "includegraphics",
        ]
        for cmd_name in known_commands:
            line = line.replace(f"\\textbackslash{{}}{cmd_name}", f"\\{cmd_name}")

        # 1. All other special characters
        escapes = [
            ("&", "\\&"),
            ("%", "\\%"),
            ("$", "\\$"),
            ("#", "\\#"),
            ("_", "\\_"),
            ("{", "\\{"),
            ("}", "\\}"),
            ("~", "\\textasciitilde{}"),
            ("^", "\\^{}"),
        ]
        for char, replacement in escapes:
            line = line.replace(char, replacement)

        result.append(line)

    return "\n".join(result)


def remove_emoji(text):
    """Strip Unicode emoji (LaTeX cannot render them)."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # misc
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)


def convert_html_to_md(text):
    """Convert embedded HTML to Markdown syntax."""
    # <img src="..." ...> → ![image](src)
    text = re.sub(
        r'<img\s+[^>]*?src=["\']([^"\']+)["\'][^>]*?>',
        r"![](\1)",
        text,
        flags=re.IGNORECASE,
    )
    # Strip <div> / <span> tags, keep content
    text = re.sub(r"</?div[^>]*?>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"</?span[^>]*?>", "", text, flags=re.IGNORECASE)
    return text


def convert_task_lists(text):
    """Convert Markdown task lists to plain lists."""
    text = re.sub(r"^- \[x\] ", "- ", text, flags=re.MULTILINE)
    text = re.sub(r"^- \[ \] ", "- ", text, flags=re.MULTILINE)
    return text


def preprocess_markdown(text):
    """
    Pre-Markdown safety preprocessing pipeline.

    IMPORTANT: This runs BEFORE Pandoc converts MD → LaTeX.
    Pandoc natively handles LaTeX special character escaping ($ % & _ # ~ ^ { }).
    We must NOT escape those characters here — doing so would corrupt Markdown
    syntax (# headings, _ emphasis) and cause double-escaping in the output.

    Only preprocess things Pandoc cannot handle:
      1. HTML tags → Markdown syntax (Pandoc passes HTML through to LaTeX)
      2. Task lists → plain lists (Pandoc doesn't support task list → LaTeX)
      3. Emoji removal (LaTeX cannot render Unicode emoji)
    """
    text = convert_html_to_md(text)              # 1. HTML → MD
    text = convert_task_lists(text)               # 2. Task lists → plain
    text = remove_emoji(text)                     # 3. Remove emoji
    return text


def extract_title_from_md(filepath):
    """Extract H1 heading from a Markdown file as document title."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                m = re.match(r"^#\s+(.+)", line)
                if m:
                    return m.group(1).strip()
        return filepath.stem
    except Exception:
        return filepath.stem


def scan_directory(directory, output_file=None):
    """
    Recursively scan a directory, collect all .md files (excluding
    README-zh_CN.md and _-prefixed files), sort by directory structure,
    and generate an index file.

    Returns: list[dict] — each entry has {title, path, abs_path}
    """
    dir_path = (WORKSPACE_ROOT / directory).resolve()

    if not dir_path.exists():
        rprint(f"Directory not found: {dir_path}", "err")
        sys.exit(1)

    md_files = []
    for root, dirs, files in os.walk(dir_path):
        # Skip hidden and _-prefixed directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and not d.startswith("_")]
        for f in files:
            if f.endswith(".md") and not f.startswith("_"):
                # Skip bilingual README copies (keep English primary)
                if f in ("README-zh_CN.md",):
                    continue
                full_path = os.path.join(root, f)
                md_files.append(full_path)

    # Sort by directory structure
    md_files.sort()

    if not md_files:
        rprint(f"No Markdown files found in '{directory}'", "warn")
        return []

    # Build index entries
    entries = []
    for fp in md_files:
        title = extract_title_from_md(fp)
        rel_path = os.path.relpath(fp, WORKSPACE_ROOT)
        entries.append({
            "title": title,
            "path": rel_path,
            "abs_path": fp,
        })

    # Write index file
    if output_file is None:
        output_file = WORKSPACE_ROOT / "task.md"

    idx_lines = [f"# Toolbook TOC\n"]
    idx_lines.append(f"> Scanned: `{directory}` · {len(entries)} documents\n")
    idx_lines.append(f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

    for i, e in enumerate(entries, 1):
        idx_lines.append(f"{i}. [{e['title']}]({e['path']})")

    idx_content = "\n".join(idx_lines)
    output_path = Path(output_file)
    output_path.write_text(idx_content, encoding="utf-8")

    rprint(f"Index generated: {output_path}", "ok")
    rprint(f"Total: {len(entries)} documents", "info")
    for e in entries:
        rprint(f"  {e['title']}  ({e['path']})", "info")

    return entries


def check_dependencies():
    """Check if xelatex and pandoc are available."""
    results = {
        "xelatex": cmd("xelatex"),
        "pandoc": cmd("pandoc"),
    }
    all_ok = all(results.values())

    for name, ok in results.items():
        status = "available" if ok else "missing"
        prefix = "ok" if ok else "err"
        rprint(f"{name}: {status}", prefix)

    return all_ok


def resolve_image_paths(md_content, md_dir):
    """
    Resolve relative image paths in Markdown to absolute paths.

    Matches: ![alt](path) and <img src="path">
    """
    def replacer(match):
        prefix = match.group(1)  # ![alt](  or  <img src="
        img_path = match.group(2)
        suffix = match.group(3)  # )  or  "

        # Skip URLs and absolute paths
        if img_path.startswith(("http://", "https://", "/", "file://")):
            return match.group(0)

        # Resolve relative path
        abs_img = (md_dir / img_path).resolve()
        if abs_img.exists():
            return f'{prefix}{abs_img}{suffix}'
        else:
            rprint(f"Image not found: {img_path} (from {md_dir})", "warn")
            return match.group(0)

    # Markdown image syntax
    content = re.sub(
        r'(!\[.*?\])\(([^)]+)\)',
        replacer,
        md_content
    )
    # HTML img syntax
    content = re.sub(
        r'(<img\s+[^>]*?src=["\'])([^"\']+)(["\'])',
        replacer,
        content
    )
    return content


def merge_markdown(entries, output_file):
    """
    Merge indexed documents into a single Markdown file.

    Prepends chapter headers with page breaks.
    Applies preprocessing: HTML→MD, task lists→plain, emoji removal.
    Then resolves relative image paths to absolute.
    """
    merged_lines = []
    chapter_num = 0

    for e in entries:
        md_path = Path(WORKSPACE_ROOT) / e["path"]
        if not md_path.exists():
            rprint(f"Skipping missing file: {e['path']}", "warn")
            continue

        chapter_num += 1
        content = md_path.read_text(encoding="utf-8")

        # Step 1: LaTeX preprocessing (must happen before image path resolution)
        content = preprocess_markdown(content)

        # Step 2: Resolve image paths
        md_dir = md_path.parent
        content = resolve_image_paths(content, md_dir)

        # Add chapter separator (ctexbook auto-numbers chapters, so use title only)
        merged_lines.append("\n\n\\newpage\n\n")
        merged_lines.append(f"# {e['title']}\n\n")
        merged_lines.append(content)

    merged = "\n".join(merged_lines)
    output_path = Path(output_file)
    output_path.write_text(merged, encoding="utf-8")
    rprint(f"Documents merged: {output_path} ({chapter_num} chapters)", "ok")
    return output_path, chapter_num



# ── LaTeX Compilation ─────────────────────────────────


def generate_tex(template_file, merged_md_path, output_tex_path,
                 title="4i_e-acc Toolbook", author="4i_e-acc Workspace",
                 date=None, toc=True):
    """Generate .tex source from merged Markdown via Pandoc (no compilation)."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    pandoc_args = [
        "pandoc",
        str(merged_md_path),
        "-o", str(output_tex_path),
        f"--template={template_file}",
        f"--metadata=title:{title}",
        f"--metadata=author:{author}",
        f"--metadata=date:{date}",
        f"--metadata=lang:zh-CN",
        "-V", "CJKmainfont=PingFang SC",
        "-V", "CJKsansfont=PingFang SC",
        "-V", "CJKmonofont=STSongti-SC-Regular",
        "-V", "mainfont=PingFang SC",
        "-V", "monofont=SF Mono",
        "-V", "geometry:margin=2.5cm",
        "--highlight-style=tango",
        "--listings",
        "--standalone",
    ]

    if toc:
        pandoc_args.append("--toc")
        pandoc_args.append("--toc-depth=2")

    rprint("Generating .tex source...", "step")
    try:
        subprocess.run(pandoc_args, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        rprint("Pandoc conversion failed!", "err")
        if e.stderr:
            print("    Pandoc stderr:")
            for line in e.stderr.split("\n")[:20]:
                if line.strip():
                    print(f"    {line.strip()}")
        if e.stdout:
            print("    Pandoc stdout:")
            for line in e.stdout.split("\n")[:20]:
                if line.strip():
                    print(f"    {line.strip()}")
        raise
    rprint(f".tex written: {output_tex_path}", "ok")
    return output_tex_path


def should_split(merged_md_path, chapter_count):
    """Decide whether to split into main.tex + chapter .tex files."""
    size_kb = merged_md_path.stat().st_size / 1024
    if chapter_count >= SPLIT_CHAPTER_MIN:
        rprint(f"Splitting: {chapter_count} chapters (>= {SPLIT_CHAPTER_MIN})", "info")
        return True
    if size_kb > SPLIT_SIZE_KB:
        rprint(f"Splitting: merged MD is {size_kb:.0f}KB (> {SPLIT_SIZE_KB}KB)", "info")
        return True
    rprint(f"Single file: {chapter_count} chapters, {size_kb:.0f}KB", "info")
    return False


def split_tex_into_chapters(tex_path, chapter_count, output_dir):
    """
    Split a monolithic .tex file into main.tex + chapter_XX.tex files.

    The generated .tex from Pandoc has:
      - Preamble (\\documentclass … \\begin{document})
      - Cover + TOC (everything before first \\chapter or \\hypertarget)
      - Chapter bodies
      - \\end{document}

    This function extracts the preamble + cover/TOC into main.tex,
    splits each chapter body into chapter_XX.tex, and connects them with \\input.

    Returns the path to main.tex.
    """
    tex_content = Path(tex_path).read_text(encoding="utf-8")

    # Find \begin{document} — everything before it is preamble
    begin_doc_pos = tex_content.find("\\begin{document}")
    if begin_doc_pos == -1:
        rprint("Cannot split: no \\begin{document} found", "warn")
        return tex_path

    preamble = tex_content[:begin_doc_pos + len("\\begin{document}")]
    body = tex_content[begin_doc_pos + len("\\begin{document}"):]

    # Find \end{document} — everything after is postamble
    end_doc_pos = body.rfind("\\end{document}")
    postamble = ""
    if end_doc_pos != -1:
        postamble = body[end_doc_pos:]
        body = body[:end_doc_pos]

    # Split body by chapter markers
    # Pandoc may use \chapter{...} or \hypertarget{...}{...\chapter{...}}
    chapter_pattern = r'(\\hypertarget\{[^}]*\}\{%\s*\n)?\s*(\\chapter\{[^}]*\})'
    parts = re.split(chapter_pattern, body)

    chapters = []
    i = 0
    # parts[0] is text before first chapter (TOC, cover content after \begin{document})
    pre_chapter_content = parts[0] if len(parts) > 0 else ""

    # Subsequent parts are: [hypertarget, chapter_cmd, chapter_body, hypertarget, chapter_cmd, chapter_body, ...]
    i = 1
    while i < len(parts):
        # parts[i] may be the hypertarget (or None if no match)
        chunk = ""
        if i < len(parts) and parts[i] and parts[i].strip().startswith("\\hypertarget"):
            chunk += parts[i]
            i += 1
        # parts[i] is the \chapter{...}
        if i < len(parts) and parts[i]:
            chunk += parts[i]
            i += 1
        # parts[i] is the chapter body
        if i < len(parts):
            body_text = ""
            if parts[i]:
                body_text = parts[i]
            chapters.append(chunk + body_text)
            i += 1
        else:
            if chunk:
                chapters.append(chunk)

    if not chapters:
        rprint("Cannot split: no chapter markers found in body", "warn")
        return tex_path

    rprint(f"Splitting into {len(chapters)} chapter files...", "step")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write each chapter file
    chapter_files = []
    for idx, ch_content in enumerate(chapters, 1):
        ch_filename = f"chapter_{idx:02d}.tex"
        ch_path = output_dir / ch_filename
        ch_path.write_text(ch_content, encoding="utf-8")
        chapter_files.append(ch_filename)
        rprint(f"  {ch_filename} written ({len(ch_content)} chars)", "info")

    # Build main.tex with preamble + cover/TOC + \input{chapter_XX} + \end{document}
    main_lines = [preamble]
    main_lines.append(pre_chapter_content)
    main_lines.append("")

    for ch_file in chapter_files:
        main_lines.append(f"\\input{{{ch_file}}}")
        main_lines.append("")

    main_lines.append(postamble if postamble else "\\end{document}")

    main_path = output_dir / "main.tex"
    main_path.write_text("\n".join(main_lines), encoding="utf-8")
    rprint(f"main.tex written with {len(chapter_files)} chapter inputs", "ok")

    return str(main_path)


def run_xelatex(tex_path, work_dir, passes=2):
    """
    Run XeLaTeX multiple passes for correct cross-references and TOC.

    Pass 1: generates .aux, .toc files
    Pass 2: reads .aux/.toc → resolves all references, page numbers
    Pass 3: only if Pass 2 reports unresolved references (rare)

    The working directory MUST be the directory containing the .tex file,
    so XeLaTeX finds \\input{} files and writes aux files correctly.
    """
    tex_file = Path(tex_path).name
    tex_dir = Path(tex_path).parent

    for p in range(1, passes + 1):
        rprint(f"XeLaTeX pass {p}/{passes}...", "step")
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-output-directory",
             str(work_dir), tex_file],
            cwd=str(tex_dir),
            capture_output=True,
            text=True,
        )

        # Check for fatal errors
        if "Fatal error" in result.stdout or "Fatal error" in result.stderr:
            rprint(f"XeLaTeX pass {p} failed with fatal error", "err")
            # Try to read the .log file for detailed error info
            log_file = work_dir / Path(tex_file).with_suffix(".log").name
            if log_file.exists():
                rprint(f"Reading log: {log_file}", "info")
                log_content = log_file.read_text(encoding="utf-8", errors="replace")
                # Extract error lines and surrounding context
                log_lines = log_content.split("\n")
                error_context = []
                for idx, line in enumerate(log_lines):
                    if line.startswith("!") or "Error" in line or "Fatal" in line:
                        start = max(0, idx - 2)
                        end = min(len(log_lines), idx + 5)
                        error_context.extend(log_lines[start:end])
                        error_context.append("---")
                if error_context:
                    print("    Log error context:")
                    for line in error_context[-30:]:
                        if line.strip():
                            print(f"    {line.strip()}")
                else:
                    # Fallback: print last 30 lines of stdout
                    log_lines = (result.stdout + result.stderr).split("\n")
                    for line in log_lines[-30:]:
                        if line.strip():
                            print(f"    {line.strip()}")
            else:
                log_lines = (result.stdout + result.stderr).split("\n")
                for line in log_lines[-30:]:
                    if line.strip():
                        print(f"    {line.strip()}")
            return False

        # Check for unresolved references (only warn on final pass)
        if "LaTeX Warning: Reference" in result.stdout:
            rprint(f"Pass {p}: unresolved references remain (expected if not final pass)", "warn")

        if "LaTeX Warning: Rerun" in result.stdout or "Rerun to get" in result.stdout:
            rprint(f"Pass {p}: LaTeX suggests another rerun", "info")

    rprint("XeLaTeX compilation complete", "ok")
    return True


def clean_aux_files(work_dir):
    """Remove LaTeX auxiliary files after successful compilation."""
    aux_extensions = {".aux", ".log", ".out", ".toc", ".lof", ".lot",
                      ".bbl", ".blg", ".synctex.gz", ".fls", ".fdb_latexmk",
                      ".xdv", ".idx", ".ind", ".ilg"}
    work_dir = Path(work_dir)

    cleaned = 0
    for f in work_dir.iterdir():
        if f.suffix in aux_extensions:
            f.unlink()
            cleaned += 1

    if cleaned:
        rprint(f"Cleaned {cleaned} auxiliary files", "ok")


def compile_pdf(template_file, merged_md_path, output_pdf_path,
                title="4i_e-acc Toolbook", author="4i_e-acc Workspace",
                date=None, chapter_count=1, cleanup=True):
    """
    Full compilation pipeline: MD → .tex → (optional split) → XeLaTeX 2-pass → PDF.

    1. Generate .tex from merged MD via Pandoc
    2. Check if splitting is needed (>100KB or >5 chapters)
    3. If split: main.tex + chapter_XX.tex files
    4. Compile with XeLaTeX (2 passes minimum)
    5. Move PDF to output path
    6. Clean auxiliary files
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    output_dir = Path(output_pdf_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Generate .tex
    base_name = Path(output_pdf_path).stem
    tex_path = output_dir / f"{base_name}.tex"
    generate_tex(template_file, merged_md_path, tex_path, title, author, date)

    # Step 2: Decide on splitting
    work_dir = output_dir
    if should_split(merged_md_path, chapter_count):
        work_dir = output_dir / "tex"
        tex_path = split_tex_into_chapters(tex_path, chapter_count, work_dir)

    # Step 3: Compile with XeLaTeX (2-pass minimum)
    rprint(f"Compiling PDF (2-pass XeLaTeX)...", "step")
    success = run_xelatex(tex_path, work_dir, passes=2)

    if not success:
        rprint("Compilation failed. See log for details.", "err")
        rprint(f"Check: {work_dir / Path(tex_path).with_suffix('.log').name}",
               "info")
        return False

    # Step 4: Move resulting PDF to output path
    pdf_name = Path(tex_path).with_suffix(".pdf").name
    generated_pdf = work_dir / pdf_name
    if generated_pdf.exists():
        shutil.move(str(generated_pdf), str(output_pdf_path))
        rprint(f"PDF saved: {output_pdf_path}", "ok")
    else:
        rprint(f"PDF not found at expected location: {generated_pdf}", "err")
        # Try to find it
        for f in output_dir.rglob("*.pdf"):
            rprint(f"  Found PDF candidate: {f}", "info")
        return False

    # Step 5: Clean auxiliary files
    if cleanup:
        clean_aux_files(work_dir)
        clean_aux_files(output_dir)
        # Also clean merged intermediate if in output dir
        if merged_md_path.parent == output_dir:
            merged_md_path.unlink(missing_ok=True)

    return True


# ── CLI ───────────────────────────────────────────────


def parse_index(index_content):
    """Parse document entries from an index file."""
    entries = []
    for line in index_content.splitlines():
        m = re.match(r"^\d+\.\s*\[(.+)\]\((.+)\)", line.strip())
        if m:
            entries.append({
                "title": m.group(1).strip(),
                "path": m.group(2).strip(),
            })
    return entries


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "scan":
        if len(sys.argv) < 3:
            rprint("Usage: build_pdf.py scan <directory> [output_index]", "err")
            sys.exit(1)
        directory = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else None
        entries = scan_directory(directory, output)
        if entries:
            print(f"\nINDEX_COUNT:{len(entries)}")
            for e in entries:
                print(f"INDEX_ENTRY:{e['title']}||{e['path']}")

    elif command == "check":
        ok = check_dependencies()
        print(f"\nDEPS_OK:{ok}")

    elif command == "build":
        if len(sys.argv) < 3:
            rprint("Usage: build_pdf.py build <index_file> [output_pdf] [title] [author] [date]", "err")
            sys.exit(1)

        index_file = sys.argv[2]
        output_pdf = sys.argv[3] if len(sys.argv) > 3 else str(WORKSPACE_ROOT / "output" / "toolbook.pdf")
        title = sys.argv[4] if len(sys.argv) > 4 else "4i_e-acc Toolbook"
        author = sys.argv[5] if len(sys.argv) > 5 else "4i_e-acc Workspace"
        date = sys.argv[6] if len(sys.argv) > 6 else None

        # Parse index
        idx_content = Path(index_file).read_text(encoding="utf-8")
        entries = parse_index(idx_content)

        if not entries:
            rprint("No document entries found in index file", "err")
            sys.exit(1)

        # Merge MD with preprocessing
        merged_path = WORKSPACE_ROOT / "output" / "_merged.md"
        merged_path.parent.mkdir(parents=True, exist_ok=True)
        merged_path, chapter_count = merge_markdown(entries, merged_path)

        # Find template
        template = TEMPLATE_DIR / "pandoc-template.tex"
        if not template.exists():
            rprint(f"Template not found: {template}", "err")
            sys.exit(1)

        # Compile PDF (2-pass XeLaTeX, auto-split if large)
        output_path = Path(output_pdf)
        try:
            success = compile_pdf(
                template, merged_path, output_path,
                title, author, date, chapter_count
            )
        except Exception as e:
            rprint(f"Unexpected error during compilation: {e}", "err")
            rprint("Check the log file and intermediate .tex for details.", "err")
            import traceback
            traceback.print_exc()
            sys.exit(1)

        if success:
            print(f"\nPDF_PATH:{output_path}")
        else:
            sys.exit(1)

    elif command == "tex":
        if len(sys.argv) < 3:
            rprint("Usage: build_pdf.py tex <index_file> [output_tex] [title] [author] [date]", "err")
            sys.exit(1)

        index_file = sys.argv[2]
        output_tex = sys.argv[3] if len(sys.argv) > 3 else str(WORKSPACE_ROOT / "output" / "toolbook.tex")
        title = sys.argv[4] if len(sys.argv) > 4 else "4i_e-acc Toolbook"
        author = sys.argv[5] if len(sys.argv) > 5 else "4i_e-acc Workspace"
        date = sys.argv[6] if len(sys.argv) > 6 else None

        idx_content = Path(index_file).read_text(encoding="utf-8")
        entries = parse_index(idx_content)

        merged_path = WORKSPACE_ROOT / "output" / "_merged.md"
        merged_path.parent.mkdir(parents=True, exist_ok=True)
        merged_path, chapter_count = merge_markdown(entries, merged_path)

        template = TEMPLATE_DIR / "pandoc-template.tex"
        output_path = Path(output_tex)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tex_path = generate_tex(template, merged_path, output_path, title, author, date)

        # Split if needed
        if should_split(merged_path, chapter_count):
            work_dir = output_path.parent / "tex"
            tex_path = split_tex_into_chapters(tex_path, chapter_count, work_dir)

        print(f"\nTEX_PATH:{tex_path}")

    else:
        rprint(f"Unknown command: {command}", "err")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
