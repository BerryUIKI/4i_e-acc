"""
Ch11 — 股票长期收益拆解：标普500 vs 沪深300（2005-2025）
收益 = 盈利增长 + 股息收益 + 估值变化。

数据来源：Bloomberg / Wind 终端共识数据
  获取方式：终端导出各指数成分股汇总 EPS 增长、股息率、PE 变化
  公开替代：
    标普500：https://www.spglobal.com/spdji/ → 年度市场报告
    沪深300：https://www.csindex.com.cn → 指数月报 → 估值与基本面
  更新方法：修改 sp500 / csi300 数组中的年化数值
"""
import numpy as np
from _style import C_NAVY, C_RED, C_BLUE, C_RULE, figure, save_chart, style_axes

categories = ["盈利增长", "股息收益", "估值变化", "总年化回报"]
sp500 = [6.8, 2.0, 1.0, 9.8]
csi300 = [8.5, 2.2, -2.8, 7.9]

x = np.arange(len(categories))
width = 0.34

fig, ax = figure(ratio=0.66)
style_axes(ax, grid_axis="y")

bars1 = ax.bar(x - width / 2, sp500, width, color=C_BLUE, label="标普500", zorder=3)
bars2 = ax.bar(x + width / 2, csi300, width, color=C_RED, label="沪深300", zorder=3)

# Value labels sit outside the bar on whichever side the bar points, so the
# negative 估值变化 bar is labelled below rather than inside the axis. The two
# bars in a pair are narrow, so labels are nudged apart horizontally to stop
# adjacent pairs colliding (observed on the 2.0/2.2 group).
for bars, color, dx in ((bars1, C_BLUE, -4), (bars2, C_RED, 4)):
    for bar in bars:
        v = bar.get_height()
        offset = 4 if v >= 0 else -12
        ax.annotate(
            f"{v:+.1f}%", (bar.get_x() + bar.get_width() / 2, v),
            textcoords="offset points", xytext=(dx, offset),
            ha="center", fontsize=8.5, color=color,
        )

ax.axhline(y=0, color=C_RULE, linewidth=0.9, zorder=2)
ax.set_title("股票长期回报拆解（2005–2025 年化）", loc="left")

# Legend in the upper-left: with ylim headroom raised, the area above the
# 盈利增长 bars is the only region no bar or value label occupies.
ax.legend(loc="upper left", frameon=False, ncol=2,
          columnspacing=1.4, handlelength=1.2, borderaxespad=0.4)

ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.tick_params(axis="x", length=0)
ax.set_ylim(-3.8, 13.6)

fig.tight_layout()
save_chart(fig, "ch11_stock_returns.png")
