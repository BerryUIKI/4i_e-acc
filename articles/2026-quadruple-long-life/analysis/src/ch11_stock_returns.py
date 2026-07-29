"""
Ch11 — 股票长期收益拆解：标普500 vs 沪深300
收益 = 盈利增长 + 股息 + 估值变化。展示 2005-2025 年化回报。
数据来源：Bloomberg / Wind 共识数据。
"""
import matplotlib.pyplot as plt
import numpy as np
from _style import C_NAVY, C_RED, C_BLUE, C_ORANGE, C_GRAY, C_CREAM, save_chart

categories = ["盈利增长", "股息收益", "估值变化", "总年化回报"]
sp500 = [6.8, 2.0, 1.0, 9.8]
csi300 = [8.5, 2.2, -2.8, 7.9]

x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(C_CREAM)
ax.set_facecolor(C_CREAM)

bars1 = ax.bar(x - width/2, sp500, width, color=C_BLUE, edgecolor="white", label="标普500")
bars2 = ax.bar(x + width/2, csi300, width, color=C_RED, edgecolor="white", label="沪深300")

for bar in bars1:
    v = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, v + 0.2 if v > 0 else v - 0.8,
            f"{v:+.1f}%", ha="center", fontsize=10, color=C_BLUE, fontweight="bold")
for bar in bars2:
    v = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, v + 0.2 if v > 0 else v - 0.8,
            f"{v:+.1f}%", ha="center", fontsize=10, color=C_RED, fontweight="bold")

ax.axhline(y=0, color=C_GRAY, linewidth=0.5)
ax.set_title("股票长期回报拆解：标普500 vs 沪深300（2005-2025 年化）",
             fontsize=13, fontweight="bold", color=C_NAVY)
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
ax.grid(axis="y", alpha=0.2)

plt.tight_layout()
save_chart(fig, "ch11_stock_returns.png")
