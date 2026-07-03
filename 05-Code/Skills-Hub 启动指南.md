# Skills-Hub 启动指南

> Skills Hub 是一个跨平台桌面应用，用于集中管理 AI 编程工具的 Skills，并同步到多个工具的全局或项目级目录。支持 40+ 种 AI 工具（Claude Code、Cursor、Codex、GitHub Copilot 等）。

## 项目信息

| 项目 | 说明 |
|------|------|
| 位置 | `E:\skills-hub` |
| 技术栈 | Tauri + React + TypeScript + Rust |
| GitHub | https://github.com/qufei1993/skills-hub |
| 默认端口 | 1420 |

## 环境要求

| 依赖 | 版本要求 | 验证命令 |
|------|---------|---------|
| Node.js | 18+ | `node --version` |
| npm | 任意 | `npm --version` |
| Rust | stable | `rustc --version` |

## 启动步骤

### 1. 进入项目目录

```bash
cd E:\skills-hub
```

### 2. 启动开发模式

```bash
npm run tauri:dev
```

> 首次启动会编译 Rust 代码，需要 2-5 分钟。后续启动会使用缓存，速度更快。

### 3. 访问应用

编译完成后会自动打开桌面窗口，或手动访问 `http://localhost:1420`。

## 常用命令

| 命令 | 用途 |
|------|------|
| `npm run tauri:dev` | 启动开发模式（热更新） |
| `npm run build` | 仅构建 Web 部分 |
| `npm run tauri:build` | 构建完整桌面应用 |
| `npm run tauri:build:win:msi` | 构建 MSI 安装包 |
| `npm run tauri:build:win:exe` | 构建 NSIS 安装包 |

## 项目结构

```
E:\skills-hub\
├── src/              # React 前端代码
├── src-tauri/        # Tauri (Rust) 后端代码
├── public/           # 静态资源
├── scripts/          # 构建脚本
├── docs/             # 文档
├── package.json      # Node.js 依赖
└── vite.config.ts    # Vite 配置
```

## 核心功能

- **Explore 页面** — 浏览精选 skill 和在线搜索，一键安装同步到多个 AI 工具
- **Tags 页面** — 创建、重命名、删除自定义标签，按标签筛选 skill
- **全局/项目同步** — 将 skill 同步到所有项目或指定项目目录
- **Skill 详情** — 点击 skill 名称查看文件内容，支持 Markdown 渲染和语法高亮
- **导入来源** — 支持本地文件夹 / Git URL 导入

## 支持的 AI 工具（部分）

Claude Code、Cursor、Codex、GitHub Copilot、Windsurf、Cline、Trae、Gemini CLI、Kiro CLI 等 40+ 种。

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| Rust 命令找不到 | 重启终端，或手动添加 `C:\Users\Lenovo\.cargo\bin` 到 PATH |
| npm install 失败 | `npm cache clean --force` 后重试 |
| Tauri 编译很慢 | 首次编译正常，后续会用缓存 |
| 启动后白屏 | 检查端口 1420 是否被占用 |

---

*创建日期：2026-06-17*
*项目路径：E:\skills-hub*
