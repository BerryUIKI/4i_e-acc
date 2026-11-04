"""Pure mathematical model: two hypothetical assets with equal weights,
volatility .20 and .10, correlations -.5/0/.8. Portfolio standard deviation
is sqrt(.5^2*.2^2+.5^2*.1^2+2*.5*.5*.2*.1*rho); no historical input.
Retrieved/verified: 2026-11-05. Update source, manuscript, parameters and image together.
"""
from _style import C_BLUE,C_BRONZE,C_NAVY_SOFT,figure,save_chart,style_axes
from math import sqrt
labels=['−0.5', '0', '0.8']
values=[100*sqrt(.0125+.01*rho) for rho in (-.5,0,.8)]
fig,ax=figure(ratio=.70)
style_axes(ax)
ax.bar(labels,values,color=C_BLUE,width=.52)
span=max(values)-min(min(values),0) or 1
for i,v in enumerate(values):ax.text(i,v+span*.035,f'{v:.2f}',ha='center',fontsize=9,color=C_BRONZE)
ax.set_ylim(min(min(values),0)-span*.10,max(values)+span*.22)
ax.set_title('不同相关性下的组合波动（假设）',loc='left')
ax.set_ylabel('组合收益标准差（%）')
fig.text(.02,-.01,'纯数学模型；各占一半，单项波动率假设为 20% 与 10%。',fontsize=8,color=C_NAVY_SOFT)
fig.tight_layout()
save_chart(fig,'ch20_correlation.png')
