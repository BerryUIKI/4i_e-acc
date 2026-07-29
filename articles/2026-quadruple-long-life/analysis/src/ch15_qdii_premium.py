"""
Ch15 — QDII-ETF 溢价案例
展示 QDII ETF 在额度受限时的溢价率峰值及投资者亏损计算。

数据来源：各 QDII-ETF 历史 IOPV 折溢价数据
  获取方式：东方财富 (https://quote.eastmoney.com) → 搜索 ETF 代码 →
            F10/基金概况 → IOPV 折溢价历史 → 取各产品历史溢价率峰值
  更新方法：修改 products / premium_peak / loss_10w 数组
  注意：溢价率峰值随时间变化，应标注数据截止日期
"""
import matplotlib.pyplot as plt
import numpy as np
from _style import C_NAVY, C_RED, C_BLUE, C_CREAM, C_GRAY, save_chart

# Case data
products = ["纳指ETF\n(513100)", "标普ETF\n(513500)", "日经ETF\n(513520)", "德国ETF\n(513030)"]
premium_peak = [20.5, 15.8, 22.3, 12.1]    # 溢价率峰值%
loss_10w = [1.71, 1.36, 1.82, 1.08]         # 10万投资若溢价买入亏损(万)

x = np.arange(len(products))
width = 0.35

fig, ax1 = plt.subplots(figsize=(11, 6))
fig.patch.set_facecolor(C_CREAM)
ax1.set_facecolor(C_CREAM)

bars = ax1.bar(x - width/2, premium_peak, width, color=C_RED, edgecolor="white", label="溢价率峰值")
ax1.set_ylabel("溢价率 (%)", color=C_RED)
ax1.tick_params(axis="y", labelcolor=C_RED)

for bar, val in zip(bars, premium_peak):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{val}%", ha="center", fontsize=11, fontweight="bold", color=C_RED)

ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, loss_10w, width, color=C_NAVY, edgecolor="white", label="10万投资亏损")
ax2.set_ylabel("10万元投资亏损 (万元)", color=C_NAVY)
ax2.tick_params(axis="y", labelcolor=C_NAVY)

for bar, val in zip(bars2, loss_10w):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f"¥{val}万", ha="center", fontsize=10, color=C_NAVY)

ax1.set_title("QDII-ETF 高溢价风险：溢价买入的代价", fontsize=14, fontweight="bold", color=C_NAVY)
ax1.set_xticks(x)
ax1.set_xticklabels(products)
ax1.set_ylim(0, 28)
ax2.set_ylim(0, 2.5)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

plt.tight_layout()
save_chart(fig, "ch15_qdii_premium.png")
