# Project Agent Workflow Framework v8

这是一套给 Claude、Codex 等代码 Agent 使用的**项目级工作流框架**。它不是一份普通的 `AGENTS.md`，而是给项目安装的一整套 Agent 工作系统：项目说明书 + Agent 交通规则 + 开发流程 + 文档目录 + 多 Agent 协作协议 + Session 交接机制 + 老项目接管机制 + 防覆盖合并机制。

自然语言完整说明见 [`NATURAL_LANGUAGE_OVERVIEW.md`](NATURAL_LANGUAGE_OVERVIEW.md)。

## 解决什么问题

- Agent 看到需求就直接改代码，没有 spec、没有实现计划。
- 老项目已有的 `README`、`docs`、CI、部署说明被新模板覆盖。
- Claude 写计划、Codex 接手时丢上下文；Codex 改完，Claude review 时不知道改了什么。
- 多个 Agent 同时改同一批文件。
- Session 快满或换窗口后任务状态丢失，`SESSION_HANDOFF.md` 不断膨胀。
- 部署、凭证、数据库迁移等高风险文件被误改。

## 基本工作方式

所有非平凡代码改动都走：

```text
需求 → Spec → Spec Review → 实现计划 → Plan Review
     → 分支/Worktree → 逐任务实现 → 验证 → Review
     → Session 保存/交接 → 最终集成
```

一句话：**先想清楚，再拆计划，再按任务做，再验证，再交接。**

## 目录结构

```text
project_agent_workflow_framework_v8/
├── README.md                     # 本文件
├── NATURAL_LANGUAGE_OVERVIEW.md  # 自然语言完整说明
├── SAFE_ADOPTION_POLICY.md       # 全文件安全采用策略
├── INSTALL_OR_ADOPT_WORKFLOW.md  # 安装 / 接管 / dry-run 指令
├── FRAMEWORK_QUICK_PROMPTS.md    # 常用 Prompt 速查
├── FILE_TREE.md
└── templates/
    ├── FILE_ADOPTION_MANIFEST.md # 每个目标文件如何落地的规则表
    └── target/                   # 所有待落地的模板内容
```

## 怎么用

- **新项目**：先建规则再写功能。用 [`INSTALL_OR_ADOPT_WORKFLOW.md`](INSTALL_OR_ADOPT_WORKFLOW.md) 第 1 节的 Install Mode 指令，按 [`templates/FILE_ADOPTION_MANIFEST.md`](templates/FILE_ADOPTION_MANIFEST.md) 的 `adoption_mode` 创建文件，**文件不存在才创建**。
- **老项目**：先接管再优化。用 Existing Project Adoption Mode 扫描现有文件、生成 baseline / migration map / 冲突记录，**已有文件绝不覆盖**，需要合并的只走 proposed 文件或受控区块。
- **只看不改**：用 Dry Run 模式列出每个目标文件的状态和将采取的处理方式。

核心安全规则见 [`SAFE_ADOPTION_POLICY.md`](SAFE_ADOPTION_POLICY.md)：所有目标文件按 `adoption_mode`（`create_if_missing` / `managed_block_merge` / `propose_if_exists` / `append_index` / `generated_runtime` / `directory_create` / `archive_only` / `never_overwrite`）处理。

## Session 保存与恢复

Session 不会自动保存。旧窗口结束前说「请执行 Session Save Handoff」，新窗口开始时说「请执行 Session Restore」。原则：**旧窗口负责保存，新窗口负责恢复；没有保存就不要假装可以无损恢复。**

## Claude 与 Codex 分工

| Agent | 适合做 |
|---|---|
| Claude | spec review、架构分析、计划拆分、风险评审、文档整理、handoff 总结 |
| Codex | 读 repo、改代码、跑测试、修 CI、小范围实现 |
| Reviewer / Documentation / Integration | 评审、文档迁移、最终集成与 retro |

交给 Codex 前必须保存 handoff；Codex 接手前必须 restore；改完输出 Agent Output Contract；Claude review 不扩大 scope。

## v8 新增：并行 Session 的提交协调

v8 补全了多 Session 并行时的提交 / 合并规则（落地项目里的 `docs/IMPLEMENTATION_WORKFLOW.md` §3.2 Commit and Merge Autonomy）：

- 每个 Session 在自己分支 / worktree 上自动 commit 与 push，无需逐次人工确认；合并进 base 前必须先过一轮独立对抗式评审，P3 高风险变更仍需显式人工批准。
- spec / plan 一落地就 commit，创建前查重文件名、撞名加后缀，避免并行 Session 撞名或重复编辑。
- 工作完成或写小结（Agent Output Contract、handoff）后自动 commit + push，让其他 Session 与 reviewer 随时看到进度。
