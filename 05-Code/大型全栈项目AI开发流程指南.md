# 大型全栈项目 AI 开发流程指南

> 适用场景：大型全栈项目、企业级项目、任务周期 >2 周的项目
> 核心思想：先想清楚再动手，每一步有明确产出物和检查清单

---

## 总览

```
需求澄清 → 任务拆解 → 技术选型 → 架构设计 → 骨架搭建 → 并行开发 → 测试验证 → 部署上线
  │          │          │          │          │          │          │          │
/bdd      /prd-      /brain-    architect  手动        TDD       TDD       /dockerfile
          to-spec    storming             +Agent                +e2e      -optimizer
```
阶段专用（按流程顺序）

### 第一步：需求澄清

| Skill | 来源 | 用途 | 何时用 |
|-------|------|------|--------|
| `/bdd` | gstack | 梳理用户故事和验收标准 | 需求明确时 |
| `/brainstorming` | gstack | 发散思路 | 需求模糊时 |

### 第二步：任务拆解

| Skill | 来源 | 用途 | 何时用 |
|-------|------|------|--------|
| `/prd-to-spec` | 自建 | PRD 拆成可执行 Spec | 有需求文档后 |
| `/writing-plans` | Superpowers | 创建实现计划 | 需要计划时 |

### 第三步：技术选型

| Skill | 来源 | 用途 | 何时用 |
|-------|------|------|--------|
| `/brainstorming` | gstack | 方案对比 | 多个方案抉择时 |
| `/api-design` | ECC | REST API 设计规范 | 设计 API 时 |
| `/postgres-patterns` | ECC | PostgreSQL 设计模式 | 选 PostgreSQL 时 |

### 第四步：架构设计

| Skill | 来源 | 用途 | 何时用 |
|-------|------|------|--------|
| `/api-docs-generator` | ECC | 生成 API 文档 | 架构设计阶段 |
| `/system-design-generator` | ECC | 系统架构设计 | 从头设计系统 |
| `/design-consultation` | gstack | 设计系统（DESIGN.md） | 需要设计规范 |

### 第五步：骨架搭建

| Skill | 来源 | 用途 | 何时用 |
|-------|------|------|--------|
| `/frontend-design` | ECC | 创建前端界面 | 搭建前端骨架 |
| `/frontend-patterns` | ECC | 前端开发模式 | React/Next.js 开发 |
| `/backend-patterns` | ECC | 后端架构模式 | Node.js 后端 |
| `/python-patterns` | ECC | Pythonic 编码 | FastAPI 后端 |
| `/docker-patterns` | ECC | Docker 配置 | 容器化部署 |

### 第六步：并行开发

| Skill                          | 来源          | 用途          | 何时用    |
| ------------------------------ | ----------- | ----------- | ------ |
| `/test-driven-development`     | Superpowers | TDD 流程      | 写功能前   |
| `/subagent-driven-development` | Superpowers | 子Agent 执行计划 | 多任务并行  |
| `/dispatching-parallel-agents` | Superpowers | 并行任务分发      | 独立任务   |
| `/systematic-debugging`        | Superpowers | 系统化调试       | 遇到 bug |
| `/frontend-debug`              | ECC         | 前端调试        | 前端显示问题 |
| `/code-review`                 | gstack      | 代码审查        | 代码写完后  |
| `/simplify`                    | ECC         | 代码简化        | 重构优化时  |

### 第七步：测试验证

| Skill                        | 来源          | 用途         | 何时用       |
| ---------------------------- | ----------- | ---------- | --------- |
| `/test-driven-development`   | Superpowers | 写测试        | 开发时       |
| `/tdd-workflow`              | ECC         | TDD 工作流    | 新功能/bug修复 |
| `/e2e-testing`               | ECC         | E2E 测试     | 关键流程      |
| `/qa`                        | gstack      | QA 测试 + 修复 | 功能完成      |
| `/qa-only`                   | gstack      | QA 报告（不修复） | 只查不改      |
| `/bdd`                       | gstack      | 验收测试场景     | 验收阶段      |
| `/autonomous-test-debugging` | 自建          | 自主测试修复循环   | 测试失败自动修复  |

### 第八步：部署上线

