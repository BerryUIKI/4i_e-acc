"""
Ch9 — 货币基金收益率走势 vs 活期存款（2013-2026）
货币基金 7 日年化 vs 活期存款基准利率。

数据来源：
  货币基金：天弘余额宝历史 7 日年化收益率
    获取：https://fund.eastmoney.com → 余额宝(000198) → 历史净值
  活期利率：中国人民银行活期存款基准利率
    获取：http://www.pbc.gov.cn → 货币政策 → 利率政策
  更新方法：在下方 moneymkt / demand 列表中追加最新年份数据
"""
from _style import C_NAVY, C_NAVY_SOFT, C_GRAY, C_BLUE, C_RULE, figure, save_chart, style_axes

years = list(range(2013, 2027))
moneymkt = [4.5, 4.8, 3.6, 2.5, 3.9, 3.5, 2.5, 2.1, 2.3, 1.8, 2.0, 1.8, 1.5, 1.4]
demand = [0.35] * len(years)  # ~0.35% throughout

fig, ax = figure(ratio=0.62)
style_axes(ax, grid_axis="y")

# The gap between the two lines IS the story, so shade it rather than relying on
# two bare lines the reader has to compare by eye.
ax.fill_between(years, demand, moneymkt, color=C_BLUE, alpha=0.10, zorder=2)
ax.plot(years, moneymkt, color=C_BLUE, linewidth=2, marker="o", markersize=4,
        label="货币基金 7 日年化", zorder=3)
ax.plot(years, demand, color=C_GRAY, linewidth=1.4, linestyle=(0, (5, 3)),
        label="活期存款利率", zorder=3)

# Label the endpoints only — 14 value labels across a 4.5in figure overlap.
ax.annotate(
    f"{moneymkt[0]}%", (years[0], moneymkt[0]), textcoords="offset points",
    xytext=(0, 9), fontsize=9, color=C_NAVY, ha="center",
)
ax.annotate(
    f"{moneymkt[-1]}%", (years[-1], moneymkt[-1]), textcoords="offset points",
    xytext=(0, 9), fontsize=9, color=C_NAVY, ha="center",
)

ax.set_title("货币基金 vs 活期存款：收益对比（2013–2026）", loc="left")
ax.set_ylabel("年化收益率 (%)")
ax.set_xlabel("")
ax.legend(loc="upper right", frameon=False)
ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], rotation=45, ha="right")
ax.tick_params(axis="x", length=0)
ax.set_ylim(0, 5.5)

fig.tight_layout()
save_chart(fig, "ch09_money_market.png")
