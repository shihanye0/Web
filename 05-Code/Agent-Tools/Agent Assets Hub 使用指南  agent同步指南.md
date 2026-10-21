---
status: evergreen
tags:
  - agent-hub
  - ai-tools
  - skills
  - mcp
  - 跨agent
  - 配置同步
  - 能力投影
  - windows11
updated: 2026-10-21
---
# Agent Assets Hub 使用指南（Windows 11 本地版）

> 跨 Agent（Codex / Claude Code / Antigravity / WorkBuddy AI / WorkBuddy 国内版 / DSH / Qoder）共享 Skills / 规则契约 / 习惯 / MCP 的统一真源与同步管理  
> 更新时间：2026-10-21（第三轮：能力差异化投影定案；更正 DSH/Qoder 规则面；DSH MCP 漂移修复；补 WorkBuddy CODEBUDDY.md）  
> 本机控制面：`C:\Users\Lenovo\.agent-config\`  
> 共享技能库真源：`C:\Users\Lenovo\.skillshub\`（615 个含 SKILL.md 的技能）

---

## 一、解决什么问题

在 Windows 11 环境下同时使用 **Codex**、**Claude Code** 与 **Antigravity（反重力）** 时：

- **技能碎片化**：Skill 各写一份或全量暴力拷贝，导致各端版本漂移、更新不同步。
- **规则冲突与上下文膨胀**：`CLAUDE.md` 堆砌上千行历史踩坑日记，浪费上万 Token 并引发“注意力稀释”与规则互斥。
- **MCP 重复配置**：各端配置文件格式不同（TOML vs JSON），手动维护极易遗漏。
- **链接不兼容**：Windows 原生不支持或易失效 POSIX Symlink，需要一套原生稳定的联接机制。

**本体系原则：资产集中维护，按端能力差异化投影；契约统一共享，隐私与原生配置本地隔离。**

各端能力与定位不同，**不追求逐端配置一致**——核心集必齐，扩展集按端定位（见第三章「能力差异化投影」）。基地的价值是让各端按需取用、互相借鉴，而不是把差异拉平。

---

## 二、架构与目录结构

```text
C:\Users\Lenovo\
├── .agent-config/                 # Agent 配置控制面（非敏感中枢）
│   ├── rules/                     # 跨 Agent 共享微内核 (L0 契约，7 个模块)
│   │   ├── preferences.md              #   称呼 Boss、中文优先、Windows 11、E盘 Conda
│   │   ├── document-authorship.md      #   正式产物作者视角，避免旁观者叙事
│   │   ├── evidence-debugging.md       #   FACT/INFERENCE 证据链、根因修复、杜绝假数据
│   │   ├── coding-verification.md      #   Karpathy 准则、py_compile/tsc 物理门禁
│   │   ├── git-safety.md               #   禁止 git add .、不自动提交、零凭据泄露
│   │   ├── powershell-version.md       #   只允许 PowerShell 7，禁用 5.1
│   │   └── presentation-layout-contracts.md  # 演示文稿/视觉排版先定内容区契约
│   ├── scripts/                   # PowerShell 7 原生运维脚本
│   │   ├── Get-AgentPlatformStatus.ps1  # 状态总览（对标 hub-status）
│   │   ├── Sync-AgentSkill.ps1          # 安全挂接/解挂 Skill（对标 sync-profile，支持 -WhatIf）
│   │   ├── Test-AgentPlatform.ps1       # 全端基线漂移审计（对标 hub-update 校验）
│   │   ├── Test-ProjectionPolicy.ps1    # 按能力差异化策略校验七端（技能分层/MCP 能力组/规则面）
│   │   └── Repair-QoderMcp.ps1          # Qoder 升级后重建 15 个 MCP（自动探测版本哈希目录）
│   ├── backups/                   # 变更前备份（孤儿链接清单等）
│   ├── references/                # 离线沉淀知识库（按需查阅，不占全局 System Prompt）
│   │   ├── platform-matrix.md     #   各端投影与支持能力矩阵
│   │   └── git-troubleshooting.md #   Git 9418 协议错误、凭证配置与历史大文件清理手册
│   └── registry.json              # 平台资产与 MCP 服务清单 + projection 差异化投影策略
│
└── .skillshub/                    # 共享技能库唯一真源（615 个含 SKILL.md 的技能，目录总数 616）
    ├── agent-platform-sync/       #   跨 Agent 同步专用引导技能
    ├── archify/                   #   架构归档技能
    ├── chinese-thesis-workbench/  #   学术论文写作与去 AI 化工作台
    └── ...                        #   其余 600+ 共享技能
