# AI 开发工具集配置说明

> 配置日期：2026-07-13
> 三个开源项目的说明和配置方法

---

## 📋 项目概览

| 项目 | Stars | 用途 | 许可证 |
|------|-------|------|--------|
| **grill-me-codex** | 641 ⭐ | 跨模型代码审查（Claude + Codex） | Other |
| **OpenSpec** | 60,452 ⭐ | 规格驱动开发（SDD）框架 | MIT |
| **Trellis** | 12,420 ⭐ | AI编码工程框架（持久化规格+任务+记忆） | AGPL-3.0 |

---

## 1. grill-me-codex

### 项目说明

**核心理念**：两个AI模型互相审查，避免"自己给自己打分"的问题。

**三个阶段**：
- **Act 1**：Claude 逐个问题审查你的计划，直到决策树解决
- **Act 2**：Codex 对计划进行对抗性审查（只读模式）
- **Act 3**（可选）：角色互换 — Codex 写代码，Claude 审查 diff

**可用 Skills**：
| Skill | 功能 |
|-------|------|
| `/grill-me-codex` | 完整流程：计划审查 + Codex 审查 + 可选构建 |
| `/grill-with-docs-codex` | 同上，但会对照项目的 `CONTEXT.md` 进行挑战 |
| `/codex-review` | 只做 Codex 审查（已有计划时） |
| `/codex-build` | Codex 实现计划，Claude 验证 |

### 安装配置

```bash
# 已克隆到 /home/user/github-product/grill-me-codex
# 已复制 skills 到 ~/.claude/skills/

# 前置条件
npm install -g @openai/codex@latest
codex login  # 需要 ChatGPT 账号

# 使用方式
/grill-me-codex "你的功能描述"
```

### 调参配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MAX_ROUNDS` | 5 | 最大审查轮数 |
| `PLAN_FILE` | PLAN.md | 计划文件位置 |
| `LOG_FILE` | PLAN-REVIEW-LOG.md | 审查日志 |
| `MAX_FIX_ROUNDS` | 2 | Codex 构建时的最大修复轮数 |

---

## 2. OpenSpec

### 项目说明

**核心理念**：规格驱动开发（Spec-Driven Development），在写代码前先达成共识。

**工作流程**：
```
/opsx:explore    → 探索想法，AI帮你理清需求
/opsx:propose    → 创建变更提案，生成规格文档
/opsx:apply      → 实现任务
/opsx:archive    → 归档完成的变更
```

**核心概念**：
- **Changes**：每个变更一个文件夹，包含 proposal、specs、design、tasks
- **Specs**：规格文档，定义产品行为
- **Stores**（Beta）：跨仓库的规划共享

### 安装配置

```bash
# 已全局安装
npm install -g @fission-ai/openspec@latest
openspec --version  # 1.6.0

# 在项目中初始化
cd your-project
openspec init --tools claude,codex

# 使用方式
/opsx:explore     # 探索想法
/opsx:propose "add dark mode"  # 创建提案
/opsx:apply       # 实现任务
/opsx:archive     # 归档
```

### 支持的工具

OpenSpec 支持 25+ AI 编码工具，包括：
- Claude Code (`.claude/skills/openspec-*/SKILL.md`)
- Codex (`.codex/skills/openspec-*/SKILL.md`)
- Cursor, Cline, Continue, Windsurf 等

---

## 3. Trellis

### 项目说明

**核心理念**：为AI编码提供持久化规格、任务和记忆，让每个新会话都有真实上下文。

**四大能力**：
| 能力 | 作用 |
|------|------|
| **Auto-injected specs** | 在 `.trellis/spec/` 写一次规格，自动注入每个会话 |
| **Task-centered workflow** | PRD、实现、审查上下文都在 `.trellis/tasks/` |
| **Project memory** | 工作日志保留上次发生的事情 |
| **Multi-platform** | 同一套结构支持 17+ AI 编码平台 |

**工作流程**（4阶段循环）：
1. **Plan** → `trellis-brainstorm` 逐个问题理清需求，写 `prd.md`
2. **Implement** → `trellis-implement` 子代理根据 PRD 写代码
3. **Verify** → `trellis-check` 子代理审查 diff 并运行测试
4. **Finish** → `trellis-update-spec` 将新学习写回规格

### 安装配置