| Skill | 来源 | 用途 | 何时用 |
|-------|------|------|--------|
| `/dockerfile-optimizer` | ECC | Dockerfile 优化 | Docker 部署 |
| `/vercel-deploy` | ECC | Vercel 部署 | 前端部署 |
| `/ci-cd-best-practices` | ECC | CI/CD 管道设计 | 配置 CI/CD |
| `/deployment-patterns` | ECC | 部署模式 | 部署策略 |
| `/ship` | gstack | 发布工作流 | 准备发布 |
| `/land-and-deploy` | gstack | 合并部署 | PR 合并后 |
| `/quick-package` | 自建 | 打压缩包 | 发布打包 |

---

## 第一步：需求澄清

### 做什么

把模糊需求变成清晰的**功能清单**。

```
输入：模糊需求（"做个CRM系统"）
输出：用户角色 + 功能清单 + 验收标准 + 边界定义
```

### 手动调用的 Skill

| Skill | 触发词 | 何时用 |
|-------|--------|--------|
| `/bdd` | 需求梳理、用户故事、验收标准 | 需求相对明确时 |
| `/brainstorming` | 探索可能性、不知道做什么 | 需求模糊时 |

**选择逻辑**：
- 需求模糊 → 先 `/brainstorming` 发散，再 `/bdd` 收敛
- 需求明确 → 直接 `/bdd`

### 注意事项

1. **必须书面化**：口头需求必须写成文档
2. **P0 不超过 5 个**：强制优先级，防止范围蔓延
3. **明确不做什么**：至少列 3 个 "不做"
4. **验收标准可度量**："快" 不是标准，"< 2 秒" 是

### 产出物

`.internal/01-requirements.md`

```markdown
# 需求文档

## 用户角色
| 角色 | 核心诉求 | 使用频率 |
|------|---------|---------|
| 销售 | 快速录入客户 | 每天 |

## 功能清单 (P0/P1/P2)
## 边界（不做什么）
## 验收标准（Given-When-Then）
```

### 检查清单

- [ ] 用户角色列表（至少 2 个）
- [ ] 功能清单分级（P0 不超过 5 个）
- [ ] 边界定义（至少 3 个 "不做"）
- [ ] P0 功能有 Given-When-Then 验收标准
- [ ] 文档已保存到 .internal/01-requirements.md

---

## 第二步：任务拆解

### 做什么

把功能清单拆成**可执行的小任务**。

```
输入：功能清单（"客户管理"）
输出：任务列表（"客户列表页 4h"、"新建客户弹窗 3h"）
```

### 手动调用的 Skill

| Skill          | 触发词                | 何时用    |
| -------------- | ------------------ | ------ |
| `/prd-to-spec` | PRD、需求拆解、spec、功能规格 | 第一步完成后 |

### 注意事项

1. **任务粒度 ≤ 4 小时**：太大无法估算，太小无意义
2. **前后端对齐**：先定义接口文档，再各自开发
3. **依赖关系明确**：标注"前端 X 依赖后端 Y"
4. **按 Sprint 划分**：每个 Sprint 有可演示的产出

### 产出物

`.internal/02-task-list.md`

```markdown
# 任务列表

## Sprint 1（第1-2周）- 骨架 + 认证

### 前端任务
- [ ] F-001: 项目初始化（Vite + React + TS）【2h】
- [ ] F-006: 登录页面【4h】

### 后端任务
- [ ] B-001: 项目初始化（FastAPI + SQLAlchemy）【2h】
- [ ] B-005: 登录接口（JWT）【4h】

### 依赖关系
F-006 依赖 B-005
```

### 检查清单

- [ ] 模块已拆分（至少 3 个）
- [ ] 每个任务 ≤ 4 小时
- [ ] 依赖关系已标注
- [ ] 前后端任务已对齐
- [ ] 文档已保存到 .internal/02-task-list.md

---

## 第三步：技术选型

### 做什么

确定技术栈，写入 TECH_STACK.md。

```
输入：需求文档 + 任务列表
输出：TECH_STACK.md（前端框架、后端框架、数据库等）
```

### 手动调用的 Skill

| Skill | 触发词 | 何时用 |
|-------|--------|--------|
| `/brainstorming` | 技术选型、框架选择、方案对比 | 多方案抉择时 |

### 产品形态 → 技术栈映射

| 产品形态 | 前端框架 | UI 库 | 构建工具 |
|---------|---------|-------|---------|
| 后台管理系统 | React/Vue | Ant Design/Element Plus | Vite |
| PC 网站（内容型） | Next.js/Nuxt | Tailwind + shadcn/ui | Next/Vite |
| 移动 H5 | React/Vue | Vant/NutUI | Vite |
| 桌面应用 | Electron + React/Vue | Ant Design/Element Plus | Vite |

### 注意事项

