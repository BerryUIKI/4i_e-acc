# 参考来源与计算口径

本登记册对应 2026-11-05 修订稿。历史观察与数学模型分开登记；旧稿中未取得可复核原始记录的多年收益、历史相关性矩阵、产品溢价峰值与最佳交易日统计已撤下。原审读报告是修订前快照，其中的旧数值不是现稿依据。

## 历史观察

以下均为公开一手材料，查阅日期：2026-11-05。报告时期与查阅日期分别记录，不将旧报告称为“最新”。

| 位置 | 数值与口径 | 具体来源 |
|---|---|---|
| Ch6 | 全国全年 CPI：2023 +0.2%、2024 +0.2%、2025 0.0%，非月度同比 | [2023 年发布](https://www.stats.gov.cn/sj/zxfb/202401/t20240112_1946465.html)、[2024 年发布](https://www.stats.gov.cn/sj/zxfb/202501/t20250117_1958332.html)、[2025 年统计公报](https://www.stats.gov.cn/sj/zxfb/202602/t20260228_1962662.html) |
| Ch12 | 黄金 2022 全年回报：美元 +0.4%、欧元 +6.7%、日元 +14.4%、人民币 +9.0%；LBMA PM 本币口径 | [世界黄金协会 2022 年 12 月报告，表 1](https://www.gold.org/goldhub/research/gold-market-commentary-december-2022) |
| Ch18 | 美国大盘主动股票基金一年跑输标普 500：2023 60%、2024 65% | [SPIVA U.S. Year-End 2024 官方介绍](https://www.spglobal.com/spdji/en/spiva/article/spiva-us-year-end-2024/) |

## 图表与纯数学模型

以下为本书教学输入，非预测、真实客户配置或历史市场序列。公式与全部输入记录在脚本头部及正文；复核日期：2026-11-05。除标为历史观察者外，均未使用外部市场数据。生成脚本位于 `analysis/src/`，图片位于 `analysis/output/`。

| 章 | 脚本 | 输入、方法与边界 |
|---|---|---|
| 6 | `ch06_inflation.py` | 上表三年的历史全年 CPI；不外推未来 |
| 7 | `ch07_drawdowns.py` | 回本涨幅 = 1/(1−跌幅)−1，无追加与提款 |
| 9 | `ch09_money_market.py` | 本金 10,000，固定有效年收益 1/2/3%，五年，无税费和资金流；非产品报价 |
| 10 | `ch10_bond_yields.py` | 面值 100、年末付息 3、五年还本，到期收益率 1%–5%，现金流折现，无违约/提前赎回/税费 |
| 11 | `ch11_stock_returns.py` | 初价 100、初始 EPS 5、期末 EPS 5.5、现金股息 2、期末 PE 16/20/24；单期总收益，不再投股息 |
| 12 | `ch12_gold.py` | 上表 2022 年四币种历史回报，不比较其他区间 CAGR |
| 15 | `ch15_qdii_premium.py` | 假设溢价 5/10/20/30%，净值不变、溢价归零，损失 p/(1+p)，无税费 |
| 16 | `ch16_etf_fees.py` | 本金 100,000，毛收益 7%，年度简化扣费，费率 0.15% 与 1%，三十年；不是不同真实产品的收益预测 |
| 18 | `ch18_spiva.py` | 上表同一美国基金分类、同一基准的两年历史比例 |
| 20 | `ch20_correlation.py` | 假想资产各占 50%，波动率 20/10%，相关系数 −0.5/0/0.8，按两资产方差公式计算；非历史矩阵 |
| 27 | `ch27_smile_curve.py` | 10 万元，正文所列十二期净值等额买入；未投现金零息保留，无费用与分红 |
| 29 | `ch29_market_cycles.py` | 初始 10 万、三期收益 −30/+20/+30% 及倒序，每年末取 1 万；无通胀与费用，非最佳交易日研究 |

复利与目标反推统一使用有效年收益率与月末投入。Python 核对模块为 `analysis/src/teaching_models.py`，网页共用公式为 `../../tools/shared/finance-math.js`；零收益率按累计投入计算。现金流单位与币种应在每个例子中保持一致。

## 机制与研究说明

- 资产配置与风险：[SEC 入门指南](https://www.sec.gov/investor/pubs/assetallocation.htm)、[Investor.gov 风险承受力](https://www.investor.gov/introduction-investing/investing-basics/save-and-invest/gauge-your-risk-tolerance)。
- 资产配置研究的解释边界：[CFA Institute 研究辨析](https://rpc.cfainstitute.org/blogs/enterprising-investor/2012/setting-the-record-straight-on-asset-allocation?page=0)。
- 货币基金风险：[Investor.gov 说明](https://www.investor.gov/introduction-investing/investing-basics/investment-products/mutual-funds-and-exchange-traded-5)。美国保障制度不直接套用于其他地区。
- 指数方法：[沪深 300 基金披露所附方法](https://www.sse.com.cn/disclosure/fund/announcement/c/new/2024-11-28/510330_20241128_SPIN.pdf)、[S&P 美国指数方法](https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-us-indices.pdf)；研究时另记录实际采用版本。
- ETF 机制：[Investor.gov 公告](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-24)、[上交所主动 ETF 指引](https://www.sse.com.cn/lawandrules/sselawsrules2025/fund/trading/c/c_20260617_10822565.shtml)。
- REITs：[Investor.gov 公开交易 REITs 公告](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-65)。

以上查阅日期均为 2026-11-05。税务与传承规则的具体来源另列于附录 M、N；不同司法辖区不直接类推。

## 更新与复核

图片重绘只证明图形可生成，不证明历史输入正确。新增历史数据须先记录具体序列、币种、日期、频率、分红口径与取得方式，再保留可核验记录；无法公开原始数据时说明授权限制及可复核出处。不要用供应商首页替代实际数据来源，也不要把手填数组说成程序抓取并计算的结果。

更新时同步正文、脚本、图片及本登记册，按 [复现说明](analysis/README.md) 运行与检查。历史观察不保证未来表现；数学模型的结果只在所列假设下成立。
