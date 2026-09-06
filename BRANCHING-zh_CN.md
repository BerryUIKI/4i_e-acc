# 分支与协作工作流

本仓库采用**两级主干工作流**：功能分支 → `dev` → `main`。

- `main` 始终可发布。分支保护禁止直接推送（force-push 与删除分支同样被禁止，管理员也不例外）。
- `dev` 是日常写作的集成分支。分支保护要求必须走 PR（禁止直接推送，管理员也不例外）。
- 所有改动通过「短生命周期功能分支 → **PR 到 `dev`**（写作 / 内容工作）→ **PR 到 `main`**（发布）」合入。
- 作为仓库所有者，你可以**自合并** PR（务实模式）——即仍需开 PR，但无需外部审核人。`dev` 允许 0 审批自合并；`main` 要求 1 个审批（所有者可在需要时临时降级保护后自合并）。

## 分支命名

按意图加前缀。全部小写、连字符分隔、简短。一个分支只做一件逻辑改动。

| 前缀 | 用途 |
|------|------|
| `docs/<topic>` | 投资文档 / README 内容（`reports/`、`research/`、`portfolio/`、`market/`、`strategies/`、`data/`、`archive/`、`assets/`） |
| `article/<yyyy-slug>` | `articles/` 下新增或修订的长文 |
| `fix/<desc>` | 修复死链、错别字、结构问题 |
| `ci/<desc>` | `.github/` 下的 CI / GitHub Actions / 脚本 |
| `feat/<desc>` | 新的结构性功能（目录方案、模板） |
| `chore/<desc>` | 仓库维护（如本分支规范文档本身） |
| `epic/<milestone>` | **仅按需使用。** 需要整体验收的大里程碑主题分支（如 `epic/book-v0.2`）。汇集多条功能分支；里程碑验收后整体 squash 回 `dev` 并删除。永不常设。 |
| `release/vX.Y` | **仅按需使用。** 里程碑临近发布时从 `dev` 切出的发布冻结分支；在此修 bug，合并到 `main`（并回 `dev`），打 `vX.Y` tag，删除。永不常设。 |

示例：`docs/macro-q3-outlook`、`article/2026-quadruple-long-life`、`fix/broken-readme-links`、`ci/link-checker`。

## 规则

- 从**最新的 `dev`** 切分支（热修可从 `main` 切）；日常工作**合回 `dev`**。
- 分支保持**短生命周期**；一个分支只解决一件事。
- 使用 **squash 合并**保持历史线性；合并后删除分支。
- **内容达到发布标准时**（整书完成、配图就位、检查通过）才从 `dev` → `main` 开 PR 升级。
- 绝不提交密钥——仓库已**公开**。

## 主干模型（2026-09-07 采纳）

**常设主干只有两条**：`main`（稳定发布）与 `dev`（滚动集成）。

- 常规改动一律走「短生命周期功能分支 → PR → `dev` →（内容可发布时）→ `main`」。
- `epic/` 与 `release/` 分支**按需且临时**——只在某个里程碑确实需要时才多出这一层，用完即删；绝不当成第三条常设主干，否则 `dev` 会失去"唯一集成点"的角色，且每次合并都要多跳一层。
- 需要把一个大里程碑作为整体验收时，用**按需 `epic/<milestone>`**（多条相关功能分支合入它，验收后整体 squash 回 `dev`）。
- 临近发布时用**按需 `release/vX.Y`**：从 `dev` 切出，只修阻塞发布的 bug，合并到 `main`，在 `main` 打 `vX.Y` tag，再合并回 `dev` 并删除。
- 已发布版本用 `main` 上的 tag 标记（如 `v0.1`）。

## 生命周期

1. `git switch -c <prefix>/<name>`（从 `dev` 切出）
2. 编辑后提交。本仓库 `commit.gpgsign=true`（走 1Password SSH 密钥）；若你的环境无法签名，用 `git -c commit.gpgsign=false commit …`。
3. `git push -u origin <prefix>/<name>`
4. 向 `dev` 开 PR → 审核 / 自合并（squash）→ 删除分支。
5. 里程碑达到发布标准时，开 PR `dev` → `main` → 合并（squash）。
6. 可选 — 里程碑独立验收：从 `dev` 切 `epic/<milestone>`，经 PR 合入多条功能分支，验收后整体 squash 回 `dev` 并删除。
7. 可选 — 发布：从 `dev` 切 `release/vX.Y`，修阻塞发布的 bug，合并到 `main`（并回 `dev`），在 `main` 打 `vX.Y` tag，删除分支。

参见 `AGENTS.md`（面向 Agent 的摘要）与 `CONTRIBUTING.md`（完整人工工作流）。