1. **选成熟方案**：不追求新技术，避免踩坑
2. **一个项目只用一个 UI 库**：不混用
3. **TypeScript 强制**：新项目不用 JavaScript
4. **数据库选型**：常规业务 → MySQL，复杂查询 → PostgreSQL

### 产出物

`TECH_STACK.md`

```markdown
# 技术选型文档

### 前端
| 项目 | 选型 | 版本 | 选择理由 |
|------|------|------|---------|
| 框架 | React | 18.x | 生态成熟 |
| UI 库 | Ant Design | 5.x | 组件丰富 |

### 后端
| 项目 | 选型 | 版本 | 选择理由 |
|------|------|------|---------|
| 框架 | FastAPI | 0.115.x | 异步，性能好 |
| 数据库 | PostgreSQL | 16 | 功能强大 |

### AI 开发约束
1. 不得安装未列出的 UI 框架
2. 新增依赖前必须更新本文档
```

### 检查清单

- [ ] 前端框架已确定（含版本号）
- [ ] 后端框架已确定（含版本号）
- [ ] 数据库已确定
- [ ] TECH_STACK.md 已保存

---

## 第四步：架构设计

### 做什么

设计系统架构，明确**模块边界**、**API 接口**、**数据库结构**。

```
输入：需求文档 + TECH_STACK.md
输出：架构文档 + API 设计 + 数据库 Schema
```

### 手动调用的 Skill

| Skill                      | 触发词         | 何时用         |
| -------------------------- | ----------- | ----------- |
| `/api-docs-generator`      | API 文档、接口文档 | 需要生成 API 文档 |
| `/system-design-generator` | 系统设计、架构设计   | 需要设计系统架构    |

### 架构分层

```
前端：展示层 → 业务层 → 状态层 → 数据层
后端：路由层 → 服务层 → 数据层 → 模型层
```

### 注意事项

1. **统一响应格式**：所有接口返回 `{success, data, error}`
2. **数据库命名**：表名 snake_case 复数，字段名 snake_case
3. **必备字段**：id, created_at, updated_at, deleted_at
4. **金额用 DECIMAL**：不用 FLOAT
5. **密码 bcrypt 加密**：不存明文

### 产出物

| 文件 | 位置 |
|------|------|
| 架构文档 | `.internal/04-architecture.md` |
| API 设计 | `.internal/04-api-design.md` |
| 数据库 Schema | `.internal/04-database-schema.sql` |

### 统一响应格式

```json
// 成功
{ "success": true, "data": {}, "error": null }

// 失败
{ "success": false, "data": null, "error": { "code": "USER_NOT_FOUND", "message": "用户不存在" } }
```

### 检查清单

- [ ] 有系统架构图
- [ ] 模块划分清晰
- [ ] API 接口列表完整
- [ ] 数据库表结构已定义
- [ ] 所有文档已保存到 .internal/

---

## 第五步：骨架搭建

### 做什么

搭建前后端项目骨架，确保**能跑通基础流程**。

```
输入：TECH_STACK.md + 架构文档
输出：可运行的前后端骨架项目
```

### 手动调用的 Skill

| Skill | 触发词 | 何时用 |
|-------|--------|--------|
| `/frontend-design` | 前端设计、创建页面 | 需要创建前端界面 |
| `/dockerfile-optimizer` | Docker、容器化 | 需要配置 Docker |

### 四条验收线

| 验收线 | 说明 | 验证方式 |
|--------|------|---------|
| 启动线 | 项目能启动 | `npm run dev` |
| 接口线 | 有健康检查 | `curl /health` |
| 业务线 | 分层正确 | 代码审查 |
| 运维线 | 日志正常 | 检查日志 |

### 前端目录结构

```
src/
├── app/           # 应用入口
│   ├── App.tsx
│   └── routes.tsx
├── features/      # 业务模块
│   └── auth/
├── shared/        # 共享资源
│   ├── components/
│   └── styles/tokens.css
└── assets/        # 静态资源
```

### 后端目录结构

```
server/
├── app/
│   ├── main.py         # 入口
│   ├── api/v1/         # 路由层
│   ├── services/       # 服务层
│   ├── repositories/   # 数据层
│   ├── models/         # 模型层
│   └── schemas/        # Schema 层
├── tests/
└── .env
```

### 设计 Token（前端必须）

```css
:root {
  --color-primary: oklch(60% 0.2 250);
  --text-base: clamp(0.9rem, 0.85rem + 0.2vw, 1rem);
  --space-4: 1rem;
  --radius-md: 8px;
  --shadow-md: 0 4px 6px oklch(0% 0 0 / 0.07);
}
```

