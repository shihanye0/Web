# AI 编程 Skill 实用分类手册

> 基于八步开发流程，从 367 个 Skill 中精选实际会用到的
> 分类：每日必用 / 阶段专用 / 按需查阅 / 不必关注

---

## 一、每日必用（每个阶段都会用）

| Skill | 来源 | 用途 | 触发词 |
|-------|------|------|--------|
| `/context-compact` | ECC | 上下文压缩，防止溢出 | 工具调用 >40次 |
| `/context-save` | gstack | 保存当前进度 | 保存进度 |
| `/context-restore` | gstack | 恢复之前进度 | 继续、上次 |
| `/autocommit` | 自建 | 自动 Git 提交 | 工作完成 |
| `/code-audit` | 自建 | 代码质量审计 | 检查代码质量 |

---

## 二、阶段专用（按流程顺序）

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

| Skill | 来源 | 用途 | 何时用 |
|-------|------|------|--------|
| `/test-driven-development` | Superpowers | TDD 流程 | 写功能前 |
| `/subagent-driven-development` | Superpowers | 子Agent 执行计划 | 多任务并行 |
| `/dispatching-parallel-agents` | Superpowers | 并行任务分发 | 独立任务 |
| `/systematic-debugging` | Superpowers | 系统化调试 | 遇到 bug |
| `/frontend-debug` | ECC | 前端调试 | 前端显示问题 |
| `/code-review` | gstack | 代码审查 | 代码写完后 |
| `/simplify` | ECC | 代码简化 | 重构优化时 |

### 第七步：测试验证

| Skill | 来源 | 用途 | 何时用 |
|-------|------|------|--------|
| `/test-driven-development` | Superpowers | 写测试 | 开发时 |
| `/tdd-workflow` | ECC | TDD 工作流 | 新功能/bug修复 |
| `/e2e-testing` | ECC | E2E 测试 | 关键流程 |
| `/qa` | gstack | QA 测试 + 修复 | 功能完成 |
| `/qa-only` | gstack | QA 报告（不修复） | 只查不改 |
| `/bdd` | gstack | 验收测试场景 | 验收阶段 |
| `/autonomous-test-debugging` | 自建 | 自主测试修复循环 | 测试失败自动修复 |

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

## 三、按需查阅

### 代码审查类

| Skill | 用途 |
|-------|------|
| `/security-review` | 安全检查清单 |
| `/security-scan` | 扫描配置安全漏洞 |
| `/cso` | 全面安全审计 |
| `/requesting-code-review` | 请求代码审查 |
| `/receiving-code-review` | 处理审查反馈 |

### 文档类

| Skill | 用途 |
|-------|------|
| `/document-generate` | 生成缺失文档 |
| `/document-release` | 发布后更新文档 |
| `/changelog-generator` | 从 git commit 生成 changelog |
| `/make-pdf` | Markdown 转 PDF |

### Git/GitHub 类

| Skill | 用途 |
|-------|------|
| `/gh-fix-ci` | 修复 CI 失败 |
| `/gh-address-comments` | 处理 PR 评论 |
| `/github-ops` | GitHub 操作管理 |
| `/using-git-worktrees` | Git worktree 隔离 |

### 企业级/运维类

| Skill | 用途 |
|-------|------|
| `/cso` | 安全审计 |
| `/benchmark` | 性能基准测试 |
| `/canary` | 部署后监控 |
| `/setup-deploy` | 配置部署设置 |
| `/sentry-triage` | Sentry 问题诊断 |
| `/datadog-cli` | Datadog 运维 |
| `/retro` | 工程回顾 |

### 项目管理类

| Skill | 用途 |
|-------|------|
| `/office-hours` | YC 式产品咨询 |
| `/plan-ceo-review` | CEO 视角审查 |
| `/plan-eng-review` | 工程经理审查 |
| `/plan-design-review` | 设计师审查 |
| `/project-deep-dive` | 项目深度分析 |
| `/jira-integration` | Jira 工单管理 |

### 数据/图表类

| Skill | 用途 |
|-------|------|
| `/chart-visualization` | 数据可视化 |
| `/data-analysis` | Excel/CSV 分析 |
| `/xlsx` | 电子表格操作 |
| `/dashboard-builder` | 监控仪表盘 |

### 前端设计类

| Skill | 用途 |
|-------|------|
| `/design-shotgun` | 多方案设计探索 |
| `/design-review` | 视觉 QA |
| `/web-design-guidelines` | Web 设计合规审查 |
| `/design-html` | 生成 HTML 页面 |

### 论文写作类

