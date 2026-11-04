"""
Ch16 — ETF 费率对长期收益的侵蚀（纯数学模拟）
比较 0.15%（低成本 ETF）vs 1.00%（主动基金）30 年后的终值差。

数据来源：纯数学计算
  公式：终值 = 本金 × (1 + 年化收益 - 费率)^年数
  参数：本金 10 万、年化毛收益 7%、低成本费率 0.15%、高成本费率 1.00%
  更新方法：修改 annual_return / low_fee_rate / high_fee_rate 即可
"""
import numpy as np
from _style import C_NAVY, C_NAVY_SOFT, C_RED, C_BLUE, C_CREAM, C_RULE, figure, save_chart, style_axes

years = np.arange(1, 31)
annual_return = 0.07  # 7% gross return before fees
initial = 100000

low_fee = initial * (1 + annual_return - 0.0015) ** years
high_fee = initial * (1 + annual_return - 0.01) ** years
diff = low_fee[-1] - high_fee[-1]

fig, ax = figure(ratio=0.66)
style_axes(ax, grid_axis="y")

# The shaded band between the two curves is the whole argument: it is the money
# the fee difference takes, and it widens with every year held.
ax.fill_between(years, high_fee, low_fee, color=C_RED, alpha=0.10, zorder=2)
ax.plot(years, low_fee, color=C_BLUE, linewidth=2, label="较低费率假设（0.15%）", zorder=3)
ax.plot(years, high_fee, color=C_RED, linewidth=2, label="较高费率假设（1.00%）", zorder=3)

# Endpoint values, labelled directly on the curves at the right edge. The ¥
# glyph is avoided entirely: msyh.ttc renders U+00A5 as tofu for some
# (fontweight, size) combinations, and 万元 carries the meaning without it.
ax.annotate(
    f"{low_fee[-1] / 10000:.0f} 万", (years[-1], low_fee[-1]),
    textcoords="offset points", xytext=(6, 4), fontsize=9, color=C_BLUE,
)
ax.annotate(
    f"{high_fee[-1] / 10000:.0f} 万", (years[-1], high_fee[-1]),
    textcoords="offset points", xytext=(6, -10), fontsize=9, color=C_RED,
)

# Headline number sits under the legend in the upper-left free space. It used to
# be centred at the top, where it overran the legend and the value labels.
ax.annotate(
    f"30 年差距 {diff / 10000:.0f} 万\n"
    f"相当于初始本金的 {diff / initial * 100:.0f}%",
    xy=(0.03, 0.72), xycoords="axes fraction",
    ha="left", va="top", fontsize=9, color=C_NAVY_SOFT,
    linespacing=1.6,
)

ax.set_title("纯数学模型：费率差 0.85 个百分点", loc="left")
ax.set_xlabel("投资年数")
ax.set_ylabel("资产价值 (万元)")
ax.set_xlim(0, 33)
ax.set_xticks([1, 5, 10, 15, 20, 25, 30])
ax.yaxis.set_major_formatter(lambda v, _: f"{v / 10000:.0f}")
ax.legend(loc="upper left", frameon=False)

fig.tight_layout()
save_chart(fig, "ch16_etf_fees.png")
