# 4i❤️e-acc —— 《四倍做多认知，长期做多人生》

<div align="center">

[![Language: English](https://img.shields.io/badge/Language-English-1D1E50?style=flat-square)](./README.md)
[![Language: 简体中文](https://img.shields.io/badge/语言-简体中文-B86C40?style=flat-square)](./README-zh_CN.md)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Site-0F6E56?style=flat-square)](https://berryuiki.github.io/4i_e-acc/)
[![Toolbox](https://img.shields.io/badge/Toolbox-10%20Bilingual%20Tools-E3A04B?style=flat-square)](https://berryuiki.github.io/4i_e-acc/tools/)
[![Desktop](https://img.shields.io/badge/Desktop-Tauri%202%20%7C%20Rust-FEC6CD?logo=tauri&logoColor=1D1E50&style=flat-square)](./desktop/)
[![Latest PDF](https://img.shields.io/github/v/release/BerryUIKI/4i_e-acc?label=PDF%20Release&color=1D1E50&style=flat-square)](https://github.com/BerryUIKI/4i_e-acc/releases)

**给普通人的长期投资指南 · FREE · 开放内容 · 纯本地运行**

[🌐 在线站点与工具箱](https://berryuiki.github.io/4i_e-acc/) · [📖 在线阅读书稿](./articles/2026-quadruple-long-life/README-zh_CN.md) · [📥 下载 PDF (v0.1)](https://github.com/BerryUIKI/4i_e-acc/releases) · [🧰 配套工具箱](./tools/) · [🖥️ 桌面客户端](./desktop/)

---

</div>

> **「AI 可以帮你把信息整理清楚，但『用你的钱去冒险』这个决定，只能由你来做。」**
> —— 《四倍做多认知，长期做多人生》第三十三章
>
> 不是荐股手册，也不是速富秘籍——这是一套把「资产配置、复利、定投、风险管理」讲给普通人听的方法论，外加一章「用 AI 管理你的财务」的清醒边界。全书 33 章正文 + 终章 + 12 份实用附录（约 12 万字），配套 10 款双语交互工具与 Tauri 跨平台桌面端，数据 100% 保存在本机，永远免费。

---

## 目录 (Table of Contents)

- [一、项目全景](#一项目全景)
- [二、长篇著作：《四倍做多认知，长期做多人生》](#二长篇著作四倍做多认知长期做多人生)
  - [2.1 全书九大板块](#21-全书九大板块)
  - [2.2 附录实用模板库](#22-附录实用模板库)
  - [2.3 PDF 自动化编译与获取](#23-pdf-自动化编译与获取)
- [三、配套双语工具箱 (Toolbox)](#三配套双语工具箱-toolbox)
  - [3.1 A 系列 · 数字工具箱 (6 款)](#31-a-系列--数字工具箱-6-款)
  - [3.2 B 系列 · AI 财务副驾驶 (4 款)](#32-b-系列--ai-财务副驾驶-4-款)
  - [3.3 工具核心设计规范](#33-工具核心设计规范)
- [四、桌面客户端 (Desktop Companion)](#四桌面客户端-desktop-companion)
  - [4.1 技术栈与架构](#41-技术栈与架构)
  - [4.2 快速运行与构建](#42-快速运行与构建)
- [五、仓库完整目录结构](#五仓库完整目录结构)
- [六、IP 人物与作者生态](#六ip-人物与作者生态)
  - [6.1 吉祥物：花有财 (DollarHua)](#61-吉祥物花有财-dollarhua)
  - [6.2 外部产品联动](#62-外部产品联动)
  - [6.3 关于作者](#63-关于作者)
- [七、开发协作与工作流](#七开发协作与工作流)
  - [7.1 分支管理策略](#71-分支管理策略)
  - [7.2 智能体协作与提交身份追溯](#72-智能体协作与提交身份追溯)
  - [7.3 CI/CD 自动化检查矩阵](#73-cicd-自动化检查矩阵)
- [八、免责声明与许可协议](#八免责声明与许可协议)

---

## 一、项目全景

`4i_e-acc`（Four-fold Long Cognitive Effective Accelerationism，四倍做多认知，长期做多人生）是一个长期投资知识与开源金融工具工程。

```
                     ┌──────────────────────────────────────────────┐
                     │ 4i❤️e-acc 认知体系                           │
                     │ 《四倍做多认知，长期做多人生》（12万字书稿） │
                     └──────────────────────┬───────────────────────┘
                                            │ 公式、原则与边界
                     ┌──────────────────────┴───────────────────────┐
                     ▼                                              ▼
    ┌─────────────────────────────────┐           ┌─────────────────────────────────┐
    │ 网页端工具箱 (GitHub Pages)     │           │ 桌面客户端 (Tauri 2 + Rust)     │
    │ · 纯静态单文件无网络依赖        │           │ · 原生窗口独立运行              │
    │ · 中英实时切换 + LocalStorage   │           │ · 本地文件对话框原生保存        │
    │ · Web 端一键下载与复制          │           │ · 零外部遥测，数据永不出设备    │
    └─────────────────────────────────┘           └─────────────────────────────────┘
                     │                                              │
                     └──────────────────────┬───────────────────────┘
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │ 衍生生态：AlphaForge (投研) + 蓝鲸记账 (日常)│
                     │ 吉祥物 IP：DollarHua (花有财)                │
                     └──────────────────────────────────────────────┘
```

---

## 二、长篇著作：《四倍做多认知，长期做多人生》

全书核心书稿收录于 [`articles/2026-quadruple-long-life/`](./articles/2026-quadruple-long-life/)，是一本专为零基础读者与家庭理财者撰写的咖啡馆风格长文。

### 2.1 全书九大板块

| 部分 | 对应章节 | 核心议题 | 产出小工具 |
|---|---|---|---|
| **第一部分 · 先看清自己的财务生活** | Ch1–Ch4 | 收入≠财富、个人净资产测算、储蓄率的魔力、负债分类与应急备用金安全垫 | [A6 五年规则检查器](./tools/five-year-rule-checker/) |
| **第二部分 · 理解收益、复利与风险** | Ch5–Ch8 | 复利的数学本质、隐形杀手通货膨胀、风险的真实含义与自身风险承受能力评估 | [A1 复利计算器](./tools/compound-calculator/) |
| **第三部分 · 钱到底可以放在哪里** | Ch9–Ch12 | 资产谱系全景：现金与货币基金、债券、股票、黄金及 REITs 另类资产特性 | — |
| **第四部分 · ETF 与基金的完整操作逻辑** | Ch13–Ch19 | 被动指数哲学、ETF 运作机制与申赎套利、**溢价率回归陷阱**、**管理费率复利侵蚀**、主动基金与 QDII 海外配置 | [A3 ETF 溢价率速算](./tools/etf-premium-calculator/)<br>[A4 费率侵蚀对比器](./tools/fee-erosion-calculator/) |
| **第五部分 · 家庭资产配置** | Ch20–Ch25 | 核心配置原则、资金三层分账法（日常/稳健/进攻）、**年龄动态配置模型**、不同家庭生命周期真实案例剖析、组合搭建与定期再平衡 | [A5 年龄配置建议器](./tools/age-allocation-advisor/) |
| **第六部分 · 真正开始投资** | Ch26–Ch28 | 迈出第一步心理障碍拆解、**定投（DCA）数学模型与微笑曲线**、投资日志与定期复盘方法论 | [A2 定投模拟器](./tools/dca-simulator/)<br>[B3 投资复盘生成器](./tools/review-generator/) |
| **第七部分 · 面对市场周期与人性** | Ch29–Ch30 | 牛熊周期演变规律、行为金融学（损失厌恶、心理账户、羊群效应与过度自信） | — |
| **第八部分 · 使用 AI 管理你的财务计划** | Ch31–Ch33 | **AI 自动化记账**与财务分类、**人生目标转财务数字规划**、**AI 投资辅助的三条红线与能力边界** | [B1 AI 记账对话包](./tools/ai-accounting-pack/)<br>[B2 人生目标翻译器](./tools/goal-translator/)<br>[B4 AI 投资红线卡](./tools/ai-redline-cards/) |
| **终章 · 终身财富之道** | H001 | 投资不是人生的目的；财富的终极意义是增加你生活与时间的选择权 | — |

### 2.2 附录实用模板库

位于 [`articles/2026-quadruple-long-life/Appendices/A-to-L-appendices.md`](./articles/2026-quadruple-long-life/Appendices/A-to-L-appendices.md)，包含 12 份开箱即用的落地表格与核对单：
- **附录 A**：家庭资产负债表与净资产月度自查表
- **附录 B**：家庭月度收支流水分类标准卡
- **附录 C**：家庭应急金储备月数测算矩阵
- **附录 D**：ETF 场内折溢价率风险速查对照表（高溢价买入回归损失速算）
- **附录 E**：常见指数分类与长期代表性 ETF 筛选清单
- **附录 F**：基金总费率（管理费+托管费+销售服务费）二十年侵蚀速查表
- **附录 G**：家庭「三个钱袋子」分账标准方案与资金划转规则
- **附录 H**：定投（DCA）扣款计划与动态再平衡操作备忘单
- **附录 I**：季度 / 年度投资复盘九问模版
- **附录 J**：不同年龄段与风险偏好资产配置基准参考区间
- **附录 K**：AI 理财助手 Prompt 指令精选合集
- **附录 L**：跨境投资与多司法管辖区资产自查警示清单

### 2.3 PDF 自动化编译与获取

- **GitHub Releases 下载**：每当里程碑标签（如 `v0.1`）打出时，GitHub Actions 自动化流水线自动调用 Pandoc 与 XeLaTeX 渲染排版，生成高印刷级 PDF 并发布在 [Releases 页面](https://github.com/BerryUIKI/4i_e-acc/releases)。
- **本地编译指南**：具备 XeLaTeX 环境时，进入 `skills/pdf-toolbook/` 即可通过脚本离线重新编译完整图书。

---

## 三、配套双语工具箱 (Toolbox)

所有工具均位于 [`tools/`](./tools/) 目录，采用单文件 HTML/CSS/JavaScript 原生架构，零第三方 CDN 依赖，保证在无网环境下完全可用。

在线体验入口：**[https://berryuiki.github.io/4i_e-acc/tools/](https://berryuiki.github.io/4i_e-acc/tools/)**

### 3.1 A 系列 · 数字工具箱 (6 款)

把书中的核心数学模型化为读者可触碰的实时算盘：

1. **[复利计算器 (Compound Calculator)](./tools/compound-calculator/)**：
   - 对应章节：Ch5、Ch27
   - 核心功能：本金 + 月定投 + 年化收益率 → 终值增长动态曲线、72 法则翻倍年限预估、25 岁 vs 35 岁起步造成的终值残酷差距对比。
2. **[定投模拟器 (DCA Simulator)](./tools/dca-simulator/)**：
   - 对应章节：Ch27
   - 核心功能：单笔一次性投入 vs 分月定投对比，完整呈现微笑曲线（跌深反弹）下的平均持仓成本削峰填谷优势。
3. **[ETF 溢价率速算 (ETF Premium Calculator)](./tools/etf-premium-calculator/)**：
   - 对应章节：Ch15、附录 D
   - 核心功能：输入市价与 IOPV 净值，瞬间得出实时溢价率与回归净值时的预期本金亏损，附带 10 档防套牢速查表。
4. **[费率侵蚀对比器 (Fee Erosion Comparator)](./tools/fee-erosion-calculator/)**：
   - 对应章节：Ch16、附录 F
   - 核心功能：对比两只基金费率差（如 0.2% vs 1.5%），通过复利模拟揭示 10~30 年后被中介机构吃掉的惊人财富比例。
5. **[年龄配置建议器 (Age Allocation Advisor)](./tools/age-allocation-advisor/)**：
   - 对应章节：Ch22、附录 J
   - 核心功能：基于年龄基准规则结合应急金月数、收入波动度、负债率 4 问加权，生成个性化配置区间与「不适用例外情形」警示。
6. **[五年规则检查器 (Five-Year Rule Checker)](./tools/five-year-rule-checker/)**：
   - 对应章节：Ch4
   - 核心功能：输入资金使用期限与对应资产，严格判定风险匹配度；坚决拦截「五年内要买房/读书的钱放进高波动股市」的行为。

### 3.2 B 系列 · AI 财务副驾驶 (4 款)

针对 AI 时代个人理财流程定制的结构化交互工具：

1. **[花有财记账对话包 (AI Accounting Prompt Pack)](./tools/ai-accounting-pack/)**：
   - 对应章节：Ch31
   - 核心功能：包含分类助手、收支复盘、现金流预测、边界守护 4 组经严格打磨的专业记账 Prompt，一键复制，与作者的「蓝鲸记账」无缝配套。
2. **[人生目标翻译器 (Life Goal Translator)](./tools/goal-translator/)**：
   - 对应章节：Ch32
   - 核心功能：将「买房置业、教育金储备、提早退休自由」等模糊情感目标，拆解并精确翻译为月度储蓄率与刚性定投金额。
3. **[投资复盘生成器 (Investment Review Generator)](./tools/review-generator/)**：
   - 对应章节：Ch28、附录 I
   - 核心功能：四问引导（纪律遵从、盈亏归因、情绪波动、执行纠偏），快速生成标准化 Markdown 复盘记录，支持一键复制。
4. **[AI 投资红线卡 (AI Investing Red-Line Cards)](./tools/ai-redline-cards/)**：
   - 对应章节：Ch33
   - 核心功能：清晰陈列「绝不交出账户控制权、绝不迷信单一预测、绝不在看不懂的复杂衍生品上下注」三张打印级红线自律卡。

### 3.3 工具核心设计规范

- 🌐 **双语原生**：所有工具页面右上角均可单键自由切换中文与 English。
- 💾 **输入记忆**：自动监听输入变化并保存至本地 `localStorage`，重新打开或刷新浏览器时自动恢复历史计算参数。
- ⚡ **实时响应**：参数变动实时触发数学计算与 SVG 图表刷新，提供 `重置 / Reset` 按钮恢复默认预设值。
- 📤 **多模导出**：
  - 在 **Web 浏览器** 下：点击「导出结果」直接生成 `.txt` 文件并通过浏览器下载，伴有平滑悬浮 Toast 提示；
  - 在 **Tauri 桌面端** 下：直接唤起 Windows/macOS 原生文件保存对话框。
- 🧭 **三级双向导航**：顶部集成快捷导航栏（支持直达图书主页、工具箱索引、或通过下拉框在 10 款工具间一秒切换）。

---

## 四、桌面客户端 (Desktop Companion)

位于 [`desktop/`](./desktop/)，是将工具箱原生化的跨平台桌面应用。

### 4.1 技术栈与架构

- **核心驱动**：Tauri 2 (Rust) + 系统原生 WebView (Windows WebView2 / macOS WebKit / Linux WebKitGTK)
- **依赖管理**：基于 **pnpm** 统一管理 `@tauri-apps/cli`，杜绝全局 cargo/tauri 版本冲突
- **代码同源**：直接指向仓库内的 `../../tools` 目录（`frontendDist: "../../tools"`），无需冗余构建或维护第二套前端框架
- **原生能力桥接**：通过 `window.__TAURI__.core.invoke("export_result", ...)` 调起操作系统原生 Save File 对话框

### 4.2 快速运行与构建

运行前请确保本地已安装 [Rust 编译环境](https://www.rust-lang.org/) 以及 [Node.js & pnpm](https://pnpm.io/)。

```bash
# 1. 进入桌面项目目录
cd desktop

# 2. 安装 pnpm 依赖
pnpm install

# 3. 本地开发与热重载运行
pnpm tauri dev

# 4. 构建独立生产安装包 (.exe / .msi / .app / .deb)
pnpm tauri build
```

---

## 五、仓库完整目录结构

```
4i_e-acc/
├── .github/                      # GitHub 配置与自动化
│   ├── workflows/                # CI/CD 工作流定义
│   │   ├── deploy-pages.yml      # GitHub Pages 自动部署 (dev push)
│   │   ├── docs-checks.yml       # 链接检查、样式与 Markdown 检查
│   │   ├── pr-language-check.yml # PR 语言英文主导性检查
│   │   └── build-book-pdf.yml    # PDF 自动编译与 Release 发布
│   └── scripts/                  # CI 质检脚本 (check_links.py 等)
├── .nojekyll                     # 禁用 GitHub Pages Jekyll 引擎
├── index.html                    # 网站门户主页（书籍简介 + 工具箱导流）
├── AGENTS.md                     # 智能体协作硬约束与身份生成协议
├── BRANCHING.md                  # 分支策略与双主干工作流（dev/main）
├── CONTRIBUTING.md               # 贡献者指引（双语）
├── TOOLBOX-ROADMAP.md            # 工具与产品演进规划总表
├── articles/                     # 长篇著作与深度研究文稿
│   └── 2026-quadruple-long-life/ # 《四倍做多认知，长期做多人生》完整书稿
│       ├── Front-Matter/         # 扉页、阅读须知、作者的话、目录、序章
│       ├── Main-Text/            # 33 章正文 (A001~I003) + 终章 (H001)
│       ├── Appendices/           # 12 份实用附录模板 (A-to-L)
│       └── analysis/             # 真实市场数据分析脚本与图表源
├── tools/                        # 10 款双语交互工具源代码
│   ├── index.html                # 工具箱主索引导航页
│   ├── compound-calculator/      # A1 复利计算器
│   ├── dca-simulator/            # A2 定投模拟器
│   ├── etf-premium-calculator/   # A3 ETF 溢价率速算
│   ├── fee-erosion-calculator/   # A4 费率侵蚀对比器
│   ├── age-allocation-advisor/   # A5 年龄配置建议器
│   ├── five-year-rule-checker/   # A6 五年规则检查器
│   ├── ai-accounting-pack/       # B1 AI 记账对话包
│   ├── goal-translator/          # B2 人生目标翻译器
│   ├── review-generator/         # B3 投资复盘生成器
│   └── ai-redline-cards/         # B4 AI 投资红线卡
├── desktop/                      # Tauri 2 跨平台原生桌面工程
│   ├── src-tauri/                # Rust 核心逻辑与系统桥接
│   └── package.json              # pnpm CLI 管理脚本
├── assets/                       # 静态资源、IP 视觉素材
│   ├── favicon.svg               # DollarHua 猫耳铜钱矢量 Favicon
│   └── dollarhua/                # 吉祥物 DollarHua (花有财) 设定与三视图
├── scripts/                      # 运维辅助脚本 (sync_gh_pages.py 等)
├── reports/                      # 专题深度研报与季报归档
├── research/                     # 底层宏观专题研究笔记
├── portfolio/                    # 经典资产配置组合历史回测
├── market/                       # 市场周期与突发流动性复盘
├── strategies/                   # 资产配置策略量化回测白皮书
├── data/                         # 原始统计数据与佐证源
└── archive/                      # 历史旧版文稿与迭代存档
```

---

## 六、IP 人物与作者生态

### 6.1 吉祥物：花有财 (DollarHua)

<div align="center">
  <img src="./assets/dollarhua/references/front_transparent.png" alt="DollarHua 花有财" width="160" />
  <p><i>「蓬松白发、白色猫耳、粉色连帽衫、古铜钱挂坠 —— 陪伴你的长期理财向导」</i></p>
</div>

- **角色定位**：全书插画、教学案例及配套工具的主角形象。
- **象征意义**：铜钱代表理性的财富计算，粉衫猫耳代表亲切近人的温度与长期耐心。
- **设计标准**：详见 [`assets/dollarhua/`](./assets/dollarhua/) 与 IP 设定规范。

### 6.2 外部产品联动

本书理念与作者正在研发维护的软硬件产品深度联结：

1. **[AlphaForge](https://github.com/BerryUIKI/alpha-forge)**（开源 · AGPLv3）：
   - 定位：**高端 AI 原生投研工作台**（Tauri + React + Rust + SQLite 本地向量数据库）。
   - 角色：书中第三十三章「研究侧的 AI」落地范例，把非结构化的原始投研信息提炼为严谨的知识结构。
2. **蓝鲸记账 (BlueWhale)**（Apple 原生闭源 · Swift / macOS / iOS / iPadOS）：
   - 定位：**极简无干扰的个人生活记账工具**。标语：*「记好当下，岁岁有余」*。
   - 角色：书中第三十一章「AI 记账」的实践载体，本书工具 [B1 记账对话包](./tools/ai-accounting-pack/) 即为其官方配套指令集。

### 6.3 关于作者

- **花花 (@BerryUIKI)**：独立研究者（AI 基础设施 · 芯片半导体 · 数据中心算力）× 投资内容创作者。
- 白天追踪前沿算力芯片与硬件产业链，夜晚致力于将严谨的投资数学、资产配置与风险控制框架科普给普通读者。

---

## 七、开发协作与工作流

本仓库秉承高度自动化、严谨可追溯的工程化规范（详见 [`AGENTS.md`](./AGENTS.md) 与 [`BRANCHING.md`](./BRANCHING.md)）。

### 7.1 分支管理策略

采用 **双主干模型 (Two-Tier Trunks)**：

```
功能分支 (feat/*, docs/*, fix/*) 
       │ 
       ▼ (Pull Request + CI 校验)
  dev 分支 (滚动作业与日常集成)
       │
       ▼ (里程碑验收完成)
  main 分支 (正式发布版本，严格只读)
```

- 🚫 **严禁直接向 `main` 或 `dev` 分支推送代码**，必须通过 PR 审查合并。
- 自动化发布：向 `dev` 分支合并将自动触发 Pages 部署流水线同步到 `gh-pages` 分支。

### 7.2 智能体协作与提交身份追溯

为保障多智能体并行编程的可靠性，仓库实施严格的 Git 身份规范：
- 每次 Commit 信息的标题必须带有对应的 `[ShortAgentID]` 前缀（如当前主控智能体为 `[f78f1d3e]`）。
- 提交前自动验证 committer 邮箱与注册表一致性。

### 7.3 CI/CD 自动化检查矩阵

提交 PR 时，GitHub Actions 会自动执行以下严格准入测试：
1. **`language-check`**：确保 PR 标题与说明以英文为主，保障跨国协作可读性。
2. **`link-check`**：静态分析全库 400+ 相对链接与锚点，坚决杜绝 404 断链。
3. **`style-check`**：校验 Markdown 规范、ASCII 纯净路径及目录命名准则。
4. **`markdown-lint`**：严格检查排版与格式。

---

## 八、免责声明与许可协议

### 8.1 教学与免责声明

> [!WARNING]
> 1. 本仓库所包含之全部文章、模拟工具、图表、附录及代码**仅供学习与教学研究参考**，在任何情况下均**不构成**买入、卖出或持有任何金融资产的投资建议、财务规划或法定建议。
> 2. 书中所有历史数据与测算案例均为假设模型，**历史收益绝不代表未来表现**。金融市场具有不可预测之波动风险，入市须保持独立判断与审慎态度。
> 3. 所有工具均在读者本地环境运行，开发者不收集、不存储、亦不对用户的实际财务行为或损失承担任何法律责任。

### 8.2 知识产权与许可

- **书籍文稿内容**（`articles/`、`reports/` 等）：遵循 [知识共享 署名-非商业性使用-相同方式共享 4.0 国际许可协议 (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)。欢迎自由转载与引用，但必须注明原作者署名，且不得用于任何商业盈利目的。
- **源代码与小工具工程**（`tools/`、`desktop/`、`scripts/`）：遵循 [MIT License](./LICENSE) 开源许可。
- **吉祥物 IP**（DollarHua / 花有财形象）：版权由作者花花所有，保留一切商业衍生权益。

---

<div align="center">
  <b>4i❤️e-acc · 认知是最好的杠杆，时间是最厚的朋友。</b><br>
  欢迎 Star ⭐️ 关注项目进展，或在 Discussions 交流你的长期理财心得！
</div>
