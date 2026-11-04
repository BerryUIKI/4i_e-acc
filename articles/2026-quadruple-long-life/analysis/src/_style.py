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
# Ordered by preference; the first one that is really installed AND has a
# usable normal-weight face wins.
FONT_CANDIDATES = [
    "Source Han Sans SC", "Noto Sans CJK SC", "Microsoft YaHei",
    "PingFang SC", "WenQuanYi Micro Hei", "Arial Unicode MS", "SimHei",
]

# Never use these, even though they are installed and report CJK coverage.
# MingLiU and JhengHei are Traditional Chinese: they render simplified text
# with visibly wrong glyphs. SimSun/NSimSun cover SimSun's *own* simplified
# set but ship no bold face, which matters for titles.
FONT_DENY = ("mingliu", "jhenghei", "pmingliu", "sun-ext", "songti", "fangsong", "kaiti")


def _usable_face(name):
    """True when `name` is installed with a regular-weight face that renders.

    findfont() is not enough on its own. A variable font can be present and
    found, then fail at draw time with "Failed to find font weight normal",
    which silently drops the whole figure to matplotlib's default. Noto Sans SC
    (a variable font) does exactly that on this machine, so each candidate is
    checked against the face table for a real regular-weight entry.
    """
    low = name.lower()
    if any(bad in low for bad in FONT_DENY):
        return False
    for face in fm.fontManager.ttflist:
        if face.name.lower() != low:
            continue
        weight = str(face.weight).lower()
        if weight in ("normal", "regular", "400"):
            return True
    return False


CJK_FONT = next((n for n in FONT_CANDIDATES if _usable_face(n)), None)

if CJK_FONT is None:
    raise RuntimeError(
        "No usable CJK font found. Install one of: " + ", ".join(FONT_CANDIDATES)
    )

# Font setup. The fragile part is matplotlib's fallback chain: when a glyph is
# not found it walks font.sans-serif and can land on MingLiU-ExtB (a Traditional
# Chinese font with an incomplete simplified set) or Microsoft JhengHei,
# producing tofu for common characters. That showed up only on some multi-panel
# figures, which is why it went unnoticed at first.
#
# Fix: family is the generic "sans-serif" and font.sans-serif is a SINGLE-entry
# list naming our font. With one entry there is nothing to fall back to, so
# matplotlib either uses YaHei or reports a genuine miss — it cannot silently
# switch to another East Asian font whose coverage differs.
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [CJK_FONT]
plt.rcParams["font.serif"] = [CJK_FONT]
plt.rcParams["font.monospace"] = [CJK_FONT]
plt.rcParams["axes.unicode_minus"] = False

# ── Color palette ───────────────────────────────────
# Retuned for print (B5, 1/150 dpi) and for the sober register the book aims at.
# The original set was built for the web tools: bright saturated red/green and a
# warm cream field. On paper that read as a slide deck rather than a research
# report — the saturation fought the body text and every chart shouted.
#
# This palette keeps the DollarHua identity (blossom pink stays the accent, the
# navy family stays the ink) but drops saturation and lets one restrained accent
# carry emphasis. Semantic meaning is preserved where it matters:
# red still means up/risk, green still means down/safe, per Chinese convention.

# Ink & structure
C_NAVY = "#1B2A4A"       # primary ink; deeper and less purple than #1D1E50
C_NAVY_SOFT = "#3D4F70"  # secondary text, axis labels
C_NAVY_FAINT = "#8A94A6" # gridlines, tertiary labels
C_SLATE = "#5B6577"      # neutral series

# Semantic pair — muted so they sit inside a document, not on a poster
C_RED = "#B5464C"        # up / risk / cost  (deeper than #E85D61)
C_GREEN = "#4A7C59"      # down / safe       (desaturated forest)

# Accents
C_PINK = "#E8A0A8"       # blossom accent (dimmer than #FEC6CD)
C_BRONZE = "#9C6B47"     # warm highlight    (earthy, not orange)
C_ORANGE = C_BRONZE      # legacy alias
C_BLUE = "#2F4A78"       # cool series partner to C_RED
C_GRAY = "#9AA0AA"

# Fields
C_CREAM = "#FBFAF7"      # page field: near-white, faintly warm
C_FIELD = "#F2F0EB"      # chart panel fill, one step off the page
C_RULE = "#D8D5CE"       # hairline rules and baseline

# Sequential stops for multi-series charts (low → high emphasis)
C_SEQ = ["#1B2A4A", "#2F4A78", "#5B7BA6", "#8FA8C4", "#C3D0DE"]

