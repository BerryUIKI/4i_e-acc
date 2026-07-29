# Multi-Window Agent Architecture

> **Date**: 2026-07-30
> **Author**: 小花蟹 (f78f1d3e)
> **Status**: 已采纳，已执行

---

## 1. 核心原则

> **一台设备一个 Main Agent。两种并行方式：Sub Context Window（轻量，同分支）和 Sub Agent（独立身份，各走各分支）。**

---

## 2. 概念定义

### 2.1 Main Agent

一台设备上有且仅有一个 Main Agent。当前：`f78f1d3e`（小花蟹）。

### 2.2 Sub Context Window —— 轻量并行

同 Main Agent 身份，同分支干活。适合文件不重叠的简单并行。

| 特性 | 说明 |
|------|------|
| 身份 | 同 Main Agent |
| 注册 | 不注册 |
| 分支 | 同分支 |
| Push | 不 push（MAIN 统一 push） |
| 防冲突 | `locks/`（按章节） |
| 通信 | `tasks/` + `handoffs/` |

### 2.3 Sub Agent —— 正式并行开发

独立 ShortAgentID，自己的分支，自己 push，MAIN 通过 PR 合并。适合可能冲突的同目录并发。

| 特性 | 说明 |
|------|------|
| 身份 | 独立 ShortAgentID，注册在 roster |
| 分支 | `sub/{ShortAgentID}/{task-slug}` |
| Push | 可 push 到自己的分支 |
| 防冲突 | Git merge（天然支持） |
| 通信 | handoff：注册指令 → SUB 自注册 + push → handoff 回传结果 → MAIN review |

### 2.4 决策树

```
需要并行？

  改不同文件/目录？（不重叠）
    ├── 是 → Sub Context Window（简单快）
    └── 否 →

  同目录并发？可能冲突？需要独立审计？
    ├── 是 → Sub Agent（独立分支）
    └── 不确定 → Sub Context Window 先试
```

---

## 3. 目录结构

```
agents/
├── AGENTS.md                          ← 根规则（硬规则）
│
├── shared/                            ← 跨 Main Agent 共享
│   ├── references/                    ← data-provenance, dollarhua-ip, file-naming
│   ├── workflows/                     ← git-safety, multi-agent-collaboration
│   └── templates/                     ← handoff, sub-agent, task
│
└── f78f1d3e/                         ← Main Agent 专属
    ├── AGENTS.md                      ← 本 Main 规则
    ├── roster.md                      ← Agent 注册表
    ├── roadmap.md                     ← 路线图
    ├── sub-agents/                    ← Sub Agent 角色定义（按需，空时仅 _template.md）
    ├── context/                       ← 上下文窗口定义（MAIN.md + 按需 SUB）
    ├── tasks/                         ← 任务分配
    ├── locks/                         ← 文件锁（Sub Context Window 用）
    ├── handoffs/                      ← 跨窗口/跨 Agent 通信
    └── decisions/                     ← 重大决策记录
```

---

## 4. 窗口生命周期（Context Window）

Sub Context Window 和 Sub Agent 窗口共用此生命周期：

```
DEFINED → ACTIVE → WORKING → DONE → CLOSED
```

| 状态 | 含义 |
|------|------|
| `DEFINED` | 定义文件存在，窗口未开 |
| `ACTIVE` | 窗口已开，等待任务 |
| `WORKING` | 正在执行任务 |
| `DONE` | 任务完成，等 MAIN 审核 |
| `CLOSED` | 任务归档 |

---

## 5. 任务流转

### 路径 1：MAIN 直接干（默认）

```
花花 → MAIN → 干活 → commit → push。完成。
```

### 路径 2：Sub Context Window（轻量并行）

```
MAIN 写 task → 检查 locks/ → 花花开窗口贴 prompt → SUB 干活 → handoff 回传
→ MAIN review → 集成 push
```

### 路径 3：Sub Agent（正式并行）

```
MAIN 写注册 handoff → 花花开窗口贴 prompt → SUB 自注册（算 ID、写 roster、
sub-agent.md、context.md）→ SUB commit + push 到 sub/{id}/{task} 分支 →
SUB 写结果 handoff → MAIN 读 handoff → MAIN PR review → squash merge → 退役 SUB
```

---

## 6. 锁机制（Sub Context Window 专用）

Sub Agent 不需要 locks/——Git 分支本身隔离了冲突。

Sub Context Window 在改文件前创建 `locks/{安全文件名}.lock`。粒度：按章节。

---

## 7. Sub Agent 注册流程

1. MAIN 确定需要 Sub Agent（同目录并发、需要独立审计）
2. MAIN 写注册 handoff：`handoffs/register-{task-slug}.md`，含 role 描述、允许的工作目录
3. 花花开新 WorkBuddy 窗口，贴 handoff 里的 prompt
4. SUB 计算 ShortAgentID（SHA256 算法），写入 roster，创建 `sub-agents/{name}.md` 和 `context/{name}.md`
5. SUB 创建分支 `sub/{ShortAgentID}/{task-slug}`，commit 所有注册文件，push
6. SUB 写完成 handoff：`handoffs/registered-{ShortAgentID}.md`
7. MAIN 读到 handoff → 分配具体任务 → SUB 执行 → handoff 回传 → MAIN review → PR merge → roster 标记 RETIRED

---

## 8. 分支命名规范

### Sub Agent 分支

```
sub/{ShortAgentID}/{task-slug}
```

- `ShortAgentID`: Sub Agent 的后 8 位 hex
- `task-slug`: 短横线分隔的任务描述（英文小写）

示例：
```
sub/cb544a5b/illustrations-ch3-5
sub/cb544a5b/editorial-rewrites
sub/cb544a5b/ci-pdf-fix
```

### 其他分支（沿用现有）

| 前缀 | 用途 |
|------|------|
| `article/` | 书稿/文章 |
| `fix/` | bug 修复 |
| `feat/` | 新功能 |
| `ci/` | CI 变更 |
| `sub/` | Sub Agent 工作分支 |

---

## 9. 确认记录

| # | 问题 | 结果 |
|---|------|------|
| 1 | 目录结构 | ✅ `agents/0101aaa313a11c56/f78f1d3e/` 专属目录 |
| 2 | 窗口启动 | ✅ 手动开窗口贴 prompt |
| 3 | 锁粒度 | ✅ 按章节（Sub Context Window） |
| 4 | Sub Agent 概念 | ✅ 与 Sub Context Window 区分，独立分支 + push + PR |
| 5 | MAIN 角色 | ✅ 默认执行者，不是纯协调者 |
| 6 | windows/ → context/ | ✅ 已重命名 |
| 7 | Sub Agent 按需注册 | ✅ 不预注册 |
| 8 | 分支规范 | ✅ `sub/{id}/{slug}` |
