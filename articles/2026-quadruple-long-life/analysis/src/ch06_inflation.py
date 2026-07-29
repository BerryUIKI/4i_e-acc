"""
Ch6 — 通胀与中国 CPI 数据（2013-2025）
展示 CPI 同比走势 + 100 元购买力逐年侵蚀。
数据来源：中国国家统计局 CPI 月度数据。
"""
import matplotlib.pyplot as plt
import numpy as np
from _style import CJK_FONT, C_RED, C_NAVY, C_GRAY, C_CREAM, save_chart

# ── Data ────────────────────────────────────────────
years = list(range(2013, 2026))
cpi_yoy = [2.6, 2.0, 1.4, 2.0, 1.6, 2.1, 2.9, 2.5, 0.9, 2.0, 0.2, 0.3, 0.3]
# 100 yuan purchasing power = 100 / cumulative inflation factor
cumulative = [100.0]
for i, cpi in enumerate(cpi_yoy):
    cumulative.append(round(cumulative[-1] / (1 + cpi/100), 1))

cumulative = cumulative[1:]  # align with years

# ── Chart ──────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor(C_CREAM)

# Left: CPI YoY
bars = ax1.bar(years, cpi_yoy, color=[C_RED if v >= 2 else C_GRAY for v in cpi_yoy], edgecolor="white")
ax1.axhline(y=2.0, color=C_NAVY, linestyle="--", linewidth=0.8, alpha=0.5)
ax1.text(2013.3, 2.15, "2% 温和通胀线", fontsize=8, color=C_NAVY, alpha=0.6)
for bar, val in zip(bars, cpi_yoy):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f"{val}%",
             ha="center", va="bottom", fontsize=9, color=C_NAVY)
ax1.set_title("中国 CPI 同比涨幅（2013-2025）", fontsize=13, fontweight="bold", color=C_NAVY)
ax1.set_ylabel("CPI 同比 (%)")
ax1.set_ylim(0, 3.8)
ax1.set_xticks(years)
ax1.set_xticklabels(years, rotation=45)
ax1.grid(axis="y", alpha=0.2)

# Right: Purchasing power erosion
ax2.fill_between(years, cumulative, 100, alpha=0.25, color=C_RED)
ax2.plot(years, cumulative, color=C_RED, linewidth=2.5, marker="o", markersize=4)
for y, v in zip(years, cumulative):
    ax2.annotate(f"¥{v:.1f}", (y, v), textcoords="offset points", xytext=(0, 10),
                 fontsize=8, ha="center", color=C_NAVY)
ax2.set_title("100 元的实际购买力", fontsize=13, fontweight="bold", color=C_NAVY)
ax2.set_ylabel("相当于 2013 年的 ¥")
ax2.set_ylim(70, 102)
ax2.set_xticks(years)
ax2.set_xticklabels(years, rotation=45)
ax2.grid(axis="y", alpha=0.2)

fig.suptitle("通货膨胀的隐形侵蚀", fontsize=15, fontweight="bold", color=C_NAVY, y=1.01)
plt.tight_layout()
save_chart(fig, "ch06_inflation.png")
