# skills-hub 使用指南（Ubuntu 版）

> 跨平台桌面应用，集中管理 AI 编程工具的 Skills，支持 40+ 种工具

---

## 一、项目信息

| 项目 | 值 |
|------|-----|
| 项目路径 | `/home/user/github-product/skills-hub/` |
| GitHub | https://github.com/qufei1993/skills-hub |
| 技术栈 | Tauri + React + TypeScript + Rust |
| 版本 | v0.6.3 |

---

## 二、环境要求

| 依赖 | 版本 | 状态 | 验证命令 |
|------|------|------|---------|
| Node.js | 18+ | ✅ v22.19.0 | `node --version` |
| npm | 任意 | ✅ | `npm --version` |
| Rust | stable | ✅ v1.96.1 | `rustc --version` |
| Tauri CLI | 2.x | ✅ v2.11.4 | `cargo tauri --version` |

---

## 三、安装步骤

### 3.1 安装 Rust（如未安装）

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source ~/.cargo/env
```

### 3.2 安装 Tauri CLI

```bash
cargo install tauri-cli
```

### 3.3 安装前端依赖

```bash
cd /home/user/github-product/skills-hub
npm install
```

---

## 四、启动应用

### 4.1 开发模式（推荐）

```bash
cd /home/user/github-product/skills-hub
source ~/.cargo/env
npm run tauri:dev
```

> 首次启动会编译 Rust 代码，需要 5-10 分钟。后续启动会使用缓存，速度更快。

### 4.2 访问应用

编译完成后会自动打开桌面窗口，或手动访问 `http://localhost:1420`。

---

## 五、常用命令

| 命令 | 用途 |
|------|------|
| `npm run tauri:dev` | 启动开发模式（热更新） |
| `npm run build` | 仅构建 Web 部分 |
| `npm run tauri:build` | 构建完整桌面应用 |
| `npm run tauri:build:linux:deb` | 构建 DEB 安装包 |
| `npm run tauri:build:linux:appimage` | 构建 AppImage |

---

## 六、核心功能

- **Explore 页面** — 浏览精选 skill 和在线搜索，一键安装同步到多个 AI 工具
- **Tags 页面** — 创建、重命名、删除自定义标签，按标签筛选 skill
- **全局/项目同步** — 将 skill 同步到所有项目或指定项目目录
- **Skill 详情** — 点击 skill 名称查看文件内容，支持 Markdown 渲染和语法高亮
- **导入来源** — 支持本地文件夹 / Git URL 导入

---

## 七、支持的 AI 工具

Claude Code、Cursor、Codex、GitHub Copilot、Windsurf、Cline、Trae、Gemini CLI、Kiro CLI 等 40+ 种。

| 工具 | 全局 skills 目录 |
|------|-----------------|
| Claude Code | `~/.claude/skills` |
| Codex | `~/.codex/skills` |
| Cursor | `~/.cursor/skills` |
| OpenCode | `~/.config/opencode/skills` |

---

## 八、项目结构

```
/home/user/github-product/skills-hub/
├── src/              # React 前端代码
├── src-tauri/        # Tauri (Rust) 后端代码
├── package.json      # Node.js 依赖
├── Cargo.toml        # Rust 依赖
└── README.md         # 项目文档
```

---

## 九、常见问题

| 问题 | 解决方案 |
|------|---------|
| Rust 命令找不到 | `source ~/.cargo/env` |
| npm install 失败 | `npm cache clean --force` 后重试 |
| Tauri 编译很慢 | 首次编译正常，后续会用缓存 |
| 启动后白屏 | 检查端口 1420 是否被占用 |

---

## 十、本机环境信息

| 项目 | 值 |
|------|-----|
| 项目路径 | `/home/user/github-product/skills-hub/` |
| Rust 版本 | v1.96.1 |
| Tauri CLI | v2.11.4 |
| Node.js | v22.19.0 |

---

*文档更新日期：2026年7月6日*
*系统：Ubuntu 22.04*
