"""
Shared matplotlib style for 2026-quadruple-long-life charts.
CJK font discovery + consistent color palette + output helpers.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path
import os

# ── CJK font discovery ──────────────────────────────
FONT_CANDIDATES = [
    "Noto Sans CJK SC", "Microsoft YaHei", "SimHei",
    "PingFang SC", "WenQuanYi Micro Hei", "Source Han Sans SC",
    "Noto Sans SC", "Arial Unicode MS",
]
CJK_FONT = None

for fname in FONT_CANDIDATES:
    try:
        fp = fm.findfont(fname, fallback_to_default=False)
        if fp and fp != fm.findfont("sans-serif", fallback_to_default=False):
            CJK_FONT = fname
            break
    except Exception:
        continue

if CJK_FONT is None:
    # Fallback: scan system fonts for any CJK
    for fp in fm.findSystemFonts():
        try:
            prop = fm.FontProperties(fname=fp)
            if any(kw in prop.get_name().lower() for kw in ["cjk", "hei", "song", "ming", "yahei", "noto sans"]):
                CJK_FONT = prop.get_name()
                break
        except Exception:
            pass

if CJK_FONT is None:
    CJK_FONT = "sans-serif"
    print("WARNING: No CJK font found, Chinese text may not render correctly.")

plt.rcParams["font.family"] = CJK_FONT
plt.rcParams["font.sans-serif"] = [CJK_FONT]
plt.rcParams["axes.unicode_minus"] = False

# ── Color palette ───────────────────────────────────
# Chinese stock convention: red = up, green = down
C_RED = "#E85D61"        # Red (涨)
C_GREEN = "#4CAF50"      # Green (跌)
C_BLUE = "#3F51B5"       # Blue
C_ORANGE = "#E3A04B"     # Warm orange
C_NAVY = "#1D1E50"       # Navy
C_PINK = "#FEC6CD"       # Light pink
C_GRAY = "#9E9E9E"       # Neutral gray
C_BRONZE = "#B86C40"     # Bronze
C_CREAM = "#FBF7F0"      # Background cream

# ── Output helpers ──────────────────────────────────
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_chart(fig, name):
    """Save figure to output/ with consistent settings."""
    path = OUTPUT_DIR / name
    fig.savefig(str(path), dpi=150, bbox_inches="tight", facecolor=C_CREAM)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path
