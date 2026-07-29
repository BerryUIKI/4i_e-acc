# Multi-Window Collaboration — Workflow

> See also: `agents/0101aaa313a11c56/f78f1d3e/decisions/multi-window-architecture.md` for the full architecture.

## Two parallel modes

| Mode | Identity | Branch | Push | Conflict |
|------|----------|--------|------|----------|
| **Sub Context Window** | Same as MAIN | Same branch | No (MAIN pushes) | `locks/` |
| **Sub Agent** | Own ShortAgentID | `sub/{id}/{task}` | Yes (own branch) | Git merge |

---

## A. Sub Context Window (轻量并行)

### Communication

1. MAIN writes task: `agents/0101aaa313a11c56/f78f1d3e/tasks/TASK-NNN.md`
2. MAIN checks `locks/`, tells 花花: "开窗口，贴 prompt"
3. SUB reads context definition + task → executes
4. SUB writes result: `agents/0101aaa313a11c56/f78f1d3e/handoffs/result-TASK-NNN.md`
5. MAIN reviews → integrates → pushes

### Startup prompt

```
你是 Main Agent f78f1d3e (小花蟹) 的一个子上下文窗口。

请先读取：
1. agents/0101aaa313a11c56/f78f1d3e/context/{name}.md
2. agents/0101aaa313a11c56/f78f1d3e/tasks/{task-id}.md

完成后写结果：agents/0101aaa313a11c56/f78f1d3e/handoffs/result-{task-id}.md
改文件前先在 agents/0101aaa313a11c56/f78f1d3e/locks/ 创建锁。不要 push。
```

### Lock protocol

- Granularity: per chapter (`B002.md.lock`, `G001.md.lock`)
- Lock before touching any file. Delete when done.
- MAIN checks locks before assigning tasks.

---

## B. Sub Agent (正式并行)

### Communication

1. MAIN writes registration handoff: `agents/0101aaa313a11c56/f78f1d3e/handoffs/register-{task-slug}.md`
2. 花花 opens new window, pastes registration prompt
3. SUB self-registers: computes ShortAgentID, writes roster, creates `sub-agents/{name}.md` and `context/{name}.md`
4. SUB configures git identity (`[{id}]` / `{id}@agents.local`)
5. SUB creates branch `sub/{id}/{task-slug}`, commits registration files, pushes
6. SUB writes confirmation: `agents/0101aaa313a11c56/f78f1d3e/handoffs/registered-{id}.md`
7. MAIN reads handoff → assigns task → SUB executes → result handoff → MAIN review
8. MAIN opens PR from `sub/{id}/{task-slug}` → review → squash-merge to integration branch
9. MAIN marks Sub Agent RETIRED in roster

### Registration prompt

```
你是 Main Agent f78f1d3e (小花蟹) 即将注册的一个 Sub Agent。

你的任务：自注册。

1. 计算你的 ShortAgentID：
   SHA256("{device_fp}|{role}|f78f1d3e|{utc_ms}|022a2e4326219260")，取后 8 位
   device_fp = SHA256("{hostname}-{username}")，取前 16 位

2. 注册到 agents/0101aaa313a11c56/f78f1d3e/roster.md

3. 创建你的角色定义：agents/0101aaa313a11c56/f78f1d3e/sub-agents/{name}.md
4. 创建你的上下文窗口：agents/0101aaa313a11c56/f78f1d3e/context/{name}.md

5. 配置 git：git config user.name "[{your-id}]" / git config user.email "{your-id}@agents.local"

6. 创建分支 sub/{your-id}/{task-slug}，commit 所有��册文件，push

7. 写 handoff：agents/0101aaa313a11c56/f78f1d3e/handoffs/registered-{your-id}.md
```

### Branch naming

```
sub/{ShortAgentID}/{task-slug}
```

Example: `sub/cb544a5b/illustrations-ch3-5`

---

## Session handoff checklist (MAIN window)

Before ending a MAIN window session:

- [ ] All Sub Context Windows done or their results archived
- [ ] All Sub Agent PRs reviewed or documented for next session
- [ ] No leftover locks in `locks/`
- [ ] No tokens, keys, or secrets in any committed file
