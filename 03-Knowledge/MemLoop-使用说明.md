# MemLoop 使用说明

## 跨终端跨智能体记忆系统

**每次打开新终端，在任何电脑上，用任何智能体——它都记得你做过的一切。**

不再重复解释。不再丢失上下文。一个文件。一个循环。无限记忆。

---

## 目录

1. 简介
2. 系统要求
3. 快速开始
4. 详细安装步骤
5. 使用方法
6. 跨设备使用
7. 跨智能体使用
8. 自动同步配置
9. 记忆文件结构
10. 常见问题
11. 最佳实践
12. 故障排除

---

## 简介

MemLoop 是一个跨终端、跨智能体的记忆系统，通过 Git 实现记忆的持久化和同步。它解决了一个核心问题：**每次开新会话都要重新解释我在做什么**。

### 核心特性

- **跨终端**：任何电脑、任何终端都能访问同一份记忆
- **跨智能体**：Claude Code、Codex、Hermes 等任何 AI 都能使用
- **自动同步**：CLI 模式下 AI 自动拉取和推送记忆
- **版本控制**：Git 版本历史，可回滚任何修改
- **零配置**：3 分钟即可完成设置

### 工作原理

任何机器 -> git pull -> 启动 AI -> AI 读取记忆 -> 工作 -> AI 更新记忆 -> git push

下一台机器 -> git pull -> AI 读取最新记忆 -> 继续工作 -> push

任何智能体 -> git pull -> 读取同一份记忆 -> 不同模型，相同记忆

---

## 系统要求

### 必需

- **Git**：版本 2.0 或更高
- **AI 智能体**：支持 CLI/终端访问的 AI（Claude Code CLI、Codex Terminal 等）
- **GitHub 账户**：用于创建私有仓库
- **网络连接**：用于 Git 同步

### 平台支持

| 平台 | 支持状态 | 说明 |
|------|----------|------|
| Windows | 完全支持 | 推荐使用 Git for Windows |
| macOS | 完全支持 | 使用 Homebrew 安装 Git |
| Linux | 完全支持 | 使用包管理器安装 Git |

### 智能体支持

| 智能体 | 支持状态 | 自动同步 | 说明 |
|--------|----------|----------|------|
| Claude Code CLI | 完全支持 | 自动 | 推荐使用 |
| Codex Terminal | 完全支持 | 自动 | 推荐使用 |
| Hermes CLI | 完全支持 | 自动 | 推荐使用 |
| Claude Desktop | 部分支持 | 手动 | 沙盒限制，需手动同步 |

---

## 快速开始

### 3 分钟设置

#### 1. 创建 GitHub 私有仓库

1. 打开 https://github.com/new
2. 仓库名：session-context
3. 选择 Private（私有）
4. 点击 "Create repository"

#### 2. 创建 GitHub Personal Access Token

1. 打开 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 repo 权限
4. 复制生成的 token

#### 3. 克隆仓库并配置

克隆仓库：
```
git clone https://github.com/YOUR_USERNAME/session-context.git
cd session-context
```

配置 Git 凭证：
```
git config --global credential.helper store
echo "YOUR_USERNAME:YOUR_TOKEN" > ~/.git-credentials
```

初始化记忆文件：
```
echo "# Session Context" > session-context.md
git add .
git commit -m "初始化 MemLoop"
git push origin main
```

#### 4. 开始使用

```
git pull
claude  # 或 codex
```

---

## 详细安装步骤

### Windows 安装

#### 1. 安装 Git

```
winget install --id Git.Git -e --source winget
```

或下载安装包：https://git-scm.com/download/win

#### 2. 配置 Git

```
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
git config --global credential.helper store
```

#### 3. 创建 GitHub 仓库

1. 登录 GitHub
2. 点击右上角 "+" -> "New repository"
3. 填写 Repository name: session-context
4. 选择 Private
5. 点击 "Create repository"

#### 4. 创建 Personal Access Token

1. 打开 https://github.com/settings/tokens
2. 点击 "Generate new token" -> "Classic"
3. Note: MemLoop Token
4. Expiration: 90 days 或 No expiration
5. 勾选 repo（完整仓库访问）
6. 点击 "Generate token"
7. 立即复制 token（只显示一次）

#### 5. 克隆并配置仓库

```
git clone https://github.com/YOUR_USERNAME/session-context.git
cd session-context
echo "YOUR_USERNAME:YOUR_TOKEN" > ~/.git-credentials
git pull
```

### macOS 安装

```
brew install git
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
git config --global credential.helper osxkeychain
```

### Linux 安装

```
sudo apt update && sudo apt install git  # Ubuntu/Debian
sudo yum install git                      # CentOS/RHEL
sudo dnf install git                      # Fedora

git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
git config --global credential.helper store
```

