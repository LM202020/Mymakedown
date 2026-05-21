# Safe Adoption Policy：全文件安全采用策略

这个策略适用于所有目标文件，不只适用于 `AGENTS.md`、`CLAUDE.md`、`CODEX.md`。

## 1. 核心规则

```text
任何目标文件，如果已经存在，都不能直接覆盖。
```

所有文件必须按照 `templates/FILE_ADOPTION_MANIFEST.md` 里的 `adoption_mode` 处理。

---

## 2. adoption_mode 定义

| adoption_mode | 含义 | 行为 |
|---|---|---|
| `create_if_missing` | 缺失才创建 | 文件不存在时从 template 创建；存在则不覆盖 |
| `managed_block_merge` | 受控区块合并 | 只新增或更新 BEGIN/END 标记内的内容 |
| `propose_if_exists` | 已存在则生成 proposed | 文件不存在则创建；存在则生成 proposed 文件供人工 review |
| `append_index` | 追加索引 | 只追加短记录，不粘贴长内容 |
| `generated_runtime` | 运行中生成 | 由工作流运行时创建，不在安装时覆盖 |
| `archive_only` | 归档目录 | 不主动移动或删除，需要人工确认 |
| `directory_create` | 创建目录 | 目录不存在才创建 |
| `never_overwrite` | 永不覆盖 | 只读、记录、生成合并计划 |

---

## 3. 老项目采用步骤

1. 读取 `templates/FILE_ADOPTION_MANIFEST.md`。
2. 对每个 target_path 检查是否存在。
3. 根据 adoption_mode 决定处理方式。
4. 已存在文件必须摘要现有内容。
5. 检查是否与模板冲突。
6. 冲突写入 `docs/DOC_CONFLICTS.md`。
7. 生成 adoption plan。
8. 只有安全项才执行。
9. 不安全项只生成 proposed 文件。

---

## 4. proposed 文件位置

如果文件已存在且不能直接合并，把模板输出到：

```text
docs/adoption/proposed/<target_path>.proposed.md
```

例如：

```text
docs/adoption/proposed/docs/ARCHITECTURE.md.proposed.md
```

---

## 5. 受控区块模式

适合 `AGENTS.md`、`CLAUDE.md`、`CODEX.md`、`README.md`。

格式：

```md
<!-- BEGIN PROJECT_AGENT_WORKFLOW -->

managed content

<!-- END PROJECT_AGENT_WORKFLOW -->
```

规则：

1. 区块不存在时可以追加。
2. 区块存在时只更新区块内部。
3. 区块外内容视为项目所有，不能改。
4. 如有冲突，写入 `DOC_CONFLICTS.md`。

---

## 6. 文档模板模式

适合 `docs/ARCHITECTURE.md`、`docs/DEPLOYMENT.md` 等。

规则：

1. 文件不存在，可以从 template 创建。
2. 文件存在，不覆盖。
3. 生成 proposed 文件。
4. 在 `DOC_MIGRATION_MAP.md` 里记录映射关系。
5. 冲突写入 `DOC_CONFLICTS.md`。

---

## 7. 安装 Prompt

```text
请按 Safe Adoption Policy 安装这个框架。

要求：

1. 读取 templates/FILE_ADOPTION_MANIFEST.md。
2. 对每个文件按 adoption_mode 处理。
3. 文件不存在才创建。
4. 文件存在绝不覆盖。
5. managed_block_merge 只改 BEGIN/END 受控区块。
6. propose_if_exists 只生成 proposed 文件。
7. 冲突写入 docs/DOC_CONFLICTS.md。
8. 生成 adoption summary。
9. 不要修改业务代码。
```

---

## 8. Optional Hooks 和 Safe Adoption

v7 的 optional hooks 可以辅助检查 Safe Adoption 是否被破坏。

推荐开启：

```text
check_no_overwrite.py
check_adoption_manifest.py
```

它们会检查：

1. 是否修改了受保护入口文件。
2. 是否缺少 adoption manifest。
3. 是否可能绕过 adoption_mode 直接覆盖文件。

注意：hooks 只能辅助检查，不能替代人工 review。
