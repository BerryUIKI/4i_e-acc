"""
Ch16 — ETF 费率对长期收益的侵蚀（纯数学模拟）
比较 0.15%（低成本ETF）vs 1.00%（主动基金）30年后的终值差。

数据来源：纯数学计算
  公式：终值 = 本金 × (1 + 年化收益 - 费率)^年数
  参数：本金 10 万、年化毛收益 7%、低成本费率 0.15%、高成本费率 1.00%
  更新方法：修改 annual_return / low_fee_rate / high_fee_rate 即可
"""
import matplotlib.pyplot as plt
import numpy as np
from _style import C_NAVY, C_RED, C_BLUE, C_CREAM, C_GRAY, save_chart

years = np.arange(1, 31)
annual_return = 0.07  # 7% gross return before fees
initial = 100000

low_fee = initial * (1 + annual_return - 0.0015) ** years
high_fee = initial * (1 + annual_return - 0.01) ** years

fig, ax = plt.subplots(figsize=(11, 6))
fig.patch.set_facecolor(C_CREAM)
ax.set_facecolor(C_CREAM)

ax.fill_between(years, high_fee, low_fee, alpha=0.2, color=C_RED, label="费率差距")

l1, = ax.plot(years, low_fee, color=C_BLUE, linewidth=2.5, label="低成本 ETF（0.15%）")
l2, = ax.plot(years, high_fee, color=C_RED, linewidth=2.5, label="主动基金（1.00%）")

# Annotations
diff = low_fee[-1] - high_fee[-1]
ax.annotate(f"¥{low_fee[-1]:,.0f}", xy=(29, low_fee[-1]), fontsize=10, color=C_BLUE,
            fontweight="bold", textcoords="offset points", xytext=(-30, 10))
ax.annotate(f"¥{high_fee[-1]:,.0f}", xy=(29, high_fee[-1]), fontsize=10, color=C_RED,
            fontweight="bold", textcoords="offset points", xytext=(-30, -15))
ax.annotate(f"30年差距: ¥{diff:,.0f}\n({diff/initial*100:.0f}% 被费率吞噬)",
            xy=(20, (low_fee[19] + high_fee[19]) / 2), fontsize=12,
            color=C_RED, fontweight="bold", ha="center",
            bbox=dict(boxstyle="round,pad=0.4", facecolor=C_CREAM, edgecolor=C_RED, alpha=0.9))

ax.set_title("ETF 费率：不起眼的 0.85% 差，30 年吞噬掉多少？", fontsize=14, fontweight="bold", color=C_NAVY)
ax.set_xlabel("投资年数")
ax.set_ylabel("资产价值 (¥)")
ax.legend()
ax.grid(alpha=0.2)
ax.set_xlim(0, 31)

plt.tight_layout()
save_chart(fig, "ch16_etf_fees.png")