---

## 使用方法

### 日常工作流程

#### 1. 每天开始工作前

```
cd ~/session-context
git pull origin main
# 或
./pull-memory.sh
```

#### 2. 启动 AI

```
claude  # Claude Code
codex   # Codex
hermes  # Hermes
```

#### 3. 工作结束后

```
cd ~/session-context
git add .
git commit -m "更新记忆"
git push origin main
# 或
./push-memory.sh
```

### 创建自动脚本

**pull-memory.sh:**
```bash
#!/bin/bash
echo "正在获取最新记忆..."
cd ~/session-context
git pull origin main
```

**push-memory.sh:**
```bash
#!/bin/bash
echo "正在保存记忆..."
cd ~/session-context
git add .
git commit -m "自动更新记忆 - $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
```

---

## 跨设备使用

### 在其他电脑上设置

```
git clone https://github.com/YOUR_USERNAME/session-context.git
cd session-context
echo "YOUR_USERNAME:YOUR_TOKEN" > ~/.git-credentials
git pull
claude
```

### 多设备同步流程

- 电脑 A：工作 -> git push
- 电脑 B：git pull -> 继续工作 -> git push
- 电脑 C：git pull -> 继续工作 -> git push

---

## 跨智能体使用

### Claude Code

```
cd ~/session-context && git pull && claude
```

### Codex

```
cd ~/session-context && git pull && codex
```

### Hermes Agent

```
cd ~/session-context && git pull && hermes
```

### 其他智能体

任何能读取本地文件的 AI 都可以使用 MemLoop。

---

## 自动同步配置

### Claude Code Hooks 配置

创建 `~/.claude/hooks/session-start.sh`:
```bash
#!/bin/bash
cd ~/session-context && git pull origin main
```

创建 `~/.claude/hooks/session-end.sh`:
```bash
#!/bin/bash
cd ~/session-context && git add . && git commit -m "auto" && git push
```

在 `~/.claude/hooks/hooks.json` 中添加 SessionStart 和 SessionEnd hooks。

---

## 记忆文件结构

```markdown
# Session Context

## 用户档案
- 用户名: YOUR_USERNAME
- GitHub: https://github.com/YOUR_USERNAME
- 创建日期: YYYY-MM-DD
- 使用智能体: Claude Code, Codex, Hermes Agent

## 工作偏好
- 操作系统: Windows
- 开发环境: E 盘
- 时区: UTC+8

## 已完成的工作
- YYYY-MM-DD: 工作描述

## 方法论迭代
- 方法论 1: 描述

## 阅读清单
- 待读内容

## Agent 闲聊区
（不同智能体可以在这里交流）
```

---

## 常见问题

### Q: Git 命令找不到
A: 安装 Git 后重启终端或刷新环境变量。

### Q: git push 失败
A: 检查 Token 是否正确、是否有 repo 权限、网络连接是否正常。

### Q: 如何在其他电脑使用
A: 克隆仓库 -> 配置凭证 -> git pull -> 启动 AI。

### Q: 记忆文件太大怎么办
A: 定期清理旧内容，建议保持文件 < 100KB。

### Q: AI 不会自动推送
A: 确保使用 CLI 版本（Claude Code CLI、Codex Terminal），桌面版不支持。

### Q: 如何回滚记忆
A: `git log --oneline` -> `git reset --hard COMMIT_HASH` -> `git push --force`

---

## 最佳实践

1. **每天开始**：`cd ~/session-context && git pull && claude`
2. **工作结束**：`./push-memory.sh`
3. **定期检查**：每周检查 session-context.md 大小
4. **备份重要记忆**：创建 Git 快照
5. **使用分支管理**：创建实验分支

---

## 故障排除

### 网络连接失败
- 检查网络连接
- 配置代理：`git config --global http.proxy http://proxy:port`
- 使用 SSH 替代 HTTPS

### 权限被拒绝
- 生成 SSH 密钥：`ssh-keygen -t rsa -b 4096`
- 添加到 GitHub Settings -> SSH Keys

### 合并冲突
- 手动解决冲突
- `git add . && git commit -m "解决冲突" && git push`

### Token 过期
- 生成新 Token
- 更新凭证：`echo "USER:NEW_TOKEN" > ~/.git-credentials`

---

## 更新日志

### v1.0.0 (2026-05-29)
- 初始版本
- 支持跨终端记忆同步
- 支持跨智能体使用
- 自动拉取/推送配置

---

## 许可证

MIT License

---

## 联系方式

- GitHub: https://github.com/queyue0728-sys/memloop
- Issues: https://github.com/queyue0728-sys/memloop/issues

---

**开始使用 MemLoop，让 AI 记住你的一切！**
