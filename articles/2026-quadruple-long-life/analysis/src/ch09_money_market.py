"""
Ch9 — 货币基金收益率走势 vs 活期存款（2013-2026）
数据来源：天弘余额宝 / 货币基金平均 7 日年化。
"""
import matplotlib.pyplot as plt
from _style import C_NAVY, C_GRAY, C_RED, C_BLUE, C_CREAM, save_chart

years = list(range(2013, 2027))
moneymkt = [4.5, 4.8, 3.6, 2.5, 3.9, 3.5, 2.5, 2.1, 2.3, 1.8, 2.0, 1.8, 1.5, 1.4]
demand = [0.35]*4 + [0.35]*10  # ~0.35% throughout

fig, ax = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor(C_CREAM)
ax.set_facecolor(C_CREAM)

ax.fill_between(years, demand, moneymkt, alpha=0.12, color=C_BLUE)
ax.plot(years, moneymkt, color=C_BLUE, linewidth=2.5, marker="o", markersize=5, label="货币基金 7日年化")
ax.plot(years, demand, color=C_GRAY, linewidth=1.5, linestyle="--", label="活期存款利率")

for y, m in zip(years, moneymkt):
    ax.text(y, m + 0.15, f"{m}%", ha="center", fontsize=8, color=C_NAVY)

ax.set_title("货币基金 vs 活期存款：收益对比（2013-2026）", fontsize=14, fontweight="bold", color=C_NAVY)
ax.set_ylabel("年化收益率 (%)")
ax.legend(loc="upper right")
ax.set_xticks(years)
ax.set_xticklabels(years, rotation=45)
ax.grid(axis="y", alpha=0.2)
ax.set_ylim(0, 5.5)

plt.tight_layout()
save_chart(fig, "ch09_money_market.png")
