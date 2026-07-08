# Codex / Claude Code Agent 工具接入记录

日期：2026-07-07

## 结论

本轮处理的四个工具：

| 工具 | 状态 | Codex | Claude Code | 备注 |
|---|---|---|---|---|
| Agent-Reach | 已安装，基础通道部分可用 | 已接入 skill | 已接入 skill | GitHub 已登录可用；部分站点受 DNS/代理影响 |
| CodeGraph | 已安装并写入 MCP 配置 | 已写入 `~/.codex/config.toml` 和 `~/.codex/AGENTS.md` | 已写入 `~/.claude.json` 和 `~/.claude/CLAUDE.md` | 每个项目需单独 `codegraph init` 后才有图谱 |
| Ponytail | 已安装 npm 包和本地 skills；官方插件未装上 | 已接入 skills 和全局规则 | 已接入 skills 和全局规则 | 官方 marketplace 受 GitHub TLS/clone 超时影响，当前是降级接入 |
| Firecrawl | 已有 MCP 配置 | `npx -y firecrawl-mcp` | `npx -y firecrawl-mcp` | 本地配置已存在；新版还支持 hosted keyless free tier |

## Agent-Reach

仓库：https://github.com/Panniantong/Agent-Reach

定位：给 agent 提供网页、GitHub、社媒、视频字幕、RSS、搜索等多平台读取能力。

本机状态：

- CLI：`/home/user/.local/bin/agent-reach`
- Codex skill：`/home/user/.codex/skills/agent-reach`
- Claude skill：`/home/user/.claude/skills/agent-reach`
- `gh`：`/home/user/.local/bin/gh`，版本 `2.96.0`
- `mcporter`：已安装，版本由 npm 管理

验收结果：

- `agent-reach doctor`：4/15 个通道可用。
- 可用：YouTube、RSS/Atom、全网语义搜索、任意网页。
- GitHub：CLI 已登录，账号 `shihanye0`，仓库/代码读取、搜索、Fork、Issue、PR 等完整可用。
- V2EX / Exa 实时调用：当前 DNS 解析不稳定，出现 `EAI_AGAIN`。

## CodeGraph

仓库：https://github.com/colbymchenry/codegraph

定位：本地代码图谱和 MCP 工具，让 agent 通过 `codegraph_explore` 获取符号、调用链、影响面，减少 grep/read 工具调用。

本机状态：

- CLI：`codegraph`
- 版本：`1.2.0`
- Codex MCP：`[mcp_servers.codegraph] command = "codegraph", args = ["serve", "--mcp"]`
- Claude MCP：`~/.claude.json` 中已加入 `codegraph`
- 全局说明：CodeGraph 已追加到 `~/.codex/AGENTS.md` 和 `~/.claude/CLAUDE.md`

使用边界：

- CodeGraph 不会自动索引所有项目。
- 进入具体代码库后，需要执行 `codegraph init` 生成 `.codegraph/`。
- 只有存在 `.codegraph/` 的项目，agent 才应优先使用 CodeGraph；未初始化项目仍走普通代码发现流程。

## Ponytail

仓库：https://github.com/DietrichGebert/ponytail

定位：约束 AI 编程助手先走“最少必要代码”阶梯：不做不必要功能，优先复用已有代码、标准库、平台原生能力和已安装依赖，只在必要时写最小可读代码。

本机状态：

- npm 包：`@dietrichgebert/ponytail`
- 默认模式：`~/.config/ponytail/config.json` 中设置为 `full`
- Codex skills：`ponytail`、`ponytail-review`、`ponytail-audit`、`ponytail-debt`、`ponytail-gain`、`ponytail-help`
- Claude skills：同上
- 全局规则：已追加到 `~/.codex/AGENTS.md` 和 `~/.claude/CLAUDE.md`

限制：

- 官方 Codex/Claude 插件 marketplace 安装已尝试，但 GitHub TLS / clone timeout 失败。
- 当前不是“插件层安装成功”，而是“npm 包 + skills + 全局规则”的降级接入。
- 降级接入已能让 agent 在编码任务中读取 Ponytail 规则，但没有插件命令和 hook 的完整体验。

## Firecrawl

仓库：https://github.com/firecrawl/firecrawl

MCP 包：https://github.com/firecrawl/firecrawl-mcp-server

定位：把网页转换为干净 Markdown/JSON/截图，并支持搜索、抓取和交互式网页操作。

本机状态：

- Codex：`~/.codex/config.toml` 已配置 `firecrawl` MCP，命令为 `npx -y firecrawl-mcp`。
- Claude Code：`~/.claude/.mcp.json` 已配置 `firecrawl` MCP，命令为 `npx -y firecrawl-mcp`。
- Claude 配置中存在 `FIRECRAWL_API_KEY` 环境键，说明当前是本地 npx + API key 模式。

新版要点：

- Firecrawl MCP `3.22.2` 文档显示 Hosted MCP 支持 keyless free tier。
- keyless free tier 可用能力有限：`scrape`、`search`、`interact` 可无需 API key，且有速率限制。
- `crawl`、`map`、`agent`、`extract` 等完整能力仍需要 API key 或 OAuth。

## 后续动作

- 如需要 Twitter/Reddit/小红书/雪球/LinkedIn 等渠道，再按需执行 `agent-reach install --channels=...` 并提供 cookies、浏览器登录态或代理。
- 新项目需要 CodeGraph 时，在项目根目录执行 `codegraph init`。
- 网络稳定后可重试 Ponytail 官方插件：
  - Codex：`codex plugin marketplace add DietrichGebert/ponytail`
  - Claude Code：`claude plugin marketplace add https://github.com/DietrichGebert/ponytail`
