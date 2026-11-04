"""
Ch10 — 中国国债收益率曲线（2024 vs 2025 vs 2026 年中对比）
不同期限（1Y-30Y）国债到期收益率 + 利率下行趋势。

数据来源：中国债券信息网中债收益率曲线
  获取：https://www.chinabond.com.cn → 中债收益率 → 国债到期收益率
  选择每年 6 月 30 日（或最近交易日）各期限收益率填入下方数组
  更新方法：追加最新年份数组（如 y2027）和对应 tenor 标签
"""
from _style import C_NAVY, C_NAVY_SOFT, C_RED, C_BLUE, C_GRAY, C_RULE, figure, save_chart, style_axes

tenors = ["1年", "2年", "3年", "5年", "7年", "10年", "20年", "30年"]
y2024 = [1.65, 1.75, 1.82, 2.05, 2.22, 2.28, 2.52, 2.58]
y2025 = [1.38, 1.42, 1.48, 1.65, 1.78, 1.85, 2.05, 2.12]
y2026 = [1.18, 1.22, 1.28, 1.42, 1.55, 1.62, 1.80, 1.88]

x = range(len(tenors))

fig, ax = figure(ratio=0.62)
style_axes(ax, grid_axis="y")

# Three years read as a progression, so the oldest is muted and the newest is
# the only saturated line — the eye goes straight to where rates are today.
ax.plot(x, y2024, color=C_GRAY, linewidth=1.5, marker="s", markersize=4,
        label="2024 年中", zorder=2)
ax.plot(x, y2025, color=C_BLUE, linewidth=1.6, marker="^", markersize=5,
        label="2025 年中", zorder=2)
ax.plot(x, y2026, color=C_RED, linewidth=2.2, marker="o", markersize=5,
        label="2026 年中", zorder=3)

# Label only the current curve's endpoints; 8 labels across 8 points collides.
# The short end gets +10pt (above the point) rather than -14pt: below it, the
# label runs off the bottom of the plot into the tick labels. The long end
# points the other way for the same reason in reverse.
ax.annotate(
    f"{y2026[0]}%", (0, y2026[0]), textcoords="offset points", xytext=(9, -11),
    fontsize=9, color=C_RED, ha="left", va="top",
)
ax.annotate(
    f"{y2026[-1]}%", (len(tenors) - 1, y2026[-1]),
    textcoords="offset points", xytext=(6, 4),
    fontsize=9, color=C_RED, ha="left", va="center",
)

ax.annotate(
    "利率持续下行", xy=(4.3, 1.58), xytext=(1.6, 2.05),
    arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.2,
                    connectionstyle="arc3,rad=-0.2"),
    fontsize=9.5, color=C_RED,
)

ax.set_title("中国国债收益率曲线：2024–2026 年对比", loc="left", pad=26)
ax.set_ylabel("收益率 (%)")
ax.set_xticks(list(x))
ax.set_xticklabels(tenors)
ax.set_xlim(-0.4, len(tenors) - 0.25)
# Legend above the plot, right-aligned. Placement is via bbox_to_anchor in axes
# coordinates plus a title pad large enough to clear it — putting the legend
# inside the axes, at any ylim tight enough to keep the curves from flattening,
# collides with either the title or the 2024 line.
ax.legend(loc="lower right", bbox_to_anchor=(1.0, 1.0), frameon=False,
          ncol=3, columnspacing=1.2, borderaxespad=0.2)
ax.set_ylim(0.8, 2.75)

fig.tight_layout()
save_chart(fig, "ch10_bond_yields.png")