```

---

## 三、各端能力投影矩阵（Windows 11 实测）

| 端 (Agent) | 共享 Skills 机制 | MCP 维护机制 | 全局规则文件 | 插件 (Plugins) |
|---|---|---|---|---|
| **Codex** | **NTFS Junction**（按需单 Skill 挂接至 `~/.agents/skills`，实测 13 个） | 原生 `~/.codex/config.toml`（16 个服务） | `~/.codex/AGENTS.md`（吸收共享微内核） | TOML 声明，本地插件缓存 |
| **Claude Code** | **NTFS Junction**（11 个挂接）+ **89 个本地目录**（其中 30 个是没有 `SKILL.md` 的容器目录，如 `research/` 下挂 arxiv、polymarket 等子技能，不会作为单技能加载） | 原生 `~/.claude/.mcp.json`（19 个服务） | `~/.claude/CLAUDE.md`（精炼薄壳，吸收共享微内核） | `settings.json` 启用声明 |
| **Antigravity** | **已确认 2.0 读新根 `~/.gemini/config/skills`**（判据见第十二章）：现为 **11 个 Junction + 1 个本地 `codex-continuity`**，与 WorkBuddy 精选集对齐。旧根 `~/.gemini/antigravity/skills` 的 616 个整目录 Junction 已失效 | 原生 `~/.gemini/config/mcp_config.json`（15 个服务） | `~/.gemini/GEMINI.md`（吸收共享微内核） | 不适用（原生 MCP/Skills 架构） |
| **WorkBuddy AI**（`WorkBuddyAI.exe` 5.8.4） | 11 个 Junction 至 `~/.workbuddy-ai/skills` | `~/.workbuddy-ai/mcp.json`（15 个） | `~/.workbuddy-ai/AGENTS.md` + `user-<uid>-personal/MEMORY.md` | `settings.json` 的 `enabledPlugins`（16 个，含 8 个市场插件） |
| **WorkBuddy 国内版**（`WorkBuddy.exe` 37.10.3-42） | 11 个 Junction 至 `~/.workbuddy/skills`（与 AI 端同一精选集） | `~/.workbuddy/mcp.json`（15 个） | `~/.workbuddy/AGENTS.md` + `user-<uid>-personal/MEMORY.md` | 仅 8 个内置插件；AI 端那 8 个市场插件未安装（构建版本不同，必须走市场装） |
| **DSH**（DeepSeek Harness Desktop） | 30 个 Junction 至 `~/.dsh/skills` | `~/.dsh/storages/mcp_connector.json`（connector-store 格式，**9/15** 覆盖） | **`~/.dsh/AGENTS.md`**（原生 AGENTS.md，**2026-10-21 更正**） | 15 个 profile bundle |
| **Qoder**（CodeGeeX 内核） | **387 个 Junction** 至 `E:\Program Files\.qoder\skills`（`~/.qoder` 是符号链接） | 扩展目录内 `user_mcp_config.json`（15 个，**版本锁定路径**） | **`~/.qoder/AGENTS.md`**（原生，**2026-10-21 更正**） | `~/.qoder/settings.json`（hooks + enabledPlugins） |

> 逐端完整字段（路径、格式、验证命令、已知缺陷）见 `C:\Users\Lenovo\.agent-config\references\platform-matrix.md`。

> **关键机制说明**：在 Windows 11 下，放弃不稳定的 POSIX Symlink 和盲目拷贝，统一采用 **NTFS Junction（目录联接）**。既保证了零文件复制冗余、修改真源全局实时生效，又保证了删除联接点绝不伤及源文件。选择该机制与官方建议一致：symlink 在 Windows 需管理员或开发者模式，且 Git 需开启 `core.symlinks` 才不会被当成普通文本文件检出。

### 能力差异化投影（2026-10-21 定案）

> 机器可读策略在 `registry.json` 的 `projection` 键；只读校验脚本 `scripts\Test-ProjectionPolicy.ps1`。

**共享的是资产与契约，不是某一端的配置文件。** 七端能力与定位不同，强制一致只会制造无用上下文。

| 层 | 内容 | 投影端 |
|---|---|---|
| **core（11）** | agent-platform-sync、agent-browser、cdp-host-browser-automation、computer-use-agents、anatomy、cad、dfm、engineering-drawing、urdf、reverse-engineer-anything、chinese-thesis-workbench | 七端必齐 |
| **extended（19）** | archify、brainstorming、context-window-management、deep-research、dispatching-parallel-agents、docx、executing-plans、humanizer-cn、mcp-builder、multi-agent-team、pptx、research、subagent-driven-development、systematic-debugging、thesis-deai、token-budget-advisor、writing-plans、writing-skills、xlsx | **仅 DSH** |
| **端专属** | Codex 另挂 archify、ppt-master；Claude 自有 59 技能 + 30 容器目录；反重力本地 codex-continuity | 各自保留 |
| **全库** | Qoder 387 个 Junction（核心 11/11 齐备） | 全量检索端 |

**取舍理由**：DSH 有 subagent 委派、计划/执行、上下文与 token 预算工具，计划-编排-文档类技能在这里有真实落点；Codex 的 archify/ppt-master 补它的架构图与演示交付。MCP 同步按**能力组**（search-fetch / browser / code-repo / memory / visual / automation / specialist）校验：DSH 按覆盖率（9/15 达标即可），其余六端要求能力组全齐。

---

## 四、共享什么 / 不共享什么（安全底线）

### 共享（核心内容资产）
- **Skills 技能库**：以 `SKILL.md` 标准打包的所有功能技能（脚本、Prompt、参考资料）。
- **微内核规则契约**：称呼、沟通风格、Windows 11 环境、调试证据分级、编译运行门禁。
- **通用 MCP 服务定义**：服务名、命令（如 `uvx` / `node`）、URL、参数名（10 大通用服务）。
- **离线知识库**：历史踩坑教程、平台矩阵、故障排查手册。

### 不共享（各端本地独立）
- **API Key / 令牌 / 凭据**：严禁写入任何共享规则或清单，各自在本地环境变量或专属配置中注入。
- **客户端配置文件原生格式**：Codex 维持 `.toml`，Claude / Antigravity 维持 `.json`，由清单校验一致性，不搞跨格式乱拷。
- **插件二进制缓存与临时会话**：避免各客户端缓存机制互斥导致崩溃。

---

## 五、日常高频管理指令 (PowerShell 7)

日常运维已全部封装为 PowerShell 7 原生脚本，开箱即用：

### 1. 查看全端投影与状态（最常用，对标 `hub-status`）
```powershell
& 'C:\Users\Lenovo\.agent-config\scripts\Get-AgentPlatformStatus.ps1'
```
*一键扫描 Codex、Claude、Antigravity 的规则状态、MCP 服务总数、挂接的 Skills 清单及断链检测。*

### 2. 将共享技能挂接给 Codex 或 Claude（对标 `sync-profile`）
```powershell
# 挂接前安全预览（-WhatIf 预演）
& 'C:\Users\Lenovo\.agent-config\scripts\Sync-AgentSkill.ps1' -Agent codex -SkillName archify -WhatIf

