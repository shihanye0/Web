# Claude Code 使用指南

> 本文档介绍 Claude Code 的常用命令、Superpowers 工作流和 OpenSpec 规范框架

---

## 目录

1. [Claude Code 基础命令](#1-claude-code-基础命令)
2. [Superpowers 工作流](#2-superpowers-工作流)
3. [OpenSpec 规范框架](#3-openspec-规范框架)
4. [常用 Skills 速查](#4-常用-skills-速查)

---

## 1. Claude Code 基础命令

### 1.1 会话控制

| 命令 | 功能 | 示例 |
|------|------|------|
| `/clear` | 清空对话历史 | `/clear` |
| `/compact` | 压缩上下文 | `/compact` |
| `/continue` | 继续上次会话 | `/continue` |
| `/exit` | 退出 Claude Code | `/exit` |

### 1.2 项目管理

| 命令 | 功能 | 示例 |
|------|------|------|
| `/init` | 初始化新项目 | `/init` |
| `/plan` | 进入计划模式 | `/plan` |
| `/review` | 代码审查 | `/review` |
| `/help` | 显示帮助 | `/help` |

### 1.3 开发工作流

| 命令 | 功能 | 示例 |
|------|------|------|
| `/test` | 运行测试 | `/test` |
| `/build` | 构建项目 | `/build` |
| `/debug` | 调试模式 | `/debug` |
| `/audit` | 代码审计 | `/audit` |

### 1.4 Slash Commands (Skills)

使用 `/` 开头的命令可以调用各种 Skills：

```
/brainstorming        # 头脑风暴设计
/subagent-driven      # 子Agent驱动开发
/test-driven          # TDD测试驱动
/using-git-worktrees  # Git工作树隔离
/writing-plans        # 编写计划
/systematic-debugging # 系统调试
/verification         # 验证完成
```

---

## 2. Superpowers 工作流

> Superpowers 是一个完整的软件开发方法论，为 Claude Code 提供自动化工作流

### 2.1 核心工作流

```
1. brainstorm    → 设计前头脑风暴
2. writing-plans → 任务规划
3. subagent-driven-development → 子Agent开发
4. test-driven-development → TDD测试驱动
5. requesting-code-review → 代码审查
6. finishing-a-development-branch → 完成分支
Superpowers 触发方式
在 Claude Code 对话中直接输入：                                                                                /brainstorming                    # 头脑风暴设计              
/writing-plans                     # 编写任务计划            
/subagent-driven-development      # 子Agent驱动开发
/test-driven-development          # TDD测试驱动
/systematic-debugging             # 系统调试
/using-git-worktrees              # Git工作树隔离
/verification-before-completion   # 完成前验证
/requesting-code-review           # 代码审查

Karpathy Skills 插件中的内容完全一致：

  1. 动手前先想清楚 — 不要猜，不要隐藏困惑
  2. 简单优先 — 用最少代码解决问题
  3. 精准改动 — 只碰必须改的
  4. 目标导向执行 — 定义成功标准，循环验证
```

### 2.2 可用 Skills

#### brainstorming
- 在写代码前进行头脑风暴
- 通过提问细化想法
- 展示设计供确认
- 保存设计文档

#### writing-plans
- 将工作分解为小任务（每个2-5分钟）
- 每个任务有精确的文件路径
- 包含完整代码和验证步骤

#### subagent-driven-development
- 为每个任务分发独立子Agent
- 两阶段审查（规范合规性 → 代码质量）
- 可批量执行，有人检查点

#### test-driven-development
- 强制 RED-GREEN-REFACTOR 循环
- 先写失败的测试
- 看测试失败
- 写最小代码
- 看测试通过
- 提交

#### requesting-code-review
- 任务间进行代码审查
- 按严重程度报告问题
- 关键问题阻塞进度

#### finishing-a-development-branch
- 验证测试
- 提供选项（合并/PR/保留/丢弃）
- 清理工作树

### 2.3 使用示例

```
你: /brainstorming
AI: 问你想做什么 → 细化想法 → 展示设计 → 确认 → 保存设计文档

你: 好的，开始
AI: 启动子Agent开发流程，自动执行每个任务...

你: /verification-before-completion
AI: 验证所有任务是否完成，报告问题
```

---

## 3. OpenSpec 规范框架

> OpenSpec 是一个轻量级规范框架，让 AI 在写代码前先达成共识

### 3.1 核心命令

| 命令 | 功能 |
|------|------|
| `openspec init` | 在项目中初始化 OpenSpec |
| `openspec change` | 管理变更提案 |
| `openspec apply` | 应用变更 |
| `openspec archive` | 归档完成的变更 |
| `openspec status` | 显示工件完成状态 |

### 3.2 工作流

```
/opsx:propose <feature>  → 创建提案 (proposal.md, specs/, design.md, tasks.md)
/opsx:apply              → 实现任务
/opsx:archive            → 归档完成的变更
```

### 3.3 使用示例

```bash
# 在项目中初始化
cd your-project
openspec init

# 告诉 AI 创建新功能
/opsx:propose add-dark-mode
```

AI 会创建：
```
openspec/changes/add-dark-mode/
├── proposal.md    # 为什么做这个，改变了什么
├── specs/         # 需求和场景
├── design.md      # 技术方案
└── tasks.md       # 实现清单
```

### 3.4 优势

- **编码前达成共识** — 人和 AI 在写代码前对齐规范
- **保持有序** — 每个变更有自己的文件夹
- **流畅工作** — 随时更新任何工件
- **使用你的工具** — 支持 25+ AI 助手

---

## 4. 常用 Skills 速查

### 4.1 开发流程类

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `/brainstorming` | 头脑风暴、设计讨论 | Socratic 设计细化 |
| `/writing-plans` | 任务规划 | 详细实现计划 |
| `/subagent-driven-development` | 子Agent开发 | 并发子Agent工作流 |
| `/test-driven-development` | TDD测试 | RED-GREEN-REFACTOR 循环 |
| `/executing-plans` | 执行计划 | 批量执行带检查点 |

### 4.2 代码质量类

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `/requesting-code-review` | 代码审查 | 预审查清单 |
| `/receiving-code-review` | 审查反馈 | 处理反馈 |
| `/simplify` | 代码简化 | 扫描冗余代码 |

### 4.3 调试类

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `/systematic-debugging` | 系统调试 | 4阶段根因分析 |
| `/verification-before-completion` | 完成验证 | 确保真正修复 |

### 4.4 Git/版本控制类

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `/using-git-worktrees` | Git工作树 | 并行开发分支 |
| `/finishing-a-development-branch` | 完成分支 | 合并/PR决策工作流 |

### 4.5 Meta 类

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `/writing-skills` | 编写Skills | 创建新Skills |
| `/using-superpowers` | 使用指南 | Skills系统介绍 |

---

## 5. 快速参考

### 5.1 开发新功能流程

```
1. /brainstorming
   └→ 细化需求，设计方案

2. /using-git-worktrees
   └→ 创建隔离的分支工作空间

3. /writing-plans
   └→ 分解为小任务

4. /subagent-driven-development
   └→ 子Agent执行任务，两阶段审查

5. /verification-before-completion
   └→ 验证所有修改

6. /finishing-a-development-branch
   └→ 合并/PR/清理
```

### 5.2 修复 Bug 流程

```
1. /systematic-debugging
   └→ 4阶段根因分析

2. 定位问题后
   └→ /test-driven-development 写测试

3. 修复代码
   └→ /verification-before-completion 验证
```

### 5.3 OpenSpec 流程

```
1. openspec init
   └→ 初始化项目

2. /opsx:propose <feature>
   └→ 创建功能提案和规范

3. 确认设计
   └→ AI 实现任务

4. /opsx:archive
   └→ 归档完成的功能
```

---

## 6. 安装和更新

### Superpowers
- 插件位置: `~/.claude/plugins/superpowers/`
- Skills 自动可用，通过 `/skill-name` 调用

### OpenSpec
- 安装: `npm install -g @fission-ai/openspec`
- 更新: `npm install -g @fission-ai/openspec@latest`
- 在项目中使用: `openspec init`

---

## 7. 参考链接

- [Superpowers GitHub](https://github.com/obra/superpowers)
- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [Claude Code 文档](https://docs.anthropic.com/claude-code)

---

## 8. gstack 技能

> gstack 是 Garry Tan（Y Combinator CEO）开发的 Claude Code 增强工具，将 Claude Code 变成虚拟工程团队。

### 8.1 基本信息

- **安装位置**：`~/.claude/skills/gstack/`
- **版本**：1.45.0.0
- **技能数量**：53 个
- **GitHub**：https://github.com/garrytan/gstack

### 8.2 产品规划类

| 命令                    | 功能       | 使用场景          |
| --------------------- | -------- | ------------- |
| `/office-hours`       | 产品咨询     | 描述要构建什么，获得建议  |
| `/plan-ceo-review`    | CEO 视角审查 | 功能优先级、商业价值分析  |
| `/plan-eng-review`    | 工程经理审查   | 技术方案、架构设计评审   |
| `/plan-design-review` | 设计师审查    | UI/UX 设计评审    |
| `/plan-devex-review`  | 开发者体验审查  | API 设计、文档质量评估 |

**示例**：
```
/office-hours 我想做一个在线代码编辑器
/plan-ceo-review 先做用户系统还是支付功能？
```

### 8.3 代码开发类

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| `/autoplan` | 自动生成开发计划 | 功能开发前的规划 |
| `/review` | 代码审查 | 提交代码前检查 |
| `/ship` | 准备发布 | 版本发布前检查 |
| `/land-and-deploy` | 合并和部署 | PR 合并、自动部署 |

**示例**：
```
/autoplan 实现用户注册和登录功能
/review
```

### 8.4 质量保证类

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| `/qa` | QA 测试 | 功能测试、回归测试 |
| `/qa-only` | 仅生成 QA 报告 | 测试报告生成 |
| `/benchmark` | 性能基准测试 | 性能测试、瓶颈分析 |
| `/canary` | 金丝雀发布测试 | 小范围发布测试 |

**示例**：
```
/qa http://localhost:3000
/benchmark
```

### 8.5 设计类

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| `/design-consultation` | 设计咨询 | 设计方向讨论 |
| `/design-review` | 设计审查 | 设计稿评审 |
| `/design-html` | HTML 设计 | 快速原型设计 |
| `/design-shotgun` | 快速设计迭代 | 多方案探索 |

**示例**：
```
/design-consultation 如何设计一个直观的仪表盘？
/design-shotgun 给我 3 种不同的导航栏设计方案
```

### 8.6 文档类

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| `/document-generate` | 生成文档 | API 文档、README |
| `/document-release` | 发布文档 | 版本发布说明 |

**示例**：
```
/document-generate 为这个项目生成 API 文档
/document-release v2.0.0 的发布说明
```

### 8.7 调试和调查类

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| `/investigate` | 调查问题 | Bug 调试、性能分析 |
| `/retro` | 回顾总结 | 项目回顾、经验总结 |

**示例**：
```
/investigate 为什么页面加载这么慢？
/retro 这个 sprint 的工作回顾
```

### 8.8 上下文管理类

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| `/context-save` | 保存上下文 | 长对话保存 |
| `/context-restore` | 恢复上下文 | 继续之前的工作 |

### 8.9 其他常用命令

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| `/learn` | 学习模式 | 学习新框架、代码示例 |
| `/health` | 健康检查 | 环境检查、依赖检查 |
| `/gstack-upgrade` | 升级 gstack | 获取最新功能 |
| `/freeze` | 冻结代码 | 保护重要代码 |
| `/unfreeze` | 解冻代码 | 恢复可编辑状态 |
| `/guard` | 代码保护 | 关键文件保护 |

### 8.10 gstack 典型工作流

```
1. /office-hours
   └→ 描述要构建什么

2. /plan-ceo-review
   └→ CEO 视角审查

3. /autoplan
   └→ 自动生成开发计划

4. 编写代码...

5. /review
   └→ 代码审查

6. /qa
   └→ QA 测试

7. /ship
   └→ 准备发布

8. /land-and-deploy
   └→ 合并和部署
```

---

## 9. 快速参考卡片

### 日常开发

```
/brainstorming          # 设计前头脑风暴
/autoplan               # 自动生成计划
/test-driven-development # TDD 测试驱动
/review                 # 代码审查
```

### Bug 修复

```
/systematic-debugging   # 系统调试
/investigate            # 调查问题
/verification           # 验证修复
```

### 产品规划

```
/office-hours           # 产品咨询
/plan-ceo-review        # CEO 审查
/plan-eng-review        # 工程审查
```

### 质量保证

```
/qa                     # QA 测试
/benchmark              # 性能测试
/design-review          # 设计审查
```

---

## 10. Everything Claude Code (ECC)

> ECC 是 Anthropic 黑客松获奖者的 Claude Code 配置集合，42K+ GitHub Stars，提供生产级的 agents、skills、hooks、commands、rules 和 MCP 配置。

### 10.1 基本信息

- **GitHub**：https://github.com/affaan-m/everything-claude-code
- **Stars**：42K+
- **安装方式**：`/plugin install everything-claude-code`
- **版本**：1.4.1
- **安装位置**：`~/.claude/plugins/marketplaces/everything-claude-code/`

### 10.2 核心组件

| 组件 | 说明 |
|------|------|
| `agents/` | 专业化子代理（planner、code-reviewer、tdd-guide 等） |
| `skills/` | 工作流定义和领域知识（43 个技能） |
| `commands/` | Slash 命令（/tdd、/plan、/e2e 等） |
| `hooks/` | 触发式自动化（会话持久化、工具前后钩子） |
| `rules/` | 始终遵循的指南（安全、编码风格、测试要求） |
| `mcp-configs/` | MCP 服务器配置 |

### 10.3 常用命令

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| `/tdd` | 测试驱动开发 | 新功能开发前 |
| `/plan` | 实现规划 | 复杂功能拆解 |
| `/e2e` | E2E 测试 | 关键用户流程测试 |
| `/code-review` | 代码审查 | 提交代码前 |
| `/build-fix` | 修复构建错误 | 构建失败时 |
| `/learn` | 从会话中提取模式 | 积累经验 |
| `/skill-create` | 从 git 历史生成技能 | 复用成功模式 |
| `/configure-ecc` | ECC 安装向导 | 首次配置 ECC |

### 10.4 技能分类

#### 框架与语言（21 个）

| 技能 | 说明 |
|------|------|
| `backend-patterns` | 后端架构、API 设计（Node.js/Express/Next.js） |
| `frontend-patterns` | React、Next.js、状态管理、性能优化 |
| `coding-standards` | TypeScript/JavaScript/React/Node.js 编码标准 |
| `python-patterns` | Pythonic 惯用法、PEP 8、类型提示 |
| `python-testing` | pytest、TDD、fixtures、mocking |
| `golang-patterns` | 惯用 Go 模式和约定 |
| `golang-testing` | 表驱动测试、子测试、基准测试 |
| `django-patterns` | Django 架构、DRF REST API、ORM、缓存 |
| `django-security` | Django 安全：认证、CSRF、SQL 注入、XSS |
| `django-tdd` | Django 测试：pytest-django、factory_boy |
| `django-verification` | Django 验证循环：迁移、lint、测试、安全扫描 |
| `laravel-patterns` | Laravel 路由、控制器、Eloquent、队列 |
| `laravel-security` | Laravel 安全：认证、策略、CSRF |
| `laravel-tdd` | Laravel 测试：PHPUnit/Pest、factories |
| `laravel-verification` | Laravel 验证：lint、静态分析、测试 |
| `springboot-patterns` | Spring Boot 架构、REST API、分层服务 |
| `springboot-security` | Spring Security：认证授权、验证、CSRF |
| `springboot-tdd` | Spring Boot TDD：JUnit 5、Mockito、Testcontainers |
| `springboot-verification` | Spring Boot 验证：构建、静态分析、测试 |
| `java-coding-standards` | Java 编码标准：命名、不可变性、Optional、streams |
| `cpp-coding-standards` / `cpp-testing` | C++ 编码标准和测试 |

#### 数据库（3 个）

| 技能 | 说明 |
|------|------|
| `postgres-patterns` | PostgreSQL 查询优化、Schema 设计、索引 |
| `clickhouse-io` | ClickHouse 模式、查询优化、数据分析 |
| `jpa-patterns` | JPA/Hibernate 实体设计、关系、查询优化 |

#### 工作流与质量（8 个）

| 技能 | 说明 |
|------|------|
| `tdd-workflow` | 强制 TDD，80%+ 覆盖率 |
| `verification-loop` | 验证和质量循环模式 |
| `eval-harness` | 评估驱动开发（EDD）框架 |
| `security-review` | 安全检查清单 |
| `security-scan` | 安全扫描 |
| `strategic-compact` | 智能上下文压缩建议 |
| `continuous-learning-v2` | 基于本能的学习，自动提取模式 |
| `iterative-retrieval` | 渐进式上下文精炼 |

#### 研究与 API（3 个）

| 技能 | 说明 |
|------|------|
| `deep-research` | 多源深度研究（firecrawl + exa） |
| `exa-search` | Exa 神经搜索 |
| `claude-api` | Claude API 模式：Messages、streaming、tool use |

#### 业务与内容（5 个）

| 技能 | 说明 |
|------|------|
| `article-writing` | 长文写作 |
| `content-engine` | 多平台内容分发 |
| `market-research` | 市场研究 |
| `investor-materials` | 投资材料 |
| `investor-outreach` | 投资者联系 |

#### 媒体生成（2 个）

| 技能 | 说明 |
|------|------|
| `fal-ai-media` | AI 媒体生成（图像、视频、音频） |
| `video-editing` | AI 辅助视频编辑 |

#### 编排（1 个）

| 技能 | 说明 |
|------|------|
| `dmux-workflows` | 多代理编排（dmux 并行会话） |

### 10.5 规则集

ECC 提供多语言规则集，可按需安装：

| 规则集 | 文件数 | 内容 |
|--------|--------|------|
| Common（推荐） | 8 个 | 编码风格、Git 工作流、测试、安全、性能等 |
| TypeScript/JavaScript | 5 个 | TS/JS 模式、hooks、Playwright 测试 |
| Python | 5 个 | Python 模式、pytest、black/ruff 格式化 |
| Go | 5 个 | Go 模式、表驱动测试、gofmt/staticcheck |

### 10.6 安装与配置

```bash
# 方式 1：插件安装（推荐）
/plugin install everything-claude-code

# 方式 2：使用安装向导
# 在 Claude Code 中说 "configure ecc" 或 "安装 ecc"

# 方式 3：手动安装
git clone https://github.com/affaan-m/everything-claude-code.git /tmp/ecc
# 然后按需复制 skills/ 和 rules/ 到 ~/.claude/
```

### 10.7 与其他工具的对比

| 工具 | 定位 | 特点 |
|------|------|------|
| **ECC** | 全栈开发配置集合 | 43 个技能 + 多语言规则 + hooks |
| **gstack** | 虚拟工程团队 | 产品规划 + QA + 设计 + 部署 |
| **Superpowers** | 开发方法论 | 头脑风暴 → 计划 → 子Agent → TDD |

**推荐搭配使用**：ECC 提供编码标准和框架模式，gstack 提供产品和设计，Superpowers 提供工作流。

---

---

## 11. 迁移后修复指南（2026-05-30 新增）

> 将 Claude Code 从 C 盘迁移到其他盘后，需要执行以下修复步骤，否则所有插件技能不可用。

### 11.1 必须检查的配置

| 配置项 | 文件 | 要求 |
|--------|------|------|
| `CLAUDE_CODE_SIMPLE` | settings.json env | **必须删除**（会禁用所有插件） |
| `skillListingBudgetFraction` | settings.local.json | 设为 `0.8`（显示全部技能） |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | settings.json env | 设为 `500000` |
| `installed_plugins.json` | plugins/ | 所有路径指向实际盘符 |
| `known_marketplaces.json` | plugins/ | 所有路径指向实际盘符 |
| `ecc/install-state.json` | ecc/ | 所有路径指向实际盘符 |
| `.mcp.json` | 根目录 | filesystem 路径正确 |
| gstack 子技能 | skills/ | 运行 `cd ~/.claude/skills/gstack && bash setup` |
| Superpowers 插件 | plugins/ | 在 installed_plugins.json 中注册 |

### 11.2 快速修复脚本

```python
import os

OLD = bytes([0x45, 0x3a, 0x5c, 0x5c, 0x55, 0x73, 0x65, 0x72, 0x73, 0x5c, 0x5c, 0x4c, 0x65, 0x6e, 0x6f, 0x76, 0x6f])
NEW = bytes([0x43, 0x3a, 0x5c, 0x5c, 0x55, 0x73, 0x65, 0x72, 0x73, 0x5c, 0x5c, 0x4c, 0x65, 0x6e, 0x6f, 0x76, 0x6f])

for path in [
    r'C:\Users\Lenovo\.claude\plugins\installed_plugins.json',
    r'C:\Users\Lenovo\.claude\plugins\known_marketplaces.json',
    r'C:\Users\Lenovo\.claude\ecc\install-state.json',
    r'C:\Users\Lenovo\.claude\.mcp.json',
    r'C:\Users\Lenovo\.codex\config.toml',
]:
    if not os.path.exists(path):
        continue
    with open(path, 'rb') as f:
        content = f.read()
    count = content.count(OLD)
    if count > 0:
        with open(path, 'wb') as f:
            f.write(content.replace(OLD, NEW))
        print(f'Fixed {os.path.basename(path)}: {count}')
```

---

*文档更新日期: 2026-05-30*
