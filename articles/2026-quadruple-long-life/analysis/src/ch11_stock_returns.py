"""Pure mathematical model: initial price 100, EPS 5, ending EPS 5.5,
cash dividend 2, ending P/E 16/20/24. Return=(EPS*PE+dividend)/100-1;
one period, no dividend reinvestment, taxes or fees; no historical index data.
Retrieved/verified: 2026-11-05. Update source, manuscript, parameters and image together.
"""
from _style import C_BLUE,C_BRONZE,C_NAVY_SOFT,figure,save_chart,style_axes

labels=['16 倍', '20 倍', '24 倍']
values=[(5.5*pe+2-100) for pe in (16,20,24)]
fig,ax=figure(ratio=.70)
style_axes(ax)
ax.bar(labels,values,color=C_BLUE,width=.52)
span=max(values)-min(min(values),0) or 1
for i,v in enumerate(values):ax.text(i,v+(span*.035 if v>=0 else -span*.07),f'{v:.2f}',ha='center',fontsize=9,color=C_BRONZE)
ax.set_ylim(min(min(values),0)-span*.10,max(values)+span*.22)
ax.set_title('同样盈利与股息，不同期末估值',loc='left')
ax.set_ylabel('单期总收益（%）')
fig.text(.02,-.01,'纯数学模型；期末市盈率为假设，不是估值建议。',fontsize=8,color=C_NAVY_SOFT)
fig.tight_layout()
save_chart(fig,'ch11_stock_returns.png')