| Skill | 用途 |
|-------|------|
| `/thesis-rewrite` | 论文改写 |
| `/humanizer-cn` | 中文去 AI 化 |
| `/de-ai-fy` | 通用去 AI 化 |
| `/chinese-thesis-workbench` | 毕业论文全流程 |
| `/reference-count` | 参考文献数量控制 |

### 数据库类

| Skill | 用途 |
|-------|------|
| `/database-migrations` | 数据库迁移 |
| `/postgres-patterns` | PostgreSQL 优化 |
| `/sql-query-optimizer` | SQL 优化 |

---

## 四、不必关注（场景不匹配）

### 语言不匹配

| 语言 | 相关 Skill（无需关注） |
|------|----------------------|
| Go | golang-patterns, golang-testing, go-build, go-review, go-test |
| Java | java-coding-standards, springboot-patterns, jpa-patterns, springboot-tdd |
| Kotlin | kotlin-patterns, kotlin-testing, kotlin-build, kotlin-review |
| Rust | rust-patterns, rust-testing, rust-build, rust-review |
| Swift/iOS | swiftui-patterns, ios-qa, ios-fix, liquid-glass-design |
| C++ | cpp-coding-standards, cpp-testing, opencv-cpp |
| C# | csharp-testing, dotnet-patterns |
| Dart/Flutter | dart-flutter-patterns, flutter-review, flutter-build |
| PHP | laravel-patterns, laravel-security, laravel-tdd |
| Perl | perl-patterns, perl-security, perl-testing |

### 平台不匹配

| Skill | 原因 |
|-------|------|
| android-clean-architecture | Android 开发 |
| compose-multiplatform-patterns | KMP 跨平台 |
| foundation-models-on-device | Apple iOS 26+ |
| vue3-spa-multi-role-isolation | Vue 3（你主要用 React） |

### 领域不匹配

| Skill | 原因 |
|-------|------|
| defi-amm-security | 区块链/Solidity |
| evm-token-decimals | 以太坊 |
| healthcare-phi-compliance | 医疗合规 |
| hipaa-compliance | 美国医疗法规 |
| lead-intelligence | 销售线索 |
| carrier-relationship-management | 物流运输 |
| customs-trade-compliance | 海关贸易 |
| energy-procurement | 能源采购 |
| inventory-demand-planning | 库存管理 |
| logistics-exception-management | 物流异常 |
| production-scheduling | 生产排程 |
| quality-nonconformance | 质量控制 |
| returns-reverse-logistics | 逆向物流 |

### 内容创作类（偶尔用）

| Skill | 用途 | 何时可能用到 |
|-------|------|------------|
| `/ppt-studio` | PPT 制作 | 答辩/汇报 |
| `/article-writing` | 文章写作 | 博客/文档 |
| `/podcast-generation` | 播客 | 内容创作 |
| `/short-video-script` | 短视频脚本 | 社交媒体 |
| `/khazix-writer` | 公众号长文 | 公众号 |

---

## 五、快速查找索引

### 按问题类型找 Skill

| 我想做什么 | 用什么 Skill |
|-----------|-------------|
| 梳理需求 | `/bdd` |
| 探索可能性 | `/brainstorming` |
| 拆解 PRD | `/prd-to-spec` |
| 创建计划 | `/writing-plans` |
| 写测试 | `/test-driven-development` |
| 代码审查 | `/code-audit` `/code-review` |
| 调试 bug | `/systematic-debugging` `/investigate` |
| 前端调试 | `/frontend-debug` |
| 简化代码 | `/simplify` |
| 安全检查 | `/security-review` `/cso` |
| 部署上线 | `/dockerfile-optimizer` `/ship` |
| 上下文满了 | `/context-compact` |
| 保存/恢复进度 | `/context-save` `/context-restore` |
| 自动提交 | `/autocommit` |
| 打压缩包 | `/quick-package` |
| 更新文档 | `/document-generate` `/document-release` |
| 生成 API 文档 | `/api-docs-generator` |
| 设计数据库 | `/postgres-patterns` |
| 性能测试 | `/benchmark` |
| 部署监控 | `/canary` |
| 规则审查 | `/rules-audit` |
| 配置同步 | 运行 `~/.claude/sync-all.sh` |

---

## 六、统计

| 分类 | 数量 |
|------|------|
| 每日必用 | 5 |
| 阶段专用 | 38 |
| 按需查阅 | 42 |
| 不必关注（语言/平台/领域不匹配） | ~277 |
| 偶尔可用（内容创作等） | 5 |

**实际常用 ~85 个，占总量 367 的 23%。**

---

*最后更新：2026-06-17*
