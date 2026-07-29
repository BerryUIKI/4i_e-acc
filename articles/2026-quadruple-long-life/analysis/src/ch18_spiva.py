"""
Ch18 — SPIVA 主动基金 vs 被动指数基金
不同市场、不同周期下，主动基金跑输指数的比例。
数据来源：S&P SPIVA Scorecard（2024 年终）。
"""
import matplotlib.pyplot as plt
import numpy as np
from _style import C_NAVY, C_RED, C_BLUE, C_GREEN, C_CREAM, C_GRAY, save_chart

categories = [
    "美股大盘\n1年", "美股大盘\n5年", "美股大盘\n10年",
    "美股中盘\n5年", "美股小盘\n5年",
    "新兴市场\n5年", "国际股票\n5年",
    "A股主动\n1年", "A股主动\n3年", "A股主动\n5年"
]
underperform = [51, 75, 87, 58, 62, 84, 65, 42, 55, 68]  # % underperform

colors = [C_RED if v >= 70 else C_BLUE if v >= 60 else C_GRAY for v in underperform]

fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor(C_CREAM)

bars = ax.barh(categories, underperform, color=colors, edgecolor="white", height=0.7)
ax.axvline(x=50, color=C_GRAY, linewidth=1, linestyle="--", alpha=0.5)
ax.text(52, -0.7, "50% 分界线", fontsize=8, color=C_GRAY, alpha=0.7)

for bar, val in zip(bars, underperform):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f"{val}%",
            va="center", fontsize=11, fontweight="bold", color=C_NAVY)

ax.set_title("主动基金跑输指数的比例（SPIVA 数据）", fontsize=14, fontweight="bold", color=C_NAVY)
ax.set_xlabel("跑输基准的主动基金占比 (%)")
ax.set_xlim(0, 105)
ax.invert_yaxis()
ax.grid(axis="x", alpha=0.2)

# Legend explanation
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=C_RED, label="≥70% 跑输（时间越长越难战胜市场）"),
    Patch(facecolor=C_BLUE, label="60-69% 跑输"),
    Patch(facecolor=C_GRAY, label="<60% 跑输"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=8)

plt.tight_layout()
save_chart(fig, "ch18_spiva.png")
