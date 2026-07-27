# 贡献指南

本仓库采用**基于 Pull Request 的工作流**。默认分支为 `main`。

> ⚠️ **强制力说明。** `BerryUIKI/4i_e-acc` 目前是 **GitHub 免费版的私有仓库**。GitHub 在免费私有库上不允许设置分支保护规则（如「要求 PR」「禁止直推」等），因此下面的规则是**约定，而非硬性拦截**——直接向 `main` 推送在技术上仍然可行。若日后仓库升级为 GitHub Pro 或改为公开，维护者可开启真正的分支保护（见下方「未来：强制保护」）。

## 工作流

1. **绝不直接提交到 `main`。** 始终从工作分支开始。
2. **分支命名**（英文、小写、连字符）：
   - `docs/<简短主题>` —— 文档改动（如 `docs/bilingual-readme`）
   - `article/<slug>` —— `articles/` 下的新文章（如 `article/quadruple-long-life`）
   - `fix/<简短主题>` —— 修复
   - `feat/<简短主题>` —— 新内容或新分区
3. **提交**时写明清晰的 message。推荐使用 Conventional Commits，如 `docs: add contributing guide`。
4. **推送**分支：`git push -u origin <branch>`。
5. **发起 Pull Request**，目标分支为 `main`。CODEOWNERS 会自动向 `@BerryUIKI` 请求审核。
6. **审核与合并。** 建议用 squash-merge 保持线性历史。合并后删除分支。

## 文章

长文位于 `articles/`，遵循 `articles/STYLE.md`（中文为主、英文混排），并使用 `articles/_template/` 中的单篇脚手架。

## 未来：强制保护

若仓库改为公开或升级 GitHub Pro，可在 `main` 上应用如下分支保护规则：

- 合并前必须走 Pull Request
- 至少 **1** 个审核通过
- `enforce_admins: true`（连所有者也不能绕过）
- 禁止 force push、禁止删除分支

维护者笔记中已保存可直接调用的 API 请求体。
