"""Ch29: pure mathematical return-sequence and withdrawal model.
Source: balance=prior_balance*(1+return)-1, starting balance 10 (ten-thousand CNY).
Sequences (-.3,.2,.3) and (.3,.2,-.3); withdraw 1 at each year end. No inflation,
fees or taxes, no real market data. Update chapter alongside model, 2026-11-05.
"""
from _style import C_BLUE,C_BRONZE,C_NAVY_SOFT,figure,save_chart,style_axes
fig,ax=figure(ratio=.70);style_axes(ax)
for returns,label,color in [((-.3,.2,.3),'先跌后涨',C_BLUE),((.3,.2,-.3),'先涨后跌',C_BRONZE)]:
 values=[10.]
 for r in returns:values.append(values[-1]*(1+r)-1)
 ax.plot(range(4),values,label=label,color=color,marker='o')
 ax.text(3,values[-1]+.2,f'{values[-1]:.2f} 万',ha='right',color=color,fontsize=9)
ax.set_xticks(range(4));ax.set_xlabel('年末（0 为起点）');ax.set_ylabel('提款后余额（万元）')
ax.set_title('同一组收益，不同顺序与提款结果',loc='left');ax.legend(loc='upper left')
fig.text(.02,-.01,'纯数学模型；初始 10 万，每年末提款 1 万，不代表市场路径。',fontsize=8,color=C_NAVY_SOFT)
fig.tight_layout();save_chart(fig,'ch29_market_cycles.png')
