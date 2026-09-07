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
import platform
import urllib.request
import zipfile
from pathlib import Path
from datetime import datetime

# ── Configuration ─────────────────────────────────────

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = SKILL_DIR / "assets" / "template"
FONTS_DIR = SKILL_DIR / "assets" / "fonts"

# Source Han font download URLs (Adobe releases, same as CI workflow)
SOURCE_HAN_SERIF_SC_URL = (
    "https://github.com/adobe-fonts/source-han-serif/releases/download/"
    "2.003R/09_SourceHanSerifSC.zip"
)
SOURCE_HAN_SANS_SC_URL = (
    "https://github.com/adobe-fonts/source-han-sans/releases/download/"
    "2.005R/09_SourceHanSansSC.zip"
)

# Thresholds for file splitting
SPLIT_SIZE_KB = 100        # Split if merged MD > 100KB
SPLIT_CHAPTER_MIN = 6       # Split if > 5 chapters (always split at 6+)

# ── Utility Functions ─────────────────────────────────


def cmd(name):
    """Check if a CLI command is available."""
    return shutil.which(name) is not None


# ── Font Management ──────────────────────────────────


def _run(cmd_args, **kwargs):
    """Run a command and return (returncode, stdout, stderr)."""
    result = subprocess.run(cmd_args, capture_output=True, text=True, **kwargs)
    return result.returncode, result.stdout, result.stderr


def check_source_han_fonts():
    """
    Check whether any Source Han CJK font (SC or CN) is available system-wide.
    Returns True if at least one Source Han Serif/Sans font is found.
    """
    if platform.system() == "Windows":
        fonts_dir = Path(os.environ.get("WINDIR", "C:\\Windows")) / "Fonts"
        if fonts_dir.exists():
            for f in fonts_dir.iterdir():
                name = f.name.lower()
                if "sourcehanserif" in name or "sourcehansans" in name:
                    rprint(f"Found Source Han font: {f.name}", "ok")
                    return True
        return False
    else:
        try:
            rc, stdout, _ = _run(["fc-list", ":family"])
            if rc == 0 and ("Source Han Serif" in stdout or "Source Han Sans" in stdout):
                lines = [l for l in stdout.split("\n") if "Source Han" in l]
                rprint(f"Found {len(lines)} Source Han font(s)", "ok")
                return True
        except FileNotFoundError:
            pass
        return False


def _download_file(url, dest_path):
    """Download a file with progress indication."""
    rprint(f"Downloading {url.split('/')[-1]}...", "step")
    try:
        urllib.request.urlretrieve(url, str(dest_path))
        rprint(f"  Saved: {dest_path}", "ok")
        return True
    except Exception as e:
        rprint(f"Download failed: {e}", "err")
        return False


def install_source_han_fonts():
    """
    Download and install Source Han Serif/Sans SC fonts from GitHub releases.
    On Linux: copies OTF files to ~/.fonts/ and runs fc-cache.
    On macOS: copies to ~/Library/Fonts/.
    On Windows: copies to C:\\Windows\\Fonts\\ (may require admin);
                falls back to local assets/fonts/ dir.
    """
    system = platform.system()
    FONTS_DIR.mkdir(parents=True, exist_ok=True)

    if system == "Linux":
        target_dir = Path.home() / ".fonts"
        target_dir.mkdir(parents=True, exist_ok=True)
        font_cmd = ["fc-cache", "-fv"]
    elif system == "Darwin":
        target_dir = Path.home() / "Library" / "Fonts"
        target_dir.mkdir(parents=True, exist_ok=True)
        font_cmd = None
    else:
        target_dir = Path(os.environ.get("WINDIR", "C:\\Windows")) / "Fonts"
        try:
            test = target_dir / ".write_test"
            test.touch()
            test.unlink()
            font_cmd = None
        except (PermissionError, OSError):
            rprint("Cannot write to system Fonts directory (admin required)", "warn")
            rprint(f"Installing to local: {FONTS_DIR}", "info")
            target_dir = FONTS_DIR
            font_cmd = None

    font_urls = [
        ("SourceHanSerifSC.zip", SOURCE_HAN_SERIF_SC_URL),
        ("SourceHanSansSC.zip", SOURCE_HAN_SANS_SC_URL),
    ]

    for zip_name, url in font_urls:
        zip_path = FONTS_DIR / zip_name
        if zip_path.exists():
            rprint(f"Using cached: {zip_name}", "info")
        else:
            if not _download_file(url, zip_path):
                return False

        rprint(f"Extracting {zip_name}...", "step")
        try:
            with zipfile.ZipFile(str(zip_path), "r") as zf:
                for member in zf.namelist():
                    if member.lower().endswith(".otf"):
                        basename = os.path.basename(member)
                        dest = target_dir / basename
                        if not dest.exists():
                            with zf.open(member) as src, open(str(dest), "wb") as dst:
                                dst.write(src.read())
            rprint(f"  OTF files installed to {target_dir}", "ok")
        except Exception as e:
            rprint(f"Extraction failed: {e}", "err")
            return False

    if font_cmd:
        rprint("Refreshing font cache...", "step")
        rc, stdout, stderr = _run(font_cmd)
        if rc == 0:
            rprint("Font cache refreshed", "ok")
        else:
            rprint(f"fc-cache warning: {stderr.strip()}", "warn")

    if system == "Windows" and target_dir == FONTS_DIR:
        rprint(
            f"Fonts installed to {FONTS_DIR}. "
            f"To use system-wide, copy OTF files to "
            f"{os.environ.get('WINDIR', 'C:\\\\Windows')}\\Fonts\\ "
            f"(requires admin).",
            "warn"
        )
    return True


