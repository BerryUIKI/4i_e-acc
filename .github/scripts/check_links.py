#!/usr/bin/env python3
"""Check internal (relative) markdown links for broken targets.

Walks the repo for every *.md file, extracts markdown links and images,
resolves relative targets against the file's directory, and reports any
target that does not exist on disk. External URLs (http/https/mailto) and
pure #anchors are skipped (no network access).
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
SKIP_DIRS = {".git", ".workbuddy", "node_modules"}

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    broken = []
    checked = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            fp = Path(dirpath) / fn
            try:
                text = fp.read_text(encoding="utf-8")
            except Exception as e:  # pragma: no cover
                print(f"WARN cannot read {fp.relative_to(ROOT)}: {e}")
                continue
            for m in LINK_RE.finditer(text):
                target = m.group(1).strip()
                # Drop query string / fragment for existence check.
                target = target.split("#")[0].split("?")[0]
                if not target:
                    continue
                if target.startswith(("http://", "https://", "mailto:", "tel:")):
                    continue
                if target.startswith("//"):
                    continue
                if target.startswith("/"):
                    resolved = (ROOT / target[1:]).resolve()
                else:
                    resolved = (fp.parent / target).resolve()
                checked += 1
                if not resolved.exists():
                    broken.append((str(fp.relative_to(ROOT)), target))

    if broken:
        print(f"❌ Found {len(broken)} broken internal link(s):")
        for src, tgt in broken:
            print(f"  {src} -> {tgt}")
        return 1
    print(f"✅ No broken internal links ({checked} links checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