```bash
# 已全局安装
npm install -g @mindfoldhq/trellis@latest
trellis --version  # 0.6.6

# 在项目中初始化
cd your-project
trellis init --claude --codex -u your-name --yes

# 使用方式
# 1. 描述你想要什么
# 2. AI 逐个问题理清需求
# 3. 让它运行 — AI 自动检查规格、lint、类型检查、测试
# 4. 输入 /trellis:finish-work 完成工作
```

### 目录结构

```
.trellis/
├── spec/           # 规格文件（跨会话持久化）
├── tasks/          # 任务 PRD、实现上下文
└── workspace/      # 工作日志（每个开发者独立）

.claude/
├── skills/         # Trellis skills
├── commands/       # Trellis commands
├── hooks/          # 自动注入钩子
└── settings.json   # 配置
```

---

## 🔧 配置状态

### 已完成的配置

| 项目             | 全局安装         | Claude Code Skills | Codex Skills |
| -------------- | ------------ | ------------------ | ------------ |
| grill-me-codex | -            | ✅ 已复制              | -            |
| OpenSpec       | ✅ `openspec` | ✅ 已初始化             | ✅ 已初始化       |
| Trellis        | ✅ `trellis`  | ✅ 项目级配置            | ✅ 项目级配置      |

### 克隆位置

```
/home/user/github-product/
├── grill-me-codex/    # 跨模型代码审查
├── OpenSpec/          # 规格驱动开发
├── Trellis/           # AI编码工程框架（浅克隆）
└── trellis-workspace/ # Trellis 初始化示例
```

---

## 📖 详细使用教程

### 1. grill-me-codex 使用教程

#### 场景一：从零开始规划一个功能

```bash
# 在 Claude Code 中输入
/grill-me-codex "实现一个用户认证系统，支持手机号登录和JWT token"
```

**Claude 会做的事**：

```
Act 1（Claude 审查你）：
  Claude: "你的目标用户是谁？"
  你: "移动端用户"
  Claude: "需要支持第三方登录吗？"
  你: "暂时不需要"
  Claude: "JWT 过期时间设多少？"
  你: "2小时"
  ... 逐个问题直到决策树解决
  ↓
  输出: PLAN.md（完整的计划文档）

Act 2（Codex 审查计划）：
  Claude 调用 Codex（只读模式）
  Codex: "你的密码存储方案是什么？"
  Codex: "并发登录怎么处理？"
  Codex: "Token 刷新机制呢？"
  ... Codex 提出问题，Claude 回答并修改计划
  ↓
  输出: PLAN-REVIEW-LOG.md（审查日志）

Act 3（可选：角色互换构建）：
  Codex 按照 PLAN.md 写代码
  Claude 审查 Codex 的 diff
  有问题就让 Codex 修复
```

#### 场景二：已有计划，只想让 Codex 审查

```bash
# 先写好 PLAN.md，然后
/codex-review
```

#### 场景三：计划已通过，让 Codex 实现

```bash
/codex-build
# Codex 会按照 PLAN.md 写代码
# Claude 会审查 diff
```

#### 调参示例

```bash
# 设置最大审查轮数为 3 轮
/grill-me-codex "实现XX功能" rounds=3

# 指定计划文件
/codex-review plan=MY_PLAN.md
```

---

### 2. OpenSpec 使用教程

#### 完整工作流示例

```bash
# 步骤1：探索想法（不确定怎么做时）
/opsx:explore
# AI: 你想做什么？
# 你: 我想给网站加暗色模式，但不确定怎么做最干净
# AI: 让我看看你的样式设置...最干净的路径是 CSS 变量 + 小型主题上下文
# AI: 要我帮你规划吗？
# 你: 好的

# 步骤2：创建提案
/opsx:propose add-dark-mode
# AI 会创建：
# openspec/changes/add-dark-mode/
#   ├── proposal.md    ← 为什么做、改什么
#   ├── specs/         ← 需求和场景
#   ├── design.md      ← 技术方案
#   └── tasks.md       ← 实现清单

# 步骤3：实现任务
/opsx:apply
# AI 会按 tasks.md 逐个实现：
# ✓ 1.1 添加主题上下文 provider
# ✓ 1.2 创建切换组件
# ✓ 2.1 添加 CSS 变量
# ✓ 2.2 接入 localStorage

# 步骤4：归档
/opsx:archive
# 变更归档到 openspec/changes/archive/2026-07-13-add-dark-mode/
```

