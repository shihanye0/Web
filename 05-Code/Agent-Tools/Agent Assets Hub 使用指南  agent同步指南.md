---
status: evergreen
tags:
  - agent-hub
  - ai-tools
  - skills
  - mcp
  - 跨agent
  - 配置同步
  - windows11
updated: 2026-10-20
---
# Agent Assets Hub 使用指南（Windows 11 本地版）

> 跨 Agent（Codex / Claude Code / Antigravity / WorkBuddy AI / WorkBuddy 国内版 / DSH / Qoder）共享 Skills / 规则契约 / 习惯 / MCP 的统一真源与同步管理  
> 更新时间：2026-10-20（本轮新增：WorkBuddy 国内版、DSH、Qoder 三端登记与验证）  
> 本机控制面：`C:\Users\Lenovo\.agent-config\`  
> 共享技能库真源：`C:\Users\Lenovo\.skillshub\`（615 个含 SKILL.md 的技能）

---

## 一、解决什么问题

在 Windows 11 环境下同时使用 **Codex**、**Claude Code** 与 **Antigravity（反重力）** 时：

- **技能碎片化**：Skill 各写一份或全量暴力拷贝，导致各端版本漂移、更新不同步。
- **规则冲突与上下文膨胀**：`CLAUDE.md` 堆砌上千行历史踩坑日记，浪费上万 Token 并引发“注意力稀释”与规则互斥。
- **MCP 重复配置**：各端配置文件格式不同（TOML vs JSON），手动维护极易遗漏。
- **链接不兼容**：Windows 原生不支持或易失效 POSIX Symlink，需要一套原生稳定的联接机制。

**本体系原则：资产集中维护，按端能力投影；契约统一共享，隐私与原生配置本地隔离。**

---

## 二、架构与目录结构

```text
C:\Users\Lenovo\
├── .agent-config/                 # Agent 配置控制面（非敏感中枢）
│   ├── rules/                     # 跨 Agent 共享微内核 (L0 规则，高信噪比)
│   │   ├── preferences.md         #   称呼 Boss、中文优先、Windows 11、E盘 Conda
│   │   ├── evidence-debugging.md  #   Codex 证据链(FACT/INFERENCE)、根因修复、杜绝假数据
│   │   ├── coding-verification.md #   Karpathy 准则、py_compile/tsc 物理门禁、大文件排除
│   │   └── git-safety.md          #   禁止 git add .、不自动提交、零凭据泄露
│   ├── scripts/                   # PowerShell 7 原生运维脚本
│   │   ├── Get-AgentPlatformStatus.ps1  # 状态总览（对标 hub-status）
│   │   ├── Sync-AgentSkill.ps1          # 安全挂接/解挂 Skill（对标 sync-profile，支持 -WhatIf）
│   │   └── Test-AgentPlatform.ps1       # 全端基线漂移审计（对标 hub-update 校验）
│   ├── references/                # 离线沉淀知识库（按需查阅，不占全局 System Prompt）
│   │   ├── platform-matrix.md     #   各端投影与支持能力矩阵
│   │   └── git-troubleshooting.md #   Git 9418 协议错误、凭证配置与历史大文件清理手册
│   └── registry.json              # 平台资产与 MCP 服务清单注册表
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
| **Claude Code** | **NTFS Junction**（11 个挂接）+ **89 个本地目录**（88 个为 Claude 独有、1 个 `research` 是待清理的重复副本） | 原生 `~/.claude/.mcp.json`（19 个服务） | `~/.claude/CLAUDE.md`（精炼薄壳，吸收共享微内核） | `settings.json` 启用声明 |
| **Antigravity** | 新原生根 `~/.gemini/config/skills` 仅 **7 个 Junction + 1 个本地**；旧根 `~/.gemini/antigravity/skills` 才是整目录直通 `.skillshub`（616 个）。**2.0 读新根，等于只有 7 个技能可用** | 原生 `~/.gemini/config/mcp_config.json`（15 个服务） | `~/.gemini/GEMINI.md`（吸收共享微内核） | 不适用（原生 MCP/Skills 架构） |
| **WorkBuddy AI**（`WorkBuddyAI.exe` 5.8.4） | 11 个 Junction 至 `~/.workbuddy-ai/skills` | `~/.workbuddy-ai/mcp.json`（15 个） | `~/.workbuddy-ai/AGENTS.md` + `user-<uid>-personal/MEMORY.md` | `settings.json` 的 `enabledPlugins`（16 个，含 8 个市场插件） |
| **WorkBuddy 国内版**（`WorkBuddy.exe` 37.10.3-42） | 11 个 Junction 至 `~/.workbuddy/skills`（与 AI 端同一精选集） | `~/.workbuddy/mcp.json`（15 个） | `~/.workbuddy/AGENTS.md` + `user-<uid>-personal/MEMORY.md` | 仅 8 个内置插件；AI 端那 8 个市场插件未安装（构建版本不同，必须走市场装） |
| **DSH**（DeepSeek Harness Desktop） | 27 个 Junction 至 `~/.dsh/skills` | `~/.dsh/storages/mcp_connector.json`（connector-store 格式，**5/15** 覆盖） | 无原生规则文件（行为在 profile patch 层） | 16 个 profile bundle |
| **Qoder**（CodeGeeX 内核） | **380 个 Junction** 至 `E:\Program Files\.qoder\skills`（`~/.qoder` 是符号链接） | 扩展目录内 `user_mcp_config.json`（15 个，**版本锁定路径**） | 无原生全局规则文件；`memory/MEMORY.md` 是记忆索引而非规则 | `~/.qoder/settings.json`（hooks + enabledPlugins） |

