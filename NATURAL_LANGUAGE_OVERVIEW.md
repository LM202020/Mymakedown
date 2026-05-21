# 自然语言版：这个开发模板到底是什么

这套模板不是一个单纯的 `AGENTS.md`，也不是一份普通的开发规范。

它更像是给一个项目安装一套 **Agent 工作系统**。

你可以把它理解成：

```text
项目说明书
+ Agent 交通规则
+ 开发流程
+ 文档目录
+ 多 Agent 协作协议
+ Session 交接机制
+ 老项目接管机制
+ 防覆盖合并机制
```

---

## 1. 它解决什么问题

当你让 Claude、Codex 或其他 Agent 做项目开发时，常见风险是：

1. Agent 直接看需求就开始改代码。
2. 没有 spec，没有 implementation plan。
3. 老项目已有文档被新模板覆盖。
4. Claude 写计划，Codex 接手时丢上下文。
5. Codex 改完代码，Claude review 时不知道改了什么。
6. 多个 Agent 同时改同一批文件。
7. Session 快满或换窗口后，任务状态丢失。
8. `SESSION_HANDOFF.md` 被不断追加，越来越大。
9. 部署、凭证、数据库迁移等高风险文件被误改。
10. 老项目的 README、docs、CI、部署说明互相冲突，Agent 不知道该信哪个。

这套模板就是为了解决这些问题。

---

## 2. 它的基本工作方式

它要求所有非平凡代码改动都走这个流程：

```text
需求
  ↓
Spec
  ↓
Spec Review
  ↓
Implementation Plan
  ↓
Plan Review
  ↓
Branch / Worktree
  ↓
Task-by-task Implementation
  ↓
Verification
  ↓
Review
  ↓
Session Save / Handoff
  ↓
Final Integration
```

简单说：

```text
先想清楚，再拆计划，再按任务做，再验证，再交接。
```

不过流程有轻重两档（lane），不必每个改动都走完整套：

- **Light Lane（小改动）**：一份简短的"目标 + 方案 + 涉及文件 + 验证命令"合并说明，跳过独立的 spec/plan 评审闸门，但仍然要写测试和做一次自检。适合单人做小修小补。
- **Full Lane（大项目 / 高风险）**：完整的 spec → plan → review → 逐任务 → 集成流程。适合一个人啃大项目，或碰到部署、凭证、数据库迁移等高风险改动。

按 `docs/IMPLEMENTATION_WORKFLOW.md` 第 3 节的 P0–P3 分类选 lane，详见第 3.1 节。

---

## 3. 新项目怎么用

新项目里，Agent 不应该一上来就写业务功能。

它应该先做：

1. 建立项目文档目录。
2. 建立 `docs/IMPLEMENTATION_WORKFLOW.md`。
3. 建立 `docs/DOCUMENT_INDEX.md`。
4. 建立 `docs/SESSION_HANDOFF.md`。
5. 建立 `docs/PROMPT_LIBRARY.md`。
6. 建立 specs、plans、reviews、handoffs、retros 等目录。
7. 如果缺少 `AGENTS.md`、`CLAUDE.md`、`CODEX.md`，才从模板创建。
8. 如果这些文件已经存在，就不能覆盖。

新项目的核心目标是：

```text
先建立规则，再开始开发。
```

---

## 4. 老项目怎么用

老项目最危险的是覆盖已有文件。

所以老项目接管时，Agent 必须先做 adoption：

1. 扫描现有 README、docs、CI、测试、部署、数据库、配置。
2. 检查是否已有 `AGENTS.md`、`CLAUDE.md`、`CODEX.md`。
3. 生成 `PROJECT_BASELINE.md`。
4. 生成 `DOC_MIGRATION_MAP.md`。
5. 生成 `DOC_CONFLICTS.md`。
6. 生成 `ENTRYPOINT_MERGE_PLAN.md`。
7. 对已有文档分类：canonical、outdated、conflicting、archive candidate。
8. 不覆盖任何已有文件。

