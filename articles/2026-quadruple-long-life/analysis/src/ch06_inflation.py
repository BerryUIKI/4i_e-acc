"""
Ch6 — 通胀与中国 CPI 数据（2013-2025）
展示 CPI 同比走势 + 100 元购买力逐年侵蚀。

数据来源：中国国家统计局 CPI 月度数据
  获取方式：https://data.stats.gov.cn → 居民消费价格指数(CPI) → 年度同比
  更新方法：在下方 cpi_yoy 列表中追加最新年份数据即可
"""
from _style import (
    C_RED, C_NAVY, C_NAVY_SOFT, C_GRAY, C_RULE, C_FIELD,
    figure, save_chart, style_axes,
)

# ── Data (2013-2025 CPI YoY %) ─────────────────────
# 来源：国家统计局年度 CPI 同比涨幅
years = list(range(2013, 2026))
cpi_yoy = [2.6, 2.0, 1.4, 2.0, 1.6, 2.1, 2.9, 2.5, 0.9, 2.0, 0.2, 0.3, 0.3]
# 100 yuan purchasing power = 100 / cumulative inflation factor
cumulative = [100.0]
for i, cpi in enumerate(cpi_yoy):
    cumulative.append(round(cumulative[-1] / (1 + cpi/100), 1))
cumulative = cumulative[1:]

# ── Chart ──────────────────────────────────────────────
# Stacked vertically: at B5 width a side-by-side pair leaves each panel only
# ~5.7cm, which crushes the 13 year labels into an unreadable wedge. Stacking
# gives each panel the full measure and reads top-to-bottom as cause -> effect.
fig, axes = figure(ratio=1.05, nrows=2, ncols=1)
ax1, ax2 = axes

# Top: CPI YoY. Bars above the 2% line are the ones eroding purchasing power.
style_axes(ax1, grid_axis="y")
bar_colors = [C_RED if v >= 2 else C_GRAY for v in cpi_yoy]
bars = ax1.bar(years, cpi_yoy, color=bar_colors, width=0.66, zorder=3)
ax1.axhline(y=2.0, color=C_NAVY_SOFT, linestyle=(0, (4, 3)), linewidth=0.9, zorder=2)
ax1.annotate(
    "2% 温和通胀线", xy=(years[-1], 2.0), xytext=(0, 5),
    textcoords="offset points", fontsize=8, color=C_NAVY_SOFT,
    ha="right", va="bottom",
)
ax1.set_title("中国 CPI 同比涨幅（2013–2025）", loc="left")
ax1.set_ylabel("CPI 同比 (%)")
ax1.set_ylim(0, 3.6)
ax1.set_xlim(years[0] - 0.5, years[-1] + 0.5)
ax1.set_xticks(years)
ax1.set_xticklabels([str(y) for y in years], rotation=45, ha="right")
ax1.tick_params(axis="x", length=0)

# Bottom: purchasing power erosion, drawn as the area between 100 and the curve.
style_axes(ax2, grid_axis="y")
ax2.fill_between(years, cumulative, 100, color=C_RED, alpha=0.12, zorder=2)
ax2.plot(years, cumulative, color=C_RED, linewidth=2, zorder=3)
ax2.set_title("100 元的实际购买力", loc="left")
ax2.set_ylabel("相当于 2013 年的金额")
ax2.set_ylim(70, 102)
# Half a year of padding on each side: fill_between closes its area with a
# vertical stub at the first and last x. Flush against the axes limit that stub
# reads as a hard edge cutting the band short, rather than the band simply
# ending at the last data point.
ax2.set_xlim(years[0] - 0.5, years[-1] + 0.5)
ax2.set_xticks(years)
ax2.set_xticklabels([str(y) for y in years], rotation=45, ha="right")
ax2.tick_params(axis="x", length=0)

# Label only first and last to avoid 13 overlapping annotations. The first
# label sits below the curve (the curve descends from the top-left, so there
# is clear space underneath), the last sits above it.
#
# No fontweight="bold" here: msyh.ttc has no bold face, so matplotlib
# synthesises one and the ¥ glyph (U+00A5) comes out as a tofu box in the
# synthesised variant only. Regular weight renders it correctly.
for (y, v), dy in (((years[0], cumulative[0]), -16), ((years[-1], cumulative[-1]), 12)):
    ax2.annotate(
        f"{v:.1f} 元", (y, v), textcoords="offset points", xytext=(0, dy),
        fontsize=9, ha="center", color=C_NAVY,
    )

fig.tight_layout(h_pad=1.6)
save_chart(fig, "ch06_inflation.png")
