![Sliver Engineering Workflow 封面](assets/cover-zh-CN.png)

# Sliver Engineering Workflow

Sliver Engineering Workflow 是一套面向 Codex / Cursor / 其他代码 agent 的工程执行 skill。它把一套偏生产级的个人工程方法论固化为可安装、可复用、可检查的 agent 工作流：先确认当前真源，再锁定 owner 层和产品边界，然后设计主线架构、实现、验收、写回文档，最后做漂移检查。

它不是提示词合集，也不是通用项目脚手架。它的目标是让 agent 在立项、新增功能、修改功能、重构、排障、验收和交付时少漂移，尤其避免常见的“先写 UI/接口/补丁，再倒推架构”的工作方式。

## 能干什么

- 立项和从 0 到 1：先建立立项期临时 agent 宪法，把笼统想法整理成唯一推荐产品主线，记录非目标和第一闭环，推荐并确认一个技术栈，然后再建立 `dev-docs/`、架构 owner、框架最佳实践门禁和验收证据，最后才搭建代码骨架。
- 半路项目接管：针对已经写到一半、继承而来、缺少 `AGENTS.md` 或缺少 `dev-docs` 真源的项目，先审计现状、立 agent 宪法、建立内部真源索引，并在危险治理/产品边界动作前让用户确认。
- 新增功能和修改功能：要求先审计当前代码、文档、脚本、测试、git 状态，再决定单一 owner 层和契约。
- 重构和排障：把问题归到正确层面，要求先复现、查证据、审计 git 引入历史，必要时查官方文档/GitHub issue/PR，建立可证伪假设和回归门禁，避免靠猜乱补丁。
- 严格验收：按风险面选择 build/test/contract/browser/live-device/doc gate，并区分代码门禁、集成链路、真实设备或用户验收。
- 防漂移：通过 `agent-drift-lock`、Evidence Log、停止条件、文档写回和 guardrails 脚本约束 agent。
- 上下文交接：在窗口上下文过大或换 agent 时，输出可直接复制的新窗口交接文本，包含 git 状态、验证证据、运行状态、漂移警告和下一步命令。
- 交接给其他 agent：提供项目 bootstrap 模板、检查脚本和一份完整 feature lifecycle 示例，降低新人或新 agent 上手时的抽象漂移。

## 适合什么项目

适合这些场景：

- 你希望 agent 严格遵守“架构优先、设计优先、不乱补丁、严格验收”。
- 项目中有 `AGENTS.md`、`dev-docs/`、`docs/`、架构文档、验收文档或 agent 宪法。
- 项目还没启动，但你希望先建立产品边界、架构主线和验收真源。
- 项目已经做到一半，但缺少 `AGENTS.md`、`dev-docs`、可靠 owner map 或当前交接记录。
- 项目已经启动，但 agent 经常忘记当前代码事实、旧结论、文档索引或 git 边界。

不适合这些场景：

- 只想要一次性代码生成，不关心长期维护。
- 不允许 agent 读当前仓库事实，只想根据口头描述直接写代码。
- 希望 skill 数学意义上保证任何模型永远不漂移。这个 skill 能显著压低漂移概率，但语义质量仍依赖 agent 如实读取真源、记录证据并执行验收。

## 目录结构

```text
sliver-code-skill/
├── README.zh-CN.md
├── README.md
└── sliver-engineering-workflow/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── assets/
    │   ├── project-bootstrap/
    │   └── project-adoption/
    ├── examples/
    │   ├── one-feature-lifecycle.md
    │   └── mid-project-adoption-lifecycle.md
    ├── references/
    └── scripts/
        └── check_project_guardrails.py
```

## 安装到 Codex

从仓库根目录执行：

```bash
mkdir -p ~/.codex/skills
cp -R sliver-engineering-workflow ~/.codex/skills/sliver-engineering-workflow
```

如果本机已经装过旧版本，可以用覆盖更新：

```bash
mkdir -p ~/.codex/skills/sliver-engineering-workflow
cp -R sliver-engineering-workflow/. ~/.codex/skills/sliver-engineering-workflow/
```

安装后重启 Codex，让新的 skill 进入后续会话的可用 skills 列表。

## 验证安装

如果你的 Codex 带有官方 skill validator，可以运行：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  ~/.codex/skills/sliver-engineering-workflow
```

检查 bundled bootstrap 模板：

```bash
python3 ~/.codex/skills/sliver-engineering-workflow/scripts/check_project_guardrails.py \
  ~/.codex/skills/sliver-engineering-workflow/assets/project-bootstrap \
  --allow-template
```

检查一个真实项目：

```bash
python3 ~/.codex/skills/sliver-engineering-workflow/scripts/check_project_guardrails.py \
  /path/to/project
```

如果项目只有 `docs/`，还没有 `dev-docs/`，可以先用轻量模式：

```bash
python3 ~/.codex/skills/sliver-engineering-workflow/scripts/check_project_guardrails.py \
  /path/to/project \
  --truth-dir docs
```

如果是已经做了一半、继承而来、需要半路接管的项目：

```bash
python3 ~/.codex/skills/sliver-engineering-workflow/scripts/check_project_guardrails.py \
  /path/to/project \
  --mode adoption
```

## 怎么使用

在 Codex 里直接要求 agent 使用这个 skill，例如：

```text
用 sliver-engineering-workflow 给这个空项目做立项和第一阶段架构。
```

```text
用 sliver-engineering-workflow 审计当前真源后，再实现这个功能，禁止乱补丁。
```

```text
用 sliver-engineering-workflow 检查这个项目有没有漂移，重点看 dev-docs、owner 层、停止条件和验收证据。
```

```text
用 sliver-engineering-workflow 先接管这个半路项目：审计当前真源，提出 AGENTS.md/dev-docs 治理面，列出需要我确认的危险接管动作，然后给第一个安全任务。
```

Cursor 或其他 agent 环境也可以复用这套文件，但没有 Codex 的 `.codex/sessions` 和 memories 时，应改用 `agent-transcripts/`、聊天导出、当前 diff、commit history、review comments 和当前文档作为会话证据。

## 许可证

MIT。详见 [LICENSE](LICENSE)。