def ensure_fonts():
    """
    Ensure Source Han fonts are available. Downloads them if missing.
    """
    if check_source_han_fonts():
        return True
    rprint("Source Han fonts not found. Downloading from GitHub...", "warn")
    rprint("  (One-time setup, cached after first download)", "info")
    if install_source_han_fonts():
        if check_source_han_fonts():
            return True
        rprint(
            "Fonts installed but may not be immediately available to XeLaTeX. "
            "Try running 'fc-cache -fv' or restarting your terminal.",
            "warn"
        )
        return True
    rprint("Failed to install Source Han fonts. PDF compilation may fall back to Fandol.", "err")
    return False


def rprint(msg, level="info"):
    """Prefixed logging."""
    prefixes = {"info": "  📄", "ok": "  ✅", "warn": "  ⚠️", "err": "  ❌", "step": "🔧"}
    p = prefixes.get(level, "  ")
    try:
        print(f"{p} {msg}")
    except UnicodeEncodeError:
        safe_prefixes = {"info": "  [INFO]", "ok": "  [OK]", "warn": "  [WARN]", "err": "  [ERR]", "step": ">>"}
        sp = safe_prefixes.get(level, "  ")
        print(f"{sp} {msg}".encode("ascii", errors="replace").decode("ascii"))


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
    """
    Strip Unicode emoji and decorative symbols (LaTeX cannot render them).

    ⚠️ CAREFUL: The regex ranges MUST NOT overlap with CJK blocks
    (U+2E80-U+2EFF, U+3000-U+303F, U+4E00-U+9FFF, U+F900-U+FAFF,
    U+FE30-U+FE4F, U+20000-U+2FFFF, etc.).
    Use discrete, non-overlapping ranges only.
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # chess symbols
        "\U0001FA70-\U0001FAFF"  # symbols extended-A
        "\U0001F000-\U0001F02F"  # mahjong tiles
        "\U0001F0A0-\U0001F0FF"  # playing cards
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


def strip_yaml_frontmatter(text):
    """
    Strip YAML frontmatter (--- ... ---) from the beginning of a Markdown
    file.  Pandoc treats text between --- delimiters as metadata; if CJK
    body text falls inside a YAML block, it is silently discarded.

    Only strips when the body between the --- markers looks like YAML
    (contains at least one ``key: value`` line) AND the closing ---
    appears within the first 50 lines.  This guardrail is critical:
    ``---`` is also a valid Markdown thematic break, and many source
    files use back-to-back ``---`` pairs to bracket an epigraph.
    Without this check, the entire bracketed epigraph (e.g. B001)
    would be silently discarded.
    """
    stripped = text.lstrip("\n")
    if not stripped.startswith("---"):
        return text

    # Closing --- must be a standalone line within the first 50 lines
    head = stripped.split("\n", 50)[:50]
    closer_idx = None
    for i, line in enumerate(head[1:], start=1):
        if line.strip() == "---":
            closer_idx = i
            break
    if closer_idx is None:
        return text

    # YAML-content guardrail: body between --- must look like YAML
    # (at least one `key: value` line).  Without this check, back-to-back
    # thematic breaks would be mistaken for a YAML block and the entire
    # bracketed epigraph would be silently discarded.
    body = "\n".join(head[1:closer_idx])
    if not re.search(r"^\s*[A-Za-z_][\w-]*\s*:", body, re.MULTILINE):
        return text

    after_closer = "\n".join(head[closer_idx + 1:])
    return after_closer.lstrip("\n")


# ── Chapter title normalization ────────────────────────

# Match "第N章" or "第N部分" prefix (with optional whitespace) where N is
# 1-3 ASCII digits or 1-3 CJK numerals.  Anchored to the start of the
# title to avoid false positives mid-title.
_CHAPTER_PREFIX_RE = re.compile(
    r"^第[\d零一二三四五六七八九十百千]{1,3}\s*(?:章|部分)\s*[\s·•・:：\-—]+"
)


def clean_chapter_title(title):
    """
    Strip a leading "第N章 · " or "第N部分 · " prefix from a chapter
    title.  The LaTeX template's \\titleformat{\\chapter} already adds
    "第 N 章" via \\thechapter, so a duplicate prefix in the title
    yields "第 5 章 第五章 · 复利..." in the rendered page.  Removing
    the prefix gives the clean "第 5 章 复利究竟如何工作" form.

    Also collapses multiple whitespace into a single space.
    """
    cleaned = _CHAPTER_PREFIX_RE.sub("", title).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def rewrite_image_paths(text):
    """
    Rewrite image references in the merged Markdown so xelatex can
    find them via the template's \\graphicspath entries.

    Source MDs (e.g. B002-inflation.md) use relative paths such as
    `../analysis/output/ch06_inflation.png`.  These paths only resolve
    when xelatex is invoked from the source-MD's directory, not from
    the build output directory.  build_pdf.py copies the chart images
    into the build directory, so we strip the directory prefix and
    keep only the filename.  \\graphicspath then locates the file in
    the build directory.
    """
    return re.sub(
        r"\.\.?/analysis/output/",
        "",
        text,
    )


def strip_chapter_heading(text):
    """
    Strip the first heading (h1 or h2) from a document.

    merge_markdown() prepends `# {title}` to every entry so each becomes
    a chapter.  If the source MD also has its own chapter title (commonly
    `## 第N章 · ...`), the result is a redundant "section" inside the new
    chapter with the same name.  This function removes the first such
    heading so only the prepended chapter title remains.

    The first heading can appear after blank lines, leading `---`
    thematic breaks, or other decoration — we scan the whole text
    rather than just the first non-empty line.
    """
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# ") or line.startswith("## "):
            return "\n".join(lines[:i] + lines[i + 1:])
    return text


# Match standalone "**第N部分 · 标题**" or "**第N部分 标题**" lines.
#   第 / 部分 must be present; the part ordinal may be 1-3 digits or CJK numerals.
PART_DIVIDER_RE = re.compile(
    r"^\*\*第[\d零一二三四五六七八九十百千]+部分(?:\s*[·•・:：\-—]+\s*.+?)\*\*\s*$",
    re.MULTILINE,
)

# Canonical 8 parts mapped to their opening chapters (per book-task.md & TOC)
CHAPTER_PART_MAP = {
    "第一章": "第一部分 · 先看清自己的财务生活",
    "第五章": "第二部分 · 理解收益、复利与风险",
    "第九章": "第三部分 · 弄清楚钱到底可以放在哪里",
    "第十三章": "第四部分 · ETF：普通人最值得掌握的投资工具",
    "第二十章": "第五部分 · 家庭资产配置实战",
    "第二十六章": "第六部分 · 开始投资",
    "第二十九章": "第七部分 · 穿越市场周期",
    "第三十一章": "第八部分 · AI 时代的个人财务",
}


def convert_part_dividers(text):
    """
    Convert standalone `**第N部分 · 标题**` lines into pandoc raw-LaTeX
    blocks invoking `\\partdivider{...}` (defined in pandoc-template.tex).

    A "part divider" line must occupy a line on its own (between blank
    lines).  Inline `**第N部分**` inside a paragraph is left untouched.

    The pattern uses `第` and `部分` as the strict markers, so headings
    like `## 第五章` or `**注意**` are unaffected.
    """
    def replacer(m):
        raw = m.group(0)
        inner = raw.strip().strip("*").strip()
        return (
            "```{=latex}\n"
            f"\\partdivider{{{inner}}}\n"
            "```"
        )
    return PART_DIVIDER_RE.sub(replacer, text)


def ensure_block_images(text):
    """
    Ensure all Markdown images ![alt](path) are standalone block elements
    (surrounded by newlines) so Pandoc creates a proper \begin{figure} environment
    and centers them rather than rendering them inline after a text sentence.
    """
    # If preceded by non-newline, insert two newlines
    text = re.sub(r'([^\n])\s*(!\[.*?\]\([^)]+\))', r'\1\n\n\2', text)
    # If followed by non-newline, insert two newlines
    text = re.sub(r'(!\[.*?\]\([^)]+\))\s*([^\n])', r'\1\n\n\2', text)
    return text


def remove_footer_instructions(text):
    """
    Remove editorial footer instructions (e.g. '> **页脚（每页 Footer）：** ...')
    from document body so they don't render as awkward blockquotes.
    The footer disclaimer is handled at the template level via fancyfoot.
    """
    return re.sub(
        r'^\s*>\s*\*\*页脚（每页\s*Footer）[：:]\*\*.*$',
        '',
        text,
        flags=re.MULTILINE
    )


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
      4. Ensure block images (prevent inline image overflow)
      5. Strip editorial footer instructions (rendered in fancyfoot instead)
    """
    text = convert_html_to_md(text)              # 1. HTML → MD
    text = convert_task_lists(text)               # 2. Task lists → plain
    text = remove_emoji(text)                     # 3. Remove emoji
    text = ensure_block_images(text)             # 4. Ensure images are standalone paragraphs
    text = remove_footer_instructions(text)      # 5. Strip editorial footer notes
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
        return Path(filepath).stem
    except Exception:
        return Path(filepath).stem


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
        try:
            suffix = match.group(3)  # )  or  "
        except IndexError:
            suffix = ""

        # Skip URLs and absolute paths
        if img_path.startswith(("http://", "https://", "/", "file://")):
            return match.group(0)

        # Resolve relative path
        abs_img = (md_dir / img_path).resolve()
        if abs_img.exists():
            return f'{prefix}{str(abs_img).replace(chr(92), "/")}{suffix}'
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