#### 单独使用某个命令

```bash
# 只探索，不写代码
/opsx:explore

# 查看当前变更状态
/opsx:sync

# 更新规格文档
/opsx:update
```

#### 在已有项目中使用

```bash
cd your-existing-project
openspec init --tools claude,codex

# 然后正常对话
/opsx:propose "重构用户模块"
```

---

### 3. Trellis 使用教程

#### 首次初始化

```bash
cd your-project
trellis init --claude --codex -u your-name --yes
```

#### 日常工作流

```
步骤1：描述你想要什么（自然语言）
  你: "我需要一个用户仪表盘，显示最近的订单和统计数据"
  
步骤2：AI 逐个问题理清需求（brainstorm）
  AI: "仪表盘需要实时更新吗？"
  你: "不需要，手动刷新就行"
  AI: "统计数据包括哪些维度？"
  你: "按天、按周、按月"
  ... 
  AI 写入 prd.md

步骤3：自动实现
  AI 调用 trellis-implement 子代理
  - 根据 PRD 写代码
  - 自动检查规格、lint、类型检查、测试
  
步骤4：完成工作
  /trellis:finish-work
  - 归档任务
  - 更新工作日志
  - 下次会话自动加载上下文
```

#### Trellis 目录结构

```
your-project/
├── .trellis/
│   ├── spec/              # 规格文件（跨会话持久化）
│   │   ├── architecture.md
│   │   └── conventions.md
│   ├── tasks/             # 任务 PRD、实现上下文
│   │   └── dashboard/
│   │       ├── prd.md
│   │       └── implement.jsonl
│   └── workspace/         # 工作日志
│       └── journal.md
├── .claude/
│   ├── skills/            # Trellis skills
│   │   ├── trellis-brainstorm/
│   │   ├── trellis-implement/
│   │   └── trellis-check/
│   └── commands/
│       └── trellis/
└── src/                   # 你的代码
```

#### 跨会话记忆

```
会话1：你开发了用户模块
  → /trellis:finish-work
  → 工作日志记录：完成了用户CRUD、用了JWT认证

会话2：你开始新功能
  → Trellis 自动读取工作日志
  → AI 知道：已有用户模块、用JWT、不用重复实现认证
```

---

## 🔧 常见问题

### Q: 三个工具会冲突吗？
**A**: 不会。它们的配置在不同位置：
- grill-me-codex: `~/.claude/skills/grill-me-codex/`
- OpenSpec: `~/.claude/skills/openspec-*/`
- Trellis: 项目级 `.claude/skills/trellis-*/`

### Q: 必须三个都用吗？
**A**: 不是。根据需求选择：
- 只需要规格管理 → OpenSpec
- 只需要跨会话记忆 → Trellis
- 只需要跨模型审查 → grill-me-codex
- 都需要 → 组合使用

### Q: grill-me-codex 需要 OpenAI API Key 吗？
**A**: 需要 Codex CLI 登录（ChatGPT 账号即可，Free/Plus/Pro 都行）。

### Q: Trellis 的规格会和 CLAUDE.md 冲突吗？
**A**: 不会。Trellis 在 `.trellis/spec/` 管理规格，CLAUDE.md 是全局配置，两者互补。

---

## 📖 使用建议

### 选择哪个工具？

| 场景 | 推荐工具 |
|------|----------|
| 需要跨模型审查计划 | grill-me-codex |
| 需要规格驱动开发 | OpenSpec |
| 需要持久化项目记忆 | Trellis |
| 大型项目长期维护 | Trellis + OpenSpec |
| 快速原型验证 | grill-me-codex |

### 组合使用

这三个工具可以组合使用：

1. **OpenSpec** 管理规格和变更流程
2. **Trellis** 管理任务和项目记忆
3. **grill-me-codex** 在关键决策时进行跨模型审查

---

## 🔗 相关链接

- grill-me-codex: https://github.com/chaseai-yt/grill-me-codex
- OpenSpec: https://github.com/Fission-AI/OpenSpec
- Trellis: https://github.com/mindfold-ai/Trellis
- Trellis 文档: https://docs.trytrellis.app/
- OpenSpec 文档: https://openspec.dev/

---

*最后更新：2026-07-13*