# ── Typographic scale for charts ────────────────────
# Sized for B5 at 150 dpi: a chart occupies ~11.5cm, so 9-10pt type lands near
# the body text's optical weight instead of looking like an embedded screenshot.
plt.rcParams.update({
    "figure.facecolor": C_CREAM,
    "axes.facecolor": C_CREAM,
    "savefig.facecolor": C_CREAM,
    "axes.edgecolor": C_NAVY_FAINT,
    "axes.linewidth": 0.8,
    "axes.labelcolor": C_NAVY_SOFT,
    "axes.labelsize": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.titlecolor": C_NAVY,
    "axes.titlepad": 12,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": C_RULE,
    "grid.linewidth": 0.6,
    "grid.alpha": 1.0,
    "xtick.color": C_NAVY_SOFT,
    "ytick.color": C_NAVY_SOFT,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "legend.frameon": False,
    "legend.fontsize": 9,
    "font.size": 10,
    "figure.autolayout": False,
})


def style_axes(ax, *, grid_axis="y", spines=("left", "bottom")):
    """Apply the house chart style to an Axes.

    Strips the box down to the two spines that carry information, keeps a single
    grid direction so the eye reads values without crossing lines, and keeps
    tick marks short and outward so they do not intrude on the plot area.
    """
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in spines)
    for side in spines:
        ax.spines[side].set_color(C_RULE)
        ax.spines[side].set_linewidth(0.8)
    ax.grid(False)
    if grid_axis:
        ax.grid(True, axis=grid_axis, color=C_RULE, linewidth=0.6)
    ax.tick_params(length=3, width=0.7, pad=4)
    return ax


# ── Two matplotlib traps found while rebuilding these charts ──
#
# 1. Font. msyh.ttc ships regular and light faces only — there is NO bold face.
#    Asking for fontweight="bold" makes matplotlib synthesise a bold variant,
#    and some glyphs (observed: ¥ U+00A5) come out as tofu boxes in the
#    synthesised variant while rendering fine at regular weight.
#
# 2. Layout. Always finish with fig.tight_layout(), never fig.subplots_adjust().
#    Called before savefig, subplots_adjust reproducibly turned every CJK string
#    in the figure into tofu boxes while leaving Latin text intact. tight_layout
#    has no such effect on the same figure.
#
# Prefer emphasis via size or colour rather than weight for any string holding
# currency or symbol characters.

# ── Output helpers ──────────────────────────────────
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# B5 text block is 115mm wide. Charts are authored at that width so they land
# at 1:1 on the page instead of being scaled down (which blurs labels) or
# scaled up (which fattens strokes). Figures are 4:3 unless a chart needs a
# different proportion — pass figsize to override.
B5_TEXT_WIDTH_IN = 115 / 25.4      # ≈ 4.53in
DEFAULT_FIGSIZE = (B5_TEXT_WIDTH_IN, B5_TEXT_WIDTH_IN * 0.62)


def figure(width_in=B5_TEXT_WIDTH_IN, height_in=None, ratio=0.62,
           nrows=1, ncols=1, **subplot_kw):
    """Create a figure sized for the B5 text block.

    ratio is height/width; 0.62 ≈ 8:5, which suits bar and line charts in a
    portrait page without forcing a full-page figure. For multi-panel charts
    pass nrows/ncols and a larger ratio (≈1.05 for two stacked panels).

    Returns (fig, ax) when there is one panel, (fig, axes_array) otherwise.
    Panels are created with squeeze=False so a 1×N or N×1 grid always comes
    back as an indexable array rather than a bare Axes.
    """
    h = height_in if height_in is not None else width_in * ratio
    fig, axes = plt.subplots(
        nrows, ncols, figsize=(width_in, h), squeeze=False, **subplot_kw
    )
    fig.patch.set_facecolor(C_CREAM)
    for row in axes:
        for ax in row:
            ax.set_facecolor(C_CREAM)
    if nrows == 1 and ncols == 1:
        return fig, axes[0][0]
    return fig, axes.ravel()


def save_chart(fig, name):
    """Save figure to output/ with print-appropriate settings.

    200 dpi (not 150) because the figure is authored at final size: at 1:1 on a
    B5 page, 150 dpi leaves visible stair-stepping on thin axis rules.
    bbox_inches uses a small pad so long labels are not clipped at the edge.
    """
    path = OUTPUT_DIR / name
    fig.savefig(
        str(path),
        dpi=200,
        bbox_inches="tight",
        pad_inches=0.08,
        facecolor=C_CREAM,
    )
    plt.close(fig)
    print(f"  Saved: {path}")
    return path
