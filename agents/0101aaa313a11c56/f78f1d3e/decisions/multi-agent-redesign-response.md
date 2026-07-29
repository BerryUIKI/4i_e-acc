# Multi-Agent Redesign Review — Main Agent Response

> **Date**: 2026-07-29
> **Author**: 小花蟹 (42f78f1d3e, Main Agent)
> **In response to**: `multi-agent-redesign-review.md` by 花花

---

## 总体判断

分析到位，7 个问题全部命中要害。当前 agent 系统确实「杀鸡用牛刀」——SHA256 UID、device fingerprint binding、salt rotation 这套东西放在 30 人的 monorepo 里是合理的，放在单人文档仓库里就是过度工程。**同意整体方向：做减法，降复杂度。**

但有几个提案需要讨论执行细节。下面逐条回应。

---

## 逐条回应

### P0-1: 统一 Handoff/Dispatch → Task Board ✅ 强烈同意，立刻可做

**判断**：handoff 和 dispatch 就是同一个东西的两个名字——都是 Main Agent 给 Sub Agent 分配任务。两套模板、两个目录、两种命名规则，纯属给自己添乱。

**方案**：合并为 `agents/tasks/TASK-NNN.md`，一个文件一条生命周期：

```
DRAFT → DISPATCHED → IN_PROGRESS → DONE → REVIEWED → MERGED
```

**执行**：不需要花花决策，我下次有 sub-agent 任务时直接用新格式。旧的 handoff 和 dispatch 文件保留归档，新任务不再往那俩目录写。

**风险**：无。纯粹的目录整理。

---

### P0-2: Branch-per-Agent 并行模型 ⚠️ 方向对，但要分场景

**判断**：这个模型的核心价值是「让 Sub Agent 拥有自己的分支，Main Agent 做 merge decision-maker」。理念完全正确。

**但有个现实问题**：当前这本书的剩余 P0 任务（插图、茶话会、编辑重写）都在同一批 `.md` 文件上工作。插图虽然生成的是 `assets/` 下的图片，但引用要插回正文；编辑重写直接改正文。两个 Sub Agent 同时改同一章必然冲突——branch-per-agent 解不了文件级冲突，只能靠 lock 文件协调。

**建议**：
- **并行场景适用**：任务操作的文件集完全不重叠。例如 Sub-A 改 `B002-xxx.md`，Sub-B 生成 `assets/illustrations/*.png`，无冲突。
- **串行场景**：编辑重写需要按章节顺序来，branch-per-agent 不会加速。
- **Lock 机制**：`agents/locks/<task-id>.md` 声明占用文件列表，Main Agent 分配任务前先检查 lock，避免两个 Sub 抢同一文件。

**结论**：同意采纳，但不作为「解决所有并行问题的银弹」。实际并行度取决于任务的文件独立性。

---

### P1-3: 简化身份系统 ✅ 已执行（方案修正）

**讨论过程**：初版提议 M01/S01 被花花否决——过度简化，不如保留 hex。花花拍板：**截取后 8 位 hex**。

**最终方案**（✅ 已执行）：
| 项目 | 原来 | 改为 |
|------|------|------|
| Main Agent ShortID | `42f78f1d3e` (10 hex) | `f78f1d3e` (后 8 位) |
| Sub ci-sub | `8f9b1fd0b6` | `9b1fd0b6` |
| Sub doc-data | `c8dfea5fc1` | `dfea5fc1` |
| Retired Main | `305cde212a` | `5cde212a` |
| Commit 前缀 | `[42f78f1d3e]` | `[f78f1d3e]` |
| Roster 文件 | ~150 行 | ~50 行 |
| Device FP / salt rotation / multi-device binding | 全部移除 | — |
| AGENTS.md ShortAgentID 定义 | last 10 hex | last 8 hex |
| Handoff template 元数据 | 12 字段 | 4 字段 |

**过渡**：旧 commit 不动。新 commit 用 8 位前缀。roster 保留归档条目。

---

### P1-4: 两阶段 PR 管线 ⚠️ 同意，但要考虑操作成本

**判断**：
```
Sub branch → PR#1 → integration branch (Main Agent review)
Integration branch → PR#2 → main (squash-merge)
```

