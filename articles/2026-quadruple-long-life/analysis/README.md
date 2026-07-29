# 分析图表 — 数据来源与复现说明

> 所有图表由 `src/` 下的 Python 脚本生成，输出到 `output/`。  
> 运行：`cd src && pip install matplotlib pandas numpy && python ch*.py`

## 数据来源一览

| 图表 | 脚本 | 数据来源 | 获取方式 |
|------|------|----------|----------|
| Ch6 通胀 | `ch06_inflation.py` | 中国国家统计局 CPI 月度数据 | [stats.gov.cn](https://data.stats.gov.cn) → 居民消费价格指数(CPI) → 年度同比 |
| Ch7 亏损回本 | `ch07_drawdowns.py` | 纯数学计算 | `回本涨幅 = 1/(1-跌幅) - 1`，无需外部数据 |
| Ch9 货币基金 | `ch09_money_market.py` | 天弘余额宝 7日年化 + 人民银行活期利率 | [天天基金网](https://fund.eastmoney.com) → 余额宝历史收益；[pbc.gov.cn](http://www.pbc.gov.cn) → 存款基准利率 |
| Ch10 国债收益率 | `ch10_bond_yields.py` | 中国债券信息网中债收益率曲线 | [chinabond.com.cn](https://www.chinabond.com.cn) → 中债收益率 → 国债到期收益率 |
| Ch11 股票收益拆解 | `ch11_stock_returns.py` | Bloomberg / Wind 终端共识数据 | 专业终端导出（盈利增长、股息率、PE 变化）；或 [S&P DJI](https://www.spglobal.com/spdji/) + [中证指数](https://www.csindex.com.cn) 公开年报 |
| Ch12 黄金 | `ch12_gold.py` | 伦敦金定盘价 USD/oz（年化涨跌） | [LBMA](https://www.lbma.org.uk) 或 [World Gold Council](https://www.gold.org) |
| Ch15 QDII 溢价 | `ch15_qdii_premium.py` | 各 QDII-ETF 历史溢价率峰值 | [东方财富](https://quote.eastmoney.com) → ETF 详情页 → IOPV 折溢价历史 |
| Ch16 费率侵蚀 | `ch16_etf_fees.py` | 纯数学模拟 | `终值 = 本金 × (1 + 年化收益 - 费率)^年数`，参数见脚本注释 |
| Ch18 SPIVA | `ch18_spiva.py` | S&P SPIVA Scorecard（2024 年终） | [spglobal.com/spiva](https://www.spglobal.com/spdji/en/research-insights/spiva/) → 免费下载 PDF 报告 |
| Ch20 相关性 | `ch20_correlation.py` | 大类资产年化收益相关系数 | Bloomberg/Wind/Portfolio Visualizer 导出日收益 → 计算 Pearson 相关系数 |
| Ch27 微笑曲线 | `ch27_smile_curve.py` | 纯数学模拟 | V 形价格路径（100→50→100），参数见脚本注释 |
| Ch29 市场周期 | `ch29_market_cycles.py` | Bloomberg 终端沪深300 + 标普500 历史数据 | 终端导出年化回报；或 [Yahoo Finance](https://finance.yahoo.com) / [AKShare](https://github.com/akfamily/akshare) Python 库拉取 |

## 复现步骤

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install matplotlib pandas numpy

# 3. 运行所有脚本
cd src
python ch06_inflation.py
python ch07_drawdowns.py
# ... (依次运行)
# 或一次运行全部：
for f in ch*.py; do python "$f"; done
```

图表输出到 `../output/` 目录。

## 数据更新

本书图表基于 2024-2025 年度数据构建。如需要更新到最新年份：
1. 编辑对应脚本中的数据数组（均标注在脚本头部注释中）
2. 重新运行脚本
3. 输出 PNG 会自动覆盖

所有数值均已标注年份范围，方便定位更新点。
