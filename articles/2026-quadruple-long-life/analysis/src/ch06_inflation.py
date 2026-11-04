"""Historical annual national CPI changes, NBS releases:
https://www.stats.gov.cn/sj/zxfb/202401/t20240112_1946465.html
https://www.stats.gov.cn/sj/zxfb/202501/t20250117_1958332.html
https://www.stats.gov.cn/sj/zxfb/202602/t20260228_1962662.html
2023 0.2%, 2024 0.2%, 2025 0.0%; no monthly data or forecast.
Retrieved/verified: 2026-11-05. Update source, manuscript, parameters and image together.
"""
from _style import C_BLUE,C_BRONZE,C_NAVY_SOFT,figure,save_chart,style_axes

labels=['2023', '2024', '2025']
values=[.2,.2,0]
fig,ax=figure(ratio=.70)
style_axes(ax)
ax.bar(labels,values,color=C_BLUE,width=.52)
span=max(values)-min(min(values),0) or 1
for i,v in enumerate(values):ax.text(i,v+span*.035,f'{v:.2f}',ha='center',fontsize=9,color=C_BRONZE)
ax.set_ylim(min(min(values),0)-span*.10,max(values)+span*.22)
ax.set_title('全国全年 CPI 涨幅：三个历史年份',loc='left')
ax.set_ylabel('较上年变化（%）')
fig.text(.02,-.01,'来源：国家统计局对应年度发布；不是未来通胀预测。',fontsize=8,color=C_NAVY_SOFT)
fig.tight_layout()
save_chart(fig,'ch06_inflation.png')
