# 参考来源 / References

> 本书引用的外部数据与文献登记册。正文采用**内联来源标注**（章节图表下方的「数据来源：…」），
> 不使用脚注编号；本文件按章节汇总，供读者复核与复现。

## 图表数据来源

全部图表由 `analysis/src/` 下的 Python 脚本生成并输出到 `analysis/output/`，
复现步骤见 [`analysis/README.md`](analysis/README.md)。

| 章节 | 图表文件 | 脚本 | 数据来源 | 获取路径 |
|------|---------|------|----------|----------|
| Ch6 通胀 | `ch06_inflation.png` | `ch06_inflation.py` | 中国国家统计局 CPI 月度数据 | [data.stats.gov.cn](https://data.stats.gov.cn) → 居民消费价格指数 (CPI) → 年度同比 |
| Ch7 风险 | `ch07_drawdowns.png` | `ch07_drawdowns.py` | 纯数学计算 | 回本涨幅 = 1/(1 − 跌幅) − 1，无需外部数据 |
| Ch9 现金 | `ch09_money_market.png` | `ch09_money_market.py` | 天弘余额宝 7 日年化 + 人民银行活期利率 | [fund.eastmoney.com](https://fund.eastmoney.com) → 余额宝 (000198) 历史收益；[pbc.gov.cn](http://www.pbc.gov.cn) → 存款基准利率 |
| Ch10 债券 | `ch10_bond_yields.png` | `ch10_bond_yields.py` | 中国债券信息网中债收益率曲线 | [chinabond.com.cn](https://www.chinabond.com.cn) → 中债收益率 → 国债到期收益率 |
| Ch11 股票 | `ch11_stock_returns.png` | `ch11_stock_returns.py` | Bloomberg / Wind 终端共识数据 | 终端导出（盈利增长、股息率、PE 变化）；或 [S&P DJI](https://www.spglobal.com/spdji/) + [中证指数](https://www.csindex.com.cn) 公开年报 |
| Ch12 黄金 | `ch12_gold.png` | `ch12_gold.py` | 伦敦金定盘价 USD/oz 年化涨跌 | [LBMA](https://www.lbma.org.uk) 或 [World Gold Council](https://www.gold.org) |
| Ch15 溢价 | `ch15_qdii_premium.png` | `ch15_qdii_premium.py` | 各 QDII-ETF 历史溢价率峰值 | [东方财富](https://quote.eastmoney.com) → ETF 详情页 → IOPV 折溢价历史 |
| Ch16 费率 | `ch16_etf_fees.png` | `ch16_etf_fees.py` | 纯数学模拟 | 终值 = 本金 × (1 + 年化收益 − 费率)^年数，参数见脚本注释 |
| Ch18 主动基金 | `ch18_spiva.png` | `ch18_spiva.py` | S&P SPIVA Scorecard（2024 年终） | [spglobal.com/spiva](https://www.spglobal.com/spdji/en/research-insights/spiva/) → 免费下载 PDF |
| Ch20 配置 | `ch20_correlation.png` | `ch20_correlation.py` | 五大类资产年化收益相关系数 | Bloomberg / Wind 导出日收益 → Pearson 相关系数；替代来源 [Portfolio Visualizer](https://www.portfoliovisualizer.com) |
| Ch27 定投 | `ch27_smile_curve.png` | `ch27_smile_curve.py` | 纯数学模拟 | V 形价格路径（100→50→100），参数见脚本注释 |
| Ch29 周期 | `ch29_market_cycles.png` | `ch29_market_cycles.py` | Bloomberg 终端沪深300 + 标普500 历史数据 | 终端导出年化回报；替代来源 [Yahoo Finance](https://finance.yahoo.com) / [AKShare](https://github.com/akfamily/akshare) |

## 文献与报告

| 引用位置 | 文献 | 用途 |
|---------|------|------|
| Ch18 · 主动基金 | S&P Dow Jones Indices, *SPIVA Scorecard*（年度） | 主动基金跑输基准的比例 |
| Ch11 · 股票收益 | 杰里米·西格尔《股市长线法宝》(*Stocks for the Long Run*) | 总收益拆解的方法论框架 |
| Ch7 · 风险 | S&P Dow Jones Indices *History of Market* | 标普500 历史回撤与恢复时间 |

## 数据口径说明

- **Ch11 / Ch20 / Ch29**：所有回报均为**含分红再投资的总回报**，非价格指数。
- **Ch5 / Ch7 / Ch16 / Ch27**：纯教学数学模拟，参数标注在各脚本头部注释中，不代表历史表现。
- **时间窗**：图表数据基于 2024–2025 年度构建；更新方式见 `analysis/README.md` 的「数据更新」一节。

## 免责声明

所有数据与图表仅用于**教学与模拟**，不构成投资建议。历史表现不代表未来收益。
