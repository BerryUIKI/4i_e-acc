"""
Ch20 — 大类资产相关性矩阵（2005-2025，年化）
展示股票/债券/黄金/现金之间的历史 Pearson 相关系数。

数据来源：Bloomberg / Wind / Portfolio Visualizer
  获取方式：
    - Bloomberg: 导出各资产年度总回报 → Excel → 计算 =CORREL()
    - Portfolio Visualizer (免费): https://www.portfoliovisualizer.com →
      Asset Correlations → 输入各资产 ETF 代码 → 导出矩阵
    - Python 替代：使用 AKShare/yfinance 拉取价格 → df.corr()
  更新方法：修改 corr_data 矩阵（5×5），保持对称
"""
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from _style import C_NAVY, C_NAVY_SOFT, C_RED, C_BLUE, C_CREAM, C_RULE, figure, save_chart

assets = ["沪深300", "标普500", "中债综合", "黄金", "货基"]
corr_data = [
    [1.00, 0.45, -0.12, 0.08, 0.02],   # CSI300
    [0.45, 1.00, -0.08, 0.15, 0.01],   # SP500
    [-0.12, -0.08, 1.00, 0.22, 0.35],  # Bonds
    [0.08, 0.15, 0.22, 1.00, 0.05],    # Gold
    [0.02, 0.01, 0.35, 0.05, 1.00],    # Money Market
]

# A house colormap instead of matplotlib's RdBu_r: that stock ramp is a bright
# saturated blue-to-red that clashes with the muted palette used everywhere
# else in the book. This goes cream -> slate -> deep red, so low correlation
# recedes into the page and only real co-movement takes colour.
cmap = LinearSegmentedColormap.from_list(
    "dh_corr", [C_BLUE, "#DDE3EC", C_CREAM, "#EBD9D6", C_RED], N=256
)

fig, ax = figure(ratio=0.94)
ax.set_facecolor(C_CREAM)

im = ax.imshow(np.array(corr_data), cmap=cmap, vmin=-1, vmax=1, aspect="auto")

ax.set_xticks(range(len(assets)))
ax.set_yticks(range(len(assets)))
ax.set_xticklabels(assets, rotation=30, ha="right")
ax.set_yticklabels(assets)

# No grid lines inside the matrix, and no tick marks on either axis: the cells
# already delimit themselves.
ax.grid(False)
ax.tick_params(length=0, pad=6)
for side in ("top", "right", "left", "bottom"):
    ax.spines[side].set_visible(False)

for i in range(len(assets)):
    for j in range(len(assets)):
        val = corr_data[i][j]
        ax.text(
            j, i, f"{val:+.2f}", ha="center", va="center", fontsize=9,
            color="white" if abs(val) > 0.55 else C_NAVY,
        )

cbar = fig.colorbar(im, ax=ax, shrink=0.72, pad=0.03, aspect=28)
cbar.set_label("相关系数", fontsize=8.5)
cbar.outline.set_visible(False)
cbar.ax.tick_params(length=2, width=0.6, labelsize=8)

ax.set_title("大类资产相关性矩阵（2005–2025，年化）", loc="left")

# Explainer moved below the matrix as a caption line; rotated down the side it
# fought with the colourbar and was hard to read.
fig.text(
    0.02, -0.02, "数值越低分散效果越好；负相关资产在股市下跌时提供缓冲。",
    fontsize=8, color=C_NAVY_SOFT, ha="left",
)

fig.tight_layout()
save_chart(fig, "ch20_correlation.png")
