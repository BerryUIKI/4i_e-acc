# Lock Protocol

> Main Agent f78f1d3e — Context Window concurrency control.
> Three-tier lock: branch → directory → file.

---

## 1. 核心规则

1. **任何窗口（含 MAIN）改任何文件前，必须先拿锁。**
2. **锁由窗口自己申请、自己释放。** MAIN 只写 task，不代管锁。
3. **拿锁顺序：分支 → 目录 → 文件。放锁顺序：文件 → 目录 → 分支。**
4. **锁文件创建必须原子（O_EXCL / `set -C`），先检查再创建不安全。**

---

## 2. 锁文件位置

```
locks/
├── branch/
│   └── {safe-branch-name}.lock
├── dir/
│   └── {safe-dir-path}.lock
└── file/
    └── {safe-file-path}.lock
```

### 路径编码规则

`/` 和空格 → `_`，其余字符保留。

```
articles/2026-quadruple-long-life/Main-Text/B002.md
→ articles_2026-quadruple-long-life_Main-Text_B002.lock
```

---

## 3. 锁文件格式

```yaml
task: TASK-003
window: editorial
branch: article/2026-quadruple-long-life
scope: articles/2026-quadruple-long-life/Main-Text/B002.md
since: 2026-07-30T03:00:00+08:00
timeout: 2026-07-30T03:30:00+08:00
```

| 字段 | 说明 |
|------|------|
| `task` | 归属的 task 编号 |
| `window` | 持有此锁的窗口名 |
| `branch` | 锁绑定的 Git 分支 |
| `scope` | 锁作用范围的原始路径 |
| `since` | 锁创建时间（ISO 8601 含时区） |
| `timeout` | 锁自动过期时间（since + 30min） |

---

## 4. 锁层级规则

### 4.1 分支锁

- 每个分支最多一把。**独占。**
- 目的：防止任何窗口切换分支。
- 第一个 task 创建，所有 task 只读检查，所有 task 完成后 MAIN 删除。
- 创建前检查：`locks/branch/` 下没有**其他分支名**的锁。

### 4.2 目录锁

- 锁一个目录及其所有子文件/子目录。
- **共享**：不同目录可同时锁。
- 创建前检查：目标目录不在任何现有目录锁的子树内，也不包含任何现有文件锁的路径。

### 4.3 文件锁

- 锁单个文件。**独占。**
- 创建前检查：目标文件不被现有文件锁或目录锁覆盖。

### 4.4 冲突检查算法

```
新锁 scope X 检查冲突：

for each 现有锁 L:
  if X 在 L.scope 之内       → 冲突（被父目录锁覆盖）
  if L.scope 在 X 之内       → 冲突（X 是目录锁，覆盖了已有文件锁）
  if X == L.scope            → 冲突（同一个文件/目录）
  → 没有冲突 → OK
```

---

## 5. 流程

### 5.1 MAIN 分配 task

```
1. MAIN 写 task 文件到 tasks/TASK-NNN.md
2. task 中声明建议的锁范围（窗口执行时参考，不是强制）
3. MAIN 告诉花花：「{窗口名} 窗口，读 TASK-NNN」
```

### 5.2 窗口启动 + 拿锁

```
1. 窗口读 task → 确认要改的文件范围
2. 窗口读 locks/branch/ → 检查分支锁
   ├── 无分支锁 → 创建分支锁（原子创建）
   ├── 有，分支名一致 → 通过
   └── 有，分支名不一致 → 阻塞，报告 MAIN
3. 窗口读 locks/dir/ + locks/file/ → 冲突检查
   ├── 无冲突 → 创建自己的目录锁/文件锁（原子创建）
   ├── 有冲突 → 等待 30s 重试一次
   └── 重试仍冲突 → 阻塞，报告 MAIN
4. 拿锁成功 → 开始干活
```

### 5.3 窗口释放锁

```
1. 改完文件 → commit
2. 删除文件锁（按拿锁的反序）
3. 删除目录锁
4. 写 handoff
5. 如果这是该分支最后一个 task → 删除分支锁（MAIN 巡检时处理）
```

### 5.4 MAIN 自己干活

MAIN 也要走完整拿锁/放锁流程。不能因为自己是 MAIN 就跳过。

---

## 6. 原子创建

使用 shell 的 noclobber 或 Python 的 `os.open(path, os.O_CREAT | os.O_EXCL)`：

```python
import os
try:
    fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    os.write(fd, lock_content.encode())
    os.close(fd)
    # 锁创建成功
except FileExistsError:
    # 锁已存在 → 读内容判断是死锁还是真冲突
```

**禁止先读后写**（`if not exists → create`）——竞态窗口会让两个窗口同时以为锁不存在。

---

## 7. 僵尸锁清理

MAIN 每次处理花花消息时执行巡检：

```
1. 扫描 locks/ 下所有 .lock 文件
2. 读取 timeout 字段
3. 若 当前时间 > timeout → 读取锁中的 task 字段
4. 检查 tasks/TASK-NNN.md 的 status
   ├── status = DONE 或 MERGED → 僵尸 → 删除锁
   └── status 仍为 IN_PROGRESS → 可能窗口还在工作 → 延长 timeout 30min
5. 记录清理到 handoffs/lock-cleanup.md
```

不需要定时任务。花花活跃时自然巡检，不活跃时僵尸锁无影响。

---

## 8. 举例

```
TASK-001 — 编辑重写第 2-3 章
窗口: editorial
锁申请:

1. locks/branch/article-2026-quadruple-long-life.lock  ← 原子创建
2. locks/dir/articles_2026_Main-Text.lock               ← 原子创建

TASK-002 — 生成第 3 章插图
窗口: illustration
锁申请:

1. locks/branch/article-2026-quadruple-long-life.lock  ← 已存在，分支一致，通过
2. locks/dir/assets_illustrations.lock                  ← 原子创建（不同目录，OK）

TASK-003 — 修复 CI
窗口: general
锁申请:

1. locks/branch/article-2026-quadruple-long-life.lock  ← 已存在，分支一致，通过
2. locks/dir/pipeline_ci  ← 原子创建（又不同目录，OK）

三个 task 并行，零冲突。
```
