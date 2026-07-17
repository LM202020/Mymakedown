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
