# 4i❤️e-acc — Quadruple Leverage on Cognition, Long Life

<div align="center">

[![Language: English](https://img.shields.io/badge/Language-English-1D1E50?style=flat-square)](./README.md)
[![Language: 简体中文](https://img.shields.io/badge/语言-简体中文-B86C40?style=flat-square)](./README-zh_CN.md)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Site-0F6E56?style=flat-square)](https://berryuiki.github.io/4i_e-acc/)
[![Toolbox](https://img.shields.io/badge/Toolbox-10%20Bilingual%20Tools-E3A04B?style=flat-square)](https://berryuiki.github.io/4i_e-acc/tools/)
[![Desktop](https://img.shields.io/badge/Desktop-Tauri%202%20%7C%20Rust-FEC6CD?logo=tauri&logoColor=1D1E50&style=flat-square)](./desktop/)
[![Latest PDF](https://img.shields.io/github/v/release/BerryUIKI/4i_e-acc?label=PDF%20Release&color=1D1E50&style=flat-square)](https://github.com/BerryUIKI/4i_e-acc/releases)

**A Long-Term Investing Guide for Ordinary People · FREE · Open Content · 100% Local-First**

[🌐 Live Site & Toolbox](https://berryuiki.github.io/4i_e-acc/) · [📖 Read Manuscript Online](./articles/2026-quadruple-long-life/README.md) · [📥 Download PDF (v0.1)](https://github.com/BerryUIKI/4i_e-acc/releases) · [🧰 Bilingual Toolbox](./tools/) · [🖥️ Desktop Companion](./desktop/)

---

</div>

> **"AI can help you organize information, but the decision to risk your money is yours alone."**
> — *Quadruple Leverage on Cognition, Long Life*, Chapter 33
>
> Not a stock-tip handbook, not a get-rich-quick scheme — this is a sober, caffeine-friend style framework for everyday people: understanding asset allocation, compounding, dollar-cost averaging (DCA), and risk management, plus a candid chapter on using AI for your personal finances. It contains 33 main chapters + an epilogue + 12 practical appendices (~120,000 words in Chinese/English), accompanied by 10 bilingual interactive web tools and a Tauri desktop companion app. 100% runs locally, zero data leaves your machine, and always free.

---

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. The Book: *Quadruple Leverage on Cognition, Long Life*](#2-the-book-quadruple-leverage-on-cognition-long-life)
  - [2.1 Nine Major Book Parts](#21-nine-major-book-parts)
  - [2.2 Appendix Templates Library](#22-appendix-templates-library)
  - [2.3 Automated PDF Compilation & Releases](#23-automated-pdf-compilation--releases)
- [3. Companion Bilingual Toolbox](#3-companion-bilingual-toolbox)
  - [3.1 Part A · Numeric Tools (6 Tools)](#31-part-a--numeric-tools-6-tools)
  - [3.2 Part B · AI Financial Co-Pilot (4 Tools)](#32-part-b--ai-financial-co-pilot-4-tools)
  - [3.3 Key Design Principles](#33-key-design-principles)
- [4. Desktop Companion App](#4-desktop-companion-app)
  - [4.1 Stack & Architecture](#41-stack--architecture)
  - [4.2 Quick Start & Build](#42-quick-start--build)
- [5. Repository Directory Structure](#5-repository-directory-structure)
- [6. Mascot IP & Author Ecosystem](#6-mascot-ip--author-ecosystem)
  - [6.1 Mascot: DollarHua (花有财)](#61-mascot-dollarhua-花有财)
  - [6.2 Product Ecosystem Connections](#62-product-ecosystem-connections)
  - [6.3 About the Author](#63-about-the-author)
- [7. Development & Collaboration Workflow](#7-development--collaboration-workflow)
  - [7.1 Branching Strategy (Two-Tier Trunks)](#71-branching-strategy-two-tier-trunks)
  - [7.2 Agent Git Identity & Traceability](#72-agent-git-identity--traceability)
  - [7.3 Automated CI Check Matrix](#73-automated-ci-check-matrix)
- [8. Disclaimer & License](#8-disclaimer--license)

---

## 1. Project Overview

`4i_e-acc` (Four-fold Long Cognitive Effective Accelerationism / 四倍做多认知，长期做多人生) is an open-source long-term investment knowledge and financial tools project.

```
                     ┌──────────────────────────────────────────────┐
                     │ 4i❤️e-acc Knowledge Engine                    │
                     │ Book: Quadruple Leverage (120k words)        │
                     └──────────────────────┬───────────────────────┘
                                            │ Formulas, Principles & Boundaries
                     ┌──────────────────────┴───────────────────────┐
                     ▼                                              ▼
    ┌─────────────────────────────────┐           ┌─────────────────────────────────┐
    │ Web Toolbox (GitHub Pages)      │           │ Desktop App (Tauri 2 + Rust)    │
    │ · Pure static single-file HTML  │           │ · Native OS window & UI         │
    │ · ZH / EN live toggle           │           │ · Native OS file save dialog    │
    │ · Persistent input memory       │           │ · Zero telemetry, 100% offline  │
    │ · One-click download & copy     │           │ · Zero network dependencies     │
    └─────────────────────────────────┘           └─────────────────────────────────┘
                     │                                              │
                     └──────────────────────┬───────────────────────┘
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │ Ecosystem: AlphaForge (Research) + BlueWhale │
                     │ Mascot IP: DollarHua (花有财)                │
                     └──────────────────────────────────────────────┘
```

---

## 2. The Book: *Quadruple Leverage on Cognition, Long Life*

The complete book manuscript is maintained under [`articles/2026-quadruple-long-life/`](./articles/2026-quadruple-long-life/). It is written in an accessible, friendly conversational tone designed for beginner to intermediate self-directed investors.

### 2.1 Nine Major Book Parts

| Part | Chapters | Core Topic | Companion Tool |
|---|---|---|---|
| **Part I · Understand Your Finances First** | Ch1–Ch4 | Income ≠ wealth; net worth calculation; the magic of savings rate; debt classification and emergency funds | [A6 Five-Year Rule Checker](./tools/five-year-rule-checker/) |
| **Part II · Returns, Compounding & Risk** | Ch5–Ch8 | Mathematical compounding; the invisible inflation tax; real nature of risk and measuring risk capacity | [A1 Compound Calculator](./tools/compound-calculator/) |
| **Part III · Where Money Can Live** | Ch9–Ch12 | Comprehensive asset spectrum: cash, money funds, bonds, equities, gold, and REITs | — |
| **Part IV · ETFs & Funds End-to-End** | Ch13–Ch19 | Passive indexing philosophy; ETF creation/redemption mechanics; **the premium reversion trap**; **fee compounding erosion**; active funds and cross-border QDII | [A3 ETF Premium Calculator](./tools/etf-premium-calculator/)<br>[A4 Fee Erosion Comparator](./tools/fee-erosion-calculator/) |
| **Part V · Household Asset Allocation** | Ch20–Ch25 | Core allocation principles; three-bucket accounting (daily, safety, offensive); **dynamic age-based models**; real lifecycle case studies; portfolio construction and periodic rebalancing | [A5 Age Allocation Advisor](./tools/age-allocation-advisor/) |
| **Part VI · Actually Start Investing** | Ch26–Ch28 | Breaking the first-trade paralysis; **dollar-cost averaging (DCA) mathematical models and the smile curve**; investment journaling and systematic reviews | [A2 DCA Simulator](./tools/dca-simulator/)<br>[B3 Investment Review Generator](./tools/review-generator/) |
| **Part VII · Market Cycles & Human Nature** | Ch29–Ch30 | Bull/bear cycle mechanics; behavioral finance (loss aversion, mental accounting, herd behavior, and overconfidence) | — |
| **Part VIII · AI for Your Financial Plan** | Ch31–Ch33 | **Automated AI bookkeeping** and categorization; **translating life goals into financial numbers**; **three inviolable red lines and boundaries of AI in investing** | [B1 AI Accounting Prompt Pack](./tools/ai-accounting-pack/)<br>[B2 Life Goal Translator](./tools/goal-translator/)<br>[B4 AI Investing Red-Line Cards](./tools/ai-redline-cards/) |
| **Epilogue · The Lifelong Wealth Way** | H001 | Investing is not the goal of life; the ultimate purpose of wealth is expanding your freedom of choice and personal agency | — |

### 2.2 Appendix Templates Library

Located in [`articles/2026-quadruple-long-life/Appendices/A-to-L-appendices.md`](./articles/2026-quadruple-long-life/Appendices/A-to-L-appendices.md), providing 12 battle-tested templates:
- **Appendix A**: Household Balance Sheet & Monthly Net Worth Ledger
- **Appendix B**: Monthly Income/Expense Categorization Standard Card
- **Appendix C**: Emergency Fund Requirement Matrix
- **Appendix D**: ETF Premium/Discount Loss Lookup Table
- **Appendix E**: Broad-Based Index Classifications & Representative ETF Checklist
- **Appendix F**: 20-Year Cumulative Fee Erosion Matrix
- **Appendix G**: Three-Bucket Family Asset Separation Scheme
- **Appendix H**: Dollar-Cost Averaging & Dynamic Rebalancing Protocol
- **Appendix I**: Quarterly & Annual Investment Review 9-Question Template
- **Appendix J**: Age-Bracket & Risk-Tolerance Asset Allocation Reference Ranges
- **Appendix K**: Curated AI Financial Prompt Collection
- **Appendix L**: Multi-Jurisdiction & Cross-Border Compliance Checklist

### 2.3 Automated PDF Compilation & Releases

- **Download Pre-compiled PDFs**: Every milestone release tag (e.g. `v0.1`) triggers a GitHub Actions workflow that renders the entire manuscript via Pandoc and XeLaTeX into a print-ready PDF, published on the [GitHub Releases page](https://github.com/BerryUIKI/4i_e-acc/releases).
- **Local Compilation**: If you have a local XeLaTeX environment, you can run the offline build script in `skills/pdf-toolbook/`.

---

## 3. Companion Bilingual Toolbox

All 10 interactive tools live in [`tools/`](./tools/). Each is implemented as a single self-contained HTML/CSS/JavaScript file with zero CDN dependencies, guaranteeing 100% offline functionality.

Live Web Access: **[https://berryuiki.github.io/4i_e-acc/tools/](https://berryuiki.github.io/4i_e-acc/tools/)**

### 3.1 Part A · Numeric Tools (6 Tools)

Turning the mathematical formulas from the book into interactive simulations:

1. **[Compound Calculator](./tools/compound-calculator/)** (Ch5, Ch27):
   Principal + monthly contribution + expected return → growth curve, Rule of 72 doubling timeline, and the cost of waiting (age 25 vs 35 starting age comparison).
2. **[DCA Simulator](./tools/dca-simulator/)** (Ch27):
   Lump-sum vs monthly dollar-cost averaging, illustrating the cost-dampening advantage in a smile-curve dip.
3. **[ETF Premium Calculator](./tools/etf-premium-calculator/)** (Ch15, Appendix D):
   Market price vs NAV → real-time premium rate and expected principal loss upon reversion, with a 10-step lookup guide.
4. **[Fee Erosion Comparator](./tools/fee-erosion-calculator/)** (Ch16, Appendix F):
   Visualizing how an expense gap (e.g. 0.2% vs 1.5%) compounds into a massive wealth disparity over 10–30 years.
5. **[Age Allocation Advisor](./tools/age-allocation-advisor/)** (Ch22, Appendix J):
   Age rule weighted by emergency fund cushion, income volatility, and debt ratio → tailored allocation ranges and boundary caveats.
6. **[Five-Year Rule Checker](./tools/five-year-rule-checker/)** (Ch4):
   Time horizon × asset volatility match check; intercepting the dangerous mistake of parking 5-year goal funds into volatile equities.

### 3.2 Part B · AI Financial Co-Pilot (4 Tools)

Structured workflows and prompts designed for everyday personal financial planning with AI:

1. **[AI Accounting Prompt Pack](./tools/ai-accounting-pack/)** (Ch31):
   Four copy-ready prompts (categorization, monthly review, cash flow forecasting, boundary guard) tailored for the BlueWhale ledger.
2. **[Life Goal Translator](./tools/goal-translator/)** (Ch32):
   Translating vague dreams (buying a home, children's education, early retirement) into concrete monthly savings numbers and disciplined timelines.
3. **[Investment Review Generator](./tools/review-generator/)** (Ch28, Appendix I):
   Guided 4-part inquiry (discipline, attribution, emotion, corrections) producing clean, structured Markdown review journals.
4. **[AI Investing Red-Line Cards](./tools/ai-redline-cards/)** (Ch33):
   Printable desk cards containing the three never-cross boundary rules: never surrender custody, never trust black-box predictions, never trade unhedged derivatives.

### 3.3 Key Design Principles

- 🌐 **Native Bilingual**: Switch between English and Simplified Chinese seamlessly in the header.
- 💾 **Persistent Input Memory**: Automatically remembers your previous calculations via `localStorage`.
- ⚡ **Reactive Real-Time Updates**: Instantly recalculates values and updates SVG charts as inputs change, with a `Reset Defaults` button.
- 📤 **Universal Export**:
  - In **Web Browsers**: Direct `.txt` file download with smooth Toast notifications.
  - In **Tauri Desktop**: Native system file save dialog.
- 🧭 **Multi-Tier Navigation**: Fast breadcrumb buttons (Home, Toolbox, and a quick dropdown switcher across all 10 tools).

---

## 4. Desktop Companion App

Located in [`desktop/`](./desktop/), providing a native desktop package for the toolbox.

### 4.1 Stack & Architecture

- **Engine**: Tauri 2 (Rust) + OS Native Webview (Windows WebView2 / macOS WebKit / Linux WebKitGTK).
- **Package Management**: Managed through **pnpm** (`@tauri-apps/cli`), preventing global cargo/tauri conflicts.
- **Shared Codebase**: Reuses [`../../tools`](./tools/) directly (`frontendDist: "../../tools"`), keeping a single source of truth.
- **Native Bridge**: Direct bridge through `window.__TAURI__.core.invoke("export_result", ...)` for system file save dialogs.

### 4.2 Quick Start & Build

Make sure [Rust](https://www.rust-lang.org/) and [Node.js with pnpm](https://pnpm.io/) are installed locally.

```bash
# 1. Navigate to desktop directory
cd desktop

# 2. Install dependencies
pnpm install

# 3. Launch local dev window
pnpm tauri dev

# 4. Build native production installer (.exe / .msi / .app / .deb)
pnpm tauri build
```

---

## 5. Repository Directory Structure

```
4i_e-acc/
├── .github/                      # GitHub workflows and automation scripts
│   ├── workflows/                # CI/CD workflows
│   │   ├── deploy-pages.yml      # Automated GitHub Pages deploy on dev push
│   │   ├── docs-checks.yml       # Link check, Markdown lint & style rules
│   │   ├── pr-language-check.yml # Enforces English as primary language in PRs
│   │   └── build-book-pdf.yml    # Auto-compile PDF and publish to Releases
│   └── scripts/                  # CI validation scripts (check_links.py, etc.)
├── .nojekyll                     # Disables Jekyll processing on GitHub Pages
├── index.html                    # Live web landing portal (Book intro + Toolbox)
├── AGENTS.md                     # Agent collaboration guidelines and identity protocol
├── BRANCHING.md                  # Two-tier branching workflow (dev/main)
├── CONTRIBUTING.md               # Human-facing contribution guide
├── TOOLBOX-ROADMAP.md            # Master roadmap for tools and author products
├── articles/                     # Long-form manuscripts and essays
│   └── 2026-quadruple-long-life/ # Full book manuscript
│       ├── Front-Matter/         # Opening, reading notice, author note, TOC, prologue
│       ├── Main-Text/            # 33 chapters (A001–I003) + Epilogue (H001)
│       ├── Appendices/           # 12 appendix templates (A-to-L)
│       └── analysis/             # Market data scripts and chart sources
├── tools/                        # 10 bilingual interactive web tools
│   ├── index.html                # Toolbox portal navigation page
│   ├── compound-calculator/      # A1 Compound Calculator
│   ├── dca-simulator/            # A2 DCA Simulator
│   ├── etf-premium-calculator/   # A3 ETF Premium Calculator
│   ├── fee-erosion-calculator/   # A4 Fee Erosion Comparator
│   ├── age-allocation-advisor/   # A5 Age Allocation Advisor
│   ├── five-year-rule-checker/   # A6 Five-Year Rule Checker
│   ├── ai-accounting-pack/       # B1 AI Accounting Prompt Pack
│   ├── goal-translator/          # B2 Life Goal Translator
│   ├── review-generator/         # B3 Investment Review Generator
│   └── ai-redline-cards/         # B4 AI Investing Red-Line Cards
├── desktop/                      # Tauri 2 native desktop wrapper
│   ├── src-tauri/                # Rust core and native dialog commands
│   └── package.json              # pnpm CLI runner
├── assets/                       # Static media and brand IP assets
│   ├── favicon.svg               # DollarHua coin mascot SVG favicon
│   └── dollarhua/                # Mascot DollarHua (花有财) specifications
├── scripts/                      # Maintenance and deployment utilities
├── reports/                      # Investment research notes and earnings memos
├── research/                     # Macro research and literature notes
├── portfolio/                    # Asset allocation case studies and backtests
├── market/                       # Market regime analysis and liquidity reviews
├── strategies/                   # Systematic strategy playbooks
├── data/                         # Verified datasets and provenance sources
└── archive/                      # Historical drafts and superseded notes
```

---

## 6. Mascot IP & Author Ecosystem

### 6.1 Mascot: DollarHua (花有财)

<div align="center">
  <img src="./assets/dollarhua/references/front_transparent.png" alt="DollarHua Mascot" width="160" />
  <p><i>"Fluffy white hair, cat ears, pink hoodie, bronze coin pendant — your long-term investing companion."</i></p>
</div>

- **Role**: The character starring in all teaching examples, diagrams, and tools throughout the book.
- **Design Guidelines**: Refer to [`assets/dollarhua/`](./assets/dollarhua/) and IP reference documents.

### 6.2 Product Ecosystem Connections

The concepts in this project connect directly with the author's real-world software tools:

1. **[AlphaForge](https://github.com/BerryUIKI/alpha-forge)** (Open Source · AGPLv3):
   - **Positioning**: High-end AI-native investment research workbench (Tauri + React + Rust + local SQLite vector database).
   - **Connection**: Highlighted in Chapter 33 as a tangible example of "research-side AI" transforming raw financial data into structured knowledge.
2. **BlueWhale Ledger (蓝鲸记账)** (Apple-Native Private Software · Swift):
   - **Positioning**: Minimalist, private personal finance tracker for iOS/macOS. Tagline: *"Record the present, thrive with surplus."*
   - **Connection**: Practical counterpart for Chapter 31's AI bookkeeping principles; companion prompt tool [B1](./tools/ai-accounting-pack/) is specifically designed for it.

### 6.3 About the Author

- **Huahua (@BerryUIKI)**: Independent researcher (AI Infrastructure · Semiconductors · Data Centers) × investing content creator.
- Spends daylight hours studying silicon chips and compute infrastructure, and evenings distilling disciplined investment mathematics and risk management for everyday individuals.

---

## 7. Development & Collaboration Workflow

This repository adheres to strict automation and provenance standards (see [`AGENTS.md`](./AGENTS.md) and [`BRANCHING.md`](./BRANCHING.md)).

### 7.1 Branching Strategy (Two-Tier Trunks)

```
Feature Branch (feat/*, docs/*, fix/*)
       │
       ▼ (Pull Request + Automated CI)
   dev Branch (Rolling integration trunk)
       │
       ▼ (Milestone release tag)
  main Branch (Stable public release trunk)
```

- 🚫 **Never push directly to `main` or `dev`**; all changes require a short-lived branch and PR.
- Merging to `dev` automatically deploys the latest static site and tools to the `gh-pages` branch.

### 7.2 Agent Git Identity & Traceability

All commits must carry the registered agent prefix in the message title:
- Format: `[ShortAgentID] <type>: <description>` (e.g. `[f78f1d3e] feat: ...`).
- Local git config must match the ShortAgentID recorded in `roster.md`.

### 7.3 Automated CI Check Matrix

Every PR triggers automated GitHub Actions checks:
1. **`language-check`**: Validates that PR titles and descriptions are primarily in English for transparent international collaboration.
2. **`link-check`**: Exhaustively verifies 400+ internal markdown links and cross-references.
3. **`style-check`**: Checks formatting rules, ASCII-only path names, and kebab-case file structures.
4. **`markdown-lint`**: Enforces consistent typography and markdown syntax.

---

## 8. Disclaimer & License

### 8.1 Educational & Investment Disclaimer

> [!WARNING]
> 1. All articles, tools, spreadsheets, diagrams, and code in this repository are for **educational, simulation, and academic purposes only**. Under no circumstances do they constitute investment advice, financial planning, or recommendations to buy, sell, or hold any financial asset.
> 2. All historical data and test cases are hypothetical simulations. **Past returns never guarantee future results**. Financial markets involve inherent volatility and risk of capital loss.
> 3. All tools run entirely in the user's local browser or desktop environment. The authors collect no telemetry and accept no legal liability for any personal financial decisions or outcomes.

### 8.2 Licensing & Intellectual Property

- **Book Manuscript & Educational Content** (`articles/`, `reports/`, etc.): Licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/). You are free to share and adapt the material with appropriate attribution for non-commercial purposes.
- **Source Code & Interactive Tools** (`tools/`, `desktop/`, `scripts/`): Licensed under the open-source [MIT License](./LICENSE).
- **Mascot IP** (DollarHua / 花有财): All character likeness and derivative rights are reserved by author Huahua.

---

<div align="center">
  <b>4i❤️e-acc · Cognition is your greatest leverage; time is your deepest ally.</b><br>
  Star ⭐️ this repo to follow along, or share your thoughts in GitHub Discussions!
</div>
