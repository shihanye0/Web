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
updated: 2026-09-22
---
# Agent Assets Hub 使用指南（Windows 11 本地版）

> 跨 Agent（Codex / Claude Code / Antigravity）共享 Skills / 规则契约 / 习惯 / MCP 的统一真源与同步管理  
> 更新时间：2026-09-22  
> 本机控制面：`C:\Users\Lenovo\.agent-config\`  
> 共享技能库真源：`C:\Users\Lenovo\.skillshub\`

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
└── .skillshub/                    # 共享技能库唯一真源（608+ 精选 Skills，SKILL.md 标准）
    ├── agent-platform-sync/       #   跨 Agent 同步专用引导技能
    ├── archify/                   #   架构归档技能
    ├── chinese-thesis-workbench/  #   学术论文写作与去 AI 化工作台
    └── ...                        #   其余 600+ 共享技能
```

---

## 三、各端能力投影矩阵（Windows 11 实测）

| 端 (Agent) | 共享 Skills 机制 | MCP 维护机制 | 全局规则文件 | 插件 (Plugins) |
|---|---|---|---|---|
| **Codex** | **NTFS Junction**（按需单 Skill 挂接至 `~/.agents/skills`） | 原生 `~/.codex/config.toml`（保留本地原生服务） | `~/.codex/AGENTS.md`（吸收共享微内核） | TOML 声明，本地插件缓存 |
| **Claude Code** | **NTFS Junction**（按需单 Skill 挂接至 `~/.claude/skills`） | 原生 `~/.claude/.mcp.json`（JSON 合并） | `~/.claude/CLAUDE.md`（精炼薄壳 37 行，吸收共享微内核） | `settings.json` 启用声明 |
| **Antigravity** | **全量 Direct Junction**（根目录直通 `.skillshub`，608+ 技能全量可用） | 原生 `~/.gemini/config/mcp_config.json`（JSON 合并） | `~/.gemini/GEMINI.md`（吸收共享微内核） | 不适用（原生 MCP/Skills 架构） |

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
*(注：Antigravity 整个技能目录已直通 `.skillshub`，无需手动挂接单个技能，自动全量可用)*

### 3. 运行全平台基线审计
```powershell
& 'C:\Users\Lenovo\.agent-config\scripts\Test-AgentPlatform.ps1'
```
*校验各端 rules 是否健在、10 个通用 MCP 是否全部对齐、引导技能是否正常。*

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
| **共享技能真源** | `C:\Users\Lenovo\.skillshub`（约 608 个可用技能），作为本机所有 Agent 的**唯一权威真源**。 |
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

#agent-hub #windows11 #skills #mcp #跨agent #配置同步 #agent-config