老项目的核心目标是：

```text
先接管，再优化。
```

---

## 5. 为什么 v6 要把所有文件都改成模板模式

之前只保护 `AGENTS.md`、`CLAUDE.md`、`CODEX.md` 还不够。

因为老项目也可能已经有：

```text
README.md
docs/ARCHITECTURE.md
docs/DEPLOYMENT.md
docs/TEST_CONVENTIONS.md
docs/SECURITY.md
docs/API_PATHS.md
```

如果直接复制模板，就会覆盖老项目已有内容。

所以 v6 统一改成：

```text
templates/target/...
```

所有文件都先作为模板存在，不直接落到项目根目录。

真正落地时，必须看：

```text
templates/FILE_ADOPTION_MANIFEST.md
```

这个 manifest 会告诉 Agent 每个文件应该怎么处理：

| adoption_mode | 含义 |
|---|---|
| create_if_missing | 文件不存在才创建 |
| managed_block_merge | 文件存在就只改受控区块 |
| propose_if_exists | 文件存在就生成 proposed 文件，不覆盖 |
| append_index | 只追加索引记录 |
| generated_runtime | 运行过程中生成 |
| archive_only | 只归档，不自动删除 |
| directory_create | 只创建目录 |

---

## 6. Session 怎么保存和恢复

Session 不会自动保存。

旧窗口结束前必须说：

```text
请执行 Session Save Handoff。
```

它会更新：

```text
docs/SESSION_HANDOFF.md
docs/handoffs/<timestamp>.md
docs/HANDOFF_INDEX.md
active plan task status
```

新窗口开始时必须说：

```text
请执行 Session Restore。
```

它会读取：

```text
AGENTS.md
docs/IMPLEMENTATION_WORKFLOW.md
docs/DOCUMENT_INDEX.md
docs/HANDOFF_POLICY.md
docs/SESSION_HANDOFF.md
active spec
active plan
```

核心原则：

```text
旧窗口负责保存，新窗口负责恢复。
没有保存，就不要假装可以无损恢复。
```

---

## 7. Claude 和 Codex 怎么配合

推荐分工：

| Agent | 适合做 |
|---|---|
| Claude | spec review、架构分析、计划拆分、风险评审、文档整理、handoff 总结 |
| Codex | 读 repo、改代码、跑测试、修 CI、做小范围实现 |
| Reviewer Agent | 检查 spec compliance、plan compliance、代码质量、测试充分性 |
| Documentation Agent | 更新 docs、迁移旧文档、整理交接 |
| Integration Agent | 最终 diff review、PR summary、release notes、retro |

Claude 交给 Codex 前必须保存 handoff。  
Codex 接手前必须 restore。  
Codex 改完后必须输出 Agent Output Contract。  
Claude review 时不能扩大需求范围。

---

## 8. 这套模板最重要的原则

```text
新项目先建规则，再写功能。
老项目先接管，再优化。
不知道就写 UNKNOWN。
不适用就写 N/A。
已有文件不覆盖。
所有目标文件按 adoption_mode 处理。
旧 Session 负责保存。
新 Session 负责恢复。
Codex 执行前确认 owned files。
Claude review 不扩大 scope。
高风险文件必须显式批准。
```

---

## 9. v7 的 Optional Hooks 是什么

v7 增加了一个可选的 hooks 层。

你可以理解成：

```text
文档规则是交通规则。
Hooks 是路口的警示灯和栏杆。
```

v6 已经告诉 Agent：

- 不要覆盖老项目文件
- 不要让 SESSION_HANDOFF 膨胀
- 不要提交 secrets
- 不要改 owned files 之外的文件
- plan 不要留 TODO / TBD

v7 的 hooks 会在 commit / push 前帮你检查这些问题。

但它默认不启用，因为不同项目环境不一样。

建议先用 `warn` 模式，稳定后再切换到 `block` 模式。
