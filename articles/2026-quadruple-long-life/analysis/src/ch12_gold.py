"""
Ch12 — 黄金年度回报 + 危机期间表现（2005-2025）
伦敦金定盘价 USD/oz 年度涨跌幅。

数据来源：
  伦敦金定盘价（LBMA Gold Price）
    获取：https://www.lbma.org.uk → Pricing & Statistics
  替代来源：World Gold Council (https://www.gold.org) 或 Investing.com
  更新方法：在下方 gold_return 列表中追加最新年度涨跌幅
"""
from _style import C_NAVY, C_RED, C_GREEN, C_RULE, C_BRONZE, figure, save_chart, style_axes

years = list(range(2005, 2026))
gold_return = [18.4, 23.2, 31.9, 4.3, 24.8, 29.5, 9.5, 7.1, -28.3, -1.5,
               -10.7, 8.6, 13.1, -1.6, 18.9, 24.6, -3.5, -0.3, 13.1, 27.1, 26.5]

colors = [C_RED if v > 0 else C_GREEN for v in gold_return]

fig, ax = figure(ratio=0.60)
style_axes(ax, grid_axis="y")

bars = ax.bar(years, gold_return, color=colors, width=0.68, zorder=3)
ax.axhline(y=0, color=C_RULE, linewidth=0.9, zorder=2)

# Label only the deepest drawdown. The 21 year-to-year values are unreadable as
# text on a 4.5in axis and the bar shape already carries them; the single peak
# label was dropped because it collided with the 金融危机 marker.
#
# Placed to the right of the bar rather than under it: the bar hangs below the
# zero line, so a label underneath lands in the empty lower band where the
# rotated year labels are, and they overprint.
trough_idx = gold_return.index(min(gold_return))
ax.annotate(
    f"{gold_return[trough_idx]:+.1f}%", (years[trough_idx], gold_return[trough_idx]),
    textcoords="offset points", xytext=(9, -4),
    ha="left", va="top", fontsize=8.5, color=C_NAVY,
)

# Crisis markers: the point is that gold held up while equities fell, so these
# are called out rather than left for the reader to spot. Labels are lifted
# above the plot on leader lines; 2008 and 2011 are only three years apart, so
# their labels are staggered vertically to stop them overprinting.
crisis_years = {2008: ("金融危机", 36), 2011: ("欧债危机", 44), 2020: ("疫情", 36)}
for yr, (label, label_y) in crisis_years.items():
    idx = years.index(yr)
    ax.annotate(
        label, xy=(yr, gold_return[idx] + 1.5), xytext=(yr, label_y),
        ha="center", va="bottom", fontsize=8.5, color=C_BRONZE,
        arrowprops=dict(arrowstyle="-", color=C_BRONZE, lw=0.8,
                        shrinkA=2, shrinkB=2),
    )

ax.set_title("黄金年度回报（2005–2025，伦敦金 USD/oz）", loc="left")
ax.set_ylabel("年度涨跌幅 (%)")
ax.set_xticks(years[::2])
ax.set_xticklabels([str(y) for y in years[::2]], rotation=45, ha="right")
ax.tick_params(axis="x", length=0)
ax.set_ylim(-34, 54)

fig.tight_layout()
save_chart(fig, "ch12_gold.png")
