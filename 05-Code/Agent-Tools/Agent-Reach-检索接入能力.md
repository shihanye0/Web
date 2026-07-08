# Agent-Reach：智能体信息读取与检索接入

## 基本信息

- 仓库：https://github.com/Panniantong/Agent-Reach
- 本机 Skill：`/home/user/.skillshub/agent-reach/SKILL.md`
- 定位：给 agent 提供网页、GitHub、社媒、视频字幕等多平台读取和检索能力。

## 本机状态

已存在 Skill，Codex 通过符号链接读取，Claude Code 有本地 skill 副本：

```bash
/home/user/.skillshub/agent-reach/SKILL.md
/home/user/.codex/skills/agent-reach -> /home/user/.skillshub/agent-reach
/home/user/.claude/skills/agent-reach/SKILL.md
```

CLI 已安装：

```bash
which agent-reach
/home/user/.local/bin/agent-reach
```

`agent-reach doctor` 当前结果：

- 可用：GitHub、YouTube、RSS/Atom、全网语义搜索、任意网页、B站搜索 API。
- GitHub：`gh` CLI 已登录，账号 `shihanye0`，GitHub 仓库/代码读取、搜索、Fork、Issue、PR 等完整可用。
- V2EX：当前连接超时，可能需要代理。
- 可选渠道：Twitter/X、Reddit、Facebook、Instagram、小红书、小宇宙、雪球、LinkedIn 仍需按需安装或登录。

## Skill 中记录的能力

- search：网页搜索。
- dev：GitHub/代码读取。
- web：网页、文章、公众号、RSS。
- video：YouTube、B站、播客字幕。
- social：小红书、抖音、微博、Twitter、B站、V2EX、Reddit。
- career：LinkedIn/职位。

## 使用建议

- P0：保留作为研究前置能力。
- 对当前 Codex/Claude Code 环境来说，优先使用已安装 Skill 和 CLI。
- 若后续需要社媒/招聘类渠道，再按 `agent-reach install --channels=...` 安装，并由用户提供 cookies、浏览器登录态或代理。
- GitHub 通道已完成登录，无需继续配置。