> 逐端完整字段（路径、格式、验证命令、已知缺陷）见 `C:\Users\Lenovo\.agent-config\references\platform-matrix.md`。

> **关键机制说明**：在 Windows 11 下，放弃不稳定的 POSIX Symlink 和盲目拷贝，统一采用 **NTFS Junction（目录联接）**。既保证了零文件复制冗余、修改真源全局实时生效，又保证了删除联接点绝不伤及源文件。

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

---

## 六、改了配置之后怎么维护

| 修改内容 | 对应路径 | 生效方式 |
|---|---|---|
| **习惯 / 称呼 / 交付门禁** | `C:\Users\Lenovo\.agent-config\rules\*.md` | 修改后，各端新会话中自然生效（各端均已吸收微内核约定） |
| **新增 / 更新 Skill** | `C:\Users\Lenovo\.skillshub\<skill>\` | Antigravity 立即生效；Codex / Claude 运行 `Sync-AgentSkill.ps1` 挂接 |
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

DeepSeek Harness Desktop，27 个 Junction 至 `~/.dsh/skills`，引导技能已就位。

| 项目 | 路径 | 说明 |
|---|---|---|
| 技能投影 | `~/.dsh/skills` | 27 个 Junction，0 断链 |
| 规则 | 无 | 行为在 profile patch 层，`registry` 里 `rules: null`，审计显示 `UNRESOLVED` 属预期 |
| MCP | `~/.dsh/storages/mcp_connector.json` | `connector-store` 格式，只统计 `tables.connections` 中 `enabled != false` 的连接；当前 **5/15** 覆盖（codex 系 15 个，DSH 只接了 5 个） |
| 插件 | `~/.dsh/profiles/desktop/package.json` | 16 个 profile bundle |

```powershell
& 'C:\Users\Lenovo\.agent-config\scripts\Sync-AgentSkill.ps1' -Agent dsh -SkillName archify
```

---

## 十一、Qoder 端接入（2026-10-20 登记）

Qoder（CodeGeeX 内核）。**`~/.qoder` 是符号链接**，真实位置 `E:\Program Files\.qoder`——所有路径都在 E 盘 Program Files 下，这是它与其他端的最大差异。

| 项目 | 路径 | 说明 |
|---|---|---|
| 技能投影 | `E:\Program Files\.qoder\skills` | **380 个 Junction**，0 副本、0 断链（本轮补挂了 `agent-platform-sync`） |
| 规则 | 无原生全局规则文件 | `memory\MEMORY.md` 是记忆索引（指向 `memory\*.md`），不是规则文件；`registry` 里 `rules: null` |
| MCP | `...\extensions\.184c6178-...\dist\agent\configs\user_mcp_config.json` | 15 个服务已写入。**路径含扩展版本哈希，Qoder 升级会丢** |
| 插件 | `E:\Program Files\.qoder\settings.json` | hooks + enabledPlugins |

```powershell
& 'C:\Users\Lenovo\.agent-config\scripts\Sync-AgentSkill.ps1' -Agent qoder -SkillName archify
```

---

## 十二、已知漂移与待办（对抗式审查结论，2026-10-20）

| # | 问题 | 级别 | 处置 |
|---|---|---|---|
| 1 | Antigravity 新根只有 7 个技能，旧根才是全量直通；若 2.0 只读新根，等于 615 个技能里只有 7 个可用 | 高 | 确认 2.0 实际读取根，再决定是否在新根补挂 |
| 2 | Qoder 的 MCP 配置写在**版本锁定的扩展目录**里，升级即丢 | 高 | 升级后必须重跑审计；长期方案是找官方用户级 MCP 路径 |
| 3 | Qoder `settings.json` 的 hook 指向 `E:\clawd-on-desk-main\hooks\qoder-hook.js`，实际文件在 `...\clawd-on-desk-main\clawd-on-desk-main\hooks\qoder-hook.js`，**少一层目录，hook 静默失效** | 中 | 修 clawd 侧路径或改 settings |
| 4 | Claude Code 有 89 个本地技能目录，其中 `research` 与 `.skillshub` 重名（是副本不是 Junction），会随真源更新而漂移 | 中 | 删副本 → 建 Junction |
| 5 | Qoder 内置 `mcp_config.json` 自带 3 个 `python -m codegeex_mcp_tools.*` 服务，本机禁系统 Python，预计启动即失败 | 中 | 在 Qoder 里禁用这 3 个内置服务 |
| 6 | `Get-AgentPlatformStatus.ps1` 用 `Get-ChildItem` 未加 `-Directory`，把 `.workbuddy\skills` 下两个迁移标记 JSON 算成"本地技能"（显示 2 local/native） | 低 | 脚本加 `-Directory` 过滤 |
| 7 | `Test-AgentPlatform.ps1` 的 `PluginInventory` 只认 codex / claudeCode / dsh，workbuddy 系与 qoder 没有插件行，容易误读为"全绿" | 低 | 按 `enabledPlugins` 通用化 |
| 8 | 国内版缺 AI 端那 8 个市场插件（构建版本不同，不能拷缓存） | 低 | 在国内版插件市场安装 |
| 9 | DSH 只覆盖 5/15 通用 MCP | 低 | 按需在 connector store 里补 |

---

#agent-hub #windows11 #skills #mcp #跨agent #配置同步 #agent-config
