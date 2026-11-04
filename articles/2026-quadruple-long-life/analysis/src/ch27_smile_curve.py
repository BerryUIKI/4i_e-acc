"""
Ch27 — 微笑曲线定投 vs 一次性投资（纯数学模拟）
在 V 形走势（100→50→100）中，定投积累更多份额，跑赢一次性买入。

数据来源：纯数学模拟
  参数：
    - 投资总额：10 万元
    - 价格路径：24 个月 V 形（100 → 50 → 100）
    - 一次性：期初全仓买入
    - 定投：每月等额 4,167 元（=100,000/24）
  更新方法：修改 price 数组可模拟不同市场走势
"""
import numpy as np
from _style import C_NAVY, C_NAVY_SOFT, C_RED, C_BLUE, C_BRONZE, C_GRAY, C_RULE, figure, save_chart, style_axes

# Simulate a V-shaped recovery over 24 months
# Price: starts at 100, drops to 50 at month 12, recovers to 100 at month 24
months = np.arange(1, 25)
price = np.array([100 - i * (50 / 11) if i <= 12 else 50 + (i - 12) * (50 / 12) for i in range(24)])

# Lump sum: buy at month 0, hold
lump_units = 100000 / price[0]
lump_value = lump_units * price

# DCA: 4167/month (=100k/24)
monthly_invest = 100000 / 24
dca_units = np.cumsum(monthly_invest / price)
dca_value = dca_units * price
gain = dca_value[-1] - lump_value[-1]

# Stacked rather than side by side: at B5 width two panels each get ~5.7cm,
# which crushes 24 monthly ticks. Stacked, each panel gets the full measure.
fig, axes = figure(ratio=1.05, nrows=2, ncols=1)
ax1, ax2 = axes

# Top: the price path, with the two buying patterns marked on it.
style_axes(ax1, grid_axis="y")
ax1.fill_between(months, 45, price, color=C_BLUE, alpha=0.08, zorder=2)
ax1.plot(months, price, color=C_BLUE, linewidth=2, zorder=3)
ax1.scatter([1], [price[0]], color=C_RED, s=46, zorder=5, label="一次性买入")
ax1.scatter([6, 12, 18], [price[5], price[11], price[17]],
            color=C_BRONZE, s=34, zorder=5, label="定投买入点")
# The dip lands at month ~13 (the generated series bottoms just after 12). The
# label sits in the empty wedge above and to the right of the vertex — below it
# is the shaded area, and left is the descending leg.
ax1.annotate("谷底", (13, price[11]), textcoords="offset points", xytext=(14, 16),
             ha="left", va="bottom", fontsize=8.5, color=C_NAVY_SOFT)
ax1.set_title("价格走势：V 形微笑曲线", loc="left", pad=22)
ax1.set_ylabel("价格")
ax1.set_xlabel("月份")
# Legend above the axes: the first buy point sits at x=1, y=100, right under
# where an upper-right in-axes legend would reach.
ax1.legend(loc="lower right", bbox_to_anchor=(1.0, 1.0), frameon=False,
           ncol=2, borderaxespad=0.2)
ax1.set_ylim(40, 112)
ax1.set_xlim(0, 25)

# Bottom: what each strategy is worth along the same path.
style_axes(ax2, grid_axis="y")
ax2.plot(months, dca_value, color=C_BRONZE, linewidth=2, label="定投", zorder=3)
ax2.plot(months, lump_value, color=C_GRAY, linewidth=1.6,
         linestyle=(0, (5, 3)), label="一次性", zorder=2)
ax2.axhline(y=100000, color=C_RULE, linewidth=0.9, zorder=2)

# Endpoint values, anchored above the end of each curve and right-aligned to
# it. The curves converge at the last month, so both labels are lifted clear
# of the other line rather than centred on their own point.
ax2.annotate(f"{dca_value[-1] / 10000:.1f} 万", (months[-1], dca_value[-1]),
             textcoords="offset points", xytext=(0, 10), ha="center", va="bottom",
             fontsize=9, color=C_BRONZE)
ax2.annotate(f"{lump_value[-1] / 10000:.1f} 万", (months[-1], lump_value[-1]),
             textcoords="offset points", xytext=(0, -12), ha="center", va="top",
             fontsize=9, color=C_GRAY)

ax2.annotate(
    f"定投多赚 {gain / 10000:.1f} 万（{gain / lump_value[-1] * 100:.1f}%）",
    xy=(0.03, 0.96), xycoords="axes fraction", ha="left", va="top",
    fontsize=9, color=C_RED,
)

ax2.set_title("定投 vs 一次性：10 万元投资对比", loc="left")
ax2.set_ylabel("账户价值 (万元)")
ax2.set_xlabel("月份")
ax2.yaxis.set_major_formatter(lambda v, _: f"{v / 10000:.0f}")
ax2.legend(loc="lower right", frameon=False, ncol=2)
ax2.set_xlim(0, 26)
ax2.set_ylim(0, 195000)

fig.tight_layout(h_pad=1.4)
save_chart(fig, "ch27_smile_curve.png")
