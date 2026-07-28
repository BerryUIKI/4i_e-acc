#!/bin/bash
#===========================================================
#  install_deps.sh — PDF Toolbook Dependency Checker
#  Version: v1.0 · Updated: 2026-07-28
#===========================================================

set -e

echo "🔍 Checking PDF toolbook dependencies..."

MISSING=()

# Check xelatex
if command -v xelatex &>/dev/null; then
    echo "  ✅ xelatex: $(xelatex --version 2>&1 | head -1)"
else
    echo "  ❌ xelatex: not installed"
    MISSING+=("xelatex")
fi

# Check pandoc
if command -v pandoc &>/dev/null; then
    echo "  ✅ pandoc: $(pandoc --version | head -1)"
else
    echo "  ❌ pandoc: not installed"
    MISSING+=("pandoc")
fi

echo ""

if [ ${#MISSING[@]} -eq 0 ]; then
    echo "✅ All dependencies ready. PDF generation can proceed!"
    exit 0
fi

echo "⚠️  Missing dependencies: ${MISSING[*]}"
echo ""
echo "Install options:"
echo "  A) Manual install — show me the commands"
echo "  B) Auto-install via brew"
echo "  C) Skip install, generate .tex source only"
echo ""
echo "Notes:"
echo "  - BasicTeX (~200MB) or MacTeX (~2GB) required for xelatex"
echo "  - Pandoc (~100MB) via brew install pandoc"
echo "  - Both install with: brew install --cask basictex && brew install pandoc"
echo "  - After installing BasicTeX, you may need:"
echo "      sudo tlmgr update --self"
echo "      sudo tlmgr install ctex collection-langchinese"

exit 1
