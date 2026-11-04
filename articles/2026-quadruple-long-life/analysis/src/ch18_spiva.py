"""
Ch18 — SPIVA 主动基金 vs 被动指数基金（2024 年终）
不同市场、不同周期下，主动基金跑输指数的比例。

数据来源：S&P SPIVA Scorecard（年度报告，免费公开）
  获取：https://www.spglobal.com/spdji/en/research-insights/spiva/
        → 下载最新 PDF 报告 → 提取各分类「跑输基准的主动基金占比」
  更新方法：修改 categories / underperform 数组为最新报告数据
"""
from matplotlib.patches import Patch
from _style import (
    C_NAVY, C_NAVY_SOFT, C_RED, C_BLUE, C_GRAY, C_RULE, C_CREAM,
    figure, save_chart, style_axes,
)

categories = [
    "美股大盘 1 年", "美股大盘 5 年", "美股大盘 10 年",
    "美股中盘 5 年", "美股小盘 5 年",
    "新兴市场 5 年", "国际股票 5 年",
    "A股主动 1 年", "A股主动 3 年", "A股主动 5 年",
]
underperform = [51, 75, 87, 58, 62, 84, 65, 42, 55, 68]  # % underperform

# Three tiers rather than a continuous ramp: the argument is qualitative —
# the longer the horizon, the worse active management does.
colors = [C_RED if v >= 70 else C_BLUE if v >= 60 else C_GRAY for v in underperform]

fig, ax = figure(ratio=1.00)
style_axes(ax, grid_axis="x")

bars = ax.barh(categories, underperform, color=colors, height=0.62, zorder=3)

# 50% is the point where active merely matches the coin flip; it is the only
# reference line the chart needs.
ax.axvline(x=50, color=C_RULE, linewidth=1, linestyle=(0, (4, 3)), zorder=2)
ax.annotate(
    "50% 分界", xy=(50, 1), xycoords=("data", "axes fraction"),
    xytext=(1.5, -0.075), textcoords="offset points",
    fontsize=8, color=C_NAVY_SOFT, ha="left", va="top",
)

for bar, val in zip(bars, underperform):
    ax.annotate(
        f"{val}%", (bar.get_width(), bar.get_y() + bar.get_height() / 2),
        textcoords="offset points", xytext=(4, 0),
        va="center", fontsize=9, color=C_NAVY,
    )

ax.set_title("主动基金跑输指数的比例（SPIVA 数据）", loc="left")
ax.set_xlabel("跑输基准的主动基金占比 (%)")
# Headroom past 100 so the longest bar's "87%" label lands outside the plot
# instead of being clipped by the axis edge.
ax.set_xlim(0, 112)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0, pad=6)

legend_elements = [
    Patch(facecolor=C_RED, label="70% 以上"),
    Patch(facecolor=C_BLUE, label="60–69%"),
    Patch(facecolor=C_GRAY, label="60% 以下"),
]
# Legend goes in the lower right, which is empty because only the bottom three
# rows reach that far right and none of them do. framealpha is explicit: at the
# default the legend is drawn on the cream field but the bars behind it show
# through the last row's value label.
ax.legend(handles=legend_elements, loc="lower right", frameon=True,
          facecolor=C_CREAM, edgecolor="none", framealpha=1.0,
          fontsize=8.5, handlelength=1.1, title=None,
          bbox_to_anchor=(1.0, 0.02))

fig.tight_layout()
save_chart(fig, "ch18_spiva.png")
