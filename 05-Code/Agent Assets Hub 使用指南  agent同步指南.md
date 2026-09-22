---
status: evergreen
tags:
  - agent-hub
  - ai-tools
  - skills
  - mcp
  - 跨agent
  - 配置同步
updated: 2026-09-22
---
# Agent Assets Hub 使用指南

> 跨 Agent 共享 Skills / 规则 / 习惯 / MCP 的统一真源与一键同步
> 更新：2026-09-22
> 根目录：`~/.agents/`

---

## 一、解决什么问题

同时用 Codex、Claude Code、Antigravity（反重力）、dsh、Gemini CLI、mimo 时：

- Skill 各写一份，版本对不齐
- `AGENTS.md` / 偏好 / 调试习惯分散在各端
- MCP 服务在 `config.toml`、`.mcp.json`、`mcp_config.json` 重复维护
- 插件安装器互不兼容，无法硬共享

**原则：一处维护，按端能力投影。能同步的同步，不能的跳过。**

---

## 二、目录结构

```text
~/.agents/                      # Agent Assets Hub（唯一真源）
├── skills/                     # Agent Skills（SKILL.md 标准，~75 精选）
├── rules/                      # 用户习惯 / 风格 / 调试 / 工作流
│   ├── preferences.md          #   称呼、沟通、决策、路径习惯
│   ├── coding-style.md         #   代码风格
│   ├── debugging.md            #   调试习惯
│   ├── workflow.md             #   工作流
│   └── lessons-learned.md      #   历史教训
├── agents/AGENTS.md            # 全局指令正文
├── mcp/
│   ├── servers.yaml            # 可移植 MCP 定义（禁止写密钥）
│   └── servers.local.yaml      # 本机密钥/覆盖（gitignore）
├── commands/                   # 可移植命令（暂空）
├── plugins/                    # 仅可拆解内容；安装器不同步
├── manifest.yaml               # 各端能力矩阵
└── bin/
    ├── hub-update              # 一键：状态 → 同步 → 状态
    ├── hub-status              # 查看投影情况
    └── sync-profile            # 按能力投影
```

---

## 三、各端投影能力

| 端 | skills | MCP | rules / AGENTS | commands | plugins |
|---|---|---|---|---|---|
| **Codex** | symlink | 片段 `~/.agents/.projection/codex.mcp.toml`（不自动改 config.toml） | `AGENTS.md` 软链到 hub | 支持 | 只拆内容 |
| **Claude Code** | symlink | `.mcp.json` merge | `CLAUDE.md` 薄壳 `@` 引用 | 支持 | 只拆内容 |
| **Antigravity** | **copy**（symlink 不稳） | `mcp_config.json` merge | `GEMINI.md` 薄壳 | 跳过 | 跳过 |
| **Gemini CLI** | symlink | `mcp_config.json` merge | `GEMINI.md` 薄壳 | 跳过 | 跳过 |
| **dsh** | symlink | **跳过** | `AGENTS.md` 软链 | 跳过 | 跳过 |
| **mimo / 共享别名** | 已在 `~/.agents/skills`，不拷 | 跳过 | 跳过 | 跳过 | 跳过 |

> 不支持的类别直接 skip，不硬塞。

---

## 四、共享什么 / 不共享什么

### 共享（内容资产）

- Skills（`SKILL.md` + scripts/references/assets）
- 全局指令 `AGENTS.md` 正文
- 用户习惯 / 风格 / 调试 / 工作流（`rules/`）
- MCP **服务定义**（命令、URL；密钥用 env 名）
- 可移植 commands 文本

### 不共享（各端本地）

- API Key / 凭据 / token
- 权限、审批、hooks 路径策略
- 模型目录、reasoning effort
- 插件安装器与厂商私有二进制
- Codex 自带 `node_repl` 等绑定安装前缀的服务

---

## 五、一键更新指令

### 日常最常用

```bash
~/.agents/bin/hub-update
```

看状态 → 按能力同步 → 再看状态。

### 其它命令

```bash
~/.agents/bin/hub-status                          # 只看投影情况
~/.agents/bin/sync-profile                        # 全量同步
~/.agents/bin/sync-profile --dry-run              # 预览
~/.agents/bin/sync-profile --only skills,mcp,rules
~/.agents/bin/sync-profile --agent codex,dsh
```

建议加入 PATH：

```bash
export PATH="$HOME/.agents/bin:$PATH"
# 之后：hub-update / hub-status / sync-profile
```

### Skill 入口（各 Agent 里可直接说）

已安装 skill：**`hub-sync`**（已投影到 Codex / Claude / 反重力 / Gemini / dsh）

触发说法：

- 「hub-sync」
- 「一键同步」
- 「同步共享配置」
- 「更新 skill / 规则 / MCP」

---

## 六、改了配置之后怎么更新

| 你改了                            | 之后执行                      |
| ------------------------------ | ------------------------- |
| `~/.agents/skills/**`          | `hub-update`              |
| `~/.agents/rules/**`           | `hub-update --only rules` |
| `~/.agents/agents/AGENTS.md`   | `hub-update --only rules` |
| `~/.agents/mcp/servers.yaml`   | `hub-update --only mcp`   |
| `~/.agents/manifest.yaml`（端能力） | `hub-update`              |

改一处，多端生效：

- 改 **技能** → 各端 skills 目录
- 改 **习惯 / 偏好** → `rules/*.md`，被 AGENTS 正文索引 + Claude/Gemini 薄壳 `@`
- 改 **全局指令** → `agents/AGENTS.md`（Codex / dsh 软链直接吃）
- 改 **MCP** → Claude / Gemini / 反重力 JSON；Codex 看下一节

---

## 七、Codex MCP 合并（可选）

Codex 的 `~/.codex/config.toml` **不会被自动改**，避免覆盖 `node_repl` 等本机项。

1. 片段：`~/.agents/.projection/codex.mcp.toml`
2. 需要时**备份** `config.toml` 后，把 `[mcp_servers.*]` 手动合并进去
3. 保留本地私有服务，不要整文件覆盖

---

## 八、与 skills-hub 桌面端

| 项 | 说明 |
|---|---|
| skills-hub | 浏览 / 安装技能的 GUI（`~/github-product/skills-hub`） |
| 历史库 | `~/.skillshub`（约 381 个）作**安装源**，不是运行时真源 |
| 运行时真源 | `~/.agents/skills`（精选约 75 个） |
| 建议 | skills-hub Settings 里 Central Repo 可指到 `~/.agents/skills` |

---

## 九、备份与安全

- 投影前入口文件备份在：`~/.agents/.backup/`
- `mcp/servers.local.yaml` 已 gitignore，放密钥
- 勿把 token 写进 `servers.yaml` 或任何共享文件
- 第三方 skill 先审再进 `skills/`

---

## 十、相关

- [[skills-hub 使用指南]]
- [[Claude Code 使用指南]]
- Agent Skills 标准：https://agentskills.io
- 备份目录：`~/.agents/.backup/`

---

#agent-hub #ai-tools #skills #mcp #跨agent #配置同步
