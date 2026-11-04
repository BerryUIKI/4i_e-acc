"""Ch18: historical one-year US large-cap active-fund underperformance.

Source: S&P SPIVA U.S. Year-End 2024 introduction, accessed 2026-11-05:
https://www.spglobal.com/spdji/en/spiva/article/spiva-us-year-end-2024/
Reported values: 2023 60%, 2024 65%, relative to the S&P 500.
Update: retain report dates and category; replace data only from the same report.
"""
from _style import C_BLUE, C_BRONZE, C_NAVY_SOFT, figure, save_chart, style_axes
fig, ax = figure(ratio=.68)
style_axes(ax)
ax.bar(['2023', '2024'], [60,65], color=[C_BLUE,C_BRONZE], width=.5)
for i,v in enumerate([60,65]): ax.text(i,v+2,f'{v}%',ha='center',fontsize=10)
ax.set_ylim(0,100)
ax.set_ylabel('一年跑输基准的基金占比（%）')
ax.set_title('美国大盘主动股票基金：两个历史年份',loc='left')
fig.text(.02,-.01,'基准：标普 500；来源：SPIVA U.S. Year-End 2024 官方介绍。',fontsize=8,color=C_NAVY_SOFT)
fig.tight_layout()
save_chart(fig,'ch18_spiva.png')
