"""
Ch7 — 亏损与回本对照表
跌幅越大，需要的涨幅越大才能回本。

数据来源：纯数学计算
  公式：回本所需涨幅 = 1/(1 - 跌幅) - 1
  无需外部数据源，仅改动 loss_pcts 列表可调整展示范围
"""
import matplotlib.pyplot as plt
import numpy as np
from _style import C_RED, C_GREEN, C_NAVY, C_CREAM, save_chart

loss_pcts = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70]
gain_needed = [round(100/(100-p) - 1, 4)*100 for p in loss_pcts]

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(C_CREAM)
ax.set_facecolor(C_CREAM)

colors = [C_GREEN if p <= 25 else C_RED for p in loss_pcts]
bars = ax.barh([f"-{p}%" for p in loss_pcts], gain_needed, color=colors, edgecolor="white", height=0.65)

for bar, val in zip(bars, gain_needed):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f"+{val:.1f}%",
            va="center", fontsize=11, fontweight="bold", color=C_NAVY)

ax.set_title("亏损越多，回本越难", fontsize=14, fontweight="bold", color=C_NAVY)
ax.set_xlabel("回本所需涨幅 (%)")
ax.invert_yaxis()
ax.grid(axis="x", alpha=0.2)
ax.axvline(x=100, color=C_RED, linestyle="--", linewidth=1, alpha=0.4)
ax.text(102, 1.5, "需翻倍", fontsize=9, color=C_RED, alpha=0.7)

plt.tight_layout()
save_chart(fig, "ch07_drawdowns.png")
