# Hooks 使用说明

v7 在 v6 的基础上新增 `optional-hooks/`。

它默认不启用，不会自动影响项目。你可以在项目稳定后手动安装。

## 1. 它解决什么

Hooks 用来自动检查 Agent 常犯的明显错误：

- 把 secrets 或 `.env` 提交进去
- 让 `SESSION_HANDOFF.md` 不断膨胀
- 直接覆盖老项目已有文件
- 在 spec / plan 里留下 TODO、TBD、模糊占位
- 修改 owned files 之外的文件
- 缺少 adoption manifest

## 2. 安装

在项目根目录执行：

```bash
bash optional-hooks/install-hooks.sh
```

### Windows 说明

安装脚本和 git hooks 是 bash 脚本，Windows 上需通过 **Git Bash**(Git for Windows 自带)运行。

git hooks 会自动探测解释器:优先用 `python3`，没有则回退到 `python`。手动运行检查时，如果系统没有 `python3` 命令，把下文示例里的 `python3` 换成 `python` 即可。

## 3. 卸载

```bash
bash optional-hooks/uninstall-hooks.sh
```

## 4. 配置 warn / block

配置文件：

```text
optional-hooks/config/hooks-config.yaml
```

默认：

```yaml
mode: warn
```

含义：只警告，不阻止 commit。

改成：

```yaml
mode: block
```

含义：发现问题就阻止 commit / push。

## 5. 手动运行

```bash
python3 optional-hooks/scripts/run_all_checks.py
```

## 6. 单项运行

```bash
python3 optional-hooks/scripts/check_secrets.py
python3 optional-hooks/scripts/check_handoff_size.py
python3 optional-hooks/scripts/check_no_overwrite.py
python3 optional-hooks/scripts/check_plan_placeholders.py
python3 optional-hooks/scripts/check_adoption_manifest.py
python3 optional-hooks/scripts/check_owned_files.py
```

## 7. owned files 为什么默认关闭

`owned files` 检查需要项目已经有 active task 和 `SESSION_HANDOFF.md` 里的 owned files。

刚初始化项目时通常还没有 active task，所以默认关闭。

进入多 Agent 实现阶段后，可以打开：

```yaml
checks:
  owned_files: true
```

## 8. 给 Agent 的安装指令

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

## 9. 推荐启用顺序

1. 先保持 `mode: warn`。
2. 观察几次 commit。
3. 没有误报后改成 `mode: block`。
4. 多 Agent 任务开始后再启用 `owned_files`。
