"""
Ch12 — 黄金年度回报 + 危机期间表现（2005-2025）
伦敦金定盘价 USD/oz 年度涨跌幅。

数据来源：
  伦敦金定盘价（LBMA Gold Price）
    获取：https://www.lbma.org.uk → Pricing & Statistics
  替代来源：World Gold Council (https://www.gold.org) 或 Investing.com
  更新方法：在下方 gold_return 列表中追加最新年度涨跌幅
"""
import matplotlib.pyplot as plt
import numpy as np
from _style import C_NAVY, C_RED, C_GREEN, C_ORANGE, C_CREAM, C_GRAY, save_chart

years = list(range(2005, 2026))
gold_return = [18.4, 23.2, 31.9, 4.3, 24.8, 29.5, 9.5, 7.1, -28.3, -1.5,
               -10.7, 8.6, 13.1, -1.6, 18.9, 24.6, -3.5, -0.3, 13.1, 27.1, 26.5]

colors = [C_RED if v > 0 else C_GREEN for v in gold_return]

fig, ax = plt.subplots(figsize=(14, 5))
fig.patch.set_facecolor(C_CREAM)
ax.set_facecolor(C_CREAM)

bars = ax.bar(years, gold_return, color=colors, edgecolor="white")
ax.axhline(y=0, color=C_GRAY, linewidth=0.5)

for bar, val in zip(bars, gold_return):
    offset = 0.5 if val > 0 else -1.5
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + offset,
            f"{val:+.1f}%", ha="center", fontsize=8, color=C_NAVY)

# Highlight crisis years
crisis_years = {2008: "金融危机", 2011: "欧债危机", 2020: "疫情"}
for yr, label in crisis_years.items():
    idx = years.index(yr)
    ax.annotate(label, (yr, gold_return[idx]), textcoords="offset points",
                xytext=(0, 15), fontsize=9, color=C_RED, fontweight="bold",
                ha="center", arrowprops=dict(arrowstyle="->", color=C_RED, lw=1))

ax.set_title("黄金年度回报（2005-2025，伦敦金 USD/oz）", fontsize=14, fontweight="bold", color=C_NAVY)
ax.set_ylabel("年度涨跌幅 (%)")
ax.set_xticks(years[::2])
ax.set_xticklabels(years[::2], rotation=45)
ax.grid(axis="y", alpha=0.2)

plt.tight_layout()
save_chart(fig, "ch12_gold.png")
