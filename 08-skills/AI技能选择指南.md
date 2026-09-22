# AI 技能选择指南

> 配置日期：2026-07-13
> 解决"技能太多不知道用哪个"的问题

---

## 🎯 核心原则

```
不要试图用所有技能
根据场景选择 1-2 个最合适的
```

---

## 📊 技能分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    第一层：元技能（指导如何使用技能）          │
│  using-superpowers, gstack                                  │
├─────────────────────────────────────────────────────────────┤
│                    第二层：规划技能（做什么）                 │
│  autoplan, plan, brainstorming, grill-me-codex, OpenSpec    │
├─────────────────────────────────────────────────────────────┤
│                    第三层：执行技能（怎么做）                 │
│  tdd-workflow, code-review, ship, Trellis                   │
├─────────────────────────────────────────────────────────────┤
│                    第四层：专项技能（特定领域）               │
│  frontend-design, security-review, database-reviewer        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 按场景选择技能

### 场景 1：接到新需求，不知道怎么做

```
你: "老板让我做一个用户仪表盘"
    ↓
用什么？→ brainstorming 或 autoplan
```

| 技能 | 用途 | 调用方式 |
|------|------|----------|
| **brainstorming** | 头脑风暴，理清需求 | `/brainstorming` |
| **autoplan** | 自动生成开发计划 | `/autoplan` |
| **plan** | 手动规划，更可控 | `/plan` |

**推荐组合**：`brainstorming` → `plan`

---

### 场景 2：需求明确，要写代码了

```
你: "需求清楚了，开始写代码"
    ↓
用什么？→ tdd-workflow 或直接写
```

| 技能 | 用途 | 调用方式 |
|------|------|----------|
| **tdd-workflow** | 测试驱动开发 | `/tdd-workflow` |
| **bdd** | 行为驱动开发 | `/bdd` |
| **直接写** | 简单任务不需要技能 | 直接 coding |

**推荐**：简单任务直接写，复杂任务用 `tdd-workflow`

---

### 场景 3：代码写完了，要审查

```
你: "代码写完了，帮我看看"
    ↓
用什么？→ code-review 或 security-review
```

| 技能 | 用途 | 调用方式 |
|------|------|----------|
| **code-review** | 通用代码审查 | `/code-review` |
| **security-review** | 安全审查 | `/security-review` |
| **requesting-code-review** | 请求他人审查 | `/requesting-code-review` |

**推荐**：先 `code-review`，涉及安全再加 `security-review`

---

### 场景 4：要部署上线

```
你: "测试通过了，准备部署"
    ↓
用什么？→ ship
```

| 技能 | 用途 | 调用方式 |
|------|------|----------|
| **ship** | 准备发布 | `/ship` |
| **canary** | 金丝雀发布 | `/canary` |
| **land-and-deploy** | 合并和部署 | `/land-and-deploy` |

**推荐**：`ship` → `land-and-deploy`

---

### 场景 5：需要跨模型审查计划

```
你: "这个方案靠谱吗？让另一个AI看看"
    ↓
用什么？→ grill-me-codex
```

| 技能 | 用途 | 调用方式 |
|------|------|----------|
| **grill-me-codex** | Claude + Codex 交叉审查 | `/grill-me-codex` |
| **codex-review** | 只让 Codex 审查 | `/codex-review` |

**推荐**：重要决策用 `grill-me-codex`

---

### 场景 6：需要规格驱动开发

```
你: "先定义清楚需求再写码"
    ↓
用什么？→ OpenSpec
```

| 技能 | 用途 | 调用方式 |
|------|------|----------|
| **OpenSpec** | 规格驱动开发 | `/opsx:explore` → `/opsx:propose` |
| **Trellis** | 持久化规格+任务 | `/trellis:brainstorm` |

**推荐**：单功能用 OpenSpec，长期项目用 Trellis

---

### 场景 7：前端界面设计

```
你: "帮我设计一个登录页面"
    ↓
用什么？→ frontend-design 或 design-html
```

| 技能 | 用途 | 调用方式 |
|------|------|----------|
| **frontend-design** | 前端设计 | `/frontend-design` |
| **design-html** | HTML 设计 | `/design-html` |
| **design-shotgun** | 快速设计迭代 | `/design-shotgun` |

**推荐**：`frontend-design`

---

### 场景 8：调试 Bug

```
你: "这个 bug 怎么都修不好"
    ↓
用什么？→ systematic-debugging
```

| 技能 | 用途 | 调用方式 |
|------|------|----------|
| **systematic-debugging** | 系统化调试 | `/systematic-debugging` |
| **investigate** | 调查问题 | `/investigate` |
| **retro** | 回顾总结 | `/retro` |

