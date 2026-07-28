#!/usr/bin/env python3
"""Style / structure guard derived from articles/STYLE.md conventions.

Rules enforced (exit non-zero on violations):
  1. Every top-level document folder must ship both README.md (English)
     and README-zh_CN.md (中文).
  2. Article folders must use a single `manuscript.md` (Chinese-primary +
     English inline). Leftover `manuscript.zh.md` / `manuscript.en.md`
     from the old policy are flagged as warnings.
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
DOC_FOLDERS = [
    "reports", "research", "portfolio", "market",
    "strategies", "data", "archive", "assets", "articles",
]


def main() -> int:
    errors = []
    warnings = []

    for f in DOC_FOLDERS:
        d = ROOT / f
        if not d.is_dir():
            continue
        for readme in ("README.md", "README-zh_CN.md"):
            if not (d / readme).is_file():
                errors.append(f"missing {d.name}/{readme}")

    articles = ROOT / "articles"
    if articles.is_dir():
        for child in sorted(articles.iterdir()):
            if not child.is_dir():
                continue
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
