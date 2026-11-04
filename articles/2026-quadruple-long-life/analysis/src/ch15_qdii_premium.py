"""
Ch15 — QDII-ETF 溢价案例
展示 QDII ETF 在额度受限时的溢价率峰值及投资者亏损计算。

数据来源：各 QDII-ETF 历史 IOPV 折溢价数据
  获取方式：东方财富 (https://quote.eastmoney.com) → 搜索 ETF 代码 →
            F10/基金概况 → IOPV 折溢价历史 → 取各产品历史溢价率峰值
  更新方法：修改 products / premium_peak / loss_10w 数组
  注意：溢价率峰值随时间变化，应标注数据截止日期
"""
import numpy as np
from _style import C_NAVY, C_NAVY_SOFT, C_RED, C_GRAY, C_RULE, figure, save_chart, style_axes

# Case data
products = ["纳指ETF", "标普ETF", "日经ETF", "德国ETF"]
codes = ["513100", "513500", "513520", "513030"]
premium_peak = [20.5, 15.8, 22.3, 12.1]   # 溢价率峰值 %
loss_10w = [1.71, 1.36, 1.82, 1.08]       # 10 万投资若溢价买入的亏损（万）

x = np.arange(len(products))

# One quantity on the axis, the second in the annotation. An earlier version
# drew premium and loss as paired bars on twin axes; at B5 width the two label
# sets collided and the dual scales made the comparison harder, not easier.
# The point of the chart is the premium itself — the loss figure follows from it
# and belongs in the label.
fig, ax = figure(ratio=0.72)
style_axes(ax, grid_axis="y")

bars = ax.bar(x, premium_peak, width=0.52, color=C_RED, zorder=3)

for bar, prem, loss in zip(bars, premium_peak, loss_10w):
    cx = bar.get_x() + bar.get_width() / 2
    # Two stacked lines above each bar: the premium on top, the loss beneath it
    # in a lighter weight. Putting the loss inside the bar failed — at 0.52 bar
    # width the text was wider than the bar and spilled over the edges.
    ax.annotate(f"{prem}%", (cx, prem), textcoords="offset points", xytext=(0, 18),
                ha="center", fontsize=9.5, color=C_RED)
    ax.annotate(f"亏 {loss} 万", (cx, prem), textcoords="offset points", xytext=(0, 5),
                ha="center", fontsize=8, color=C_NAVY_SOFT)

# Fund codes as a second, muted tick row.
for i, code in enumerate(codes):
    ax.annotate(code, (i, 0), xycoords=("data", "axes fraction"),
                xytext=(0, -34), textcoords="offset points",
                ha="center", fontsize=7.5, color=C_GRAY)

ax.set_title("QDII-ETF 高溢价风险：溢价买入的代价", loc="left")
ax.set_ylabel("溢价率峰值 (%)")
ax.set_xticks(x)
ax.set_xticklabels(products)
ax.tick_params(axis="x", length=0, pad=4)
ax.set_ylim(0, 30)

fig.tight_layout()
save_chart(fig, "ch15_qdii_premium.png")