**推荐**：`systematic-debugging`

---

### 场景 9：需要测试

```
你: "帮我写测试"
    ↓
用什么？→ tdd-workflow 或 e2e-testing
```

| 技能               | 用途     | 调用方式            |
| ---------------- | ------ | --------------- |
| **tdd-workflow** | TDD 流程 | `/tdd-workflow` |
| **e2e-testing**  | 端到端测试  | `/e2e-testing`  |
| **qa**           | QA 测试  | `/qa`           |

**推荐**：新功能用 `tdd-workflow`，现有功能用 `e2e-testing`

---

### 场景 10：浏览器测试

```
你: "帮我测试这个网页"
    ↓
用什么？→ gstack (browse)
```

| 技能 | 用途 | 调用方式 |
|------|------|----------|
| **gstack/browse** | 浏览器测试 | `/browse` |
| **gstack/qa** | QA 测试 | `/qa` |
| **gstack/land-and-deploy** | 部署验证 | `/land-and-deploy` |

**推荐**：`/browse` 或 `/qa`

---

## ⚡ 快速选择表

| 你想做什么 | 用这个技能 | 备注 |
|-----------|-----------|------|
| 理清需求 | `brainstorming` | 头脑风暴 |
| 写计划 | `plan` 或 `autoplan` | 手动或自动 |
| 跨模型审查 | `grill-me-codex` | 重要决策 |
| 规格驱动 | `OpenSpec` | `/opsx:propose` |
| 持久化记忆 | `Trellis` | 长期项目 |
| 写代码 | 直接写 | 简单任务 |
| TDD | `tdd-workflow` | 测试驱动 |
| BDD | `bdd` | 行为驱动 |
| 代码审查 | `code-review` | 通用审查 |
| 安全审查 | `security-review` | 安全相关 |
| 前端设计 | `frontend-design` | UI 界面 |
| 调试 Bug | `systematic-debugging` | 系统化调试 |
| 写测试 | `e2e-testing` | 端到端 |
| 浏览器测试 | `gstack/browse` | 浏览器自动化 |
| 部署上线 | `ship` → `land-and-deploy` | 发布流程 |
| 文档生成 | `document-generate` | 生成文档 |

---

## 🚫 不要这样做

```
❌ 同时用 3+ 个规划技能
❌ 每次都用 grill-me-codex（太重了）
❌ 简单 bug 也用 systematic-debugging
❌ 所有项目都用 Trellis（小项目不需要）
❌ 每个 PR 都用 security-review（除非涉及安全）
```

---

## ✅ 推荐工作流

### 小任务（< 1小时）

```
直接写代码 → code-review → 提交
```

### 中等任务（1-4小时）

```
brainstorming → plan → tdd-workflow → code-review → 提交
```

### 大任务（> 4小时）

```
brainstorming → plan → grill-me-codex（可选）→ tdd-workflow → code-review → ship → 提交
```

### 重要决策

```
brainstorming → grill-me-codex → plan → 执行
```

---

## 🔧 技能详细说明

### gstack（Garry Tan's Stack）

**定位**：浏览器自动化 + QA 测试

**核心技能**：
- `/browse` — 浏览器测试
- `/qa` — QA 测试
- `/ship` — 准备发布
- `/land-and-deploy` — 合并部署

**适用场景**：需要浏览器交互的测试和部署

---

### superpowers（元技能）

**定位**：指导如何使用其他技能

**核心原则**：
- 有 1% 可能性用到技能，就必须调用
- 先检查技能，再行动

**适用场景**：任何对话开始时自动生效

---

### grill-me-codex（跨模型审查）

**定位**：Claude + Codex 交叉审查

**核心价值**：避免自己给自己打分

**适用场景**：重要决策、架构设计

---

### OpenSpec（规格驱动）

**定位**：在写代码前达成共识

**核心命令**：
- `/opsx:explore` — 探索想法
- `/opsx:propose` — 创建提案
- `/opsx:apply` — 实现任务

**适用场景**：单功能开发、需要规格文档

---

### Trellis（持久化记忆）

**定位**：跨会话保持上下文

**核心能力**：
- 规格持久化
- 任务状态管理
- 工作日志

**适用场景**：长期项目、团队协作

---

## 📝 总结

```
技能是工具，不是目的
用最少的技能完成任务
简单任务 → 简单技能
复杂任务 → 组合技能
```

**记住**：你不需要用所有技能，只需要用对的技能。

---

*最后更新：2026-07-13*
