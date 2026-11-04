"""
Ch29 — 市场周期与「错过最佳交易日」的代价
沪深300 牛熊周期 + 错过标普500 最佳 N 个交易日的年化回报差异。

数据来源：Bloomberg 终端历史数据
  获取方式：
    - 牛熊周期：终端导出沪深300 年度涨跌 → 按市场事件划分周期
    - 错过最佳交易日：终端导出标普500 日收益 → 剔除最高 N 天 → 计算剩余年化
    - Python 替代：使用 yfinance 拉取 ^GSPC / 000300.SS 日线 →
      按日期排序 → 剔除 top N → 计算 CAGR
  更新方法：
    - cycles / csi300_chg：追加最新周期数据
    - scenarios / annual_return：重新计算最新区间数据
"""
import numpy as np
from _style import C_NAVY, C_NAVY_SOFT, C_RED, C_GREEN, C_BLUE, C_BRONZE, C_GRAY, C_RULE, figure, save_chart, style_axes

# ── Panel A: market cycles ──
cycles = ["2007–08 熊市", "2009–14 慢牛", "2015 疯牛+股灾", "2016–17 慢牛",
          "2018 熊市", "2019–20 牛市", "2021 震荡", "2022 熊市", "2023–24 修复"]
csi300_chg = [-72, 155, 15, 28, -25, 65, -5, -22, 18]
colors_cycle = [C_GREEN if v < 0 else C_RED for v in csi300_chg]

# ── Panel B: missing the best days ──
scenarios = ["完整持有", "错过 5 天", "错过 10 天", "错过 20 天", "错过 30 天"]
annual_return = [9.8, 7.1, 5.2, 2.8, 0.9]

# Stacked: two side-by-side panels at B5 width leave ~5.7cm each, which cannot
# hold nine two-line cycle labels or five scenario labels without overlap.
fig, axes = figure(ratio=1.16, nrows=2, ncols=1)
ax1, ax2 = axes

# Panel A: horizontal bars make the long cycle labels readable.
style_axes(ax1, grid_axis="x")
bars = ax1.barh(cycles, csi300_chg, color=colors_cycle, height=0.62, zorder=3)
ax1.axvline(x=0, color=C_RULE, linewidth=0.9, zorder=2)

for bar, val in zip(bars, csi300_chg):
    x = bar.get_width()
    ax1.annotate(
        f"{val:+d}%", (x, bar.get_y() + bar.get_height() / 2),
        textcoords="offset points", xytext=(5 if val > 0 else -5, 0),
        ha="left" if val > 0 else "right", va="center",
        fontsize=8.5, color=C_NAVY,
    )

ax1.set_title("沪深300 牛熊周期（区间涨跌幅）", loc="left")
ax1.invert_yaxis()
ax1.tick_params(axis="y", length=0, pad=6)
# Headroom on the left so the "-72%" label on the widest negative bar stays
# inside the axes. At -95 the label ran up against the axis edge and read as
# part of the "2007–08 熊市" tick label.
ax1.set_xlim(-130, 185)

# Panel B: a monotonic decay — colour darkens as the outcome worsens.
style_axes(ax2, grid_axis="y")
shade = [C_BLUE, C_BRONZE, C_BRONZE, C_RED, C_RED]
bars2 = ax2.bar(scenarios, annual_return, color=shade, width=0.56, zorder=3)

for bar, val in zip(bars2, annual_return):
    ax2.annotate(
        f"{val}%", (bar.get_x() + bar.get_width() / 2, val),
        textcoords="offset points", xytext=(0, 4),
        ha="center", fontsize=8.5, color=C_NAVY,
    )

ax2.set_title("错过最佳交易日的代价（标普500，2005–2025 年化）", loc="left")
ax2.set_ylabel("年化回报 (%)")
ax2.tick_params(axis="x", length=0)
# Five two-word labels ("错过 5 天") at B5 width do not fit on one line; rotate
# them rather than shrinking the type below the axis-label size.
ax2.set_xticks(range(len(scenarios)))
ax2.set_xticklabels(scenarios, rotation=30, ha="right", rotation_mode="anchor")
ax2.set_ylim(0, 11.6)

fig.tight_layout(h_pad=1.5)
save_chart(fig, "ch29_market_cycles.png")
