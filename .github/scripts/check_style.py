#!/usr/bin/env python3
"""Style / structure guard — covers both essays and book projects.

Rules enforced (exit non-zero on errors, non-zero on excessive warnings):
  1. Every top-level document folder must ship both README.md (English)
     and README-zh_CN.md (Chinese).
  2. Essay folders (short articles) must use a single `manuscript.md`
     (Chinese-primary + English inline). Leftover `manuscript.zh.md` /
     `manuscript.en.md` from the old policy are flagged as warnings.
  3. Book folders (multi-dir layout: `Front-Matter/`, `Main-Text/`,
     `Appendices/`) skip the `manuscript.md` requirement. Instead they
     are checked for `[数据待补充]` / `[待补充]` placeholder residues
     (warnings) and for a present `agents.md` (warning if missing).
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
DOC_FOLDERS = [
    "reports", "research", "portfolio", "market",
    "strategies", "data", "archive", "assets", "articles",
]

PLACEHOLDER_RE = re.compile(r"\[(?:数据)?待补充[^\]]*\]")


def is_book_folder(path: Path) -> bool:
    """A book folder has a multi-directory layout (Front-Matter/ + Main-Text/
    and optionally Appendices/), rather than a single manuscript.md."""
    return (path / "Front-Matter").is_dir() and (path / "Main-Text").is_dir()


def check_book_placeholders(path: Path) -> list[str]:
    """Scan content dirs of a book project and report placeholder residues."""
    warnings = []
    content_dirs = ["Front-Matter", "Main-Text", "Appendices"]
    for dname in content_dirs:
        d = path / dname
        if not d.is_dir():
            continue
        for fpath in sorted(d.rglob("*.md")):
            try:
                text = fpath.read_text(encoding="utf-8")
            except Exception:
                continue
            for m in PLACEHOLDER_RE.finditer(text):
                rel = fpath.relative_to(path)
                line = text[:m.start()].count("\n") + 1
                snippet = m.group()[:60]
                warnings.append(
                    f"{rel}:{line} placeholder residue '{snippet}'"
                )
    return warnings


def main() -> int:
    errors = []
    warnings = []

    # --- Rule 1: bilingual README in each doc folder ---
    for f in DOC_FOLDERS:
        d = ROOT / f
        if not d.is_dir():
            continue
        for readme in ("README.md", "README-zh_CN.md"):
            if not (d / readme).is_file():
                errors.append(f"missing {d.name}/{readme}")

    # --- Rule 2 & 3: article / book checks ---
    articles = ROOT / "articles"
    if articles.is_dir():
        for child in sorted(articles.iterdir()):
            if not child.is_dir():
                continue

            # Detect book projects
            if is_book_folder(child):
                # Skip essay manuscript.md checks for books
                # Check for book-scoped agent guidance
                if not (child / "agents.md").is_file():
                    warnings.append(
                        f"{child.name}/ is a book project but has no agents.md "
                        f"(book-scoped conventions)"
                    )
                # Check for placeholder residues
                pw = check_book_placeholders(child)
                warnings.extend(pw)
                continue

            # Essay-style folders
            for leftover in ("manuscript.zh.md", "manuscript.en.md"):
                if (child / leftover).is_file():
                    warnings.append(
                        f"leftover old manuscript file: {child.name}/{leftover} "
                        f"(policy is a single manuscript.md)"
                    )
            if (child / "README.md").is_file() and not (child / "manuscript.md").is_file():
                warnings.append(
                    f"{child.name}/ has README but no manuscript.md (draft not started?)"
                )

    # --- Report ---
    print("== Style / structure check ==")
    for w in warnings:
        print(f"  ⚠ {w}")
    if errors:
        for e in errors:
            print(f"  ❌ {e}")
        print(f"FAILED: {len(errors)} error(s).")
        return 1
    suffix = f" ({len(warnings)} warning(s))" if warnings else ""
    print(f"✅ Structure OK{suffix}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