def merge_markdown(entries, output_file, frontmatter_count=5):
    """
    Merge indexed documents into a single Markdown file.

    Prepends chapter headers with page breaks.
    Applies preprocessing: YAML frontmatter stripping, source chapter
    heading removal, HTML→MD, task lists→plain, emoji removal, part
    divider conversion.
    Then resolves relative image paths to absolute.

    Sectioning (ctexbook \\frontmatter / \\mainmatter / \\backmatter):
      • \\frontmatter is opened at the very start
      • The first entry whose title contains "第" + ordinal + "章"
        triggers \\mainmatter (logical "first chapter" detection)
      • The final entry (if it contains "附录" in title or path)
        triggers \\backmatter
      • Manual TOC entries (title contains "目录") are skipped because
        the LaTeX template emits \\tableofcontents for the auto-TOC
    """
    import re as _re
    chapter_re = _re.compile(r"第[一二三四五六七八九十百千零\d]+章")

    # ── Pass 1: filter out manual TOC, keep order intact ──────────────
    kept = []
    for e in entries:
        if "目录" in e["title"] and not chapter_re.search(e["title"]):
            rprint(
                f"Skipping manual TOC: {e['title']} "
                "(\\tableofcontents handles this)", "info",
            )
            continue
        kept.append(e)

    # ── Pass 2: write merged MD with section markers ──────────────────
    # Note: \frontmatter is emitted by the LaTeX template right before
    # \tableofcontents, so TOC pages receive roman numerals (i, ii, ...).
    merged_lines = []
    chapter_num = 0
    switched_to_main = False
    switched_to_back = False

    for e in kept:
        md_path = Path(WORKSPACE_ROOT) / e["path"]
        if not md_path.exists():
            rprint(f"Skipping missing file: {e['path']}", "warn")
            continue

        # Switch to \mainmatter at the first "第N章" entry
        if not switched_to_main and chapter_re.search(e["title"]):
            merged_lines.append("\\mainmatter\n")
            switched_to_main = True

        # Switch to \backmatter right before an appendix entry
        is_appendix_entry = "附录" in e["title"] or "附录" in e["path"]
        if is_appendix_entry and not switched_to_back:
            merged_lines.append("\\backmatter\n")
            switched_to_back = True

        chapter_num += 1
        content = md_path.read_text(encoding="utf-8")

        # Step 0: Strip YAML frontmatter (--- ... ---).
        # Crucial: Pandoc treats --- blocks as YAML metadata; if CJK
        # body text falls inside a YAML block, Pandoc silently discards it.
        content = strip_yaml_frontmatter(content)

        # Step 0.5: Strip the source's own first heading (h1/h2).
        # The script prepends "# {title}" below; without this, the source's
        # own chapter heading (e.g. "## 第五章") becomes a redundant section
        # inside the newly-created chapter.
        content = strip_chapter_heading(content)

        # Step 1: LaTeX preprocessing (must happen before image path resolution)
        content = preprocess_markdown(content)

        # Step 1.5: Handle Part dividers.
        # If this chapter marks the start of a Part, emit \partdivider BEFORE \chapter
        part_title = None
        part_match = PART_DIVIDER_RE.search(content)
        if part_match:
            part_title = part_match.group(0).strip().strip("*").strip()
            content = PART_DIVIDER_RE.sub("", content)

        if not part_title:
            for k, v in CHAPTER_PART_MAP.items():
                if k in e["title"]:
                    part_title = v
                    break

        if part_title:
            merged_lines.append(f"\n\n```{{=latex}}\n\\partdivider{{{part_title}}}\n```\n\n")

        # Step 2: Rewrite image paths so xelatex can find them via
        # the template's \graphicspath entries (the build script copies
        # the chart images into the build directory).
        content = rewrite_image_paths(content)

        # Add chapter separator (ctexbook auto-numbers chapters, so use title only)
        merged_lines.append("\n\n\\newpage\n\n")
        # Strip leading "第N章" / "第N部分" — the LaTeX chapter format
        # already renders the chapter number via \thechapter.
        chapter_title = clean_chapter_title(e["title"])
        merged_lines.append(f"# {chapter_title}\n\n")
        merged_lines.append(content)

    merged = "\n".join(merged_lines)
    output_path = Path(output_file)
    output_path.write_text(merged, encoding="utf-8")
    rprint(f"Documents merged: {output_path} ({chapter_num} chapters)", "ok")
    return output_path, chapter_num