### 检查清单

- [ ] 前端 npm run dev 能启动
- [ ] 后端能启动，/health 正常
- [ ] 目录结构符合规范
- [ ] 设计 Token 已定义
- [ ] .gitignore 已配置
- [ ] 无 TypeScript / 语法错误

---

## 第六步：并行开发

### 做什么

前后端并行开发功能模块。

```
输入：可运行的骨架 + 任务列表
输出：功能模块代码
```

### 手动调用的 Skill

| Skill                      | 触发词         | 何时用          |
| -------------------------- | ----------- | ------------ |
| `/test-driven-development` | TDD、测试驱动    | 写功能前先写测试     |
| `/code-audit`              | 代码审计、检查代码质量 | 代码写完后        |
| `/systematic-debugging`    | 调试、排查问题     | 遇到 bug 时     |
| `/context-compact`         | 压缩上下文       | 工具调用 > 40 次时 |

### 单个模块开发流程

```
1. 写 Spec（任务描述 + 输入输出 + 验收标准）
    ↓
2. 写测试（TDD，/test-driven-development）
    ↓
3. 写实现代码
    ↓
4. 运行测试验证
    ↓
5. 代码审查（/code-audit）
    ↓
6. 提交代码
```

### TDD 工作流

| 阶段 | 说明 |
|------|------|
| RED | 先写测试，测试应该失败 |
| GREEN | 写最小实现，测试应该通过 |
| REFACTOR | 重构优化，测试仍然通过 |

### 并行模式

```
主会话（Boss）
    ├── 后端 Agent（独立 session）→ 开发 API
    ├── 前端 Agent（独立 session）→ 开发页面
    ├── 测试 Agent（后台）→ 编写测试
    └── 审查 Agent（后台）→ 代码审查
```

### 代码质量要求

- 函数 ≤ 50 行
- 文件 ≤ 800 行
- 嵌套 ≤ 4 层
- 测试覆盖率 ≥ 80%
- 无 console.log

### 前端检查

- 组件单一职责
- TypeScript 严格模式（不用 any）
- 样式用 Token，不硬编码颜色
- 路由层不写业务逻辑

### 后端检查

- 分层清晰：路由 → 服务 → 数据
- 路由层只做请求解析，不写业务
- 统一响应格式
- 全局异常捕获

### 检查清单（每个模块）

- [ ] 有 Spec（功能描述、输入输出、验收标准）
- [ ] 有测试用例
- [ ] 测试全部通过
- [ ] 代码审查通过
- [ ] git commit 消息规范

---

## 第七步：测试验证

### 做什么

确保代码质量，覆盖率达到 80%+。

```
输入：功能代码
输出：测试报告、覆盖率报告
```

### 手动调用的 Skill

| Skill | 触发词 | 何时用 |
|-------|--------|--------|
| `/test-driven-development` | TDD、测试驱动、写测试 | 写测试时 |
| `/bdd` | 验收标准、场景测试 | 写验收测试时 |
| `/systematic-debugging` | 调试、排查问题 | 测试失败时 |

### 测试金字塔

```
     /\
    /  \       E2E 测试（少量）- 关键用户流程
   /----\
  /      \     集成测试（适量）- API 端点、数据库
 /--------\
/          \    单元测试（大量）- 函数、工具、组件
```

### 测试覆盖率目标

| 指标 | 目标 |
|------|------|
| 行覆盖率 | ≥ 80% |
| 分支覆盖率 | ≥ 70% |
| 函数覆盖率 | ≥ 90% |

### AAA 模式

```typescript
test('计算相似度正确', () => {
  // Arrange - 准备
  const v1 = [1, 0, 0], v2 = [0, 1, 0]

  // Act - 执行
  const result = calculate(v1, v2)

  // Assert - 断言
  expect(result).toBe(0)
})
```

### 常见坑

- 测试依赖外部服务 → 用 Mock
- 测试之间有顺序 → 每个测试独立
- 测试数据残留 → 每个测试清理

### 检查清单

- [ ] 单元测试覆盖率 ≥ 80%
- [ ] 关键接口有集成测试
- [ ] 关键流程有 E2E 测试
- [ ] 测试命名描述行为
- [ ] 所有测试通过

---

## 第八步：部署上线

### 做什么

配置部署，上线运行。

```
输入：通过测试的代码
输出：可访问的线上服务
```

### 手动调用的 Skill

