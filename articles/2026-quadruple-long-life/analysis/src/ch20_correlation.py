"""
Ch20 — 大类资产相关性矩阵
展示股票/债券/黄金/现金之间的历史相关系数（2005-2025）。
"""
import matplotlib.pyplot as plt
import numpy as np
from _style import C_NAVY, C_RED, C_BLUE, C_CREAM, C_GRAY, save_chart

assets = ["沪深300", "标普500", "中债综合", "黄金", "货基"]
corr_data = [
    [1.00, 0.45, -0.12, 0.08, 0.02],   # CSI300
    [0.45, 1.00, -0.08, 0.15, 0.01],   # SP500
    [-0.12, -0.08, 1.00, 0.22, 0.35],  # Bonds
    [0.08, 0.15, 0.22, 1.00, 0.05],    # Gold
    [0.02, 0.01, 0.35, 0.05, 1.00],    # Money Market
]

fig, ax = plt.subplots(figsize=(8, 7))
fig.patch.set_facecolor(C_CREAM)

im = ax.imshow(corr_data, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")

ax.set_xticks(range(len(assets)))
ax.set_yticks(range(len(assets)))
ax.set_xticklabels(assets, rotation=30, ha="right", fontsize=10)
ax.set_yticklabels(assets, fontsize=10)

for i in range(len(assets)):
    for j in range(len(assets)):
        val = corr_data[i][j]
        c = "white" if abs(val) > 0.5 else C_NAVY
        ax.text(j, i, f"{val:+.2f}", ha="center", va="center", fontsize=10,
                fontweight="bold" if abs(val) > 0.4 else "normal", color=c)

cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label("相关系数", fontsize=9)

ax.set_title("大类资产相关性矩阵（2005-2025，年化）", fontsize=13, fontweight="bold", color=C_NAVY, pad=15)

# Annotation
ax.text(5.5, 1.5, "负相关 = 分散效果好", fontsize=9, color=C_BLUE, ha="center",
        rotation=90, va="center")

plt.tight_layout()
save_chart(fig, "ch20_correlation.png")
