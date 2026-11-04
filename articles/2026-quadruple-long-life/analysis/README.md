# 图表复现与数据边界

对应 2026-11-05 修订稿；具体来源、取得日期、公式和参数见 [参考登记册](../references.md) 与各脚本头部。现稿保留三组可回查历史观察：2023–2025 全年 CPI、2022 黄金四币种回报、SPIVA 美国大盘主动基金两年一年期比例。其余图表均为明确参数的纯数学模型，不能称作历史实证。

## 运行

在仓库根目录运行，需 Python、matplotlib、numpy，以及 `_style.py` 支持的一种简体中文字体：

```bash
python -m pip install matplotlib numpy
python articles/2026-quadruple-long-life/analysis/src/teaching_models.py
python articles/2026-quadruple-long-life/analysis/src/ch27_smile_curve.py
node tools/shared/finance-math.test.cjs
```

其他图表逐个运行相应 `chNN_*.py`，输出到本目录 `output/`，会覆盖同名生成图片。运行前确认当前分支和改动，生成后对照正文及真实放置尺寸检查图例、单位、图注与裁切。

`ch01_data_verification.py` 现仅复算书中年金数值，不再宣称验证未提供原始记录的历史数据。`teaching_models.py` 与网页 `tools/shared/finance-math.js` 使用有效年收益率与月末投入；零收益场景单独处理。

## 更新

先确定历史观察还是数学模型，再修改输入。历史图必须指向具体材料和统计口径；模型图必须完整列出假设。正文与图不同步时不要发布。已撤下的多年终端共识统计与手填相关性矩阵不应仅因旧图片仍可打开而重新引用；旧版可在 Git 历史中查阅。
