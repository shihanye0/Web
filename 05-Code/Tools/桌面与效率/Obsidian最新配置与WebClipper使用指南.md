# Obsidian 最新配置与 Web Clipper 使用指南 (2026 版)

> 本文档记录 2026 年 Obsidian 知识库的架构升级、新特性应用以及与 AI Agent（Claude / Antigravity）的端到端自动化联动。

---

## 一、 当前核心架构与版本

* **Obsidian 核心版本**：`v1.14.4`（正式版）
* **同步引擎**：`obsidian-git`（每 5 分钟自动备份与拉取，已由 `.gitattributes` 锁定 LF 换行符，杜绝跨平台冲突）
* **数据库引擎**：**Obsidian Bases (官方原生 Core Plugin)**（取代已停用的 `dbfolder` 和传统第三方数据库）
* **AI & 自动化交互**：
  * **Obsidian CLI**：本地命令行 RPC，供 Agent 静默读写与搜索
  * **Smart Connections**：本地向量语义检索（基于 bge-micro-v2）
  * **MCP Tools / Local REST API**：外部 Coding Agent 统一桥梁

---

## 二、 2026 最新原生特性与使用技巧

### 1. 原生 Bases 动态看板与表格 (`.base`)
Bases 是 Obsidian 官方内置的关系型数据管理功能，直接基于笔记的 YAML Frontmatter（Properties），无代码、秒级渲染、双向同步。

知识库中已部署四大 Bases 视图：
1. [[00-Inbox/inbox.base|收件箱待办看板]]：按 `note.processed` 分组，直观查看哪些素材尚未处理。
2. [[01-Projects/projects.base|项目进度看板]]：按 `note.status` 分组，直观管理进行中、待办与已完成项目。
3. [[02-Papers/papers.base|论文库列表]]：结构化整理阅读过的论文、发表日期与作者。
4. [[03-Knowledge/knowledge.base|概念生命周期看板]]：按 `seed → growing → mature → evergreen` 视觉化追踪概念的成长阶段。

### 2. 外部 Markdown 文件直接编辑 (1.14 新增)
系统中的任意 `.md`、`.canvas` 或 `.base` 文件，现在支持右键“使用 Obsidian 打开”。无需先将文件拷贝进 Vault，即可享有完整的实时预览和 Markdown 编辑能力。

### 3. 原生 6 色高亮标记与图片原地缩放
* **多色高亮**：使用原生 `==高亮文本==` 语法，点击色块即可切换 6 种官方高亮色。
* **图片缩放**：在实时预览（Live Preview）中，鼠标悬停图片直接拖拽右下角手柄调整显示尺寸，无需手动键入 `|300` 像素参数。

---

## 三、 官方 Web Clipper（网页剪藏）自动化配置

官方 Web Clipper 是目前输入端最高效的工具，能够将网络文章与学术论文一键转化为符合知识库规范的 Markdown。

### 1. 安装插件
在 Chrome、Edge、Firefox 或 Safari 商店搜索并安装 **Obsidian Web Clipper**。

### 2. 导入预设模板
在 Web Clipper 的设置（Settings）→ **Templates** 中，点击 **Import**，分别导入知识库中的两个预配置 JSON 文件：
1. `07-Templates/web-clipper-inbox.json`（通用网页与技术文章剪藏）
2. `07-Templates/web-clipper-paper.json`（arXiv、Google Scholar 论文剪藏）

### 3. 剪藏与知识库流转（全闭环流程）

```
[浏览器浏览文章/论文]
        │
        ▼ (点击 Web Clipper 扩展图标)
[自动解析 Schema / 提取正文，生成 Frontmatter: processed: false]
        │
        ▼ (自动存入知识库)
[00-Inbox/ 目录]
        │
        ▼ (在终端或聊天中对 Agent 说: "处理 Inbox")
[Agent 读取 cloud.md 增量规则，提炼核心概念，关联已有知识，标记 processed: true]
        │
        ▼
[03-Knowledge/ 与 02-Papers/ 自动沉淀新资产，Bases 看板实时同步刷新]
```

---

## 四、 插件瘦身与性能维护记录

为了保证桌面端与移动端的丝滑体验，已清理以下历史过渡期组件：
* ❌ **停用 `table-editor-obsidian`**：已被 1.5+ 原生所见即所得表格全面取代。
* ❌ **停用 `obsidian-db-folder`**：库中无依赖，功能由原生 Bases 完美接管。
* ❌ **停用 `remotely-save`**：避免与 `obsidian-git` 双引擎并发运行产生竞态冲突。

---

*创建时间：2026-10-14*
