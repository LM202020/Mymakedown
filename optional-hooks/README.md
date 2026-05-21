# Optional Hooks

这是 Project Agent Workflow Framework v7 的可选 Hook 层。

它默认不启用，不会自动修改你的项目。你可以在项目稳定后手动安装。

## 能检查什么

- secrets / `.env` 是否被提交
- `SESSION_HANDOFF.md` 是否膨胀
- 是否直接覆盖老项目已有文件
- spec / plan 是否含 TODO、TBD、模糊占位
- 是否修改 owned files 之外的文件
- adoption manifest 是否存在且基本有效

## 默认模式

默认是 `warn`：发现问题只警告，不阻止 commit。

配置文件：

```text
optional-hooks/config/hooks-config.yaml
```

## 安装

```bash
bash optional-hooks/install-hooks.sh
```

## 卸载

```bash
bash optional-hooks/uninstall-hooks.sh
```

## 手动运行全部检查

```bash
python3 optional-hooks/scripts/run_all_checks.py
```

## 推荐启用顺序

1. secrets 检查
2. handoff size 检查
3. no-overwrite 检查
4. plan placeholder 检查
5. adoption manifest 检查
6. owned files 检查
