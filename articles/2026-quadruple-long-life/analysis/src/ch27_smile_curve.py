"""
Ch27 — 微笑曲线定投 vs 一次性投资（纯数学模拟）
在 V 形走势（100→50→100）中，定投积累更多份额，跑赢一次性买入。

数据来源：纯数学模拟
  参数：
    - 投资总额：10 万元
    - 价格路径：24 个月 V 形（100 → 50 → 100）
    - 一次性：期初全仓买入
    - 定投：每月等额 ¥4,167（=100,000/24）
  更新方法：修改 price 数组可模拟不同市场走势
"""
import matplotlib.pyplot as plt
import numpy as np
from _style import C_NAVY, C_RED, C_BLUE, C_ORANGE, C_CREAM, C_GRAY, save_chart

# Simulate a V-shaped recovery over 24 months
# Price: starts at 100, drops to 50 at month 12, recovers to 100 at month 24
months = np.arange(1, 25)
price = np.array([100 - i*(50/11) if i <= 12 else 50 + (i-12)*(50/12) for i in range(24)])

# Lump sum: buy at month 0, hold
lump_units = 100000 / price[0]  # ¥100k investment
lump_value = lump_units * price

# DCA: ¥4167/month (=100k/24)
monthly_invest = 100000 / 24
dca_units = np.cumsum(monthly_invest / price)
dca_value = dca_units * price

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
fig.patch.set_facecolor(C_CREAM)

# Left: Price path
ax1.set_facecolor(C_CREAM)
ax1.fill_between(months, 45, price, alpha=0.15, color=C_BLUE)
ax1.plot(months, price, color=C_BLUE, linewidth=2.5)
ax1.scatter([1], [100], color=C_RED, s=80, zorder=5, label="一次性买入")
ax1.scatter([6, 12, 18], [price[5], price[11], price[17]],
           color=C_ORANGE, s=50, zorder=5, label="定投买入点")
ax1.set_title("价格走势（V 形微笑曲线）", fontsize=12, fontweight="bold", color=C_NAVY)
ax1.set_ylabel("价格")
ax1.set_xlabel("月份")
ax1.legend(loc="lower right")
ax1.grid(alpha=0.2)
ax1.set_ylim(40, 115)

# Right: Value comparison
ax2.set_facecolor(C_CREAM)
ax2.plot(months, dca_value, color=C_ORANGE, linewidth=2.5, label="定投")
ax2.plot(months, lump_value, color=C_GRAY, linewidth=2, linestyle="--", label="一次性")
ax2.axhline(y=100000, color=C_GRAY, linewidth=0.5, alpha=0.3)

# Final values
ax2.annotate(f"¥{dca_value[-1]:,.0f}", xy=(23, dca_value[-1]), fontsize=10,
             color=C_ORANGE, fontweight="bold", textcoords="offset points", xytext=(0, 8))
ax2.annotate(f"¥{lump_value[-1]:,.0f}", xy=(23, lump_value[-1]), fontsize=10,
             color=C_GRAY, fontweight="bold", textcoords="offset points", xytext=(0, -15))

gain = dca_value[-1] - lump_value[-1]
ax2.annotate(f"定投多赚 ¥{gain:,.0f}\n({gain/lump_value[-1]*100:.1f}%)",
             xy=(14, 108000), fontsize=11, color=C_RED, fontweight="bold",
             bbox=dict(boxstyle="round", facecolor=C_CREAM, edgecolor=C_RED, alpha=0.9))

ax2.set_title("定投 vs 一次性：¥10 万投资对比", fontsize=12, fontweight="bold", color=C_NAVY)
ax2.set_xlabel("月份")
ax2.legend(loc="lower right")
ax2.grid(alpha=0.2)

fig.suptitle("微笑曲线：定投在下跌中积累更多份额", fontsize=14, fontweight="bold", color=C_NAVY, y=1.01)
plt.tight_layout()
save_chart(fig, "ch27_smile_curve.png")
