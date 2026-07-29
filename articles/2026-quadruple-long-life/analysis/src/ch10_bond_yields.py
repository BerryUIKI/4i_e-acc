"""
Ch10 — 中国国债收益率曲线（2024 vs 2025 vs 2026 年中对比）
展示不同期限的收益率变化 + 利率下行趋势。
"""
import matplotlib.pyplot as plt
from _style import C_NAVY, C_RED, C_BLUE, C_GREEN, C_CREAM, C_GRAY, save_chart

tenors = ["1年", "2年", "3年", "5年", "7年", "10年", "20年", "30年"]
y2024 = [1.65, 1.75, 1.82, 2.05, 2.22, 2.28, 2.52, 2.58]
y2025 = [1.38, 1.42, 1.48, 1.65, 1.78, 1.85, 2.05, 2.12]
y2026 = [1.18, 1.22, 1.28, 1.42, 1.55, 1.62, 1.80, 1.88]

x = range(len(tenors))

fig, ax = plt.subplots(figsize=(12, 5.5))
fig.patch.set_facecolor(C_CREAM)
ax.set_facecolor(C_CREAM)

ax.plot(x, y2024, color=C_GRAY, linewidth=2, marker="s", markersize=6, label="2024 年中")
ax.plot(x, y2025, color=C_BLUE, linewidth=2, marker="^", markersize=6, label="2025 年中")
ax.plot(x, y2026, color=C_RED, linewidth=2.5, marker="o", markersize=7, label="2026 年中")

for i, (v24, v25, v26) in enumerate(zip(y2024, y2025, y2026)):
    ax.text(i, v26 + 0.06, f"{v26}%", ha="center", fontsize=8, color=C_RED, fontweight="bold")

# Arrow annotation: rate decline
ax.annotate("利率持续下行", xy=(4, 1.55), xytext=(2, 2.3),
            arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.5),
            fontsize=11, color=C_RED, fontweight="bold")

ax.set_title("中国国债收益率曲线：2024-2026 年对比", fontsize=14, fontweight="bold", color=C_NAVY)
ax.set_ylabel("收益率 (%)")
ax.set_xticks(x)
ax.set_xticklabels(tenors)
ax.legend(loc="upper left")
ax.grid(axis="y", alpha=0.2)
ax.set_ylim(0.8, 3.0)

plt.tight_layout()
save_chart(fig, "ch10_bond_yields.png")
