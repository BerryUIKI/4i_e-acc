# 配图生成 — 交接文档

> 写给后续接手配图工作的 AI Agent 或人工编辑。

## 当前进度

| 文件 | 状态 | 来源 | 比例 | 说明 |
|------|------|------|------|------|
| 00-cover.png | ✅ 已就位 | 花花生成 | 2:3 | 封面，flatten PNG（压缩版，待替换） |
| 01-preface.png | ✅ 已就位 | 花花生成 | 16:9 | PNG 高清原图（3 张之一） |
| 02-compounding.png | ✅ 已就位 | 花花生成 | 4:3 | PNG 高清原图（3 张之一） |
| 03-cognition-leverage.png | ⚠️ 占位 | 小花蟹(Pending) | 1:1 | 1:1 比例，待花花生成 |
| 04-asset-baskets.png | ✅ 已就位 | 花花生成 | 4:3 | PNG 高清原图（3 张之一） |
| 05-dca-stairs.png | ⚠️ 占位 | 小花蟹(Pending) | 4:3 | 待花花生成 |
| 06-boat-waves.png | ⚠️ 占位 | 小花蟹(Pending) | 16:9 | 待花花生成 |
| 07-asset-tree.png | ⚠️ 占位 | 小花蟹(Pending) | 4:3 | 待花花生成 |
| 08-smile-curve.png | ⚠️ 占位 | 小花蟹(Pending) | 4:3 | 待花花生成 |
| 09-fund-pyramid.png | ❌ 缺失 | — | 3:4 | 未生成 |
| 10-family-portfolio.png | ❌ 缺失 | — | 4:3 | 未生成 |
| 11-bull-bear-thermometer.png | ❌ 缺失 | — | 3:4 | 未生成 |
| 12-inflation-ghost.png | ❌ 缺失 | — | 4:3 | 未生成 |
| 13-active-vs-passive.png | ❌ 缺失 | — | 4:3 | 未生成 |
| 14-compounding-25vs35.png | ❌ 缺失 | — | 4:3 | 未生成 |
| 15-fee-erosion.png | ❌ 缺失 | — | 4:3 | 未生成 |
| 16-global-map.png | ❌ 缺失 | — | 4:3 | 未生成 |
| 17-epilogue-path.png | ❌ 缺失 | — | 4:3 | 未生成 |

## 仓库规范（已更新）

详见 `ALL-SPECS.md` 完整规格。

| 项目 | 值 |
|------|-----|
| 书芯尺寸 | **B5**（176×250mm，5:7 比例） |
| 封面插图比例 | **2:3**（竖版） |
| 内文插图 | 4:3 为主，16:9 / 3:4 / 1:1 为辅 |
| 源码管理 | Git LFS（`.gitattributes` 已配置 `*.png` `*.jpg` `*.jpeg` `*.csv` `*.pdf`) |

## 工作流程

### 花花的工作流约定
1. **Prompt 不带比例** — 花花在 GPT-IMAGE 工作流里默认配置了比例参数，代码框给出的 Prompt 已省略比例描述
2. **通过 tmp/ 传原图** — 花花生成后将原始 PNG 丢入仓库根目录下的 `tmp/` 目录，Agent 再取图
3. **归类后删除原图** — Agent 将图片归类到 `assets/illustrations/` 并重命名后，删除 `tmp/` 内容
4. **按比例分组生成** — 优先做 4:3（12 张），再做 16:9（2 张）、3:4（2 张）、1:1（1 张）

### Agent 操作步骤
1. 检查 `tmp/` 目录是否有新图
2. `cp` 到 `assets/illustrations/`，按规范命名 `NN-name.png`
3. 删除 `tmp/` 中的原图
4. 如需替换占位图，直接覆盖同名文件

### Prompt 格式（花花版，已去掉比例）
```text
依据参考图形象生成：[场景描述内容]。扁平编辑插画风格，暖奶油色底色，焦糖色和奶油色为主，圆润线条。
```
花花会在 GPT-IMAGE 工作流中设置角色参考图和比例参数。

## 已知问题

- **00-cover.png** 当前为压缩版本（441KB），花花曾提供过 4.2MB 的原版 PNG 但已丢失，如需替换需花花重新生成
- 占位图（03, 05-08）由小花蟹生成，文件偏大（1-1.3MB），仅供版式占位用，待花花用原图替换
- 分支 `article/2026-quadruple-long-life` 已 force push，本地如使用 `cd "F:/.../[ALL]-4i_e-acc/..."` 带 `[]` 的路径会导致 git 分支 ref 写入失败（`refs/heads/` 下子目录不创建），`git -C` 参数可绕过
