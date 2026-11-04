"""Ch15: pure mathematical premium-normalization loss, no historical products.

Source: loss = p/(1+p). Inputs: hypothetical premiums 5%, 10%, 20%, 30%;
NAV unchanged, premium returns to zero, no fees/taxes. Verified 2026-11-05.
Update parameters alongside chapter 15 and appendix D; do not imply peak history.
"""
from _style import C_BLUE,C_BRONZE,C_NAVY_SOFT,figure,save_chart,style_axes
premiums=[.05,.1,.2,.3]
losses=[p/(1+p)*100 for p in premiums]
fig,ax=figure(ratio=.68)
style_axes(ax)
ax.bar([f'{p:.0%}' for p in premiums],losses,color=C_BLUE,width=.55)
for i,v in enumerate(losses):ax.text(i,v+.8,f'{v:.2f}%',ha='center',fontsize=9,color=C_BRONZE)
ax.set_ylim(0,28)
ax.set_xlabel('买入时假设溢价率')
ax.set_ylabel('相对买入成本的亏损（%）')
ax.set_title('净值不变、溢价归零：损失是多少',loc='left')
fig.text(.02,-.01,'纯数学模型；无具体产品与历史峰值数据，不计税费。',fontsize=8,color=C_NAVY_SOFT)
fig.tight_layout()
save_chart(fig,'ch15_qdii_premium.png')
