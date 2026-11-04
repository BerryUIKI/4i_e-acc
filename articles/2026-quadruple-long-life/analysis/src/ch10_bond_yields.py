"""Ch10: pure mathematical price/yield model, not a government yield curve.
Source: price=sum(3/(1+y)^t,t=1..5)+100/(1+y)^5.
Five annual year-end coupons, face 100, no default/call/tax/fees. Rates .01-.05
are teaching assumptions; update chapter and model together. Verified 2026-11-05.
"""
import numpy as np
from _style import C_BLUE,C_NAVY_SOFT,figure,save_chart,style_axes
rates=np.linspace(.01,.05,81)
prices=[sum(3/(1+r)**t for t in range(1,6))+100/(1+r)**5 for r in rates]
fig,ax=figure(ratio=.68);style_axes(ax)
ax.plot(rates*100,prices,color=C_BLUE)
ax.set_xlabel('假设到期收益率（%）');ax.set_ylabel('债券价格（元）')
ax.set_title('固定现金流：收益率升，价格降',loc='left')
fig.text(.02,-.01,'纯数学模型；面值 100、年票息 3、五年期，非实际报价。',fontsize=8,color=C_NAVY_SOFT)
fig.tight_layout();save_chart(fig,'ch10_bond_yields.png')
