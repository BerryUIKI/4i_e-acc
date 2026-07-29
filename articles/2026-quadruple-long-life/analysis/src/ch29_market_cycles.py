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
import matplotlib.pyplot as plt
import numpy as np
from _style import C_NAVY, C_RED, C_GREEN, C_BLUE, C_ORANGE, C_CREAM, C_GRAY, save_chart

# ── Left: Market cycles ──
cycles = ["2007-2008\n熊市", "2009-2014\n慢牛", "2015\n疯牛+股灾",
          "2016-2017\n慢牛", "2018\n熊市", "2019-2020\n牛市",
          "2021\n震荡", "2022\n熊市", "2023-2024\n修复"]
csi300_chg = [-72, 155, 15, 28, -25, 65, -5, -22, 18]
colors_cycle = [C_GREEN if v < 0 else C_RED for v in csi300_chg]

# ── Right: Missing best days ──
scenarios = ["完整持有\n（252天/年）", "错过最好的\n5个交易日", "错过最好的\n10个交易日",
             "错过最好的\n20个交易日", "错过最好的\n30个交易日"]
annual_return = [9.8, 7.1, 5.2, 2.8, 0.9]
colors_miss = [C_BLUE, C_ORANGE, C_ORANGE, C_RED, C_RED]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5))
fig.patch.set_facecolor(C_CREAM)

# Left subplot
ax1.set_facecolor(C_CREAM)
bars = ax1.barh(cycles, csi300_chg, color=colors_cycle, edgecolor="white", height=0.7)
for bar, val in zip(bars, csi300_chg):
    offset = 2 if val > 0 else -6
    ax1.text(bar.get_width() + offset, bar.get_y() + bar.get_height()/2,
             f"{val:+d}%", va="center", fontsize=10, fontweight="bold", color=C_NAVY)
ax1.axvline(x=0, color=C_GRAY, linewidth=0.5)
ax1.set_title("沪深300 牛熊周期", fontsize=12, fontweight="bold", color=C_NAVY)
ax1.invert_yaxis()
ax1.grid(axis="x", alpha=0.2)

# Right subplot
ax2.set_facecolor(C_CREAM)
bars2 = ax2.bar(scenarios, annual_return, color=colors_miss, edgecolor="white", width=0.6)
for bar, val in zip(bars2, annual_return):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.12,
             f"{val}%", ha="center", fontsize=10, fontweight="bold", color=C_NAVY)
ax2.set_title("错过最佳交易日的代价\n（标普500，2005-2025年化回报）",
             fontsize=12, fontweight="bold", color=C_NAVY)
ax2.set_ylabel("年化回报 (%)")
ax2.set_xticklabels(scenarios, rotation=15, ha="right", fontsize=9)
ax2.grid(axis="y", alpha=0.2)

fig.suptitle("市场周期 + 错过最佳交易日的代价", fontsize=14, fontweight="bold", color=C_NAVY, y=1.01)
plt.tight_layout()
save_chart(fig, "ch29_market_cycles.png")
