"""Ch9: pure mathematical interest accumulation, not money-market history.
Source: FV=10000*(1+r)^years, assumed effective annual rates .01/.02/.03.
Five years, no additions/withdrawals, fees or taxes. Verified 2026-11-05.
Update model parameters and chapter together; rates are not bank/product quotes.
"""
from _style import C_BLUE,C_BRONZE,C_GRAY,C_NAVY_SOFT,figure,save_chart,style_axes
fig,ax=figure(ratio=.68);style_axes(ax)
for r,c in zip([.01,.02,.03],[C_GRAY,C_BLUE,C_BRONZE]):
 ax.plot(range(6),[10000*(1+r)**y for y in range(6)],label=f'假设 {r:.0%}',color=c)
ax.set_xlabel('年数');ax.set_ylabel('模型终值（元）')
ax.set_title('固定收益假设下的利息累积',loc='left');ax.legend(loc='upper left')
fig.text(.02,-.01,'纯数学模型；本金 1 万元，无税费，不代表现行产品报价。',fontsize=8,color=C_NAVY_SOFT)
fig.tight_layout();save_chart(fig,'ch09_money_market.png')
