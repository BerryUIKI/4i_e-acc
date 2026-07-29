# Window: {name}

- **Window ID**: {name}
- **Type**: SUB
- **Sub Agent**: {sub-agent-name}
- **Status**: DEFINED
- **Current Task**: NONE
- **Created**: {date}

## Role

<!-- What this window does. One paragraph. -->

## Permissions

<!-- Which directories/files this window can modify. -->

## Constraints

<!-- Hard rules. Refer to root AGENTS.md and f78f1d3e/AGENTS.md. -->

## Startup Prompt

<!-- 花花 pastes this into a new WorkBuddy window. Keep it self-contained — assume the new window knows nothing. -->

```
你是 Main Agent f78f1d3e (小花蟹) 的一个子窗口。

你的角色：{role-description}

请先读取以下文件了解你的身份和任务：
1. agents/0101aaa313a11c56/f78f1d3e/context/{name}.md — 窗口定义
2. agents/0101aaa313a11c56/f78f1d3e/sub-agents/{sub-agent-name}.md — Sub Agent 角色
3. agents/0101aaa313a11c56/f78f1d3e/tasks/{task-id}.md — 当前任务

完成后的结果写入：agents/0101aaa313a11c56/f78f1d3e/handoffs/result-{task-id}.md
遇到阻塞写入：agents/0101aaa313a11c56/f78f1d3e/handoffs/blocked-{task-id}.md
```
