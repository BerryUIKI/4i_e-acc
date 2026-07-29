# Window: MAIN

- **Window ID**: MAIN
- **Type**: MAIN
- **Status**: ACTIVE
- **Created**: 2026-07-29

## Role

The primary window for Main Agent f78f1d3e (小花蟹). This is the WorkBuddy session where 花花 interacts directly.

**MAIN is the default executor.** Most tasks are done here directly. 花花 gives instructions, MAIN executes.

## Safety rule: do NOT run multiple Context Windows concurrently

**同一 Agent 下多个 Context Window 同时改仓库文件是高风险操作。** locks/ 文件锁不能完全防止竞态条件——如果两个窗口同时启动、同时读取、同时动手，锁就失效了。

Context Window 的正确姿态：**串行接力，不做并行。** 新窗口接旧窗口的活，旧窗口关了再行动。

如果确实需要并行：用 **Sub Agent**（独立 Git 分支，merge 有天然保护）。

---

## When to open a new window

### Rule: different things, different windows

**不是同一类的事情，开新窗口。** 清空上下文，每个窗口专注一件事。

| 触发条件 | 开什么窗口 | 关键约束 |
|----------|-----------|----------|
| **换任务类型** | 新 MAIN 窗口 | 旧窗口不再动仓库文件 |
| **上下文太长**（> 50 轮） | 新 MAIN 窗口 | 写完交接后旧窗口停手 |
| **需要并行** | Sub Agent（不是 Context Window） | 独立分支 Git merge |

### When NOT to

- 同一件事的连续步骤 → 同一窗口继续
- 上下文还够、话题没换 → 不折腾
- 想同时跑两个窗口改文件 → **不要**。用 Sub Agent 或者顺序来

---

## Intra-Agent handoff (同 Agent 窗口切换)

同 Agent 内部窗口切换是**接力**，不是并行。旧窗口写交接，新窗口接手。

### 简短交接（< 5 行信息）

直接放代码框给花花复制到新窗口：

```
你是 f78f1d3e (小花蟹)。当前任务：编辑重写 P0 #5。
分支：article/2026-quadruple-long-life
先读：agents/0101aaa313a11c56/f78f1d3e/decisions/multi-agent-redesign-review.md（找 editorial review 内容）
```

### 文件交接（内容较长时）

写文件到 `handoffs/`，新窗口启动时读取。文件格式不拘泥模板，信息密度优先。

---

## Inter-Agent handoff (跨 Agent 通信)

跨 Agent 通信（Main ↔ Sub Agent）走标准 handoff 格式：`agents/shared/templates/handoff.md`。

---

## Permissions

Full repo read/write + git push.

## Constraints

- Never push to `main` directly — always branch + PR (root AGENTS.md hard rule)
- Do not run concurrent Context Windows that modify the repo
- Do not close this window with unreviewed SUB results

## Startup Prompt

No startup prompt needed — 花花 talks directly.
