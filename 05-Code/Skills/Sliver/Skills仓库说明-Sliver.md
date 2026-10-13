# 可安装 Skill 清单

## 微信群

![微信群：甲壳虫 Agent-vibe coding 交流](assets/wechat-group.jpg)

这份清单用于发给用户，列出当前整理出的可安装 skill 项目、简短描述和源链接。这里的“可安装项”只按独立安装边界列：可以单独安装的 skill 单独列；同属于一个技能包/项目的子 skill 不拆成一级条目，只写在该技能包的“包含能力”里。

不包含本机 Codex 预装的 system skill，也不包含插件缓存里的运行时副本。

## 推荐安装方式

- OpenAI 官方 curated skills：每个 `skills/.curated/<skill-name>` 是独立可安装 skill，可使用 Codex 的 `skill-installer` 按需安装。
- Superpowers：这是一个技能包/项目，按项目安装说明执行：`https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.codex/INSTALL.md`。
- PUA：这是一个技能包/项目，Codex 推荐执行：`https://raw.githubusercontent.com/tanweai/pua/main/.codex/INSTALL.md`。
- Sliver Engineering Workflow：使用 Gitee 仓库 `https://gitee.com/sliver-ring_admin/sliver-code-skill`。

## 技能包 / 项目

| 可安装项 | 简短描述 | 包含能力 | 链接 |
|---|---|---|---|
| `superpowers` | 面向 coding agent 的完整软件开发工作流技能包，强调先查相关 skill、计划、TDD、系统调试、验证和分支收尾。 | `brainstorming`、`writing-plans`、`executing-plans`、`test-driven-development`、`systematic-debugging`、`verification-before-completion`、`requesting-code-review`、`receiving-code-review`、`dispatching-parallel-agents`、`subagent-driven-development`、`using-git-worktrees`、`finishing-a-development-branch`、`writing-skills` 等。 | [https://github.com/obra/superpowers](https://github.com/obra/superpowers) |
| `pua` | 高能动性/反摆烂技能包，用压力升级、方法论路由和自动迭代逼迫 agent 穷尽方案。 | Codex 推荐核心：`pua`、`pua-en`、`pua-ja`；通用/Claude Code 子模式：`pua-loop`、`shot`、`yes`、`mama`、`p7`、`p9`、`p10`、`pro` 等。 | [https://github.com/tanweai/pua](https://github.com/tanweai/pua) |
| `sliver-engineering-workflow` | Sliver 风格 repo-native 工程流：立项、接管、feature/refactor/debug/review/release、新窗口交接；强调架构优先、真源/dev-docs、agent 宪法、严格验收和 debug 证据纪律。 | `sliver-engineering-workflow` | [https://gitee.com/sliver-ring_admin/sliver-code-skill](https://gitee.com/sliver-ring_admin/sliver-code-skill) |

## OpenAI 官方可单独安装 Skills

来源：https://github.com/openai/skills/tree/main/skills/.curated

| Skill | 简短描述 | 链接 |
|---|---|---|
| `aspnet-core` | ASP.NET Core 应用开发、重构、架构与升级。 | [openai/skills: aspnet-core](https://github.com/openai/skills/tree/main/skills/.curated/aspnet-core) |
| `chatgpt-apps` | ChatGPT Apps SDK 应用开发，覆盖 MCP server 与 widget UI。 | [openai/skills: chatgpt-apps](https://github.com/openai/skills/tree/main/skills/.curated/chatgpt-apps) |
| `cli-creator` | 从 API、OpenAPI、curl、SDK 或脚本生成可复用 CLI。 | [openai/skills: cli-creator](https://github.com/openai/skills/tree/main/skills/.curated/cli-creator) |
| `cloudflare-deploy` | 部署 Workers、Pages 等 Cloudflare 应用和基础设施。 | [openai/skills: cloudflare-deploy](https://github.com/openai/skills/tree/main/skills/.curated/cloudflare-deploy) |
| `define-goal` | 把模糊目标澄清成可衡量、可执行的目标。 | [openai/skills: define-goal](https://github.com/openai/skills/tree/main/skills/.curated/define-goal) |
| `figma` | 读取 Figma 设计上下文、资产和变量，并辅助转代码。 | [openai/skills: figma](https://github.com/openai/skills/tree/main/skills/.curated/figma) |
| `figma-code-connect-components` | 建立 Figma 组件与代码组件的 Code Connect 映射。 | [openai/skills: figma-code-connect-components](https://github.com/openai/skills/tree/main/skills/.curated/figma-code-connect-components) |
| `figma-create-design-system-rules` | 为代码库生成 Figma-to-code 设计系统规则。 | [openai/skills: figma-create-design-system-rules](https://github.com/openai/skills/tree/main/skills/.curated/figma-create-design-system-rules) |
| `figma-create-new-file` | 创建新的 Figma 或 FigJam 文件。 | [openai/skills: figma-create-new-file](https://github.com/openai/skills/tree/main/skills/.curated/figma-create-new-file) |
| `figma-generate-design` | 把页面、视图或描述生成到 Figma 画布。 | [openai/skills: figma-generate-design](https://github.com/openai/skills/tree/main/skills/.curated/figma-generate-design) |
| `figma-generate-library` | 从代码库生成或更新专业级 Figma 设计系统。 | [openai/skills: figma-generate-library](https://github.com/openai/skills/tree/main/skills/.curated/figma-generate-library) |
| `figma-implement-design` | 按 Figma 设计实现生产级 UI 代码。 | [openai/skills: figma-implement-design](https://github.com/openai/skills/tree/main/skills/.curated/figma-implement-design) |
| `figma-use` | 调用 use_figma 前的必需前置 skill，指导 Figma 文件内读写操作。 | [openai/skills: figma-use](https://github.com/openai/skills/tree/main/skills/.curated/figma-use) |
| `gh-address-comments` | 处理 GitHub PR review comments 或 issue comments。 | [openai/skills: gh-address-comments](https://github.com/openai/skills/tree/main/skills/.curated/gh-address-comments) |
| `gh-fix-ci` | 排查并修复 GitHub Actions CI 失败。 | [openai/skills: gh-fix-ci](https://github.com/openai/skills/tree/main/skills/.curated/gh-fix-ci) |
| `hatch-pet` | 创建、修复、验证和打包 Codex 动画宠物 spritesheet。 | [openai/skills: hatch-pet](https://github.com/openai/skills/tree/main/skills/.curated/hatch-pet) |
| `jupyter-notebook` | 创建、脚手架化或编辑 Jupyter Notebook。 | [openai/skills: jupyter-notebook](https://github.com/openai/skills/tree/main/skills/.curated/jupyter-notebook) |
| `linear` | 读取、创建或更新 Linear issue、项目和团队工作流。 | [openai/skills: linear](https://github.com/openai/skills/tree/main/skills/.curated/linear) |
| `migrate-to-codex` | 把指令文件、skills、agents、MCP 配置迁移到 Codex。 | [openai/skills: migrate-to-codex](https://github.com/openai/skills/tree/main/skills/.curated/migrate-to-codex) |
| `netlify-deploy` | 使用 Netlify CLI 部署、发布或关联站点。 | [openai/skills: netlify-deploy](https://github.com/openai/skills/tree/main/skills/.curated/netlify-deploy) |
| `notion-knowledge-capture` | 把对话、笔记和决策整理成 Notion 知识库页面。 | [openai/skills: notion-knowledge-capture](https://github.com/openai/skills/tree/main/skills/.curated/notion-knowledge-capture) |
| `notion-meeting-intelligence` | 基于 Notion 上下文准备会议议程、预读和材料。 | [openai/skills: notion-meeting-intelligence](https://github.com/openai/skills/tree/main/skills/.curated/notion-meeting-intelligence) |
| `notion-research-documentation` | 跨 Notion 资料研究并输出结构化文档。 | [openai/skills: notion-research-documentation](https://github.com/openai/skills/tree/main/skills/.curated/notion-research-documentation) |
| `notion-spec-to-implementation` | 把 Notion PRD/spec 转成实施计划、任务和进度跟踪。 | [openai/skills: notion-spec-to-implementation](https://github.com/openai/skills/tree/main/skills/.curated/notion-spec-to-implementation) |
| `openai-docs` | 查 OpenAI 官方文档，辅助模型/API 选择和升级。 | [openai/skills: openai-docs](https://github.com/openai/skills/tree/main/skills/.curated/openai-docs) |
| `pdf` | 读写、审阅 PDF，并通过渲染检查布局。 | [openai/skills: pdf](https://github.com/openai/skills/tree/main/skills/.curated/pdf) |
| `playwright` | 从终端自动化真实浏览器，做 UI 流程调试和截图。 | [openai/skills: playwright](https://github.com/openai/skills/tree/main/skills/.curated/playwright) |
| `playwright-interactive` | 通过持久浏览器/Electron 会话做快速交互式 UI 调试。 | [openai/skills: playwright-interactive](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive) |
| `render-deploy` | 分析项目并生成 Render 部署配置和 Dashboard 链接。 | [openai/skills: render-deploy](https://github.com/openai/skills/tree/main/skills/.curated/render-deploy) |
| `screenshot` | 执行桌面或系统级截图。 | [openai/skills: screenshot](https://github.com/openai/skills/tree/main/skills/.curated/screenshot) |
| `security-best-practices` | 对 Python、JS/TS、Go 做安全最佳实践审查。 | [openai/skills: security-best-practices](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices) |
| `security-ownership-map` | 基于 git 历史生成安全 ownership、bus factor 和敏感代码归属图。 | [openai/skills: security-ownership-map](https://github.com/openai/skills/tree/main/skills/.curated/security-ownership-map) |
| `security-threat-model` | 对代码库或路径做威胁建模，列出资产、边界、攻击路径和缓解措施。 | [openai/skills: security-threat-model](https://github.com/openai/skills/tree/main/skills/.curated/security-threat-model) |
| `sentry` | 通过 Sentry CLI 只读查询 issue、event 和生产错误概况。 | [openai/skills: sentry](https://github.com/openai/skills/tree/main/skills/.curated/sentry) |
| `speech` | 通过 OpenAI Audio API 生成旁白、语音提示或批量 TTS。 | [openai/skills: speech](https://github.com/openai/skills/tree/main/skills/.curated/speech) |
| `transcribe` | 转写音频/视频，可带说话人提示和 diarization。 | [openai/skills: transcribe](https://github.com/openai/skills/tree/main/skills/.curated/transcribe) |
| `vercel-deploy` | 部署应用或网站到 Vercel，生成预览或生产部署。 | [openai/skills: vercel-deploy](https://github.com/openai/skills/tree/main/skills/.curated/vercel-deploy) |
| `winui-app` | 用 C#、Windows App SDK 和 WinUI 3 开发现代 Windows 桌面应用。 | [openai/skills: winui-app](https://github.com/openai/skills/tree/main/skills/.curated/winui-app) |
| `yeet` | 在用户明确要求时完成 stage、commit、push、开 GitHub PR 流程。 | [openai/skills: yeet](https://github.com/openai/skills/tree/main/skills/.curated/yeet) |
