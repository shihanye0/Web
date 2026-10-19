---
title: DeepSeek Harness (DSH) 使用指南与桌面配置手册
date: 2026-10-19
updated: 2026-10-19
tags:
  - Agent
  - DSH
  - DeepSeek
  - Tools
  - CLI
  - 桌面应用
---

# DeepSeek Harness (DSH) 使用指南与桌面配置手册

> 本指南记录本机 DeepSeek Harness (DSH) 的架构组成、桌面版与 CLI 启动方式、后台服务维护及常见踩坑排错说明。

---

## 目录

1. [架构与环境概览](#1-架构与环境概览)
2. [如何打开 DSH（桌面启动方式）](#2-如何打开-dsh桌面启动方式)
3. [命令行 CLI 使用指南 (`dsh`)](#3-命令行-cli-使用指南-dsh)
4. [后台服务与运维命令](#4-后台服务与运维命令)
5. [核心插件与 MCP 生态矩阵](#5-核心插件与-mcp-生态矩阵)
6. [常见问题与踩坑记录 (Troubleshooting)](#6-常见问题与踩坑记录-troubleshooting)

---

## 1. 架构与环境概览

本机 DSH 采用 **双形态并存** 架构，兼顾个性化定制体验与命令行生产力：

| 形态 | 运行基线 | 访问入口 | 特色与能力 |
|------|---------|---------|-----------|
| **DSH 桌面版 (Web App)** | 源码版（端口 `3080`，由 `systemd` 用户服务托管） | 桌面快捷方式 / `dsh-desktop` (或 `dsh-source-desktop`) / 浏览器 | 21 套定制皮肤系统（峰哥骑鲸、璃月夜等）、桌宠「鲸鱼娘」、更好的工作台侧栏、GenUI 图表渲染、ModLens 视觉通道 |
| **DSH 命令行版 (CLI)** | npm 全局包 `@deepseek-ai/dsh` (`0.2.0-rc.2`) | 终端命令 `dsh`（固定 Node v24 执行） | TUI 交互式终端、Headless 单次脚本批处理、Profile 自定义补丁装配 |

* **配置主目录**：`~/.dsh/`
* **模型 API 凭据**：`~/.dsh/.credentials.yaml`
* **Agent 全局规范**：已软链至共享宪法 `~/.agents/agents/AGENTS.md`，技能与 `~/.agents/skills` 实时对齐（81 个共享技能）。

---

## 2. 如何打开 DSH（桌面启动方式）

### 方式一：桌面快捷方式（最简单）
* 在桌面找到 **DeepSeek Harness** 图标直接双击打开。
* *快捷方式路径*：`~/Desktop/deepseek-harness.desktop`
* 对应应用列表：系统菜单 -> 开发 -> DeepSeek Harness

### 方式二：终端一键启动桌面独立窗口
如果处于终端工作流，随时输入：
```bash
dsh-source-desktop
```
> **原理**：该脚本会自动检查后台 `127.0.0.1:3080` 服务，若未启动则自动唤醒 systemd 用户服务，并以 Google Chrome 应用模式（独立无边框窗口、独立用户数据目录）调出 DSH 界面。

### 方式三：浏览器直接访问
打开任意浏览器，访问：
```text
http://127.0.0.1:3080
```
> **提示**：更新皮肤或插件后，若样式未即时更新，使用快捷键 `Ctrl + Shift + R` 强制刷新浏览器缓存。

### 方式四：手机局域网远程访问
在同一 Wi-Fi 或局域网下，终端执行：
```bash
dsh-phone-url
```
终端将输出类似 `http://192.168.x.x:8080` 的地址，手机浏览器直接打开即可进行远程对话。

---

## 3. 命令行 CLI 使用指南 (`dsh`)

### 3.1 路径与版本
* 可执行入口：`~/.local/bin/dsh`（通过 Shim 锁定 `Node v24.19.0`，彻底隔离与避免 Linux 系统自带 `/usr/bin/dsh` 冲突）。
* 查看当前安装版本：
  ```bash
  dsh -V
  # 输出: 0.2.0-rc.2
  ```

### 3.2 常用命令速查

| 操作 | 对应命令 | 说明 |
|------|---------|------|
| **启动终端 TUI** | `dsh --profile cc-tui` | 类似 Claude Code / Codex 的纯终端全屏交互界面 |
| **执行单次任务** | `dsh headless "请分析当前目录的代码结构"` | 免交互，执行单轮任务并输出结果后退出 |
| **启动独立 Web** | `dsh web` | 基于官方发行版 profiles 运行 Web 服务 |
| **检查挂载树** | `dsh web --dump-config` | 打印当前 Profile 的完整插件与补丁展开配置 |
| **插件管理** | `dsh plugin --profile web <pnpm参数>` | 管理指定 Profile 的插件依赖 |

---

## 4. 后台服务与运维命令

桌面版服务由 Linux 用户级 systemd 服务托管，开机按需启动并具备自动重启机制。

### 常用服务运维命令
```bash
# 1. 检查服务运行状态
systemctl --user status dsh-source-web.service

# 2. 重启服务（修改配置、新增插件或遇到卡死时执行）
systemctl --user restart dsh-source-web.service

# 3. 停止服务
systemctl --user stop dsh-source-web.service

# 4. 实时查看后台运行日志
journalctl --user -u dsh-source-web.service -f
```

---

## 5. 核心插件与 MCP 生态矩阵

DSH 已经完整集成本机多模态及开发增强能力：

### 5.1 常驻 MCP 工具
在对话中通过原生协议无缝调用：
1. **`glmvision`**：GLM-4.6V-Flash 视觉理解服务。
2. **`codegraph`**（v1.6.2 最新版）：代码调用图与深度语义分析。
3. **`codebaseMemory`**：持久化代码知识与语义记忆。
4. **`aihot`**：实时 AI 热点与行业精选资讯检索。

### 5.2 增强 UI 与扩展插件
配置位于 `~/.dsh/profiles/web/`：
* **ModLens**：多模态看图外挂，支持在纯文本 DeepSeek 模式下直接粘贴解析图片。
* **DSH-better-sidebar**：右侧集成代码工作台（文件树预览、内嵌终端、Git 操作、嵌入式浏览器）。
* **dsh-genui**：在对话中直接渲染图表、Mermaid 架构图、数据表格及交互式 UI。
* **dsh-at-file**：输入框打 `@` 快速模糊匹配并引用工作区文件。
* **dsh-plugin-marketplace**：集成 GitHub `dsh-plugin` 社区市场，可在设置面板中一键浏览安装扩展。
* **dsh-routing-suite**：注入器与思维模式路由（`spec` 计划模式 / `react` 执行者模式 / `weak` 任务自适应）。

---

## 6. 常见问题与踩坑记录 (Troubleshooting)

### Q1: 终端输入 `dsh` 报 Distributed Shell 错误？
* **原因**：系统 `/usr/bin/dsh` 是 Linux 的 Dancer's Shell。
* **解决**：确保 `~/.local/bin` 位于 `PATH` 前列。本机已配置 `~/.local/bin/dsh` Shim 并强制指定 Node 24 运行环境。

### Q2: 启动报 `TypeError: credentials-local: the value for "refs" must be a string`？
* **原因**：DSH 凭据解析器对 [~/.dsh/.credentials.yaml](file:///home/user/.dsh/.credentials.yaml) 做了严格格式要求，必须是**顶级扁平键值对**，不能包含 `version: 1` 或 `refs:` 嵌套。
* **正确格式**：
  ```yaml
  DEEPSEEK_API_KEY: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```

### Q3: 端口 3080 被占用导致服务无法启动？
* **排查与解决**：
  ```bash
  # 查找占用端口的 PID
  ss -tlnp | grep 3080
  # 直接通过 systemd 统一重启即可接管端口
  systemctl --user restart dsh-source-web.service
  ```

### Q4: 提示插件 peerDependencies 不兼容被 skip？
* **解决**：在 DSH 0.2.0+ 中对老插件进行安全豁免：
  ```bash
  dsh plugin --profile web allow-version <插件名@版本> --dsh-version 0.2.0-rc.2 --accept-risk
  ```

---
*相关关联笔记*：
- [[05-Code/Agent-Tools/开源工具多Agent共享配置-2026-10-13|开源工具多Agent共享配置]]
- [[05-Code/Agent-Tools/Agent Assets Hub 使用指南  agent同步指南|Agent Assets Hub 使用指南]]
- [[05-Code/Agent-Tools/Claude Code 使用指南|Claude Code 使用指南]]
