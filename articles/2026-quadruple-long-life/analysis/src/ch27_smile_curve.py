"""Ch27: pure mathematical DCA comparison, matching the printed 12-month example.

Source: teaching_models.DCA_PRICES, fictional unit prices, not historical data.
Inputs: 100,000 cash; 12 equal purchases at the listed prices; unused cash earns
zero; no taxes, fees or distributions. Update chapter and shared sequence together.
"""
import numpy as np
from teaching_models import DCA_PRICES
from _style import C_NAVY_SOFT, C_BLUE, C_BRONZE, C_GRAY, figure, save_chart, style_axes

months = np.arange(1, 13)
price = np.array(DCA_PRICES)
contribution = 100000 / len(price)
units = np.cumsum(contribution / price)
dca_invested = units * price
cash = 100000 - contribution * months
dca_total = dca_invested + cash
lump = 100000 / price[0] * price

fig, axes = figure(ratio=1.08, nrows=2, ncols=1)
ax1, ax2 = axes
style_axes(ax1)
ax1.plot(months, price, color=C_BLUE, marker='o', markersize=3)
ax1.set_title('教学价格路径：12 期先跌后回升', loc='left')
ax1.set_ylabel('单位净值（假设）')
ax1.set_xticks([1, 3, 6, 9, 12])
style_axes(ax2)
ax2.plot(months, lump / 10000, color=C_GRAY, label='一次性投入')
ax2.plot(months, dca_total / 10000, color=C_BRONZE, label='分批：持仓加未投现金')
ax2.plot(months, dca_invested / 10000, color=C_BLUE, linestyle='--', label='分批：仅已投部分')
ax2.set_title('同为 10 万元预算，未投现金按零息保留', loc='left')
ax2.set_xlabel('期数')
ax2.set_ylabel('资产（万元）')
ax2.set_xticks([1, 3, 6, 9, 12])
ax2.legend(fontsize=7.5, loc='lower right', frameon=True, facecolor='white', framealpha=.95)
ax2.annotate(f'分批末值 {dca_total[-1]/10000:.2f} 万',
             (12, dca_total[-1]/10000), xytext=(-8, 8), textcoords='offset points',
             ha='right', fontsize=8, color=C_BRONZE)
fig.text(.02, -.01, '纯数学模型；不代表未来路径或年化收益优势。', fontsize=8, color=C_NAVY_SOFT)
fig.tight_layout(h_pad=1.8)
save_chart(fig, 'ch27_smile_curve.png')
