"""
Ch7 — 亏损与回本对照表
跌幅越大，需要的涨幅越大才能回本。

数据来源：纯数学计算
  公式：回本所需涨幅 = 1/(1 - 跌幅) - 1
  无需外部数据源，仅改动 loss_pcts 列表可调整展示范围
"""
from _style import (
    C_RED, C_GREEN, C_NAVY, C_NAVY_SOFT, C_RULE, C_CREAM,
    figure, save_chart, style_axes,
)

loss_pcts = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70]
gain_needed = [round(100/(100-p) - 1, 4)*100 for p in loss_pcts]

fig, ax = figure(ratio=0.66)
style_axes(ax, grid_axis="x")

# Colour carries the message: losses recoverable within one doubling stay green,
# beyond that they turn red. The 100% line is the boundary between the two.
colors = [C_GREEN if g <= 100 else C_RED for g in gain_needed]
bars = ax.barh(
    [f"-{p}%" for p in loss_pcts], gain_needed,
    color=colors, height=0.62, zorder=3,
)

for bar, val in zip(bars, gain_needed):
    ax.text(
        bar.get_width() + 2.5, bar.get_y() + bar.get_height() / 2,
        f"+{val:.1f}%", va="center", ha="left",
        fontsize=9, fontweight="bold", color=C_NAVY,
    )

# Reference line: the "must double" threshold. Placed at the TOP of the plot,
# in the empty space above the first bar — below the bars it sat on top of the
# -70% row and was unreadable against the red fill.
ax.axvline(x=100, color=C_RULE, linestyle=(0, (4, 3)), linewidth=1, zorder=2)
# Inside the axes (y=0.98, va="top"), not on the boundary: at y=1.0 the text
# rides up into the title. The cream box masks the gridline it sits on.
ax.annotate(
    "需翻倍", xy=(100, 1), xycoords=("data", "axes fraction"),
    xytext=(103, 0.985), textcoords=("data", "axes fraction"),
    fontsize=8.5, color=C_NAVY_SOFT, ha="left", va="top", zorder=4,
    bbox=dict(boxstyle="square,pad=0.15", fc=C_CREAM, ec="none"),
)

ax.set_title("亏损越多，回本越难", loc="left")
ax.set_xlabel("回本所需涨幅 (%)")
ax.set_xlim(0, max(gain_needed) * 1.20)   # headroom so the last label is not clipped
ax.invert_yaxis()
ax.tick_params(axis="y", length=0, pad=6)

fig.tight_layout()
save_chart(fig, "ch07_drawdowns.png")