| Skill | 触发词 | 何时用 |
|-------|--------|--------|
| `/dockerfile-optimizer` | Docker、容器化、Dockerfile | 需要配置 Docker |
| `/vercel-deploy` | Vercel、部署前端 | 部署到 Vercel |

### Docker 配置要点

- 多阶段构建，减小镜像体积
- 基础镜像用 Alpine 或 slim 版本
- 环境变量用 .env 文件
- 配置 HEALTHCHECK

### Docker Compose 示例

```yaml
services:
  frontend:
    build: ./client
    ports: ["3000:80"]
  backend:
    build: ./server
    ports: ["8000:8000"]
    depends_on: [db]
  db:
    image: postgres:16
    volumes: [postgres_data:/var/lib/postgresql/data]
```

### 环境变量

| 环境 | 配置文件 |
|------|---------|
| 开发 | .env.development |
| 测试 | .env.test |
| 生产 | .env.production |

### 上线检查

- 生产环境变量配置正确
- 数据库迁移已执行
- HTTPS 证书已配置
- 数据库备份策略就绪
- 应用监控已配置

### 检查清单

- [ ] Dockerfile 已创建（前后端）
- [ ] docker-compose.yml 已创建
- [ ] .env.example 已创建
- [ ] CI/CD 已配置
- [ ] 监控告警已配置

---

## 关键配置文件总览

| 文件 | 用途 | 阶段 |
|------|------|------|
| `.internal/01-requirements.md` | 需求文档 | 第一步 |
| `.internal/02-task-list.md` | 任务列表 | 第二步 |
| `TECH_STACK.md` | 技术选型 | 第三步 |
| `.internal/04-architecture.md` | 架构设计 | 第四步 |
| `.internal/04-api-design.md` | API 设计 | 第四步 |
| `.internal/04-database-schema.sql` | 数据库 Schema | 第四步 |
| 前端/后端代码 | 项目代码 | 第五、六步 |
| `tests/` | 测试代码 | 第七步 |
| `Dockerfile` | 容器配置 | 第八步 |

---

## 贯穿全流程的工具

| 工具 | 用途 | 阶段 |
|------|------|------|
| `/context-compact` | 上下文压缩 | 贯穿全程 |
| `/context-save` | 保存进度 | 贯穿全程 |
| `/context-restore` | 恢复进度 | 贯穿全程 |
| `/autocommit` | 自动提交 | 贯穿全程 |
| `/rules-audit` | 规则审查 | 定期 |
| Agent: `code-reviewer` | 代码审查（后台） | 开发阶段 |
| Agent: `security-reviewer` | 安全审查（后台） | 开发阶段 |

---

## 企业级项目额外 Skill

| Skill                   | 用途            |
| ----------------------- | ------------- |
| `/ci-cd-best-practices` | CI/CD 管道设计    |
| `/security-review`      | 安全检查清单        |
| `/codebase-migrate`     | 大规模代码迁移       |
| `/api-design`           | REST API 设计规范 |
| `/postgres-patterns`    | PostgreSQL 优化 |
| `/database-migrations`  | 数据库迁移策略       |
| `/ship`                 | 发布工作流         |
| `/retro`                | 每周回顾          |
| `/document-generate`    | 生成文档          |
| `/dogfood`              | 探索性 QA 测试     |
| `/benchmark`            | 性能基准测试        |
| `/canary`               | 部署后监控         |
| `/cso`                  | 安全审计          |

---

## 常见陷阱速查表

| 阶段 | 陷阱 | 避免方式 |
|------|------|---------|
| 需求 | 需求模糊就开始写代码 | 必须有书面需求文档 |
| 任务 | 把"客户管理"当成一个任务 | 拆到 ≤ 4h |
| 选型 | 追求新技术导致踩坑 | 选成熟方案 |
| 架构 | 没有统一响应格式 | 第一步就定义好 |
| 骨架 | 跳过骨架直接写业务 | 先跑通基础流程 |
| 开发 | 前后端字段名不一致 | 先定义接口文档 |
| 开发 | N+1 查询 | 用 JOIN 或预加载 |
| 开发 | useEffect 依赖漏填 | ESLint 规则 |
| 测试 | 测试覆盖实现细节 | 测试行为，不测试实现 |
| 部署 | 生产环境配置错误 | 使用环境变量，有检查清单 |

---

## 快速启动

```bash
# 开始一个新项目
1. 创建项目目录
2. 配置 .gitignore
3. mkdir .internal
4. /bdd 开始需求澄清
5. 按照八步流程推进
```

---

*最后更新：2026-06-17*
