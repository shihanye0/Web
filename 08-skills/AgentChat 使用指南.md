# AgentChat 使用指南

## 概述

AgentChat 是一套零成本的 Claude Code 技能套件，通过接管本地 Chrome 浏览器桥接 8 个免费网页 AI（Gemini、ChatGPT、Claude、Qwen、Kimi、MiniMax、MiMo、DeepSeek），实现免费额度用尽后自动切换、并行编排、串行深度推理管道等能力。

**核心价值**：零 API 成本，8 个免费 AI 随你用。

## 安装状态

| 平台 | 状态 | 路径 |
|------|------|------|
| Claude Code | ✅ 已安装 | `~/.claude/skills/AgentChat-*` |
| Codex | ✅ 已安装 | `~/.codex/skills/AgentChat-*` |

## 支持的免费 AI

| AI | 登录地址 | 账号要求 |
|----|---------|---------|
| Gemini | gemini.google.com | Google 账号 |
| ChatGPT | chatgpt.com | OpenAI 账号 |
| Claude | claude.ai | Anthropic 账号 |
| Qwen（通义千问） | qianwen.com | 阿里云账号 |
| Kimi | kimi.moonshot.cn | 微信/手机号 |
| MiniMax | agent.minimaxi.com | 手机号 |
| MiMo（小米） | aistudio.xiaomimimo.com | 小米账号 |
| DeepSeek | chat.deepseek.com | 微信/手机号 |

## 三个 Skill 详解

### 1. AgentChat-WebExtended（串行降级链）

**职责**：只使用一个你最喜欢的 AI，免费额度耗尽后自动切换到下一个。

**触发条件**：
- `/AgentChat-WebExtended 帮我写个 Python 脚本`
- `/AgentChat-WebExtended 根据文字生成视频`

**工作原理**：
1. 尝试使用首选 AI（如 Gemini）
2. 如果额度用尽或报错，自动切换到下一个 AI
3. 8 个 AI 依次降级，直到任务完成

**适合场景**：单个任务，希望高可用。

### 2. AgentChat-FreeSubAgent（并行编排器）

**职责**：8 路并发执行大量独立任务，每个 AI 各执行 2 个任务。

**触发条件**：
- `/AgentChat-FreeSubAgent 我有 16 个独立任务，分别让不同 AI 执行`

**工作原理**：
1. 将任务拆分成 8 组（DAG 拆解）
2. 8 个 AI 并行执行
3. 证据仲裁：对比多个 AI 的结果，选出最优

**适合场景**：大量高独立性任务（如生成 8 个脚本、8 个视频）。

### 3. Web-SubAgent-Workflow（串行 6 步管道）

**职责**：深度推理管道：规划→搜索→推理→合成→审查→修复。

**触发条件**：
- `/Web-SubAgent-Workflow 帮我设计一个高并发消息队列的架构方案`

**工作流程**：
1. **规划**：Agent 拆解任务
2. **搜索**：Kimi 搜索相关信息
3. **推理**：Gemini 深度推理
4. **合成**：Agent 整合结果
5. **审查**：ChatGPT 或 Claude 审查
6. **修复**：发现问题后自动修复

**适合场景**：需要深度推理和质量审查的复杂任务。

## 使用前必做

### 1. 登录 AI 网页

在 Chrome 中手动登录至少 2-3 个 AI（登录态保存在 Profile，只需一次）。

### 2. 启动 Chrome 调试模式

```bash
cd /home/user/github-product/AgentChat
bash scripts/start-chrome-debug.sh
```

### 3. 配置代理（中国大陆必做）

编辑 `/home/user/github-product/AgentChat/.env`：

```bash
PROXY_SERVER=http://127.0.0.1:7897  # 改成你的代理地址
```

**注意**：不能用 VLESS Reality，只能用 HTTP/SOCKS5 代理。

## 使用示例

### 基本用法

```
你：/AgentChat-WebExtended 帮我写个 Python 爬虫脚本
```

AgentChat 会：
1. 启动 Chrome，打开 Gemini/ChatGPT 等
2. 将你的任务发送给 AI
3. 如果额度用尽，自动切换到下一个 AI
4. 返回结果给你

### 并行任务

```
你：/AgentChat-FreeSubAgent 我有 8 个独立任务：任务1-任务8
```

AgentChat 会：
1. 将 8 个任务拆分成 2 组
2. 分别发给 2 个 AI 并行执行
3. 汇总结果，对比选出最优

### 深度推理

```
你：/Web-SubAgent-Workflow 帮我分析 AgentChat 项目的架构设计
```

AgentChat 会：
1. Kimi 搜索相关信息
2. Gemini 深度分析架构
3. Agent 整合分析结果
4. ChatGPT 审查方案合理性
5. 发现问题自动修复

## 常见问题

### Chrome 启动失败

```bash
# 完全重启
pkill -9 -f "start-chrome-debug.py" && pkill -9 chrome
sleep 2 && bash scripts/start-chrome-debug.sh
```

### Gemini 显示 about:blank

GFW 问题，需要配置正确的代理：

```bash
# .env 中配置
PROXY_SERVER=http://127.0.0.1:7897
```

### 报错 MODULE_NOT_FOUND

```bash
cd /home/user/github-product/AgentChat
npm install
```

## 环境诊断

```bash
# 检查 Chrome 连接
curl -s http://127.0.0.1:9222/json/list

# 检查日志
cat /tmp/chrome-debug.log
```

## 最佳实践

- **省钱**：用 AgentChat-WebExtended 做日常任务，免费额度用尽自动切换
- **并行**：用 AgentChat-FreeSubAgent 处理大量独立任务
- **深度**：用 Web-SubAgent-Workflow 做需要推理和审查的复杂任务
- **登录**：至少登录 3 个 AI，确保降级链足够长

## 文件结构

```
/home/user/github-product/AgentChat/
├── .env                    # 配置文件（Chrome 路径、代理等）
├── scripts/
│   ├── start-chrome-debug.sh  # 启动 Chrome 调试模式
│   └── setup.sh              # 环境检查
└── skills/
    ├── AgentChat-WebExtended/      # 串行降级链
    ├── AgentChat-FreeSubAgent/     # 并行编排器
    └── Web-SubAgent-Workflow/      # 串行 6 步管道
```

## 相关链接

- 原始仓库：https://github.com/ziwang-Physics/AgentChat
- 架构图：见仓库中 `1.png`
