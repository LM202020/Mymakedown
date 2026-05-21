# Framework Quick Prompts

## 新项目安装

```text
请按 Framework Install Mode 初始化新项目。
读取 SAFE_ADOPTION_POLICY.md 和 templates/FILE_ADOPTION_MANIFEST.md。
所有文件按 adoption_mode 处理。
文件不存在才创建，文件存在绝不覆盖。
不要写业务代码。
```

## 老项目接管

```text
请按 Existing Project Adoption Mode 接管老项目。
读取 SAFE_ADOPTION_POLICY.md 和 templates/FILE_ADOPTION_MANIFEST.md。
扫描已有文件，生成 adoption plan。
所有已有文件不要覆盖。
propose_if_exists 只生成 proposed 文件。
managed_block_merge 只改受控区块。
冲突写入 DOC_CONFLICTS。
不要修改业务代码。
```

## 只 dry-run

```text
请 dry-run 安装这个框架，不要写文件。
列出每个 target_path 的状态和将采取的 adoption_mode。
输出安全创建项、需要 proposed 文件的项、冲突项、需要人工确认项。
```

---

## 启用 Optional Hooks

```text
请为这个项目启用 optional hooks。

要求：

1. 读取 HOOKS_USAGE.md。
2. 读取 optional-hooks/config/hooks-config.yaml。
3. 确认当前项目是 git repo。
4. 执行 bash optional-hooks/install-hooks.sh。
5. 执行 python3 optional-hooks/scripts/run_all_checks.py。
6. 如果有 warning，只汇报，不要擅自修改业务代码。
```

## 运行 Optional Hooks 检查

```text
请运行 optional hooks 检查。

要求：

1. 执行 python3 optional-hooks/scripts/run_all_checks.py。
2. 汇总每个检查结果。
3. warn 模式下不要当成失败。
4. block 模式失败时说明阻塞原因。
5. 不要修改业务代码。
```

## 切换到 block 模式

```text
请把 optional hooks 从 warn 模式切换到 block 模式。

要求：

1. 修改 optional-hooks/config/hooks-config.yaml。
2. 只把 mode 从 warn 改成 block。
3. 不要修改其他配置。
4. 运行 python3 optional-hooks/scripts/run_all_checks.py。
5. 如果检查失败，先汇报原因，不要擅自修复业务代码。
```