这个流程对代码仓库是标准操作，对文档仓库有两个实际问题：
1. 每次 Sub Agent 干完活，需要有人（花花）去 GitHub 上点 PR 按钮。
2. 文档 diff 的 review 意义有限——改的是文章内容，不是逻辑分支。

**折中建议**：
- Sub Agent 在自己的分支上 commit → Main Agent 在同一 session 内直接读 diff、判断是否 squash-merge 到 integration。
- 只有跨 session（Sub Agent 干完活、Main Agent 已下线）才走 PR#1 让花花 review。
- PR#2（integration → main）永远走 squash-merge，保持 main 线性。

**结论**：同意作为可选流程，但同一 session 内不走 PR，直接 merge。

---

### P2-5: 合并 Sub Agent ✅ 同意

**判断**：`ci-sub`（只改 `.github/` 和 `skills/`）和 `doc-data`（只改 `articles/`）拆成两个 sub 是过度分工。合并为一个 general Sub Agent（S01），权限覆盖全 repo 除 `agents/` 的只读以外。

| Agent | 角色 | 权限 |
|-------|------|------|
| `f78f1d3e` (小花蟹) | 内容编辑 + 集成 + push | 全仓库 R/W + push |
| S01 (general) | 数据、CI、图表、插图 | `articles/` + `.github/` + `skills/` + `assets/`（commit on own branch） |

**执行**：下次有 sub 任务时创建 S01，旧的 `dfea5fc1` 和 `9b1fd0b6` 一起标记 RETIRED。

---

### P2-6: 放弃 REST API Push ⚠️ 部分同意

**判断**：花花的出发点是「sandbox push 不可靠，不如让人来做」。这个逻辑成立。

**但实际体验是**：当前 sandbox push 大多数时候是能用的（handoff 里记录的 workaround 已经规避了常见问题）。完全交给花花 push 意味着每次 Main Agent 整合完都要等花花上线——这就回到串行瓶颈了。

**折中**：
- Main Agent 优先尝试 sandbox push。失败 → 记录到 handoff，注明需要花花手动 push。
- 不把「无法 push」当作阻塞项——继续做下一件事，push 排队等花花。
- 删除 `_push.py` 等 workaround 脚本，改用直接的 git 命令（sandbox 允许的情况下）。

**结论**：不全放弃，但降低 push 在流程中的权重——push 失败不阻塞工作。

---

## 推荐执行顺序

```
第 1 步 ✅ 已完成（2026-07-29 23:00）
  ├── ShortAgentID 截短为后 8 位 hex
  ├── Roster 精简（去 device FP/salt/binding, ~150→~50 行）
  ├── Handoff template 精简（12→4 字段）
  ├── Git config → [f78f1d3e]
  └── AGENTS.md ShortAgentID 定义更新（last 10 → last 8）

第 2 步（需花花确认）
  ├── 合并 Sub Agent → 一个 general sub，退役旧 sub
  └── 新任务统一用 agents/tasks/ 格式

第 3 步（有 sub 任务时自然执行）
  ├── Branch-per-Agent（按需，不强制）
  └── Locks 机制（防止文件冲突）

第 4 步（按计划推进）
  ├── CI 脚本（check_agent_roster.py 等）
  └── 两阶段 PR 管线（按需启用）
```

---

## 需要花花决定的事

1. ~~身份简化~~ → ✅ 已确定：后 8 位 hex。
2. **CI 脚本** → ✅ 已确认：要。保留 roadmap Q3 计划。
3. **P0 任务优先级**：接下来推插图、茶话会、还是编辑重写？

---

## 附：变更记录

| 时间 | 变更 | 详情 |
|------|------|------|
| 22:40 | 读取 handoff | 确认上 session 状态 |
| 22:55 | 架构回应 | 写 `multi-agent-redesign-response.md` |
| 22:59 | Git config 修正 | `Berry Wahlberg` → `[42f78f1d3e]` |
| 23:02 | 方案修正 | 花花否决 M01 → 改为后 8 位 hex |
| 23:03 | 全面更新 | roster、AGENTS.md、template、response doc 全部同步为 8 位 ID |