# 实际挂接（秒级创建 NTFS Junction）
& 'C:\Users\Lenovo\.agent-config\scripts\Sync-AgentSkill.ps1' -Agent codex -SkillName archify
& 'C:\Users\Lenovo\.agent-config\scripts\Sync-AgentSkill.ps1' -Agent claudeCode -SkillName archify

# 安全解挂（仅删除联接点，绝对不损坏 .skillshub 中的源文件）
& 'C:\Users\Lenovo\.agent-config\scripts\Sync-AgentSkill.ps1' -Agent codex -SkillName archify -Action Unlink
```
*(注：`-Agent` 现支持 `codex` / `claudeCode` / `antigravity` / `dsh` / `workbuddy` / `workbuddyCn` / `qoder` 七端，全部从 `registry.json` 的 `sharedSkills.targets` 取目标目录。Antigravity 的**旧根** `~/.gemini/antigravity/skills` 仍是整目录直通 `.skillshub`，但 2.0 实际读的是新根 `~/.gemini/config/skills`（只有 7 个 Junction），需要按需逐个挂接。)*

### 3. 运行全平台基线审计
```powershell
& 'C:\Users\Lenovo\.agent-config\scripts\Test-AgentPlatform.ps1'
```
*校验各端 rules 是否健在、15 个通用 MCP 是否全部对齐、引导技能是否正常。*

### 4. 一键看七端状态
```powershell
& 'C:\Users\Lenovo\.agent-config\scripts\Get-AgentPlatformStatus.ps1'
```
*输出 codex / claudeCode / antigravity / dsh / workbuddy / workbuddyCn / qoder 七端的规则、MCP 服务数、技能挂接数与断链清单。*

### 5. Qoder 升级后重建 MCP
```powershell
& 'C:\Users\Lenovo\.agent-config\scripts\Repair-QoderMcp.ps1' -WhatIf   # 预演
& 'C:\Users\Lenovo\.agent-config\scripts\Repair-QoderMcp.ps1'           # 实跑
```
*Qoder 的 MCP 存在扩展版本目录里，升级即丢；脚本自动探测当前目录、缺文件自动创建、保留本地项、幂等。*

### 6. 按能力策略校验七端（本次新增）
```powershell
& 'C:\Users\Lenovo\.agent-config\scripts\Test-ProjectionPolicy.ps1'
```
*校验三层：技能分层是否符合策略（core 必齐、扩展集按端）、规则面是否存在、MCP 能力组是否覆盖。只有 `FAIL` / `DRIFT` 才是问题；`UNRESOLVED` 表示该端确实没有这个原生面。*

---

## 六、改了配置之后怎么维护

| 修改内容 | 对应路径 | 生效方式 |
|---|---|---|
| **习惯 / 称呼 / 交付门禁** | `C:\Users\Lenovo\.agent-config\rules\*.md` | 修改后，各端新会话中自然生效（各端均已吸收微内核约定） |
| **新增 / 更新 Skill** | `C:\Users\Lenovo\.skillshub\<skill>\` | 改真源即对所有已挂接端生效；需要在新端出现时运行 `Sync-AgentSkill.ps1 -Agent <端> -SkillName <name>` 挂接 |
| **新增通用 MCP** | 各端原生配置文件 | 分别写入各端原生配置，在 `registry.json` 的 `commonMcpIds` 中登记，运行 `Test-AgentPlatform.ps1` 审计 |
| **学术论文 / 专项排错** | 独立 Skill 或 `references/` 知识库 | 按需触发对应 Skill（如 `chinese-thesis-workbench`），不占用常驻上下文 |

---

## 七、与 skills-hub 桌面端的关系

| 设施 | 角色与说明 |
|---|---|
| **skills-hub (GUI)** | 用于搜索、浏览、下载 GitHub 开源技能的桌面可视化客户端。 |
| **共享技能真源** | `C:\Users\Lenovo\.skillshub`（615 个含 SKILL.md 的技能），作为本机所有 Agent 的**唯一权威真源**。 |
| **推荐配置** | skills-hub 客户端中的 Central Repo / 本地库路径建议直接指向 `C:\Users\Lenovo\.skillshub`。 |

---

## 八、备份与防呆机制

1. **历史遗留规则备份**：
   原 1392 行的 Claude 规则已完整归档在：  
   `C:\Users\Lenovo\.claude\CLAUDE.md.legacy-backup`（64 KB，包含全部历史踩坑日记，随时可回溯查阅）。
2. **离线排错知识库**：
   Git 9418 端口错误解决法、GitHub Token 凭证助手配置等，归档至：  
   `C:\Users\Lenovo\.agent-config\references\git-troubleshooting.md`。
3. **安全操作边界**：
   禁止运行旧的 `sync-all.sh` 脚本；写入配置前先查看状态与 diff。

---

## 九、WorkBuddy 双端接入（AI 端 + 国内版，2026-10-20）

WorkBuddy 有**两套互不相通的客户端与账号体系**，配置根也不同，必须分开登记：

| 端 | 可执行文件 | 配置根 | 账号 |
|---|---|---|---|
| WorkBuddy AI | `E:\workbuddy\WorkBuddyAI\WorkBuddyAI.exe`（5.8.4） | `C:\Users\Lenovo\.workbuddy-ai` | shihanye0 |
| WorkBuddy 国内版 | `E:\workbuddy\WorkBuddy.exe`（37.10.3-42） | `C:\Users\Lenovo\.workbuddy` | 枕风宿雪（UIN 330106394748） |

两端投影内容一致（各自独立落地）：

| 项目 | 路径（以 `~` 代指对应配置根） | 说明 |
|---|---|---|
| 技能投影 | `~/skills` | 11 个 Junction 指向 `.skillshub`，两端同一精选集 |
| 规则 | `~/AGENTS.md` | 微内核 7 模块的浓缩投影 + 真源索引 |
| 常驻记忆 | `~/user-<uid>-personal/MEMORY.md` | 称呼/语言/环境/交付门禁的极简版，每会话自动加载 |
| MCP | `~/mcp.json` | 15 个 `commonMcpIds` 全量导入，JSON 结构同 Claude Code |
| UI 语言 | `storage/user-<uid>-personal/scoped/<id>/preferences.json` | `language: zh-CN`；**不在** `settings.json` 里 |

```powershell
# 挂接/解挂（已支持 workbuddy 与 workbuddyCn 两个目标）
& 'C:\Users\Lenovo\.agent-config\scripts\Sync-AgentSkill.ps1' -Agent workbuddyCn -SkillName archify -WhatIf
& 'C:\Users\Lenovo\.agent-config\scripts\Sync-AgentSkill.ps1' -Agent workbuddyCn -SkillName archify

