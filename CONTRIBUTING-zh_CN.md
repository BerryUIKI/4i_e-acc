# 贡献指南

本仓库采用**基于 Pull Request 的工作流**。默认分支为 `main`。仓库为**公开仓库**，且 `main` 已开启分支保护。

> **分支保护 —— 务实模式。** 对 `main` 的任何改动都必须经由 Pull Request。协作者（非管理员）至少需要 **1** 个审核通过。`enforce_admins` 为**关闭**状态，因此仓库所有者可以开 PR 并**自己合并（self-merge）**。所以管理员在技术上仍可直接 `git push` 到 `main`，但不建议这么做——请始终走 PR。对 `main` 的 force push 与删除分支，对所有人都是禁止的。

## 工作流

1. **绝不直接提交到 `main`。** 始终从工作分支开始。
2. **分支命名**（英文、小写、连字符）：完整前缀表见 [`BRANCHING-zh_CN.md`](./BRANCHING-zh_CN.md)。简版：
   - `docs/<简短主题>` —— 文档改动（如 `docs/bilingual-readme`）
   - `article/<yyyy-slug>` —— `articles/` 下的新文章（如 `article/2026-quadruple-long-life`）
   - `fix/<简短主题>` —— 修复
   - `ci/<简短主题>` —— CI / 工具
   - `feat/<简短主题>` —— 新内容或新分区
   - `chore/<简短主题>` —— 仓库维护
3. **提交**时写明清晰的 message。推荐使用 Conventional Commits，如 `docs: add contributing guide`。
4. **推送**分支：`git push -u origin <branch>`。
5. **发起 Pull Request**，目标分支为 `main`。CODEOWNERS 会自动向 `@BerryUIKI` 请求审核。
6. **审核与合并。** 建议用 squash-merge 保持线性历史。合并后删除分支。

## 文章

长文位于 `articles/`，遵循 `articles/STYLE.md`（中文为主、英文混排），并使用 `articles/_template/` 中的单篇脚手架。

## 补充说明

- 若日后想更严格（连所有者也不能自合并），可开启 `enforce_admins`——但那时需要第二个 GitHub 账号来审核所有者自己的 PR。
- CI 会在每个改动 `.md` 文件的 PR 上、以及每周定时运行（见 `.github/workflows/docs-checks.yml`）。
