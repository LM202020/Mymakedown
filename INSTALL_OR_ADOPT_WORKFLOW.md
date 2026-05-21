# Install or Adopt Workflow

Use this file to decide how to apply the framework.

## 1. New Project Install

```text
请按 Framework Install Mode 初始化新项目。

要求：

1. 读取 SAFE_ADOPTION_POLICY.md。
2. 读取 templates/FILE_ADOPTION_MANIFEST.md。
3. 对每个 target_path 按 adoption_mode 处理。
4. 文件不存在才创建。
5. 文件存在绝不覆盖。
6. 创建必要目录。
7. 生成安装摘要。
8. 不要写业务代码。
```

## 2. Existing Project Adoption

```text
请按 Existing Project Adoption Mode 接管老项目。

要求：

1. 读取 SAFE_ADOPTION_POLICY.md。
2. 读取 templates/FILE_ADOPTION_MANIFEST.md。
3. 扫描所有 target_path 是否已经存在。
4. 对已有文件摘要现有内容。
5. 对每个文件按 adoption_mode 生成 adoption plan。
6. managed_block_merge 只操作受控区块。
7. propose_if_exists 只生成 proposed 文件。
8. 冲突写入 docs/DOC_CONFLICTS.md。
9. 生成 docs/DOC_MIGRATION_MAP.md。
10. 不要覆盖任何已有文件。
11. 不要修改业务代码。
```

## 3. Dry Run Only

```text
请 dry-run 安装这个框架，不要实际写文件。

要求：

1. 读取 templates/FILE_ADOPTION_MANIFEST.md。
2. 列出每个 target_path 的状态：missing、exists、conflict、safe to create、needs proposed。
3. 输出会创建哪些文件。
4. 输出会生成哪些 proposed 文件。
5. 输出哪些文件需要人工确认。
6. 不要修改任何文件。
```

---

## 4. Optional Hooks Installation

框架安装或老项目接管完成后，可以选择启用 hooks。

```text
请为这个项目启用 optional hooks。

要求：

1. 先读取 HOOKS_USAGE.md。
2. 先读取 optional-hooks/config/hooks-config.yaml。
3. 不要直接改业务代码。
4. 安装 hooks 前先确认当前项目是 git repo。
5. 运行 bash optional-hooks/install-hooks.sh。
6. 安装后运行 python3 optional-hooks/scripts/run_all_checks.py。
7. 如果有 warning，只汇报，不要擅自大改。
```
