# Codex 与 Claude Code 开源工具集成指南

更新日期：2026-07-17

## 当前状态

| 工具 | 类型 | Codex | Claude Code | 状态 |
| --- | --- | --- | --- | --- |
| CodeGraph | 本地代码图谱 MCP | 已移除 | 已移除 | CLI、全局 MCP 与后台进程均已清理；项目索引保留 |
| Ponytail | 工作流 skills / 插件 | 六个 skills 已安装 | `ponytail@ponytail` 已安装 | hooks 未自动信任 |
| Agent-Reach | 搜索能力路由 CLI / skill | 共享 skill 已存在 | 共享 skill 已存在 | CLI 1.5.0、安全模式已配置 |
| AnySearch | 搜索与网页提取 skill | 已安装 | 已安装 | 匿名模式已验证 |
| Codebase Memory MCP | 本地代码图谱 MCP | 已注册 | 已注册 | 已安装，自动监听已关闭 |

## 使用边界

- CodeGraph 与 Codebase Memory 都会读取、索引并持续观察项目文件。每个项目优先只选一个，避免重复索引、重复 token 消耗和两套图谱结论冲突。
- AnySearch 适合轻量公开搜索与网页提取；Agent-Reach 适合 GitHub、RSS、视频和按需启用的站点渠道。不要让二者都成为默认搜索入口。
- 对私有代码、密钥、客户数据或未公开 URL，不要发送到 AnySearch、Exa、Jina Reader 或其他远程服务。

## CodeGraph

已于 2026-07-17 移除 CodeGraph CLI、Codex MCP、Claude Code MCP 与相关后台进程，以避免与 Codebase Memory 的重复图谱能力。各项目已有的 `.codegraph/` 目录未删除；确认不再需要其中历史索引后，可在对应项目手工删除或执行原工具的清理流程。
## Ponytail

Claude Code 已安装 `ponytail@ponytail`。Codex 已添加官方市场，但当前 Codex 版本未识别该仓库的市场索引；因此已安装同仓库提供的六个 skills：`ponytail`、`ponytail-review`、`ponytail-audit`、`ponytail-debt`、`ponytail-gain`、`ponytail-help`。

Ponytail 强制偏好最小实现、YAGNI 和标准库优先。它还提供两个 Node 生命周期 hook，会改变每轮与子 agent 的上下文注入。为避免隐式改变工作流，hooks 没有被自动信任。重启客户端后可使用 skills；若要启用 Codex hooks，先在 `/hooks` 中逐项阅读并确认。

## Agent-Reach

CLI 位于：

```text
C:\Users\Lenovo\.agent-reach-venv\Scripts\agent-reach.exe
```

已使用 Python 3.11 从官方源码安装 Agent-Reach 1.5.0，并完成 `install --env=auto --safe`。当前可用核心能力包括 GitHub、RSS、Jina Reader 和 B 站搜索；可选的 X、Reddit、小红书、Instagram、LinkedIn 等渠道没有安装，也不应使用主账号 Cookie 直接启用。

已安装 `mcporter` 并在用户级配置注册 Exa 远程 MCP。验证与维护：

```powershell
C:\Users\Lenovo\.agent-reach-venv\Scripts\agent-reach.exe doctor
mcporter config get exa --json
```

注意：`mcporter` 0.9.0 可以启动，但 npm 报告一个传递依赖要求 Node 22.12+；当前 Node 是 22.11.0。升级 Node 后应重新运行 `agent-reach doctor`。

## AnySearch

AnySearch v2.1.0 已分别安装到：

```text
C:\Users\Lenovo\.agents\skills\anysearch
C:\Users\Lenovo\.claude\skills\anysearch
```

两端均配置 Python 3.11 运行时，并已在匿名模式成功完成公开查询。典型调用：

```powershell
C:\Windows\py.exe -3 C:\Users\Lenovo\.agents\skills\anysearch\scripts\anysearch_cli.py search "OpenAI official documentation" --max_results 3
```

匿名配额有限。需要更高限额时，只在用户环境变量或该 skill 的私有 `.env` 中设置 `ANYSEARCH_API_KEY`，不要写入项目仓库、Obsidian 笔记或 MCP 配置。

## Codebase Memory MCP

已安装官方 Windows amd64 release `0.9.0`，下载已通过官方 SHA-256 校验。二进制位于：

```text
C:\Users\Lenovo\.agent-tools\codebase-memory-mcp\codebase-memory-mcp.exe
```

Codex 与 Claude Code 均已注册同一个 stdio MCP。启动环境只允许索引 `C:\Users\Lenovo`，缓存写入 `C:\Users\Lenovo\.agent-tools\codebase-memory-cache`；`auto_watch` 已关闭。首次对具体项目使用时再显式请求索引，不要把私有或无关目录加入允许根目录。

```powershell
C:\Users\Lenovo\.agent-tools\codebase-memory-mcp\codebase-memory-mcp.exe config get auto_watch
```

两套代码图谱不应默认同时用于同一项目：需要轻量实时符号/调用关系时优先 CodeGraph；需要持久化 SQLite 图谱、LSP 混合分析和团队 artifact 时选 Codebase Memory。需要卸载时先运行 `codex mcp remove codebase-memory` 与 `claude mcp remove codebase-memory -s user`，再执行该二进制的 `uninstall`。
## 已新增推荐项

| 项目 | 当前状态 | 使用边界 |
| --- | --- | --- |
| `github/github-mcp-server` | 官方原生 MCP 1.6.0 已注册到 Codex 与 Claude Code | 首次使用在浏览器完成 OAuth；不保存 PAT。需要写入仓库、Issue 或 PR 前仍应明确授权。 |
| `vercel-labs/agent-skills` | `composition-patterns` 与 `react-best-practices` 已安装到两端 | 用于 React/组件架构任务；不包含默认部署权限。 |
| `web-design-guidelines` | 两端原本已通过受管理共享目录安装 | 保留现有来源，不重复覆盖。 |
| `upstash/context7` | 已存在 | 仅查公开库文档，不提交私有代码或敏感上下文。 |
| `microsoft/playwright-mcp` | 已存在 | 使用隔离浏览器 profile，不登录生产账号。 |

GitHub MCP 原生二进制位于：

```text
C:\Users\Lenovo\.agent-tools\github-mcp\bin\github-mcp-server.exe
```
## 图谱选择

CodeGraph 已移除。Codebase Memory 是当前唯一代码图谱 MCP：允许根目录限制为 `C:\Users\Lenovo`、缓存使用独立目录、`auto_watch=false`。对具体项目需要图谱分析时再显式请求索引，避免扫描无关或私有目录。
## 验收更新

- 2026-07-17：Agent-Reach `doctor` 已通过，核心可用渠道为 5/15；全网语义搜索经 mcporter + Exa 验证可用。
- 2026-07-17：Claude Code 的 Ponytail 插件已启用，用户级 `defaultMode` 已设为 `lite`；仍建议在重启后的首个项目中观察其规则注入是否符合当前工作流。
- 2026-07-17：Codebase Memory MCP `0.9.0` 已通过官方 SHA-256 校验并安装；Codex 已注册，Claude Code 显示 `Connected`，`auto_watch=false`。`
- 2026-07-17：CodeGraph 已从 Codex 与 Claude Code 移除；npm CLI 与后台进程残留已清理，项目内 `.codegraph/` 索引保留。