# ── LaTeX Compilation ─────────────────────────────────


def generate_tex(template_file, merged_md_path, output_tex_path,
                 title="四倍做多认知，长期做多人生", author="花花 | @BerryUIKI",
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
        "--highlight-style=tango",
        "--listings",
        "--standalone",
        # Force h1 → \chapter even when pandoc does not detect ctexbook
        # as a book-class template (e.g. when the template uses ctexbook
        # with a custom preamble).  Without this, all top-level headings
        # collapse into \section{...} and the chapter styling never fires.
        "--top-level-division=chapter",
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

    # Post-process generated LaTeX (brand rules, quotes, table headers)
    postprocess_tex(output_tex_path)

    rprint(f".tex written: {output_tex_path}", "ok")
    return output_tex_path


def postprocess_tex(tex_path):
    """
    Post-process Pandoc-generated .tex file for brand-consistent typography:
      1. Horizontal rules: replace Pandoc's default 0.5-linewidth black rule
         with a 0.2\\textwidth dh-bronze rule (print-safe, elegant).
      2. Block quotes: replace \\begin{quote}...\\end{quote} with \\begin{dhquote}...\\end{dhquote}.
      3. Table headers: inject \\rowcolor{dh-pink!25} after \\toprule\\noalign{}.
    """
    tex_path = Path(tex_path)
    content = tex_path.read_text(encoding="utf-8")

    # 1. Horizontal rules
    content = content.replace(
        r"\begin{center}\rule{0.5\linewidth}{0.5pt}\end{center}",
        r"\begin{center}{\color{dh-bronze}\rule{0.2\textwidth}{0.5pt}}\end{center}"
    )

    # 2. Block quotes
    content = re.sub(r"\\begin\{quote\}", r"\\begin{dhquote}", content)
    content = re.sub(r"\\end\{quote\}", r"\\end{dhquote}", content)

    # 3. Table header background
    content = content.replace(
        r"\toprule\noalign{}",
        r"\toprule\noalign{}\rowcolor{dh-pink!25}"
    )

    tex_path.write_text(content, encoding="utf-8")
    rprint("Post-processed .tex with brand rules, dhquotes, and table styling", "ok")


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

    # Split body by chapter markers using finditer to avoid empty parts
    chapter_pattern = re.compile(r'((?:\\hypertarget\{[^}]*\}\{%\s*\n)?\s*\\chapter\{[^}]*\})')
    matches = list(chapter_pattern.finditer(body))

    if not matches:
        rprint("Cannot split: no chapter markers found in body", "warn")
        return tex_path

    pre_chapter_content = body[:matches[0].start()]
    chapters = []
    for idx, m in enumerate(matches):
        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        chapters.append(body[start:end])

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
        xelatex_args = ["xelatex", "-interaction=nonstopmode", "-halt-on-error"]
        if str(work_dir) != str(tex_dir):
            xelatex_args.extend(["-output-directory", str(work_dir)])
        xelatex_args.append(tex_file)
        result = subprocess.run(
            xelatex_args,
            cwd=str(tex_dir),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        stdout_text = result.stdout or ""
        stderr_text = result.stderr or ""

        # Check for fatal errors via returncode and PDF existence
        if result.returncode != 0:
            pdf_name = Path(tex_file).with_suffix(".pdf").name
            generated_in_pass = work_dir / pdf_name
            if not generated_in_pass.exists():
                rprint(f"XeLaTeX pass {p} failed (returncode={result.returncode}) and no PDF produced", "err")
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
                    log_lines = (stdout_text + stderr_text).split("\n")
                    for line in log_lines[-30:]:
                        if line.strip():
                            print(f"    {line.strip()}")
            else:
                log_lines = (stdout_text + stderr_text).split("\n")
                for line in log_lines[-30:]:
                    if line.strip():
                        print(f"    {line.strip()}")
            return False

        # Check for unresolved references (only warn on final pass)
        if "LaTeX Warning: Reference" in stdout_text:
            rprint(f"Pass {p}: unresolved references remain (expected if not final pass)", "warn")

        if "LaTeX Warning: Rerun" in stdout_text or "Rerun to get" in stdout_text:
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
        try:
            split_result = split_tex_into_chapters(tex_path, chapter_count, output_dir / "tex")
            if split_result and str(split_result) != str(tex_path):
                work_dir = output_dir / "tex"
                tex_path = split_result
        except Exception as e:
            rprint(f"Split failed (continuing with single file): {e}", "warn")

    # Step 3: Compile with XeLaTeX (3 passes for full TOC + labels)
    rprint(f"Compiling PDF (3-pass XeLaTeX)...", "step")
    success = run_xelatex(tex_path, work_dir, passes=3)

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
        title = sys.argv[4] if len(sys.argv) > 4 else "四倍做多认知，长期做多人生"
        author = sys.argv[5] if len(sys.argv) > 5 else "花花 | @BerryUIKI"
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

        # Copy Chart images from book assets to output directory
        book_chart_src = WORKSPACE_ROOT / "articles" / "2026-quadruple-long-life" / "analysis" / "output"
        if book_chart_src.exists():
            chart_dest = merged_path.parent
            for img in book_chart_src.glob("*.png"):
                shutil.copy2(img, chart_dest / img.name)
            rprint(f"Chart images copied from {book_chart_src}", "ok")

        # Ensure Source Han fonts (download if missing)
        ensure_fonts()

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
        title = sys.argv[4] if len(sys.argv) > 4 else "四倍做多认知，长期做多人生"
        author = sys.argv[5] if len(sys.argv) > 5 else "花花 | @BerryUIKI"
        date = sys.argv[6] if len(sys.argv) > 6 else None

        idx_content = Path(index_file).read_text(encoding="utf-8")
        entries = parse_index(idx_content)

        merged_path = WORKSPACE_ROOT / "output" / "_merged.md"
        merged_path.parent.mkdir(parents=True, exist_ok=True)
        merged_path, chapter_count = merge_markdown(entries, merged_path)

        # Copy Chart images from book assets to output directory
        book_chart_src = WORKSPACE_ROOT / "articles" / "2026-quadruple-long-life" / "analysis" / "output"
        if book_chart_src.exists():
            chart_dest = merged_path.parent
            for img in book_chart_src.glob("*.png"):
                shutil.copy2(img, chart_dest / img.name)
            rprint(f"Chart images copied from {book_chart_src}", "ok")

        # Ensure Source Han fonts (download if missing)
        ensure_fonts()

        template = TEMPLATE_DIR / "pandoc-template.tex"
        output_path = Path(output_tex)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tex_path = generate_tex(template, merged_path, output_path, title, author, date)

        # Split if needed
        if should_split(merged_path, chapter_count):
            work_dir = output_path.parent / "tex"
            try:
                split_result = split_tex_into_chapters(tex_path, chapter_count, work_dir)
                if split_result and str(split_result) != str(tex_path):
                    tex_path = split_result
            except Exception as e:
                rprint(f"Split failed (continuing with single file): {e}", "warn")

        print(f"\nTEX_PATH:{tex_path}")

    else:
        rprint(f"Unknown command: {command}", "err")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
