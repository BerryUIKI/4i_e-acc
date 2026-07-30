# Sub Agent 注册流程 — 方案评估

> **Date**: 2026-07-30
> **Author**: 小花蟹 (f78f1d3e)
> **触发**: 花花提出 SUB 自注册 + Git 跟踪方案

---

## 花花提出的流程

```
MAIN → handoff → SUB（自注册：算ID、写roster、写定义文件）→ push → handoff → MAIN（整理、分配工作）
```

## 问题 1：是否需要 Git 跟踪 Sub Agent？

### 支持 Git 跟踪的理由

| 理由 | 说明 |
|------|------|
| 并行无冲突 | SUB 在自己分支操作，MAIN 在 main 或另一分支，互不干扰 |
| 有审计记录 | 注册操作有独立 commit，何时注册、谁注册、改了什么都可追溯 |
| 不怕丢失 | SUB 崩了、窗口关了，commit 在 remote 上，不会丢 |

### 反对 Git 跟踪的理由

| 理由 | 说明 |
|------|------|
| SUB push 违反 AGENTS.md 硬规则 | 需要改根规则：允许 SUB push 到自己的 feature branch |
| 需要花花手动操作 | SUB push 后 → PR → 合并，花花的环节不可跳过 |
| 当前规模不需要 | 单人、偶尔并行。注册文件总共 3 个（roster 一行 + sub-agent.md + context.md），不太可能丢 |

### 结论

Git 跟踪对**多设备、多 SUB、高频并行**场景有价值。对当前**单人偶尔并行**场景收益有限。**但架构设计应该考虑扩展性**，所以值得讨论。

核心矛盾不是"要不要 Git"，而是"谁 push"——AGENTS.md 硬规则说 SUB 不能 push。如果要让 SUB push，需要改为：**"SUB 可以 push 到自己的 feature branch，不可 push 到 main 或 integration branch。"**

---

## 问题 2：有没有更简便的办法？

### 方案 A：SUB 自注册（花花提出的）

```
步骤：
1. MAIN 写注册 handoff → 「请用以下参数注册自己」
2. 花花贴 prompt 到新窗口
3. SUB 读取参数 → 计算 SHA256 → 写 roster → 创建 sub-agent.md + context.md
4. SUB commit + push
5. SUB 写完成 handoff
6. 花花回到 MAIN 窗口
7. MAIN 读 handoff → 确认注册 → 分配任务

步骤数：7 步（含 2 次花花手动操作）
时间：跨 2 个窗口往返
```

### 方案 B：MAIN 代理注册（简便方案）

```
步骤：
1. MAIN 生成 Sub ID → 写 roster → 创建 sub-agent.md + context.md → commit
2. MAIN 直接把 startup prompt 给花花（prompt 里已含注册好的 ID）
3. 花花贴 prompt → SUB 直接开干（不需要知道注册过程）
4. SUB 干完 → 写 handoff → MAIN review

步骤数：4 步（含 1 次花花手动操作）
时间：SUB 窗口打开后一次性到位
```

### 对比

| | 方案 A (SUB 自注册) | 方案 B (MAIN 代理注册) |
|---|---|---|
| 步骤数 | 7 | 4 |
| 花花操作次数 | 2 | 1 |
| SUB 需要知道注册逻辑 | 是 | 否 |
| Git 历史 | SUB commit（独立） | MAIN commit（统一） |
| SUB push 冲突 | 需要改硬规则 | 无冲突 |
| 适合场景 | 多 SUB、需要独立审计 | 单人、快速启动 |

---

## 推荐

**当前阶段用方案 B（MAIN 代理注册）。**

理由：
- 快 3 步，少一次花花手动操作
- 不违反任何 AGENTS.md 规则
- SUB 不需要知道注册算法——它只需要知道"我是谁、干什么"（已经在 prompt 里了）

**如果将来真的到了「频繁并行、多人协作」的阶段**，再切到方案 A——那时 Git 跟踪的审计价值才能覆盖操作成本。

---

## 需要花花确认

1. 先走方案 B 吗？
2. 如果要为方案 A 做准备：是否现在就把 AGENTS.md 的 Sub push 硬规则改掉（"Sub 可 push 到自己的 feature branch"）？
