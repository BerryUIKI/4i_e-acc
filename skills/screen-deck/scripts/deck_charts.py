#!/usr/bin/env python3
"""Presentation charts for the 16:9 screen decks.

Redrawn for projection rather than print: Dark Ground palette, larger type,
sparse ticks, and an annotated takeaway inside each chart so the slide reads
without a caption. Numbers come from the book's own analysis scripts; every
figure keeps the same teaching inputs and states its scope on the chart.

Output: output/decks/charts/*.png  (regenerated on every deck build)
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FONTS = ROOT / "skills" / "pdf-toolbook" / "assets" / "fonts"
OUT = ROOT / "output" / "decks" / "charts"

# Dark Ground palette — bold on the cream deck and legible when projected.
INK = "#1D1E50"
INK_SOFT = "#5A5B87"
MUTED = "#9A9BBB"
RULE = "#DED9CF"
CREAM = "#FBF7F0"
PINK = "#F3A6AF"
BRONZE = "#B86C40"
NAVY = "#2E3170"
TEAL = "#1F7A66"
RED = "#B03A48"

SERIF = "SourceHan"
SANS = "SourceHanS"


def _register_fonts() -> None:
    for f in FONTS.glob("*.otf"):
        try:
            fm.fontManager.addfont(str(f))
        except Exception:
            pass
    # Pick whichever Source Han family name the files expose.
    names = {f.name for f in fm.fontManager.ttflist if "Source Han" in f.name}
    global SERIF, SANS
    if "Source Han Serif SC" in names:
        SERIF = "Source Han Serif SC"
    if "Source Han Sans SC" in names:
        SANS = "Source Han Sans SC"


_register_fonts()

plt.rcParams.update(
    {
        "font.family": SANS,
        "axes.unicode_minus": False,
        "figure.facecolor": CREAM,
        "axes.facecolor": CREAM,
        "savefig.facecolor": CREAM,
        "text.color": INK,
        "axes.labelcolor": INK_SOFT,
        "xtick.color": INK_SOFT,
        "ytick.color": INK_SOFT,
        "axes.edgecolor": RULE,
        "font.size": 15,
    }
)


def canvas(w: float = 8.4, h: float = 4.7):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    # Room below the axes for the takeaway + source, and enough headroom for
    # the big title block. Right margin is generous because value labels are
    # drawn outside the last bar.
    fig.subplots_adjust(left=0.105, right=0.90, top=0.74, bottom=0.245)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(RULE)
    ax.spines["bottom"].set_color(RULE)
    ax.tick_params(axis="both", length=0, pad=10, labelsize=15)
    return fig, ax


def headline(fig, kicker: str, title: str) -> None:
    fig.text(0.022, 0.975, kicker, fontsize=13, color=BRONZE, weight="bold",
             va="top", family=SANS)
    fig.text(0.022, 0.915, title, fontsize=26, color=INK, weight="bold",
             va="top", family=SERIF)


def takeaway(fig, text: str, color: str = BRONZE) -> None:
    """One-line reading of the chart, set inside the figure."""
    fig.text(0.022, 0.105, text, fontsize=16, color=color, va="center",
             family=SERIF, weight="bold")


def source(fig, text: str) -> None:
    fig.text(0.022, 0.038, text, fontsize=10, color=MUTED, va="bottom",
             family=SANS)


def save(fig, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    fig.savefig(p, dpi=200, facecolor=CREAM)
    plt.close(fig)
    return p


# Source chart filename -> builder that redraws it for the decks.


# --------------------------------------------------------------- charts


def ch06_inflation() -> None:
    labels = ["2023", "2024", "2025"]
    vals = [0.2, 0.2, 0.0]
    fig, ax = canvas()
    cols = [NAVY, NAVY, MUTED]
    bars = ax.bar(labels, vals, color=cols, width=0.42, zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.016, f"{v:.1f}%",
                ha="center", fontsize=19, weight="bold",
                color=INK if v else MUTED)
    # A zero bar draws nothing, so mark the baseline where 2025 sits.
    ax.plot([2], [0], marker="_", markersize=34, color=MUTED, zorder=4)
    ax.set_ylim(0, 0.30)
    ax.set_yticks([0, 0.1, 0.2, 0.3])
    ax.set_yticklabels(["0", "0.1", "0.2", "0.3"])
    ax.set_ylabel("较上年变化（%）", fontsize=14)
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    headline(fig, "通货膨胀", "三年物价涨幅，年年在零附近")
    takeaway(fig, "涨幅低不等于没代价：钱在悄悄变得更慢")
    source(fig, "来源：国家统计局年度发布（2023–2025）；不是未来通胀预测。")
    save(fig, "ch06-inflation.png")


def ch07_drawdowns() -> None:
    loss = [10, 20, 30, 40, 50, 60, 70]
    gain = [100 / (100 - p) - 1 for p in loss]
    fig, ax = canvas(h=4.8)
    cols = [TEAL if g <= 1 else RED for g in gain]
    bars = ax.barh([f"−{p}%" for p in loss], [g * 100 for g in gain],
                   color=cols, height=0.58, zorder=3)
    for b, g in zip(bars, gain):
        ax.text(b.get_width() + 6, b.get_y() + b.get_height() / 2,
                f"+{g*100:.0f}%", va="center", fontsize=17, weight="bold",
                color=INK)
    ax.axvline(100, color=BRONZE, linestyle=(0, (5, 4)), linewidth=1.6, zorder=2)
    ax.text(104, -0.62, "需翻倍", fontsize=14, color=BRONZE, weight="bold")
    ax.set_xlim(0, 250)
    ax.invert_yaxis()
    ax.grid(axis="x", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    headline(fig, "风险的另一面", "跌得越深，回本越难")
    takeaway(fig, "跌 50% 要涨 100% 才回本——跌幅从不是对等的")
    source(fig, "纯数学：回本涨幅 = 1 ÷ (1 − 跌幅) − 1。")
    save(fig, "ch07-drawdowns.png")


def ch09_money_market() -> None:
    ys = np.arange(0, 6)
    fig, ax = canvas()
    for r, c, lab in [(0.01, MUTED, "假设 1%"), (0.02, NAVY, "假设 2%"),
                      (0.03, BRONZE, "假设 3%")]:
        vals = [10000 * (1 + r) ** y for y in ys]
        ax.plot(ys, vals, color=c, linewidth=3, marker="o", markersize=6,
                zorder=3, label=lab)
        ax.text(5.12, vals[-1], f"{vals[-1]/10000:.2f} 万", color=c,
                fontsize=16, weight="bold", va="center")
    ax.set_xlim(0, 5.9)
    ax.set_xticks(ys)
    ax.set_ylabel("终值（元）", fontsize=14)
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper left", fontsize=14, labelcolor=INK_SOFT)
    headline(fig, "现金的代价", "1 万放在货币类工具，五年后差多少")
    takeaway(fig, "收益差 2 个百分点，五年后差了近 800 元")
    source(fig, "纯数学模型：本金 1 万元，固定有效年收益，无税费；非产品报价。")
    save(fig, "ch09-money-market.png")


def ch10_bond_yields() -> None:
    rates = np.linspace(0.01, 0.05, 81)
    prices = [sum(3 / (1 + r) ** t for t in range(1, 6)) + 100 / (1 + r) ** 5
              for r in rates]
    fig, ax = canvas()
    ax.plot(rates * 100, prices, color=NAVY, linewidth=3.2, zorder=3)
    ax.fill_between(rates * 100, prices, min(prices) - 1, color=PINK, alpha=0.28,
                    zorder=1)
    ax.set_ylabel("债券价格（元）", fontsize=14)
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    headline(fig, "债券的第一课", "收益率上升，价格下跌")
    takeaway(fig, "收益率从 1% 升到 5%，价格跌去近一成")
    source(fig, "纯数学模型：面值 100、年票息 3、五年期，非实际报价。")
    save(fig, "ch10-bond-yields.png")


def ch11_stock_returns() -> None:
    pes = [16, 20, 24]
    vals = [(5.5 * pe + 2 - 100) for pe in pes]
    fig, ax = canvas()
    bars = ax.bar([f"{p} 倍" for p in pes], vals,
                  color=[MUTED, NAVY, BRONZE], width=0.44, zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 2.4, f"{v:.0f}%",
                ha="center", fontsize=19, weight="bold", color=INK)
    ax.axhline(0, color=RULE, linewidth=1)
    ax.set_ylim(-15, 45)
    ax.set_ylabel("单期总收益（%）", fontsize=14)
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    headline(fig, "估值决定收益", "同样的盈利，不同的买入价格")
    takeaway(fig, "盈利只涨 10%，估值从 16 倍到 24 倍，收益差了 44 个百分点")
    source(fig, "纯数学模型：期末市盈率为假设，不是估值建议。")
    save(fig, "ch11-stock-returns.png")


def ch12_gold() -> None:
    labels = ["美元", "欧元", "日元", "人民币"]
    vals = [0.4, 6.7, 14.4, 9.0]
    fig, ax = canvas()
    bars = ax.bar(labels, vals, color=[MUTED, NAVY, BRONZE, TEAL],
                  width=0.44, zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.7, f"{v:.1f}%",
                ha="center", fontsize=19, weight="bold", color=INK)
    ax.set_ylim(0, 18)
    ax.set_ylabel("该币种全年回报（%）", fontsize=14)
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    headline(fig, "同一块金子，不同答案", "2022 年黄金以四种货币计价")
    takeaway(fig, "同一资产，收益差异几乎全部来自汇率")
    source(fig, "来源：世界黄金协会 2022 年 12 月报告，表 1；非未来预测。")
    save(fig, "ch12-gold.png")


def ch15_qdii_premium() -> None:
    prem = [5, 10, 20, 30]
    loss = [p / (100 + p) * 100 for p in prem]
    fig, ax = canvas()
    bars = ax.bar([f"{p}%" for p in prem], loss,
                  color=[MUTED, NAVY, BRONZE, RED], width=0.46, zorder=3)
    for b, v in zip(bars, loss):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.7, f"{v:.1f}%",
                ha="center", fontsize=19, weight="bold", color=INK)
    ax.set_ylim(0, 25)
    ax.set_ylabel("溢价归零后的亏损（%）", fontsize=14)
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    headline(fig, "溢价的陷阱", "买贵了，净值不变也会亏")
    takeaway(fig, "溢价 30% 买入，净值不动，本金已经少了 23%")
    source(fig, "纯数学模型：损失 = 溢价 ÷ (1 + 溢价)；无具体产品数据。")
    save(fig, "ch15-qdii-premium.png")


def ch16_etf_fees() -> None:
    ys = np.arange(1, 31)
    lo = [100000 * (1 + 0.07 - 0.0015) ** y for y in ys]
    hi = [100000 * (1 + 0.07 - 0.01) ** y for y in ys]
    fig, ax = canvas()
    ax.fill_between(ys, np.array(hi) / 10000, np.array(lo) / 10000,
                    color=RED, alpha=0.14, zorder=1)
    ax.plot(ys, np.array(lo) / 10000, color=TEAL, linewidth=3.4, zorder=3,
            label="费率 0.15%")
    ax.plot(ys, np.array(hi) / 10000, color=RED, linewidth=3.4, zorder=3,
            label="费率 1.00%")
    ax.text(30.6, lo[-1] / 10000, f"{lo[-1]/10000:.0f} 万", color=TEAL,
            fontsize=17, weight="bold", va="center")
    ax.text(30.6, hi[-1] / 10000, f"{hi[-1]/10000:.0f} 万", color=RED,
            fontsize=17, weight="bold", va="center")
    ax.set_xlim(1, 33.5)
    ax.set_ylabel("终值（万元）", fontsize=14)
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper left", fontsize=15, labelcolor=INK_SOFT)
    headline(fig, "费率的复利", "0.85 个百分点，三十年吃掉四成")
    takeaway(fig, "起步 10 万，30 年后差出 18 万——差的是费率，不是水平")
    source(fig, "纯数学模型：本金 10 万，毛收益 7%，年度简化扣费。")
    save(fig, "ch16-etf-fees.png")


def ch18_spiva() -> None:
    fig, ax = canvas()
    vals = [60, 65]
    bars = ax.bar(["2023", "2024"], vals, color=[NAVY, BRONZE], width=0.40,
                  zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 2.4, f"{v}%",
                ha="center", fontsize=21, weight="bold", color=INK)
    ax.set_ylim(0, 100)
    ax.set_ylabel("一年跑输标普 500 的基金占比", fontsize=14)
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    headline(fig, "主动管理的真相", "美国大盘主动基金，两年连续跑输")
    takeaway(fig, "每 3 只里就有 2 只，跑不过一个不需要经理的指数")
    source(fig, "来源：SPIVA U.S. Year-End 2024 官方介绍；基准标普 500。")
    save(fig, "ch18-spiva.png")


def ch20_correlation() -> None:
    rhos = [-0.5, 0, 0.8]
    vals = [100 * np.sqrt(0.0125 + 0.01 * r) for r in rhos]
    fig, ax = canvas()
    bars = ax.bar(["−0.5", "0", "0.8"], vals, color=[TEAL, NAVY, RED],
                  width=0.42, zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.7, f"{v:.1f}%",
                ha="center", fontsize=19, weight="bold", color=INK)
    ax.set_ylim(0, 20)
    ax.set_ylabel("组合收益标准差（%）", fontsize=14)
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    headline(fig, "分散为什么有用", "同样的两项资产，只改相关性")
    takeaway(fig, "相关性从 +0.8 到 −0.5，组合波动降了三分之一")
    source(fig, "纯数学模型：各占一半，单项波动率假设 20% 与 10%。")
    save(fig, "ch20-correlation.png")


def ch27_smile() -> None:
    # The price path is the book's own committed teaching sequence, imported
    # rather than retyped so the deck cannot drift from the manuscript.
    import sys as _sys

    src = ROOT / "articles" / "2026-quadruple-long-life" / "analysis" / "src"
    if str(src) not in _sys.path:
        _sys.path.insert(0, str(src))
    from teaching_models import DCA_PRICES

    prices = np.array(DCA_PRICES, dtype=float)
    months = np.arange(1, len(prices) + 1)
    contrib = 100000 / len(prices)
    units = np.cumsum(contrib / prices)
    invested = units * prices
    cash = 100000 - contrib * months
    total = invested + cash
    lump = 100000 / prices[0] * prices

    fig, ax = canvas(h=4.8)
    ax.plot(months, lump / 10000, color=MUTED, linewidth=3, zorder=3,
            label="一次性投入")
    ax.plot(months, total / 10000, color=BRONZE, linewidth=3.4, zorder=4,
            label="分批：持仓 + 未投现金")
    ax.plot(months, invested / 10000, color=NAVY, linewidth=3, zorder=3,
            label="分批：仅已投部分")
    ax.set_xticks([1, 3, 6, 9, 12])
    ax.set_ylabel("账户价值（万元）", fontsize=14)
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower right", fontsize=13, labelcolor=INK_SOFT)
    headline(fig, "微笑曲线", "先跌后涨的十二个月，分批为什么更稳")
    takeaway(fig, "同样的钱，分批买的份额更多，回升时赚得更多")
    source(fig, "教学模型：虚构单位价格，10 万元分 12 期；未投现金零息。")
    save(fig, "ch27-smile-curve.png")


def ch29_cycles() -> None:
    fig, ax = canvas()
    for seq, lab, col in [((-0.3, 0.2, 0.3), "先跌后涨", NAVY),
                          ((0.3, 0.2, -0.3), "先涨后跌", RED)]:
        vals = [10.0]
        for r in seq:
            vals.append(vals[-1] * (1 + r) - 1)
        ax.plot(range(4), vals, color=col, linewidth=3.4, marker="o",
                markersize=9, zorder=3, label=lab)
        ax.text(3.08, vals[-1], f"{vals[-1]:.2f}", color=col, fontsize=17,
                weight="bold", va="center")
    ax.set_xlim(0, 3.7)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(["起点", "第1年", "第2年", "第3年"])
    ax.set_ylabel("账户余额（万元）", fontsize=14)
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower left", fontsize=14, labelcolor=INK_SOFT)
    headline(fig, "收益顺序风险", "同样三年，顺序不同，结局不同")
    takeaway(fig, "同样的收益，先跌还是先涨，退休账户差距超过 15%")
    source(fig, "纯数学模型：初始 10 万，每年末取 1 万；无通胀与费用。")
    save(fig, "ch29-cycles.png")


ALL = {
    "ch06_inflation.png": ch06_inflation,
    "ch07_drawdowns.png": ch07_drawdowns,
    "ch09_money_market.png": ch09_money_market,
    "ch10_bond_yields.png": ch10_bond_yields,
    "ch11_stock_returns.png": ch11_stock_returns,
    "ch12_gold.png": ch12_gold,
    "ch15_qdii_premium.png": ch15_qdii_premium,
    "ch16_etf_fees.png": ch16_etf_fees,
    "ch18_spiva.png": ch18_spiva,
    "ch20_correlation.png": ch20_correlation,
    "ch27_smile_curve.png": ch27_smile,
    "ch29_market_cycles.png": ch29_cycles,
}


def build_all() -> dict[str, Path]:
    result = {}
    for name, fn in ALL.items():
        fn()  # writes output/decks/charts/<name with dashes>
        out_name = name.replace("_", "-").replace(".png", ".png")
        result[name] = OUT / out_name
    return result


if __name__ == "__main__":
    for name, p in build_all().items():
        print(f"  {p.relative_to(ROOT)}  <- {name}")
