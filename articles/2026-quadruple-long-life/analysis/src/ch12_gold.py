"""Historical gold returns for calendar 2022, LBMA Gold Price PM basis.
Source: World Gold Council, December 2022, Table 1:
https://www.gold.org/goldhub/research/gold-market-commentary-december-2022
USD 0.4%, EUR 6.7%, JPY 14.4%, CNY 9.0%.
Retrieved/verified: 2026-11-05. Update source, manuscript, parameters and image together.
"""
from _style import C_BLUE,C_BRONZE,C_NAVY_SOFT,figure,save_chart,style_axes

labels=['美元', '欧元', '日元', '人民币']
values=[.4,6.7,14.4,9]
fig,ax=figure(ratio=.70)
style_axes(ax)
ax.bar(labels,values,color=C_BLUE,width=.52)
span=max(values)-min(min(values),0) or 1
for i,v in enumerate(values):ax.text(i,v+span*.035,f'{v:.2f}',ha='center',fontsize=9,color=C_BRONZE)
ax.set_ylim(min(min(values),0)-span*.10,max(values)+span*.22)
ax.set_title('2022 年黄金回报：计价货币不同',loc='left')
ax.set_ylabel('该币种全年回报（%）')
fig.text(.02,-.01,'来源：世界黄金协会，2022-12-31；非未来预测。',fontsize=8,color=C_NAVY_SOFT)
fig.tight_layout()
save_chart(fig,'ch12_gold.png')