# 状态与审计已自动覆盖两端
& 'C:\Users\Lenovo\.agent-config\scripts\Get-AgentPlatformStatus.ps1'
& 'C:\Users\Lenovo\.agent-config\scripts\Test-AgentPlatform.ps1'
```

**注意**：`registry.json` 的 `agents.workbuddy` 与 `agents.workbuddyCn` 均已登记，`Sync-AgentSkill.ps1` 的 `ValidateSet` 已扩到七端。两端**不可共享**的东西：连接器授权（加密存储、绑账号）、插件缓存（5.8.3 vs 5.8.4 构建版本不同）、会话与积分。

---

## 十、DSH 端接入（2026-10-20 登记）

DeepSeek Harness Desktop，30 个 Junction 至 `~/.dsh/skills`，引导技能已就位。

| 项目 | 路径 | 说明 |
|---|---|---|
| 技能投影 | `~/.dsh/skills` | 30 个 Junction，0 断链 |
| 规则 | `~/.dsh/AGENTS.md` | 原生用户全局指令文件（`$DSH_HOME/AGENTS.md`，官方包 `dsh-agent-instructions`），其后读 `~/.agents/AGENTS.md`。**2026-10-21 更正**：此前记为「无规则文件」有误 |
| MCP | `~/.dsh/storages/mcp_connector.json` | `connector-store` 格式，只统计 `tables.connections` 中 `enabled != false` 的连接；**2026-10-21 补 8 条并启用后为 9/15**（剩余 6 条为原有 disabled：memory / context7 / codebase-memory / drawio / rea / cad） |
| 插件 | `~/.dsh/profiles/desktop/package.json` | 16 个 profile bundle |

> 行结构（补连接时照抄）：`key` / `connectorId: "__custom__"` / `kind: manual` / `name` / `transport` / `command` / `args` / `env` / `cwd` / `serverName` / `headers` / `enabled` / `createdAt` / `updatedAt`。写之前先备份，且确认 DSH 未运行——它是应用私有存储，运行中写可能被内存状态覆盖。

```powershell
& 'C:\Users\Lenovo\.agent-config\scripts\Sync-AgentSkill.ps1' -Agent dsh -SkillName archify
```

---

## 十一、Qoder 端接入（2026-10-20 登记）

Qoder（CodeGeeX 内核）。**`~/.qoder` 是符号链接**，真实位置 `E:\Program Files\.qoder`——所有路径都在 E 盘 Program Files 下，这是它与其他端的最大差异。

| 项目 | 路径 | 说明 |
|---|---|---|
| 技能投影 | `E:\Program Files\.qoder\skills` | **387 个 Junction**，0 副本、0 断链（补挂 `agent-platform-sync` + 7 个精选集技能，11 精选集已齐） |
| 规则 | `~/.qoder/AGENTS.md` | 官方默认上下文文件名即 `AGENTS.md`；另有用户级规则目录 `~/.qoder/rules/**/*.md`（frontmatter `trigger` / `alwaysApply` / `paths`）。**2026-10-21 更正** |
| MCP | `...\extensions\.184c6178-...\dist\agent\configs\user_mcp_config.json` | 15 个服务已写入。**路径含扩展版本哈希，Qoder 升级会丢** |
| 插件 | `E:\Program Files\.qoder\settings.json` | hooks + enabledPlugins |

```powershell
& 'C:\Users\Lenovo\.agent-config\scripts\Sync-AgentSkill.ps1' -Agent qoder -SkillName archify
```

---

## 十二、已知漂移与待办（对抗式审查，2026-10-20 首轮 / 2026-10-21 复核）

### 已确认并修复

| # | 结论 | 证据 | 处置 |
|---|---|---|---|
| 1 | **Antigravity 2.0 读的是 `~/.gemini/config/skills`**，不是 `~/.gemini/antigravity/skills` | `agy mcp list` 输出 15 个服务，与 `~/.gemini/config/mcp_config.json` 完全一致；旧根 `~/.gemini/antigravity/mcp_config.json` 是 **0 字节**空文件，CLI 不可能从那里读到 15 个 | 新根从 7 个补到 **11 个 Junction + 1 个本地**，与其他端精选集对齐 |
| 2 | 首轮把 Claude 的 `research` 判成"重复副本"，**判错了** | Claude 版 `research/` 是 1.4 MB / 64 文件的**容器**（下挂 arxiv、blogwatcher、llm-wiki、polymarket、research-paper-writing、web-perception-toolkit，无顶层 `SKILL.md`）；hub 版 `research` 是 903 B 的单技能。同名不同物 | **不做任何转换**，保留原状；若日后要统一，先改名再链接 |
| 3 | `Get-AgentPlatformStatus.ps1` 把迁移标记 JSON 当成"本地技能" | 修复前 workbuddy/workbuddyCn 显示 `2 local/native`，修复后 `0` | 已加 `-Directory` |
| 4 | `Test-AgentPlatform.ps1` 的 `PluginInventory` 只认 3 端，其余端"没有行"＝没检查 | 修复后 workbuddy / workbuddyCn / qoder 各多出一行插件统计（6 条目/端） | 已按 `enabledPlugins` 通用化，并对 `pluginConfig: null` 加空值保护 |

### 仍待处理

| # | 问题 | 级别 | 处置 |
|---|---|---|---|
| 5 | Qoder 的 MCP 配置写在**版本锁定的扩展目录**里（`extensions\.184c6178-...`），Qoder 或扩展一升级即丢 | 高→已缓解 | 已提供 `Repair-QoderMcp.ps1`（自动探测当前哈希目录、缺文件自动创建、保留本地项、幂等，三条路径实测通过）；升级后跑一条命令即可 |
| 6 | ~~Qoder hook 路径少一层目录~~ **误判，已撤回**：把 10 条 `-EncodedCommand` 全部 base64 解码后，路径是 `E:/clawd-on-desk-main/clawd-on-desk-main/hooks/qoder-hook.js`，脚本存在，10/10 全部命中 | 已撤回 | 无需改动；教训是不要对着 base64 密文肉眼判断路径 |
| 7 | Qoder 内置 `mcp_config.json` 的 3 个 `python -m codegeex_mcp_tools.*` 服务**必然启动失败**：包是 src-layout 源码（0.1.5），从未 pip 安装，`python -m codegeex_mcp_tools.frontend` 实测 `ModuleNotFoundError` | 中→已解决 | 已移除这 3 条，备份 `mcp_config.json.bak-20261021`；若要恢复，先把包装进独立环境再补回 |
| 8 | ~~两个孤儿技能根~~ **已于 2026-10-21 移除**：`~/.gemini/skills`（379 个 Junction，本机已无 gemini CLI）与 `~/.gemini/antigravity/skills`（616 个整目录 Junction，2.0 已不读） | 中→已解决 | 删除前确认无配置引用、无进程占用；恢复清单 `.agent-config\backups\orphan-skills-20261021.json`（380 条）；`.skillshub` 删除前后字节级一致（615 目录 / 33805 文件 / 1,683,356,412 字节） |
| 9 | Claude 的 89 个本地目录里有 **30 个没有 `SKILL.md`**，是容器而非技能，`89 local/native` 这个数字虚高 | 低→已解决 | 状态脚本改为按 `SKILL.md` 分流：现显示 `59 local/native (+30 container dirs without SKILL.md)` |
| 10 | 国内版缺 AI 端那 8 个市场插件（构建版本不同，不能拷缓存） | 低 | 在国内版插件市场安装 |
| 11 | DSH 只覆盖 5/15 通用 MCP（审计口径 = `enabled != false`） | 低→已改善 | 已补 8 条连接并启用（playwright / antv-chart / exa / tavily / firecrawl / github / n8n / zai-mcp-server）→ **9/15**；剩余 6 条是原有 `enabled:false`（memory / context7 / codebase-memory / drawio / rea / cad），未擅自改动，需要时在 DSH 面板开启。备份 `mcp_connector.json.bak-20261021` |
| 12 | `agy.exe` 会在执行命令时**自动更新自身**（本次 `agy --help` 触发升级，留下 `agy.exe.<ts>.old`），CLI 升级可能改动配置路径 | 低 | 升级后重跑审计 |
| 13 | **"11 精选集"在各端并不齐**（此前只比总数没比成员）：Qoder 缺 7 个（anatomy / cad / cdp-host-browser-automation / dfm / engineering-drawing / reverse-engineer-anything / urdf），DSH 缺 3 个（agent-browser / chinese-thesis-workbench / computer-use-agents） | 中→已解决 | 已逐端补齐：Qoder 380→**387**、DSH 27→**30**；现七端精选集均 **11/11** |
| 14 | **DSH 的 MCP 曾全部掉线**：15 条连接一度全 `enabled:false`（DSH 自检 `connectionState=disabled`），指南记的 9/15 失效 | 高→已修复 | 判定为 DSH 运行中私有存储被重写。改用**原生 `mcp_connector_set_enabled` 接口**（不再手改 JSON）恢复 9 条；回滚快照 `snapshot-1792559606789-6a6ee985` |
| 15 | 指南第二章只列 4 条规则模块，实际 `rules\` 有 **7 条**（漏 document-authorship / powershell-version / presentation-layout-contracts） | 低→已修复 | 已按实际补全 |
| 16 | **DSH 与 Qoder 被误记为「无原生规则面」**：DSH 官方包 `dsh-agent-instructions` 与 Qoder 官方文档均证明其原生读 `AGENTS.md` | 高→已修复 | 已新增 `~/.dsh/AGENTS.md` 与 `~/.qoder/AGENTS.md`（微内核投影）；registry 由 `null` 改为实际路径，审计 `RulesProjection` 转 PASS |
| 17 | **WorkBuddy 官方全局指令文件名是 `CODEBUDDY.md`**，而本机只有 `AGENTS.md`（官方对 AGENTS.md 是否解析未表态） | 中→已修复 | 已在两处配置根**新增 `CODEBUDDY.md`**（与 `AGENTS.md` 同源同内容），任一机制命中即生效 |
| 18 | Qoder 387 个 Junction 与其他端 11~30 差 35 倍 | 低→已定性 | 判为**定位差异**而非漂移：Qoder 作全库检索端，核心 11/11 齐备，已写入 projection 策略 |

---

## 十三、升级/换版后的恢复清单（2026-10-21）

Qoder、Antigravity、WorkBuddy 都会在升级时改动配置路径，**升级后按顺序跑这四步**：

### 1. Qoder 升级 → 重建 MCP（必须）

Qoder 的用户级 MCP 只存在 `extensions\<版本哈希>\dist\agent\configs\user_mcp_config.json`，升级换哈希即丢。用脚本重建：

```powershell
# 预演
& 'C:\Users\Lenovo\.agent-config\scripts\Repair-QoderMcp.ps1' -WhatIf
# 实跑（自动探测当前扩展目录；文件不存在会自动创建；保留你手动加的本地服务）
& 'C:\Users\Lenovo\.agent-config\scripts\Repair-QoderMcp.ps1'
```

脚本三条路径均已实测：全新扩展目录（创建 15 个）、部分配置（补 14 改 1、保留本地项、自动备份）、已同步（幂等不写）。

### 2. WorkBuddy 国内版 → 补 8 个市场插件（需手动点）

国内版是 5.8.3 构建，缺 AI 端那 8 个插件，**不能拷缓存**，只能在客户端里装：

| 插件 | 来源 |
|---|---|
| `sheetagent@workbuddy-builtin` | 内置市场 |
| `tencent-pptx@workbuddy-builtin` | 内置市场 |
| `tencent-docx@workbuddy-builtin` | 内置市场 |
| `document-skills@cb_teams_marketplace` | 团队市场 |
| `finance-data@cb_teams_marketplace` | 团队市场 |
| `agent-browser@codebuddy-plugins-official` | 官方市场 |
| `playwright-cli@codebuddy-plugins-official` | 官方市场 |
| `find-skills@codebuddy-plugins-official` | 官方市场 |

入口：客户端左下角 `+` → 插件/连接器 → 搜索插件名安装。装完用下面命令核对差集（输出为空即齐了）：

```powershell
$ai = (Get-Content 'C:\Users\Lenovo\.workbuddy-ai\settings.json' -Raw | ConvertFrom-Json).enabledPlugins.PSObject.Properties.Name
$cn = (Get-Content 'C:\Users\Lenovo\.workbuddy\settings.json' -Raw | ConvertFrom-Json).enabledPlugins.PSObject.Properties.Name
$ai | Where-Object { $_ -notin $cn } | Sort-Object
```

### 3. Antigravity / agy 升级 → 重跑审计

`agy.exe` 会自行升级（执行任何命令都可能触发，留下 `agy.exe.<时间戳>.old`）。升级后确认技能根仍是 `~/.gemini/config/skills`，并重跑审计：

```powershell
& 'C:\Users\Lenovo\.agent-config\scripts\Test-AgentPlatform.ps1'
```

### 4. 每次升级后的统一验收

```powershell
& 'C:\Users\Lenovo\.agent-config\scripts\Get-AgentPlatformStatus.ps1'
& 'C:\Users\Lenovo\.agent-config\scripts\Test-AgentPlatform.ps1'
& 'C:\Users\Lenovo\.agent-config\scripts\Test-ProjectionPolicy.ps1'
```

判定标准：**`FAIL` 才是故障**；`UNRESOLVED` 表示该端没有这个原生表面（Antigravity 无插件配置；DSH/Qoder 的规则文件本轮已补齐），属预期。

---

## 十四、外部依据与调研结论（2026-10-21）

> 结论分级：`FACT` 有官方来源 / `INFERENCE` 由来源推得 / `UNRESOLVED` 无可靠来源。

### 14.1 两个事实标准 + 一个「没有标准」

| 资产 | 标准与治理 | 对本机的含义 |
|---|---|---|
| 指令文件 | **AGENTS.md**：6 万+ 项目使用，Linux Foundation 下 Agentic AI Foundation 托管（https://agents.md/ ） | Codex 原生 owner；DSH、Qoder 原生读取；Claude Code v2.1.277+ 也读，但**通道语义不同**（hooks 不触发、`--add-dir` 不加载） |
| 技能 | **Agent Skills / SKILL.md**：官方 Showcase 46 个客户端（https://agentskills.io/ ） | 规范**要求同时扫描客户端私有目录与 `.agents/skills/` 跨端目录**——标准本身不主张「只留一份」 |
| MCP | 官方只有**元数据** registry（https://modelcontextprotocol.io/registry/about ） | 客户端配置格式至少 18 种，**无统一标准**，必须逐端编译 |

### 14.2 本轮更正的三个事实（对应第十二章 16/17 条）

| 端 | 官方依据 | 落点 |
|---|---|---|
| **DSH** | 官方包 `@deepseek-ai/dsh-agent-instructions`：候选 `AGENTS.md` / `CLAUDE.md`，用户全局为 `$DSH_HOME/AGENTS.md` → `$DSH_AGENTS_HOME/AGENTS.md`，项目链按 `.git` 自根到 cwd；默认字节预算 65536；不支持 `.claude/rules/` 与 `@path` 导入 | 新增 `~/.dsh/AGENTS.md` |
| **Qoder** | 官方文档：`AGENTS.md` 是默认上下文文件名；用户级 `~/.qoder/AGENTS.md`，用户规则 `~/.qoder/rules/**/*.md`（`trigger` / `alwaysApply` / `paths`）；技能同名时**用户级覆盖项目级** | 新增 `~/.qoder/AGENTS.md` |
| **WorkBuddy / CodeBuddy** | 官方命名的全局指令文件是 `CODEBUDDY.md`（`~/.codebuddy/CODEBUDDY.md`），支持 `@path` 导入与 `${VAR}` 插值；AGENTS.md 是否解析官方未表态 | 两处配置根新增 `CODEBUDDY.md` |

### 14.3 为什么不用现成同步器

| 工具 | ★ | 结论 |
|---|---|---|
| [ruler](https://github.com/intellectronica/ruler) | 2.9k | 逐端四列表建模能力差异，但自述 Beta；端能力位不可用户自定义 |
| [rulesync](https://github.com/dyoshikawa/rulesync) | 1.5k | 覆盖最广，但投影语义最「平」，难表达「某端无此概念」 |
| [dotagents](https://github.com/getsentry/dotagents) | 254 | 以 symlink 为中心，Windows 上最脆 |
| [amtiYo/agents](https://github.com/amtiYo/agents) | 102 | 18 种 MCP 格式逐端生成；skills 三态 native/bridge/— |
| [spxrogers/agentsync](https://github.com/spxrogers/agentsync) | 37 | 唯一把「完整 / 有损但上报 / 显式跳过绝不静默」三态产品化 |

**结论（INFERENCE）**：没有一个工具同时满足「七端 + Windows + 保留原生差异」，且社区共识集中在**内容质量**而非工具统一。本机保留自建的薄投影层（真源 + 能力矩阵 + NTFS Junction + 原生格式隔离），把上述工具作为参考实现。

### 14.4 已验证与仍待验证

- **已验证（FACT）**：七端技能分层、MCP 能力组、规则文件存在性由 `Test-ProjectionPolicy.ps1` 只读校验通过；DSH MCP 经其原生接口恢复至 9/15。
- **仍待验证（UNRESOLVED）**：WorkBuddy 是否也解析 `AGENTS.md`（官方未表态，故两文件并存）；Qoder 桌面端是否读取配置根的 `AGENTS.md`（官方文档主要描述 CLI，Desktop 仅确认 rules frontmatter 兼容）；Qoder MCP 是否支持 `${VAR}` 插值。

#agent-hub #windows11 #skills #mcp #跨agent #配置同步 #agent-config
